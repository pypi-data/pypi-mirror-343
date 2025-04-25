# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ....._models import BaseModel

__all__ = ["StockRetrieveDividendsResponse", "StockRetrieveDividendsResponseItem"]


class StockRetrieveDividendsResponseItem(BaseModel):
    cash_amount: Optional[float] = None
    """Cash amount of the dividend per share owned."""

    currency: Optional[str] = None
    """Currency in which the dividend is paid."""

    declaration_date: Optional[str] = None
    """Date on which the dividend was announced."""

    dividend_type: Optional[str] = None
    """Type of dividend.

    Dividends that have been paid and/or are expected to be paid on consistent
    schedules are denoted as CD. Special Cash dividends that have been paid that are
    infrequent or unusual, and/or can not be expected to occur in the future are
    denoted as SC. Long-Term and Short-Term capital gain distributions are denoted
    as LT and ST, respectively.
    """

    ex_dividend_date: Optional[str] = None
    """
    Date on or after which a stock is traded without the right to receive the next
    dividend payment. (If you purchase a stock on or after the ex-dividend date, you
    will not receive the upcoming dividend.)
    """

    frequency: Optional[int] = None
    """Frequency of the dividend. The following values are possible:

                        1 - Annual

                        2 - Semi-Annual

                        4 - Quarterly

                        12 - Monthly

                        52 - Weekly

                        365 - Daily
    """

    pay_date: Optional[str] = None
    """Date that the dividend is paid out."""

    record_date: Optional[str] = None
    """Date that the stock must be held to receive the dividend; set by the company."""

    ticker: Optional[str] = None
    """Ticker symbol of the stock."""


StockRetrieveDividendsResponse: TypeAlias = List[StockRetrieveDividendsResponseItem]
