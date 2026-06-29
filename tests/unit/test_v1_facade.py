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
        return FakeResponse({"success": {"data": [], "meta": None}, "error": None})


V1_DATA_OPERATION_METHODS = {
    ("GET", "/api/v1/account-grants"): "list_account_grants",
    ("GET", "/api/v1/account-grants/{grantId}"): "get_account_grant",
    ("PATCH", "/api/v1/account-grants/{grantId}"): "update_account_grant",
    ("POST", "/api/v1/account-grants/{grantId}/revoke"): "revoke_account_grant",
    ("GET", "/api/v1/accounts"): "list_accounts",
    ("GET", "/api/v1/accounts/{accountId}"): "get_account",
    ("GET", "/api/v1/accounts/{accountId}/balances"): "list_balances",
    ("GET", "/api/v1/accounts/{accountId}/orders"): "list_orders",
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
    ("GET", "/api/v1/accounts/{accountId}/positions"): "list_positions",
    (
        "GET",
        "/api/v1/accounts/{accountId}/transactions",
    ): "list_transactions",
    ("GET", "/api/v1/accounts/{accountId}/{resource}"): "list_account_resource",
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
            if "sdk" in audiences:
                operations.add((method.upper(), path))
    return operations


def _data_openapi_operations() -> set[tuple[str, str]]:
    return {
        operation
        for operation in _v1_openapi_operations()
        if "/session" not in operation[1]
    }


def test_v1_facade_covers_data_openapi_sdk_audience_operations() -> None:
    openapi_operations = _data_openapi_operations()

    assert len(openapi_operations) == len(V1_DATA_OPERATION_METHODS)
    assert set(V1_DATA_OPERATION_METHODS) == openapi_operations

    for method_name in V1_DATA_OPERATION_METHODS.values():
        assert hasattr(V1Client, method_name)

    assert not hasattr(V1Client, "create_session")
    assert hasattr(V1Client, "start_session")
    assert hasattr(V1Client, "get_portal_url")


def test_finatic_server_exposes_v1_facade_with_environment() -> None:
    sdk = FinaticServer(
        api_key="fntc_sandbox_key",
        sdk_config={"base_url": "https://api.test", "environment": "sandbox"},
    )

    assert isinstance(sdk.v1, V1Client)
    assert sdk.v1.environment == "sandbox"


@pytest.mark.asyncio
async def test_v1_account_routes_use_session_environment_and_query() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key",
        sdk_config={"base_url": "https://api.test", "environment": "sandbox"},
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]
    sdk.v1.set_session_context("session-1", "company-1")

    await sdk.v1.list_transactions("account-1", limit=50, offset=10)

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


def test_v1_reads_trace_header_from_generated_response() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")

    response = sdk.v1._deserialize_response(FakeGeneratedResponse())

    assert response["traceId"] == "trace-from-generated-response"
    assert response["data"] == {"ok": True}
