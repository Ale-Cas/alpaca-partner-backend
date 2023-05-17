"""Test assets router."""
import httpx
from alpaca.common.enums import BaseURL
from alpaca.trading import Asset
from fastapi.testclient import TestClient
from requests_mock import Mocker

from alpaca_partner_backend.enums import Routers

ROUTER = Routers.ASSETS.value


def test_get_assets(
    mock_api_client: TestClient,
) -> None:
    """Test the GET assets endpoint with underlying API call cached."""
    response = mock_api_client.get(url=ROUTER)
    assert httpx.codes.is_success(response.status_code)
    assets = [Asset(**a) for a in response.json()]
    assert assets


def test_mock_get_assets(
    reqmock: Mocker,
    mock_api_client: TestClient,
    mock_assets_json: str,
) -> None:
    """Test the GET assets endpoint with underlying API call cached."""
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/assets",
        text=mock_assets_json,
    )
    response = mock_api_client.get(url=ROUTER)
    assert httpx.codes.is_success(response.status_code)
    assets = [Asset(**a) for a in response.json()]
    assert assets
