"""Router for market data."""
import logging
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Any

import pandas as pd
from alpaca.data import Adjustment, BarSet, StockBarsRequest, StockHistoricalDataClient, TimeFrame
from fastapi import APIRouter, Depends

from alpaca_partner_backend.api import parsers
from alpaca_partner_backend.api.common import get_data_client
from alpaca_partner_backend.enums import BarsField, Routers

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

router = APIRouter(
    prefix=Routers.PRICES.value,
    tags=[Routers.PRICES.name],
)


@lru_cache
def _cached_get_bars(
    data_client: StockHistoricalDataClient,
    symbol: str,
    start: datetime | None = None,
    end: datetime | None = None,
) -> pd.DataFrame:
    """Cache the bars call to the data client."""
    _now = datetime.now(tz=timezone.utc)
    bars = data_client.get_stock_bars(
        StockBarsRequest(
            symbol_or_symbols=symbol,
            start=start or _now - timedelta(days=365 * 2, minutes=15),
            end=end or _now - timedelta(minutes=15),
            timeframe=TimeFrame.Day,
            adjustment=Adjustment.ALL,
        )
    )
    assert isinstance(bars, BarSet)
    _df = bars.df
    assert isinstance(_df, pd.DataFrame)
    _df.reset_index(inplace=True)
    _df.drop("symbol", inplace=True, axis=1)
    _df["timestamp"] = pd.to_datetime(_df["timestamp"], unit="s").dt.strftime("%Y-%m-%d")
    return _df


@router.get("/bars")
def get_bars(
    symbol: str,
    start: datetime | None = None,
    end: datetime | None = None,
    bars_field: BarsField | None = None,
    data_client: StockHistoricalDataClient = Depends(get_data_client),
) -> list[list[Any]]:
    """Get the bars for a certain symbol and timeframe."""
    bars = _cached_get_bars(
        data_client=data_client,
        symbol=symbol,
        start=start,
        end=end,
    )
    return parsers.parse_df_to_list(
        bars if not bars_field else bars.loc[:, ["timestamp", bars_field]]
    )
