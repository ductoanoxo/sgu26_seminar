"""NL2SQL service Pydantic schemas."""

from pydantic import BaseModel, Field


class NL2SQLRequest(BaseModel):
    query: str = Field(..., description="Natural language query from the user")


class AgentStep(BaseModel):
    agent: str
    input_summary: str
    output_summary: str
    raw_output: dict | str | None = None


class NL2SQLResponse(BaseModel):
    success: bool
    sql_query: str = ""
    explanation: str = ""
    selected_tables: list[str] = Field(default_factory=list)
    intermediate_steps: list[AgentStep] = Field(default_factory=list)
    error: str | None = None


class ExplainRequest(BaseModel):
    sql_query: str = Field(..., description="SQL query to explain")


class ExplainResponse(BaseModel):
    success: bool
    explanation: str = ""
    error: str | None = None
