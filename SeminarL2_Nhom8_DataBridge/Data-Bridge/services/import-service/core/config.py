from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SUPABASE_DB_HOST: str = "localhost"
    SUPABASE_DB_PORT: int = 5432
    SUPABASE_DB_NAME: str = "postgres"
    SUPABASE_DB_USER: str = "postgres"
    SUPABASE_DB_PASSWORD: str = ""

    NL2SQL_SERVICE_URL: str = "http://localhost:8002"

    SERVICE_PORT: int = 8000
    SERVICE_HOST: str = "0.0.0.0"
    DEBUG: bool = False

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
