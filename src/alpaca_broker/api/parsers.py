"""Parse models for the API endpoints."""
from alpaca.broker import Account

from alpaca_broker.models import AccountJson


def parse_account_to_jsonable(account: Account) -> AccountJson:
    """
    Parse the account to a jsonable version of it.

    Takes care of UUID to str conversion.
    """
    return AccountJson(id=str(account.id), **account.dict(exclude={"id"}))
