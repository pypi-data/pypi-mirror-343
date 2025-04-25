# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["OrderGetEstimatedFeeParams"]


class OrderGetEstimatedFeeParams(TypedDict, total=False):
    chain_id: Required[int]
    """Chain where the order is placed"""

    contract_address: Required[str]
    """Order contract address"""

    order_data: Required[Dict[str, str]]
    """Order data from which to calculate the fees. To be specified in the future"""
