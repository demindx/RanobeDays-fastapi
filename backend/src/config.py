from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    POSTGRES_DB_HOST_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_URL: str = ""
    SECRET_KEY: str = "qewdfqwefqwef"

    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    DB_ECHO: bool = False

    DEFAULT_PAGINATION_LIMIT: int = 50

    COOKIE_SECURE: bool = False

    model_config = SettingsConfigDict(env_file=".env")

    @model_validator(mode="after")
    def generate_db_url(self) -> Config:
        self.POSTGRES_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@db:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return self


config = Config()
