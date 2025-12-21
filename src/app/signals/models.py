from pydantic import BaseModel
from app.signals.enums import SignalType


class TradingSignal(BaseModel):
    symbol: str
    signal: SignalType
    reason: str
