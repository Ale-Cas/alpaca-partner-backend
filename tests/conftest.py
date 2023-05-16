"""Configurations, mocks, constants and fixtures that are used in the tests."""
import pytest
import mongomock

from alpaca_broker.database.mongo import MongoDatabase
from alpaca_broker.models import UserCreate

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


@pytest.fixture()
def mock_database() -> MongoDatabase:
    """
    Fixture for mocking the MongoDB database host.

    Uses the client from mongomock to create a fake client.
    """
    return MongoDatabase(
        client=mongomock.MongoClient(),
    )
