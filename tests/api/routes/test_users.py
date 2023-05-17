"""Test users router."""
import httpx
from alpaca_partner_backend.api.routes.users import get_current_user
from alpaca_partner_backend.database.mongo import MongoDatabase
from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models import AuthCredentials, UserCreate
from alpaca_partner_backend.models.user import User
from fastapi.testclient import TestClient

ROUTER = Routers.USERS.value


def test_get_current_user(
    database: MongoDatabase,
    mock_user: UserCreate,
) -> None:
    """Test create_user method."""
    user = get_current_user(database=database, _email=mock_user.email)
    assert isinstance(user, User)


def test_login(mock_api_client_with_user: TestClient, mock_user: UserCreate) -> None:
    """Test POST method on the accounts router."""
    response = mock_api_client_with_user.post(
        url=ROUTER + "/login",
        json=AuthCredentials(
            email=mock_user.email,
            password=mock_user.password,
        ).dict(),
    )
    assert httpx.codes.is_success(response.status_code)
