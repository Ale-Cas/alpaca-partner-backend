"""Accounts endpoint router."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import EmailStr

from alpaca_partner_backend.api.parsers import parse_user_to_output
from alpaca_partner_backend.database import MongoDatabase, get_db
from alpaca_partner_backend.enums.api import Routers
from alpaca_partner_backend.models import AuthCredentials, Token, User, UserOut
from alpaca_partner_backend.settings import SETTINGS
from alpaca_partner_backend.utils.security import create_access_token

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.USERS.value,
    tags=[Routers.USERS.name],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    database: MongoDatabase = Depends(get_db),
    token: str | None = Depends(oauth2_scheme),
    _email: EmailStr | None = None,
) -> User:
    """Function to get the current user and validate it's credentials."""
    assert token or _email, "You must provide an oauth2 token or an email."
    _headers = {"WWW-Authenticate": "Bearer"}
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers=_headers,
    )
    if not _email and token:
        try:
            payload = jwt.decode(
                token, SETTINGS.AUTH_SECRET_KEY, algorithms=[SETTINGS.HASHING_ALGORITHM]
            )
            _email = payload.get("sub")
            if _email is None:
                raise credentials_exception
        except JWTError as jwt_exception:
            raise credentials_exception from jwt_exception
    return database.get_user_by_email(email=_email)


@router.post("/register")
def register(
    credentials: AuthCredentials,
    database: MongoDatabase = Depends(get_db),
) -> UserOut:
    """Endpoint to log-in and get the JWT access token."""
    database.create_user(auth_credentials=credentials)
    return parse_user_to_output(get_current_user(database=database, _email=credentials.email))


@router.post("/login")
def login(
    credentials: AuthCredentials,
    database: MongoDatabase = Depends(get_db),
) -> Token:
    """Endpoint to log-in and get the JWT access token."""
    user = database.authenticate_user(
        email=credentials.email,
        password=credentials.password,
    )
    access_token = create_access_token(
        data={"sub": user.email},
    )

    return Token(access_token=access_token, token_type="bearer")
