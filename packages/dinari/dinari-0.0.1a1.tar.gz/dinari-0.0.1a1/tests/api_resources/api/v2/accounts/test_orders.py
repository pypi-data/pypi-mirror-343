# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from dinari import Dinari, AsyncDinari
from tests.utils import assert_matches_type
from dinari.types.api.v2.accounts import (
    Order,
    OrderListResponse,
    OrderGetEstimatedFeeResponse,
    OrderRetrieveFulfillmentsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOrders:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Dinari) -> None:
        order = client.api.v2.accounts.orders.retrieve(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Order, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Dinari) -> None:
        response = client.api.v2.accounts.orders.with_raw_response.retrieve(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(Order, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Dinari) -> None:
        with client.api.v2.accounts.orders.with_streaming_response.retrieve(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(Order, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.orders.with_raw_response.retrieve(
                order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.api.v2.accounts.orders.with_raw_response.retrieve(
                order_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Dinari) -> None:
        order = client.api.v2.accounts.orders.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Dinari) -> None:
        response = client.api.v2.accounts.orders.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Dinari) -> None:
        with client.api.v2.accounts.orders.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderListResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.orders.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_cancel(self, client: Dinari) -> None:
        order = client.api.v2.accounts.orders.cancel(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Order, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_cancel(self, client: Dinari) -> None:
        response = client.api.v2.accounts.orders.with_raw_response.cancel(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(Order, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_cancel(self, client: Dinari) -> None:
        with client.api.v2.accounts.orders.with_streaming_response.cancel(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(Order, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_cancel(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.orders.with_raw_response.cancel(
                order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.api.v2.accounts.orders.with_raw_response.cancel(
                order_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_estimated_fee(self, client: Dinari) -> None:
        order = client.api.v2.accounts.orders.get_estimated_fee(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            chain_id=0,
            contract_address="contract_address",
            order_data={"foo": "string"},
        )
        assert_matches_type(OrderGetEstimatedFeeResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_estimated_fee(self, client: Dinari) -> None:
        response = client.api.v2.accounts.orders.with_raw_response.get_estimated_fee(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            chain_id=0,
            contract_address="contract_address",
            order_data={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderGetEstimatedFeeResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_estimated_fee(self, client: Dinari) -> None:
        with client.api.v2.accounts.orders.with_streaming_response.get_estimated_fee(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            chain_id=0,
            contract_address="contract_address",
            order_data={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderGetEstimatedFeeResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_estimated_fee(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.orders.with_raw_response.get_estimated_fee(
                account_id="",
                chain_id=0,
                contract_address="contract_address",
                order_data={"foo": "string"},
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_fulfillments(self, client: Dinari) -> None:
        order = client.api.v2.accounts.orders.retrieve_fulfillments(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderRetrieveFulfillmentsResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_fulfillments(self, client: Dinari) -> None:
        response = client.api.v2.accounts.orders.with_raw_response.retrieve_fulfillments(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = response.parse()
        assert_matches_type(OrderRetrieveFulfillmentsResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_fulfillments(self, client: Dinari) -> None:
        with client.api.v2.accounts.orders.with_streaming_response.retrieve_fulfillments(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = response.parse()
            assert_matches_type(OrderRetrieveFulfillmentsResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_fulfillments(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.orders.with_raw_response.retrieve_fulfillments(
                order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            client.api.v2.accounts.orders.with_raw_response.retrieve_fulfillments(
                order_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )


class TestAsyncOrders:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncDinari) -> None:
        order = await async_client.api.v2.accounts.orders.retrieve(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Order, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.orders.with_raw_response.retrieve(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(Order, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.orders.with_streaming_response.retrieve(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(Order, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.orders.with_raw_response.retrieve(
                order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.api.v2.accounts.orders.with_raw_response.retrieve(
                order_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncDinari) -> None:
        order = await async_client.api.v2.accounts.orders.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.orders.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderListResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.orders.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderListResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.orders.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_cancel(self, async_client: AsyncDinari) -> None:
        order = await async_client.api.v2.accounts.orders.cancel(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Order, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.orders.with_raw_response.cancel(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(Order, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.orders.with_streaming_response.cancel(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(Order, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.orders.with_raw_response.cancel(
                order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.api.v2.accounts.orders.with_raw_response.cancel(
                order_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_estimated_fee(self, async_client: AsyncDinari) -> None:
        order = await async_client.api.v2.accounts.orders.get_estimated_fee(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            chain_id=0,
            contract_address="contract_address",
            order_data={"foo": "string"},
        )
        assert_matches_type(OrderGetEstimatedFeeResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_estimated_fee(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.orders.with_raw_response.get_estimated_fee(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            chain_id=0,
            contract_address="contract_address",
            order_data={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderGetEstimatedFeeResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_estimated_fee(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.orders.with_streaming_response.get_estimated_fee(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            chain_id=0,
            contract_address="contract_address",
            order_data={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderGetEstimatedFeeResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_estimated_fee(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.orders.with_raw_response.get_estimated_fee(
                account_id="",
                chain_id=0,
                contract_address="contract_address",
                order_data={"foo": "string"},
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_fulfillments(self, async_client: AsyncDinari) -> None:
        order = await async_client.api.v2.accounts.orders.retrieve_fulfillments(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderRetrieveFulfillmentsResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_fulfillments(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.orders.with_raw_response.retrieve_fulfillments(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order = await response.parse()
        assert_matches_type(OrderRetrieveFulfillmentsResponse, order, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_fulfillments(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.orders.with_streaming_response.retrieve_fulfillments(
            order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order = await response.parse()
            assert_matches_type(OrderRetrieveFulfillmentsResponse, order, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_fulfillments(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.orders.with_raw_response.retrieve_fulfillments(
                order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `order_id` but received ''"):
            await async_client.api.v2.accounts.orders.with_raw_response.retrieve_fulfillments(
                order_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )
