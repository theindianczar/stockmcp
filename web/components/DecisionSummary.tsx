"use client";

type Decision = {
  category: "INVEST" | "CAUTION" | "REJECT";
  score: number;
  reasons: string[];
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
    </div>
  );
}
