"""Accounts endpoint router."""

from alpaca.broker import Account, CreateAccountRequest
from fastapi import APIRouter

from alpaca_broker.api.common import get_broker_client
from alpaca_broker.enums.api import Routers

router = APIRouter(
    prefix=Routers.ACCOUNTS.value,
    tags=[Routers.ACCOUNTS.name],
)

broker_client = get_broker_client()


@router.post("/")
def create_account(
    account_request: CreateAccountRequest,
    # broker_client: BrokerClient = Depends(get_broker_client),
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
    account = broker_client.create_account(account_request)
    assert isinstance(account, Account), "The account has not being parsed for pydantic validation."
    return account
