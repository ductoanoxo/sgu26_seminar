"""API Gateway orchestration service — communicates via Kafka."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional
import httpx

from core.config import get_settings
from core.history import history_manager
from core.kafka_producer import request
from core.connection_store import connection_store
from core.encryption import decrypt_value
from domain.models import GatewayResult

logger = logging.getLogger(__name__)
settings = get_settings()


class GatewayService:
    """Orchestrates calls between NL2SQL and Query services."""

    async def _get_connection_params(self, connection_id: Optional[str], user_id: str) -> Optional[dict]:
        """Fetch and decrypt connection parameters if connection_id is provided."""
        if not connection_id:
            return None
        
        conn_info = connection_store.get_connection(connection_id, user_id)
        if not conn_info:
            logger.warning(f"Connection {connection_id} not found for user {user_id}")
            return None
            
        try:
            # Decrypt password
            password = decrypt_value(conn_info["password_enc"])
            return {
                "host": conn_info["host"],
                "port": conn_info["port"],
                "database_name": conn_info["database_name"],
                "username": conn_info["username"],
                "password": password,
                "db_type": conn_info.get("db_type", "postgresql")
            }
        except Exception as e:
            logger.error(f"Failed to resolve connection {connection_id}: {e}")
            return None

    async def ask(self, question: str, connection_id: Optional[str] = None, user_id: str = "public") -> GatewayResult:
        """Full pipeline: NL → SQL → Execute → Response."""
        logger.info(f"[Gateway] Processing question: '{question}' (connection: {connection_id})")
        correlation_id = str(uuid.uuid4())

        # Resolve connection params
        connection_params = await self._get_connection_params(connection_id, user_id)

        # Step 1: NL2SQL via Kafka
        try:
            nl2sql_payload = {"correlation_id": correlation_id, "query": question}
            if connection_params:
                nl2sql_payload["connection_params"] = connection_params
                
            nl2sql_data = await request(
                topic="nl2sql.requests",
                payload=nl2sql_payload,
                timeout=60.0,
            )
        except Exception as e:
            logger.error(f"[Gateway] NL2SQL error: {e}")
            return GatewayResult(success=False, error=f"NL2SQL service unavailable: {e}")

        if not nl2sql_data.get("success"):
            error = nl2sql_data.get("error", "SQL generation failed")
            history_manager.log_query(question, "", "", False)
            return GatewayResult(
                success=False,
                error=error,
                metadata={"intermediate_steps": nl2sql_data.get("intermediate_steps", [])},
            )

        sql_query = nl2sql_data["sql_query"]
        explanation = nl2sql_data["explanation"]
        selected_tables = nl2sql_data.get("selected_tables", [])
        intermediate_steps = nl2sql_data.get("intermediate_steps", [])

        # Step 2: Execute SQL via Kafka
        try:
            query_payload = {
                "correlation_id": correlation_id, 
                "sql_query": sql_query
            }
            if connection_params:
                query_payload["connection_params"] = connection_params

            query_data = await request(
                topic="query.requests",
                payload=query_payload,
                timeout=30.0,
            )
        except Exception as e:
            logger.error(f"[Gateway] Query service error: {e}")
            history_manager.log_query(question, sql_query, explanation, False)
            return GatewayResult(
                success=False,
                sql_query=sql_query,
                explanation=explanation,
                error=f"Query service unavailable: {e}",
                metadata={"selected_tables": selected_tables, "intermediate_steps": intermediate_steps},
            )

        if not query_data.get("success"):
            error = query_data.get("error", "Query execution failed")
            history_manager.log_query(question, sql_query, explanation, False)
            return GatewayResult(
                success=False,
                sql_query=sql_query,
                explanation=explanation,
                error=error,
                metadata={"selected_tables": selected_tables, "intermediate_steps": intermediate_steps},
            )

        row_count = query_data.get("row_count", 0)
        history_manager.log_query(question, sql_query, explanation, True, row_count)

        return GatewayResult(
            success=True,
            sql_query=sql_query,
            explanation=explanation,
            data={
                "columns": query_data.get("columns", []),
                "rows": query_data.get("rows", []),
                "row_count": row_count,
            },
            metadata={
                "correlation_id": correlation_id,
                "selected_tables": selected_tables,
                "intermediate_steps": intermediate_steps,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    async def explain(self, sql_query: str, connection_id: Optional[str] = None, user_id: str = "public") -> dict:
        """Explain a SQL query — still calls NL2SQL via Kafka."""
        correlation_id = str(uuid.uuid4())
        try:
            result = await request(
                topic="nl2sql.requests",
                payload={"correlation_id": correlation_id, "action": "explain", "sql_query": sql_query},
                timeout=30.0,
            )
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def manual_query(
        self,
        sql_query: str,
        question: str | None = None,
        sql_original: str | None = None,
        connection_id: Optional[str] = None,
        user_id: str = "public"
    ) -> GatewayResult:
        """Execute a user-edited SQL query via the Query service."""
        
        # Resolve connection params
        connection_params = await self._get_connection_params(connection_id, user_id)
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                payload = {"sql_query": sql_query}
                if connection_params:
                    payload["connection_params"] = connection_params
                    
                query_resp = await client.post(
                    f"{settings.QUERY_SERVICE_URL}/execute",
                    json=payload,
                )
                query_data = query_resp.json()
            except Exception as e:
                logger.error(f"[Gateway] Query service error: {e}")
                history_manager.log_query(
                    question or "",
                    sql_query,
                    "",
                    False,
                    source="manual",
                    sql_original=sql_original,
                )
                return GatewayResult(
                    success=False,
                    sql_query=sql_query,
                    error=f"Query service unavailable: {str(e)}",
                    metadata={
                        "source": "manual",
                        "sql_original": sql_original,
                    },
                )

            if not query_data.get("success"):
                error = query_data.get("error", "Query execution failed")
                history_manager.log_query(
                    question or "",
                    sql_query,
                    "",
                    False,
                    source="manual",
                    sql_original=sql_original,
                )
                return GatewayResult(
                    success=False,
                    sql_query=sql_query,
                    error=error,
                    metadata={
                        "source": "manual",
                        "sql_original": sql_original,
                    },
                )

            row_count = query_data.get("row_count", 0)
            duration_ms = query_data.get("duration_ms", 0)
            history_manager.log_query(
                question or "",
                sql_query,
                "",
                True,
                row_count,
                source="manual",
                sql_original=sql_original,
                duration_ms=duration_ms,
            )

            return GatewayResult(
                success=True,
                sql_query=sql_query,
                data={
                    "columns": query_data.get("columns", []),
                    "rows": query_data.get("rows", []),
                    "row_count": row_count,
                },
                metadata={
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "duration_ms": duration_ms,
                    "truncated": query_data.get("truncated", False),
                    "source": "manual",
                    "sql_original": sql_original,
                },
            )


gateway_service = GatewayService()
