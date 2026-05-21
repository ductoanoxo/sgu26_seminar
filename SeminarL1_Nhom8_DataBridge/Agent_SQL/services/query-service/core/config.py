"""Query Service configuration."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Supabase PostgreSQL
    SUPABASE_DB_HOST: str = "localhost"
    SUPABASE_DB_PORT: int = 5432
    SUPABASE_DB_NAME: str = "postgres"
    SUPABASE_DB_USER: str = "postgres"
    SUPABASE_DB_PASSWORD: str = ""

    # Service
    SERVICE_PORT: int = 8001
    SERVICE_HOST: str = "0.0.0.0"
    DEBUG: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"

    # Query limits
    QUERY_TIMEOUT_MS: int = 30000
    QUERY_MAX_ROWS: int = 1000

    @property
    def database_url(self) -> str:
        return (
            f"host={self.SUPABASE_DB_HOST} "
            f"port={self.SUPABASE_DB_PORT} "
            f"dbname={self.SUPABASE_DB_NAME} "
            f"user={self.SUPABASE_DB_USER} "
            f"password={self.SUPABASE_DB_PASSWORD}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
