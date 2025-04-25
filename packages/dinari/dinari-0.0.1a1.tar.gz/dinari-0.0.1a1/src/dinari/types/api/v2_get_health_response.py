# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["V2GetHealthResponse"]


class V2GetHealthResponse(BaseModel):
    status: str
    """Status of server"""
