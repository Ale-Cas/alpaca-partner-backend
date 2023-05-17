"""Base model for the MongoDB doc."""
from bson.objectid import ObjectId
from pydantic import BaseModel, Extra, Field


class DatabaseDocument(BaseModel):
    """Configuration of pydantic BaseModel for documents arriving from MongoDB queries."""

    id: ObjectId = Field(alias="_id")  # noqa: A003

    class Config:
        """Configuration class."""

        validate_all = True
        validate_assignment = True
        use_enum_values = True
        arbitrary_types_allowed = True
        extra = Extra.forbid
