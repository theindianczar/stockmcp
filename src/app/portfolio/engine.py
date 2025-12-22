from app.portfolio.models import Portfolio, Position
from app.portfolio.sizing import fixed_fractional_sizing
from app.signals.enums import SignalType

"""
PortfolioEngine is responsible for managing a portfolio of positions based on trading signals.
It applies buy and sell signals to update the portfolio's positions and cash balance accordingly.
"""


class PortfolioEngine:
    def apply_signal(
        self,
        portfolio: Portfolio,
        symbol: str,
        signal: SignalType,
        price: float,
        date,
    ) -> Portfolio:
        """Applies a trading signal to the portfolio and returns the updated portfolio.

        Args:
            portfolio (Portfolio): The current state of the portfolio.
            symbol (str): The stock or asset symbol for which the signal is applied.
            signal (SignalType): The trading signal indicating whether to buy, sell, or hold.
            price (float): The current price of the asset.
            date (_type_): The date when the signal is applied.

        Returns:
            Portfolio: The updated state of the portfolio after applying the signal.
        """
        if signal == SignalType.BUY and symbol not in portfolio.positions:
            qty = fixed_fractional_sizing(portfolio.cash, price)
            if qty > 0:
                portfolio.positions[symbol] = Position(
                    symbol=symbol, quantity=qty, avg_price=price, entry_date=date
                )
                portfolio.cash -= qty * price
        elif signal == SignalType.SELL and symbol in portfolio.positions:
            pos = portfolio.positions.pop(symbol)
            portfolio.cash += pos.quantity * price

        portfolio.equity = portfolio.cash + sum(
            p.quantity * price for p in portfolio.positions.values()
        )

        return portfolio
