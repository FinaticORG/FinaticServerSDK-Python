from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from src.FinaticServerCore import FinaticServer
from src.v1 import V1Client


class FakeResponse:
    status = 200

    def __init__(self, payload: dict[str, Any]) -> None:
        self.data = json.dumps(payload).encode("utf-8")
        self.headers = {"x-trace-id": "trace-1"}

    def read(self) -> bytes:
        return self.data


class FakeGeneratedResponse:
    status = 200
    data = b'{"data": {"ok": true}, "warnings": [], "errors": []}'

    def getheaders(self) -> dict[str, str]:
        return {"x-trace-id": "trace-from-generated-response"}


class FakeApiClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def call_api(
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


V1_OPENAPI_OPERATION_METHODS = {
    ("GET", "/api/v1/account-grants"): "list_account_grants",
    ("GET", "/api/v1/account-grants/{grantId}"): "get_account_grant",
    ("PATCH", "/api/v1/account-grants/{grantId}"): "update_account_grant",
    ("POST", "/api/v1/account-grants/{grantId}/revoke"): "revoke_account_grant",
    ("GET", "/api/v1/accounts"): "list_accounts",
    ("GET", "/api/v1/accounts/{accountId}"): "get_account",
    ("GET", "/api/v1/accounts/{accountId}/balances"): "list_account_balances",
    ("GET", "/api/v1/accounts/{accountId}/orders"): "list_account_orders",
    ("POST", "/api/v1/accounts/{accountId}/orders"): "create_account_order",
    (
        "DELETE",
        "/api/v1/accounts/{accountId}/orders/{orderId}",
    ): "cancel_account_order",
    ("GET", "/api/v1/accounts/{accountId}/orders/{orderId}"): "get_account_order",
    (
        "PATCH",
        "/api/v1/accounts/{accountId}/orders/{orderId}",
    ): "modify_account_order",
    (
        "GET",
        "/api/v1/accounts/{accountId}/orders/{orderId}/events",
    ): "get_account_order_events",
    (
        "GET",
        "/api/v1/accounts/{accountId}/orders/{orderId}/fills",
    ): "get_account_order_fills",
    (
        "GET",
        "/api/v1/accounts/{accountId}/position-lots",
    ): "list_account_position_lots",
    (
        "GET",
        "/api/v1/accounts/{accountId}/position-lots/{lotId}/fills",
    ): "get_account_position_lot_fills",
    ("GET", "/api/v1/accounts/{accountId}/positions"): "list_account_positions",
    (
        "GET",
        "/api/v1/accounts/{accountId}/transactions",
    ): "list_account_transactions",
    ("GET", "/api/v1/accounts/{accountId}/{resource}"): "list_account_resource",
    ("GET", "/api/v1/consents"): "list_consents",
    ("POST", "/api/v1/consents"): "create_consent",
    ("GET", "/api/v1/consents/{consentId}"): "get_consent",
    ("POST", "/api/v1/consents/{consentId}/revoke"): "revoke_consent",
    ("GET", "/api/v1/portal/oauth/completion/{token}"): ("get_portal_oauth_completion"),
    ("POST", "/api/v1/portal/{sessionId}/account-grants"): (
        "create_portal_account_grant"
    ),
    ("POST", "/api/v1/portal/{sessionId}/auth-attempts"): (
        "create_portal_auth_attempt"
    ),
    ("GET", "/api/v1/portal/{sessionId}/auth-attempts/{authAttemptId}"): (
        "get_portal_auth_attempt"
    ),
    ("POST", "/api/v1/portal/{sessionId}/complete"): "complete_portal_session",
    ("GET", "/api/v1/portal/{sessionId}/discovered-accounts"): (
        "list_discovered_accounts"
    ),
    ("GET", "/api/v1/portal/{sessionId}/institutions"): ("list_portal_institutions"),
    ("POST", "/api/v1/portal/{sessionId}/user-link"): "link_portal_user",
    ("GET", "/api/v1/portal/{token}"): "get_portal",
    ("POST", "/api/v1/sessions"): "create_session",
    ("GET", "/api/v1/sessions/{sessionId}"): "get_session",
    ("POST", "/api/v1/sessions/{sessionId}/portal-links"): "create_portal_link",
    ("GET", "/api/v1/sessions/{sessionId}/sync-status"): ("get_session_sync_status"),
    ("GET", "/api/v1/sessions/{sessionId}/user"): "get_session_user",
    ("GET", "/api/v1/webhooks/catalog"): "get_webhook_catalog",
    ("GET", "/api/v1/webhooks/payload-schema"): "get_webhook_payload_schema",
    ("GET", "/api/v1/webhooks/subscriptions"): "list_webhook_subscriptions",
    ("POST", "/api/v1/webhooks/subscriptions"): "create_webhook_subscription",
    ("PATCH", "/api/v1/webhooks/subscriptions/{subscriptionId}"): (
        "update_webhook_subscription"
    ),
    ("POST", "/api/v1/webhooks/subscriptions/{subscriptionId}/revoke"): (
        "revoke_webhook_subscription"
    ),
}


def _v1_openapi_operations() -> set[tuple[str, str]]:
    artifact_path = (
        Path(__file__).resolve().parents[2]
        / "artifacts"
        / "openapi"
        / "finaticapi-v1.json"
    )
    schema = json.loads(artifact_path.read_text(encoding="utf-8"))
    operations: set[tuple[str, str]] = set()
    for path, path_item in schema["paths"].items():
        if not path.startswith("/api/v1/"):
            continue
        for method, operation in path_item.items():
            if not isinstance(operation, dict):
                continue
            audiences = set(operation.get("x-sdk-audiences") or [])
            if audiences.intersection({"sdk", "portal"}):
                operations.add((method.upper(), path))
    return operations


def test_v1_facade_covers_openapi_sdk_and_portal_audience_operations() -> None:
    openapi_operations = _v1_openapi_operations()

    assert len(openapi_operations) == len(V1_OPENAPI_OPERATION_METHODS)
    assert set(V1_OPENAPI_OPERATION_METHODS) == openapi_operations

    for method_name in V1_OPENAPI_OPERATION_METHODS.values():
        assert hasattr(V1Client, method_name)


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
    assert fake_api_client.calls[0]["body"] == {"deviceInfo": {"platform": "server"}}


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
    await sdk.v1.get_portal("portal-token-1")
    await sdk.v1.get_portal_oauth_completion("portal-token-1")
    await sdk.v1.list_portal_institutions()
    await sdk.v1.create_portal_auth_attempt("alpaca")
    await sdk.v1.get_portal_auth_attempt("attempt-1")
    await sdk.v1.list_discovered_accounts(
        auth_attempt_id="attempt-1", include_sync_status=True
    )
    await sdk.v1.create_portal_account_grant(
        {
            "accountId": "22222222-2222-2222-2222-222222222222",
            "authAttemptId": "44444444-4444-4444-4444-444444444444",
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
        == "https://api.test/api/v1/portal/portal-token-1"
    )
    assert (
        fake_api_client.calls[2]["url"]
        == "https://api.test/api/v1/portal/oauth/completion/portal-token-1"
    )
    assert (
        fake_api_client.calls[3]["url"]
        == "https://api.test/api/v1/portal/session-1/institutions"
    )
    assert (
        fake_api_client.calls[4]["url"]
        == "https://api.test/api/v1/portal/session-1/auth-attempts"
    )
    assert fake_api_client.calls[4]["body"] == {"brokerId": "alpaca"}
    assert (
        fake_api_client.calls[5]["url"]
        == "https://api.test/api/v1/portal/session-1/auth-attempts/attempt-1"
    )
    assert (
        fake_api_client.calls[6]["url"]
        == "https://api.test/api/v1/portal/session-1/discovered-accounts?authAttemptId=attempt-1&includeSyncStatus=True"
    )
    assert (
        fake_api_client.calls[7]["url"]
        == "https://api.test/api/v1/portal/session-1/account-grants"
    )
    assert fake_api_client.calls[7]["body"]["accountId"] == (
        "22222222-2222-2222-2222-222222222222"
    )
    assert fake_api_client.calls[7]["body"]["authAttemptId"] == (
        "44444444-4444-4444-4444-444444444444"
    )
    assert "userBrokerConnectionId" not in fake_api_client.calls[7]["body"]
    assert "brokerId" not in fake_api_client.calls[7]["body"]
    assert (
        fake_api_client.calls[8]["url"]
        == "https://api.test/api/v1/portal/session-1/complete"
    )


@pytest.mark.asyncio
async def test_v1_session_compatibility_routes_match_sdk_openapi() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key",
        sdk_config={"base_url": "https://api.test", "environment": "live"},
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]
    sdk.v1.set_session_context("session-1", "company-1")

    await sdk.v1.init_legacy_session()
    await sdk.v1.start_legacy_session("ott-1", user_id="user-1")
    await sdk.v1.link_session_user(
        "user-1", email="user@example.com", link_context_id="link-context-1"
    )
    await sdk.v1.link_mcp_session_user("user-1", "mcp-link-context-1")
    await sdk.v1.get_legacy_portal_url()
    await sdk.v1.get_legacy_session_user()
    await sdk.v1.get_session_sync_status()

    assert fake_api_client.calls[0]["method"] == "POST"
    assert fake_api_client.calls[0]["url"] == "https://api.test/api/v1/session/init"
    assert fake_api_client.calls[1]["method"] == "POST"
    assert fake_api_client.calls[1]["url"] == "https://api.test/api/v1/session/start"
    assert fake_api_client.calls[1]["headers"]["One-Time-Token"] == "ott-1"
    assert fake_api_client.calls[1]["body"] == {"user_id": "user-1"}
    assert (
        fake_api_client.calls[2]["url"]
        == "https://api.test/api/v1/session/link-user?session_id=session-1"
    )
    assert fake_api_client.calls[2]["body"] == {
        "user_id": "user-1",
        "email": "user@example.com",
        "link_context_id": "link-context-1",
    }
    assert (
        fake_api_client.calls[3]["url"]
        == "https://api.test/api/v1/session/mcp/link-user"
    )
    assert fake_api_client.calls[3]["body"] == {
        "user_id": "user-1",
        "link_context_id": "mcp-link-context-1",
    }
    assert fake_api_client.calls[4]["url"] == "https://api.test/api/v1/session/portal"
    assert fake_api_client.calls[4]["headers"]["session-id"] == "session-1"
    assert (
        fake_api_client.calls[5]["url"]
        == "https://api.test/api/v1/session/session-1/user"
    )
    assert (
        fake_api_client.calls[6]["url"]
        == "https://api.test/api/v1/sessions/session-1/sync-status"
    )


@pytest.mark.asyncio
async def test_v1_company_and_fdx_alias_routes_match_sdk_openapi() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key",
        sdk_config={"base_url": "https://api.test", "environment": "sandbox"},
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]
    sdk.v1.set_session_context("session-1", "company-1")

    await sdk.v1.get_company("company-1")
    await sdk.v1.list_fdx_balances(account_id="account-1", limit=25, offset=5)
    await sdk.v1.list_fdx_accounts(broker_id="alpaca", include_metadata=True)

    assert fake_api_client.calls[0]["method"] == "GET"
    assert (
        fake_api_client.calls[0]["url"] == "https://api.test/api/v1/company/company-1"
    )
    assert fake_api_client.calls[0]["headers"]["X-Finatic-Environment"] == "sandbox"
    assert fake_api_client.calls[1]["url"] == (
        "https://api.test/api/v1/brokers/data/balances?"
        "account_id=account-1&limit=25&offset=5"
    )
    assert fake_api_client.calls[2]["url"] == (
        "https://api.test/api/v1/brokers/data/accounts?"
        "broker_id=alpaca&include_metadata=True"
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


@pytest.mark.asyncio
async def test_v1_cancel_account_order_sends_no_body() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]

    await sdk.v1.cancel_account_order(
        "account-1",
        "order-1",
        idempotency_key="cancel-key-1",
    )

    call = fake_api_client.calls[0]
    assert call["method"] == "DELETE"
    assert call["url"] == "https://api.test/api/v1/accounts/account-1/orders/order-1"
    assert call["headers"]["Idempotency-Key"] == "cancel-key-1"
    assert call["body"] is None


