"""Base models for the user."""

from uuid import UUID

from pydantic import BaseModel, EmailStr

from alpaca_broker.models import DatabaseDocument


class UserBase(DatabaseDocument):
    """Base model for the User stored in MongoDB."""

    email: EmailStr
    alpaca_account_id: UUID
    alpaca_account_number: int


class User(UserBase):
    """User data model for the User stored in MongoDB."""

    hashed_password: str


class UserOut(UserBase):
    """Output model for the User."""


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
