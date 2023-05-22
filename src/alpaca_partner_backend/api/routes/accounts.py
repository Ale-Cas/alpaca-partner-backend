"""Accounts endpoint router."""

import logging

from alpaca.broker import Account
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from alpaca_partner_backend.api import parsers
from alpaca_partner_backend.api.common import get_broker_client
from alpaca_partner_backend.api.routes.users import get_current_user
from alpaca_partner_backend.database import MongoDatabase, get_db
from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models import (
    AccountJson,
    AccountTrading,
    AuthCredentials,
    CreateAccountRequest,
    User,
)

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
        AuthCredentials(
            email=account_request.contact.email_address,
            password=account_request.password,
        )
    )
    log.info("User %s created", insert_result.inserted_id)
    log.info("Account creation request.")
    account = broker_client.create_account(account_request)
    assert isinstance(account, Account), "The account has not being parsed for pydantic validation."
    return parsers.parse_account_to_jsonable(account)


def _get_account_id_by_email(
    email: EmailStr,
) -> str:
    """
    Get the account ID with a specific email.

    Parameters
    ----------
    `email`: EmailStr
        the email of the requested account.

    Raises
    ------
    `HTTPException`:
        Raise 404 if no account with that email address is found.

    Returns
    -------
    `str`:
        the Alpaca account ID with that email.
    """
    accounts = broker_client.get(f"/accounts?query={str(email)}")
    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email address {email} not found",
        )
    return accounts[0].get("id")


@router.get("/")
def get_account_by_email(
    email: EmailStr,
) -> AccountJson:
    """
    Get the account with a specific email.

    Parameters
    ----------
    `email`: EmailStr
        the email of the requested account.

    Returns
    -------
    `AccountJson`:
        the Alpaca account with that email.
    """
    account_id = _get_account_id_by_email(email)
    account = broker_client.get_account_by_id(account_id=account_id)
    return parsers.parse_account_to_jsonable(account)


@router.get("/trading")
def get_account_trading_info(user: User = Depends(get_current_user)) -> AccountTrading:
    """
    Get the account trading information for a specific account ID.

    Parameters
    ----------
    `account_id`: str
        the ID of the account. Gets validated as UUID.

    Returns
    -------
    `AccountTrading`:
        the trading information for that account.
    """
    return parsers.parse_account_to_trading(
        broker_client.get_trade_account_by_id(account_id=_get_account_id_by_email(user.email))
    )
