"""Utils for security and encoding."""
from datetime import datetime, timedelta
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from alpaca_broker.settings import SETTINGS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Get the hash of the password provided."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that the plain and hashed password match up."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create the JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES, minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SETTINGS.AUTH_SECRET_KEY, algorithm=SETTINGS.HASHING_ALGORITHM)
