"""Accounts endpoint router."""

import logging

from alpaca.broker import Account
from alpaca.common.exceptions import APIError as BrokerAPIError
from alpaca_partner_backend.api.common import get_broker_client
from alpaca_partner_backend.api.parsers import parse_account_to_jsonable
from alpaca_partner_backend.database import MongoDatabase, get_db
from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models import AccountJson, CreateAccountRequest, UserCreate
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.ACCOUNTS.value,
    tags=[Routers.ACCOUNTS.name],
)

broker_client = get_broker_client()


@router.post("/")
def create_account(
    account_request: CreateAccountRequest,
    database: MongoDatabase = Depends(get_db),
) -> AccountJson:
    """Create an Alpaca account from the account request.

    Parameters
    ----------
    `account_request`: CreateAccountRequest
        The parameters for the account request.

    Returns
    -------
    AccountJson:
        The account that has been created.
    """
    insert_result = database.create_user(
        UserCreate(
            email=account_request.contact.email_address,
            password=account_request.password,
        )
    )
    log.info("User %s created", insert_result.inserted_id)
    log.info("Account creation request.")
    log.info(account_request.dict(exclude_none=True))
    try:
        account = broker_client.create_account(account_request)
    except BrokerAPIError as broker_api_error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An account with the same email address {account_request.contact.email_address} already exists.",
        ) from broker_api_error
    assert isinstance(account, Account), "The account has not being parsed for pydantic validation."
    return parse_account_to_jsonable(account)


@router.get("/{email}")
def get_account_by_email(
    email: EmailStr,
) -> AccountJson:
    """
    Get the account with a specific email.

    Parameters
    ----------
    `account_request`: CreateAccountRequest
        The parameters for the account request.

    Returns
    -------
    AccountJson:
        The account that has been created.
    """
    accounts = broker_client.get(f"/accounts?query={str(email)}")
    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email address {email} not found",
        )
    account_id = accounts[0].get("id")
    assert isinstance(account_id, str)
    try:
        account = broker_client.get_account_by_id(account_id=account_id)
    except BrokerAPIError as broker_api_error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found.",
        ) from broker_api_error
    return parse_account_to_jsonable(account)
