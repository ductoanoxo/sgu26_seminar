"""Import Service API router."""

import logging
import os
import uuid
import tempfile
from fastapi import APIRouter, UploadFile, File, Header

from core.supabase_writer import writer
from schemas.import_schemas import (
    TestConnectionRequest, TestConnectionResponse,
    ListSourcesRequest, ListSourcesResponse,
    ImportExecuteRequest, ImportExecuteResponse,
    FileUploadResponse, FileImportRequest, FileImportResponse,
)
from services.import_service import import_service
from services.connection_service import connection_service

router = APIRouter()
logger = logging.getLogger(__name__)

# Store uploaded files on disk so all workers share the same files.
# Each upload creates two files: <file_id> (content) and <file_id>.meta (original filename).
UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "import_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/registry")
async def list_registry():
    """Return all previously imported datasets from import_registry."""
    rows = writer.list_registry()
    return {"success": True, "registry": rows}


@router.post("/test-connection", response_model=TestConnectionResponse)
async def test_connection(request: TestConnectionRequest):
    ok, msg = import_service.test_connection(
        request.db_type, request.host, request.port,
        request.database, request.username, request.password,
        request.connection_string,
    )
    return TestConnectionResponse(success=ok, message=msg)


@router.post("/list-sources", response_model=ListSourcesResponse)
async def list_sources(request: ListSourcesRequest):
    ok, sources, error = import_service.list_sources(
        request.db_type, request.host, request.port,
        request.database, request.username, request.password,
        request.connection_string,
    )
    return ListSourcesResponse(success=ok, sources=sources, error=error or None)


@router.post("/execute", response_model=ImportExecuteResponse)
async def execute_import(request: ImportExecuteRequest, x_user_id: str = Header(default="public")):
    imported, errors = import_service.execute_import(
        request.db_type, request.host, request.port,
        request.database, request.username, request.password,
        request.tables, request.limit, request.connection_string,
    )
    if imported:
        try:
            destination_tables = [t.destination_table for t in imported]
            # Use user-provided name, or auto-generate from connection info
            if request.name and request.name.strip():
                label = request.name.strip()
            elif request.connection_string:
                from urllib.parse import urlparse as _urlparse
                _parsed = _urlparse(request.connection_string)
                _host = _parsed.hostname or request.host or request.db_type.value
                _db   = (_parsed.path or "").lstrip("/").split("?")[0] or request.database
                label = f"{request.db_type.value}:{_host}/{_db}" if _db else f"{request.db_type.value}:{_host}"
            else:
                label = f"{request.db_type.value}:{request.database or request.host}"
            conn = connection_service.create_file_source(x_user_id, label, destination_tables)
            connection_service.activate(conn.id, user_id=x_user_id)
        except Exception as e:
            logger.warning(f"create_file_source failed for imported database: {e}")
    return ImportExecuteResponse(
        success=len(imported) > 0,
        imported=imported,
        errors=errors,
    )


@router.post("/upload-file", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    original_filename = file.filename or "upload.bin"
    try:
        sources = import_service.list_file_sources(content, original_filename)
        file_id = uuid.uuid4().hex
        # Save file content
        with open(os.path.join(UPLOAD_DIR, file_id), "wb") as f:
            f.write(content)
        # Save original filename so execute-file can reconstruct the correct FileAdapter
        with open(os.path.join(UPLOAD_DIR, f"{file_id}.meta"), "w", encoding="utf-8") as f:
            f.write(original_filename)
        return FileUploadResponse(success=True, file_id=file_id, sources=sources)
    except Exception as e:
        logger.error(f"File upload error: {e}")
        return FileUploadResponse(success=False, error=str(e))


@router.post("/execute-file", response_model=FileImportResponse)
async def execute_file_import(request: FileImportRequest, x_user_id: str = Header(default="public")):
    content_path = os.path.join(UPLOAD_DIR, request.file_id)
    meta_path = os.path.join(UPLOAD_DIR, f"{request.file_id}.meta")

    if not os.path.exists(content_path):
        logger.error(f"Temp file not found: {content_path}")
        return FileImportResponse(
            success=False,
            errors=["File not found. Please re-upload and try again."],
        )

    with open(content_path, "rb") as f:
        content = f.read()

    # Restore original filename so FileAdapter detects format and generates matching source names
    original_filename = request.file_id
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            original_filename = f.read().strip() or request.file_id

    imported, errors = import_service.import_file(content, original_filename, request.tables)

    # Register the entire file as a single scoped data source in saved_connections
    if imported:
        try:
            destination_tables = [t.destination_table for t in imported]
            label = (request.name.strip() if request.name and request.name.strip() else original_filename)
            conn = connection_service.create_file_source(x_user_id, label, destination_tables)
            connection_service.activate(conn.id, user_id=x_user_id)
        except Exception as e:
            logger.warning(f"create_file_source failed for {original_filename}: {e}")

    # Clean up temp files after import
    for path in (content_path, meta_path):
        try:
            os.remove(path)
        except Exception:
            pass

    return FileImportResponse(
        success=len(imported) > 0,
        imported=imported,
        errors=errors,
    )
