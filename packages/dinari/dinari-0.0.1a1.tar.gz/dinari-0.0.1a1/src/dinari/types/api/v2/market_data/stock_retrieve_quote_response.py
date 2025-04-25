# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ....._models import BaseModel

__all__ = ["StockRetrieveQuoteResponse"]


class StockRetrieveQuoteResponse(BaseModel):
    price: float
    """The ask price."""

    stock_id: str

    change: Optional[float] = None
    """The change in price from the previous close."""

    change_percent: Optional[float] = None
    """The percentage change in price from the previous close."""

    close: Optional[float] = None
    """The close price for the stock in the given time period."""

    high: Optional[float] = None
    """The highest price for the stock in the given time period"""

    low: Optional[float] = None
    """The lowest price for the stock in the given time period."""

    market_cap: Optional[int] = None
    """
    The most recent close price of the ticker multiplied by weighted outstanding
    shares
    """

    open: Optional[float] = None
    """The open price for the stock in the given time period."""

    previous_close: Optional[float] = None
    """The close price for the stock for the previous trading day."""

    volume: Optional[float] = None
    """The trading volume of the stock in the given time period."""

    weighted_shares_outstanding: Optional[int] = None
    """The number of shares outstanding in the given time period"""
