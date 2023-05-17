"""Base models for the user."""

from uuid import UUID

from alpaca.broker import CreateAccountRequest as AlpacaCreateAccountRequest
from alpaca_partner_backend.models import DatabaseDocument
from pydantic import BaseModel, EmailStr


class UserBase(DatabaseDocument):
    """Base model for the User stored in MongoDB."""

    email: EmailStr


class User(UserBase):
    """User data model for the User stored in MongoDB.

    Attributes
    ----------
    `password`: str
        Hashed password from the database.
    """

    password: str


class UserOut(UserBase):
    """Output model for the User."""


class UserWithAlpacaAccount(UserBase):
    """Output model for the User."""

    alpaca_account_id: UUID
    alpaca_account_number: int


class AuthCredentials(BaseModel):
    """
    Model to represent the user credentials.

    Attributes
    ----------
    `email` : EmailStr
        Email address used as username.
    `password`` : str
        Plain text password.
    """

    email: EmailStr
    password: str  # plain text


class UserCreate(AuthCredentials):
    """Base model to validate user creation request."""


class Token(BaseModel):
    """
    Model to represent the user auth token.

    Attributes
    ----------
    - ``access_token`` : Token to access the API.
    - ``token_type`` : The type of token.
    """

    access_token: str
    token_type: str


class CreateAccountRequest(AlpacaCreateAccountRequest):
    """
    Extensions of the CreateAccountRequest from alpaca-py.

    This includes the unashed password that is needed to create the user
    and then the account from the alpaca_partner_backend API.
    """

    password: str
