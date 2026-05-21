"""Dashboard storage using Supabase Postgres."""

import json
import logging
from contextlib import contextmanager
from typing import Any, Generator

import psycopg2
import psycopg2.extras

from core.config import get_settings

logger = logging.getLogger(__name__)


class DashboardStore:
    """CRUD operations for dashboards."""

    def __init__(self):
        self._settings = get_settings()
        self._table = "app_private.dashboards"

    @contextmanager
    def get_connection(self) -> Generator:
        conn = None
        try:
            conn = psycopg2.connect(self._settings.database_url)
            yield conn
            conn.commit()
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Dashboard DB error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def create_dashboard(self, name: str, owner_id: str, description: str | None, widgets: list[dict[str, Any]]):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"""
                    INSERT INTO {self._table} (name, owner_id, description, widgets)
                    VALUES (%s, %s, %s, %s::jsonb)
                    RETURNING id, name, owner_id, description, widgets, created_at, updated_at
                    """,
                    (name, owner_id, description, json.dumps(widgets)),
                )
                row = cur.fetchone()
                return _normalize_row(row)

    def get_dashboard(self, dashboard_id: str, owner_id: str):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"""
                    SELECT id, name, owner_id, description, widgets, created_at, updated_at
                    FROM {self._table}
                    WHERE id = %s AND owner_id = %s
                    """,
                    (dashboard_id, owner_id),
                )
                row = cur.fetchone()
                return _normalize_row(row)

    def list_dashboards(self, owner_id: str, limit: int = 20):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"""
                    SELECT id, name, owner_id, description, widgets, created_at, updated_at
                    FROM {self._table}
                    WHERE owner_id = %s
                    ORDER BY updated_at DESC
                    LIMIT %s
                    """,
                    (owner_id, limit),
                )
                rows = cur.fetchall()
                return [_normalize_row(row) for row in rows]

    def update_dashboard(self, dashboard_id: str, owner_id: str, fields: dict[str, Any]):
        if not fields:
            return self.get_dashboard(dashboard_id, owner_id)

        set_parts = []
        values: list[Any] = []
        for key, value in fields.items():
            if key == "widgets":
                set_parts.append("widgets = %s::jsonb")
                values.append(json.dumps(value))
            else:
                set_parts.append(f"{key} = %s")
                values.append(value)

        set_parts.append("updated_at = now()")
        values.append(dashboard_id)

        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"""
                    UPDATE {self._table}
                    SET {', '.join(set_parts)}
                    WHERE id = %s AND owner_id = %s
                    RETURNING id, name, owner_id, description, widgets, created_at, updated_at
                    """,
                    values + [owner_id],
                )
                row = cur.fetchone()
                return _normalize_row(row)


def _normalize_row(row: dict | None):
    if not row:
        return row
    widgets = row.get("widgets")
    if isinstance(widgets, str):
        try:
            row["widgets"] = json.loads(widgets)
        except json.JSONDecodeError:
            row["widgets"] = []
    return row


dashboard_store = DashboardStore()
