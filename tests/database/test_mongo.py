"""Test suite for the mongo module."""

from alpaca_broker.database import MongoDatabase, get_db
from alpaca_broker.models.user import UserCreate


def test_get_db() -> None:
    """Test get_db dependency injection function."""
    database = get_db()
    assert isinstance(database, MongoDatabase)


# def test_create_user(database: MongoDatabase, mock_user: UserCreate) -> None:
#     """Test create_user method."""
#     insert_result = database.create_user(user_to_create=mock_user)
#     assert insert_result.acknowledged
#     assert insert_result.inserted_id


def test_mock_create_user(mock_database: MongoDatabase, mock_user: UserCreate) -> None:
    """Test create_user method."""
    insert_result = mock_database.create_user(user_to_create=mock_user)
    assert insert_result.acknowledged
    assert insert_result.inserted_id
