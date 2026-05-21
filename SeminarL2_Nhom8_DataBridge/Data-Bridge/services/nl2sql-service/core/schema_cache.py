"""Dynamic active-schema fetcher with a short in-memory cache."""

import logging
import time

import httpx

from core.config import get_settings

logger = logging.getLogger(__name__)

_CACHE_TTL = 30  # seconds

_cached_schema: str = ""
_cached_at: float = 0.0


def invalidate_cache():
    """Force cache expiry so next get_schema() call fetches fresh data."""
    global _cached_at
    _cached_at = 0.0


def get_schema() -> str:
    """Return the active DB schema, refreshing from query-service if needed."""
    global _cached_schema, _cached_at

    now = time.monotonic()
    if _cached_schema and (now - _cached_at) < _CACHE_TTL:
        return _cached_schema

    settings = get_settings()
    url = f"{settings.QUERY_SERVICE_URL}/schema"

    try:
        resp = httpx.get(url, timeout=5.0)
        resp.raise_for_status()
        schema = resp.json().get("schema", "")
        if schema:
            _cached_schema = schema
            _cached_at = now
            logger.info("Schema cache refreshed from query-service")
            return _cached_schema
        logger.warning("query-service returned empty schema - will retry next request")
    except Exception as e:
        logger.warning(f"Could not fetch schema from query-service: {e}")

    # Never fall back to hardcoded public tables. That can make the LLM generate
    # SQL outside the active dataset.
    return _cached_schema
