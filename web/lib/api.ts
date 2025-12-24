export type Trade = {
  symbol: string;
  quantity: number;
  entry_date: string;
  entry_price: number;
  exit_date?: string | null;
  exit_price?: number | null;
  pnl?: number | null;
};

export type BacktestResult = {
  symbol: string;
  initial_cash: number;
  total_pnl: number;
  max_drawdown: number;
  equity_curve: number[];
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
