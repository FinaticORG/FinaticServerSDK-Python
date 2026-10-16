from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import src.v1 as v1_module
from finatic_server_python import (
    AccountOrderPayload,
    SessionStartResult,
    SessionStatus,
)
from src.FinaticServerCore import FinaticServer
from src.v1 import V1Client


def test_public_session_types_match_v1_contract() -> None:
    assert SessionStartResult is v1_module.SessionStartResult
    assert SessionStatus is v1_module.SessionStatus


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


class DescriptorApiClient(FakeApiClient):
    def call_api(
        self,
        method: str,
        url: str,
        header_params: dict[str, str] | None = None,
        body: dict[str, Any] | None = None,
    ) -> FakeResponse:
        instrument = {
            "version": "1",
            "finaticInstrumentId": "finatic:future:MGCZ6",
            "displaySymbol": "MGCZ6",
            "assetType": "FUTURE",
            "future": {"productRoot": "MGC", "identityQuality": "EXACT"},
        }
        if url.endswith("/fills"):
            data = [{"fillId": "fill-1", "instrument": instrument}]
        elif url.endswith("/events"):
            data = [{"eventId": "event-1", "affectedInstruments": [instrument]}]
        elif url.endswith("/positions"):
            data = [{"id": "position-1", "instrument": instrument}]
        else:
            data = [{"orderId": "order-1", "legs": [{"instrument": instrument}]}]
        return FakeResponse({"data": data, "warnings": [], "errors": []})


class SessionApiClient(FakeApiClient):
    def __init__(self, payloads: list[dict[str, Any]]) -> None:
        super().__init__()
        self.payloads = payloads

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
        return FakeResponse(self.payloads.pop(0))


V1_DATA_OPERATION_METHODS = {
    ("GET", "/api/v1/account-grants"): "list_account_grants",
    ("GET", "/api/v1/account-grants/{grantId}"): "get_account_grant",
    ("PATCH", "/api/v1/account-grants/{grantId}"): "update_account_grant",
    ("POST", "/api/v1/account-grants/{grantId}/revoke"): "revoke_account_grant",
    (
        "POST",
        "/api/v1/users/{userId}/broker-connections/offboarding",
    ): "offboard_broker_connection",
    ("GET", "/api/v1/accounts"): "list_accounts",
    ("GET", "/api/v1/accounts/{accountId}"): "get_account",
    ("GET", "/api/v1/accounts/{accountId}/balances"): "list_balances",
    (
        "GET",
        "/api/v1/accounts/{accountId}/order-schemas",
    ): "get_account_order_schema",
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
        if (
            operation[1].startswith(
                (
                    "/api/v1/account-grants",
                    "/api/v1/accounts",
                    "/api/v1/webhooks",
                )
            )
            or operation[1] == "/api/v1/users/{userId}/broker-connections/offboarding"
        )
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
async def test_start_session_preserves_authoritative_active_identity() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    fake_api_client = SessionApiClient(
        [
            {
                "data": {
                    "session_id": "session-1",
                    "company_id": "company-1",
                    "csrf_token": "csrf-1",
                    "status": "active",
                    "user_id": "server-user",
                    "provided_user_id_rejected": False,
                    "portal_connection_management_pending": True,
                },
                "errors": [],
            }
        ]
    )
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]

    result: SessionStartResult = await sdk.v1.start_session(
        one_time_token="token-1", user_id="requested-user"
    )

    assert result == {
        "success": True,
        "session_id": "session-1",
        "company_id": "company-1",
        "error": None,
        "status": "active",
        "user_id": "server-user",
        "provided_user_id_rejected": False,
        "portal_connection_management_pending": True,
        "authenticated": True,
    }
    assert fake_api_client.calls[0]["body"] == {"user_id": "requested-user"}
    assert sdk.v1.get_user_id() == "server-user"
    assert sdk.v1.is_authed() is True


@pytest.mark.asyncio
async def test_rejected_session_clears_reused_identity_and_accepts_wire_aliases() -> (
    None
):
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    sdk.v1.api_client = SessionApiClient(  # type: ignore[assignment]
        [
            {
                "data": {
                    "sessionId": "session-1",
                    "companyId": "company-1",
                    "status": "active",
                    "userId": "server-user",
                },
                "errors": [],
            },
            {
                "data": {
                    "sessionId": "session-2",
                    "companyId": "company-1",
                    "status": "authenticating",
                    "userId": None,
                    "providedUserIdRejected": True,
                    "portalConnectionManagementPending": True,
                },
                "errors": [],
            },
        ]
    )

    active = await sdk.v1.start_session(one_time_token="token-1")
    rejected = await sdk.v1.start_session(
        one_time_token="token-2", user_id="requested-user"
    )

    assert active["authenticated"] is True
    assert rejected == {
        "success": True,
        "session_id": "session-2",
        "company_id": "company-1",
        "error": None,
        "status": "authenticating",
        "user_id": None,
        "provided_user_id_rejected": True,
        "portal_connection_management_pending": True,
        "authenticated": False,
    }
    assert sdk.v1.get_user_id() is None
    assert sdk.v1.is_authed() is False


