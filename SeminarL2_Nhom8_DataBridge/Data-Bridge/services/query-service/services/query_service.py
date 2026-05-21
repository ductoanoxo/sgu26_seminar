"""Query execution service."""

import logging
import re
import time
from core.database import db_manager
from core.errors import map_query_error
from core.security import validate_sql
from core.active_connection import get_active_connection, invalidate as invalidate_conn_cache
from core.external_executor import execute_on_external, is_sql_type
from domain.models import QueryResult

logger = logging.getLogger(__name__)


class QueryService:
    """Service for validating and executing SQL queries."""

    def execute(self, sql: str) -> QueryResult:
        validation = validate_sql(sql)
        if not validation.is_valid:
            logger.warning(f"SQL validation failed: {validation.error_message}")
            return QueryResult(success=False, error=validation.error_message)

        safe_sql = validation.sanitized_sql

        active = get_active_connection()
        if active and active.get("db_type") == "file":
            return self._exec_imported_scope(safe_sql, active)
        if active and is_sql_type(active.get("db_type", "")):
            return self._exec_external(safe_sql, active)

        return QueryResult(
            success=False,
            error="No active dataset selected. Please import or select a data source before running queries.",
        )

    def _exec_supabase(self, sql: str) -> QueryResult:
        try:
            start = time.perf_counter()
            result = db_manager.execute_query(sql)
            duration_ms = int((time.perf_counter() - start) * 1000)
            logger.info(f"Supabase query: {result['row_count']} rows")
            return QueryResult(
                columns=result["columns"],
                rows=result["rows"],
                row_count=result["row_count"],
                duration_ms=duration_ms,
                truncated=result.get("truncated", False),
                success=True,
            )
        except Exception as e:
            logger.exception("Supabase query error")
            return QueryResult(success=False, error=map_query_error(e))

    def _exec_external(self, sql: str, conn_row: dict) -> QueryResult:
        try:
            start = time.perf_counter()
            result = execute_on_external(conn_row, sql, db_manager._settings.QUERY_MAX_ROWS)
            duration_ms = int((time.perf_counter() - start) * 1000)
            logger.info(f"External({conn_row['db_type']}) query: {result['row_count']} rows")
            return QueryResult(
                columns=result["columns"],
                rows=result["rows"],
                row_count=result["row_count"],
                duration_ms=duration_ms,
                truncated=result.get("truncated", False),
                success=True,
            )
        except Exception as e:
            logger.exception("External query error")
            invalidate_conn_cache()
            return QueryResult(success=False, error=str(e))

    def _exec_imported_scope(self, sql: str, conn_row: dict) -> QueryResult:
        allowed_tables = {
            t.strip().lower()
            for t in (conn_row.get("database_name") or "").split(",")
            if t.strip()
        }
        if not allowed_tables:
            return QueryResult(success=False, error="Active imported dataset has no table scope.")

        referenced_tables = _extract_referenced_tables(sql)
        out_of_scope = sorted(t for t in referenced_tables if t not in allowed_tables)
        if out_of_scope:
            return QueryResult(
                success=False,
                error=(
                    "Query references table(s) outside the active dataset: "
                    + ", ".join(out_of_scope)
                ),
            )

        return self._exec_supabase(sql)

    def health_check(self) -> bool:
        return db_manager.test_connection()

    @property
    def db(self):
        return db_manager


query_service = QueryService()


def _extract_referenced_tables(sql: str) -> set[str]:
    """Best-effort table scope extraction for SELECT queries."""
    clean_sql = re.sub(r"'[^']*'", "''", sql)
    cte_names = {
        m.group(1).lower()
        for m in re.finditer(r"(?:WITH|,)\s+\"?([a-zA-Z_][\w]*)\"?\s+AS\s*\(", clean_sql, re.IGNORECASE)
    }

    refs: set[str] = set()
    table_token = re.compile(r'^((?:"?[a-zA-Z_][\w]*"?\.)?"?[a-zA-Z_][\w]*"?)')
    clause_end = (
        r"(?=\bWHERE\b|\bGROUP\s+BY\b|\bORDER\s+BY\b|\bHAVING\b|\bLIMIT\b|"
        r"\bOFFSET\b|\bUNION\b|\bEXCEPT\b|\bINTERSECT\b|$)"
    )

    for segment_match in re.finditer(r"\bFROM\s+(.+?)" + clause_end, clean_sql, re.IGNORECASE | re.DOTALL):
        segment = re.sub(r"\b(?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\b", ",", segment_match.group(1), flags=re.IGNORECASE)
        for part in segment.split(","):
            part = re.split(r"\bON\b", part, maxsplit=1, flags=re.IGNORECASE)[0].strip()
            if not part or part.startswith("("):
                continue
            token = table_token.search(part)
            if token:
                _add_table_ref(refs, token.group(1), cte_names)

    for join_match in re.finditer(
        r"\bJOIN\s+((?:\"?[a-zA-Z_][\w]*\"?\.)?\"?[a-zA-Z_][\w]*\"?)",
        clean_sql,
        re.IGNORECASE,
    ):
        _add_table_ref(refs, join_match.group(1), cte_names)
    return refs


def _add_table_ref(refs: set[str], raw_name: str, cte_names: set[str]) -> None:
    parts = raw_name.replace('"', "").lower().split(".")
    table = parts[-1]
    if table not in cte_names:
        if len(parts) > 1 and parts[-2] != "public":
            refs.add(".".join(parts[-2:]))
        else:
            refs.add(table)
