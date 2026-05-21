"""Read active saved connection from Supabase. Cached 5 seconds."""

import time
import logging
import psycopg2
import psycopg2.extras
from typing import Optional
from core.config import get_settings

logger = logging.getLogger(__name__)

_cache: Optional[dict] = "UNSET"   # type: ignore  sentinel
_cached_at: float = 0.0
_TTL = 5  # seconds


def get_active_connection() -> Optional[dict]:
    global _cache, _cached_at
    now = time.monotonic()
    if _cache != "UNSET" and (now - _cached_at) < _TTL:
        return _cache

    try:
        conn = psycopg2.connect(get_settings().database_url)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM public.saved_connections
                WHERE is_active = true LIMIT 1
            """)
            row = cur.fetchone()
        conn.close()
        _cache = dict(row) if row else None
        _cached_at = now
        return _cache
    except Exception as e:
        logger.warning(f"active_connection fetch failed: {e}")
        _cache = None
        _cached_at = now
        return None


def invalidate():
    global _cached_at
    _cached_at = 0.0
