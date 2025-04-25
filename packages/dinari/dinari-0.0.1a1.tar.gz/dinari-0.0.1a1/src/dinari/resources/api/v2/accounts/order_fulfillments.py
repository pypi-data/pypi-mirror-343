# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.api.v2.accounts.order_fulfillment import OrderFulfillment
from .....types.api.v2.accounts.order_fulfillment_query_response import OrderFulfillmentQueryResponse

__all__ = ["OrderFulfillmentsResource", "AsyncOrderFulfillmentsResource"]


class OrderFulfillmentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OrderFulfillmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return OrderFulfillmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrderFulfillmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return OrderFulfillmentsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        fulfillment_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderFulfillment:
        """
        Retrieves details of a specific order fulfillment by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not fulfillment_id:
            raise ValueError(f"Expected a non-empty value for `fulfillment_id` but received {fulfillment_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}/order_fulfillments/{fulfillment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderFulfillment,
        )

    def query(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderFulfillmentQueryResponse:
        """
        Queries all order fulfillments under the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            f"/api/v2/accounts/{account_id}/order_fulfillments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderFulfillmentQueryResponse,
        )


class AsyncOrderFulfillmentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOrderFulfillmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOrderFulfillmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrderFulfillmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/dinaricrypto/dinari-api-sdk-python#with_streaming_response
        """
        return AsyncOrderFulfillmentsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        fulfillment_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderFulfillment:
        """
        Retrieves details of a specific order fulfillment by its ID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not fulfillment_id:
            raise ValueError(f"Expected a non-empty value for `fulfillment_id` but received {fulfillment_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}/order_fulfillments/{fulfillment_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderFulfillment,
        )

    async def query(
        self,
        account_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OrderFulfillmentQueryResponse:
        """
        Queries all order fulfillments under the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            f"/api/v2/accounts/{account_id}/order_fulfillments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OrderFulfillmentQueryResponse,
        )


class OrderFulfillmentsResourceWithRawResponse:
    def __init__(self, order_fulfillments: OrderFulfillmentsResource) -> None:
        self._order_fulfillments = order_fulfillments

        self.retrieve = to_raw_response_wrapper(
            order_fulfillments.retrieve,
        )
        self.query = to_raw_response_wrapper(
            order_fulfillments.query,
        )


class AsyncOrderFulfillmentsResourceWithRawResponse:
    def __init__(self, order_fulfillments: AsyncOrderFulfillmentsResource) -> None:
        self._order_fulfillments = order_fulfillments

        self.retrieve = async_to_raw_response_wrapper(
            order_fulfillments.retrieve,
        )
        self.query = async_to_raw_response_wrapper(
            order_fulfillments.query,
        )


class OrderFulfillmentsResourceWithStreamingResponse:
    def __init__(self, order_fulfillments: OrderFulfillmentsResource) -> None:
        self._order_fulfillments = order_fulfillments

        self.retrieve = to_streamed_response_wrapper(
            order_fulfillments.retrieve,
        )
        self.query = to_streamed_response_wrapper(
            order_fulfillments.query,
        )


class AsyncOrderFulfillmentsResourceWithStreamingResponse:
    def __init__(self, order_fulfillments: AsyncOrderFulfillmentsResource) -> None:
        self._order_fulfillments = order_fulfillments

        self.retrieve = async_to_streamed_response_wrapper(
            order_fulfillments.retrieve,
        )
        self.query = async_to_streamed_response_wrapper(
            order_fulfillments.query,
        )
