"""Test assets router."""
import httpx
from fastapi.testclient import TestClient

from alpaca_partner_backend.enums import Routers

ROUTER = Routers.LOGOS.value


def test_get_logos(
    mock_api_client: TestClient,
) -> None:
    """Test the GET assets endpoint with underlying API call cached."""
    symbol = "AAPL"
    response = mock_api_client.get(
        url=f"{ROUTER}/{symbol}",
    )
    assert httpx.codes.is_success(response.status_code)
    logo_bytes = response.content
    assert isinstance(logo_bytes, bytes)
