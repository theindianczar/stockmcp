from typing import List
from app.backtest.metrics import calculate_drawdowns
from app.backtest.models import BacktestResult, Trade, EquityPoint
from app.decision.engine import DecisionEngine
from app.market.models import OHLCV
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio
from app.signals.base import SignalStrategy
from app.backtest.metrics import (
    calculate_returns,
    calculate_cagr,
    calculate_volatility,
    calculate_sharpe,
    calculate_sortino,
    calculate_profit_factor,
    calculate_time_in_market,
    calculate_avg_trade_duration,
    calculate_max_consecutive_losses,
)


class BacktestEngine:
    """
    Portfolio-aware backtesting engine.
    """

    def _empty_metrics(self) -> dict:
        return {
            "cagr": 0.0,
            "volatility": 0.0,
            "sharpe": 0.0,
            "sortino": 0.0,
            "profit_factor": 0.0,
            "time_in_market": 0.0,
            "avg_trade_duration_days": 0.0,
            "max_consecutive_losses": 0,
        }

    def run(
        self,
        data: List[OHLCV],
        strategy: SignalStrategy,
        initial_cash: float = 100_000,
        symbol: str | None = None,
    ) -> BacktestResult:
        portfolio = Portfolio(
            cash=initial_cash,
            positions={},
            equity=initial_cash,
        )

        portfolio_engine = PortfolioEngine()
        equity_values = []
        dates = []
        trades = []

        for i, candle in enumerate(data):
            slice_data = data[: i + 1]

            try:
                signal = strategy.generate_signal(slice_data)
            except ValueError:
                equity_values.append(portfolio.equity)
                dates.append(candle.candle_date)
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
                pos = portfolio.positions[candle.symbol]
                trades.append(
                    Trade(
                        symbol=candle.symbol,
                        quantity=pos.quantity,
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
                last_trade.pnl = (
                    last_trade.exit_price - last_trade.entry_price
                ) * last_trade.quantity
            equity_values.append(portfolio.equity)
            dates.append(candle.candle_date)

        # Calculate drawdowns
        drawdowns = calculate_drawdowns(equity_values)

        # Create equity curve with dates and drawdowns
        equity_curve = [
            EquityPoint(date=dt, equity=eq, drawdown=dd)
            for dt, eq, dd in zip(dates, equity_values, drawdowns)
        ]

        returns = calculate_returns(equity_values)

        max_dd = max(drawdowns) if drawdowns else 0.0

        cagr_val = (
            calculate_cagr(initial_cash, portfolio.equity, dates[0], dates[-1])
            if dates
            else 0.0
        )

        metrics = {
            "cagr": cagr_val,
            "volatility": calculate_volatility(returns),
            "sharpe": calculate_sharpe(cagr_val, calculate_volatility(returns)),
            "sortino": calculate_sortino(cagr_val, returns),
            "profit_factor": calculate_profit_factor(trades),
            "time_in_market": calculate_time_in_market(equity_curve, trades),
            "avg_trade_duration_days": calculate_avg_trade_duration(trades),
            "max_consecutive_losses": calculate_max_consecutive_losses(trades),
            "max_drawdown": max_dd,
        }

        decision = DecisionEngine().evaluate(metrics)

        return BacktestResult(
            symbol=symbol,
            initial_cash=initial_cash,
            total_trades=len(trades),
            total_pnl=portfolio.equity - initial_cash,
            win_rate=(
                len([t for t in trades if t.pnl and t.pnl > 0]) / len(trades)
                if trades
                else 0.0
            ),
            trades=trades,
            equity_curve=equity_curve,
            metrics=metrics,
            max_drawdown=max_dd,
            decision=decision,
        )
