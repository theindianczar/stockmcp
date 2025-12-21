from datetime import date
from pydantic import BaseModel
from typing import List


class Trade(BaseModel):
    symbol: str
    entry_date: date
    entry_price: float
    exit_date: date | None = None
    exit_price: float | None = None
    pnl: float | None = None


class BacktestResult(BaseModel):
    total_trades: int
    total_pnl: float
    win_rate: float
    trades: List[Trade]
