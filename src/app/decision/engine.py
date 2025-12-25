from typing import Dict, List, Any


FD_RETURN = 0.07  # 7% FD baseline (India)


class DecisionResult(dict):
    category: str
    score: float
    reasons: List[str]
    details: Dict[str, float]
    checks: List[Dict[str, Any]]
    contributions: List[Dict[str, Any]]


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
            return self._reject("CAGR below FD return", metrics)

        if profit_factor < 1.0:
            return self._reject("Profit factor below 1 (losing edge)", metrics)

        if sharpe < 0.5:
            return self._reject("Sharpe ratio below acceptable risk threshold", metrics)

        if max_dd > 0.35:
            return self._reject("Maximum drawdown exceeds 35%", metrics)

        # -------- SCORING --------
        score = 0.0

        cagr_contrib = min(cagr / 0.25, 1.0) * 30
        sharpe_contrib = min(sharpe / 2.0, 1.0) * 25
        sortino_contrib = min(sortino / 2.5, 1.0) * 20
        dd_contrib = (1 - min(max_dd / 0.35, 1.0)) * 15
        pf_contrib = min(profit_factor / 2.0, 1.0) * 10

        score += (
            cagr_contrib + sharpe_contrib + sortino_contrib + dd_contrib + pf_contrib
        )

        contributions = [
            {
                "metric": "cagr",
                "value": cagr,
                "weight": 30,
                "contribution": round(cagr_contrib, 2),
            },
            {
                "metric": "sharpe",
                "value": sharpe,
                "weight": 25,
                "contribution": round(sharpe_contrib, 2),
            },
            {
                "metric": "sortino",
                "value": sortino,
                "weight": 20,
                "contribution": round(sortino_contrib, 2),
            },
            {
                "metric": "max_drawdown",
                "value": max_dd,
                "weight": 15,
                "contribution": round(dd_contrib, 2),
            },
            {
                "metric": "profit_factor",
                "value": profit_factor,
                "weight": 10,
                "contribution": round(pf_contrib, 2),
            },
        ]

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

        # build checks for each significant rule/threshold
        checks = [
            {
                "name": "CAGR >= FD return",
                "metric": "cagr",
                "value": cagr,
                "threshold": FD_RETURN,
                "passed": cagr >= FD_RETURN,
            },
            {
                "name": "Profit factor >= 1",
                "metric": "profit_factor",
                "value": profit_factor,
                "threshold": 1.0,
                "passed": profit_factor >= 1.0,
            },
            {
                "name": "Sharpe >= 0.5",
                "metric": "sharpe",
                "value": sharpe,
                "threshold": 0.5,
                "passed": sharpe >= 0.5,
            },
            {
                "name": "Max drawdown <= 35%",
                "metric": "max_drawdown",
                "value": max_dd,
                "threshold": 0.35,
                "passed": max_dd <= 0.35,
            },
        ]

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
            "details": metrics,
            "checks": checks,
            "contributions": contributions,
        }

    def _reject(
        self, reason: str, metrics: Dict[str, float] | None = None
    ) -> DecisionResult:
        # Build minimal checks and contributions from provided metrics so UI can show pass/fail
        m = metrics or {}
        cagr = m.get("cagr", 0.0)
        sharpe = m.get("sharpe", 0.0)
        profit_factor = m.get("profit_factor", 0.0)
        max_dd = m.get("max_drawdown", 0.0)

        checks = [
            {
                "name": "CAGR >= FD return",
                "metric": "cagr",
                "value": cagr,
                "threshold": FD_RETURN,
                "passed": cagr >= FD_RETURN,
            },
            {
                "name": "Profit factor >= 1",
                "metric": "profit_factor",
                "value": profit_factor,
                "threshold": 1.0,
                "passed": profit_factor >= 1.0,
            },
            {
                "name": "Sharpe >= 0.5",
                "metric": "sharpe",
                "value": sharpe,
                "threshold": 0.5,
                "passed": sharpe >= 0.5,
            },
            {
                "name": "Max drawdown <= 35%",
                "metric": "max_drawdown",
                "value": max_dd,
                "threshold": 0.35,
                "passed": max_dd <= 0.35,
            },
        ]

        # contributions can be computed similarly but will reflect low/0 score for reject
        cagr_contrib = min(cagr / 0.25, 1.0) * 30
        sharpe_contrib = min(sharpe / 2.0, 1.0) * 25
        sortino_contrib = min(m.get("sortino", 0.0) / 2.5, 1.0) * 20
        dd_contrib = (1 - min(max_dd / 0.35, 1.0)) * 15
        pf_contrib = min(profit_factor / 2.0, 1.0) * 10

        contributions = [
            {
                "metric": "cagr",
                "value": cagr,
                "weight": 30,
                "contribution": round(cagr_contrib, 2),
            },
            {
                "metric": "sharpe",
                "value": sharpe,
                "weight": 25,
                "contribution": round(sharpe_contrib, 2),
            },
            {
                "metric": "sortino",
                "value": m.get("sortino", 0.0),
                "weight": 20,
                "contribution": round(sortino_contrib, 2),
            },
            {
                "metric": "max_drawdown",
                "value": max_dd,
                "weight": 15,
                "contribution": round(dd_contrib, 2),
            },
            {
                "metric": "profit_factor",
                "value": profit_factor,
                "weight": 10,
                "contribution": round(pf_contrib, 2),
            },
        ]

        return {
            "category": "REJECT",
            "score": 0.0,
            "reasons": [reason],
            "details": m,
            "checks": checks,
            "contributions": contributions,
        }
