# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["MarketDataGetMarketHoursResponse"]


class MarketDataGetMarketHoursResponse(BaseModel):
    is_market_open: bool
    """Whether or not the market is open"""

    next_session_close_dt: datetime
    """Timestamp in ISO 8601 format at which the next session closes"""

    next_session_open_dt: datetime
    """Timestamp in ISO 8601 format at which the next session opens"""

    current_session_close_dt: Optional[datetime] = None
    """
    Timestamp in ISO 8601 format at which the current session closes or null if the
    market is currently closed
    """

    current_session_open_dt: Optional[datetime] = None
    """
    Timestamp in ISO 8601 format at which the current session opened or null if the
    market is currently closed
    """
