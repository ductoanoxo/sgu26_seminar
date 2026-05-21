"""Router for connection management endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

import logging
from core.auth import get_user_id
from services.connection_service import connection_service
from schemas.connection_schemas import (
    ConnectionCreateRequest, 
    ConnectionResponse, 
    ConnectionListResponse,
    ConnectionTestResponse,
    MemberAddRequest,
    MemberListResponse
)

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("", response_model=ConnectionResponse)
async def create_connection(request: ConnectionCreateRequest, user_id: str = Depends(get_user_id)):
    """Create a new database connection."""
    try:
        conn = connection_service.create(user_id, request)
        return ConnectionResponse(success=True, connection=conn)
    except Exception as e:
        logger.error(f"Failed to create connection: {e}")
        return ConnectionResponse(success=False, error=str(e))

@router.get("", response_model=ConnectionListResponse)
async def list_connections(user_id: str = Depends(get_user_id)):
    """List all connections the user has access to."""
    try:
        conns = connection_service.list(user_id)
        return ConnectionListResponse(success=True, connections=conns)
    except Exception as e:
        logger.error(f"Failed to list connections: {e}")
        return ConnectionListResponse(success=False, connections=[])

@router.delete("/{connection_id}")
async def delete_connection(connection_id: str, user_id: str = Depends(get_user_id)):
    """Delete a connection (Owner only)."""
    success = connection_service.delete(connection_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Connection not found or permission denied")
    return {"success": True}

from schemas.connection_schemas import ConnectionUpdateRequest
from typing import Any

@router.put("/{connection_id}", response_model=ConnectionResponse)
async def update_connection(connection_id: str, request: ConnectionUpdateRequest, user_id: str = Depends(get_user_id)):
    """Update a connection (Owner only)."""
    try:
        conn = connection_service.update(connection_id, user_id, request)
        if not conn:
            return ConnectionResponse(success=False, error="Connection not found or permission denied")
        return ConnectionResponse(success=True, connection=conn)
    except Exception as e:
        return ConnectionResponse(success=False, error=str(e))

@router.post("/{connection_id}/test", response_model=ConnectionTestResponse)
async def test_connection(connection_id: str, user_id: str = Depends(get_user_id)):
    """Test a database connection."""
    result = connection_service.test_connection(connection_id, user_id)
    return ConnectionTestResponse(**result)

@router.post("/{connection_id}/members")
async def add_member(connection_id: str, request: MemberAddRequest, user_id: str = Depends(get_user_id)):
    """Share a connection with another user."""
    try:
        connection_service.add_member(connection_id, user_id, request.email, request.role)
        return {"success": True}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{connection_id}/members", response_model=MemberListResponse)
async def get_members(connection_id: str, user_id: str = Depends(get_user_id)):
    """Get all members of a connection."""
    try:
        members = connection_service.get_members(connection_id, user_id)
        return MemberListResponse(success=True, members=members)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        return MemberListResponse(success=False, error=str(e))

@router.delete("/{connection_id}/members/{email}")
async def remove_member(connection_id: str, email: str, user_id: str = Depends(get_user_id)):
    """Remove a member from a connection."""
    try:
        connection_service.remove_member(connection_id, user_id, email)
        return {"success": True}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
