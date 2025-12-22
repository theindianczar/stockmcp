def max_drawdown_allowed(
    equity_peak: float,
    current_equity: float,
    max_dd: float = 0.2,
) -> bool:
    """
    Check if the current drawdown exceeds the maximum allowed drawdown.

    Args:
        equity_peak (float): The peak equity value.
        current_equity (float): The current equity value.
        max_dd (float, optional): The maximum allowed drawdown as a decimal. Defaults to 0.2 (20%).

    Returns:
        bool: True if the drawdown exceeds the maximum allowed, False otherwise.
    """
    if equity_peak <= 0:
        raise ValueError("Equity peak must be greater than zero.")

    drawdown = (equity_peak - current_equity) / equity_peak
    return drawdown >= max_dd
