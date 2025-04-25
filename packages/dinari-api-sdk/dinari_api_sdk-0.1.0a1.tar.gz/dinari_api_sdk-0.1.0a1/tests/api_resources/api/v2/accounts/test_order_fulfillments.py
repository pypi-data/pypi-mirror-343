# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dinari_api_sdk import Dinari, AsyncDinari
from dinari_api_sdk.types.api.v2.accounts import OrderFulfillment, OrderFulfillmentQueryResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOrderFulfillments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Dinari) -> None:
        order_fulfillment = client.api.v2.accounts.order_fulfillments.retrieve(
            fulfillment_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderFulfillment, order_fulfillment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Dinari) -> None:
        response = client.api.v2.accounts.order_fulfillments.with_raw_response.retrieve(
            fulfillment_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_fulfillment = response.parse()
        assert_matches_type(OrderFulfillment, order_fulfillment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Dinari) -> None:
        with client.api.v2.accounts.order_fulfillments.with_streaming_response.retrieve(
            fulfillment_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_fulfillment = response.parse()
            assert_matches_type(OrderFulfillment, order_fulfillment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.order_fulfillments.with_raw_response.retrieve(
                fulfillment_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fulfillment_id` but received ''"):
            client.api.v2.accounts.order_fulfillments.with_raw_response.retrieve(
                fulfillment_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_query(self, client: Dinari) -> None:
        order_fulfillment = client.api.v2.accounts.order_fulfillments.query(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderFulfillmentQueryResponse, order_fulfillment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_query(self, client: Dinari) -> None:
        response = client.api.v2.accounts.order_fulfillments.with_raw_response.query(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_fulfillment = response.parse()
        assert_matches_type(OrderFulfillmentQueryResponse, order_fulfillment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_query(self, client: Dinari) -> None:
        with client.api.v2.accounts.order_fulfillments.with_streaming_response.query(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_fulfillment = response.parse()
            assert_matches_type(OrderFulfillmentQueryResponse, order_fulfillment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_query(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.order_fulfillments.with_raw_response.query(
                "",
            )


class TestAsyncOrderFulfillments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncDinari) -> None:
        order_fulfillment = await async_client.api.v2.accounts.order_fulfillments.retrieve(
            fulfillment_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderFulfillment, order_fulfillment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.order_fulfillments.with_raw_response.retrieve(
            fulfillment_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_fulfillment = await response.parse()
        assert_matches_type(OrderFulfillment, order_fulfillment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.order_fulfillments.with_streaming_response.retrieve(
            fulfillment_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_fulfillment = await response.parse()
            assert_matches_type(OrderFulfillment, order_fulfillment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.order_fulfillments.with_raw_response.retrieve(
                fulfillment_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `fulfillment_id` but received ''"):
            await async_client.api.v2.accounts.order_fulfillments.with_raw_response.retrieve(
                fulfillment_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_query(self, async_client: AsyncDinari) -> None:
        order_fulfillment = await async_client.api.v2.accounts.order_fulfillments.query(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderFulfillmentQueryResponse, order_fulfillment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_query(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.order_fulfillments.with_raw_response.query(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_fulfillment = await response.parse()
        assert_matches_type(OrderFulfillmentQueryResponse, order_fulfillment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.order_fulfillments.with_streaming_response.query(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_fulfillment = await response.parse()
            assert_matches_type(OrderFulfillmentQueryResponse, order_fulfillment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_query(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.order_fulfillments.with_raw_response.query(
                "",
            )
