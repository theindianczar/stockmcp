from abc import ABC, abstractmethod
from typing import List

from app.market.models import OHLCV
from app.signals.models import TradingSignal


class SignalStrategy(ABC):
    """
    Base interface for all trading strategies.
    """

    @abstractmethod
    def generate_signal(self, data: List[OHLCV]) -> TradingSignal:
        raise NotImplementedError
