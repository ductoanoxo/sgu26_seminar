"""Parse SQL dump files (MySQL, PostgreSQL, SQLite) into table data."""

import re
from typing import Any, Dict, List, Optional, Tuple

from .base import ColumnDef, SourceMeta

_MAX_ROWS = 10_000  # safety cap per table during parsing


# ── helpers ──────────────────────────────────────────────────────────────────

def _strip_id(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] in ('`', '"', '[') and s[-1] in ('`', '"', ']'):
        return s[1:-1]
    return s


def _safe_col(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', '_', str(name).strip()).lower()


def _parse_scalar(s: str) -> Any:
    s = s.strip()
    if not s or s.upper() == 'NULL':
        return None
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        inner = s[1:-1]
        inner = (inner
                 .replace("\\'", "'").replace('\\"', '"').replace('\\\\', '\\')
                 .replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r'))
        return inner
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


# ── split SQL text into individual statements ─────────────────────────────────

def _split_statements(sql: str) -> List[str]:
    statements: List[str] = []
    buf: List[str] = []
    in_str = False
    str_ch = ''
    i = 0
    n = len(sql)

    while i < n:
        ch = sql[i]

        if in_str:
            buf.append(ch)
            if ch == '\\':          # MySQL-style escape inside string
                i += 1
                if i < n:
                    buf.append(sql[i])
            elif ch == str_ch:
                if i + 1 < n and sql[i + 1] == str_ch:  # doubled-quote escape
                    buf.append(sql[i + 1])
                    i += 1
                else:
                    in_str = False
        else:
            if ch in ("'", '"', '`'):
                in_str = True
                str_ch = ch
                buf.append(ch)
            elif sql[i:i + 2] == '--':          # line comment
                while i < n and sql[i] != '\n':
                    i += 1
                continue
            elif ch == ';':
                stmt = ''.join(buf).strip()
                if stmt:
                    statements.append(stmt)
                buf = []
            else:
                buf.append(ch)
        i += 1

    tail = ''.join(buf).strip()
    if tail:
        statements.append(tail)
    return statements


# ── parse VALUES (...), (...), ... ────────────────────────────────────────────

def _parse_insert_rows(text: str) -> List[List[Any]]:
    """Return list of rows from the VALUES portion of an INSERT statement."""
    rows: List[List[Any]] = []
    i = 0
    n = len(text)

    while i < n:
        # advance to next '('
        while i < n and text[i] != '(':
            i += 1
        if i >= n:
            break
        i += 1  # skip '('

        row: List[Any] = []
        val: List[str] = []
        in_str = False
        str_ch = ''
        depth = 1

        while i < n and depth > 0:
            ch = text[i]
            if in_str:
                if ch == '\\' and i + 1 < n:
                    val.extend([ch, text[i + 1]])
                    i += 2
                    continue
                if ch == str_ch:
                    if i + 1 < n and text[i + 1] == str_ch:
                        val.extend([ch, ch])
                        i += 2
                        continue
                    in_str = False
                val.append(ch)
            else:
                if ch in ("'", '"'):
                    in_str = True
                    str_ch = ch
                    val.append(ch)
                elif ch == '(':
                    depth += 1
                    val.append(ch)
                elif ch == ')':
                    depth -= 1
                    if depth == 0:
                        row.append(_parse_scalar(''.join(val).strip()))
                    else:
                        val.append(ch)
                elif ch == ',' and depth == 1:
                    row.append(_parse_scalar(''.join(val).strip()))
                    val = []
                else:
                    val.append(ch)
            i += 1

        if row:
            rows.append(row)

    return rows


# ── main adapter class ────────────────────────────────────────────────────────

class SQLFileAdapter:
    """
    Parse MySQL / PostgreSQL / SQLite SQL dump files.

    Supported constructs:
    - CREATE TABLE … (…)
    - INSERT INTO table [(cols)] VALUES (…), …
    - COPY table (cols) FROM stdin; … \\.   (PostgreSQL pg_dump)
    """

    def __init__(self, file_content: bytes, filename: str):
        self._tables: Dict[str, Dict] = {}  # name -> {columns: list[str], rows: list[dict]}
        try:
            sql = file_content.decode('utf-8', errors='replace')
        except Exception:
            sql = file_content.decode('latin-1', errors='replace')
        self._parse(sql)

    # ── internal parse ────────────────────────────────────────────────────────

    def _parse(self, sql: str):
        # Remove block comments before splitting
        sql_no_block = re.sub(r'/\*.*?\*/', ' ', sql, flags=re.DOTALL)

        for stmt in _split_statements(sql_no_block):
            upper = stmt.lstrip().upper()
            if upper.startswith('CREATE TABLE'):
                self._handle_create(stmt)
            elif upper.startswith('INSERT'):
                self._handle_insert(stmt)

        # PostgreSQL COPY blocks span statement boundaries; parse from raw sql
        self._handle_copy_blocks(sql)

    # ── CREATE TABLE ─────────────────────────────────────────────────────────

    _ID = r'(?:`([^`]+)`|"([^"]+)"|(\w+))'
    _SCHEMA_PREFIX = r'(?:' + _ID + r'\s*\.\s*)?'

    def _parse_identifier(self, m, grp_offset=1) -> str:
        return m.group(grp_offset) or m.group(grp_offset + 1) or m.group(grp_offset + 2) or ''

    def _handle_create(self, stmt: str):
        pat = (
            r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?'
            + self._SCHEMA_PREFIX
            + self._ID
            + r'\s*\('
        )
        m = re.search(pat, stmt, re.IGNORECASE)
        if not m:
            return

        # The table name is in the LAST three groups of the match
        tname = m.group(4) or m.group(5) or m.group(6)
        if not tname:
            return

        paren_start = stmt.index('(', m.start())
        columns = self._extract_columns(stmt, paren_start)

        if tname not in self._tables:
            self._tables[tname] = {'columns': columns, 'rows': []}
        elif columns and not self._tables[tname]['columns']:
            self._tables[tname]['columns'] = columns

    def _extract_columns(self, stmt: str, paren_start: int) -> List[str]:
        """Return list of column names from CREATE TABLE body."""
        depth = 0
        body: List[str] = []
        for ch in stmt[paren_start:]:
            if ch == '(':
                depth += 1
                if depth > 1:
                    body.append(ch)
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    break
                body.append(ch)
            else:
                body.append(ch)

        columns: List[str] = []
        _SKIP = {
            'PRIMARY', 'UNIQUE', 'INDEX', 'KEY', 'CONSTRAINT',
            'FOREIGN', 'CHECK', 'FULLTEXT', 'SPATIAL',
        }
        for line in ''.join(body).split('\n'):
            line = line.strip().rstrip(',').strip()
            if not line:
                continue
            first_word = re.split(r'\s', line)[0].strip('`"[]').upper()
            if first_word in _SKIP:
                continue
            cm = re.match(r'`([^`]+)`|"([^"]+)"|(\w+)', line)
            if cm:
                col = cm.group(1) or cm.group(2) or cm.group(3)
                if col.upper() not in _SKIP:
                    columns.append(_safe_col(col))
        return columns

    # ── INSERT INTO ───────────────────────────────────────────────────────────

    def _handle_insert(self, stmt: str):
        pat = (
            r'INSERT\s+(?:OR\s+\w+\s+)?(?:INTO\s+)?'
            + self._SCHEMA_PREFIX
            + self._ID
            + r'(\s*\([^)]*\))?\s+VALUES\s*'
        )
        m = re.match(pat, stmt, re.IGNORECASE)
        if not m:
            return

        tname = m.group(4) or m.group(5) or m.group(6)
        col_list_raw: Optional[str] = m.group(7)
        values_text = stmt[m.end():]

        col_names: Optional[List[str]] = None
        if col_list_raw:
            col_names = [
                _safe_col(c[0] or c[1] or c[2])
                for c in re.findall(r'`([^`]+)`|"([^"]+)"|(\w+)', col_list_raw)
            ]

        if tname not in self._tables:
            self._tables[tname] = {'columns': col_names or [], 'rows': []}

        entry = self._tables[tname]
        if col_names and not entry['columns']:
            entry['columns'] = col_names

        if len(entry['rows']) >= _MAX_ROWS:
            return

        for row_vals in _parse_insert_rows(values_text):
            if len(entry['rows']) >= _MAX_ROWS:
                break
            cols = col_names or entry['columns']
            if cols:
                row = dict(zip(cols, row_vals))
            else:
                row = {f'col_{i}': v for i, v in enumerate(row_vals)}
                # Store positional keys for future rows
                if not entry['columns']:
                    entry['columns'] = list(row.keys())
            entry['rows'].append(row)

    # ── COPY … FROM stdin (PostgreSQL) ────────────────────────────────────────

    def _handle_copy_blocks(self, sql: str):
        pat = re.compile(
            r'COPY\s+' + self._SCHEMA_PREFIX + self._ID
            + r'\s*\(([^)]+)\)\s+FROM\s+stdin\s*;(.*?)\\\.',
            re.IGNORECASE | re.DOTALL,
        )
        for m in pat.finditer(sql):
            tname = m.group(4) or m.group(5) or m.group(6)
            cols_raw = m.group(7)
            data_block = m.group(8)

            col_names = [
                _safe_col(c[0] or c[1] or c[2])
                for c in re.findall(r'`([^`]+)`|"([^"]+)"|(\w+)', cols_raw)
            ]

            if tname not in self._tables:
                self._tables[tname] = {'columns': col_names, 'rows': []}
            entry = self._tables[tname]
            if col_names and not entry['columns']:
                entry['columns'] = col_names

            for line in data_block.splitlines():
                if len(entry['rows']) >= _MAX_ROWS:
                    break
                line = line.strip()
                if not line or line == '\\.':
                    continue
                parts = line.split('\t')
                row = {}
                for col, val in zip(col_names, parts):
                    if val == '\\N':
                        row[col] = None
                    else:
                        row[col] = (val
                                    .replace('\\t', '\t')
                                    .replace('\\n', '\n')
                                    .replace('\\\\', '\\'))
                entry['rows'].append(row)

    # ── public interface ──────────────────────────────────────────────────────

    def list_sources(self) -> List[SourceMeta]:
        result = []
        for name, data in self._tables.items():
            if not data['rows']:
                continue
            if data['columns']:
                cols = [ColumnDef(name=c, type='text') for c in data['columns']]
            elif data['rows']:
                cols = [ColumnDef(name=k, type='text') for k in data['rows'][0]]
            else:
                cols = []
            result.append(SourceMeta(name=name, columns=cols, estimated_rows=len(data['rows'])))
        return result

    def read_data(self, source: str, limit: int = 10_000) -> Dict[str, Any]:
        data = self._tables.get(source)
        if not data or not data['rows']:
            return {'columns': [], 'rows': []}

        rows = data['rows'][:limit]
        columns = data['columns'] if data['columns'] else (list(rows[0].keys()) if rows else [])
        return {'columns': columns, 'rows': rows}
