# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .orders import (
    OrdersResource,
    AsyncOrdersResource,
    OrdersResourceWithRawResponse,
    AsyncOrdersResourceWithRawResponse,
    OrdersResourceWithStreamingResponse,
    AsyncOrdersResourceWithStreamingResponse,
)
from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .wallet.wallet import (
    WalletResource,
    AsyncWalletResource,
    WalletResourceWithRawResponse,
    AsyncWalletResourceWithRawResponse,
    WalletResourceWithStreamingResponse,
    AsyncWalletResourceWithStreamingResponse,
)
from .order_requests import (
    OrderRequestsResource,
    AsyncOrderRequestsResource,
    OrderRequestsResourceWithRawResponse,
    AsyncOrderRequestsResourceWithRawResponse,
    OrderRequestsResourceWithStreamingResponse,
    AsyncOrderRequestsResourceWithStreamingResponse,
)
from ....._base_client import make_request_options
from .order_fulfillments import (
    OrderFulfillmentsResource,
    AsyncOrderFulfillmentsResource,
    OrderFulfillmentsResourceWithRawResponse,
    AsyncOrderFulfillmentsResourceWithRawResponse,
    OrderFulfillmentsResourceWithStreamingResponse,
    AsyncOrderFulfillmentsResourceWithStreamingResponse,
)
from .....types.api.v2.entities.account import Account
from .....types.api.v2.account_retrieve_cash_response import AccountRetrieveCashResponse
from .....types.api.v2.account_retrieve_portfolio_response import AccountRetrievePortfolioResponse
from .....types.api.v2.account_retrieve_dividend_payments_response import AccountRetrieveDividendPaymentsResponse
from .....types.api.v2.account_retrieve_interest_payments_response import AccountRetrieveInterestPaymentsResponse

__all__ = ["AccountsResource", "AsyncAccountsResource"]


class AccountsResource(SyncAPIResource):
    @cached_property
    def wallet(self) -> WalletResource:
        return WalletResource(self._client)

    @cached_property
    def orders(self) -> OrdersResource:
        return OrdersResource(self._client)

    @cached_property
    def order_fulfillments(self) -> OrderFulfillmentsResource:
        return OrderFulfillmentsResource(self._client)

    @cached_property
    def order_requests(self) -> OrderRequestsResource:
        return OrderRequestsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return AccountsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Account:
        """
        Retrieves a specific account by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Account,
        )

    def deactivate(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Account:
        """
        Sets the account to be inactive.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            f"/api/v2/accounts/{account_id}/deactivate",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Account,
        )

    def retrieve_cash(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveCashResponse:
        """
        Retrieves the cash amount in the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}/cash",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveCashResponse,
        )

    def retrieve_dividend_payments(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveDividendPaymentsResponse:
        """
        Retrieves dividend payments made to the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}/dividend_payments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveDividendPaymentsResponse,
        )

    def retrieve_interest_payments(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveInterestPaymentsResponse:
        """
        Retrieves interest payments made to the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}/interest_payments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveInterestPaymentsResponse,
        )

    def retrieve_portfolio(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrievePortfolioResponse:
        """
        Retrieves the portfolio of the account, sans cash equivalents.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}/portfolio",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrievePortfolioResponse,
        )


class AsyncAccountsResource(AsyncAPIResource):
    @cached_property
    def wallet(self) -> AsyncWalletResource:
        return AsyncWalletResource(self._client)

    @cached_property
    def orders(self) -> AsyncOrdersResource:
        return AsyncOrdersResource(self._client)

    @cached_property
    def order_fulfillments(self) -> AsyncOrderFulfillmentsResource:
        return AsyncOrderFulfillmentsResource(self._client)

    @cached_property
    def order_requests(self) -> AsyncOrderRequestsResource:
        return AsyncOrderRequestsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return AsyncAccountsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Account:
        """
        Retrieves a specific account by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Account,
        )

    async def deactivate(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Account:
        """
        Sets the account to be inactive.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            f"/api/v2/accounts/{account_id}/deactivate",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Account,
        )

    async def retrieve_cash(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveCashResponse:
        """
        Retrieves the cash amount in the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}/cash",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveCashResponse,
        )

    async def retrieve_dividend_payments(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveDividendPaymentsResponse:
        """
        Retrieves dividend payments made to the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}/dividend_payments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveDividendPaymentsResponse,
        )

    async def retrieve_interest_payments(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrieveInterestPaymentsResponse:
        """
        Retrieves interest payments made to the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}/interest_payments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveInterestPaymentsResponse,
        )

    async def retrieve_portfolio(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AccountRetrievePortfolioResponse:
        """
        Retrieves the portfolio of the account, sans cash equivalents.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}/portfolio",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrievePortfolioResponse,
        )


class AccountsResourceWithRawResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = to_raw_response_wrapper(
            accounts.retrieve,
        )
        self.deactivate = to_raw_response_wrapper(
            accounts.deactivate,
        )
        self.retrieve_cash = to_raw_response_wrapper(
            accounts.retrieve_cash,
        )
        self.retrieve_dividend_payments = to_raw_response_wrapper(
            accounts.retrieve_dividend_payments,
        )
        self.retrieve_interest_payments = to_raw_response_wrapper(
            accounts.retrieve_interest_payments,
        )
        self.retrieve_portfolio = to_raw_response_wrapper(
            accounts.retrieve_portfolio,
        )

    @cached_property
    def wallet(self) -> WalletResourceWithRawResponse:
        return WalletResourceWithRawResponse(self._accounts.wallet)

    @cached_property
    def orders(self) -> OrdersResourceWithRawResponse:
        return OrdersResourceWithRawResponse(self._accounts.orders)

    @cached_property
    def order_fulfillments(self) -> OrderFulfillmentsResourceWithRawResponse:
        return OrderFulfillmentsResourceWithRawResponse(self._accounts.order_fulfillments)

    @cached_property
    def order_requests(self) -> OrderRequestsResourceWithRawResponse:
        return OrderRequestsResourceWithRawResponse(self._accounts.order_requests)


class AsyncAccountsResourceWithRawResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = async_to_raw_response_wrapper(
            accounts.retrieve,
        )
        self.deactivate = async_to_raw_response_wrapper(
            accounts.deactivate,
        )
        self.retrieve_cash = async_to_raw_response_wrapper(
            accounts.retrieve_cash,
        )
        self.retrieve_dividend_payments = async_to_raw_response_wrapper(
            accounts.retrieve_dividend_payments,
        )
        self.retrieve_interest_payments = async_to_raw_response_wrapper(
            accounts.retrieve_interest_payments,
        )
        self.retrieve_portfolio = async_to_raw_response_wrapper(
            accounts.retrieve_portfolio,
        )

    @cached_property
    def wallet(self) -> AsyncWalletResourceWithRawResponse:
        return AsyncWalletResourceWithRawResponse(self._accounts.wallet)

    @cached_property
    def orders(self) -> AsyncOrdersResourceWithRawResponse:
        return AsyncOrdersResourceWithRawResponse(self._accounts.orders)

    @cached_property
    def order_fulfillments(self) -> AsyncOrderFulfillmentsResourceWithRawResponse:
        return AsyncOrderFulfillmentsResourceWithRawResponse(self._accounts.order_fulfillments)

    @cached_property
    def order_requests(self) -> AsyncOrderRequestsResourceWithRawResponse:
        return AsyncOrderRequestsResourceWithRawResponse(self._accounts.order_requests)


class AccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = to_streamed_response_wrapper(
            accounts.retrieve,
        )
        self.deactivate = to_streamed_response_wrapper(
            accounts.deactivate,
        )
        self.retrieve_cash = to_streamed_response_wrapper(
            accounts.retrieve_cash,
        )
        self.retrieve_dividend_payments = to_streamed_response_wrapper(
            accounts.retrieve_dividend_payments,
        )
        self.retrieve_interest_payments = to_streamed_response_wrapper(
            accounts.retrieve_interest_payments,
        )
        self.retrieve_portfolio = to_streamed_response_wrapper(
            accounts.retrieve_portfolio,
        )

    @cached_property
    def wallet(self) -> WalletResourceWithStreamingResponse:
        return WalletResourceWithStreamingResponse(self._accounts.wallet)

    @cached_property
    def orders(self) -> OrdersResourceWithStreamingResponse:
        return OrdersResourceWithStreamingResponse(self._accounts.orders)

    @cached_property
    def order_fulfillments(self) -> OrderFulfillmentsResourceWithStreamingResponse:
        return OrderFulfillmentsResourceWithStreamingResponse(self._accounts.order_fulfillments)

    @cached_property
    def order_requests(self) -> OrderRequestsResourceWithStreamingResponse:
        return OrderRequestsResourceWithStreamingResponse(self._accounts.order_requests)


class AsyncAccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = async_to_streamed_response_wrapper(
            accounts.retrieve,
        )
        self.deactivate = async_to_streamed_response_wrapper(
            accounts.deactivate,
        )
        self.retrieve_cash = async_to_streamed_response_wrapper(
            accounts.retrieve_cash,
        )
        self.retrieve_dividend_payments = async_to_streamed_response_wrapper(
            accounts.retrieve_dividend_payments,
        )
        self.retrieve_interest_payments = async_to_streamed_response_wrapper(
            accounts.retrieve_interest_payments,
        )
        self.retrieve_portfolio = async_to_streamed_response_wrapper(
            accounts.retrieve_portfolio,
        )

    @cached_property
    def wallet(self) -> AsyncWalletResourceWithStreamingResponse:
        return AsyncWalletResourceWithStreamingResponse(self._accounts.wallet)

    @cached_property
    def orders(self) -> AsyncOrdersResourceWithStreamingResponse:
        return AsyncOrdersResourceWithStreamingResponse(self._accounts.orders)

    @cached_property
    def order_fulfillments(self) -> AsyncOrderFulfillmentsResourceWithStreamingResponse:
        return AsyncOrderFulfillmentsResourceWithStreamingResponse(self._accounts.order_fulfillments)

    @cached_property
    def order_requests(self) -> AsyncOrderRequestsResourceWithStreamingResponse:
        return AsyncOrderRequestsResourceWithStreamingResponse(self._accounts.order_requests)
