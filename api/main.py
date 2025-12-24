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

    return result
