from datetime import date
from fastapi import FastAPI, Query

from app.backtest.engine import BacktestEngine
from app.market.yahoo import YahooMarketDataProvider
from app.signals.swing_sma_rsi import SwingSMARsiStrategy
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="StockMCP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/backtest/run")
def run_backtest(
    symbol: str = Query(..., description="Stock symbol, e.g. AAPL or WIPRO.NS"),
    start: date = Query(...),
    end: date = Query(...),
    initial_cash: float = Query(100_000),
):
    provider = YahooMarketDataProvider()
    data = provider.get_daily_ohlcv(
        symbol=symbol,
        start=start,
        end=end,
    )

    strategy = SwingSMARsiStrategy()
    engine = BacktestEngine()

    result = engine.run(
        data=data,
        strategy=strategy,
        initial_cash=initial_cash,
    )

    return {
        "symbol": symbol,
        "initial_cash": initial_cash,
        "total_pnl": result.total_pnl,
        "max_drawdown": result.max_drawdown,
        "metrics": {
            "cagr": result.cagr,
            "volatility": result.volatility,
            "sharpe": result.sharpe,
            "sortino": result.sortino,
            "profit_factor": result.profit_factor,
            "time_in_market": result.time_in_market,
            "avg_trade_duration_days": result.avg_trade_duration_days,
            "max_consecutive_losses": result.max_consecutive_losses,
            "max_drawdown": result.max_drawdown,
            "total_pnl": result.total_pnl,
        },
        "equity_curve": [
            {
                "date": str(point.point_date),
                "equity": point.equity,
                "drawdown": point.drawdown,
            }
            for point in result.equity_curve
        ],
        "trades": [
            {
                "symbol": t.symbol,
                "quantity": t.quantity,
                "entry_date": str(t.entry_date),
                "entry_price": t.entry_price,
                "exit_date": str(t.exit_date) if t.exit_date else None,
                "exit_price": t.exit_price,
                "pnl": t.pnl,
            }
            for t in result.trades
        ],
    }
