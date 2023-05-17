"""Enums for the FastAPI implementation."""
from enum import Enum


class Routers(str, Enum):
    """Possible routers of the API."""

    ACCOUNTS = "/accounts"
    ASSETS = "/assets"
    USERS = "/users"
