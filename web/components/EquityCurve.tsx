"use client";

import { useState } from "react";
import { HelpCircle } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { EquityPoint } from "@/lib/api";
import HelpModal from "./HelpModal";

type Props = {
  equityCurve: EquityPoint[];
};

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

interface TooltipPayload {
  payload: {
    date: string;
    equity: number;
  };
}

const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: TooltipPayload[] }) => {
  if (active && payload?.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white border border-gray-300 rounded p-3 shadow-lg">
        <p className="font-semibold">{`Date: ${formatDate(data.date)}`}</p>
        <p className="text-blue-600">{`Equity: ${formatCurrency(data.equity)}`}</p>
      </div>
    );
  }
  return null;
};

export default function EquityCurve({ equityCurve }: Readonly<Props>) {
  const [showHelp, setShowHelp] = useState(false);

  const data = equityCurve.map((point) => ({
    date: point.date,
    equity: point.equity,
  }));

  return (
    <div className="border rounded p-4">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-xl font-semibold">Equity Curve</h2>
        <button
          onClick={() => setShowHelp(true)}
          className="text-gray-500 hover:text-gray-700"
          title="Help"
        >
          <HelpCircle size={20} />
        </button>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            interval="preserveStartEnd"
          />
          <YAxis
            tickFormatter={formatCurrency}
            domain={["auto", "auto"]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="equity"
            stroke="#2563eb"
            dot={false}
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>

      <HelpModal
        isOpen={showHelp}
        onClose={() => setShowHelp(false)}
        title="Equity Curve - Understanding Your Portfolio Growth"
        content={`The Equity Curve shows how your portfolio value changes over time.

• Y-axis: Portfolio value in INR
• X-axis: Trading dates
• Line: Your equity progression

To maximize returns:
• Look for upward trending lines (growth)
• Minimize flat or downward periods
• Steeper upward slopes indicate better performance
• Consistent growth is better than volatile ups/downs

The goal is to see your portfolio value increasing steadily over time, indicating successful trading strategies.`}
      />
    </div>
  );
}
