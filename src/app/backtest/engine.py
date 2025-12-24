from typing import List
from app.backtest.metrics import calculate_drawdowns
from app.backtest.models import BacktestResult, Trade, EquityPoint
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
        peak = equity_values[0] if equity_values else initial_cash
        for eq in equity_values:
            if eq > peak:
                peak = eq
            drawdowns.append((peak - eq) / peak if peak > 0 else 0.0)

        # Create equity curve with dates and drawdowns
        equity_curve = [
            EquityPoint(point_date=date, equity=equity, drawdown=drawdown)
            for date, equity, drawdown in zip(dates, equity_values, drawdowns)
        ]

        returns = calculate_returns(equity_values)

        cagr = calculate_cagr(
            initial_cash,
            portfolio.equity,
            dates[0],
            dates[-1],
        )

        volatility = calculate_volatility(returns)
        sharpe = calculate_sharpe(cagr, volatility)
        sortino = calculate_sortino(cagr, returns)
        result = BacktestResult(
            total_trades=len(trades),
            total_pnl=portfolio.equity - initial_cash,
            win_rate=(
                len([t for t in trades if t.pnl and t.pnl > 0]) / len(trades)
                if trades
                else 0.0
            ),
            trades=trades,
            equity_curve=equity_curve,
            max_drawdown=max(drawdowns) if drawdowns else 0.0,
            cagr=cagr,
            volatility=volatility,
            sharpe=sharpe,
            sortino=sortino,
            profit_factor=calculate_profit_factor(trades),
            time_in_market=calculate_time_in_market(equity_curve, trades),
            avg_trade_duration_days=calculate_avg_trade_duration(trades),
            max_consecutive_losses=calculate_max_consecutive_losses(trades),
        )

        return result
