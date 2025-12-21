from abc import ABC, abstractmethod
from datetime import date
from typing import List

from app.market.models import OHLCV


class MarketDataProvider(ABC):
    """
    Contract for all market data providers.
    """

    @abstractmethod
    def get_daily_ohlcv(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> List[OHLCV]:
        """
        Fetch daily OHLCV candles for a symbol.
        """
        raise NotImplementedError
