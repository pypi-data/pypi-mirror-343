# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import analyze_analyze_source_code_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.analyze_analyze_source_code_response import AnalyzeAnalyzeSourceCodeResponse

__all__ = ["AnalyzeResource", "AsyncAnalyzeResource"]


class AnalyzeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AnalyzeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/deepcode-ai/deepcode-python#accessing-raw-response-data-eg-headers
        """
        return AnalyzeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnalyzeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/deepcode-ai/deepcode-python#with_streaming_response
        """
        return AnalyzeResourceWithStreamingResponse(self)

    def analyze_source_code(
        self,
        *,
        code: str,
        language: str,
        options: analyze_analyze_source_code_params.Options | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnalyzeAnalyzeSourceCodeResponse:
        """
        Sends source code for static analysis and optimization insights.

        Args:
          code: Source code to analyze

          language: Programming language (e.g., python, javascript, rust)

          options: Optional analysis parameters

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/analyze",
            body=maybe_transform(
                {
                    "code": code,
                    "language": language,
                    "options": options,
                },
                analyze_analyze_source_code_params.AnalyzeAnalyzeSourceCodeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AnalyzeAnalyzeSourceCodeResponse,
        )


class AsyncAnalyzeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAnalyzeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/deepcode-ai/deepcode-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAnalyzeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnalyzeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/deepcode-ai/deepcode-python#with_streaming_response
        """
        return AsyncAnalyzeResourceWithStreamingResponse(self)

    async def analyze_source_code(
        self,
        *,
        code: str,
        language: str,
        options: analyze_analyze_source_code_params.Options | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AnalyzeAnalyzeSourceCodeResponse:
        """
        Sends source code for static analysis and optimization insights.

        Args:
          code: Source code to analyze

          language: Programming language (e.g., python, javascript, rust)

          options: Optional analysis parameters

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/analyze",
            body=await async_maybe_transform(
                {
                    "code": code,
                    "language": language,
                    "options": options,
                },
                analyze_analyze_source_code_params.AnalyzeAnalyzeSourceCodeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AnalyzeAnalyzeSourceCodeResponse,
        )


class AnalyzeResourceWithRawResponse:
    def __init__(self, analyze: AnalyzeResource) -> None:
        self._analyze = analyze

        self.analyze_source_code = to_raw_response_wrapper(
            analyze.analyze_source_code,
        )


class AsyncAnalyzeResourceWithRawResponse:
    def __init__(self, analyze: AsyncAnalyzeResource) -> None:
        self._analyze = analyze

        self.analyze_source_code = async_to_raw_response_wrapper(
            analyze.analyze_source_code,
        )


class AnalyzeResourceWithStreamingResponse:
    def __init__(self, analyze: AnalyzeResource) -> None:
        self._analyze = analyze

        self.analyze_source_code = to_streamed_response_wrapper(
            analyze.analyze_source_code,
        )


class AsyncAnalyzeResourceWithStreamingResponse:
    def __init__(self, analyze: AsyncAnalyzeResource) -> None:
        self._analyze = analyze

        self.analyze_source_code = async_to_streamed_response_wrapper(
            analyze.analyze_source_code,
        )
