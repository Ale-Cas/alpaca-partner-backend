"""Test alpaca-broker."""

import alpaca_broker


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(alpaca_broker.__name__, str)
