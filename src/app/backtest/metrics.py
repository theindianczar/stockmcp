from typing import List
from datetime import date
import math


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


def calculate_drawdowns(equity_curve: List[float]) -> List[float]:
    """Calculate the drawdown series from an equity curve.

    Args:
        equity_curve (List[float]): A list representing the equity curve over time.
    Returns:
        List[float]: A list of drawdown percentages at each point.
    """
    if not equity_curve:
        return []

    peak = equity_curve[0]
    drawdowns = []

    for equity in equity_curve:
        if equity > peak:
            peak = equity
        drawdown = (peak - equity) / peak if peak > 0 else 0.0
        drawdowns.append(drawdown)

    return drawdowns


def calculate_returns(equity: List[float]) -> List[float]:
    if len(equity) < 2:
        return []

    returns = []
    for i in range(1, len(equity)):
        prev = equity[i - 1]
        curr = equity[i]
        if prev > 0:
            returns.append((curr - prev) / prev)
    return returns


def calculate_cagr(
    initial_equity: float,
    final_equity: float,
    start_date: date,
    end_date: date,
) -> float:
    days = (end_date - start_date).days
    if days <= 0 or initial_equity <= 0:
        return 0.0

    years = days / 365.25
    return (final_equity / initial_equity) ** (1 / years) - 1


def calculate_volatility(returns: List[float]) -> float:
    if len(returns) < 2:
        return 0.0

    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    daily_vol = math.sqrt(variance)
    return daily_vol * math.sqrt(252)


def calculate_sharpe(cagr: float, volatility: float) -> float:
    if volatility == 0:
        return 0.0
    return cagr / volatility


def calculate_sortino(cagr: float, returns: List[float]) -> float:
    downside = [r for r in returns if r < 0]
    if not downside:
        return 0.0

    mean_down = sum(downside) / len(downside)
    downside_var = sum((r - mean_down) ** 2 for r in downside) / len(downside)
    downside_dev = math.sqrt(downside_var) * math.sqrt(252)

    if downside_dev == 0:
        return 0.0
    return cagr / downside_dev


def calculate_profit_factor(trades) -> float:
    gross_profit = sum(t.pnl for t in trades if t.pnl and t.pnl > 0)
    gross_loss = abs(sum(t.pnl for t in trades if t.pnl and t.pnl < 0))
    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0
    return gross_profit / gross_loss


def calculate_time_in_market(equity_curve, trades) -> float:
    if not equity_curve or not trades:
        return 0.0

    total_days = len(equity_curve)
    days_in_position = 0

    for trade in trades:
        if trade.exit_date:
            days_in_position += (trade.exit_date - trade.entry_date).days

    return days_in_position / total_days


def calculate_avg_trade_duration(trades) -> float:
    durations = [(t.exit_date - t.entry_date).days for t in trades if t.exit_date]
    if not durations:
        return 0.0
    return sum(durations) / len(durations)


def calculate_max_consecutive_losses(trades) -> int:
    max_losses = 0
    current_losses = 0

    for trade in trades:
        if trade.pnl and trade.pnl < 0:
            current_losses += 1
            max_losses = max(max_losses, current_losses)
        else:
            current_losses = 0

    return max_losses
