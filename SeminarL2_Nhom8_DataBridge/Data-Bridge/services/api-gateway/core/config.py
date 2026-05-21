"""API Gateway configuration."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase PostgreSQL connection (for dashboard storage)
    SUPABASE_DB_HOST: str = "localhost"
    SUPABASE_DB_PORT: int = 5432
    SUPABASE_DB_NAME: str = "postgres"
    SUPABASE_DB_USER: str = "postgres"
    SUPABASE_DB_PASSWORD: str = ""

    # Supabase Auth (JWT)
    SUPABASE_JWKS_URL: str = ""
    SUPABASE_JWT_ISSUER: str = ""
    SUPABASE_JWT_AUDIENCE: str = "authenticated"
    AUTH_REQUIRED: bool = False
    AUTH_FALLBACK_USER_ID: str = "00000000-0000-0000-0000-000000000000"

    NL2SQL_SERVICE_URL: str = "http://localhost:8002"
    QUERY_SERVICE_URL: str = "http://localhost:8001"
    IMPORT_SERVICE_URL: str = "http://localhost:8003"
    SERVICE_PORT: int = 8000
    SERVICE_HOST: str = "0.0.0.0"
    DEBUG: bool = False
    HISTORY_FILE: str = "query_history.json"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    GROQ_API_KEY: str = ""
    STT_MAX_FILE_MB: int = 25

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
