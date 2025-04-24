# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["AnalyzeAnalyzeSourceCodeParams", "Options"]


class AnalyzeAnalyzeSourceCodeParams(TypedDict, total=False):
    code: Required[str]
    """Source code to analyze"""

    language: Required[str]
    """Programming language (e.g., python, javascript, rust)"""

    options: Options
    """Optional analysis parameters"""


class Options(TypedDict, total=False):
    deep: bool
    """Enable deep learning-based semantic analysis"""

    performance_hints: Annotated[bool, PropertyInfo(alias="performanceHints")]
    """Provide performance improvement hints"""
