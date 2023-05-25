"""Enums for the FastAPI implementation."""
from enum import Enum


class Routers(str, Enum):
    """Possible routers of the API."""

    ACCOUNTS = "/accounts"
    ASSETS = "/assets"
    FUNDING = "/funding"
    ORDERS = "/orders"
    PRICES = "/prices"
    USERS = "/users"


class BarsField(str, Enum):
    """Field of a BarSet object."""

    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"
    TRADE_COUNT = "trade_count"
    VWAP = "vwap"


class ActivityName(str, Enum):
    """Human readable activity name mapped from the activity type."""

    BUY_ORDER = "Buy Order"
    SELL_ORDER = "Sell Order"
    JNLC_DEPOSIT = "Journal Deposit"
    JNLC_WITHDRAWAL = "Journal Withdrawal"
    ACH_DEPOSIT = "ACH Deposit"
    ACH_WITHDRAWAL = "ACH Withdrawal"
    REG_FEE = "REG Fee"
    TAF_FEE = "TAF Fee"
    DIV = "Dividend"
    SPLIT = "Split"
    SPIN = "Spin-off"
    MA = "Merger / Acquisition"
    JNLS = "Stock Journal"

    # other activities
    ACATC = "ACATC"
    ACATS = "ACATS"
    CIL = "CIL"
    DIVCGL = "DIVCGL"
    DIVCGS = "DIVCGS"
    DIVNRA = "DIVNRA"
    DIVROC = "DIVROC"
    DIVTXEX = "DIVTXEX"
    INT = "INT"
    PTC = "PTC"
    REORG = "REORG"
