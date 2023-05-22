"""Parse models for the API endpoints."""
from alpaca.broker import Account, TradeAccount

from alpaca_partner_backend.models import AccountJson, AccountTrading, User, UserOut


def parse_account_to_jsonable(account: Account) -> AccountJson:
    """
    Parse the account to a jsonable version of it.

    Takes care of UUID to str conversion.
    """
    return AccountJson(id=str(account.id), **account.dict(exclude={"id"}))


def parse_account_to_trading(account: TradeAccount) -> AccountTrading:
    """
    Parse the account to a jsonable version of it.

    Takes care of UUID to str conversion.
    """
    return AccountTrading(
        equity=account.equity,
        cash=account.cash,
        buying_power=account.buying_power,
        currency=account.currency,
        daytrade_count=account.daytrade_count,
    )


def parse_user_to_output(user: User) -> UserOut:
    """
    Parse the user to a jsonable version for the frontend.

    Takes care of not returning passwords or IDs.
    """
    return UserOut(email=user.email)
