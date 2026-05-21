"""Connection storage using Supabase Postgres."""

import json
import logging
from contextlib import contextmanager
from typing import Any, Generator
import uuid

import psycopg2
import psycopg2.extras

from core.config import get_settings

logger = logging.getLogger(__name__)


class ConnectionStore:
    """CRUD operations for database connections."""

    def __init__(self):
        self._settings = get_settings()
        self._table_connections = "app_private.connections"
        self._table_members = "app_private.connection_members"

    @contextmanager
    def db_session(self) -> Generator:
        conn = None
        try:
            conn = psycopg2.connect(self._settings.database_url)
            yield conn
            conn.commit()
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Connection DB error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def create_connection(self, owner_id: str, params: dict[str, Any]):
        """Create a new connection and automatically add the owner as admin."""
        with self.db_session() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # 1. Insert connection
                cur.execute(
                    f"""
                    INSERT INTO {self._table_connections} 
                    (owner_id, name, db_type, host, port, database_name, username, password_enc, ssl_enabled, settings)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
                    RETURNING id, name, owner_id, db_type, host, port, database_name, username, password_enc, ssl_enabled, settings, created_at
                    """,
                    (
                        owner_id, 
                        params["name"], 
                        params.get("db_type", "postgresql"),
                        params["host"],
                        params.get("port", 5432),
                        params["database_name"],
                        params["username"],
                        params["password_enc"],
                        params.get("ssl_enabled", True),
                        json.dumps(params.get("settings", {"timeout_ms": 30000, "max_rows": 500}))
                    ),
                )
                conn_row = cur.fetchone()
                conn_id = conn_row["id"]

                # 2. Add owner as admin member
                cur.execute(
                    f"""
                    INSERT INTO {self._table_members} (connection_id, user_id, role, granted_by)
                    VALUES (%s, %s, 'admin', %s)
                    """,
                    (conn_id, owner_id, owner_id)
                )
                
                return _normalize_row(conn_row)

    def get_connection(self, connection_id: str, user_id: str):
        """Get a connection if the user has access to it."""
        with self.db_session() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"""
                    SELECT c.*, m.role
                    FROM {self._table_connections} c
                    JOIN {self._table_members} m ON c.id = m.connection_id
                    WHERE c.id = %s AND m.user_id = %s
                    """,
                    (connection_id, user_id),
                )
                row = cur.fetchone()
                return _normalize_row(row)

    def list_connections(self, user_id: str, limit: int = 50):
        """List all connections the user has access to."""
        with self.db_session() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    f"""
                    SELECT c.id, c.name, c.db_type, c.host, c.database_name, c.is_active, c.created_at, m.role
                    FROM {self._table_connections} c
                    JOIN {self._table_members} m ON c.id = m.connection_id
                    WHERE m.user_id = %s
                    ORDER BY c.created_at DESC
                    LIMIT %s
                    """,
                    (user_id, limit),
                )
                rows = cur.fetchall()
                return [_normalize_row(row) for row in rows]

    def delete_connection(self, connection_id: str, owner_id: str):
        """Delete a connection (only the owner can do this)."""
        with self.db_session() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"DELETE FROM {self._table_connections} WHERE id = %s AND owner_id = %s RETURNING id",
                    (connection_id, owner_id),
                )
                return cur.fetchone() is not None

    def update_connection(self, connection_id: str, owner_id: str, params: dict[str, Any]):
        """Update a connection (only the owner can do this)."""
        with self.db_session() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # Build dynamic SET clause
                set_parts = []
                args = []
                for key, value in params.items():
                    if key == "settings":
                        set_parts.append(f"{key} = %s::jsonb")
                        args.append(json.dumps(value))
                    else:
                        set_parts.append(f"{key} = %s")
                        args.append(value)
                
                if not set_parts:
                    return None
                
                args.extend([connection_id, owner_id])
                query = f"""
                    UPDATE {self._table_connections}
                    SET {", ".join(set_parts)}
                    WHERE id = %s AND owner_id = %s
                    RETURNING *
                """
                cur.execute(query, args)
                row = cur.fetchone()
                return _normalize_row(row)

    def add_member(self, connection_id: str, admin_id: str, target_email: str, role: str = "viewer"):
        """Add a member to a connection using their email address."""
        with self.db_session() as conn:
            with conn.cursor() as cur:
                # 1. Resolve email to user_id
                cur.execute(
                    "SELECT id FROM auth.users WHERE email = %s",
                    (target_email,)
                )
                user_row = cur.fetchone()
                if not user_row:
                    raise ValueError(f"User with email {target_email} not found")
                target_user_id = user_row[0]

                # 2. Check if admin_id is actually an admin
                cur.execute(
                    f"SELECT role FROM {self._table_members} WHERE connection_id = %s AND user_id = %s",
                    (connection_id, admin_id)
                )
                member = cur.fetchone()
                if not member or member[0] != 'admin':
                    raise PermissionError("Only connection admins can add members")

                # 3. Add or update member
                cur.execute(
                    f"""
                    INSERT INTO {self._table_members} (connection_id, user_id, role, granted_by)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (connection_id, user_id) DO UPDATE SET role = EXCLUDED.role
                    """,
                    (connection_id, target_user_id, role, admin_id)
                )
                return True

    def get_members(self, connection_id: str, admin_id: str):
        """Get list of members for a connection (requires admin)."""
        with self.db_session() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # Check admin
                cur.execute(
                    f"SELECT role FROM {self._table_members} WHERE connection_id = %s AND user_id = %s",
                    (connection_id, admin_id)
                )
                member = cur.fetchone()
                if not member or member["role"] != 'admin':
                    raise PermissionError("Only connection admins can view members")

                cur.execute(
                    f"""
                    SELECT u.email, m.role, m.created_at as granted_at
                    FROM {self._table_members} m
                    JOIN auth.users u ON m.user_id = u.id
                    WHERE m.connection_id = %s
                    ORDER BY m.created_at DESC
                    """,
                    (connection_id,)
                )
                return cur.fetchall()

    def remove_member(self, connection_id: str, admin_id: str, target_email: str):
        """Remove a member by email (requires admin)."""
        with self.db_session() as conn:
            with conn.cursor() as cur:
                # Resolve email
                cur.execute("SELECT id FROM auth.users WHERE email = %s", (target_email,))
                user_row = cur.fetchone()
                if not user_row:
                    raise ValueError(f"User with email {target_email} not found")
                target_user_id = user_row[0]

                # Prevent removing self if owner
                if target_user_id == admin_id:
                    raise PermissionError("Cannot remove yourself from the connection")

                # Check admin
                cur.execute(
                    f"SELECT role FROM {self._table_members} WHERE connection_id = %s AND user_id = %s",
                    (connection_id, admin_id)
                )
                member = cur.fetchone()
                if not member or member[0] != 'admin':
                    raise PermissionError("Only connection admins can remove members")

                cur.execute(
                    f"DELETE FROM {self._table_members} WHERE connection_id = %s AND user_id = %s",
                    (connection_id, target_user_id)
                )
                return True

def _normalize_row(row: dict | None):
    if not row:
        return row
    if "settings" in row and isinstance(row["settings"], str):
        try:
            row["settings"] = json.loads(row["settings"])
        except json.JSONDecodeError:
            row["settings"] = {}
    return row

connection_store = ConnectionStore()
