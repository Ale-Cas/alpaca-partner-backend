"""Base models for requests and responses of the API."""
from typing import Any
from uuid import uuid4

from alpaca.broker import (
    AccountDocument,
    Agreement,
    Contact,
    Disclosures,
    Identity,
    SupportedCurrencies,
    TrustedContact,
)
from alpaca.broker import CreateAccountRequest as AlpacaCreateAccountRequest
from alpaca.trading.enums import AccountStatus
from pydantic import BaseModel


def _parse_optional_id_in_documents(account_data: dict[str, Any]) -> None:
    """
    Utility to parse optional ID in the documents array in the account.

    This will only be needed until the ID is not optional in alpaca-py AccountDocument class.
    """
    docs = account_data.get("documents", None)
    if docs:
        for doc in docs:
            if isinstance(doc, dict):
                _id = doc.get("id", None)
                doc["id"] = _id if _id else str(uuid4())


class CreateAccountRequest(AlpacaCreateAccountRequest):
    """
    Extensions of the CreateAccountRequest from alpaca-py.

    This includes the unashed password that is needed to create the user
    and then the account from the alpaca_partner_backend API.
    """

    password: str

    def __init__(self, **data: Any) -> None:
        """Initialize and parse id."""
        _parse_optional_id_in_documents(data)
        super().__init__(**data)


class AccountJson(BaseModel):
    """Jsonable Alpaca Account."""

    id: str  # noqa: A003
    account_number: str
    status: AccountStatus
    crypto_status: AccountStatus | None = None
    currency: str
    last_equity: str
    created_at: str
    contact: Contact | None = None
    identity: Identity | None = None
    disclosures: Disclosures | None = None
    agreements: list[Agreement] | None = None
    documents: list[AccountDocument] | None = None
    trusted_contact: TrustedContact | None = None

    def __init__(self, **data: Any) -> None:
        """Initialize and parse id."""
        _parse_optional_id_in_documents(data)
        super().__init__(**data)


class AccountTrading(BaseModel):
    """Account trading information."""

    equity: float
    cash: float
    buying_power: float
    currency: SupportedCurrencies
    daytrade_count: int


class JournalRequestBody(BaseModel):
    """Journal request body."""

    to_user: bool
    amount: float
