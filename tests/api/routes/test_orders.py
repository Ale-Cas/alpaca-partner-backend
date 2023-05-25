"""Test assets router."""
import httpx
from alpaca.broker import Account
from alpaca.common import BaseURL
from alpaca.trading import Order, OrderRequest
from fastapi.testclient import TestClient
from requests_mock import Mocker

from alpaca_partner_backend.enums import Routers
from tests.conftest import TEST_EMAIL

ROUTER = Routers.ORDERS.value


def test_mock_create_order(  # noqa: PLR0913
    reqmock: Mocker,
    mock_order_json: str,
    mock_get_alpaca_account_by_email: str,
    alpaca_account: Account,
    mock_order_request: OrderRequest,
    mock_api_client_with_user: TestClient,
) -> None:
    """Test the POST orders endpoint with underlying API calls mocked."""
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/accounts?query={str(TEST_EMAIL)}",
        text=mock_get_alpaca_account_by_email,
    )
    reqmock.post(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/trading/accounts/{alpaca_account.id}/orders",
        text=mock_order_json,
    )
    response = mock_api_client_with_user.post(
        url=ROUTER,
        json=mock_order_request.dict(),
    )
    assert httpx.codes.is_success(response.status_code)
    order = Order(**response.json())
    assert isinstance(order, Order)
    assert order.id


def test_mock_get_orders(
    reqmock: Mocker,
    mock_get_orders_json: str,
    mock_get_alpaca_account_by_email: str,
    alpaca_account: Account,
    mock_api_client_with_user: TestClient,
) -> None:
    """Test the GET assets endpoint with underlying API call cached."""
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/accounts?query={str(TEST_EMAIL)}",
        text=mock_get_alpaca_account_by_email,
    )
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/trading/accounts/{alpaca_account.id}/orders?status=all&limit=500",
        text=mock_get_orders_json,
    )
    response = mock_api_client_with_user.get(
        url=ROUTER,
    )
    assert httpx.codes.is_success(response.status_code)
    orders = response.json()
    assert isinstance(orders, list)
