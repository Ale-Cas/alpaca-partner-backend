"""Test assets router."""
import httpx
from fastapi.testclient import TestClient

from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models.api import QuoteJson

ROUTER = Routers.PRICES.value


def test_get_bars(
    mock_api_client: TestClient,
) -> None:
    """Test the GET prices endpoint."""
    response = mock_api_client.get(
        url=f"{ROUTER}/bars",
        params={
            "symbol": "AAPL",
        },
    )
    assert httpx.codes.is_success(response.status_code)
    bars = response.json()
    assert isinstance(bars, list)


def test_get_latest_quote(
    mock_api_client: TestClient,
) -> None:
    """Test the GET latest quote endpoint."""
    response = mock_api_client.get(
        url=f"{ROUTER}/quotes/latest",
        params={
            "symbol": "AAPL",
        },
    )
    assert httpx.codes.is_success(response.status_code)
    quote = QuoteJson(**response.json())
    assert isinstance(quote, QuoteJson)
