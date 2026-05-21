"""Write imported data into Supabase PostgreSQL."""

import re
import logging
import uuid
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from core.config import get_settings

logger = logging.getLogger(__name__)


def _safe_name(name: str) -> str:
    """Convert any string to a safe PostgreSQL identifier (max 63 chars)."""
    name = str(name)
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if not name or name[0].isdigit():
        name = "col_" + name
    return name[:63].lower()


def _import_table_name(source_name: str) -> str:
    """Return a unique, safe table name for one imported dataset."""
    suffix = uuid.uuid4().hex[:8]
    prefix = f"imported_{_safe_name(source_name)}"
    max_prefix_len = 63 - len(suffix) - 1
    return f"{prefix[:max_prefix_len]}_{suffix}"


def _pg_type(python_type: str) -> str:
    mapping = {
        "int64": "BIGINT",
        "int32": "INTEGER",
        "int": "BIGINT",
        "float64": "DOUBLE PRECISION",
        "float32": "REAL",
        "float": "DOUBLE PRECISION",
        "bool": "BOOLEAN",
        "object": "TEXT",
        "str": "TEXT",
        "NoneType": "TEXT",
        "datetime64": "TIMESTAMP",
    }
    for k, v in mapping.items():
        if k in python_type:
            return v
    return "TEXT"


def _serialize(value: Any) -> Any:
    """Make value safe for psycopg2 insertion."""
    if value is None:
        return None
    if isinstance(value, (int, float, bool)):
        return value
    if isinstance(value, str):
        return value
    return str(value)


class SupabaseWriter:
    def __init__(self):
        self._settings = get_settings()

    @contextmanager
    def _get_conn(self):
        """Open a DB connection and guarantee it is closed on exit."""
        conn = psycopg2.connect(self._settings.database_url)
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def ensure_registry_table(self):
        """Create import_registry table if it doesn't exist."""
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS public.import_registry (
                        id SERIAL PRIMARY KEY,
                        source_type VARCHAR(50) NOT NULL,
                        source_name VARCHAR(200) NOT NULL,
                        destination_table VARCHAR(200) NOT NULL UNIQUE,
                        columns JSONB NOT NULL,
                        row_count INTEGER DEFAULT 0,
                        imported_at TIMESTAMP DEFAULT NOW()
                    )
                """)
            conn.commit()

    def list_registry(self) -> list[dict]:
        """Return all rows from import_registry ordered by most recent."""
        try:
            with self._get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT source_type, source_name, destination_table, row_count, imported_at
                        FROM public.import_registry
                        ORDER BY imported_at DESC
                    """)
                    cols = [d[0] for d in cur.description]
                    rows = cur.fetchall()
                    return [dict(zip(cols, r)) for r in rows]
        except Exception:
            return []

    def import_data(
        self,
        source_name: str,
        source_type: str,
        columns: List[str],
        rows: List[Dict[str, Any]],
        col_types: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Create/replace table in Supabase and insert data.
        Returns destination table name.
        """
        dest_table = _import_table_name(source_name)

        if not columns:
            raise ValueError(f"No columns provided for source '{source_name}'")

        safe_cols = [_safe_name(c) for c in columns]

        # Determine column types
        types: Dict[str, str] = {}
        if col_types:
            for orig, t in col_types.items():
                types[_safe_name(orig)] = _pg_type(t)

        if rows and not col_types:
            first = rows[0]
            for orig, safe in zip(columns, safe_cols):
                v = first.get(orig)
                types[safe] = "TEXT" if v is None else _pg_type(type(v).__name__)

        # Default TEXT for any missing
        for s in safe_cols:
            types.setdefault(s, "TEXT")

        col_defs = ", ".join(f'"{c}" {types[c]}' for c in safe_cols)

        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(f'DROP TABLE IF EXISTS public."{dest_table}"')
                cur.execute(f'CREATE TABLE public."{dest_table}" ({col_defs})')

                if rows:
                    placeholders = ", ".join(["%s"] * len(safe_cols))
                    insert_sql = f'INSERT INTO public."{dest_table}" VALUES ({placeholders})'

                    batch = []
                    for row in rows:
                        vals = tuple(_serialize(row.get(orig)) for orig in columns)
                        batch.append(vals)

                    psycopg2.extras.execute_batch(cur, insert_sql, batch, page_size=500)

                # Upsert into registry
                col_info = [{"name": s, "type": types[s]} for s in safe_cols]
                cur.execute("""
                    INSERT INTO public.import_registry
                        (source_type, source_name, destination_table, columns, row_count)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (destination_table) DO UPDATE SET
                        row_count = EXCLUDED.row_count,
                        imported_at = NOW(),
                        columns = EXCLUDED.columns
                """, (
                    source_type, source_name, dest_table,
                    psycopg2.extras.Json(col_info), len(rows),
                ))

            conn.commit()

        logger.info(f"Imported {len(rows)} rows into public.\"{dest_table}\"")
        return dest_table


writer = SupabaseWriter()
