# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["OrderRequest"]


class OrderRequest(BaseModel):
    account_id: str
    """ID of account placing the order"""

    confirmation_code: str
    """Confirmation code of order request.

    This is the primary identifier for the `/order_requests` endpoint
    """

    created_dt: datetime
    """Timestamp at which the order request was created."""

    status: Literal["PENDING", "SUBMITTED", "ERROR", "CANCELLED"]
    """Status of order request"""

    order_id: Optional[str] = None
    """ID of order created from the order request.

    This is the primary identifier for the `/orders` endpoint
    """
