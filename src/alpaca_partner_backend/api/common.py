"""Common dependencies of all API routers."""

from functools import lru_cache

from alpaca.broker import BrokerClient
from alpaca_partner_backend.settings import SETTINGS


@lru_cache
def get_broker_client() -> BrokerClient:
    """Get application settings based on the environment and cache it."""
    return BrokerClient(
        api_key=SETTINGS.BROKER_API_KEY,
        secret_key=SETTINGS.BROKER_API_SECRET,
    )
