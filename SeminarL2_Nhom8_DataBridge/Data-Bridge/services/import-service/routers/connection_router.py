"""Connection Manager router — CRUD for saved database connections."""

import logging
from fastapi import APIRouter, Header
from schemas.connection_schemas import (
    CreateConnectionRequest, ConnectionResponse,
    ConnectionListResponse, TestConnectionResponse, SchemaResponse,
)
from services.connection_service import connection_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", response_model=ConnectionListResponse)
async def list_connections(x_user_id: str = Header(default="public")):
    connections = connection_service.list_all(user_id=x_user_id)
    return ConnectionListResponse(success=True, connections=connections)


@router.post("", response_model=ConnectionResponse)
async def create_connection(req: CreateConnectionRequest, x_user_id: str = Header(default="public")):
    existing = connection_service.find_by_params(
        x_user_id, req.db_type, req.host, req.port, req.database_name,
    )
    if existing:
        return ConnectionResponse(success=True, connection=existing)

    ok, msg = connection_service.test_params(
        req.db_type, req.host, req.port,
        req.database_name, req.username, req.password,
    )
    if not ok:
        return ConnectionResponse(success=False, error=f"Cannot connect: {msg}")
    try:
        conn = connection_service.create(
            x_user_id, req.name, req.db_type, req.host, req.port,
            req.database_name, req.username, req.password,
        )
        return ConnectionResponse(success=True, connection=conn)
    except Exception as e:
        logger.error(f"create_connection error: {e}")
        return ConnectionResponse(success=False, error=str(e))


@router.delete("/{conn_id}")
async def delete_connection(conn_id: str, x_user_id: str = Header(default="public")):
    ok = connection_service.delete(conn_id, user_id=x_user_id)
    return {"success": ok}


@router.post("/{conn_id}/activate")
async def activate_connection(conn_id: str, x_user_id: str = Header(default="public")):
    ok = connection_service.activate(conn_id, user_id=x_user_id)
    return {"success": ok}


@router.post("/deactivate")
async def deactivate(x_user_id: str = Header(default="public")):
    connection_service.deactivate_all(user_id=x_user_id)
    return {"success": True, "message": "No active data source selected"}


@router.get("/active")
async def get_active(x_user_id: str = Header(default="public")):
    active = connection_service.get_active(user_id=x_user_id)
    if not active:
        return {"success": True, "connection": None}
    return {"success": True, "connection": active}


@router.post("/{conn_id}/test", response_model=TestConnectionResponse)
async def test_connection(conn_id: str, x_user_id: str = Header(default="public")):
    ok, msg = connection_service.test_by_id(conn_id, user_id=x_user_id)
    return TestConnectionResponse(success=ok, message=msg)


@router.get("/schema", response_model=SchemaResponse)
async def get_active_schema(x_user_id: str = Header(default="public")):
    """Return schema of active connection (consumed by nl2sql schema_cache)."""
    schema, active, raw_schema = connection_service.get_active_schema(user_id=x_user_id)
    return SchemaResponse(
        success=True,
        schema=schema,
        raw_schema=raw_schema,
        has_active=active is not None,
        connection_name=active.name if active else None,
        db_type=active.db_type if active else None,
    )

@router.get("/preview-data")
async def get_table_data_preview(table: str, limit: int = 10, x_user_id: str = Header(default="public")):
    """Return data preview for a table."""
    try:
        data = connection_service.preview_table_data(x_user_id, table, limit)
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"get_table_data_preview error: {e}")
        return {"success": False, "error": str(e)}
