"""Accounts endpoint router."""

import logging
from typing import Any

import pandas as pd
from alpaca.broker import Account, BrokerClient, GetAccountActivitiesRequest, TradeAccount
from alpaca.trading import GetPortfolioHistoryRequest, PortfolioHistory
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
from alpaca_partner_backend.models.api import Activity

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.ACCOUNTS.value,
    tags=[Routers.ACCOUNTS.name],
)


@router.post("/")
def create_account(
    account_request: CreateAccountRequest,
    database: MongoDatabase = Depends(get_db),
    broker_client: BrokerClient = Depends(get_broker_client),
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
    broker_client: BrokerClient,
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
    _email = str(email)
    _not_found_error = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with email address {_email} not found",
    )
    accounts = broker_client.get(f"/accounts?query={_email}&entities=contact")
    if not accounts:
        raise _not_found_error
    # iterate over the accounts that match the query to find
    # the account with the same email address
    for account in accounts:
        if account["contact"]["email_address"] == _email:
            return account["id"]
    raise _not_found_error


@router.get("/")
def get_account_info(
    user: User = Depends(get_current_user),
    broker_client: BrokerClient = Depends(get_broker_client),
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
    account_id = _get_account_id_by_email(user.email, broker_client=broker_client)
    account = broker_client.get_account_by_id(account_id=account_id)
    return parsers.parse_account_to_jsonable(account)


@router.get("/trading")
def get_account_trading_info(
    user: User = Depends(get_current_user),
    broker_client: BrokerClient = Depends(get_broker_client),
) -> AccountTrading:
    """
    Get the account trading information for a specific account ID.

    Returns
    -------
    `AccountTrading`:
        the trading information for that account.
    """
    return parsers.parse_account_to_trading(
        broker_client.get_trade_account_by_id(
            account_id=_get_account_id_by_email(user.email, broker_client=broker_client)
        )
    )


@router.get("/portfolio/history")
def get_portfolio_history(
    timeperiod: str = "1M",
    user: User = Depends(get_current_user),
    broker_client: BrokerClient = Depends(get_broker_client),
) -> list[list[Any]]:
    """
    Get the account trading information for a specific account ID.

    Parameters
    ----------
    `timeperiod`: (Optional[str])
        the duration of the data in number + unit, such as 1D.
        Unit can be D for day, W for week, M for month and A for year.
        Defaults to 1M.

    Returns
    -------
    `list[EquityEOD]`:
        the list of equity values at end of each day for that account.
    """
    _acct_id = _get_account_id_by_email(user.email, broker_client=broker_client)
    ptf_history = broker_client.get_portfolio_history_for_account(
        account_id=_acct_id,
        history_filter=GetPortfolioHistoryRequest(
            timeframe="1D",
            period=timeperiod,
        ),
    )
    assert isinstance(ptf_history, PortfolioHistory)
    acct_trading = broker_client.get_trade_account_by_id(account_id=_acct_id)
    assert isinstance(acct_trading, TradeAccount)
    ptf_history_df = pd.DataFrame(
        {
            "day": ptf_history.timestamp,
            "equity": ptf_history.equity,
        }
    )
    # replace today's equity from portfolio history
    # with the account current equity
    assert acct_trading.equity
    ptf_history_df.iloc[-1, 1] = float(acct_trading.equity)
    ptf_history_df["day"] = pd.to_datetime(ptf_history_df["day"], unit="s").dt.strftime("%Y-%m-%d")
    return parsers.parse_df_to_list(ptf_history_df)


@router.get("/activities")
def get_account_activities(
    user: User = Depends(get_current_user),
    broker_client: BrokerClient = Depends(get_broker_client),
) -> list[Activity]:
    """
    Get the account trading information for a specific account ID.

    Parameters
    ----------
    `timeperiod`: (Optional[str])
        the duration of the data in number + unit, such as 1D.
        Unit can be D for day, W for week, M for month and A for year.
        Defaults to 1M.

    Returns
    -------
    `list[EquityEOD]`:
        the list of equity values at end of each day for that account.
    """
    activities = broker_client.get_account_activities(
        activity_filter=GetAccountActivitiesRequest(
            account_id=_get_account_id_by_email(user.email, broker_client=broker_client)
        )
    )
    assert isinstance(activities, list)
    return parsers.parse_activities(activities)
