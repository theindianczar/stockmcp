from typing import List


def max_drawdown(equity_curve: List[float]) -> float:
    """Calculate the maximum drawdown from an equity curve.

    Args:
        equity_curve (List[float]): A list representing the equity curve over time.
          Each element corresponds to the equity value at a specific time point.
    Returns:
        float: The maximum drawdown as a decimal (e.g., 0.2 for 20%).
        If there is no drawdown, returns 0.0.
    """

    peak = equity_curve[0]
    max_drawdown = 0.0

    for equity in equity_curve:
        if equity > peak:
            peak = equity
        drawdown = (peak - equity) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    return max_drawdown
