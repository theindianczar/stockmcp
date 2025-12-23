from datetime import date, timedelta
from app.backtest.engine import BacktestEngine
from app.market.models import OHLCV
from app.signals.swing_sma_rsi import SwingSMARsiStrategy


def test_backtest_runs_and_returns_results():
    """Test that the BacktestEngine runs and returns results."""

    # Create mock OHLCV data
    start = date(2024, 1, 1)
    data = [
        OHLCV(
            symbol="AAPL",
            candle_date=start + timedelta(days=i),
            open_price=100 + i,
            high=105 + i,
            low=95 + i,
            close=102 + i,
            volume=1000 + i * 10,
        )
        for i in range(80)
    ]

    strategy = SwingSMARsiStrategy()
    engine = BacktestEngine()
    result = engine.run(data=data, strategy=strategy, initial_cash=100_000)

    assert isinstance(result.total_pnl, float)
    assert result.total_trades >= 0

    assert result.total_trades >= 0
    assert isinstance(result.total_pnl, float)
