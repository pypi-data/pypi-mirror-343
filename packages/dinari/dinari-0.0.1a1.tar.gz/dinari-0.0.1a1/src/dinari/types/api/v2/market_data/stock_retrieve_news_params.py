# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["StockRetrieveNewsParams"]


class StockRetrieveNewsParams(TypedDict, total=False):
    limit: int
    """The number of news articles to return, default is 10 max is 25"""
