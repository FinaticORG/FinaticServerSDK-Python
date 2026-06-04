from __future__ import annotations

import json
from typing import Any

import pytest

from src.FinaticServerCore import FinaticServer
from src.v1 import V1Client


class FakeResponse:
    status = 200

    def __init__(self, payload: dict[str, Any]) -> None:
        self.data = json.dumps(payload).encode("utf-8")
        self.headers = {"x-trace-id": "trace-1"}

    async def read(self) -> bytes:
        return self.data


class FakeApiClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def call_api(
        self,
        method: str,
        url: str,
        header_params: dict[str, str] | None = None,
        body: dict[str, Any] | None = None,
    ) -> FakeResponse:
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": header_params or {},
                "body": body,
            }
        )
        if url.endswith("/api/v1/sessions"):
            return FakeResponse(
                {
                    "success": {
                        "data": {
                            "session_id": "session-1",
                            "company_id": "company-1",
                        },
                        "meta": None,
                    },
                    "error": None,
                    "warning": None,
                }
            )
        return FakeResponse({"success": {"data": [], "meta": None}, "error": None})


def test_finatic_server_exposes_v1_facade_with_environment() -> None:
    sdk = FinaticServer(
        api_key="fntc_sandbox_key",
        sdk_config={"base_url": "https://api.test", "environment": "sandbox"},
    )

    assert isinstance(sdk.v1, V1Client)
    assert sdk.v1.environment == "sandbox"


@pytest.mark.asyncio
async def test_v1_create_session_sets_context_and_headers() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key",
        sdk_config={"base_url": "https://api.test", "environment": "live"},
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]

    response = await sdk.v1.create_session(device_info={"platform": "server"})

    assert response["data"]["session_id"] == "session-1"
    assert sdk.v1.session_id == "session-1"
    assert sdk.v1.company_id == "company-1"
    assert fake_api_client.calls[0]["method"] == "POST"
    assert fake_api_client.calls[0]["url"] == "https://api.test/api/v1/sessions"
    assert fake_api_client.calls[0]["headers"]["X-API-Key"] == "fntc_live_key"
    assert fake_api_client.calls[0]["headers"]["X-Finatic-Environment"] == "live"
    assert fake_api_client.calls[0]["body"] == {"device_info": {"platform": "server"}}


@pytest.mark.asyncio
async def test_v1_account_routes_use_session_environment_and_query() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key",
        sdk_config={"base_url": "https://api.test", "environment": "sandbox"},
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]
    sdk.v1.set_session_context("session-1", "company-1")

    await sdk.v1.list_account_transactions("account-1", limit=50, offset=10)

    call = fake_api_client.calls[0]
    assert call["method"] == "GET"
    assert (
        call["url"]
        == "https://api.test/api/v1/accounts/account-1/transactions?limit=50&offset=10"
    )
    assert call["headers"]["X-Session-ID"] == "session-1"
    assert call["headers"]["X-Company-ID"] == "company-1"
    assert call["headers"]["X-Finatic-Environment"] == "sandbox"


