# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.api.v2.accounts import (
    order_request_create_limit_buy_params,
    order_request_create_limit_sell_params,
    order_request_create_market_buy_params,
    order_request_create_market_sell_params,
)
from .....types.api.v2.accounts.order_request import OrderRequest
from .....types.api.v2.accounts.order_request_list_response import OrderRequestListResponse

__all__ = ["OrderRequestsResource", "AsyncOrderRequestsResource"]


class OrderRequestsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OrderRequestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return OrderRequestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrderRequestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return OrderRequestsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        request_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Retrieves details of a specific managed order request by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not request_id:
            raise ValueError(f"Expected a non-empty value for `request_id` but received {request_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}/order_requests/{request_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )

    def list(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequestListResponse:
        """
        Lists managed order requests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}/order_requests",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequestListResponse,
        )

    def create_limit_buy(
        self,
        account_id: str,
        *,
        asset_quantity: int,
        limit_price: float,
        stock_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Creates a managed limit buy request.

        Args:
          asset_quantity: Quantity of stock to trade. Must be a positive integer.

          limit_price: Price at which to execute the order. Must be a positive number with a precision
              of up to 2 decimal places.

          stock_id: ID of stock, as returned by the `/stocks` endpoint, e.g. 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            f"/api/v2/accounts/{account_id}/order_requests/limit_buy",
            body=maybe_transform(
                {
                    "asset_quantity": asset_quantity,
                    "limit_price": limit_price,
                    "stock_id": stock_id,
                },
                order_request_create_limit_buy_params.OrderRequestCreateLimitBuyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )

    def create_limit_sell(
        self,
        account_id: str,
        *,
        asset_quantity: int,
        limit_price: float,
        stock_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Creates a managed limit sell request.

        Args:
          asset_quantity: Quantity of stock to trade. Must be a positive integer.

          limit_price: Price at which to execute the order. Must be a positive number with a precision
              of up to 2 decimal places.

          stock_id: ID of stock, as returned by the `/stocks` endpoint, e.g. 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            f"/api/v2/accounts/{account_id}/order_requests/limit_sell",
            body=maybe_transform(
                {
                    "asset_quantity": asset_quantity,
                    "limit_price": limit_price,
                    "stock_id": stock_id,
                },
                order_request_create_limit_sell_params.OrderRequestCreateLimitSellParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )

    def create_market_buy(
        self,
        account_id: str,
        *,
        payment_amount: float,
        stock_id: str,
        include_fees: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Creates a managed market buy request.

        Args:
          payment_amount: Amount of USD to pay or receive for the order. Must be a positive number with a
              precision of up to 2 decimal places.

          stock_id: ID of stock, as returned by the `/stocks` endpoint, e.g. 1

          include_fees: Whether to include fees in the `payment_amount` input field.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            f"/api/v2/accounts/{account_id}/order_requests/market_buy",
            body=maybe_transform(
                {
                    "payment_amount": payment_amount,
                    "stock_id": stock_id,
                    "include_fees": include_fees,
                },
                order_request_create_market_buy_params.OrderRequestCreateMarketBuyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )

    def create_market_sell(
        self,
        account_id: str,
        *,
        asset_quantity: float,
        stock_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Creates a managed market sell request.

        Args:
          asset_quantity: Quantity of stock to trade. Must be a positive number with a precision of up to
              9 decimal places.

          stock_id: ID of stock, as returned by the `/stocks` endpoint, e.g. 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            f"/api/v2/accounts/{account_id}/order_requests/market_sell",
            body=maybe_transform(
                {
                    "asset_quantity": asset_quantity,
                    "stock_id": stock_id,
                },
                order_request_create_market_sell_params.OrderRequestCreateMarketSellParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )


class AsyncOrderRequestsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOrderRequestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOrderRequestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrderRequestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return AsyncOrderRequestsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        request_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Retrieves details of a specific managed order request by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not request_id:
            raise ValueError(f"Expected a non-empty value for `request_id` but received {request_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}/order_requests/{request_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )

    async def list(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequestListResponse:
        """
        Lists managed order requests.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}/order_requests",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequestListResponse,
        )

    async def create_limit_buy(
        self,
        account_id: str,
        *,
        asset_quantity: int,
        limit_price: float,
        stock_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Creates a managed limit buy request.

        Args:
          asset_quantity: Quantity of stock to trade. Must be a positive integer.

          limit_price: Price at which to execute the order. Must be a positive number with a precision
              of up to 2 decimal places.

          stock_id: ID of stock, as returned by the `/stocks` endpoint, e.g. 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            f"/api/v2/accounts/{account_id}/order_requests/limit_buy",
            body=await async_maybe_transform(
                {
                    "asset_quantity": asset_quantity,
                    "limit_price": limit_price,
                    "stock_id": stock_id,
                },
                order_request_create_limit_buy_params.OrderRequestCreateLimitBuyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )

    async def create_limit_sell(
        self,
        account_id: str,
        *,
        asset_quantity: int,
        limit_price: float,
        stock_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Creates a managed limit sell request.

        Args:
          asset_quantity: Quantity of stock to trade. Must be a positive integer.

          limit_price: Price at which to execute the order. Must be a positive number with a precision
              of up to 2 decimal places.

          stock_id: ID of stock, as returned by the `/stocks` endpoint, e.g. 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            f"/api/v2/accounts/{account_id}/order_requests/limit_sell",
            body=await async_maybe_transform(
                {
                    "asset_quantity": asset_quantity,
                    "limit_price": limit_price,
                    "stock_id": stock_id,
                },
                order_request_create_limit_sell_params.OrderRequestCreateLimitSellParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )

    async def create_market_buy(
        self,
        account_id: str,
        *,
        payment_amount: float,
        stock_id: str,
        include_fees: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Creates a managed market buy request.

        Args:
          payment_amount: Amount of USD to pay or receive for the order. Must be a positive number with a
              precision of up to 2 decimal places.

          stock_id: ID of stock, as returned by the `/stocks` endpoint, e.g. 1

          include_fees: Whether to include fees in the `payment_amount` input field.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            f"/api/v2/accounts/{account_id}/order_requests/market_buy",
            body=await async_maybe_transform(
                {
                    "payment_amount": payment_amount,
                    "stock_id": stock_id,
                    "include_fees": include_fees,
                },
                order_request_create_market_buy_params.OrderRequestCreateMarketBuyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )

    async def create_market_sell(
        self,
        account_id: str,
        *,
        asset_quantity: float,
        stock_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderRequest:
        """
        Creates a managed market sell request.

        Args:
          asset_quantity: Quantity of stock to trade. Must be a positive number with a precision of up to
              9 decimal places.

          stock_id: ID of stock, as returned by the `/stocks` endpoint, e.g. 1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            f"/api/v2/accounts/{account_id}/order_requests/market_sell",
            body=await async_maybe_transform(
                {
                    "asset_quantity": asset_quantity,
                    "stock_id": stock_id,
                },
                order_request_create_market_sell_params.OrderRequestCreateMarketSellParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderRequest,
        )


class OrderRequestsResourceWithRawResponse:
    def __init__(self, order_requests: OrderRequestsResource) -> None:
        self._order_requests = order_requests

        self.retrieve = to_raw_response_wrapper(
            order_requests.retrieve,
        )
        self.list = to_raw_response_wrapper(
            order_requests.list,
        )
        self.create_limit_buy = to_raw_response_wrapper(
            order_requests.create_limit_buy,
        )
        self.create_limit_sell = to_raw_response_wrapper(
            order_requests.create_limit_sell,
        )
        self.create_market_buy = to_raw_response_wrapper(
            order_requests.create_market_buy,
        )
        self.create_market_sell = to_raw_response_wrapper(
            order_requests.create_market_sell,
        )


class AsyncOrderRequestsResourceWithRawResponse:
    def __init__(self, order_requests: AsyncOrderRequestsResource) -> None:
        self._order_requests = order_requests

        self.retrieve = async_to_raw_response_wrapper(
            order_requests.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            order_requests.list,
        )
        self.create_limit_buy = async_to_raw_response_wrapper(
            order_requests.create_limit_buy,
        )
        self.create_limit_sell = async_to_raw_response_wrapper(
            order_requests.create_limit_sell,
        )
        self.create_market_buy = async_to_raw_response_wrapper(
            order_requests.create_market_buy,
        )
        self.create_market_sell = async_to_raw_response_wrapper(
            order_requests.create_market_sell,
        )


class OrderRequestsResourceWithStreamingResponse:
    def __init__(self, order_requests: OrderRequestsResource) -> None:
        self._order_requests = order_requests

        self.retrieve = to_streamed_response_wrapper(
            order_requests.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            order_requests.list,
        )
        self.create_limit_buy = to_streamed_response_wrapper(
            order_requests.create_limit_buy,
        )
        self.create_limit_sell = to_streamed_response_wrapper(
            order_requests.create_limit_sell,
        )
        self.create_market_buy = to_streamed_response_wrapper(
            order_requests.create_market_buy,
        )
        self.create_market_sell = to_streamed_response_wrapper(
            order_requests.create_market_sell,
        )


class AsyncOrderRequestsResourceWithStreamingResponse:
    def __init__(self, order_requests: AsyncOrderRequestsResource) -> None:
        self._order_requests = order_requests

        self.retrieve = async_to_streamed_response_wrapper(
            order_requests.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            order_requests.list,
        )
        self.create_limit_buy = async_to_streamed_response_wrapper(
            order_requests.create_limit_buy,
        )
        self.create_limit_sell = async_to_streamed_response_wrapper(
            order_requests.create_limit_sell,
        )
        self.create_market_buy = async_to_streamed_response_wrapper(
            order_requests.create_market_buy,
        )
        self.create_market_sell = async_to_streamed_response_wrapper(
            order_requests.create_market_sell,
        )
