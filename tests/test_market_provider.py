from datetime import date
import pytest

from app.market.mock import MockMarketDataProvider


def test_mock_market_data_provider():
    provider = MockMarketDataProvider()

    data = provider.get_daily_ohlcv(
        symbol="AAPL",
        start=date(2024, 1, 1),
        end=date(2024, 1, 2),
    )

    assert len(data) == 1
    candle = data[0]

    assert candle.symbol == "AAPL"
    assert candle.open_price == pytest.approx(100.0)
    assert candle.close == pytest.approx(105.0)
