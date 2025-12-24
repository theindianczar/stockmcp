from typing import Dict, List


FD_RETURN = 0.07  # 7% FD baseline (India)


class DecisionResult(dict):
    category: str
    score: float
    reasons: List[str]


class DecisionEngine:
    def evaluate(self, metrics: Dict[str, float]) -> DecisionResult:
        reasons: List[str] = []

        cagr = metrics["cagr"]
        sharpe = metrics["sharpe"]
        sortino = metrics["sortino"]
        max_dd = metrics["max_drawdown"]
        profit_factor = metrics["profit_factor"]
        max_consec_losses = metrics["max_consecutive_losses"]

        # -------- HARD REJECT RULES --------
        if cagr < FD_RETURN:
            return self._reject("CAGR below FD return")

        if profit_factor < 1.0:
            return self._reject("Profit factor below 1 (losing edge)")

        if sharpe < 0.5:
            return self._reject("Sharpe ratio below acceptable risk threshold")

        if max_dd > 0.35:
            return self._reject("Maximum drawdown exceeds 35%")

        # -------- SCORING --------
        score = 0.0

        score += min(cagr / 0.25, 1.0) * 30
        score += min(sharpe / 2.0, 1.0) * 25
        score += min(sortino / 2.5, 1.0) * 20
        score += (1 - min(max_dd / 0.35, 1.0)) * 15
        score += min(profit_factor / 2.0, 1.0) * 10

        # -------- CLASSIFICATION --------
        if (
            cagr >= 0.12
            and sharpe >= 1.0
            and sortino >= 1.2
            and max_dd <= 0.20
            and max_consec_losses <= 5
        ):
            category = "INVEST"
            reasons.append("Strong risk-adjusted performance across key metrics")
        else:
            category = "CAUTION"
            reasons.append("Returns are positive but risk metrics are mixed")

        # -------- EXPLANATIONS --------
        reasons.extend(
            [
                f"CAGR: {cagr:.2%}",
                f"Sharpe Ratio: {sharpe:.2f}",
                f"Sortino Ratio: {sortino:.2f}",
                f"Max Drawdown: {max_dd:.2%}",
                f"Profit Factor: {profit_factor:.2f}",
                f"Max Consecutive Losses: {max_consec_losses}",
            ]
        )

        return {
            "category": category,
            "score": round(score, 1),
            "reasons": reasons,
        }

    def _reject(self, reason: str) -> DecisionResult:
        return {
            "category": "REJECT",
            "score": 0.0,
            "reasons": [reason],
        }
