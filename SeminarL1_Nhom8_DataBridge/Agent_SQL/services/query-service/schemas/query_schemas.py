"""Query service Pydantic schemas."""

from pydantic import BaseModel, Field


class QueryExecuteRequest(BaseModel):
    sql_query: str = Field(..., description="The SQL SELECT query to execute")


class QueryExecuteResponse(BaseModel):
    success: bool
    columns: list[str] = Field(default_factory=list)
    rows: list[dict] = Field(default_factory=list)
    row_count: int = 0
    duration_ms: int = 0
    truncated: bool = False
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    service: str
    database_connected: bool
