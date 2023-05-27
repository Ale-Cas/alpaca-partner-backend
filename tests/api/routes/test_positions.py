"""Test positions router."""
import httpx
from alpaca.broker import Account
from alpaca.common import BaseURL
from alpaca.trading import Order
from fastapi.testclient import TestClient
from requests_mock import Mocker

from alpaca_partner_backend.enums import Routers
from tests.conftest import TEST_EMAIL

ROUTER = Routers.POSITIONS.value


def test_get_positions(
    mock_api_client_with_user: TestClient,
) -> None:
    """Test the GET positions endpoint."""
    response = mock_api_client_with_user.get(
        url=ROUTER,
    )
    assert httpx.codes.is_success(response.status_code)
    bars = response.json()
    assert isinstance(bars, list)


def test_mock_close_position(
    mock_api_client_with_user: TestClient,
    reqmock: Mocker,
    alpaca_account: Account,
    mock_get_alpaca_account_by_email: str,
) -> None:
    """Test the DELETE positions endpoint with underlying API calls mocked."""
    symbol = "AAPL"
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/accounts?query={str(TEST_EMAIL)}",
        text=mock_get_alpaca_account_by_email,
    )
    reqmock.delete(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/trading/accounts/{alpaca_account.id}/positions/{symbol}",
        text="""
        {
            "id": "61e69015-8549-4bfd-b9c3-01e75843f47d",
            "client_order_id": "eb9e2aaa-f71a-4f51-b5b4-52a6c565dad4",
            "created_at": "2021-03-16T18:38:01.942282Z",
            "updated_at": "2021-03-16T18:38:01.942282Z",
            "submitted_at": "2021-03-16T18:38:01.937734Z",
            "filled_at": null,
            "expired_at": null,
            "canceled_at": null,
            "failed_at": null,
            "replaced_at": null,
            "replaced_by": null,
            "replaces": null,
            "asset_id": "b0b6dd9d-8b9b-48a9-ba46-b9d54906e415",
            "symbol": "AAPL",
            "asset_class": "us_equity",
            "notional": "500",
            "qty": null,
            "filled_qty": "0",
            "filled_avg_price": null,
            "order_class": "",
            "order_type": "market",
            "type": "market",
            "side": "buy",
            "time_in_force": "day",
            "limit_price": null,
            "stop_price": null,
            "status": "accepted",
            "extended_hours": false,
            "legs": null,
            "trail_percent": null,
            "trail_price": null,
            "hwm": null
        }
        """,
    )
    response = mock_api_client_with_user.delete(
        url=f"{ROUTER}/{symbol}",
    )
    assert httpx.codes.is_success(response.status_code)
    order = Order(**response.json())
    assert order.symbol == symbol
