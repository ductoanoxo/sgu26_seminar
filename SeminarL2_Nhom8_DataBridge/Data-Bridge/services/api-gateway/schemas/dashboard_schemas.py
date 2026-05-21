"""Dashboard API schemas."""

from pydantic import BaseModel, Field


class DashboardWidget(BaseModel):
    id: str
    title: str
    sql_source: str
    chart_type: str | None = None
    fields: dict | None = None
    filters: dict | None = None


class Dashboard(BaseModel):
    id: str
    name: str
    owner_id: str
    description: str | None = None
    widgets: list[DashboardWidget] = Field(default_factory=list)
    created_at: str | None = None
    updated_at: str | None = None


class DashboardCreateRequest(BaseModel):
    name: str
    description: str | None = None
    widgets: list[DashboardWidget] = Field(default_factory=list)


class DashboardUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    widgets: list[DashboardWidget] | None = None


class DashboardResponse(BaseModel):
    success: bool
    dashboard: Dashboard | None = None
    error: str | None = None


class DashboardListResponse(BaseModel):
    success: bool
    dashboards: list[Dashboard] = Field(default_factory=list)
    error: str | None = None


class DashboardRefreshRequest(BaseModel):
    widget_ids: list[str] | None = None


class WidgetRefreshResult(BaseModel):
    widget_id: str
    success: bool
    data: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
    error: str | None = None


class DashboardRefreshResponse(BaseModel):
    success: bool
    results: list[WidgetRefreshResult] = Field(default_factory=list)
    error: str | None = None
