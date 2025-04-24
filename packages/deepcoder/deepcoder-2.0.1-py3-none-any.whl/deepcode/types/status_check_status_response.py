# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["StatusCheckStatusResponse"]


class StatusCheckStatusResponse(BaseModel):
    status: Optional[str] = None

    uptime: Optional[str] = None

    version: Optional[str] = None
