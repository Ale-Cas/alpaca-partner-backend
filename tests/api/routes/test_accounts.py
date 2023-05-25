"""Test accouts router."""
import httpx
from alpaca.broker import Account, CreateAccountRequest
from alpaca.common.enums import BaseURL
from fastapi.testclient import TestClient
from requests_mock import Mocker

from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models import AccountJson
from tests.conftest import TEST_EMAIL

ROUTER = Routers.ACCOUNTS.value


def test_mock_post_accounts(
    reqmock: Mocker,
    mock_api_client: TestClient,
    mock_alpaca_account: str,
    mock_alpaca_account_request: CreateAccountRequest,
) -> None:
    """Test POST method on the accounts router."""
    reqmock.post(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/accounts",
        text=mock_alpaca_account,
    )
    post_response = mock_api_client.post(
        url=ROUTER,
        json=mock_alpaca_account_request.to_request_fields(),
    )
    assert httpx.codes.is_success(post_response.status_code)
    account = AccountJson(**post_response.json())
    assert isinstance(account, AccountJson)
    assert account.contact
    assert account.contact.email_address == mock_alpaca_account_request.contact.email_address


def test_post_account(
    reqmock: Mocker,
    mock_alpaca_account: str,
    mock_api_client: TestClient,
    mock_alpaca_account_request: CreateAccountRequest,
) -> None:
    """Test GET method on the accounts router with email in the path."""
    reqmock.post(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/accounts",
        text=mock_alpaca_account,
    )
    post_response = mock_api_client.post(
        url=ROUTER,
        json=mock_alpaca_account_request.to_request_fields(),
    )
    assert httpx.codes.is_success(post_response.status_code)
    account = AccountJson(**post_response.json())
    assert isinstance(account, AccountJson)
    assert account.contact
    assert account.contact.email_address == TEST_EMAIL


def test_get_account_by_email(
    reqmock: Mocker,
    mock_get_alpaca_account_by_email: str,
    alpaca_account: Account,
    mock_api_client_with_user: TestClient,
) -> None:
    """Test GET method on the accounts router with email in the path."""
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/accounts?query={str(TEST_EMAIL)}",
        text=mock_get_alpaca_account_by_email,
    )
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/accounts/{alpaca_account.id}",
        text=alpaca_account.json(),
    )
    get_response = mock_api_client_with_user.get(
        url=ROUTER,
    )
    assert httpx.codes.is_success(get_response.status_code)
    account = AccountJson(**get_response.json())
    assert isinstance(account, AccountJson)
    assert account.contact
    assert account.contact.email_address == TEST_EMAIL


def test_integration_get_post_accounts(
    mock_api_client_with_user: TestClient,
    mock_alpaca_account_request: CreateAccountRequest,
) -> None:
    """Test POST method on the accounts router."""
    get_response = mock_api_client_with_user.get(
        url=ROUTER,
    )
    post_response = mock_api_client_with_user.post(
        url=ROUTER,
        json=mock_alpaca_account_request.to_request_fields(),
    )
    is_account_created = httpx.codes.is_success(post_response.status_code)
    if httpx.codes.is_success(get_response.status_code):
        assert not is_account_created
        assert httpx.codes.is_error(post_response.status_code)
        assert post_response.status_code == httpx.codes.CONFLICT.value
    else:
        assert is_account_created
    _account = (
        post_response.json()
        if is_account_created
        # parse json response from the Broker API for missing data
        else {k: v for k, v in get_response.json().items() if v}
    )
    account = Account(**_account)
    assert isinstance(account, Account)
    assert account.contact
    assert account.contact.email_address == mock_alpaca_account_request.contact.email_address


def test_integration_get_ptf_history(
    mock_api_client_with_user: TestClient,
) -> None:
    """Test get portfolio history endpoint."""
    response = mock_api_client_with_user.get(
        url=f"{ROUTER}/portfolio/history",
    )
    assert httpx.codes.is_success(response.status_code)


def test_account_activities(
    mock_api_client_with_user: TestClient,
) -> None:
    """Test get portfolio history endpoint."""
    response = mock_api_client_with_user.get(
        url=f"{ROUTER}/activities",
    )
    assert httpx.codes.is_success(response.status_code)
