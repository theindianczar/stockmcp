from typing import List
from app.market.models import OHLCV
from app.backtest.models import Trade, BacktestResult
from app.signals.base import SignalStrategy
from app.signals.enums import SignalType

"""Backtest engine for running trading strategies. """


class BacktestEngine:
    def run(
        self,
        data: List[OHLCV],
        strategy: SignalStrategy,
    ) -> BacktestResult:
        """
        Execute a backtest simulation using historical OHLCV data and a trading strategy.
        Iterates through historical price data, generates trading signals from the strategy,
        and executes buy/sell trades based on signal generation. Calculates performance
        metrics including total P&L, win rate, and individual trade details.
        Args:
            data: List of OHLCV (Open, High, Low, Close, Volume) candles to backtest against.
            strategy: SignalStrategy instance that generates buy/sell signals based on data.
        Returns:
            BacktestResult: Object containing aggregated backtest performance metrics including:
                - total_pnl: Sum of all realized profits/losses
                - total_trades: Total number of completed trades
                - win_rate: Percentage of profitable trades (0.0 to 1.0)
                - trades: List of all Trade objects with entry/exit details
        Note:
            - ValueError exceptions from strategy.generate_signal() are silently skipped
            - Only complete trades (with both entry and exit) are included in results
            - Trades are initiated on BUY signals and closed on SELL signals
            - Win rate is 0.0 if no trades were executed
        """
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
                    entry_date=candle.candle_date,
                    entry_price=candle.close,
                )
            elif signal.signal == SignalType.SELL and open_trade is not None:
                open_trade.exit_date = candle.candle_date
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
