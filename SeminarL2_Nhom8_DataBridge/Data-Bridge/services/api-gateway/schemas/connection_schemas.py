"""Connection schemas for API Gateway."""

from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class ConnectionCreateRequest(BaseModel):
    name: str
    db_type: str = "postgresql"
    host: str
    port: int = 5432
    database_name: str
    username: str
    password: str          # Plaintext - will be encrypted before saving
    ssl_enabled: bool = True
    settings: dict = {"timeout_ms": 30000, "max_rows": 500}

class ConnectionUpdateRequest(BaseModel):
    name: Optional[str] = None
    db_type: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    ssl_enabled: Optional[bool] = None
    settings: Optional[dict] = None


class ConnectionResponseItem(BaseModel):
    id: str
    name: str
    db_type: str
    host: str
    database_name: str
    is_active: bool
    created_at: datetime
    role: str

class ConnectionResponse(BaseModel):
    success: bool
    connection: Optional[dict] = None
    error: Optional[str] = None

class ConnectionListResponse(BaseModel):
    success: bool
    connections: list[ConnectionResponseItem] = []

class MemberAddRequest(BaseModel):
    email: str
    role: str = "viewer"   # 'admin' | 'viewer'

class MemberItem(BaseModel):
    email: str
    role: str
    granted_at: datetime

class MemberListResponse(BaseModel):
    success: bool
    members: list[MemberItem] = []
    error: Optional[str] = None

class ConnectionTestResponse(BaseModel):
    success: bool
    tables: list[str] = []
    error: Optional[str] = None
