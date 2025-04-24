# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AnalyzeAnalyzeSourceCodeResponse", "Issue"]


class Issue(BaseModel):
    line: Optional[int] = None

    message: Optional[str] = None

    severity: Optional[Literal["info", "warning", "error", "critical"]] = None

    suggestion: Optional[str] = None
    """AI-generated suggestion to resolve the issue"""


class AnalyzeAnalyzeSourceCodeResponse(BaseModel):
    issues: Optional[List[Issue]] = None
