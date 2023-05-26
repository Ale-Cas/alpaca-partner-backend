"""Orders endpoints router."""
import logging

from alpaca.broker import BrokerClient, Order
from alpaca.trading import GetOrdersRequest, OrderRequest, QueryOrderStatus
from fastapi import APIRouter, Depends

from alpaca_partner_backend.api.common import get_broker_client
from alpaca_partner_backend.api.routes.accounts import _get_account_id_by_email
from alpaca_partner_backend.api.routes.users import get_current_user
from alpaca_partner_backend.enums import Routers
from alpaca_partner_backend.models import (
    User,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.ORDERS.value,
    tags=[Routers.ORDERS.name],
)


@router.post("/")
def create_order(
    order_request: OrderRequest,
    user: User = Depends(get_current_user),
    broker_client: BrokerClient = Depends(get_broker_client),
) -> Order:
    """Create an order for the current user account.

    Parameters
    ----------
    `order_request`: OrderRequest
        The parameters for the order request.

    Returns
    -------
    Order:
        The order that has been created.
    """
    acct_id = _get_account_id_by_email(email=user.email, broker_client=broker_client)
    # using OrderRequest from trading module since the one from Broker it's not working
    order = broker_client.submit_order_for_account(account_id=acct_id, order_data=order_request)  # type: ignore
    assert isinstance(order, Order)
    return order


@router.get("/")
def get_all_orders(
    limit: int = 500,
    user: User = Depends(get_current_user),
    broker_client: BrokerClient = Depends(get_broker_client),
) -> list[Order]:
    """Create an order for the current user account.

    Parameters
    ----------
    `orders_request`: OrderRequest
        The parameters for the order request.

    Returns
    -------
    `list[Order]`:
        The orders for the current user account.
    """
    acct_id = _get_account_id_by_email(email=user.email, broker_client=broker_client)
    broker_client._use_raw_data = True
    _orders = broker_client.get_orders_for_account(
        account_id=acct_id,
        filter=GetOrdersRequest(
            status=QueryOrderStatus.ALL,
            limit=limit,
        ),
    )
    broker_client._use_raw_data = False
    orders = []
    for raw_order in _orders:
        assert isinstance(raw_order, dict)
        o = (
            Order(**raw_order)
            if isinstance(raw_order.get("commission", None), float)
            else Order(**raw_order, commission=0)
        )
        orders.append(o)
    return orders
