from pydantic import BaseModel, Field
from app.signals.enums import SignalType


class TradingSignal(BaseModel):
    symbol: str = Field(description="The stock symbol the signal applies to.")
    signal: SignalType = Field(
        description="The type of trading signal (e.g., buy, sell)."
    )
    reason: str = Field(description="The reason or explanation for the signal.")
