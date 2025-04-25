# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from ....._models import BaseModel

__all__ = ["KYCGetURLResponse"]


class KYCGetURLResponse(BaseModel):
    embed_url: str
    """URL of a managed KYC flow interface for the entity.

    This URL is unique per KYC attempt.
    """

    expiration_dt: datetime
    """Timestamp at which the KYC request will be expired"""
