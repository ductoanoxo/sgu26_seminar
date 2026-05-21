import sqlite3
from typing import List, Dict, Any
from .base import BaseAdapter, ColumnDef, SourceMeta


class SQLiteAdapter(BaseAdapter):
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._conn: sqlite3.Connection | None = None

    def _connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self._file_path)
            self._conn.row_factory = sqlite3.Row

    def test_connection(self) -> bool:
        try:
            self._connect()
            self._conn.execute("SELECT 1")
            return True
        except Exception:
            return False

    def list_sources(self) -> List[SourceMeta]:
        self._connect()
        cur = self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [r[0] for r in cur.fetchall()]

        result = []
        for table_name in tables:
            cur = self._conn.execute(f"PRAGMA table_info(\"{table_name}\")")
            cols = [ColumnDef(name=r["name"], type=r["type"] or "TEXT") for r in cur.fetchall()]
            cur2 = self._conn.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            row_count = cur2.fetchone()[0]
            result.append(SourceMeta(name=table_name, columns=cols, estimated_rows=row_count))
        return result

    def read_data(self, source: str, limit: int = 10000) -> Dict[str, Any]:
        self._connect()
        cur = self._conn.execute(f'SELECT * FROM "{source}" LIMIT {limit}')
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if cur.description else []
        return {"columns": columns, "rows": [dict(r) for r in rows]}

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
