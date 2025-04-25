# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ....._models import BaseModel
from .kyc_document_type import KYCDocumentType

__all__ = ["KYCUploadDocumentResponse"]


class KYCUploadDocumentResponse(BaseModel):
    id: str
    """ID of the document"""

    document_type: KYCDocumentType
    """Type of the document"""

    filename: str
    """Filename of the document"""

    url: str
    """URL to access the document. Expires in 1 hour"""
