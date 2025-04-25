# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from dinari import Dinari, AsyncDinari
from tests.utils import assert_matches_type
from dinari.types.api.v2.accounts import (
    OrderRequest,
    OrderRequestListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOrderRequests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Dinari) -> None:
        order_request = client.api.v2.accounts.order_requests.retrieve(
            request_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Dinari) -> None:
        response = client.api.v2.accounts.order_requests.with_raw_response.retrieve(
            request_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Dinari) -> None:
        with client.api.v2.accounts.order_requests.with_streaming_response.retrieve(
            request_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.order_requests.with_raw_response.retrieve(
                request_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `request_id` but received ''"):
            client.api.v2.accounts.order_requests.with_raw_response.retrieve(
                request_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Dinari) -> None:
        order_request = client.api.v2.accounts.order_requests.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderRequestListResponse, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Dinari) -> None:
        response = client.api.v2.accounts.order_requests.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = response.parse()
        assert_matches_type(OrderRequestListResponse, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Dinari) -> None:
        with client.api.v2.accounts.order_requests.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = response.parse()
            assert_matches_type(OrderRequestListResponse, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.order_requests.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_limit_buy(self, client: Dinari) -> None:
        order_request = client.api.v2.accounts.order_requests.create_limit_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_limit_buy(self, client: Dinari) -> None:
        response = client.api.v2.accounts.order_requests.with_raw_response.create_limit_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_limit_buy(self, client: Dinari) -> None:
        with client.api.v2.accounts.order_requests.with_streaming_response.create_limit_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_limit_buy(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.order_requests.with_raw_response.create_limit_buy(
                account_id="",
                asset_quantity=0,
                limit_price=0,
                stock_id="stock_id",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_limit_sell(self, client: Dinari) -> None:
        order_request = client.api.v2.accounts.order_requests.create_limit_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_limit_sell(self, client: Dinari) -> None:
        response = client.api.v2.accounts.order_requests.with_raw_response.create_limit_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_limit_sell(self, client: Dinari) -> None:
        with client.api.v2.accounts.order_requests.with_streaming_response.create_limit_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_limit_sell(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.order_requests.with_raw_response.create_limit_sell(
                account_id="",
                asset_quantity=0,
                limit_price=0,
                stock_id="stock_id",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_market_buy(self, client: Dinari) -> None:
        order_request = client.api.v2.accounts.order_requests.create_market_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            payment_amount=0,
            stock_id="stock_id",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_market_buy_with_all_params(self, client: Dinari) -> None:
        order_request = client.api.v2.accounts.order_requests.create_market_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            payment_amount=0,
            stock_id="stock_id",
            include_fees=True,
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_market_buy(self, client: Dinari) -> None:
        response = client.api.v2.accounts.order_requests.with_raw_response.create_market_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            payment_amount=0,
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_market_buy(self, client: Dinari) -> None:
        with client.api.v2.accounts.order_requests.with_streaming_response.create_market_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            payment_amount=0,
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_market_buy(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.order_requests.with_raw_response.create_market_buy(
                account_id="",
                payment_amount=0,
                stock_id="stock_id",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_market_sell(self, client: Dinari) -> None:
        order_request = client.api.v2.accounts.order_requests.create_market_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            stock_id="stock_id",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_market_sell(self, client: Dinari) -> None:
        response = client.api.v2.accounts.order_requests.with_raw_response.create_market_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_market_sell(self, client: Dinari) -> None:
        with client.api.v2.accounts.order_requests.with_streaming_response.create_market_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_market_sell(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.order_requests.with_raw_response.create_market_sell(
                account_id="",
                asset_quantity=0,
                stock_id="stock_id",
            )


class TestAsyncOrderRequests:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncDinari) -> None:
        order_request = await async_client.api.v2.accounts.order_requests.retrieve(
            request_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.order_requests.with_raw_response.retrieve(
            request_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = await response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.order_requests.with_streaming_response.retrieve(
            request_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = await response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.order_requests.with_raw_response.retrieve(
                request_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                account_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `request_id` but received ''"):
            await async_client.api.v2.accounts.order_requests.with_raw_response.retrieve(
                request_id="",
                account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncDinari) -> None:
        order_request = await async_client.api.v2.accounts.order_requests.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(OrderRequestListResponse, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.order_requests.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = await response.parse()
        assert_matches_type(OrderRequestListResponse, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.order_requests.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = await response.parse()
            assert_matches_type(OrderRequestListResponse, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.order_requests.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_limit_buy(self, async_client: AsyncDinari) -> None:
        order_request = await async_client.api.v2.accounts.order_requests.create_limit_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_limit_buy(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.order_requests.with_raw_response.create_limit_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = await response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_limit_buy(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.order_requests.with_streaming_response.create_limit_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = await response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_limit_buy(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.order_requests.with_raw_response.create_limit_buy(
                account_id="",
                asset_quantity=0,
                limit_price=0,
                stock_id="stock_id",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_limit_sell(self, async_client: AsyncDinari) -> None:
        order_request = await async_client.api.v2.accounts.order_requests.create_limit_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_limit_sell(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.order_requests.with_raw_response.create_limit_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = await response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_limit_sell(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.order_requests.with_streaming_response.create_limit_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            limit_price=0,
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = await response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_limit_sell(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.order_requests.with_raw_response.create_limit_sell(
                account_id="",
                asset_quantity=0,
                limit_price=0,
                stock_id="stock_id",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_market_buy(self, async_client: AsyncDinari) -> None:
        order_request = await async_client.api.v2.accounts.order_requests.create_market_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            payment_amount=0,
            stock_id="stock_id",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_market_buy_with_all_params(self, async_client: AsyncDinari) -> None:
        order_request = await async_client.api.v2.accounts.order_requests.create_market_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            payment_amount=0,
            stock_id="stock_id",
            include_fees=True,
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_market_buy(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.order_requests.with_raw_response.create_market_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            payment_amount=0,
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = await response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_market_buy(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.order_requests.with_streaming_response.create_market_buy(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            payment_amount=0,
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = await response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_market_buy(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.order_requests.with_raw_response.create_market_buy(
                account_id="",
                payment_amount=0,
                stock_id="stock_id",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_market_sell(self, async_client: AsyncDinari) -> None:
        order_request = await async_client.api.v2.accounts.order_requests.create_market_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            stock_id="stock_id",
        )
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_market_sell(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.order_requests.with_raw_response.create_market_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        order_request = await response.parse()
        assert_matches_type(OrderRequest, order_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_market_sell(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.order_requests.with_streaming_response.create_market_sell(
            account_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            asset_quantity=0,
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            order_request = await response.parse()
            assert_matches_type(OrderRequest, order_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_market_sell(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.order_requests.with_raw_response.create_market_sell(
                account_id="",
                asset_quantity=0,
                stock_id="stock_id",
            )
