"""Query execution service."""

import logging
import time
from core.database import db_manager
from core.errors import map_query_error
from core.security import validate_sql
from domain.models import QueryResult

logger = logging.getLogger(__name__)


class QueryService:
    """Service for validating and executing SQL queries against Supabase."""

    def execute(self, sql: str) -> QueryResult:
        """Validate and execute a SQL query."""
        # Step 1: Validate the SQL
        validation = validate_sql(sql)
        if not validation.is_valid:
            logger.warning(f"SQL validation failed: {validation.error_message}")
            return QueryResult(
                success=False,
                error=validation.error_message,
            )

        safe_sql = validation.sanitized_sql

        # Step 2: Execute the query
        try:
            start_time = time.perf_counter()
            result = db_manager.execute_query(safe_sql)
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            logger.info(f"Query executed successfully: {result['row_count']} rows returned")
            return QueryResult(
                columns=result["columns"],
                rows=result["rows"],
                row_count=result["row_count"],
                duration_ms=duration_ms,
                truncated=result.get("truncated", False),
                success=True,
            )
        except Exception as e:
            logger.exception("Query execution error")
            return QueryResult(
                success=False,
                error=map_query_error(e),
            )

    def health_check(self) -> bool:
        return db_manager.test_connection()


query_service = QueryService()
