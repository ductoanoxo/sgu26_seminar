import psycopg2
import psycopg2.extras
from typing import List, Dict, Any, Optional
from urllib.parse import quote, unquote
from .base import BaseAdapter, ColumnDef, SourceMeta


def _normalize_uri(uri: str) -> str:
    """Auto-encode special characters (e.g. @ # ? in passwords) in a database URI."""
    proto_end = uri.find('://')
    if proto_end == -1:
        return uri
    scheme = uri[:proto_end]
    rest = uri[proto_end + 3:]

    # The last '@' separates credentials from host
    at_positions = [i for i, c in enumerate(rest) if c == '@']
    if not at_positions:
        return uri

    last_at = at_positions[-1]
    auth = rest[:last_at]
    host_path = rest[last_at + 1:]

    colon_pos = auth.find(':')
    if colon_pos == -1:
        return f"{scheme}://{quote(unquote(auth), safe='')}@{host_path}"

    raw_user = auth[:colon_pos]
    raw_pass = auth[colon_pos + 1:]

    # Decode first to avoid double-encoding, then re-encode
    user_encoded = quote(unquote(raw_user), safe='')
    pass_encoded = quote(unquote(raw_pass), safe='')

    return f"{scheme}://{user_encoded}:{pass_encoded}@{host_path}"


class PostgreSQLAdapter(BaseAdapter):
    def __init__(
        self, host: str = "localhost", port: int = 5432,
        database: str = "", username: str = "", password: str = "",
        connection_string: Optional[str] = None,
    ):
        self._connection_string = _normalize_uri(connection_string) if connection_string else None
        self._params = {
            "host": host,
            "port": port or 5432,
            "dbname": database,
            "user": username or "postgres",
            "password": password or "",
            "connect_timeout": 5,
        }
        self._conn = None

    def _connect(self):
        if self._conn is None or self._conn.closed:
            if self._connection_string:
                self._conn = psycopg2.connect(self._connection_string, connect_timeout=5)
            else:
                self._conn = psycopg2.connect(**self._params)

    def test_connection(self) -> bool:
        try:
            self._connect()
            with self._conn.cursor() as cur:
                cur.execute("SELECT 1")
            return True
        except Exception:
            return False

    def list_sources(self) -> List[SourceMeta]:
        self._connect()
        with self._conn.cursor() as cur:
            cur.execute("""
                SELECT t.table_name,
                    COALESCE(
                        (SELECT reltuples::bigint FROM pg_class
                         WHERE relname = t.table_name AND relnamespace = 'public'::regnamespace),
                        0
                    ) AS row_est
                FROM information_schema.tables t
                WHERE t.table_schema = 'public'
                    AND t.table_type = 'BASE TABLE'
                ORDER BY t.table_name
            """)
            tables = cur.fetchall()

        result = []
        for table_name, row_est in tables:
            cols = self._get_columns(table_name)
            est = max(0, int(row_est or 0))
            if est == 0:
                with self._conn.cursor() as cur:
                    try:
                        cur.execute(f'SELECT count(*) FROM (SELECT 1 FROM public."{table_name}" LIMIT 10000) sub')
                        count = cur.fetchone()[0]
                        if count == 10000:
                            est = 10000
                        else:
                            est = count
                    except Exception:
                        pass
                        
            result.append(SourceMeta(
                name=table_name,
                columns=cols,
                estimated_rows=est,
            ))
        return result

    def _get_columns(self, table_name: str) -> List[ColumnDef]:
        with self._conn.cursor() as cur:
            cur.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
                ORDER BY ordinal_position
            """, (table_name,))
            return [ColumnDef(name=r[0], type=r[1]) for r in cur.fetchall()]

    def read_data(self, source: str, limit: int = 10000) -> Dict[str, Any]:
        self._connect()
        with self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f'SELECT * FROM public."{source}" LIMIT %s', (limit,))
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []
            return {"columns": columns, "rows": [dict(r) for r in rows]}

    def close(self):
        if self._conn and not self._conn.closed:
            self._conn.close()
