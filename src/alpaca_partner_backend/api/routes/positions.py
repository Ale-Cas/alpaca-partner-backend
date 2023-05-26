"""Router for market data."""
import logging

from alpaca.broker import BrokerClient
from alpaca.trading import Order, Position
from fastapi import APIRouter, Depends

from alpaca_partner_backend.api.common import get_broker_client
from alpaca_partner_backend.api.routes.accounts import _get_account_id_by_email
from alpaca_partner_backend.api.routes.users import get_current_user
from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models import User

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.POSITIONS.value,
    tags=[Routers.POSITIONS.name],
)


@router.get("/")
def get_positions(
    user: User = Depends(get_current_user),
    broker_client: BrokerClient = Depends(get_broker_client),
) -> list[Position]:
    """Get the positions for the current user account."""
    positions = broker_client.get_all_positions_for_account(
        account_id=_get_account_id_by_email(email=user.email, broker_client=broker_client)
    )
    assert isinstance(positions, list)
    return positions


@router.delete("/{symbol}")
def close_position(
    symbol: str,
    user: User = Depends(get_current_user),
    broker_client: BrokerClient = Depends(get_broker_client),
) -> Order:
    """Close the position in the symbol."""
    broker_client._use_raw_data = True
    raw_closing_order = broker_client.close_position_for_account(
        account_id=_get_account_id_by_email(email=user.email, broker_client=broker_client),
        symbol_or_asset_id=symbol,
    )
    broker_client._use_raw_data = False
    assert isinstance(raw_closing_order, dict)
    closing_order = Order(**raw_closing_order, commission=0)
    assert isinstance(closing_order, Order)
    return closing_order
