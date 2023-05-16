"""Configuration file."""

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Alpaca Broker API:
    BROKER_API_KEY: str
    BROKER_API_SECRET: str

    # Database:
    MONGO_DB_URI: str

    # User authentication:
    AUTH_SECRET_KEY: str
    HASHING_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """Configuration for settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get application settings based on the environment and cache it."""
    return Settings()


SETTINGS = get_settings()
