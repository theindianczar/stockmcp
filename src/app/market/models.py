from datetime import date
from pydantic import BaseModel, Field


class OHLCV(BaseModel):
    symbol: str = Field(description="The stock symbol for the OHLCV data.")
    candle_date: date = Field(description="The date of the candle.")
    open_price: float = Field(description="The opening price of the period.")
    high: float = Field(description="The highest price during the period.")
    low: float = Field(description="The lowest price during the period.")
    close: float = Field(description="The closing price of the period.")
    volume: int = Field(description="The trading volume during the period.")
