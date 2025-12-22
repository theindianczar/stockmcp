from datetime import date
from typing import Dict
from pydantic import BaseModel, Field


class Position(BaseModel):
    """
    A model representing a position in a specific asset within a portfolio.
    """

    symbol: str = Field(description="The stock or asset symbol.")
    quantity: float = Field(description="The quantity of the asset held.")
    avg_price: float = Field(
        description="The average price at which the asset was acquired."
    )
    entry_date: date = Field(description="The date when the position was entered.")


class Portfolio(BaseModel):
    """
    A model representing a portfolio containing multiple positions.
    """

    cash: float = Field(
        description="The amount of liquid cash available in the portfolio."
    )
    positions: Dict[str, Position] = Field(
        description="A dictionary mapping asset symbols to their respective Position objects."
    )
    equity: float = Field(
        description="The total equity of the portfolio, including cash and the market value of all positions."
    )
