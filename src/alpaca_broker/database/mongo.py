"""MongoDB client implementation class for the broker backend."""
from fastapi import HTTPException, status
from pydantic import EmailStr
from pymongo import MongoClient
from pymongo.collection import Collection, InsertOneResult
from pymongo.database import Database

from alpaca_broker.models import User, UserCreate
from alpaca_broker.settings import SETTINGS
from alpaca_broker.utils.security import get_password_hash, verify_password


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
        self.database: Database = client["sandbox"]
        self.users_collection: Collection = self.database["users"]
        self.users_collection.create_index("email", unique=True)

    def create_user(self, user_to_create: UserCreate) -> InsertOneResult:
        """Create a new user with the email and the hash of the password provided."""
        return self.users_collection.insert_one(
            UserCreate(
                email=user_to_create.email, password=get_password_hash(user_to_create.password)
            ).dict()
        )

    def get_user_by_email(self, email: EmailStr) -> User:
        """Get the user by email."""
        return self.users_collection.find_one(filter={"email": str(email)})

    def authenticate_user(
        self,
        email: EmailStr,
        password: str,
    ) -> User:
        """Authenticate user password."""
        user = self.get_user_by_email(email=email)
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
