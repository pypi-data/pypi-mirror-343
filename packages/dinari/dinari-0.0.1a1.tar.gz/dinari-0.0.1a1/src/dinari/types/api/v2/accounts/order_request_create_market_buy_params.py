# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["OrderRequestCreateMarketBuyParams"]


class OrderRequestCreateMarketBuyParams(TypedDict, total=False):
    payment_amount: Required[float]
    """Amount of USD to pay or receive for the order.

    Must be a positive number with a precision of up to 2 decimal places.
    """

    stock_id: Required[str]
    """ID of stock, as returned by the `/stocks` endpoint, e.g. 1"""

    include_fees: bool
    """Whether to include fees in the `payment_amount` input field."""
