"""NL2SQL Service configuration."""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Provider
    LLM_PROVIDER: Literal["gemini", "openai", "openrouter"] = "openrouter"

    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # OpenRouter
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    OPENROUTER_EMBEDDING_MODEL: str = "openai/text-embedding-3-large"

    # Service
    SERVICE_PORT: int = 8002
    SERVICE_HOST: str = "0.0.0.0"
    DEBUG: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
