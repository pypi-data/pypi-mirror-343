# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dinari_api_sdk import Dinari, AsyncDinari
from dinari_api_sdk.types.api import V2GetHealthResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV2:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_health(self, client: Dinari) -> None:
        v2 = client.api.v2.get_health()
        assert_matches_type(V2GetHealthResponse, v2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_health(self, client: Dinari) -> None:
        response = client.api.v2.with_raw_response.get_health()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v2 = response.parse()
        assert_matches_type(V2GetHealthResponse, v2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_health(self, client: Dinari) -> None:
        with client.api.v2.with_streaming_response.get_health() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v2 = response.parse()
            assert_matches_type(V2GetHealthResponse, v2, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncV2:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_health(self, async_client: AsyncDinari) -> None:
        v2 = await async_client.api.v2.get_health()
        assert_matches_type(V2GetHealthResponse, v2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_health(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.with_raw_response.get_health()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v2 = await response.parse()
        assert_matches_type(V2GetHealthResponse, v2, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_health(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.with_streaming_response.get_health() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v2 = await response.parse()
            assert_matches_type(V2GetHealthResponse, v2, path=["response"])

        assert cast(Any, response.is_closed) is True
