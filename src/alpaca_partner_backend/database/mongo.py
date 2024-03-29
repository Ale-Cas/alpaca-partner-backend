"""MongoDB client implementation class for the broker backend."""
from fastapi import HTTPException, status
from pydantic import EmailStr
from pymongo import MongoClient
from pymongo.collection import Collection, InsertOneResult
from pymongo.database import Database

from alpaca_partner_backend.models import AuthCredentials, User
from alpaca_partner_backend.settings import SETTINGS
from alpaca_partner_backend.utils.security import get_password_hash, verify_password


class MongoDatabase:
    """MongoDB database client."""

    def __init__(self, client: MongoClient = MongoClient(host=SETTINGS.MONGO_DB_URI)) -> None:
        """
        MongoDB database interface.

        Parameters
        ----------
        `client`: MongoClient
            The MongoClient from pymongo for the DB operations.
            In the tests is overridden using mongomock.
        """
        self.client = client
        self.database: Database = client["sandbox"]
        self.users_collection: Collection = self.database["users"]
        self.users_collection.create_index("email", unique=True)

    def create_user(self, auth_credentials: AuthCredentials) -> InsertOneResult:
        """Create a new user with the email and the hash of the password provided."""
        return self.users_collection.insert_one(
            AuthCredentials(
                email=auth_credentials.email, password=get_password_hash(auth_credentials.password)
            ).dict()
        )

    def get_all_users(self) -> list[User]:
        """Get all users in the database."""
        return [User(u) for u in list(self.users_collection.find())]

    def get_user_by_email(self, email: EmailStr) -> User:
        """Get the user by email."""
        doc = self.users_collection.find_one(filter={"email": str(email)})
        assert doc, f"Document with email {email} not found."
        return User(**doc)

    def authenticate_user(
        self,
        email: EmailStr,
        password: str,
    ) -> User:
        """Authenticate user password."""
        user = self.get_user_by_email(email=email)
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
