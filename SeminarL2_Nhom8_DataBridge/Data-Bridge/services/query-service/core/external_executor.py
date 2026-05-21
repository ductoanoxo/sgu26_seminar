"""Execute SQL on an external database (PostgreSQL, MySQL, SQLite)."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

_SQL_TYPES = {"postgresql", "mysql", "sqlite"}


def is_sql_type(db_type: str) -> bool:
    return db_type in _SQL_TYPES


def execute_on_external(conn_row: dict, sql: str, max_rows: int = 1000) -> dict[str, Any]:
    db_type = conn_row.get("db_type", "")
    if db_type == "postgresql":
        return _exec_postgres(conn_row, sql, max_rows)
    if db_type == "mysql":
        return _exec_mysql(conn_row, sql, max_rows)
    if db_type == "sqlite":
        return _exec_sqlite(conn_row, sql, max_rows)
    raise ValueError(f"Cannot execute SQL on db_type={db_type!r}")


def _serialize_row(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        if hasattr(v, "isoformat"):
            out[k] = v.isoformat()
        elif isinstance(v, (int, float, str, bool, type(None))):
            out[k] = v
        else:
            out[k] = str(v)
    return out


def _exec_postgres(row: dict, sql: str, max_rows: int) -> dict[str, Any]:
    import psycopg2
    import psycopg2.extras

    dsn = (
        f"host={row.get('host', 'localhost')} "
        f"port={row.get('port', 5432)} "
        f"dbname={row.get('database_name', '')} "
        f"user={row.get('username', '')} "
        f"password={row.get('password', '')}"
    )
    conn = psycopg2.connect(dsn)
    try:
        conn.set_session(readonly=True)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchmany(max_rows + 1)
            truncated = len(rows) > max_rows
            rows = rows[:max_rows]
            columns = [desc[0] for desc in cur.description] if cur.description else []
            serialized = [_serialize_row(dict(r)) for r in rows]
        return {"columns": columns, "rows": serialized, "row_count": len(serialized), "truncated": truncated}
    finally:
        conn.close()


def _exec_mysql(row: dict, sql: str, max_rows: int) -> dict[str, Any]:
    import pymysql
    import pymysql.cursors

    conn = pymysql.connect(
        host=row.get("host", "localhost"),
        port=int(row.get("port") or 3306),
        database=row.get("database_name", ""),
        user=row.get("username", ""),
        password=row.get("password", "") or "",
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchmany(max_rows + 1)
            truncated = len(rows) > max_rows
            rows = rows[:max_rows]
            columns = [desc[0] for desc in cur.description] if cur.description else []
            serialized = [_serialize_row(dict(r)) for r in rows]
        return {"columns": columns, "rows": serialized, "row_count": len(serialized), "truncated": truncated}
    finally:
        conn.close()


def _exec_sqlite(row: dict, sql: str, max_rows: int) -> dict[str, Any]:
    import sqlite3

    db_path = row.get("database_name", "") or row.get("host", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(sql)
        rows = cur.fetchmany(max_rows + 1)
        truncated = len(rows) > max_rows
        rows = rows[:max_rows]
        columns = [desc[0] for desc in cur.description] if cur.description else []
        serialized = [_serialize_row(dict(r)) for r in rows]
        return {"columns": columns, "rows": serialized, "row_count": len(serialized), "truncated": truncated}
    finally:
        conn.close()
