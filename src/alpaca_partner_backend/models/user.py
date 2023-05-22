"""Base models for the user."""

from uuid import UUID

from pydantic import BaseModel, EmailStr

from alpaca_partner_backend.models import DatabaseDocument


class UserBase(BaseModel):
    """Base model for the User stored in MongoDB."""

    email: EmailStr


class User(UserBase, DatabaseDocument):
    """User data model for the User stored in MongoDB.

    Attributes
    ----------
    `password`: str
        Hashed password from the database.
    """

    password: str


class UserOut(UserBase):
    """Output model for the User."""

    email: EmailStr


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