@pytest.mark.asyncio
async def test_session_state_fails_closed_for_unknown_status_and_truthy_flags() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    sdk.v1.user_id = "stale-user"
    sdk.v1.authenticated = True
    sdk.v1.api_client = SessionApiClient(  # type: ignore[assignment]
        [
            {
                "data": {
                    "session_id": "session-2",
                    "company_id": "company-1",
                    "status": "ACTIVE",
                    "user_id": "server-user",
                    "provided_user_id_rejected": 1,
                    "portal_connection_management_pending": "true",
                },
                "errors": [],
            }
        ]
    )

    result = await sdk.v1.start_session(one_time_token="token-2")

    assert result["status"] is None
    assert result["provided_user_id_rejected"] is False
    assert result["portal_connection_management_pending"] is False
    assert result["authenticated"] is False
    assert sdk.v1.get_user_id() is None
    assert sdk.v1.is_authed() is False


@pytest.mark.parametrize(
    "session_data",
    [
        {"status": "active"},
        {"status": "active", "user_id": 123},
        {"user_id": "server-user"},
        {},
    ],
)
@pytest.mark.asyncio
async def test_session_state_fails_closed_for_missing_or_malformed_identity(
    session_data: dict[str, Any],
) -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    sdk.v1.user_id = "stale-user"
    sdk.v1.authenticated = True
    sdk.v1.api_client = SessionApiClient(  # type: ignore[assignment]
        [
            {
                "data": {
                    "session_id": "session-2",
                    "company_id": "company-1",
                    **session_data,
                },
                "errors": [],
            }
        ]
    )

    result = await sdk.v1.start_session(one_time_token="token-2")

    assert result["authenticated"] is False
    assert sdk.v1.get_user_id() is None
    assert sdk.v1.is_authed() is False


@pytest.mark.asyncio
async def test_automatic_and_supplied_token_paths_share_result_shape(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    response = {
        "data": {
            "session_id": "session-1",
            "company_id": "company-1",
            "status": "pending",
        },
        "errors": [],
    }
    fake_api_client = SessionApiClient([response, response])
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]

    async def fake_get_token(api_key: str | None = None) -> str:
        return "automatic-token"

    monkeypatch.setattr(sdk.v1, "get_token", fake_get_token)

    automatic = await sdk.v1.start_session()
    supplied = await sdk.v1.start_session(one_time_token="supplied-token")

    assert automatic == supplied
    assert set(automatic) == set(SessionStartResult.__required_keys__)
    assert fake_api_client.calls[0]["headers"]["One-Time-Token"] == "automatic-token"
    assert fake_api_client.calls[1]["headers"]["One-Time-Token"] == "supplied-token"


@pytest.mark.asyncio
async def test_start_session_request_errors_use_the_normalized_failure_shape() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    sdk.v1.api_client = SessionApiClient(  # type: ignore[assignment]
        [{"data": None, "errors": [{"message": "token rejected"}]}]
    )

    result = await sdk.v1.start_session(one_time_token="bad-token")

    assert result == {
        "success": False,
        "session_id": None,
        "company_id": None,
        "error": "token rejected",
        "status": None,
        "user_id": None,
        "provided_user_id_rejected": False,
        "portal_connection_management_pending": False,
        "authenticated": False,
    }


@pytest.mark.asyncio
async def test_finatic_server_init_requires_requested_user_authentication(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def pending_start_session(
        self: V1Client,
        *,
        one_time_token: str | None = None,
        user_id: str | None = None,
    ) -> SessionStartResult:
        self.set_session_context("session-1", "company-1")
        status: SessionStatus = "authenticating"
        return {
            "success": True,
            "session_id": "session-1",
            "company_id": "company-1",
            "error": None,
            "status": status,
            "user_id": None,
            "provided_user_id_rejected": user_id is not None,
            "portal_connection_management_pending": True,
            "authenticated": False,
        }

    monkeypatch.setattr(V1Client, "start_session", pending_start_session)

    with pytest.raises(ValueError, match="requested user identity"):
        await FinaticServer.init("fntc_live_key", user_id="requested-user")

    unauthenticated = await FinaticServer.init("fntc_live_key")
    assert unauthenticated.v1.get_session_id() == "session-1"


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
async def test_v1_offboards_account_selected_connection_without_connection_id() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]

    await sdk.v1.offboard_broker_connection(
        "user-1", "account-1", idempotency_key="offboard-key-1"
    )

    call = fake_api_client.calls[0]
    assert call["method"] == "POST"
    assert call["url"] == (
        "https://api.test/api/v1/users/user-1/broker-connections/offboarding"
    )
    assert call["headers"]["Idempotency-Key"] == "offboard-key-1"
    assert call["body"] == {"accountId": "account-1"}
    assert "connectionId" not in json.dumps(call)


