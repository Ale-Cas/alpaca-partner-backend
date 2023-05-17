"""Base models for requests and responses of the API."""
from alpaca.broker import AccountDocument, Agreement, Contact, Disclosures, Identity, TrustedContact
from alpaca.trading.enums import AccountStatus
from pydantic import BaseModel


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

    # _transform_cloud = validator("id", allow_reuse=True)(lambda x: str(x) if x else x)

    # class Config:
    #     """Json encoder configuration."""

    #     json_encoders = {
    #         UUID: lambda _id: _id,
    #     }
