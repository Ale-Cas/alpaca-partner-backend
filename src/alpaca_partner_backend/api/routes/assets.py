"""Router for assets endpoints."""

import logging
from functools import lru_cache

from alpaca.broker import BrokerClient
from alpaca.common.exceptions import APIError
from alpaca.trading import Asset, AssetClass, AssetExchange, AssetStatus, GetAssetsRequest
from fastapi import APIRouter, Depends, HTTPException, status

from alpaca_partner_backend.api.common import get_broker_client
from alpaca_partner_backend.enums import Routers

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.ASSETS.value,
    tags=[Routers.ASSETS.name],
)


@lru_cache
def _cache_broker_api_call(
    broker_client: BrokerClient,
    status: AssetStatus | None = None,
    asset_class: AssetClass | None = None,
    exchange: AssetExchange | None = None,
) -> list[Asset]:
    """
    Cache the broker API call to the assets endpoint.

    Least-recently-used cache but in the future it might be
    considered to use mongo to store an assets collection.
    """
    assets = broker_client.get_all_assets(
        GetAssetsRequest(
            status=status,
            asset_class=asset_class,
            exchange=exchange,
        )
    )
    assert isinstance(assets, list)
    # filter out assets that are non tradable and not fractionable
    return [a for a in assets if a.tradable is True and a.fractionable is True]


@router.get("/")
def get_assets(
    status: AssetStatus | None = AssetStatus.ACTIVE,
    asset_class: AssetClass | None = None,
    exchange: AssetExchange | None = None,
    broker_client: BrokerClient = Depends(get_broker_client),
) -> list[Asset]:
    """
    Get the assets that match the filters.

    Parameters
    ----------
    `status`: AssetStatus | None = None
    `asset_class`: AssetClass | None = None
    `exchange`: AssetExchange | None = None

    Returns
    -------
    list[Asset]:
        the assets that match the filters.
    """
    return _cache_broker_api_call(
        broker_client=broker_client,
        status=status,
        asset_class=asset_class,
        exchange=exchange,
    )


@router.get("/symbols")
def get_symbols(
    status: AssetStatus | None = None,
    asset_class: AssetClass | None = None,
    exchange: AssetExchange | None = None,
    broker_client: BrokerClient = Depends(get_broker_client),
) -> list[str]:
    """
    Get the account with a specific email.

    Parameters
    ----------
    `status`: AssetStatus | None = None
    `asset_class`: AssetClass | None = None
    `exchange`: AssetExchange | None = None

    Returns
    -------
    list[str]:
        the symbols matching the query parameters.
    """
    return [
        a.symbol
        for a in _cache_broker_api_call(
            broker_client=broker_client,
            status=status,
            asset_class=asset_class,
            exchange=exchange,
        )
    ]


@router.get("/symbols/{symbol}")
def get_asset_by_symbol(
    symbol: str,
    broker_client: BrokerClient = Depends(get_broker_client),
) -> Asset:
    """
    Get the account with a specific email.

    Parameters
    ----------
    `status`: AssetStatus | None = None
    `asset_class`: AssetClass | None = None
    `exchange`: AssetExchange | None = None

    Returns
    -------
    `Asset`:
        the asset with that symbol.
    """
    try:
        asset = broker_client.get_asset(symbol)
    except APIError as broker_api_error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No asset with symbol {symbol} was found.",
        ) from broker_api_error
    assert isinstance(asset, Asset)
    return asset


@router.get("/names")
def get_names(
    status: AssetStatus | None = None,
    asset_class: AssetClass | None = None,
    exchange: AssetExchange | None = None,
    broker_client: BrokerClient = Depends(get_broker_client),
) -> list[str]:
    """
    Get the account with a specific email.

    Parameters
    ----------
    `status`: AssetStatus | None = None
    `asset_class`: AssetClass | None = None
    `exchange`: AssetExchange | None = None

    Returns
    -------
    list[str]:
        the names matching the query parameters.
    """
    return [
        a.name
        for a in _cache_broker_api_call(
            broker_client=broker_client,
            status=status,
            asset_class=asset_class,
            exchange=exchange,
        )
        if a.name
    ]


@router.get("/names/{name}")
def get_asset_by_name(
    name: str,
    broker_client: BrokerClient = Depends(get_broker_client),
) -> Asset:
    """
    Get the asset with a specific name.

    Parameters
    ----------
    `name`: str
        the asset name.

    Returns
    -------
    Asset:
        the asset matching the name.
    """
    for a in _cache_broker_api_call(broker_client=broker_client):
        if a.name == name:
            return a
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No asset with name {name} was found.",
    )
