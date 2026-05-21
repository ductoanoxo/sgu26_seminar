"""Manage saved database connections stored in Supabase."""

import uuid
import logging
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from typing import List, Optional, Tuple
from core.config import get_settings
from adapters.postgresql import PostgreSQLAdapter
from adapters.mysql import MySQLAdapter
from adapters.mongodb import MongoDBAdapter
from adapters.sqlite_adapter import SQLiteAdapter
from adapters.redis_adapter import RedisAdapter
from adapters.base import BaseAdapter
from schemas.connection_schemas import SavedConnection

logger = logging.getLogger(__name__)

_SQL_TYPES = {"postgresql", "mysql", "sqlite", "file"}


class ConnectionService:

    @contextmanager
    def _conn(self):
        """Open a DB connection and guarantee it is closed on exit."""
        conn = psycopg2.connect(get_settings().database_url)
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # ── Table bootstrap ──────────────────────────────────────────────────────

    def ensure_table(self):
        with self._conn() as c:
            with c.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS public.saved_connections (
                        id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_id     TEXT NOT NULL DEFAULT 'public',
                        name        VARCHAR(100) NOT NULL,
                        db_type     VARCHAR(50)  NOT NULL,
                        host        VARCHAR(255),
                        port        INTEGER,
                        database_name VARCHAR(255) DEFAULT '',
                        username    VARCHAR(255),
                        password    TEXT,
                        connection_string TEXT,
                        is_active   BOOLEAN DEFAULT false,
                        created_at  TIMESTAMP DEFAULT NOW(),
                        last_used_at TIMESTAMP
                    )
                """)
                cur.execute("""
                    DO $$ BEGIN
                        ALTER TABLE public.saved_connections
                            ADD COLUMN IF NOT EXISTS user_id TEXT NOT NULL DEFAULT 'public';
                    EXCEPTION WHEN others THEN NULL;
                    END $$;
                """)
                cur.execute("""
                    DO $$ BEGIN
                        ALTER TABLE public.saved_connections
                            ADD COLUMN IF NOT EXISTS connection_string TEXT;
                    EXCEPTION WHEN others THEN NULL;
                    END $$;
                """)
            c.commit()

    # ── CRUD ─────────────────────────────────────────────────────────────────

    def find_by_params(
        self, user_id: str, db_type: str, host: str, port: Optional[int], database_name: str
    ) -> Optional[SavedConnection]:
        """Return existing connection with same db_type/host/port/database for this user, or None."""
        self.ensure_table()
        with self._conn() as c:
            with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id,name,db_type,host,port,database_name,username,is_active,created_at,last_used_at
                    FROM public.saved_connections
                    WHERE user_id=%s AND db_type=%s AND host=%s
                      AND port IS NOT DISTINCT FROM %s AND database_name=%s
                    LIMIT 1
                """, (user_id, db_type, host or '', port, database_name or ''))
                row = cur.fetchone()
                return self._to_model(dict(row)) if row else None

    def create_file_source(
        self, user_id: str, filename: str, destination_tables: List[str],
        connection_string: Optional[str] = None,
    ) -> SavedConnection:
        """Create a single 'file' connection scoped to the tables from one import."""
        self.ensure_table()
        table_scope = ",".join(destination_tables)
        return self.create(
            user_id=user_id,
            name=filename,
            db_type='file',
            host='',
            port=None,
            database_name=table_scope,
            username=None,
            password=None,
            connection_string=connection_string,
        )

    def _find_by_name_and_type(self, user_id: str, name: str, db_type: str) -> Optional[SavedConnection]:
        with self._conn() as c:
            with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id,name,db_type,host,port,database_name,username,is_active,created_at,last_used_at
                    FROM public.saved_connections
                    WHERE user_id=%s AND db_type=%s AND name=%s
                    LIMIT 1
                """, (user_id, db_type, name))
                row = cur.fetchone()
                return self._to_model(dict(row)) if row else None

    def create(
        self, user_id: str, name: str, db_type: str, host: str, port: Optional[int],
        database_name: str, username: Optional[str], password: Optional[str],
        connection_string: Optional[str] = None,
    ) -> SavedConnection:
        self.ensure_table()
        conn_id = str(uuid.uuid4())
        with self._conn() as c:
            with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO public.saved_connections
                        (id, user_id, name, db_type, host, port, database_name, username, password, connection_string)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING id,name,db_type,host,port,database_name,username,is_active,created_at
                """, (conn_id, user_id, name, db_type, host, port, database_name or "", username, password, connection_string))
                row = dict(cur.fetchone())
            c.commit()
        return self._to_model(row)

    def list_all(self, user_id: str) -> List[SavedConnection]:
        self.ensure_table()
        with self._conn() as c:
            with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id,name,db_type,host,port,database_name,username,
                           is_active,created_at,last_used_at
                    FROM public.saved_connections
                    WHERE user_id=%s
                    ORDER BY is_active DESC, created_at DESC
                """, (user_id,))
                return [self._to_model(dict(r)) for r in cur.fetchall()]

    def delete(self, conn_id: str, user_id: str) -> bool:
        with self._conn() as c:
            with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT db_type, database_name FROM public.saved_connections WHERE id=%s AND user_id=%s",
                    (conn_id, user_id),
                )
                row = cur.fetchone()
                cur.execute("DELETE FROM public.saved_connections WHERE id=%s AND user_id=%s", (conn_id, user_id))
                ok = cur.rowcount > 0
                if ok and row and row.get("db_type") == "file":
                    table_names = [t.strip() for t in (row.get("database_name") or "").split(",") if t.strip()]
                    for table_name in table_names:
                        cur.execute('DROP TABLE IF EXISTS public."{}"'.format(table_name.replace('"', '""')))
                        cur.execute(
                            "DELETE FROM public.import_registry WHERE destination_table=%s",
                            (table_name,),
                        )
            c.commit()
        return ok

    # ── Activation ───────────────────────────────────────────────────────────

    def activate(self, conn_id: str, user_id: str) -> bool:
        with self._conn() as c:
            with c.cursor() as cur:
                # Only deactivate this user's connections
                cur.execute("UPDATE public.saved_connections SET is_active=false WHERE user_id=%s", (user_id,))
                cur.execute(
                    "UPDATE public.saved_connections SET is_active=true, last_used_at=NOW() WHERE id=%s AND user_id=%s",
                    (conn_id, user_id),
                )
                ok = cur.rowcount > 0
            c.commit()
        return ok

    def deactivate_all(self, user_id: str):
        with self._conn() as c:
            with c.cursor() as cur:
                cur.execute("UPDATE public.saved_connections SET is_active=false WHERE user_id=%s", (user_id,))
            c.commit()

    def get_active_raw(self, user_id: str) -> Optional[dict]:
        """Return full row including password (internal use only)."""
        try:
            self.ensure_table()
            with self._conn() as c:
                with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(
                        "SELECT * FROM public.saved_connections WHERE is_active=true AND user_id=%s LIMIT 1",
                        (user_id,),
                    )
                    row = cur.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"get_active_raw: {e}")
            return None

    def get_active(self, user_id: str) -> Optional[SavedConnection]:
        row = self.get_active_raw(user_id)
        return self._to_model(row) if row else None

    # ── Test ─────────────────────────────────────────────────────────────────

    def test_by_id(self, conn_id: str, user_id: str) -> Tuple[bool, str]:
        self.ensure_table()
        with self._conn() as c:
            with c.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM public.saved_connections WHERE id=%s AND user_id=%s",
                    (conn_id, user_id),
                )
                row = cur.fetchone()
        if not row:
            return False, "Connection not found"
        return self._test_row(dict(row))

    def test_params(
        self, db_type: str, host: str, port: Optional[int],
        database_name: str, username: Optional[str], password: Optional[str],
    ) -> Tuple[bool, str]:
        return self._test_row({
            "db_type": db_type, "host": host, "port": port,
            "database_name": database_name, "username": username, "password": password,
        })

    # ── Schema ───────────────────────────────────────────────────────────────

    def get_active_schema(self, user_id: str) -> Tuple[str, Optional[SavedConnection], Optional[List[dict]]]:
        """Return (schema_string, active_connection, raw_schema) for the currently active DB."""
        active_raw = self.get_active_raw(user_id)
        if not active_raw:
            return "", None, None
        active = self._to_model(active_raw)
        adapter = self._make_adapter(active_raw)
        try:
            sources = adapter.list_sources()
            raw_sources = [
                {
                    "name": s.name,
                    "estimated_rows": s.estimated_rows,
                    "columns": [{"name": c.name, "type": c.type} for c in s.columns]
                }
                for s in sources
            ]
            lines = [f"## Database Schema ({active.db_type}) — {active.name}\n"]
            for src in sources:
                lines.append(f"\n### Table: {src.name}")
                lines.append("| Column | Type |")
                lines.append("|--------|------|")
                for col in src.columns:
                    lines.append(f"| {col.name} | {col.type} |")
            schema_string = "\n".join(lines) if active.db_type in _SQL_TYPES else ""
            return schema_string, active, raw_sources
        except Exception as e:
            logger.error(f"get_active_schema: {e}")
            return "", active, None
        finally:
            adapter.close()

    def preview_table_data(self, user_id: str, table_name: str, limit: int = 10) -> dict:
        active = self.get_active(user_id)
        if not active:
            raise Exception("No active database connection.")
        active_raw = active.model_dump()
        adapter = self._make_adapter(active_raw)
        try:
            return adapter.read_data(table_name, limit)
        finally:
            adapter.close()

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _test_row(self, row: dict) -> Tuple[bool, str]:
        adapter = self._make_adapter(row)
        try:
            ok = adapter.test_connection()
            return ok, "Connection successful" if ok else "Connection failed"
        except Exception as e:
            return False, str(e)
        finally:
            adapter.close()

    def _make_adapter(self, row: dict) -> BaseAdapter:
        t = row.get("db_type", "")
        h = row.get("host", "localhost") or "localhost"
        p = row.get("port")
        db = row.get("database_name", "") or ""
        u = row.get("username") or ""
        pw = row.get("password") or ""
        cs = row.get("connection_string") or None
        if t == "postgresql": return PostgreSQLAdapter(h, p, db, u, pw, connection_string=cs)
        if t == "mysql":      return MySQLAdapter(h, p, db, u, pw)
        if t == "mongodb":    return MongoDBAdapter(h, p, db, u, pw, connection_string=cs)
        if t == "sqlite":     return SQLiteAdapter(db)
        if t == "redis":      return RedisAdapter(h, p, db, u, pw)
        if t == "file":
            settings = get_settings()
            adapter = PostgreSQLAdapter(
                host=settings.SUPABASE_DB_HOST,
                port=settings.SUPABASE_DB_PORT,
                database=settings.SUPABASE_DB_NAME,
                username=settings.SUPABASE_DB_USER,
                password=settings.SUPABASE_DB_PASSWORD
            )
            class FileAdapterWrapper(BaseAdapter):
                def __init__(self, inner, tables):
                    self.inner = inner
                    self.tables = set([x.strip() for x in tables.split(",") if x.strip()])
                def test_connection(self): return self.inner.test_connection()
                def list_sources(self):
                    return [s for s in self.inner.list_sources() if s.name in self.tables]
                def read_data(self, source, limit=10000):
                    return self.inner.read_data(source, limit)
                def close(self): return self.inner.close()
            return FileAdapterWrapper(adapter, db)
        raise ValueError(f"Unknown db_type: {t}")

    def _to_model(self, row: dict) -> SavedConnection:
        return SavedConnection(
            id=str(row["id"]),
            name=row["name"],
            db_type=row["db_type"],
            host=row.get("host"),
            port=row.get("port"),
            database_name=row.get("database_name", ""),
            username=row.get("username"),
            is_active=bool(row.get("is_active", False)),
            created_at=str(row["created_at"]) if row.get("created_at") else None,
            last_used_at=str(row["last_used_at"]) if row.get("last_used_at") else None,
        )


connection_service = ConnectionService()
