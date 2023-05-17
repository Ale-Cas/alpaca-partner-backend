"""Test the parsers module."""
from alpaca.broker import Account

from alpaca_broker.api.parsers import parse_account_to_jsonable
from alpaca_broker.models.api import AccountJson


def test_parse_account_to_jsonable(alpaca_account: Account) -> None:
    """Test parse_account_to_jsonable."""
    _json_acc = parse_account_to_jsonable(alpaca_account)
    assert isinstance(_json_acc, AccountJson)
