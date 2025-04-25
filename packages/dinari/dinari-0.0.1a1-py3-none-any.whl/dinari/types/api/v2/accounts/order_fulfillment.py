# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ....._models import BaseModel

__all__ = ["OrderFulfillment"]


class OrderFulfillment(BaseModel):
    id: str
    """Identifier of the order fulfillment"""

    asset_token_filled: float
    """Amount of asset token filled"""

    asset_token_spent: float
    """Amount of asset token spent"""

    order_id: str
    """Identifier of the order this fulfillment is for"""

    payment_token_filled: float
    """Amount of payment token filled"""

    payment_token_spent: float
    """Amount of payment token spent"""

    transaction_dt: datetime
    """Time when transaction occurred"""

    transaction_hash: str
    """Transaction hash for this fulfillment"""

    payment_token_fee: Optional[float] = None
    """Fee amount of payment token spent"""
