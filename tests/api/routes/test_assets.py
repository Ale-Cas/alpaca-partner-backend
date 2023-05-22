"""Test assets router."""
import httpx
from alpaca.common.enums import BaseURL
from alpaca.trading import Asset, AssetClass, AssetStatus
from fastapi.testclient import TestClient
from requests_mock import Mocker

from alpaca_partner_backend.enums import Routers

ROUTER = Routers.ASSETS.value


def test_get_assets(
    mock_api_client: TestClient,
) -> None:
    """Test the GET assets endpoint with underlying API call cached."""
    response = mock_api_client.get(
        url=ROUTER,
        params={
            "status": AssetStatus.ACTIVE.value,
            "asset_class": AssetClass.CRYPTO.value,
        },
    )
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


def test_mock_get_active_assets(
    reqmock: Mocker,
    mock_api_client: TestClient,
    mock_assets_json: str,
) -> None:
    """Test the GET assets endpoint with underlying API call cached."""
    status = AssetStatus.ACTIVE.value
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/assets?status={status}",
        text=mock_assets_json,
    )
    response = mock_api_client.get(url=ROUTER, params={"status": status})
    assert httpx.codes.is_success(response.status_code)
    assets = [Asset(**a) for a in response.json()]
    assert assets


def test_mock_get_equity_assets(
    reqmock: Mocker,
    mock_api_client: TestClient,
    mock_assets_json: str,
) -> None:
    """Test the GET assets endpoint with underlying API call cached."""
    asset_class = AssetClass.US_EQUITY.value
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/assets?asset_class={asset_class}",
        text=mock_assets_json,
    )
    response = mock_api_client.get(url=ROUTER, params={"asset_class": asset_class})
    assert httpx.codes.is_success(response.status_code)
    assets = [Asset(**a) for a in response.json()]
    assert assets
