from datetime import date
from pydantic import BaseModel, Field
from typing import List


class EquityPoint(BaseModel):
    """A point in the equity curve with date and value."""

    point_date: date = Field(description="The date for this equity point.")
    equity: float = Field(description="The equity value at this date.")
    drawdown: float = Field(description="The drawdown percentage at this date.")


class Trade(BaseModel):
    """A model representing a single trade executed during a backtest."""

    symbol: str = Field(description="The stock symbol for the trade.")
    quantity: int = Field(description="The quantity of shares traded.")
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
    equity_curve: List[EquityPoint] = Field(
        description="A list representing the equity curve over time with dates and drawdowns."
    )
    max_drawdown: float = Field(
        description="The maximum drawdown experienced during the backtest."
    )

    cagr: float = Field(description="The compound annual growth rate.")
    volatility: float = Field(description="The annualized volatility of returns.")
    sharpe: float = Field(description="The Sharpe ratio.")
    sortino: float = Field(description="The Sortino ratio.")
    profit_factor: float = Field(description="The profit factor.")
    time_in_market: float = Field(
        description="The percentage of time the strategy was in the market."
    )
    avg_trade_duration_days: float = Field(
        description="The average duration of trades in days."
    )
    max_consecutive_losses: int = Field(
        description="The maximum number of consecutive losing trades."
    )
