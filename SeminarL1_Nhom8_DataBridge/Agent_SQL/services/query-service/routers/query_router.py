"""Query service API router."""

from fastapi import APIRouter
from schemas.query_schemas import QueryExecuteRequest, QueryExecuteResponse, HealthResponse
from services.query_service import query_service

router = APIRouter()


@router.post("/execute", response_model=QueryExecuteResponse)
async def execute_query(request: QueryExecuteRequest):
    """Execute a validated SQL SELECT query against the database."""
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


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check service and database health."""
    db_ok = query_service.health_check()
    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        service="query-service",
        database_connected=db_ok,
    )
