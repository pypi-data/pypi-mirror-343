# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from deepcode import Deepcode, AsyncDeepcode
from tests.utils import assert_matches_type
from deepcode.types import AnalyzeAnalyzeSourceCodeResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAnalyze:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_analyze_source_code(self, client: Deepcode) -> None:
        analyze = client.analyze.analyze_source_code(
            code="code",
            language="language",
        )
        assert_matches_type(AnalyzeAnalyzeSourceCodeResponse, analyze, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_analyze_source_code_with_all_params(self, client: Deepcode) -> None:
        analyze = client.analyze.analyze_source_code(
            code="code",
            language="language",
            options={
                "deep": True,
                "performance_hints": True,
            },
        )
        assert_matches_type(AnalyzeAnalyzeSourceCodeResponse, analyze, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_analyze_source_code(self, client: Deepcode) -> None:
        response = client.analyze.with_raw_response.analyze_source_code(
            code="code",
            language="language",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        analyze = response.parse()
        assert_matches_type(AnalyzeAnalyzeSourceCodeResponse, analyze, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_analyze_source_code(self, client: Deepcode) -> None:
        with client.analyze.with_streaming_response.analyze_source_code(
            code="code",
            language="language",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            analyze = response.parse()
            assert_matches_type(AnalyzeAnalyzeSourceCodeResponse, analyze, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAnalyze:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_analyze_source_code(self, async_client: AsyncDeepcode) -> None:
        analyze = await async_client.analyze.analyze_source_code(
            code="code",
            language="language",
        )
        assert_matches_type(AnalyzeAnalyzeSourceCodeResponse, analyze, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_analyze_source_code_with_all_params(self, async_client: AsyncDeepcode) -> None:
        analyze = await async_client.analyze.analyze_source_code(
            code="code",
            language="language",
            options={
                "deep": True,
                "performance_hints": True,
            },
        )
        assert_matches_type(AnalyzeAnalyzeSourceCodeResponse, analyze, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_analyze_source_code(self, async_client: AsyncDeepcode) -> None:
        response = await async_client.analyze.with_raw_response.analyze_source_code(
            code="code",
            language="language",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        analyze = await response.parse()
        assert_matches_type(AnalyzeAnalyzeSourceCodeResponse, analyze, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_analyze_source_code(self, async_client: AsyncDeepcode) -> None:
        async with async_client.analyze.with_streaming_response.analyze_source_code(
            code="code",
            language="language",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            analyze = await response.parse()
            assert_matches_type(AnalyzeAnalyzeSourceCodeResponse, analyze, path=["response"])

        assert cast(Any, response.is_closed) is True
