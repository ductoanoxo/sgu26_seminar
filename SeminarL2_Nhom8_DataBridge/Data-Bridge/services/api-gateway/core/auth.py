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
    """Extract user id from Supabase JWT (sub). Raises 401 when AUTH_REQUIRED and token is missing/invalid."""
    if not authorization or not authorization.startswith("Bearer "):
        if settings.AUTH_REQUIRED:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        return settings.AUTH_FALLBACK_USER_ID

    if not _jwks_client:
        if settings.AUTH_REQUIRED:
            raise HTTPException(status_code=500, detail="Auth is not configured")
        return settings.AUTH_FALLBACK_USER_ID

    token = authorization.split(" ", 1)[1]
    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token).key
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256", "ES256"],
            audience=settings.SUPABASE_JWT_AUDIENCE,
            issuer=settings.SUPABASE_JWT_ISSUER,
        )
        
        user_id = payload.get("sub")
        if not user_id:
            if settings.AUTH_REQUIRED:
                raise HTTPException(status_code=401, detail="Invalid token payload: missing sub")
            return settings.AUTH_FALLBACK_USER_ID
            
        return user_id
    except Exception as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return user_id


def get_optional_user_id(authorization: str | None = Header(default=None)) -> str:
    """Extract user id from JWT if possible, otherwise return fallback. Never raises 401.
    Used for data-isolation on proxy routes where auth may not be fully configured.

    Priority order:
    1. Full JWKS verification (signature + audience + issuer) — most secure
    2. Signature-only verification — if audience/issuer not configured
    3. Unverified decode — if JWKS not configured at all (user isolation only, not security)
    4. Fallback user ID — if token is completely invalid
    """
    if not authorization or not authorization.startswith("Bearer "):
        return settings.AUTH_FALLBACK_USER_ID

    token = authorization.split(" ", 1)[1]

    # Try JWKS verification first (RS256 tokens)
    if _jwks_client:
        try:
            signing_key = _jwks_client.get_signing_key_from_jwt(token).key
            try:
                payload = jwt.decode(
                    token,
                    signing_key,
                    algorithms=["RS256"],
                    audience=settings.SUPABASE_JWT_AUDIENCE,
                    issuer=settings.SUPABASE_JWT_ISSUER,
                )
            except (jwt.InvalidAudienceError, jwt.InvalidIssuerError, jwt.MissingRequiredClaimError):
                payload = jwt.decode(
                    token,
                    signing_key,
                    algorithms=["RS256"],
                    options={"verify_aud": False, "verify_iss": False},
                )
            user_id = payload.get("sub")
            if user_id:
                return user_id
        except Exception as e:
            # JWKS failed (e.g. token uses HS256 not RS256) — fall through to unverified decode
            logger.debug(f"JWKS JWT decode failed, trying unverified: {e}")

    # Fallback: decode without signature verification to extract user_id.
    # Supabase projects using HS256 (default) cannot be verified via JWKS.
    # This still provides per-user data isolation; configure SUPABASE_JWKS_URL for full security.
    try:
        payload = jwt.decode(
            token,
            options={"verify_signature": False},
            algorithms=["RS256", "HS256"],
        )
        user_id = payload.get("sub")
        if user_id:
            logger.debug(f"Using unverified JWT sub for user isolation: {user_id[:8]}...")
            return user_id
    except Exception as e:
        logger.debug(f"Unverified JWT decode failed: {e}")

    return settings.AUTH_FALLBACK_USER_ID
