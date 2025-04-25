# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .kyc_document_type import KYCDocumentType

__all__ = ["KYCUploadDocumentParams"]


class KYCUploadDocumentParams(TypedDict, total=False):
    entity_id: Required[str]

    document_type: Required[KYCDocumentType]
    """Type of the document to be uploaded"""
