"use client";

type Decision = {
  category: "INVEST" | "CAUTION" | "REJECT";
  score: number;
  reasons: string[];
  details?: {
    cagr: number;
    volatility: number;
    sharpe: number;
    sortino: number;
    profit_factor: number;
    time_in_market: number;
    avg_trade_duration_days: number;
    max_consecutive_losses: number;
    max_drawdown?: number;
  };
  checks?: {
    name: string;
    metric: string;
    value: number;
    threshold: number;
    passed: boolean;
  }[];
  contributions?: {
    metric: string;
    value: number;
    weight: number;
    contribution: number;
  }[];
};

const badgeStyles: Record<string, string> = {
  INVEST: "bg-green-100 text-green-800 border-green-400",
  CAUTION: "bg-yellow-100 text-yellow-800 border-yellow-400",
  REJECT: "bg-red-100 text-red-800 border-red-400",
};

export default function DecisionSummary({ decision }: { decision: Decision }) {
  if (!decision) return null;

  return (
    <div className="border rounded-lg p-4 mb-6 bg-white">
      <div className="flex items-center gap-4 mb-3">
        <span
          className={`px-3 py-1 rounded-full text-sm font-semibold border ${
            badgeStyles[decision.category]
          }`}
        >
          {decision.category}
        </span>

        <span className="text-lg font-semibold">
          Score: {decision.score} / 100
        </span>
      </div>

      <div>
        <h3 className="font-medium mb-1">Why this recommendation?</h3>
        <ul className="list-disc pl-5 text-sm text-gray-700 space-y-1">
          {decision.reasons.map((reason, idx) => (
            <li key={idx}>{reason}</li>
          ))}
        </ul>
      </div>

      {/* Show checks (pass/fail per metric) */}
      {decision.checks && (
        <div className="mt-3">
          <h4 className="font-medium mb-1">Checks</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            {decision.checks.map((c, i) => (
              <li key={i} className="flex items-center gap-2">
                <span
                  className={`inline-block w-3 h-3 rounded-full ${
                    c.passed ? "bg-green-500" : "bg-red-500"
                  }`}>
                </span>
                <span className="font-medium">{c.name}</span>
                <span className="ml-auto text-xs text-gray-500">{`${(
                  c.value * (c.metric === "max_drawdown" ? 100 : 1)
                ).toFixed(c.metric === "max_drawdown" ? 2 : 2)}${
                  c.metric === "max_drawdown" ? "%" : ""
                }`}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Show contribution breakdown */}
      {decision.contributions && (
        <div className="mt-3">
          <h4 className="font-medium mb-1">Score breakdown</h4>
          <ul className="text-sm text-gray-700 space-y-1">
            {decision.contributions.map((d, i) => (
              <li key={i} className="flex justify-between">
                <span>{d.metric}</span>
                <span className="font-medium">{d.contribution}</span>
              </li>
            ))}
            <li className="flex justify-between border-t pt-1 font-semibold">
              <span>Total</span>
              <span>{decision.score}</span>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}
