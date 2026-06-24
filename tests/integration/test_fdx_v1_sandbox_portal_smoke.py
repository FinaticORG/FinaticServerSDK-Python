"""FDX v1 sandbox portal smoke — portal HTTP against local finaticAPI.

Portal auth flows are exercised via direct HTTP (FinaticConnect surface), not
the server SDK v1 facade. The server SDK is used only for session creation.
"""

from __future__ import annotations

import pytest
from finatic_server.api_client import ApiClient
from finatic_server.configuration import Configuration

from src.v1 import V1Client
from tests.integration.helpers.fdx_sandbox import (
    DEFAULT_API_BASE_URL,
    assert_api_reachable,
    bootstrap_sandbox_api_key,
    create_sandbox_portal_account_grant,
    create_sandbox_portal_auth_attempt,
    create_sandbox_portal_session,
    integration_enabled,
    list_portal_institutions_http,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not integration_enabled(),
        reason="Set FINATIC_INTEGRATION=1 to run live-stack SDK tests",
    ),
]

LINK_EMAIL = "fdx-python-sdk-smoke@finatic.test"


def _build_v1_client(api_key: str) -> V1Client:
    configuration = Configuration(host=DEFAULT_API_BASE_URL)
    api_client = ApiClient(configuration=configuration)
    return V1Client(
        api_client=api_client,
        config=configuration,
        api_key=api_key,
        environment="sandbox",
    )


@pytest.mark.asyncio
async def test_v1_sandbox_lists_portal_institutions() -> None:
    await assert_api_reachable()
    bootstrap, cleanup = await bootstrap_sandbox_api_key()
    v1_client = _build_v1_client(bootstrap.sandbox_api_key)
    try:
        portal_context = await create_sandbox_portal_session(
            v1_client,
            bootstrap.sandbox_api_key,
            LINK_EMAIL,
        )
        response = await list_portal_institutions_http(
            api_key=bootstrap.sandbox_api_key,
            session_id=portal_context.session_id,
            csrf_token=portal_context.csrf_token,
        )
        assert not response.get("errors"), response.get("errors")
        institutions = response.get("data")
        assert isinstance(institutions, list)
        assert len(institutions) >= 12
    finally:
        await cleanup()


@pytest.mark.asyncio
async def test_v1_sandbox_credential_portal_grant_fidelity() -> None:
    await assert_api_reachable()
    bootstrap, cleanup = await bootstrap_sandbox_api_key()
    v1_client = _build_v1_client(bootstrap.sandbox_api_key)
    try:
        portal_context = await create_sandbox_portal_session(
            v1_client,
            bootstrap.sandbox_api_key,
            LINK_EMAIL,
        )
        auth_attempt = await create_sandbox_portal_auth_attempt(
            api_key=bootstrap.sandbox_api_key,
            session_id=portal_context.session_id,
            csrf_token=portal_context.csrf_token,
            provider_id="fidelity",
        )
        assert auth_attempt.get("status") in {"discovered", "accounts_discovered"}

        grant = await create_sandbox_portal_account_grant(
            api_key=bootstrap.sandbox_api_key,
            session_id=portal_context.session_id,
            csrf_token=portal_context.csrf_token,
            auth_attempt=auth_attempt,
        )
        assert grant.get("status") == "active"
        assert grant.get("id") or grant.get("grantId")
    finally:
        await cleanup()


@pytest.mark.asyncio
async def test_v1_sandbox_oauth_auth_attempt_alpaca() -> None:
    await assert_api_reachable()
    bootstrap, cleanup = await bootstrap_sandbox_api_key()
    v1_client = _build_v1_client(bootstrap.sandbox_api_key)
    try:
        portal_context = await create_sandbox_portal_session(
            v1_client,
            bootstrap.sandbox_api_key,
            LINK_EMAIL,
        )
        auth_attempt = await create_sandbox_portal_auth_attempt(
            api_key=bootstrap.sandbox_api_key,
            session_id=portal_context.session_id,
            csrf_token=portal_context.csrf_token,
            provider_id="alpaca",
        )
        assert auth_attempt.get("status") in {"auth_required", "redirect_required"}
        assert (
            auth_attempt.get("callbackState")
            or auth_attempt.get("callback_state")
            or auth_attempt.get("authorizationUrl")
            or auth_attempt.get("authorization_url")
        )
    finally:
        await cleanup()
