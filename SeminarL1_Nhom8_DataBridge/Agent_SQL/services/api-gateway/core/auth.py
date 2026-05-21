"""Supabase JWT authentication helpers."""

import logging
from fastapi import Header, HTTPException
import jwt
from jwt import PyJWKClient

from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_jwks_client = PyJWKClient(settings.SUPABASE_JWKS_URL) if settings.SUPABASE_JWKS_URL else None


def get_user_id(authorization: str | None = Header(default=None)) -> str:
    """Extract user id from Supabase JWT (sub)."""
    if not authorization or not authorization.startswith("Bearer "):
        if settings.AUTH_REQUIRED:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        return settings.AUTH_FALLBACK_USER_ID

    if not _jwks_client:
        raise HTTPException(status_code=500, detail="Auth is not configured")

    token = authorization.split(" ", 1)[1]
    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token).key
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=settings.SUPABASE_JWT_AUDIENCE,
            issuer=settings.SUPABASE_JWT_ISSUER,
        )
    except jwt.PyJWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return user_id
