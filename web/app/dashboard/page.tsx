"use client";

import { useState } from "react";
import { runBacktest, BacktestResult, Trade } from "@/lib/api";
import EquityCurve from "@/components/EquityCurve";
import DrawdownChart from "@/components/DrawdownChart";
import DecisionSummary from "@/components/DecisionSummary";

const formatINR = (value: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

export default function Dashboard() {
  const [data, setData] = useState<BacktestResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const [symbol, setSymbol] = useState("WIPRO.NS");
  const [startDate, setStartDate] = useState("2024-01-01");
  const [endDate, setEndDate] = useState("2025-12-01");
  const [initialCash, setInitialCash] = useState(100000);

  const handleRunBacktest = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await runBacktest({
        symbol,
        start: startDate,
        end: endDate,
        initialCash,
      });
      setData(result);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  if (data && !data.metrics) {
    return (
      <div className="p-6 text-gray-500">
        Backtest data received but metrics are missing.
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">StockMCP Dashboard</h1>

      {/* Controls */}
      <div className="border rounded p-4 bg-gray-50">
        <h2 className="text-lg font-semibold mb-4">Backtest Parameters</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label htmlFor="symbol" className="block text-sm font-medium mb-1">Symbol</label>
            <input
              id="symbol"
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              placeholder="e.g. AAPL, WIPRO.NS"
            />
          </div>
          <div>
            <label htmlFor="startDate" className="block text-sm font-medium mb-1">Start Date</label>
            <input
              id="startDate"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label htmlFor="endDate" className="block text-sm font-medium mb-1">End Date</label>
            <input
              id="endDate"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label htmlFor="initialCash" className="block text-sm font-medium mb-1">Initial Cash</label>
            <input
              id="initialCash"
              type="number"
              value={initialCash}
              onChange={(e) => setInitialCash(Number(e.target.value))}
              className="w-full px-3 py-2 border rounded"
              min="1000"
              step="1000"
            />
          </div>
        </div>
        <button
          onClick={handleRunBacktest}
          disabled={isLoading}
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? "Running Backtest..." : "Run Backtest"}
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          Error: {error}
        </div>
      )}

      {!data && !isLoading && (
        <div className="p-6 text-center text-gray-500">
          Configure parameters above and click &quot;Run Backtest&quot; to start.
        </div>
      )}

      {isLoading && (
        <div className="p-6 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Running backtest...</p>
        </div>
      )}

      {data?.metrics &&  (
        <>
          {/* Decision Summary */}
          <DecisionSummary decision={data.decision} />
          {/* Metrics */}
          <div className="grid grid-cols-3 gap-4">
            <Metric label="Total PnL" value={formatINR(data.total_pnl)} />
            <Metric
              label="Max Drawdown"
              value={`${(data.max_drawdown * 100).toFixed(2)}%`}
            />
            <Metric label="Trades" value={data.trades.length} />
          </div>


          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <EquityCurve equityCurve={data.equity_curve} />
            <DrawdownChart equityCurve={data.equity_curve} />
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Metric label="Total PnL (₹)" value={formatINR(data.total_pnl)} />

            <Metric label="CAGR" value={(data.metrics.cagr * 100).toFixed(2) + "%"} />
            <Metric label="Sharpe" value={data.metrics.sharpe.toFixed(2)} />
            <Metric label="Sortino" value={data.metrics.sortino.toFixed(2)} />
            <Metric label="Volatility" value={(data.metrics.volatility * 100).toFixed(2) + "%"} />
            <Metric label="Max Drawdown" value={(data.max_drawdown * 100).toFixed(2) + "%"} />
            <Metric label="Profit Factor" value={data.metrics.profit_factor.toFixed(2)} />
            <Metric label="Time in Market" value={(data.metrics.time_in_market * 100).toFixed(1) + "%"} />
            <Metric label="Avg Trade Duration" value={`${data.metrics.avg_trade_duration_days.toFixed(1)} days`} />
            <Metric label="Max Consecutive Losses" value={data.metrics.max_consecutive_losses} />
          
          </div>

          <TradesTable trades={data.trades} />
        </>
      )}
    </div>
  );
}

function Metric({ label, value }: Readonly<{ label: string; value: string | number }>) {
  return (
    <div className="border rounded p-4">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-xl font-semibold">{value}</div>
    </div>
  );
}

function TradesTable({ trades }: Readonly<{ trades: Trade[] }>) {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Trades</h2>
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th>Symbol</th>
            <th>Qty</th>
            <th>Entry</th>
            <th>Exit</th>
            <th>PnL</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((t) => (
            <tr key={`${t.symbol}-${t.entry_date}-${t.entry_price}`} className="border-t">
              <td>{t.symbol}</td>
              <td>{t.quantity}</td>
              <td>
                {t.entry_date} @ {formatINR(t.entry_price)}
              </td>
              <td>
                {t.exit_date && t.exit_price
                  ? `${t.exit_date} @ ${formatINR(t.exit_price)}`
                  : "OPEN"}
              </td>
              <td
                className={
                  t.pnl && t.pnl < 0 ? "text-red-600" : "text-green-600"
                }
              >
                {t.pnl ? formatINR(t.pnl) : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
