from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class DBType(str, Enum):
    postgresql = "postgresql"
    mysql = "mysql"
    mongodb = "mongodb"
    sqlite = "sqlite"
    redis = "redis"


class ColumnInfo(BaseModel):
    name: str
    type: str


class SourceInfo(BaseModel):
    name: str
    estimated_rows: Optional[int] = None
    columns: List[ColumnInfo] = []


class TestConnectionRequest(BaseModel):
    db_type: DBType
    host: str = "localhost"
    port: Optional[int] = None
    database: str = ""
    username: Optional[str] = None
    password: Optional[str] = None
    connection_string: Optional[str] = None


class TestConnectionResponse(BaseModel):
    success: bool
    message: str


class ListSourcesRequest(BaseModel):
    db_type: DBType
    host: str = "localhost"
    port: Optional[int] = None
    database: str = ""
    username: Optional[str] = None
    password: Optional[str] = None
    connection_string: Optional[str] = None


class ListSourcesResponse(BaseModel):
    success: bool
    sources: List[SourceInfo] = []
    error: Optional[str] = None


class ImportExecuteRequest(BaseModel):
    db_type: DBType
    host: str = "localhost"
    port: Optional[int] = None
    database: str = ""
    username: Optional[str] = None
    password: Optional[str] = None
    connection_string: Optional[str] = None
    tables: List[str]
    limit: int = 10000
    name: Optional[str] = None


class ImportedTable(BaseModel):
    source: str
    destination_table: str
    rows_imported: int


class ImportExecuteResponse(BaseModel):
    success: bool
    imported: List[ImportedTable] = []
    errors: List[str] = []


class FileUploadResponse(BaseModel):
    success: bool
    file_id: str = ""
    sources: List[SourceInfo] = []
    error: Optional[str] = None


class FileImportRequest(BaseModel):
    file_id: str
    tables: List[str]
    name: Optional[str] = None


class FileImportResponse(BaseModel):
    success: bool
    imported: List[ImportedTable] = []
    errors: List[str] = []
