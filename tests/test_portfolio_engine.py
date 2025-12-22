from datetime import date
from app.portfolio.engine import PortfolioEngine
from app.portfolio.models import Portfolio
from app.signals.enums import SignalType


def test_portfolio_buy_and_sell():
    portfolio = Portfolio(cash=10000, positions={}, equity=10000)
    engine = PortfolioEngine()

    portfolio = engine.apply_signal(
        portfolio=portfolio,
        symbol="AAPL",
        signal=SignalType.BUY,
        price=100,
        date=date(2024, 1, 1),
    )

    assert "AAPL" in portfolio.positions
    assert portfolio.cash < 10000

    portfolio = engine.apply_signal(
        portfolio=portfolio,
        symbol="AAPL",
        signal=SignalType.SELL,
        price=110,
        date=date(2024, 1, 2),
    )

    assert "AAPL" not in portfolio.positions
    assert portfolio.cash > 10000
