"""database package."""
from functools import lru_cache

from alpaca_broker.database.mongo import MongoDatabase


@lru_cache
def get_db() -> MongoDatabase:
    """Get the database."""
    return MongoDatabase()


__all__ = [
    "get_db",
    "MongoDatabase",
]