@pytest.mark.asyncio
async def test_v1_order_commands_require_idempotency_key() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )

    with pytest.raises(ValueError, match="idempotency_key is required"):
        await sdk.v1.create_account_order(
            "account-1", {"symbol": "AAPL", "quantity": 1}, idempotency_key=""
        )


@pytest.mark.asyncio
async def test_v1_create_consent_uses_openapi_route() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]

    await sdk.v1.create_consent({"grantId": "grant-1", "scopes": ["balances"]})

    call = fake_api_client.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == "https://api.test/api/v1/consents"
    assert call["body"] == {"grantId": "grant-1", "scopes": ["balances"]}


def test_v1_rejects_invalid_environment_and_resource() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")

    with pytest.raises(ValueError, match="environment"):
        sdk.v1.set_environment("paper")

    with pytest.raises(ValueError, match="Unsupported account resource"):
        sdk.v1._validate_resource("connections")


@pytest.mark.asyncio
async def test_v1_discovered_accounts_requires_auth_attempt_id() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")
    sdk.v1.set_session_context("session-1", "company-1")

    with pytest.raises(TypeError, match="auth_attempt_id"):
        await sdk.v1.list_discovered_accounts()  # type: ignore[call-arg]


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


def test_v1_reads_trace_header_from_generated_response() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")

    response = sdk.v1._deserialize_response(FakeGeneratedResponse())

    assert response["traceId"] == "trace-from-generated-response"
    assert response["data"] == {"ok": True}
