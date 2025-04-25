# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .kyc_data import KYCData
from ....._models import BaseModel

__all__ = ["KYCInfo"]


class KYCInfo(BaseModel):
    id: str
    """Unique identifier for the KYC check"""

    status: Literal["PASS", "FAIL", "PENDING", "INCOMPLETE"]
    """KYC status"""

    checked_dt: Optional[datetime] = None
    """Timestamp when the KYC was last checked"""

    data: Optional[KYCData] = None
    """Object consisting of KYC data for an entity"""

    provider_name: Optional[str] = None
    """Name of the KYC provider that provided the KYC check"""
