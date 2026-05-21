"""NL2SQL Service configuration."""

from pydantic import field_validator
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal, List, Any, Optional
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Provider
    LLM_PROVIDER: Literal["gemini", "openai", "openrouter", "coordinator"] = "coordinator"

    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # Coordinator Settings
    GEMINI_MODELS: List[str] = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
    GEMINI_KEYS: Any = []
    
    @field_validator("GEMINI_KEYS", mode="before")
    @classmethod
    def parse_gemini_keys(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Fallback for plain string or comma-separated values
            return [k.strip() for k in v.split(",") if k.strip()]
        return v or []
    FAST_PASS_KEY_COUNT: int = 2
    GEMINI_TIMEOUT_MS: int = 15000
    GEMINI_COOLDOWN_S: int = 60

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    
    # OpenRouter
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    OPENROUTER_EMBEDDING_MODEL: str = "openai/text-embedding-3-large"

    # Downstream services
    QUERY_SERVICE_URL: str = "http://localhost:8001"

    # Service
    SERVICE_PORT: int = 8002
    SERVICE_HOST: str = "0.0.0.0"
    DEBUG: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    QUERY_SERVICE_URL: str = "http://query-service:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
