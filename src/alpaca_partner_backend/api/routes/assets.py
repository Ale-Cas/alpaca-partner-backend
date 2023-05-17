"""Router for assets endpoints."""

import logging
from functools import lru_cache

from alpaca.trading import Asset, GetAssetsRequest
from fastapi import APIRouter

from alpaca_partner_backend.api.common import get_broker_client
from alpaca_partner_backend.enums import Routers

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.ASSETS.value,
    tags=[Routers.ASSETS.name],
)
broker_client = get_broker_client()


@lru_cache
def _cache_broker_api_call(assets_request: GetAssetsRequest | None = None) -> list[Asset]:
    """
    Cache the broker API call to the assets endpoint.

    Least-recently-used cache but in the future it might be
    considered to use mongo to store an assets collection.
    """
    assets = broker_client.get_all_assets(assets_request)
    assert isinstance(assets, list)
    return assets


@router.get("/")
def get_assets(assets_request: GetAssetsRequest | None = None) -> list[Asset]:
    """
    Get the account with a specific email.

    Parameters
    ----------
    `account_request`: CreateAccountRequest
        The parameters for the account request.

    Returns
    -------
    AccountJson:
        The account that has been created.
    """
    return _cache_broker_api_call(assets_request=assets_request)
