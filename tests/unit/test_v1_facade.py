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

    response = await sdk.v1.create_session(user_id="user-1")

    assert response["success"]["data"]["session_id"] == "session-1"
    assert sdk.v1.session_id == "session-1"
    assert sdk.v1.company_id == "company-1"
    assert fake_api_client.calls[0]["method"] == "POST"
    assert fake_api_client.calls[0]["url"] == "https://api.test/api/v1/sessions"
    assert fake_api_client.calls[0]["headers"]["X-API-Key"] == "fntc_live_key"
    assert fake_api_client.calls[0]["headers"]["X-Finatic-Environment"] == "live"
    assert fake_api_client.calls[0]["body"] == {"user_id": "user-1"}


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
async def test_v1_order_commands_send_idempotency_key() -> None:
    sdk = FinaticServer(api_key="fntc_live_key", sdk_config={"base_url": "https://api.test"})
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
