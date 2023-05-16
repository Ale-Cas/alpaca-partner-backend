"""Accounts endpoint router."""

import logging

from alpaca.broker import Account, CreateAccountRequest
from fastapi import APIRouter, Depends

from alpaca_broker.api.common import get_broker_client
from alpaca_broker.database import MongoDatabase, get_db
from alpaca_broker.enums import Routers
from alpaca_broker.models import UserCreate

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
    password: str,
    database: MongoDatabase = Depends(get_db),
) -> Account:
    """Create an Alpaca account from the account request.

    Parameters
    ----------
    `account_request`: CreateAccountRequest
        The parameters for the account request.

    Returns
    -------
    Account:
        The account that has been created.
    """
    insert_result = database.create_user(
        UserCreate(
            email=account_request.contact.email_address,
            password=password,
        )
    )
    log.info("User %s created", insert_result.inserted_id)
    log.info("Account creation request.")
    log.info(account_request.dict(exclude_none=True))
    account = broker_client.create_account(account_request)
    assert isinstance(account, Account), "The account has not being parsed for pydantic validation."
    return account
