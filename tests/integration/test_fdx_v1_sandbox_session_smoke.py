"""FDX v1 sandbox session smoke against a local finaticAPI stack."""

from __future__ import annotations

import pytest
from finatic_server.api_client import ApiClient
from finatic_server.configuration import Configuration

from src.v1 import V1Client
from tests.integration.helpers.fdx_sandbox import (
    DEFAULT_API_BASE_URL,
    DEVICE_HEADERS,
    assert_api_reachable,
    bootstrap_sandbox_api_key,
    integration_enabled,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not integration_enabled(),
        reason="Set FINATIC_INTEGRATION=1 to run live-stack SDK tests",
    ),
]


def _build_v1_client(api_key: str) -> V1Client:
    configuration = Configuration(host=DEFAULT_API_BASE_URL)
    api_client = ApiClient(configuration=configuration)
    api_client.default_headers.update(DEVICE_HEADERS)
    return V1Client(
        api_client=api_client,
        config=configuration,
        api_key=api_key,
        environment="sandbox",
    )


@pytest.mark.asyncio
async def test_v1_starts_sandbox_session_with_api_key() -> None:
    await assert_api_reachable()
    bootstrap, cleanup = await bootstrap_sandbox_api_key()
    v1_client = _build_v1_client(bootstrap.sandbox_api_key)

    try:
        session = await v1_client.start_session()

        assert session["success"] is True, session["error"]
        assert session["session_id"]
        assert session["company_id"] == bootstrap.account_id
        assert v1_client.get_session_id() == session["session_id"]
        assert v1_client.get_company_id() == session["company_id"]
        assert v1_client.is_authed() is False
    finally:
        await cleanup()
