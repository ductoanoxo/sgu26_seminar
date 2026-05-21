from pydantic import BaseModel
from typing import Optional, List


class SavedConnection(BaseModel):
    id: str
    name: str
    db_type: str
    host: Optional[str] = None
    port: Optional[int] = None
    database_name: str = ""
    username: Optional[str] = None
    is_active: bool = False
    created_at: Optional[str] = None
    last_used_at: Optional[str] = None


class CreateConnectionRequest(BaseModel):
    name: str
    db_type: str          # postgresql | mysql | mongodb | sqlite | redis
    host: str = "localhost"
    port: Optional[int] = None
    database_name: str = ""
    username: Optional[str] = None
    password: Optional[str] = None


class ConnectionResponse(BaseModel):
    success: bool
    connection: Optional[SavedConnection] = None
    error: Optional[str] = None


class ConnectionListResponse(BaseModel):
    success: bool
    connections: List[SavedConnection] = []
    error: Optional[str] = None


class TestConnectionResponse(BaseModel):
    success: bool
    message: str


class SchemaResponse(BaseModel):
    success: bool
    schema: str = ""
    raw_schema: Optional[List[dict]] = None
    has_active: bool = False
    connection_name: Optional[str] = None
    db_type: Optional[str] = None
