"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type Props = {
  equityCurve: number[];
};

export default function EquityCurve({ equityCurve }: Props) {
  const data = equityCurve.map((value, index) => ({
    step: index + 1,
    equity: value,
  }));

  return (
    <div className="border rounded p-4">
      <h2 className="text-xl font-semibold mb-2">Equity Curve</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="step" />
          <YAxis domain={["auto", "auto"]} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="equity"
            stroke="#2563eb"
            dot={false}
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
