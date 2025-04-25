# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from dinari import Dinari, AsyncDinari
from tests.utils import assert_matches_type
from dinari.types.api.v2.market_data import (
    StockListResponse,
    StockRetrieveNewsResponse,
    StockRetrieveQuoteResponse,
    StockRetrieveDividendsResponse,
    StockRetrieveHistoricalPricesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStocks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Dinari) -> None:
        stock = client.api.v2.market_data.stocks.list()
        assert_matches_type(StockListResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Dinari) -> None:
        stock = client.api.v2.market_data.stocks.list(
            page=1,
            page_size=1,
            symbols=["string"],
        )
        assert_matches_type(StockListResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Dinari) -> None:
        response = client.api.v2.market_data.stocks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = response.parse()
        assert_matches_type(StockListResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Dinari) -> None:
        with client.api.v2.market_data.stocks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = response.parse()
            assert_matches_type(StockListResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_dividends(self, client: Dinari) -> None:
        stock = client.api.v2.market_data.stocks.retrieve_dividends(
            "stock_id",
        )
        assert_matches_type(StockRetrieveDividendsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_dividends(self, client: Dinari) -> None:
        response = client.api.v2.market_data.stocks.with_raw_response.retrieve_dividends(
            "stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = response.parse()
        assert_matches_type(StockRetrieveDividendsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_dividends(self, client: Dinari) -> None:
        with client.api.v2.market_data.stocks.with_streaming_response.retrieve_dividends(
            "stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = response.parse()
            assert_matches_type(StockRetrieveDividendsResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_dividends(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `stock_id` but received ''"):
            client.api.v2.market_data.stocks.with_raw_response.retrieve_dividends(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_historical_prices(self, client: Dinari) -> None:
        stock = client.api.v2.market_data.stocks.retrieve_historical_prices(
            stock_id="stock_id",
            timespan="DAY",
        )
        assert_matches_type(StockRetrieveHistoricalPricesResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_historical_prices(self, client: Dinari) -> None:
        response = client.api.v2.market_data.stocks.with_raw_response.retrieve_historical_prices(
            stock_id="stock_id",
            timespan="DAY",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = response.parse()
        assert_matches_type(StockRetrieveHistoricalPricesResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_historical_prices(self, client: Dinari) -> None:
        with client.api.v2.market_data.stocks.with_streaming_response.retrieve_historical_prices(
            stock_id="stock_id",
            timespan="DAY",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = response.parse()
            assert_matches_type(StockRetrieveHistoricalPricesResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_historical_prices(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `stock_id` but received ''"):
            client.api.v2.market_data.stocks.with_raw_response.retrieve_historical_prices(
                stock_id="",
                timespan="DAY",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_news(self, client: Dinari) -> None:
        stock = client.api.v2.market_data.stocks.retrieve_news(
            stock_id="stock_id",
        )
        assert_matches_type(StockRetrieveNewsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_news_with_all_params(self, client: Dinari) -> None:
        stock = client.api.v2.market_data.stocks.retrieve_news(
            stock_id="stock_id",
            limit=1,
        )
        assert_matches_type(StockRetrieveNewsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_news(self, client: Dinari) -> None:
        response = client.api.v2.market_data.stocks.with_raw_response.retrieve_news(
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = response.parse()
        assert_matches_type(StockRetrieveNewsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_news(self, client: Dinari) -> None:
        with client.api.v2.market_data.stocks.with_streaming_response.retrieve_news(
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = response.parse()
            assert_matches_type(StockRetrieveNewsResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_news(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `stock_id` but received ''"):
            client.api.v2.market_data.stocks.with_raw_response.retrieve_news(
                stock_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_quote(self, client: Dinari) -> None:
        stock = client.api.v2.market_data.stocks.retrieve_quote(
            "stock_id",
        )
        assert_matches_type(StockRetrieveQuoteResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_quote(self, client: Dinari) -> None:
        response = client.api.v2.market_data.stocks.with_raw_response.retrieve_quote(
            "stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = response.parse()
        assert_matches_type(StockRetrieveQuoteResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_quote(self, client: Dinari) -> None:
        with client.api.v2.market_data.stocks.with_streaming_response.retrieve_quote(
            "stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = response.parse()
            assert_matches_type(StockRetrieveQuoteResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_quote(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `stock_id` but received ''"):
            client.api.v2.market_data.stocks.with_raw_response.retrieve_quote(
                "",
            )


class TestAsyncStocks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncDinari) -> None:
        stock = await async_client.api.v2.market_data.stocks.list()
        assert_matches_type(StockListResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncDinari) -> None:
        stock = await async_client.api.v2.market_data.stocks.list(
            page=1,
            page_size=1,
            symbols=["string"],
        )
        assert_matches_type(StockListResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.market_data.stocks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = await response.parse()
        assert_matches_type(StockListResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.market_data.stocks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = await response.parse()
            assert_matches_type(StockListResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_dividends(self, async_client: AsyncDinari) -> None:
        stock = await async_client.api.v2.market_data.stocks.retrieve_dividends(
            "stock_id",
        )
        assert_matches_type(StockRetrieveDividendsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_dividends(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.market_data.stocks.with_raw_response.retrieve_dividends(
            "stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = await response.parse()
        assert_matches_type(StockRetrieveDividendsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_dividends(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.market_data.stocks.with_streaming_response.retrieve_dividends(
            "stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = await response.parse()
            assert_matches_type(StockRetrieveDividendsResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_dividends(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `stock_id` but received ''"):
            await async_client.api.v2.market_data.stocks.with_raw_response.retrieve_dividends(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_historical_prices(self, async_client: AsyncDinari) -> None:
        stock = await async_client.api.v2.market_data.stocks.retrieve_historical_prices(
            stock_id="stock_id",
            timespan="DAY",
        )
        assert_matches_type(StockRetrieveHistoricalPricesResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_historical_prices(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.market_data.stocks.with_raw_response.retrieve_historical_prices(
            stock_id="stock_id",
            timespan="DAY",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = await response.parse()
        assert_matches_type(StockRetrieveHistoricalPricesResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_historical_prices(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.market_data.stocks.with_streaming_response.retrieve_historical_prices(
            stock_id="stock_id",
            timespan="DAY",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = await response.parse()
            assert_matches_type(StockRetrieveHistoricalPricesResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_historical_prices(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `stock_id` but received ''"):
            await async_client.api.v2.market_data.stocks.with_raw_response.retrieve_historical_prices(
                stock_id="",
                timespan="DAY",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_news(self, async_client: AsyncDinari) -> None:
        stock = await async_client.api.v2.market_data.stocks.retrieve_news(
            stock_id="stock_id",
        )
        assert_matches_type(StockRetrieveNewsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_news_with_all_params(self, async_client: AsyncDinari) -> None:
        stock = await async_client.api.v2.market_data.stocks.retrieve_news(
            stock_id="stock_id",
            limit=1,
        )
        assert_matches_type(StockRetrieveNewsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_news(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.market_data.stocks.with_raw_response.retrieve_news(
            stock_id="stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = await response.parse()
        assert_matches_type(StockRetrieveNewsResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_news(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.market_data.stocks.with_streaming_response.retrieve_news(
            stock_id="stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = await response.parse()
            assert_matches_type(StockRetrieveNewsResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_news(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `stock_id` but received ''"):
            await async_client.api.v2.market_data.stocks.with_raw_response.retrieve_news(
                stock_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_quote(self, async_client: AsyncDinari) -> None:
        stock = await async_client.api.v2.market_data.stocks.retrieve_quote(
            "stock_id",
        )
        assert_matches_type(StockRetrieveQuoteResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_quote(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.market_data.stocks.with_raw_response.retrieve_quote(
            "stock_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stock = await response.parse()
        assert_matches_type(StockRetrieveQuoteResponse, stock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_quote(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.market_data.stocks.with_streaming_response.retrieve_quote(
            "stock_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stock = await response.parse()
            assert_matches_type(StockRetrieveQuoteResponse, stock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_quote(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `stock_id` but received ''"):
            await async_client.api.v2.market_data.stocks.with_raw_response.retrieve_quote(
                "",
            )
