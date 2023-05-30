"""Router for logos."""
import logging
from functools import lru_cache

import requests
from alpaca.data import StockHistoricalDataClient
from fastapi import APIRouter, Depends, Response, status

from alpaca_partner_backend.api.common import get_data_client
from alpaca_partner_backend.enums import Routers

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.LOGOS.value,
    tags=[Routers.LOGOS.name],
)


@lru_cache
def _cached_get_logo(
    data_client: StockHistoricalDataClient,
    symbol: str,
) -> bytes:
    """Cache the logos call to the data client."""
    response = requests.get(
        url=f"{data_client._base_url}/v1beta1/logos/{symbol}",
        headers=data_client._get_auth_headers(),
    )
    assert response.status_code == status.HTTP_200_OK, response.status_code
    return response.content


@router.get(
    "/{symbol}",
    responses={
        200: {"content": {"image/png": {}}},
    },
    response_class=Response,
)
def get_logo(
    symbol: str,
    data_client: StockHistoricalDataClient = Depends(get_data_client),
) -> Response:
    """Get the logo for a certain symbol."""
    logo_bytes = _cached_get_logo(
        data_client=data_client,
        symbol=symbol,
    )
    return Response(content=logo_bytes, media_type="image/png")
