import pymysql
import pymysql.cursors
from typing import List, Dict, Any
from .base import BaseAdapter, ColumnDef, SourceMeta


class MySQLAdapter(BaseAdapter):
    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        self._params = {
            "host": host,
            "port": port or 3306,
            "db": database,
            "user": username or "root",
            "password": password or "",
            "connect_timeout": 5,
            "cursorclass": pymysql.cursors.DictCursor,
        }
        self._conn = None

    def _connect(self):
        if self._conn is None:
            self._conn = pymysql.connect(**self._params)

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
            cur.execute("SHOW TABLES")
            tables = [list(r.values())[0] for r in cur.fetchall()]

        result = []
        for table_name in tables:
            cols = self._get_columns(table_name)
            result.append(SourceMeta(name=table_name, columns=cols))
        return result

    def _get_columns(self, table_name: str) -> List[ColumnDef]:
        with self._conn.cursor() as cur:
            cur.execute(f"DESCRIBE `{table_name}`")
            return [ColumnDef(name=r["Field"], type=r["Type"]) for r in cur.fetchall()]

    def read_data(self, source: str, limit: int = 10000) -> Dict[str, Any]:
        self._connect()
        with self._conn.cursor() as cur:
            cur.execute(f"SELECT * FROM `{source}` LIMIT %s", (limit,))
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []
            return {"columns": columns, "rows": list(rows)}

    def close(self):
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None
