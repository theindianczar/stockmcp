"""Yahoo market data provider using yfinance.

This module implements a simple `YahooMarketDataProvider` that fetches
daily OHLCV data via the `yfinance` package and returns a list of
application `OHLCV` models.

Notes:
- The provider maps DataFrame columns `Open`/`High`/`Low`/`Close`/`Volume`
  to the `OHLCV` model fields `open_price`, `high`, `low`, `close`, and
  `volume` respectively.
- The DataFrame index is converted to a date object and stored as
  `candle_date` on the model.
- Prices are not auto-adjusted (`auto_adjust=False`) so callers who
  expect split/dividend-adjusted prices should handle that.
"""

from datetime import date
from typing import List

import yfinance as yf

from app.market.base import MarketDataProvider
from app.market.models import OHLCV
from app.logging import get_logger

logger = get_logger(__name__)


class YahooMarketDataProvider(MarketDataProvider):
    """Market data provider backed by Yahoo Finance (yfinance).

    This provider returns daily OHLCV candles as `OHLCV` Pydantic models.
    It performs minimal validation and logging and intentionally keeps
    behavior simple so callers can handle retries/caching externally.
    """

    def get_daily_ohlcv(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> List[OHLCV]:
        """Fetch daily OHLCV candles for `symbol` between `start` and `end`.

        Args:
            symbol: Ticker symbol, e.g. "AAPL".
            start: Start date (inclusive) for the history request.
            end: End date (exclusive) for the history request.

        Returns:
            A list of `OHLCV` models representing each daily candle.

        Raises:
            ValueError: if `symbol` is empty or `start` > `end`.

        Implementation details:
            - Uses `yfinance.Ticker.history()` with `auto_adjust=False` to
              return raw OHLCV prices.
            - Converts pandas Timestamp index to `date` and maps DataFrame
              columns to model fields.
            - Does not retry on network errors; callers should implement
              retries, caching, or backoff as needed.

        Example:
            provider = YahooMarketDataProvider()
            candles = provider.get_daily_ohlcv("AAPL", date(2024,1,1), date(2024,1,31))
        """

        if not symbol:
            raise ValueError("symbol must be provided")
        if start > end:
            raise ValueError("start must be <= end")

        logger.info(
            "Fetching market data",
            extra={
                "provider": "yahoo",
                "symbol": symbol,
                "start": str(start),
                "end": str(end),
            },
        )

        # Create yfinance Ticker and request historical daily data. We keep
        # `auto_adjust=False` so callers get raw prices; adjust externally if needed.
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start, end=end, auto_adjust=False)

        # Handle empty results gracefully.
        if df is None or df.empty:
            logger.debug("No data returned from yfinance", extra={"symbol": symbol})
            return []

        candles: List[OHLCV] = []

        # Map DataFrame rows to the application's OHLCV model. We cast values
        # explicitly to native python types to make serialization and tests stable.
        for index, row in df.iterrows():
            candles.append(
                OHLCV(
                    symbol=symbol,
                    candle_date=index.date(),
                    open_price=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=int(row["Volume"]),
                )
            )

        logger.info(
            "Fetched market data rows", extra={"symbol": symbol, "rows": len(candles)}
        )
        return candles
