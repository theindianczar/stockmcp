from datetime import date
from pydantic import BaseModel, Field
from typing import List


class Trade(BaseModel):
    """A model representing a single trade executed during a backtest."""

    symbol: str = Field(description="The stock symbol for the trade.")
    entry_date: date = Field(description="The date when the trade was entered.")
    entry_price: float = Field(description="The price at which the trade was entered.")
    exit_date: date | None = Field(
        default=None, description="The date when the trade was exited, if applicable."
    )
    exit_price: float | None = Field(
        default=None,
        description="The price at which the trade was exited, if applicable.",
    )
    pnl: float | None = Field(
        default=None, description="The profit or loss from the trade, if calculated."
    )


class BacktestResult(BaseModel):
    """A model representing the result of a backtest."""

    total_trades: int = Field(
        description="The total number of trades executed in the backtest."
    )
    total_pnl: float = Field(description="The total profit or loss from all trades.")
    win_rate: float = Field(description="The percentage of winning trades.")
    trades: List[Trade] = Field(
        description="A list of all trades executed during the backtest."
    )
