# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from ....._models import BaseModel

__all__ = ["StockRetrieveHistoricalPricesResponse", "StockRetrieveHistoricalPricesResponseItem"]


class StockRetrieveHistoricalPricesResponseItem(BaseModel):
    close: float
    """Close price of the stock in the given time period."""

    high: float
    """Highest price of the stock in the given time period."""

    low: float
    """Lowest price of the stock in the given time period."""

    open: float
    """Open price of the stock in the given time period."""

    timestamp: int
    """The Unix timestamp in seconds for the start of the aggregate window."""


StockRetrieveHistoricalPricesResponse: TypeAlias = List[StockRetrieveHistoricalPricesResponseItem]
