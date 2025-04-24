# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from deepcode import Deepcode, AsyncDeepcode
from tests.utils import assert_matches_type
from deepcode.types import StatusCheckStatusResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStatus:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_check_status(self, client: Deepcode) -> None:
        status = client.status.check_status()
        assert_matches_type(StatusCheckStatusResponse, status, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_check_status(self, client: Deepcode) -> None:
        response = client.status.with_raw_response.check_status()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        status = response.parse()
        assert_matches_type(StatusCheckStatusResponse, status, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_check_status(self, client: Deepcode) -> None:
        with client.status.with_streaming_response.check_status() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            status = response.parse()
            assert_matches_type(StatusCheckStatusResponse, status, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStatus:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_check_status(self, async_client: AsyncDeepcode) -> None:
        status = await async_client.status.check_status()
        assert_matches_type(StatusCheckStatusResponse, status, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_check_status(self, async_client: AsyncDeepcode) -> None:
        response = await async_client.status.with_raw_response.check_status()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        status = await response.parse()
        assert_matches_type(StatusCheckStatusResponse, status, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_check_status(self, async_client: AsyncDeepcode) -> None:
        async with async_client.status.with_streaming_response.check_status() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            status = await response.parse()
            assert_matches_type(StatusCheckStatusResponse, status, path=["response"])

        assert cast(Any, response.is_closed) is True
