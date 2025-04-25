# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from dinari import Dinari, AsyncDinari
from tests.utils import assert_matches_type
from dinari.types.api.v2 import (
    AccountRetrieveCashResponse,
    AccountRetrievePortfolioResponse,
    AccountRetrieveDividendPaymentsResponse,
    AccountRetrieveInterestPaymentsResponse,
)
from dinari.types.api.v2.entities import Account

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAccounts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Dinari) -> None:
        account = client.api.v2.accounts.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Account, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Dinari) -> None:
        response = client.api.v2.accounts.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(Account, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Dinari) -> None:
        with client.api.v2.accounts.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(Account, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_deactivate(self, client: Dinari) -> None:
        account = client.api.v2.accounts.deactivate(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Account, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_deactivate(self, client: Dinari) -> None:
        response = client.api.v2.accounts.with_raw_response.deactivate(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(Account, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_deactivate(self, client: Dinari) -> None:
        with client.api.v2.accounts.with_streaming_response.deactivate(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(Account, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_deactivate(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.with_raw_response.deactivate(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_cash(self, client: Dinari) -> None:
        account = client.api.v2.accounts.retrieve_cash(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AccountRetrieveCashResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_cash(self, client: Dinari) -> None:
        response = client.api.v2.accounts.with_raw_response.retrieve_cash(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountRetrieveCashResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_cash(self, client: Dinari) -> None:
        with client.api.v2.accounts.with_streaming_response.retrieve_cash(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountRetrieveCashResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_cash(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.with_raw_response.retrieve_cash(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_dividend_payments(self, client: Dinari) -> None:
        account = client.api.v2.accounts.retrieve_dividend_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AccountRetrieveDividendPaymentsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_dividend_payments(self, client: Dinari) -> None:
        response = client.api.v2.accounts.with_raw_response.retrieve_dividend_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountRetrieveDividendPaymentsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_dividend_payments(self, client: Dinari) -> None:
        with client.api.v2.accounts.with_streaming_response.retrieve_dividend_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountRetrieveDividendPaymentsResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_dividend_payments(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.with_raw_response.retrieve_dividend_payments(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_interest_payments(self, client: Dinari) -> None:
        account = client.api.v2.accounts.retrieve_interest_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AccountRetrieveInterestPaymentsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_interest_payments(self, client: Dinari) -> None:
        response = client.api.v2.accounts.with_raw_response.retrieve_interest_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountRetrieveInterestPaymentsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_interest_payments(self, client: Dinari) -> None:
        with client.api.v2.accounts.with_streaming_response.retrieve_interest_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountRetrieveInterestPaymentsResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_interest_payments(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.with_raw_response.retrieve_interest_payments(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_portfolio(self, client: Dinari) -> None:
        account = client.api.v2.accounts.retrieve_portfolio(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AccountRetrievePortfolioResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_portfolio(self, client: Dinari) -> None:
        response = client.api.v2.accounts.with_raw_response.retrieve_portfolio(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = response.parse()
        assert_matches_type(AccountRetrievePortfolioResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_portfolio(self, client: Dinari) -> None:
        with client.api.v2.accounts.with_streaming_response.retrieve_portfolio(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = response.parse()
            assert_matches_type(AccountRetrievePortfolioResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_portfolio(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            client.api.v2.accounts.with_raw_response.retrieve_portfolio(
                "",
            )


class TestAsyncAccounts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncDinari) -> None:
        account = await async_client.api.v2.accounts.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Account, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(Account, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(Account, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_deactivate(self, async_client: AsyncDinari) -> None:
        account = await async_client.api.v2.accounts.deactivate(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(Account, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_deactivate(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.with_raw_response.deactivate(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(Account, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_deactivate(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.with_streaming_response.deactivate(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(Account, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_deactivate(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.with_raw_response.deactivate(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_cash(self, async_client: AsyncDinari) -> None:
        account = await async_client.api.v2.accounts.retrieve_cash(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AccountRetrieveCashResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_cash(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.with_raw_response.retrieve_cash(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountRetrieveCashResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_cash(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.with_streaming_response.retrieve_cash(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountRetrieveCashResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_cash(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.with_raw_response.retrieve_cash(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_dividend_payments(self, async_client: AsyncDinari) -> None:
        account = await async_client.api.v2.accounts.retrieve_dividend_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AccountRetrieveDividendPaymentsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_dividend_payments(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.with_raw_response.retrieve_dividend_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountRetrieveDividendPaymentsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_dividend_payments(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.with_streaming_response.retrieve_dividend_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountRetrieveDividendPaymentsResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_dividend_payments(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.with_raw_response.retrieve_dividend_payments(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_interest_payments(self, async_client: AsyncDinari) -> None:
        account = await async_client.api.v2.accounts.retrieve_interest_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AccountRetrieveInterestPaymentsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_interest_payments(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.with_raw_response.retrieve_interest_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountRetrieveInterestPaymentsResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_interest_payments(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.with_streaming_response.retrieve_interest_payments(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountRetrieveInterestPaymentsResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_interest_payments(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.with_raw_response.retrieve_interest_payments(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_portfolio(self, async_client: AsyncDinari) -> None:
        account = await async_client.api.v2.accounts.retrieve_portfolio(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AccountRetrievePortfolioResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_portfolio(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.accounts.with_raw_response.retrieve_portfolio(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        account = await response.parse()
        assert_matches_type(AccountRetrievePortfolioResponse, account, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_portfolio(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.accounts.with_streaming_response.retrieve_portfolio(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            account = await response.parse()
            assert_matches_type(AccountRetrievePortfolioResponse, account, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_portfolio(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `account_id` but received ''"):
            await async_client.api.v2.accounts.with_raw_response.retrieve_portfolio(
                "",
            )
