# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ... import _resource
from .v2.v2 import (
    V2Resource,
    AsyncV2Resource,
    V2ResourceWithRawResponse,
    AsyncV2ResourceWithRawResponse,
    V2ResourceWithStreamingResponse,
    AsyncV2ResourceWithStreamingResponse,
)
from ..._compat import cached_property

__all__ = ["APIResource", "AsyncAPIResource"]


class APIResource(_resource.SyncAPIResource):
    @cached_property
    def v2(self) -> V2Resource:
        return V2Resource(self._client)

    @cached_property
    def with_raw_response(self) -> APIResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return APIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> APIResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return APIResourceWithStreamingResponse(self)


class AsyncAPIResource(_resource.AsyncAPIResource):
    @cached_property
    def v2(self) -> AsyncV2Resource:
        return AsyncV2Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAPIResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAPIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAPIResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return AsyncAPIResourceWithStreamingResponse(self)


class APIResourceWithRawResponse:
    def __init__(self, api: APIResource) -> None:
        self._api = api

    @cached_property
    def v2(self) -> V2ResourceWithRawResponse:
        return V2ResourceWithRawResponse(self._api.v2)


class AsyncAPIResourceWithRawResponse:
    def __init__(self, api: AsyncAPIResource) -> None:
        self._api = api

    @cached_property
    def v2(self) -> AsyncV2ResourceWithRawResponse:
        return AsyncV2ResourceWithRawResponse(self._api.v2)


class APIResourceWithStreamingResponse:
    def __init__(self, api: APIResource) -> None:
        self._api = api

    @cached_property
    def v2(self) -> V2ResourceWithStreamingResponse:
        return V2ResourceWithStreamingResponse(self._api.v2)


class AsyncAPIResourceWithStreamingResponse:
    def __init__(self, api: AsyncAPIResource) -> None:
        self._api = api

    @cached_property
    def v2(self) -> AsyncV2ResourceWithStreamingResponse:
        return AsyncV2ResourceWithStreamingResponse(self._api.v2)