@pytest.mark.asyncio
async def test_v1_portal_flow_routes_match_account_first_api() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key",
        sdk_config={"base_url": "https://api.test", "environment": "live"},
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]
    sdk.v1.set_session_context("session-1", "company-1")

    await sdk.v1.link_portal_user("11111111-1111-1111-1111-111111111111")
    await sdk.v1.list_portal_institutions()
    await sdk.v1.create_portal_auth_attempt("alpaca")
    await sdk.v1.get_portal_auth_attempt("attempt-1")
    await sdk.v1.list_discovered_accounts()
    await sdk.v1.create_portal_account_grant(
        {
            "accountId": "22222222-2222-2222-2222-222222222222",
            "userBrokerConnectionId": "33333333-3333-3333-3333-333333333333",
            "userId": "11111111-1111-1111-1111-111111111111",
            "brokerId": "alpaca",
            "canRead": True,
            "canTrade": False,
            "dataClusters": ["accounts", "balances"],
        }
    )
    await sdk.v1.complete_portal_session()

    assert fake_api_client.calls[0]["method"] == "POST"
    assert (
        fake_api_client.calls[0]["url"]
        == "https://api.test/api/v1/portal/session-1/user-link"
    )
    assert fake_api_client.calls[0]["body"] == {
        "userId": "11111111-1111-1111-1111-111111111111"
    }
    assert (
        fake_api_client.calls[1]["url"]
        == "https://api.test/api/v1/portal/session-1/institutions"
    )
    assert (
        fake_api_client.calls[2]["url"]
        == "https://api.test/api/v1/portal/session-1/auth-attempts"
    )
    assert fake_api_client.calls[2]["body"] == {"brokerId": "alpaca"}
    assert (
        fake_api_client.calls[3]["url"]
        == "https://api.test/api/v1/portal/session-1/auth-attempts/attempt-1"
    )
    assert (
        fake_api_client.calls[4]["url"]
        == "https://api.test/api/v1/portal/session-1/discovered-accounts"
    )
    assert (
        fake_api_client.calls[5]["url"]
        == "https://api.test/api/v1/portal/session-1/account-grants"
    )
    assert fake_api_client.calls[5]["body"]["accountId"] == (
        "22222222-2222-2222-2222-222222222222"
    )
    assert (
        fake_api_client.calls[6]["url"]
        == "https://api.test/api/v1/portal/session-1/complete"
    )


@pytest.mark.asyncio
async def test_v1_webhook_catalog_uses_catalog_route() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key",
        sdk_config={"base_url": "https://api.test", "environment": "live"},
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]

    await sdk.v1.get_webhook_catalog()

    assert fake_api_client.calls[0]["method"] == "GET"
    assert fake_api_client.calls[0]["url"] == (
        "https://api.test/api/v1/webhooks/catalog"
    )


@pytest.mark.asyncio
async def test_v1_order_commands_send_idempotency_key() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]

    await sdk.v1.create_account_order(
        "account-1",
        {"symbol": "AAPL", "quantity": 1},
        idempotency_key="order-key-1",
    )

    call = fake_api_client.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == "https://api.test/api/v1/accounts/account-1/orders"
    assert call["headers"]["Idempotency-Key"] == "order-key-1"
    assert call["body"] == {"order": {"symbol": "AAPL", "quantity": 1}}


def test_v1_rejects_invalid_environment_and_resource() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")

    with pytest.raises(ValueError, match="environment"):
        sdk.v1.set_environment("paper")

    with pytest.raises(ValueError, match="Unsupported account resource"):
        sdk.v1._validate_resource("connections")


def test_v1_normalizes_success_envelope_trace_and_warning_alias() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")
    response = sdk.v1._deserialize_response(
        FakeResponse(
            {
                "success": {"data": {"syncStatus": "pending"}, "meta": None},
                "error": None,
                "warnings": [{"code": "SYNC_PENDING"}],
            }
        )
    )

    assert response["traceId"] == "trace-1"
    assert response["data"]["syncStatus"] == "pending"
    assert response["warnings"] == [{"code": "SYNC_PENDING"}]
    assert response["errors"] == []
    assert "success" not in response
    assert "warning" not in response


def test_v1_normalizes_error_envelope_with_stable_code() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")
    response = FakeResponse({"message": "missing accountId"})
    response.status = 422

    result = sdk.v1._deserialize_response(response)

    assert result["traceId"] == "trace-1"
    assert result["data"] is None
    assert result["warnings"] == []
    assert result["errors"][0]["category"] == "VALIDATION"
    assert result["errors"][0]["code"] == "VALIDATION"
    assert result["errors"][0]["status"] == 422


def test_v1_preserves_current_public_envelope_shape() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")
    response = sdk.v1._deserialize_response(
        FakeResponse(
            {
                "traceId": "trace-from-body",
                "data": {"syncStatus": "reauth_required"},
                "warnings": [],
                "errors": [],
            }
        )
    )

    assert response == {
        "traceId": "trace-from-body",
        "data": {"syncStatus": "reauth_required"},
        "warnings": [],
        "errors": [],
    }
