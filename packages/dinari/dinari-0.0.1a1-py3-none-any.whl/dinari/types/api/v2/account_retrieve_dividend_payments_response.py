# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import date
from typing_extensions import TypeAlias

from ...._models import BaseModel

__all__ = ["AccountRetrieveDividendPaymentsResponse", "AccountRetrieveDividendPaymentsResponseItem"]


class AccountRetrieveDividendPaymentsResponseItem(BaseModel):
    amount: float
    """Amount of the dividend paid."""

    currency: str
    """Currency in which the dividend was paid. (e.g. USD)"""

    payment_date: date
    """Date the dividend was distributed to the account."""

    stock_id: str
    """ID of the stock for which the dividend was paid."""


AccountRetrieveDividendPaymentsResponse: TypeAlias = List[AccountRetrieveDividendPaymentsResponseItem]
