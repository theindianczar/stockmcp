from datetime import date
from app.backtest.engine import BacktestEngine
from app.market.yahoo import YahooMarketDataProvider
from app.signals.swing_sma_rsi import SwingSMARsiStrategy


def main():
    """Run a backtest using Yahoo market data and the Swing SMA RSI strategy."""
    print(">>> Script started")
    symbol = "WIPRO.NS"
    start_date = date(2025, 4, 1)
    end_date = date(2025, 12, 20)

    provider = YahooMarketDataProvider()
    data = provider.get_daily_ohlcv(symbol=symbol, start=start_date, end=end_date)

    print(f"Fetched {len(data)} candles for {symbol}")

    strategy = SwingSMARsiStrategy()

    engine = BacktestEngine()
    result = engine.run(data=data, strategy=strategy)

    print("=== Backtest Results ===")
    print(f"Symbol        : {symbol}")
    print(f"Total trades  : {result.total_trades}")
    print(f"Total PnL     : {result.total_pnl:.2f}")
    print(f"Win rate      : {result.win_rate:.2%}")

    print("\n=== Executed Trades ===")
    for t in result.trades:
        print(
            f"{t.symbol} | "
            f"BUY {t.entry_date} @ {t.entry_price:.2f} → "
            f"SELL {t.exit_date} @ {t.exit_price:.2f} | "
            f"PnL: {t.pnl:.2f}"
        )
    print(f"Max drawdown : {result.max_drawdown:.2%}")


if __name__ == "__main__":
    main()
