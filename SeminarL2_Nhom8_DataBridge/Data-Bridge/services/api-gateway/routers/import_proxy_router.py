"""Proxy router — forwards /import/* and /connections/* requests to import-service."""

import logging
import httpx
from fastapi import APIRouter, Depends, UploadFile, File, Request
from fastapi.responses import JSONResponse
from core.config import get_settings
from core.auth import get_optional_user_id as get_user_id

router = APIRouter(tags=["Import"])
logger = logging.getLogger(__name__)


def _import_url(path: str) -> str:
    base = f"{get_settings().IMPORT_SERVICE_URL}/import"
    return f"{base}/{path}" if path else base


def _conn_url(path: str) -> str:
    base = f"{get_settings().IMPORT_SERVICE_URL}/connections"
    return f"{base}/{path}" if path else base


def _user_headers(user_id: str) -> dict:
    return {"X-User-ID": user_id}


async def _proxy_get(url: str, user_id: str = "public") -> JSONResponse:
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=_user_headers(user_id))
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except httpx.ConnectError:
        return JSONResponse({"success": False, "error": "Import service unavailable"}, status_code=503)
    except Exception as e:
        logger.error(f"Proxy GET error [{url}]: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


async def _proxy_post(url: str, body: dict | None = None, user_id: str = "public") -> JSONResponse:
    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
            resp = await client.post(url, json=body or {}, headers=_user_headers(user_id))
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except httpx.ConnectError:
        return JSONResponse({"success": False, "error": "Import service unavailable"}, status_code=503)
    except Exception as e:
        logger.error(f"Proxy POST error [{url}]: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


async def _proxy_delete(url: str, user_id: str = "public") -> JSONResponse:
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.delete(url, headers=_user_headers(user_id))
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except httpx.ConnectError:
        return JSONResponse({"success": False, "error": "Import service unavailable"}, status_code=503)
    except Exception as e:
        logger.error(f"Proxy DELETE error [{url}]: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ── Import routes ──────────────────────────────────────────────────────────────

@router.get("/import/registry")
async def proxy_registry(user_id: str = Depends(get_user_id)):
    return await _proxy_get(_import_url("registry"), user_id)


@router.post("/import/test-connection")
async def proxy_test_connection(request: Request, user_id: str = Depends(get_user_id)):
    return await _proxy_post(_import_url("test-connection"), await request.json(), user_id)


@router.post("/import/list-sources")
async def proxy_list_sources(request: Request, user_id: str = Depends(get_user_id)):
    return await _proxy_post(_import_url("list-sources"), await request.json(), user_id)


@router.post("/import/execute")
async def proxy_execute(request: Request, user_id: str = Depends(get_user_id)):
    return await _proxy_post(_import_url("execute"), await request.json(), user_id)


@router.post("/import/upload-file")
async def proxy_upload_file(file: UploadFile = File(...), user_id: str = Depends(get_user_id)):
    content = await file.read()
    try:
        async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
            resp = await client.post(
                _import_url("upload-file"),
                files={"file": (file.filename, content, file.content_type)},
                headers=_user_headers(user_id),
            )
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except httpx.ConnectError:
        return JSONResponse({"success": False, "error": "Import service unavailable"}, status_code=503)
    except Exception as e:
        logger.error(f"Import proxy upload error: {e}")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@router.post("/import/execute-file")
async def proxy_execute_file(request: Request, user_id: str = Depends(get_user_id)):
    return await _proxy_post(_import_url("execute-file"), await request.json(), user_id)


# ── Connection Manager routes ──────────────────────────────────────────────────
# IMPORTANT: Literal/specific routes MUST come before /{conn_id} parameterized routes

@router.get("/connections")
async def proxy_list_connections(user_id: str = Depends(get_user_id)):
    return await _proxy_get(_conn_url(""), user_id)


@router.post("/connections")
async def proxy_create_connection(request: Request, user_id: str = Depends(get_user_id)):
    return await _proxy_post(_conn_url(""), await request.json(), user_id)


@router.post("/connections/deactivate")
async def proxy_deactivate(user_id: str = Depends(get_user_id)):
    result = await _proxy_post(_conn_url("deactivate"), user_id=user_id)
    await _invalidate_nl2sql_schema_cache()
    return result


@router.get("/connections/active")
async def proxy_get_active(user_id: str = Depends(get_user_id)):
    return await _proxy_get(_conn_url("active"), user_id)


@router.get("/connections/schema")
async def proxy_connection_schema(user_id: str = Depends(get_user_id)):
    return await _proxy_get(_conn_url("schema"), user_id)


# NOTE: /connections/preview-data MUST be before /connections/{conn_id} DELETE
@router.get("/connections/preview-data")
async def proxy_preview_data(table: str, limit: int = 10, user_id: str = Depends(get_user_id)):
    url = _conn_url(f"preview-data?table={table}&limit={limit}")
    return await _proxy_get(url, user_id)


@router.delete("/connections/{conn_id}")
async def proxy_delete_connection(conn_id: str, user_id: str = Depends(get_user_id)):
    return await _proxy_delete(_conn_url(conn_id), user_id)


async def _invalidate_nl2sql_schema_cache() -> None:
    """Tell nl2sql-service to drop its schema cache so next query uses fresh schema."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(f"{get_settings().NL2SQL_SERVICE_URL}/schema/refresh")
        logger.info("NL2SQL schema cache invalidated")
    except Exception as e:
        logger.warning(f"Failed to invalidate NL2SQL schema cache: {e}")


@router.post("/connections/{conn_id}/activate")
async def proxy_activate_connection(conn_id: str, user_id: str = Depends(get_user_id)):
    result = await _proxy_post(_conn_url(f"{conn_id}/activate"), user_id=user_id)
    await _invalidate_nl2sql_schema_cache()
    return result


@router.post("/connections/{conn_id}/test")
async def proxy_test_connection_by_id(conn_id: str, user_id: str = Depends(get_user_id)):
    return await _proxy_post(_conn_url(f"{conn_id}/test"), user_id=user_id)


@router.get("/debug/whoami")
async def whoami(user_id: str = Depends(get_user_id)):
    """Temporary debug endpoint — returns the user_id extracted from the JWT token."""
    return {"user_id": user_id}
