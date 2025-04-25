# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["OrderGetEstimatedFeeResponse", "FeeQuote", "Fee"]


class FeeQuote(BaseModel):
    deadline: int

    fee: str

    order_id: str = FieldInfo(alias="orderId")

    requester: str

    timestamp: int


class Fee(BaseModel):
    fee_in_eth: float
    """
    The quantity of the fee paid via payment token in ETH
    <a href='https://ethereum.org/en/developers/docs/intro-to-ether/#what-is-ether' target='_blank'>(what
    is ETH?)</a>
    """

    fee_in_wei: str
    """
    The quantity of the fee paid via payment token in wei
    <a href='https://ethereum.org/en/developers/docs/intro-to-ether/#denominations' target='_blank'>(what
    is wei?)</a>
    """

    type: Literal["SPONSORED_NETWORK", "NETWORK", "TRADING", "ORDER", "PARTNER_ORDER", "PARTNER_TRADING"]
    """Type of fee"""


class OrderGetEstimatedFeeResponse(BaseModel):
    chain_id: int
    """Chain where the order is placed"""

    fee_quote: FeeQuote
    """FeeQuote structure to pass into contracts"""

    fee_quote_signature: str
    """Signed FeeQuote structure to pass into contracts"""

    fees: List[Fee]
    """Breakdown of fees"""

    payment_token: str
    """Address of payment token used for fees"""
