# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import date
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["StockSplit"]


class StockSplit(BaseModel):
    id: str
    """Unique identifier for the stock split"""

    ex_date: date
    """Ex-date of the split (Eastern Time Zone).

    First day the stock trades at post-split prices. Typically is last in the
    process, and the main important date for investors.
    """

    payable_date: date
    """Payable date (Eastern Time Zone) of the split.

    Date when company will send out the new shares. Mainly for record keeping by
    brokerages, who forward the shares to eventual owners. Typically is second in
    the process.
    """

    record_date: date
    """
    Record date (Eastern Time Zone) of the split, for company to determine where to
    send their new shares. Mainly for record keeping by brokerages, who forward the
    shares to eventual owners. Typically is first in the process.
    """

    split_from: float
    """The number of shares before the split. In a 10-for-1 split, this would be 1."""

    split_to: float
    """The number of shares after the split. In a 10-for-1 split, this would be 10."""

    status: Literal["PENDING", "IN_PROGRESS", "COMPLETE"]
    """The status of Dinari's processing of the split.

    Stocks for which a split is `IN_PROGRESS` will not be available for trading.
    """

    stock_id: str
    """Reference to the id of the stock for this split"""
