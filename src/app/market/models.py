from datetime import date
from pydantic import BaseModel


class OHLCV(BaseModel):
    """
    Canonical market candle.

    This is the ONLY format used internally.
    """

    symbol: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
