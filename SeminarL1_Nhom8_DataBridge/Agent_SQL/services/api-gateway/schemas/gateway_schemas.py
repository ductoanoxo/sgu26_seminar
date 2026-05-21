"""API Gateway Pydantic schemas."""

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., description="Natural language question about the data")


class AskResponse(BaseModel):
    success: bool
    sql_query: str = ""
    explanation: str = ""
    data: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
    error: str | None = None


class ExplainRequest(BaseModel):
    sql_query: str = Field(..., description="SQL query to explain")


class ExplainResponse(BaseModel):
    success: bool
    explanation: str = ""
    error: str | None = None


class ManualQueryRequest(BaseModel):
    sql_query: str = Field(..., description="SQL query edited by the user")
    question: str | None = Field(default=None, description="Original natural language question")
    sql_original: str | None = Field(default=None, description="Original AI-generated SQL")


class HistoryEntry(BaseModel):
    id: int
    timestamp: str
    question: str
    sql_query: str
    sql_original: str | None = None
    explanation: str
    success: bool
    row_count: int = 0
    duration_ms: int = 0
    source: str = "ai"


class HistoryResponse(BaseModel):
    entries: list[HistoryEntry] = Field(default_factory=list)
