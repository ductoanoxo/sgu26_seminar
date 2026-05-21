"""Business logic for data import from multiple sources."""

import logging
import httpx
from typing import List, Tuple
from core.config import get_settings

from adapters.postgresql import PostgreSQLAdapter
from adapters.mysql import MySQLAdapter
from adapters.mongodb import MongoDBAdapter
from adapters.sqlite_adapter import SQLiteAdapter
from adapters.redis_adapter import RedisAdapter
from adapters.file_adapter import FileAdapter
from adapters.base import BaseAdapter
from core.supabase_writer import writer
from schemas.import_schemas import DBType, SourceInfo, ColumnInfo, ImportedTable

logger = logging.getLogger(__name__)


def _build_adapter(
    db_type: DBType, host: str, port: int,
    database: str, username: str, password: str,
    connection_string: str = None,
) -> BaseAdapter:
    if db_type == DBType.postgresql:
        return PostgreSQLAdapter(host, port, database, username, password, connection_string)
    elif db_type == DBType.mysql:
        return MySQLAdapter(host, port, database, username, password)
    elif db_type == DBType.mongodb:
        return MongoDBAdapter(host, port, database, username, password, connection_string)
    elif db_type == DBType.sqlite:
        return SQLiteAdapter(database)
    elif db_type == DBType.redis:
        return RedisAdapter(host, port, database, username, password)
    raise ValueError(f"Unsupported db_type: {db_type}")


def _to_source_info(sources) -> List[SourceInfo]:
    return [
        SourceInfo(
            name=s.name,
            estimated_rows=s.estimated_rows,
            columns=[ColumnInfo(name=c.name, type=c.type) for c in s.columns],
        )
        for s in sources
    ]


def _notify_schema_refresh():
    """Tell nl2sql-service to invalidate its schema cache."""
    try:
        url = f"{get_settings().NL2SQL_SERVICE_URL}/schema/refresh"
        httpx.post(url, timeout=3.0)
        logger.info("Schema cache refresh notified")
    except Exception as e:
        logger.warning(f"Could not notify schema refresh: {e}")


class ImportService:

    def test_connection(
        self, db_type, host, port, database, username, password, connection_string=None
    ) -> Tuple[bool, str]:
        adapter = _build_adapter(db_type, host, port, database, username, password, connection_string)
        try:
            ok = adapter.test_connection()
            return ok, "Connection successful" if ok else "Connection failed"
        except Exception as e:
            return False, str(e)
        finally:
            adapter.close()

    def list_sources(
        self, db_type, host, port, database, username, password, connection_string=None
    ) -> Tuple[bool, List[SourceInfo], str]:
        adapter = _build_adapter(db_type, host, port, database, username, password, connection_string)
        try:
            sources = adapter.list_sources()
            return True, _to_source_info(sources), ""
        except Exception as e:
            logger.error(f"list_sources error: {e}")
            return False, [], str(e)
        finally:
            adapter.close()

    def execute_import(
        self, db_type, host, port, database, username, password,
        tables: List[str], limit: int = 10000, connection_string=None,
    ) -> Tuple[List[ImportedTable], List[str]]:
        try:
            writer.ensure_registry_table()
        except Exception as e:
            logger.error(f"Failed to create registry table: {e}")
            return [], [f"Database setup error: {e}"]
        adapter = _build_adapter(db_type, host, port, database, username, password, connection_string)
        imported: List[ImportedTable] = []
        errors: List[str] = []
        try:
            for table in tables:
                try:
                    data = adapter.read_data(table, limit)
                    dest = writer.import_data(
                        source_name=table,
                        source_type=db_type.value,
                        columns=data["columns"],
                        rows=data["rows"],
                    )
                    imported.append(ImportedTable(
                        source=table,
                        destination_table=dest,
                        rows_imported=len(data["rows"]),
                    ))
                except Exception as e:
                    errors.append(f"{table}: {e}")
                    logger.error(f"Import error for table '{table}': {e}")
        finally:
            adapter.close()
        if imported:
            _notify_schema_refresh()
        return imported, errors

    def list_file_sources(self, file_content: bytes, filename: str) -> List[SourceInfo]:
        adapter = FileAdapter(file_content, filename)
        return _to_source_info(adapter.list_sources())

    def import_file(
        self, file_content: bytes, filename: str,
        tables: List[str], limit: int = 10000,
    ) -> Tuple[List[ImportedTable], List[str]]:
        try:
            writer.ensure_registry_table()
        except Exception as e:
            logger.error(f"Failed to create registry table: {e}")
            return [], [f"Database setup error: {e}"]
        adapter = FileAdapter(file_content, filename)
        imported: List[ImportedTable] = []
        errors: List[str] = []

        sources_to_import = tables if tables else [s.name for s in adapter.list_sources()]

        for source in sources_to_import:
            try:
                data = adapter.read_data(source, limit)
                dest = writer.import_data(
                    source_name=source,
                    source_type="file",
                    columns=data["columns"],
                    rows=data["rows"],
                )
                imported.append(ImportedTable(
                    source=source,
                    destination_table=dest,
                    rows_imported=len(data["rows"]),
                ))
            except Exception as e:
                errors.append(f"{source}: {e}")
                logger.error(f"File import error for '{source}': {e}")

        if imported:
            _notify_schema_refresh()
        return imported, errors


import_service = ImportService()
