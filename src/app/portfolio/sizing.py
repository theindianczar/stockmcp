def fixed_fractional_sizing(
    cash: float,
    price: float,
    risk_fraction: float = 0.1,
) -> int:
    """
    Calculate the position size using fixed fractional sizing method.

    Args:
        cash (float): The total cash available in the portfolio.
        price (float): The current price of the asset.
        risk_fraction (float): The fraction of cash to risk on the trade (default is 0.1 for 10%).

    Returns:
        int: The number of shares to buy/sell.
    """
    allocation = cash * risk_fraction
    quantity = int(allocation // price)
    return max(quantity, 0)
