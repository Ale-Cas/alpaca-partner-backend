"""Test assets router."""
import httpx
from fastapi.testclient import TestClient

from alpaca_partner_backend.enums import Routers

ROUTER = Routers.PRICES.value


def test_get_bars(
    mock_api_client: TestClient,
) -> None:
    """Test the GET assets endpoint with underlying API call cached."""
    response = mock_api_client.get(
        url=f"{ROUTER}/bars",
        params={
            "symbol": "AAPL",
        },
    )
    assert httpx.codes.is_success(response.status_code)
    bars = response.json()
    assert isinstance(bars, list)
