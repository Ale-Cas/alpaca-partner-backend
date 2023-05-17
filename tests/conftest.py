"""Configurations, mocks, constants and fixtures that are used in the tests."""
import json
import typing

import mongomock
import pytest
from alpaca.broker import Account
from fastapi.testclient import TestClient
from requests_mock import Mocker

from alpaca_partner_backend.api.main import app
from alpaca_partner_backend.database import get_db
from alpaca_partner_backend.database.mongo import MongoDatabase
from alpaca_partner_backend.models import CreateAccountRequest, UserCreate
from tests.api import conftest

# Constants:
TEST_EMAIL = "test@gmail.com"
TEST_PASSWORD = "abc123"


@pytest.fixture()
def mock_user() -> UserCreate:
    """Fixture for mocking a user creation."""
    return UserCreate(email=TEST_EMAIL, password=TEST_PASSWORD)


@pytest.fixture()
def database() -> MongoDatabase:
    """Fixture for the database."""
    return MongoDatabase()


@typing.no_type_check
@pytest.fixture(autouse=True)
def mock_database() -> MongoDatabase:
    """
    Fixture for mocking the MongoDB database host.

    Uses the client from mongomock to create a fake client.
    """
    _mockdb = MongoDatabase(
        client=mongomock.MongoClient(),
    )
    yield _mockdb
    _mockdb.client.drop_database(_mockdb.database)
    _mockdb.client.close()


@pytest.fixture()
def mock_database_with_user(
    mock_database: MongoDatabase,
    mock_user: UserCreate,
) -> MongoDatabase:
    """
    Fixture for mocking the MongoDB database host.

    Uses the client from mongomock to create a fake client.
    """
    insert_result = mock_database.create_user(
        user_to_create=mock_user,
    )
    assert insert_result.acknowledged
    assert insert_result.inserted_id
    return mock_database


@pytest.fixture()
def mock_api_client(mock_database: MongoDatabase) -> TestClient:
    """
    Fixture for mocking the MongoDB database host.

    Uses the client from mongomock to create a fake client.
    """
    app.dependency_overrides[get_db] = lambda: mock_database
    return TestClient(app=app)


@pytest.fixture()
def mock_api_client_with_user(
    mock_database_with_user: MongoDatabase,
) -> TestClient:
    """
    Fixture for mocking the MongoDB database host.

    Uses the client from mongomock to create a fake client.
    """
    app.dependency_overrides[get_db] = lambda: mock_database_with_user
    return TestClient(app=app)


@pytest.fixture()
def mock_alpaca_account_request() -> CreateAccountRequest:
    """Fake Alpaca broker account."""
    return CreateAccountRequest(
        contact=conftest.create_dummy_contact(),
        identity=conftest.create_dummy_identity(),
        disclosures=conftest.create_dummy_disclosures(),
        agreements=conftest.create_dummy_agreements(),
        documents=conftest.create_dummy_account_documents(),
        trusted_contact=conftest.create_dummy_trusted_contact(),
        password=TEST_PASSWORD,
    )


@pytest.fixture()
def reqmock() -> typing.Iterator[Mocker]:
    """Requests mocker."""
    with Mocker() as m:
        yield m


@pytest.fixture()
def alpaca_account(mock_alpaca_account_request: CreateAccountRequest) -> Account:
    """Fake Alpaca broker account in json format for reqmock."""
    return Account(
        id="7ccfd029-9b91-40d0-9b4c-f928385af666",
        account_number="808971365",
        status="SUBMITTED",
        crypto_status="SUBMITTED",
        currency="USD",
        last_equity="0",
        created_at="2022-08-16T20:19:20.547306Z",
        contact=mock_alpaca_account_request.contact,
        identity=mock_alpaca_account_request.identity,
        disclosures=mock_alpaca_account_request.disclosures,
        agreements=mock_alpaca_account_request.agreements,
        documents=mock_alpaca_account_request.documents,
        trusted_contact=mock_alpaca_account_request.trusted_contact,
    )


@pytest.fixture()
def mock_alpaca_account(alpaca_account: Account) -> str:
    """Fake Alpaca broker account in json format for reqmock."""
    return alpaca_account.json()


@pytest.fixture()
def mock_get_alpaca_account_by_email(alpaca_account: Account) -> str:
    """Fake list of 1 Alpaca broker account returned in json format for reqmock."""
    return json.dumps([json.loads(alpaca_account.json())])


@pytest.fixture()
def mock_assets_json() -> str:
    """Mock json response from Alpaca Broker API assets endpoint."""
    return """
        [
            {
              "id": "904837e3-3b76-47ec-b432-046db621571b",
              "class": "us_equity",
              "exchange": "NASDAQ",
              "symbol": "AAPL",
              "name": "Apple Inc. Common Stock",
              "status": "active",
              "tradable": true,
              "marginable": true,
              "shortable": true,
              "easy_to_borrow": true,
              "fractionable": true,
              "last_close_pct_change": "string",
              "last_price": "string"
            }
      ]
      """
