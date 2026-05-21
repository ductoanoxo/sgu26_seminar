"""Query service API router."""

import asyncio
import logging
import httpx
from fastapi import APIRouter
from schemas.query_schemas import QueryExecuteRequest, QueryExecuteResponse, HealthResponse, SchemaRequest, SchemaResponse
from services.query_service import query_service
from core.active_connection import get_active_connection
from core.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/schema", response_model=SchemaResponse)
async def get_schema(request: SchemaRequest):
    """Dynamically fetch the schema of the database."""
    try:
        connection_params = request.connection_params
        if not connection_params:
            return SchemaResponse(success=False, error="No connection params provided")
            
        if connection_params.get("db_type") == "mongodb":
            schema = db_manager.get_mongodb_schema(connection_params)
            return SchemaResponse(success=True, schema_text=schema)
        elif connection_params.get("db_type") == "postgresql":
            schema = db_manager.get_postgresql_schema(connection_params)
            return SchemaResponse(success=True, schema_text=schema)
        else:
            return SchemaResponse(success=False, error=f"Dynamic schema not implemented for db_type: {connection_params.get('db_type')}")
    except Exception as e:
        return SchemaResponse(success=False, error=str(e))


@router.post("/execute", response_model=QueryExecuteResponse)
async def execute_query(request: QueryExecuteRequest):
    result = query_service.execute(request.sql_query)
    return QueryExecuteResponse(
        success=result.success,
        columns=result.columns,
        rows=result.rows,
        row_count=result.row_count,
        duration_ms=result.duration_ms,
        truncated=result.truncated,
        error=result.error,
    )


@router.get("/schema")
async def get_schema():
    """Return schema for the active connection only (used by NL2SQL agents)."""
    active = await asyncio.to_thread(get_active_connection)
    if active:
        db_type = active.get("db_type", "")
        if db_type == "file":
            # Imported data source: expose only tables from this upload/import
            table_names = [
                t.strip()
                for t in (active.get("database_name", "") or "").split(",")
                if t.strip()
            ]
            schema = await asyncio.to_thread(query_service.db.get_tables_schema, table_names)
            return {"schema": schema}
        elif db_type in {"postgresql", "mysql", "sqlite"}:
            # External DB: fetch schema from import-service (existing behavior)
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    resp = await client.get(f"{get_settings().IMPORT_SERVICE_URL}/connections/schema")
                    if resp.status_code == 200:
                        data = resp.json()
                        return {"schema": data.get("schema", "")}
            except Exception as e:
                logger.warning(f"Failed to fetch schema from import-service: {e}")
        return {"schema": ""}
    return {"schema": ""}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    db_ok = query_service.health_check()
    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        service="query-service",
        database_connected=db_ok,
    )
