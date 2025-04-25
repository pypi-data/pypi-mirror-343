# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from ....._models import BaseModel

__all__ = ["Account"]


class Account(BaseModel):
    id: str
    """Unique identifier for the account"""

    created_dt: datetime
    """Timestamp when the account was created"""

    entity_id: str
    """Identifier for the Entity that owns the account"""

    is_active: bool
    """Indicates whether the account is active"""
