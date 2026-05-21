"""API Gateway router."""

from fastapi import APIRouter, Depends, File, Form, UploadFile
from schemas.gateway_schemas import (
    AskRequest, AskResponse,
    ExplainRequest, ExplainResponse,
    ManualQueryRequest,
    HistoryResponse,
    TranscriptionResponse,
)
from schemas.dashboard_schemas import (
    DashboardCreateRequest,
    DashboardUpdateRequest,
    DashboardResponse,
    DashboardListResponse,
    DashboardRefreshRequest,
    DashboardRefreshResponse,
)
from services.gateway_service import gateway_service
from services.dashboard_service import dashboard_service
from services.speech_service import SpeechToTextError, speech_to_text_service
from core.history import history_manager
from core.auth import get_user_id

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest, user_id: str = Depends(get_user_id)):
    """Main endpoint: ask a question in natural language."""
    result = await gateway_service.ask(request.question, connection_id=request.connection_id, user_id=user_id)
    return AskResponse(
        success=result.success,
        sql_query=result.sql_query,
        explanation=result.explanation,
        data=result.data,
        metadata=result.metadata,
        error=result.error,
    )


@router.post("/explain", response_model=ExplainResponse)
async def explain_sql(request: ExplainRequest, user_id: str = Depends(get_user_id)):
    """Explain a SQL query in natural language."""
    result = await gateway_service.explain(request.sql_query, connection_id=request.connection_id, user_id=user_id)
    return ExplainResponse(
        success=result.get("success", False),
        explanation=result.get("explanation", ""),
        error=result.get("error"),
    )


@router.post("/query/manual", response_model=AskResponse)
async def manual_query(request: ManualQueryRequest, user_id: str = Depends(get_user_id)):
    """Execute a user-edited SQL query."""
    result = await gateway_service.manual_query(
        sql_query=request.sql_query,
        question=request.question,
        sql_original=request.sql_original,
        connection_id=request.connection_id,
        user_id=user_id
    )
    return AskResponse(
        success=result.success,
        sql_query=result.sql_query,
        explanation=result.explanation,
        data=result.data,
        metadata=result.metadata,
        error=result.error,
    )


@router.get("/history", response_model=HistoryResponse)
async def get_history(limit: int = 20):
    """Get recent query history."""
    entries = history_manager.get_history(limit)
    return HistoryResponse(entries=entries)


@router.post("/speech/transcribe", response_model=TranscriptionResponse)
async def transcribe_speech(
    file: UploadFile = File(...),
    model: str = Form("whisper-large-v3-turbo"),
):
    """Transcribe uploaded speech audio into text."""
    try:
        result = await speech_to_text_service.transcribe(file, model)
        return TranscriptionResponse(success=True, **result)
    except SpeechToTextError as e:
        return TranscriptionResponse(success=False, model=model, error=str(e))
    except Exception as e:
        return TranscriptionResponse(success=False, model=model, error=f"Transcription failed: {e}")


@router.post("/dashboards", response_model=DashboardResponse)
async def create_dashboard(request: DashboardCreateRequest, user_id: str = Depends(get_user_id)):
    """Create a new dashboard."""
    try:
        dashboard = dashboard_service.create(
            name=request.name,
            owner_id=user_id,
            description=request.description,
            widgets=[w.model_dump() for w in request.widgets],
        )
        return DashboardResponse(success=True, dashboard=dashboard)
    except Exception as e:
        return DashboardResponse(success=False, error=str(e))


@router.get("/dashboards", response_model=DashboardListResponse)
async def list_dashboards(limit: int = 20, user_id: str = Depends(get_user_id)):
    """List dashboards for an owner."""
    try:
        dashboards = dashboard_service.list(owner_id=user_id, limit=limit)
        return DashboardListResponse(success=True, dashboards=dashboards)
    except Exception as e:
        return DashboardListResponse(success=False, error=str(e))


@router.get("/dashboards/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(dashboard_id: str, user_id: str = Depends(get_user_id)):
    """Get a dashboard by id."""
    try:
        dashboard = dashboard_service.get(dashboard_id, owner_id=user_id)
        if not dashboard:
            return DashboardResponse(success=False, error="Dashboard not found")
        return DashboardResponse(success=True, dashboard=dashboard)
    except Exception as e:
        return DashboardResponse(success=False, error=str(e))


@router.put("/dashboards/{dashboard_id}", response_model=DashboardResponse)
async def update_dashboard(
    dashboard_id: str,
    request: DashboardUpdateRequest,
    user_id: str = Depends(get_user_id),
):
    """Update a dashboard."""
    try:
        fields = request.model_dump(exclude_unset=True)
        # Pydantic's model_dump recursively dumps nested objects, so fields["widgets"] is already a list of dicts.
        dashboard = dashboard_service.update(dashboard_id, owner_id=user_id, fields=fields)
        if not dashboard:
            return DashboardResponse(success=False, error="Dashboard not found")
        return DashboardResponse(success=True, dashboard=dashboard)
    except Exception as e:
        return DashboardResponse(success=False, error=str(e))


@router.post("/dashboards/{dashboard_id}/refresh", response_model=DashboardRefreshResponse)
async def refresh_dashboard(
    dashboard_id: str,
    request: DashboardRefreshRequest,
    user_id: str = Depends(get_user_id),
):
    """Refresh widget data for a dashboard."""
    try:
        results, error = await dashboard_service.refresh(
            dashboard_id=dashboard_id,
            owner_id=user_id,
            widget_ids=request.widget_ids,
        )
        if error:
            return DashboardRefreshResponse(success=False, error=error)
        return DashboardRefreshResponse(success=True, results=results)
    except Exception as e:
        return DashboardRefreshResponse(success=False, error=str(e))
