from datetime import date, timedelta
from app.market.models import OHLCV
from app.signals.enums import SignalType
from app.signals.indicators import simple_moving_average
from app.signals.swing_sma_rsi import SwingSMARsiStrategy


def test_sma():
    values = [10, 20, 30, 40, 50]
    assert simple_moving_average(values, 5) == 30


def test_swing_strategy_buy_signal():
    start = date(2024, 1, 1)

    data = [
        OHLCV(
            symbol="AAPL",
            date=start + timedelta(days=i),
            open=0,
            high=0,
            low=0,
            close=100 + i,
            volume=0,
        )
        for i in range(60)
    ]

    strategy = SwingSMARsiStrategy()
    signal = strategy.generate_signal(data)

    assert signal.signal in {SignalType.BUY, SignalType.HOLD}
