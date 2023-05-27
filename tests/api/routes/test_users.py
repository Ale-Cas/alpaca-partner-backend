"""Test users router."""
import httpx
import pytest
from fastapi.testclient import TestClient

from alpaca_partner_backend.api.routes.users import get_current_user
from alpaca_partner_backend.database.mongo import MongoDatabase
from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models import AuthCredentials, User, UserOut
from tests.conftest import TEST_EMAIL

ROUTER = Routers.USERS.value


def test_get_current_user(
    database: MongoDatabase,
    mock_credentials: AuthCredentials,
) -> None:
    """Test create_user method."""
    user = get_current_user(database=database, _email=mock_credentials.email)
    assert isinstance(user, User)


def test_get_current_user_db_error(
    database: MongoDatabase,
    mock_credentials: AuthCredentials,
) -> None:
    """Test create_user method."""
    _email = mock_credentials.email + "error"
    with pytest.raises(AssertionError, match=f"Document with email {_email} not found"):
        get_current_user(database=database, _email=_email)


def test_login(mock_api_client_with_user: TestClient, mock_credentials: AuthCredentials) -> None:
    """Test POST method on the accounts router."""
    response = mock_api_client_with_user.post(
        url=ROUTER + "/login",
        json=AuthCredentials(
            email=mock_credentials.email,
            password=mock_credentials.password,
        ).dict(),
    )
    assert httpx.codes.is_success(response.status_code)


def test_register_error(
    mock_api_client_with_user: TestClient, mock_credentials: AuthCredentials
) -> None:
    """Test error when registering an user that already exists."""
    response = mock_api_client_with_user.post(
        url=ROUTER + "/register",
        json=AuthCredentials(
            email=mock_credentials.email,
            password=mock_credentials.password,
        ).dict(),
    )
    assert httpx.codes.is_error(response.status_code)
    assert response.status_code == httpx.codes.CONFLICT


def test_register(mock_api_client: TestClient, mock_credentials: AuthCredentials) -> None:
    """Test POST method on the accounts router."""
    response = mock_api_client.post(
        url=ROUTER + "/register",
        json=AuthCredentials(
            email=mock_credentials.email,
            password=mock_credentials.password,
        ).dict(),
    )
    assert httpx.codes.is_success(response.status_code)
    user_out = UserOut(**response.json())
    assert isinstance(user_out, UserOut)
    assert user_out.email == TEST_EMAIL
