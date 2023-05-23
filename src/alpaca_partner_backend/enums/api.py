"""Enums for the FastAPI implementation."""
from enum import Enum


class Routers(str, Enum):
    """Possible routers of the API."""

    ACCOUNTS = "/accounts"
    ASSETS = "/assets"
    USERS = "/users"
    PRICES = "/prices"
    FUNDING = "/funding"


class BarsField(str, Enum):
    """Field of a BarSet object."""

    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"
    TRADE_COUNT = "trade_count"
    VWAP = "vwap"
