from datetime import date
from typing import List

import yfinance as yf

from app.market.base import MarketDataProvider
from app.market.models import OHLCV
from app.logging import get_logger

logger = get_logger(__name__)


class YahooMarketDataProvider(MarketDataProvider):
    """
    Yahoo Finance market data provider.
    """

    def get_daily_ohlcv(
        self,
        symbol: str,
        start: date,
        end: date,
    ) -> List[OHLCV]:
        logger.info(
            "Fetching market data",
            extra={"provider": "yahoo", "symbol": symbol},
        )

        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start, end=end, auto_adjust=False)

        candles: List[OHLCV] = []

        for index, row in df.iterrows():
            candles.append(
                OHLCV(
                    symbol=symbol,
                    date=index.date(),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=int(row["Volume"]),
                )
            )

        return candles
