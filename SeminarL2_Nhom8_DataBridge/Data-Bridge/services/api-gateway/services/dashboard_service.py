"""Dashboard orchestration service."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import List
import httpx
from core.config import get_settings
from core.dashboard_store import dashboard_store

logger = logging.getLogger(__name__)


class DashboardService:
    """Handles dashboard CRUD operations."""

    def create(self, name: str, owner_id: str, description: str | None, widgets: list[dict]):
        return dashboard_store.create_dashboard(name, owner_id, description, widgets)

    def get(self, dashboard_id: str, owner_id: str):
        return dashboard_store.get_dashboard(dashboard_id, owner_id)

    def list(self, owner_id: str, limit: int = 20):
        return dashboard_store.list_dashboards(owner_id, limit)

    def update(self, dashboard_id: str, owner_id: str, fields: dict):
        return dashboard_store.update_dashboard(dashboard_id, owner_id, fields)

    async def refresh(
        self,
        dashboard_id: str,
        owner_id: str,
        widget_ids: List[str] | None = None,
    ) -> tuple[List[dict], str | None]:
        dashboard = dashboard_store.get_dashboard(dashboard_id, owner_id)
        if not dashboard:
            return [], "Dashboard not found"

        widgets = dashboard.get("widgets") or []
        if widget_ids:
            allowed = set(widget_ids)
            widgets = [widget for widget in widgets if widget.get("id") in allowed]

        results: list[dict] = []
        tasks: list[asyncio.Task] = []
        task_widgets: list[dict] = []

        async with httpx.AsyncClient(timeout=60.0) as client:
            for widget in widgets:
                sql = (widget.get("sql_source") or "").strip()
                widget_id = widget.get("id", "")
                if not sql:
                    results.append(
                        {
                            "widget_id": widget_id,
                            "success": False,
                            "error": "Widget has no SQL source.",
                            "data": {},
                            "metadata": {},
                        }
                    )
                    continue

                task_widgets.append(widget)
                tasks.append(asyncio.create_task(self._execute_widget_query(client, sql)))

            responses = await asyncio.gather(*tasks, return_exceptions=True)

        for widget, response in zip(task_widgets, responses):
            widget_id = widget.get("id", "")
            if isinstance(response, Exception):
                results.append(
                    {
                        "widget_id": widget_id,
                        "success": False,
                        "error": "Query service unavailable.",
                        "data": {},
                        "metadata": {},
                    }
                )
                continue

            success, data, metadata, error = response
            results.append(
                {
                    "widget_id": widget_id,
                    "success": success,
                    "data": data if success else {},
                    "metadata": metadata if success else {},
                    "error": error if not success else None,
                }
            )

        return results, None

    async def _execute_widget_query(self, client: httpx.AsyncClient, sql: str):
        settings = get_settings()
        try:
            response = await client.post(
                f"{settings.QUERY_SERVICE_URL}/execute",
                json={"sql_query": sql},
            )
        except Exception:
            return False, {}, {}, "Query service unavailable."

        if response.status_code >= 400:
            return False, {}, {}, "Query service error."

        payload = response.json()
        if not payload.get("success"):
            return False, {}, {}, payload.get("error", "Widget refresh failed.")

        data = {
            "columns": payload.get("columns", []),
            "rows": payload.get("rows", []),
            "row_count": payload.get("row_count", 0),
        }
        metadata = {
            "duration_ms": payload.get("duration_ms", 0),
            "truncated": payload.get("truncated", False),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return True, data, metadata, None


dashboard_service = DashboardService()
