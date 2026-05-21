"""Query service Pydantic schemas."""

from pydantic import BaseModel, Field


class SchemaRequest(BaseModel):
    connection_params: dict | None = Field(default=None, description="Optional target database credentials")

class SchemaResponse(BaseModel):
    success: bool
    schema_text: str | None = None
    error: str | None = None

class QueryExecuteRequest(BaseModel):
    sql_query: str = Field(..., description="The SQL SELECT query to execute")
    connection_params: dict | None = Field(default=None, description="Optional target database credentials")


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
