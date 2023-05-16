"""Base model for the MongoDB doc."""
from pydantic import BaseModel, Extra, Field


class DatabaseDocument(BaseModel):
    """Configuration of pydantic BaseModel for documents arriving from MongoDB queries."""

    id: str = Field(alias="_id")  # noqa: A003

    class Config:
        """Configuration class."""

        validate_all = True
        validate_assignment = True
        use_enum_values = True
        extra = Extra.forbid
