"""Market data provider abstractions.

This module defines the `MarketDataProvider` abstract base class which
standardizes how market data providers should expose daily OHLCV data to
the application. Implementations (e.g. Yahoo, mock providers) should
subclass `MarketDataProvider` and implement the `get_daily_ohlcv` method.

The goal is to keep provider implementations interchangeable so the
rest of the codebase can request market candles via a single, stable
interface.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import List

from app.market.models import OHLCV


class MarketDataProvider(ABC):
    """Abstract interface for fetching market OHLCV data.

    Implementations must provide historical daily OHLCV candles using
    the `get_daily_ohlcv` method. The method returns a list of
    `OHLCV` models where each model represents a single daily candle.

    Subclasses should not modify the returned list in-place; callers
    may cache or transform results as needed.
    """

    @abstractmethod
    def get_daily_ohlcv(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> List[OHLCV]:
        """Fetch daily OHLCV candles for `symbol` between `start` and `end`.

        Args:
            symbol: Ticker symbol to fetch, e.g. "AAPL".
            start: Inclusive start date for the history request.
            end: Exclusive end date for the history request.

        Returns:
            A list of `OHLCV` models ordered by date (ascending).

        Raises:
            NotImplementedError: Implementations must override this method.

        Notes:
            - Providers may return an empty list if no data exists for the
              requested range; callers should handle that case.
            - Providers are responsible for choosing whether to return
              adjusted or raw prices; document the chosen behavior in the
              concrete provider implementation.
        """
        raise NotImplementedError
