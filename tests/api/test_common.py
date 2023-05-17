"""Test the common module."""


from alpaca.broker import BrokerClient
from alpaca_partner_backend.api.common import get_broker_client


def test_broker_client() -> None:
    """Test broker client initialization with env variables."""
    client = get_broker_client()
    assert isinstance(client, BrokerClient)
