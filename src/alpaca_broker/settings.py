"""Configuration file."""

from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    BROKER_API_KEY: str
    BROKER_API_SECRET: str

    class Config:
        """Configuration for settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get application settings based on the environment and cache it."""
    return Settings()


SETTINGS = get_settings()
