"""API Gateway Pydantic schemas."""

from pydantic import BaseModel, Field
from typing import Optional

class AskRequest(BaseModel):
    question: str = Field(..., description="Natural language question about the data")
    connection_id: Optional[str] = Field(default=None, description="ID of the database connection to use")


class AskResponse(BaseModel):
    success: bool
    sql_query: str = ""
    explanation: str = ""
    data: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
    error: str | None = None


class ExplainRequest(BaseModel):
    sql_query: str = Field(..., description="SQL query to explain")
    connection_id: Optional[str] = Field(default=None, description="ID of the database connection to use")


class ExplainResponse(BaseModel):
    success: bool
    explanation: str = ""
    error: str | None = None


class ManualQueryRequest(BaseModel):
    sql_query: str = Field(..., description="SQL query edited by the user")
    question: str | None = Field(default=None, description="Original natural language question")
    sql_original: str | None = Field(default=None, description="Original AI-generated SQL")
    connection_id: Optional[str] = Field(default=None, description="ID of the database connection to use")


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


class TranscriptionResponse(BaseModel):
    success: bool
    text: str = ""
    provider: str = ""
    model: str = ""
    language: str | None = None
    duration: float | None = None
    error: str | None = None
