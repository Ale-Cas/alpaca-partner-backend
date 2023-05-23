"""Common dependencies of all API routers."""

from functools import lru_cache

from alpaca.broker import BrokerClient
from alpaca.data import StockHistoricalDataClient

from alpaca_partner_backend.settings import SETTINGS


@lru_cache
def get_broker_client() -> BrokerClient:
    """Get application settings based on the environment and cache the broker client."""
    return BrokerClient(
        api_key=SETTINGS.BROKER_API_KEY,
        secret_key=SETTINGS.BROKER_API_SECRET,
    )


@lru_cache
def get_data_client() -> StockHistoricalDataClient:
    """Get application settings based on the environment and cache the market data client."""
    return StockHistoricalDataClient(
        api_key=SETTINGS.BROKER_API_KEY,
        secret_key=SETTINGS.BROKER_API_SECRET,
        url_override="https://data.sandbox.alpaca.markets",
        use_basic_auth=True,
    )
