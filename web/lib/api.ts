export type Trade = {
  symbol: string;
  quantity: number;
  entry_date: string;
  entry_price: number;
  exit_date?: string | null;
  exit_price?: number | null;
  pnl?: number | null;
};

export type EquityPoint = {
  date: string;
  equity: number;
  drawdown: number;
};

export type Metrics = {
  cagr: number;
  volatility: number;
  sharpe: number;
  sortino: number;
  profit_factor: number;
  time_in_market: number;
  avg_trade_duration_days: number;
  max_consecutive_losses: number;
  max_drawdown: number;
  total_pnl: number;
};

export type BacktestResult = {
  symbol: string;
  initial_cash: number;
  metrics: Metrics;
  equity_curve:{
    date: string;
    equity: number;
    drawdown: number;
  }[]
  total_pnl: number;
  max_drawdown: number;

  trades: Trade[];
};

const API_BASE = "http://127.0.0.1:8000";

export async function runBacktest(params: {
  symbol: string;
  start: string;
  end: string;
  initialCash?: number;
}): Promise<BacktestResult> {
  const query = new URLSearchParams({
    symbol: params.symbol,
    start: params.start,
    end: params.end,
    initial_cash: String(params.initialCash ?? 100000),
  });

  const res = await fetch(`${API_BASE}/backtest/run?${query}`);

  if (!res.ok) {
    throw new Error("Failed to fetch backtest");
  }

  return res.json();
}
