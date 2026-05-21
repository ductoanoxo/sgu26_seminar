"""Database connection management for Supabase PostgreSQL."""

import psycopg2
import psycopg2.extras
import logging
from contextlib import contextmanager
from typing import Generator, Any

from core.config import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages PostgreSQL connections to Supabase."""

    def __init__(self):
        self._settings = get_settings()

    @contextmanager
    def get_connection(self) -> Generator:
        """Get a database connection context manager."""
        conn = None
        try:
            conn = psycopg2.connect(self._settings.database_url)
            conn.set_session(readonly=True)
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(self, sql: str) -> dict[str, Any]:
        """
        Execute a SELECT query and return results as JSON-serializable dict.

        Returns:
            dict with 'columns' and 'rows' keys.
        """
        max_rows = self._settings.QUERY_MAX_ROWS
        timeout_ms = self._settings.QUERY_TIMEOUT_MS

        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SET LOCAL statement_timeout = %s", (timeout_ms,))
                cur.execute(sql)
                rows = cur.fetchmany(max_rows + 1)
                truncated = len(rows) > max_rows
                if truncated:
                    rows = rows[:max_rows]
                columns = [desc[0] for desc in cur.description] if cur.description else []

                # Convert rows to list of dicts (JSON-serializable)
                serialized_rows = []
                for row in rows:
                    serialized_row = {}
                    for key, value in row.items():
                        # Handle non-serializable types
                        if hasattr(value, "isoformat"):
                            serialized_row[key] = value.isoformat()
                        elif isinstance(value, (int, float, str, bool, type(None))):
                            serialized_row[key] = value
                        else:
                            serialized_row[key] = str(value)
                    serialized_rows.append(serialized_row)

                return {
                    "columns": columns,
                    "rows": serialized_rows,
                    "row_count": len(serialized_rows),
                    "truncated": truncated,
                }

    def test_connection(self) -> bool:
        """Test if the database connection is working."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False


# Singleton instance
db_manager = DatabaseManager()
