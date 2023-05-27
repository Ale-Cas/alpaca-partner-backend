"""Test funding router."""
import httpx
from alpaca.broker import Journal
from alpaca.common.enums import BaseURL
from fastapi.testclient import TestClient
from requests_mock import Mocker

from alpaca_partner_backend.enums import Routers
from tests.conftest import TEST_EMAIL

ROUTER = Routers.FUNDING.value


def test_mock_post_funding_journal(
    reqmock: Mocker,
    mock_get_alpaca_account_by_email: str,
    mock_api_client_with_user: TestClient,
) -> None:
    """Test GET method on the accounts router with email in the path."""
    amt = 10
    reqmock.get(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/accounts?query={str(TEST_EMAIL)}",
        text=mock_get_alpaca_account_by_email,
    )
    reqmock.post(
        url=f"{BaseURL.BROKER_SANDBOX}/v1/journals",
        text="""
        {
            "id": "1c0563fb-40b9-3d89-89d5-a976d1b45e4f",
            "to_account": "2c0563fb-40b9-3d89-89d5-a976d1b45e4f",
            "entry_type": "JNLC",
            "status": "executed",
            "from_account": "3c0563fb-40b9-3d89-89d5-a976d1b45e4f",
            "settle_date": "2020-12-24",
            "system_date": "2020-12-24",
            "net_amount": "10",
            "description": "this is a test journal",
            "currency": "USD"
        }
        """,
    )
    response = mock_api_client_with_user.post(
        url=ROUTER + "/journal",
        json={
            "to_user": True,
            "amount": amt,
        },
    )
    assert httpx.codes.is_success(response.status_code)
    journal = Journal(**response.json())
    assert journal.net_amount == amt
