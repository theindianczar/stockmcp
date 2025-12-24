"use client";

import { useEffect, useState } from "react";
import { runBacktest, BacktestResult } from "@/lib/api";
import EquityCurve from "@/components/EquityCurve";

export default function Dashboard() {
  const [data, setData] = useState<BacktestResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    runBacktest({
      symbol: "WIPRO.NS",
      start: "2024-01-01",
      end: "2025-12-01",
    })
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return <div className="p-6 text-red-600">Error: {error}</div>;
  }

  if (!data) {
    return <div className="p-6">Loading backtest...</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">StockMCP Dashboard</h1>

      <div className="grid grid-cols-3 gap-4">
        <Metric label="Total PnL" value={data.total_pnl.toFixed(2)} />
        <Metric
          label="Max Drawdown"
          value={(data.max_drawdown * 100).toFixed(2) + "%"}
        />
        <Metric label="Trades" value={data.trades.length} />
      </div>

      <EquityCurve equityCurve={data.equity_curve} />
      <TradesTable trades={data.trades} />
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="border rounded p-4">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-xl font-semibold">{value}</div>
    </div>
  );
}

function TradesTable({ trades }: { trades: any[] }) {
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
          {trades.map((t, i) => (
            <tr key={i} className="border-t">
              <td>{t.symbol}</td>
              <td>{t.quantity}</td>
              <td>
                {t.entry_date} @ {t.entry_price}
              </td>
              <td>
                {t.exit_date
                  ? `${t.exit_date} @ ${t.exit_price}`
                  : "OPEN"}
              </td>
              <td
                className={
                  t.pnl && t.pnl < 0 ? "text-red-600" : "text-green-600"
                }
              >
                {t.pnl?.toFixed(2) ?? "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