@pytest.mark.asyncio
async def test_v1_order_commands_accept_typed_additive_identity() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    fake_api_client = FakeApiClient()
    sdk.v1.api_client = fake_api_client  # type: ignore[assignment]
    order = AccountOrderPayload.from_dict(
        {
            "finaticInstrumentId": "finatic:future:MGCZ6",
            "instrumentId": 611092087,
            "symbol": "MGCZ6",
        }
    )
    assert order is not None

    await sdk.v1.create_account_order("account-1", order, idempotency_key="order-key-2")

    assert fake_api_client.calls[0]["body"] == {
        "order": {
            "finaticInstrumentId": "finatic:future:MGCZ6",
            "instrumentId": 611092087,
            "symbol": "MGCZ6",
        }
    }


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


def test_v1_preserves_event_contract_capability_without_coercion_or_field_loss() -> (
    None
):
    sdk = FinaticServer(api_key="fntc_live_key")
    response = sdk.v1._deserialize_response(
        FakeResponse(
            {
                "data": {
                    "brokerId": "tastytrade",
                    "action": "PLACE",
                    "orderSchema": {
                        "properties": {"assetType": {"const": "EVENT_CONTRACT"}}
                    },
                    "brokerWireSchema": None,
                    "supportedOrderTypesByAssetClass": {"EVENT_CONTRACT": ["MARKET"]},
                    "eventContract": {
                        "providerOffered": True,
                        "implementationEvidenced": True,
                        "publicEnabled": False,
                        "accountEntitled": True,
                        "closingOnly": False,
                        "observedAt": "2026-10-16T10:00:00Z",
                        "implementationRef": "core-sha",
                        "provenanceSource": "provider-capability-observation",
                    },
                },
                "warnings": [],
                "errors": [],
            }
        )
    )

    assert response["data"]["orderSchema"]["properties"]["assetType"]["const"] == (
        "EVENT_CONTRACT"
    )
    assert response["data"]["eventContract"] == {
        "providerOffered": True,
        "implementationEvidenced": True,
        "publicEnabled": False,
        "accountEntitled": True,
        "closingOnly": False,
        "observedAt": "2026-10-16T10:00:00Z",
        "implementationRef": "core-sha",
        "provenanceSource": "provider-capability-observation",
    }


@pytest.mark.parametrize("asset_type", ["BOND", "CFD", "EVENT_CONTRACT"])
def test_v1_preserves_public_asset_type_literals(asset_type: str) -> None:
    sdk = FinaticServer(api_key="fntc_live_key")
    response = sdk.v1._deserialize_response(
        FakeResponse(
            {
                "data": [{"id": "position-1", "assetType": asset_type}],
                "warnings": [],
                "errors": [],
            }
        )
    )

    assert response["data"][0]["assetType"] == asset_type


def test_v1_reads_trace_header_from_generated_response() -> None:
    sdk = FinaticServer(api_key="fntc_live_key")

    response = sdk.v1._deserialize_response(FakeGeneratedResponse())

    assert response["traceId"] == "trace-from-generated-response"
    assert response["data"] == {"ok": True}


@pytest.mark.asyncio
async def test_descriptor_facade_methods_return_typed_raw_mappings() -> None:
    sdk = FinaticServer(
        api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"}
    )
    sdk.v1.api_client = DescriptorApiClient()  # type: ignore[assignment]

    orders = (await sdk.v1.list_orders("account-1"))["data"] or []
    fills = (await sdk.v1.get_account_order_fills("account-1", "order-1"))["data"] or []
    events = (await sdk.v1.get_account_order_events("account-1", "order-1"))[
        "data"
    ] or []
    positions = (await sdk.v1.list_positions("account-1"))["data"] or []

    assert isinstance(orders[0], dict)
    assert orders[0]["legs"][0]["instrument"]["displaySymbol"] == "MGCZ6"
    assert fills[0]["instrument"]["finaticInstrumentId"] == "finatic:future:MGCZ6"
    assert events[0]["affectedInstruments"][0]["future"]["identityQuality"] == "EXACT"
    assert positions[0]["instrument"]["future"]["productRoot"] == "MGC"
