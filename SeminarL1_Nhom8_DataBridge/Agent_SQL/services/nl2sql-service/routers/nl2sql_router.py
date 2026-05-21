"""NL2SQL service API router."""

from fastapi import APIRouter
from schemas.nl2sql_schemas import (
    NL2SQLRequest, NL2SQLResponse, AgentStep,
    ExplainRequest, ExplainResponse,
)
from services.nl2sql_service import nl2sql_service

router = APIRouter()


@router.post("/generate-sql", response_model=NL2SQLResponse)
async def generate_sql(request: NL2SQLRequest):
    """Convert natural language to SQL using multi-agent pipeline."""
    result = nl2sql_service.generate_sql(request.query)

    steps = [
        AgentStep(
            agent=s["agent"],
            input_summary=s["input_summary"],
            output_summary=s["output_summary"],
            raw_output=s.get("raw_output"),
        )
        for s in result.intermediate_steps
    ]

    return NL2SQLResponse(
        success=result.success,
        sql_query=result.sql_query,
        explanation=result.explanation,
        selected_tables=result.selected_tables,
        intermediate_steps=steps,
        error=result.error,
    )


@router.post("/explain", response_model=ExplainResponse)
async def explain_sql(request: ExplainRequest):
    """Explain a SQL query in natural language."""
    try:
        explanation = nl2sql_service.explain_sql(request.sql_query)
        return ExplainResponse(success=True, explanation=explanation)
    except Exception as e:
        return ExplainResponse(success=False, error=str(e))
