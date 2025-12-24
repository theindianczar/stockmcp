"use client";

import { useState } from "react";
import { HelpCircle } from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { EquityPoint } from "@/lib/api";
import HelpModal from "./HelpModal";

type Props = {
  readonly equityCurve: EquityPoint[];
};

const formatPercentage = (value: number) => {
  return `${(value * 100).toFixed(2)}%`;
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
    drawdown: number;
  };
}

const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: TooltipPayload[] }) => {
  if (active && payload?.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white border border-gray-300 rounded p-3 shadow-lg">
        <p className="font-semibold">{`Date: ${formatDate(data.date)}`}</p>
        <p className="text-red-600">{`Drawdown: ${formatPercentage(data.drawdown)}`}</p>
      </div>
    );
  }
  return null;
};

export default function DrawdownChart({ equityCurve }: Props) {
  const [showHelp, setShowHelp] = useState(false);

  const data = equityCurve.map((point) => ({
    date: point.date,
    drawdown: point.drawdown,
  }));

  return (
    <div className="border rounded p-4">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-xl font-semibold">Drawdown Chart</h2>
        <button
          onClick={() => setShowHelp(true)}
          className="text-gray-500 hover:text-gray-700"
          title="Help"
        >
          <HelpCircle size={20} />
        </button>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            interval="preserveStartEnd"
          />
          <YAxis
            tickFormatter={formatPercentage}
            domain={[0, "auto"]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="drawdown"
            stroke="#dc2626"
            fill="#fecaca"
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>

      <HelpModal
        isOpen={showHelp}
        onClose={() => setShowHelp(false)}
        title="Drawdown Chart - Understanding Risk and Losses"
        content={`The Drawdown Chart shows the percentage decline from your portfolio's peak value.

• Y-axis: Drawdown percentage (0% = no loss from peak)
• X-axis: Trading dates
• Area: Magnitude of losses from previous highs

To maximize returns while managing risk:
• Smaller area under the curve is better (less severe drawdowns)
• Shorter drawdown periods are preferable
• Avoid strategies with deep, prolonged drawdowns
• Look for quick recoveries after dips

The goal is to minimize both the depth and duration of drawdowns while maintaining growth.`}
      />
    </div>
  );
}