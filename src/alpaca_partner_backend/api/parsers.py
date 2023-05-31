"""Parse models for the API endpoints."""
import pandas as pd
from alpaca.broker import Account, ActivityType, TradeAccount
from alpaca.data import Quote
from alpaca.trading import BaseActivity, OrderSide

from alpaca_partner_backend.enums import ActivityName
from alpaca_partner_backend.models import (
    AccountJson,
    AccountTrading,
    Activity,
    QuoteJson,
    User,
    UserOut,
)


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
    return AccountTrading(**account.dict())


def parse_quote_to_jsonable(quote: Quote) -> QuoteJson:
    """Parse the quote to a jsonable version of it."""
    return QuoteJson(**quote.dict())


def parse_user_to_output(user: User) -> UserOut:
    """
    Parse the user to a jsonable version for the frontend.

    Takes care of not returning passwords or IDs.
    """
    return UserOut(email=user.email)


def parse_df_to_list(df: pd.DataFrame) -> list[list[str]]:
    """Parse a dataframe to a list of its headers and values."""
    return [df.columns.to_list(), *df.values.tolist()]


def parse_activities(account_activities: list[BaseActivity]) -> list[Activity]:
    """Parse activities from Alpaca's API to a common Activity base model."""
    _activities = []
    for activity in account_activities:
        _type = activity.activity_type
        _activity = activity.dict()
        _side = _activity.get("side", None)
        _date = (
            _activity.get("date", None)
            or _activity.get("transaction_time", None)
            or _activity.get("system_date", None)
        )
        _amount = _activity.get("net_amount", None) or round(
            _activity.get("price", 0) * _activity.get("qty", 0), 2
        )
        if _type == ActivityType.FILL:
            _name = ActivityName.BUY_ORDER if _side == OrderSide.BUY else ActivityName.SELL_ORDER
        elif _type == ActivityType.JNLC:
            _name = ActivityName.JNLC_DEPOSIT if _amount > 0 else ActivityName.JNLC_WITHDRAWAL
        elif _type == ActivityType.CSD:
            _name = ActivityName.ACH_DEPOSIT
        elif _type == ActivityType.CSW:
            _name = ActivityName.ACH_WITHDRAWAL
        elif _type == ActivityType.FEE:
            _description = str(_activity.get("description"))
            if "REG" in _description:
                _name = ActivityName.REG_FEE
            elif "TAF" in _description:
                _name = ActivityName.TAF_FEE
            else:
                _name = ActivityName.FEE
        elif _type == ActivityType.DIV:
            _name = ActivityName.DIV
        else:
            _name = _type
        _activities.append(
            Activity(
                activity_type=_type,
                activity_name=_name,
                date=_date,
                amount=_amount,
                symbol=_activity.get("symbol", None),
            )
        )
    return _activities
