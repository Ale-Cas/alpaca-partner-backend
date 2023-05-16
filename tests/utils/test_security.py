"""Test security utils."""


from alpaca_broker.utils.security import create_access_token, get_password_hash, verify_password
from tests.conftest import TEST_EMAIL, TEST_PASSWORD


def test_get_password_hash() -> None:
    """Test the function that get the hash of the password provided."""
    hashed = get_password_hash(password=TEST_PASSWORD)
    assert isinstance(hashed, str)


def test_verify_password() -> None:
    """Test the verify password function."""
    assert verify_password(
        plain_password=TEST_PASSWORD, hashed_password=get_password_hash(password=TEST_PASSWORD)
    )


def test_create_access_token() -> None:
    """Test the JWT access token creation."""
    token = create_access_token(data={"sub": TEST_EMAIL})
    assert isinstance(token, str)
