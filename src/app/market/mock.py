from datetime import date
from typing import List

from app.market.base import MarketDataProvider
from app.market.models import OHLCV


class MockMarketDataProvider(MarketDataProvider):
    """
    Deterministic provider for tests and backtests.
    """

    def get_daily_ohlcv(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> List[OHLCV]:
        return [
            OHLCV(
                symbol=symbol,
                date=start,
                open=100.0,
                high=110.0,
                low=95.0,
                close=105.0,
                volume=1_000_000,
            )
        ]
