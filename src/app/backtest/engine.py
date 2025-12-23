from typing import List
from app.backtest.models import BacktestResult, Trade
from app.market.models import OHLCV
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio
from app.signals.base import SignalStrategy


class BacktestEngine:
    """
    Portfolio-aware backtesting engine.
    """

    def run(
        self,
        data: List[OHLCV],
        strategy: SignalStrategy,
        initial_cash: float = 100_000,
    ) -> BacktestResult:
        portfolio = Portfolio(
            cash=initial_cash,
            positions={},
            equity=initial_cash,
        )

        portfolio_engine = PortfolioEngine()
        equity_curve = []
        trades = []

        for i in range(len(data)):
            slice_data = data[: i + 1]
            candle = data[i]

            try:
                signal = strategy.generate_signal(slice_data)
            except ValueError:
                equity_curve.append(portfolio.equity)
                continue

            portfolio_before = portfolio.model_copy(deep=True)

            portfolio = portfolio_engine.apply_signal(
                portfolio=portfolio,
                symbol=candle.symbol,
                signal=signal.signal,
                price=candle.close,
                date=candle.candle_date,
            )

            # Detect executed trades
            if (
                signal.signal.name == "BUY"
                and candle.symbol not in portfolio_before.positions
                and candle.symbol in portfolio.positions
            ):
                trades.append(
                    Trade(
                        symbol=candle.symbol,
                        entry_date=candle.candle_date,
                        entry_price=candle.close,
                    )
                )

            elif (
                signal.signal.name == "SELL"
                and candle.symbol in portfolio_before.positions
                and candle.symbol not in portfolio.positions
            ):
                last_trade = trades[-1]
                last_trade.exit_date = candle.candle_date
                last_trade.exit_price = candle.close
                last_trade.pnl = last_trade.exit_price - last_trade.entry_price

            equity_curve.append(portfolio.equity)

        total_pnl = portfolio.equity - initial_cash
        wins = len([t for t in trades if t.pnl and t.pnl > 0])

        return BacktestResult(
            total_trades=len(trades),
            total_pnl=total_pnl,
            win_rate=(wins / len(trades)) if trades else 0.0,
            trades=trades,
        )
