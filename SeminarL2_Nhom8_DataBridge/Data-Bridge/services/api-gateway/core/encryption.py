"""Encryption utilities for sensitive data like database passwords."""

import logging
from cryptography.fernet import Fernet
from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

def _get_fernet() -> Fernet:
    """Initialize Fernet with the encryption key from settings."""
    if not settings.ENCRYPTION_KEY:
        logger.error("ENCRYPTION_KEY is not set in environment!")
        # In development, we might fallback or raise error
        raise ValueError("ENCRYPTION_KEY is required for sensitive data management")
    
    try:
        return Fernet(settings.ENCRYPTION_KEY.encode())
    except Exception as e:
        logger.error(f"Invalid ENCRYPTION_KEY: {e}")
        raise ValueError(f"Invalid ENCRYPTION_KEY: {e}")

def encrypt_value(plaintext: str) -> str:
    """Encrypt a string and return the base64 encoded ciphertext."""
    if not plaintext:
        return ""
    
    f = _get_fernet()
    ciphertext = f.encrypt(plaintext.encode())
    return ciphertext.decode()

def decrypt_value(ciphertext: str) -> str:
    """Decrypt a base64 encoded ciphertext string."""
    if not ciphertext:
        return ""
    
    try:
        f = _get_fernet()
        plaintext = f.decrypt(ciphertext.encode())
        return plaintext.decode()
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise ValueError("Failed to decrypt sensitive data")
