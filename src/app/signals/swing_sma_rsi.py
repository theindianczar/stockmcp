from typing import List

from app.market.models import OHLCV
from app.signals.base import SignalStrategy
from app.signals.enums import SignalType
from app.signals.indicators import (
    simple_moving_average,
    relative_strength_index,
)
from app.signals.models import TradingSignal


class SwingSMARsiStrategy(SignalStrategy):
    """
    Swing trading strategy using SMA trend + RSI filter.
    """

    def __init__(
        self,
        short_window: int = 20,
        long_window: int = 50,
        rsi_window: int = 14,
    ):
        if short_window >= long_window:
            raise ValueError("short_window must be < long_window")

        self.short_window = short_window
        self.long_window = long_window
        self.rsi_window = rsi_window

    def generate_signal(self, data: List[OHLCV]) -> TradingSignal:
        closes = [c.close for c in data]
        latest = data[-1]

        short_sma = simple_moving_average(closes, self.short_window)
        long_sma = simple_moving_average(closes, self.long_window)
        rsi = relative_strength_index(closes, self.rsi_window)

        if short_sma > long_sma and rsi < 70:
            return TradingSignal(
                symbol=latest.symbol,
                signal=SignalType.BUY,
                reason="Uptrend confirmed (SMA crossover) and RSI below 70",
            )

        if short_sma < long_sma and rsi > 30:
            return TradingSignal(
                symbol=latest.symbol,
                signal=SignalType.SELL,
                reason="Downtrend confirmed (SMA crossover) and RSI above 30",
            )

        return TradingSignal(
            symbol=latest.symbol,
            signal=SignalType.HOLD,
            reason="No strong trend or RSI extreme",
        )
