"""Test the parsers module."""
from alpaca.broker import Account

from alpaca_partner_backend.api.parsers import parse_account_to_jsonable, parse_activities
from alpaca_partner_backend.models.api import AccountJson
from tests.api.conftest import create_dummy_non_trade_activities, create_dummy_trade_activities


def test_parse_account_to_jsonable(alpaca_account: Account) -> None:
    """Test parse_account_to_jsonable."""
    _json_acc = parse_account_to_jsonable(alpaca_account)
    assert isinstance(_json_acc, AccountJson)


def test_parse_trade_activities() -> None:
    """Test parse_activities."""
    trades = create_dummy_trade_activities()
    parsed_activities = parse_activities(trades)
    assert isinstance(parsed_activities, list)


def test_parse_non_trade_activities() -> None:
    """Test parse_activities on NTAs."""
    ntas = create_dummy_non_trade_activities()
    parsed_activities = parse_activities(ntas)
    assert isinstance(parsed_activities, list)
