# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from .accounts.accounts import (
    AccountsResource,
    AsyncAccountsResource,
    AccountsResourceWithRawResponse,
    AsyncAccountsResourceWithRawResponse,
    AccountsResourceWithStreamingResponse,
    AsyncAccountsResourceWithStreamingResponse,
)
from .entities.entities import (
    EntitiesResource,
    AsyncEntitiesResource,
    EntitiesResourceWithRawResponse,
    AsyncEntitiesResourceWithRawResponse,
    EntitiesResourceWithStreamingResponse,
    AsyncEntitiesResourceWithStreamingResponse,
)
from .market_data.market_data import (
    MarketDataResource,
    AsyncMarketDataResource,
    MarketDataResourceWithRawResponse,
    AsyncMarketDataResourceWithRawResponse,
    MarketDataResourceWithStreamingResponse,
    AsyncMarketDataResourceWithStreamingResponse,
)
from ....types.api.v2_get_health_response import V2GetHealthResponse

__all__ = ["V2Resource", "AsyncV2Resource"]


class V2Resource(SyncAPIResource):
    @cached_property
    def market_data(self) -> MarketDataResource:
        return MarketDataResource(self._client)

    @cached_property
    def entities(self) -> EntitiesResource:
        return EntitiesResource(self._client)

    @cached_property
    def accounts(self) -> AccountsResource:
        return AccountsResource(self._client)

    @cached_property
    def with_raw_response(self) -> V2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return V2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return V2ResourceWithStreamingResponse(self)

    def get_health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V2GetHealthResponse:
        """Get Health Status"""
        return self._get(
            "/api/v2/_health/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V2GetHealthResponse,
        )


class AsyncV2Resource(AsyncAPIResource):
    @cached_property
    def market_data(self) -> AsyncMarketDataResource:
        return AsyncMarketDataResource(self._client)

    @cached_property
    def entities(self) -> AsyncEntitiesResource:
        return AsyncEntitiesResource(self._client)

    @cached_property
    def accounts(self) -> AsyncAccountsResource:
        return AsyncAccountsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncV2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncV2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return AsyncV2ResourceWithStreamingResponse(self)

    async def get_health(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V2GetHealthResponse:
        """Get Health Status"""
        return await self._get(
            "/api/v2/_health/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V2GetHealthResponse,
        )


class V2ResourceWithRawResponse:
    def __init__(self, v2: V2Resource) -> None:
        self._v2 = v2

        self.get_health = to_raw_response_wrapper(
            v2.get_health,
        )

    @cached_property
    def market_data(self) -> MarketDataResourceWithRawResponse:
        return MarketDataResourceWithRawResponse(self._v2.market_data)

    @cached_property
    def entities(self) -> EntitiesResourceWithRawResponse:
        return EntitiesResourceWithRawResponse(self._v2.entities)

    @cached_property
    def accounts(self) -> AccountsResourceWithRawResponse:
        return AccountsResourceWithRawResponse(self._v2.accounts)


class AsyncV2ResourceWithRawResponse:
    def __init__(self, v2: AsyncV2Resource) -> None:
        self._v2 = v2

        self.get_health = async_to_raw_response_wrapper(
            v2.get_health,
        )

    @cached_property
    def market_data(self) -> AsyncMarketDataResourceWithRawResponse:
        return AsyncMarketDataResourceWithRawResponse(self._v2.market_data)

    @cached_property
    def entities(self) -> AsyncEntitiesResourceWithRawResponse:
        return AsyncEntitiesResourceWithRawResponse(self._v2.entities)

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithRawResponse:
        return AsyncAccountsResourceWithRawResponse(self._v2.accounts)


class V2ResourceWithStreamingResponse:
    def __init__(self, v2: V2Resource) -> None:
        self._v2 = v2

        self.get_health = to_streamed_response_wrapper(
            v2.get_health,
        )

    @cached_property
    def market_data(self) -> MarketDataResourceWithStreamingResponse:
        return MarketDataResourceWithStreamingResponse(self._v2.market_data)

    @cached_property
    def entities(self) -> EntitiesResourceWithStreamingResponse:
        return EntitiesResourceWithStreamingResponse(self._v2.entities)

    @cached_property
    def accounts(self) -> AccountsResourceWithStreamingResponse:
        return AccountsResourceWithStreamingResponse(self._v2.accounts)


class AsyncV2ResourceWithStreamingResponse:
    def __init__(self, v2: AsyncV2Resource) -> None:
        self._v2 = v2

        self.get_health = async_to_streamed_response_wrapper(
            v2.get_health,
        )

    @cached_property
    def market_data(self) -> AsyncMarketDataResourceWithStreamingResponse:
        return AsyncMarketDataResourceWithStreamingResponse(self._v2.market_data)

    @cached_property
    def entities(self) -> AsyncEntitiesResourceWithStreamingResponse:
        return AsyncEntitiesResourceWithStreamingResponse(self._v2.entities)

    @cached_property
    def accounts(self) -> AsyncAccountsResourceWithStreamingResponse:
        return AsyncAccountsResourceWithStreamingResponse(self._v2.accounts)
