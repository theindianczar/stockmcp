from typing import List
from app.market.models import OHLCV
from app.backtest.models import Trade, BacktestResult
from app.signals.base import SignalStrategy
from app.signals.enums import SignalType


class BacktestEngine:
    def run(
        self,
        data: List[OHLCV],
        strategy: SignalStrategy,
    ) -> BacktestResult:
        trades: List[Trade] = []
        open_trade: Trade | None = None

        for i in range(len(data)):
            slice_data = data[: i + 1]
            candle = data[i]
            try:
                signal = strategy.generate_signal(slice_data)
            except ValueError:
                continue

            if signal.signal == SignalType.BUY and open_trade is None:
                open_trade = Trade(
                    symbol=candle.symbol,
                    entry_date=candle.date,
                    entry_price=candle.close,
                )
            elif signal.signal == SignalType.SELL and open_trade is not None:
                open_trade.exit_date = candle.date
                open_trade.exit_price = candle.close
                open_trade.pnl = open_trade.exit_price - open_trade.entry_price
                trades.append(open_trade)
                open_trade = None

        total_pnl = sum(trade.pnl for trade in trades if trade.pnl is not None)
        wins = len([trade for trade in trades if trade.pnl and trade.pnl > 0])

        return BacktestResult(
            total_pnl=total_pnl,
            total_trades=len(trades),
            win_rate=(wins / len(trades)) if trades else 0.0,
            trades=trades,
        )
