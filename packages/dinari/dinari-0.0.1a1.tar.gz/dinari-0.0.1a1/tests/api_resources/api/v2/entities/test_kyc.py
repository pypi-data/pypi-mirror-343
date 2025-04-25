# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from dinari import Dinari, AsyncDinari
from tests.utils import assert_matches_type
from dinari._utils import parse_date
from dinari.types.api.v2.entities import (
    KYCInfo,
    KYCGetURLResponse,
    KYCUploadDocumentResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestKYC:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Dinari) -> None:
        kyc = client.api.v2.entities.kyc.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Dinari) -> None:
        response = client.api.v2.entities.kyc.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kyc = response.parse()
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Dinari) -> None:
        with client.api.v2.entities.kyc.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kyc = response.parse()
            assert_matches_type(KYCInfo, kyc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entity_id` but received ''"):
            client.api.v2.entities.kyc.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_url(self, client: Dinari) -> None:
        kyc = client.api.v2.entities.kyc.get_url(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(KYCGetURLResponse, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_url(self, client: Dinari) -> None:
        response = client.api.v2.entities.kyc.with_raw_response.get_url(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kyc = response.parse()
        assert_matches_type(KYCGetURLResponse, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_url(self, client: Dinari) -> None:
        with client.api.v2.entities.kyc.with_streaming_response.get_url(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kyc = response.parse()
            assert_matches_type(KYCGetURLResponse, kyc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_url(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entity_id` but received ''"):
            client.api.v2.entities.kyc.with_raw_response.get_url(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_submit(self, client: Dinari) -> None:
        kyc = client.api.v2.entities.kyc.submit(
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "country_code": "SG",
                "last_name": "Doe",
            },
            provider_name="provider_name",
        )
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_submit_with_all_params(self, client: Dinari) -> None:
        kyc = client.api.v2.entities.kyc.submit(
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "country_code": "SG",
                "last_name": "Doe",
                "address_city": "San Francisco",
                "address_postal_code": "94111",
                "address_street_1": "123 Main St.",
                "address_street_2": "Apt. 123",
                "address_subdivision": "California",
                "birth_date": parse_date("2019-12-27"),
                "email": "johndoe@website.com",
                "first_name": "John",
                "middle_name": "middle_name",
                "tax_id_number": "123456789",
            },
            provider_name="provider_name",
        )
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_submit(self, client: Dinari) -> None:
        response = client.api.v2.entities.kyc.with_raw_response.submit(
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "country_code": "SG",
                "last_name": "Doe",
            },
            provider_name="provider_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kyc = response.parse()
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_submit(self, client: Dinari) -> None:
        with client.api.v2.entities.kyc.with_streaming_response.submit(
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "country_code": "SG",
                "last_name": "Doe",
            },
            provider_name="provider_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kyc = response.parse()
            assert_matches_type(KYCInfo, kyc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_submit(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entity_id` but received ''"):
            client.api.v2.entities.kyc.with_raw_response.submit(
                entity_id="",
                data={
                    "country_code": "SG",
                    "last_name": "Doe",
                },
                provider_name="provider_name",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_upload_document(self, client: Dinari) -> None:
        kyc = client.api.v2.entities.kyc.upload_document(
            kyc_id="kyc_id",
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            document_type="GOVERNMENT_ID",
        )
        assert_matches_type(KYCUploadDocumentResponse, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_upload_document(self, client: Dinari) -> None:
        response = client.api.v2.entities.kyc.with_raw_response.upload_document(
            kyc_id="kyc_id",
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            document_type="GOVERNMENT_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kyc = response.parse()
        assert_matches_type(KYCUploadDocumentResponse, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_upload_document(self, client: Dinari) -> None:
        with client.api.v2.entities.kyc.with_streaming_response.upload_document(
            kyc_id="kyc_id",
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            document_type="GOVERNMENT_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kyc = response.parse()
            assert_matches_type(KYCUploadDocumentResponse, kyc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_upload_document(self, client: Dinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entity_id` but received ''"):
            client.api.v2.entities.kyc.with_raw_response.upload_document(
                kyc_id="kyc_id",
                entity_id="",
                document_type="GOVERNMENT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kyc_id` but received ''"):
            client.api.v2.entities.kyc.with_raw_response.upload_document(
                kyc_id="",
                entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                document_type="GOVERNMENT_ID",
            )


class TestAsyncKYC:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncDinari) -> None:
        kyc = await async_client.api.v2.entities.kyc.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.entities.kyc.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kyc = await response.parse()
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.entities.kyc.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kyc = await response.parse()
            assert_matches_type(KYCInfo, kyc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entity_id` but received ''"):
            await async_client.api.v2.entities.kyc.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_url(self, async_client: AsyncDinari) -> None:
        kyc = await async_client.api.v2.entities.kyc.get_url(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(KYCGetURLResponse, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_url(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.entities.kyc.with_raw_response.get_url(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kyc = await response.parse()
        assert_matches_type(KYCGetURLResponse, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_url(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.entities.kyc.with_streaming_response.get_url(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kyc = await response.parse()
            assert_matches_type(KYCGetURLResponse, kyc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_url(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entity_id` but received ''"):
            await async_client.api.v2.entities.kyc.with_raw_response.get_url(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_submit(self, async_client: AsyncDinari) -> None:
        kyc = await async_client.api.v2.entities.kyc.submit(
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "country_code": "SG",
                "last_name": "Doe",
            },
            provider_name="provider_name",
        )
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_submit_with_all_params(self, async_client: AsyncDinari) -> None:
        kyc = await async_client.api.v2.entities.kyc.submit(
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "country_code": "SG",
                "last_name": "Doe",
                "address_city": "San Francisco",
                "address_postal_code": "94111",
                "address_street_1": "123 Main St.",
                "address_street_2": "Apt. 123",
                "address_subdivision": "California",
                "birth_date": parse_date("2019-12-27"),
                "email": "johndoe@website.com",
                "first_name": "John",
                "middle_name": "middle_name",
                "tax_id_number": "123456789",
            },
            provider_name="provider_name",
        )
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_submit(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.entities.kyc.with_raw_response.submit(
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "country_code": "SG",
                "last_name": "Doe",
            },
            provider_name="provider_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kyc = await response.parse()
        assert_matches_type(KYCInfo, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_submit(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.entities.kyc.with_streaming_response.submit(
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "country_code": "SG",
                "last_name": "Doe",
            },
            provider_name="provider_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kyc = await response.parse()
            assert_matches_type(KYCInfo, kyc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_submit(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entity_id` but received ''"):
            await async_client.api.v2.entities.kyc.with_raw_response.submit(
                entity_id="",
                data={
                    "country_code": "SG",
                    "last_name": "Doe",
                },
                provider_name="provider_name",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_upload_document(self, async_client: AsyncDinari) -> None:
        kyc = await async_client.api.v2.entities.kyc.upload_document(
            kyc_id="kyc_id",
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            document_type="GOVERNMENT_ID",
        )
        assert_matches_type(KYCUploadDocumentResponse, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_upload_document(self, async_client: AsyncDinari) -> None:
        response = await async_client.api.v2.entities.kyc.with_raw_response.upload_document(
            kyc_id="kyc_id",
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            document_type="GOVERNMENT_ID",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        kyc = await response.parse()
        assert_matches_type(KYCUploadDocumentResponse, kyc, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_upload_document(self, async_client: AsyncDinari) -> None:
        async with async_client.api.v2.entities.kyc.with_streaming_response.upload_document(
            kyc_id="kyc_id",
            entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            document_type="GOVERNMENT_ID",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            kyc = await response.parse()
            assert_matches_type(KYCUploadDocumentResponse, kyc, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_upload_document(self, async_client: AsyncDinari) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `entity_id` but received ''"):
            await async_client.api.v2.entities.kyc.with_raw_response.upload_document(
                kyc_id="kyc_id",
                entity_id="",
                document_type="GOVERNMENT_ID",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `kyc_id` but received ''"):
            await async_client.api.v2.entities.kyc.with_raw_response.upload_document(
                kyc_id="",
                entity_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                document_type="GOVERNMENT_ID",
            )
