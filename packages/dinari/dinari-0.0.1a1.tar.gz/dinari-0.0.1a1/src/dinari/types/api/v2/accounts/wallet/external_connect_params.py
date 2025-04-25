# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ExternalConnectParams"]


class ExternalConnectParams(TypedDict, total=False):
    chain_id: Required[int]
    """Blockchain the wallet to link is on"""

    nonce: Required[str]
    """Nonce used to sign the wallet connection message"""

    signature: Required[str]
    """Signature payload from signing the wallet connection message with the wallet"""

    wallet_address: Required[str]
    """Address of the wallet"""
