"""Router for market data."""
import logging

from alpaca.broker import BrokerClient, CreateJournalRequest, Journal, JournalEntryType
from fastapi import APIRouter, Depends

from alpaca_partner_backend.api.common import get_broker_client
from alpaca_partner_backend.api.routes.accounts import _get_account_id_by_email
from alpaca_partner_backend.api.routes.users import get_current_user
from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models import JournalRequestBody, User
from alpaca_partner_backend.settings import SETTINGS

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.FUNDING.value,
    tags=[Routers.FUNDING.name],
)


@router.post("/journal")
def create_journal(
    request_body: JournalRequestBody,
    broker_client: BrokerClient = Depends(get_broker_client),
    user: User = Depends(get_current_user),
) -> Journal:
    """
    Create a journal to transfer money to/from the sweep account to/from the user.

    Parameters
    ----------
    `to_user`: bool
        wether to move the money to the user (true) or from the user (false).
    `amount`: float
        the amount of the cash journal.
    """
    user_acct_id = _get_account_id_by_email(user.email, broker_client=broker_client)
    journal = broker_client.create_journal(
        CreateJournalRequest(
            from_account=SETTINGS.SWEEP_ACCOUNT_ID if request_body.to_user else user_acct_id,
            to_account=user_acct_id if request_body.to_user else SETTINGS.SWEEP_ACCOUNT_ID,
            entry_type=JournalEntryType.CASH,
            amount=request_body.amount,
        )
    )
    assert isinstance(journal, Journal)
    return journal
