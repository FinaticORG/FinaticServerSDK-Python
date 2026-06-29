"""FDX Phase 7 sandbox helpers for live-stack integration tests."""

from __future__ import annotations

import hashlib
import os
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import NAMESPACE_DNS, uuid4, uuid5

import aiohttp

if TYPE_CHECKING:
    from src.v1 import V1Client

DEVICE_HEADERS: dict[str, str] = {
    "user-agent": "finatic-sdk-integration",
    "accept-language": "en-US",
    "sec-ch-ua": '"Chromium";v="124"',
    "sec-ch-ua-platform": '"Linux"',
}

SANDBOX_USER_ID_NAMESPACE = uuid5(NAMESPACE_DNS, "sandbox_user_id_from_email")
DEFAULT_API_BASE_URL = os.environ.get("FINATIC_API_BASE_URL", "http://127.0.0.1:8000")
DEFAULT_DATABASE_URL = os.environ.get(
    "FINATIC_DATABASE_URL",
    "postgresql://postgres:postgres@127.0.0.1:54322/postgres",
)


def integration_enabled() -> bool:
    return os.environ.get("FINATIC_INTEGRATION") == "1"


def sandbox_user_id_from_email(email: str) -> str:
    normalized_email = email.strip().lower()
    if not normalized_email:
        raise ValueError("Email cannot be empty")
    return str(uuid5(SANDBOX_USER_ID_NAMESPACE, normalized_email))


@dataclass(frozen=True)
class SandboxBootstrapResult:
    sandbox_api_key: str
    account_id: str


async def bootstrap_sandbox_api_key() -> (
    tuple[SandboxBootstrapResult, Callable[[], Awaitable[None]]]
):
    existing_api_key = os.environ.get("FINATIC_SANDBOX_API_KEY")
    if existing_api_key:
        result = SandboxBootstrapResult(
            sandbox_api_key=existing_api_key,
            account_id=os.environ.get("FINATIC_SANDBOX_ACCOUNT_ID", ""),
        )

        async def noop_cleanup() -> None:
            return None

        return result, noop_cleanup

    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError(
            "Install integration extras: uv sync --extra integration"
        ) from exc

    sandbox_api_key = f"fntc_sandbox_test_{uuid4().hex}"
    sandbox_api_key_hash = hashlib.sha256(sandbox_api_key.encode()).hexdigest()
    account_id = str(uuid4())
    test_email = f"sandbox-{account_id[:8]}@test.company"

    async with await psycopg.AsyncConnection.connect(
        DEFAULT_DATABASE_URL
    ) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO auth.users (
                    id, instance_id, aud, role, email, encrypted_password,
                    email_confirmed_at, created_at, updated_at, confirmation_token,
                    email_change_token_new, recovery_token
                ) VALUES (
                    %s::uuid, '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated',
                    %s, '', NOW(), NOW(), NOW(), '', '', ''
                )
                ON CONFLICT (id) DO NOTHING
                """,
                (account_id, test_email),
            )
            await cursor.execute(
                """
                INSERT INTO accounts (
                    id, name, email, is_personal_account, primary_owner_user_id,
                    public_data, sandbox_api_key_hash, sandbox_key_created_at,
                    sandbox_key_expires_at, trading_enabled
                ) VALUES (
                    %s::uuid, %s, %s, true, %s::uuid,
                    '{}'::jsonb, %s, NOW(), NULL, true
                )
                ON CONFLICT (id) DO UPDATE SET
                    sandbox_api_key_hash = EXCLUDED.sandbox_api_key_hash,
                    sandbox_key_created_at = EXCLUDED.sandbox_key_created_at,
                    trading_enabled = EXCLUDED.trading_enabled
                """,
                (
                    account_id,
                    "SDK Integration Sandbox Company",
                    test_email,
                    account_id,
                    sandbox_api_key_hash,
                ),
            )
        await connection.commit()

    async def cleanup() -> None:
        async with await psycopg.AsyncConnection.connect(
            DEFAULT_DATABASE_URL
        ) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "DELETE FROM accounts WHERE id = %s::uuid", (account_id,)
                )
                await cursor.execute(
                    "DELETE FROM auth.users WHERE id = %s::uuid", (account_id,)
                )
            await connection.commit()

    return (
        SandboxBootstrapResult(sandbox_api_key=sandbox_api_key, account_id=account_id),
        cleanup,
    )


async def assert_api_reachable(base_url: str = DEFAULT_API_BASE_URL) -> None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{base_url}/api/v1/sessions",
                timeout=aiohttp.ClientTimeout(total=5),
            ):
                return
    except (aiohttp.ClientError, OSError, TimeoutError) as exc:
        raise RuntimeError(
            f"finaticAPI not reachable at {base_url}. "
            "Start the local stack before FINATIC_INTEGRATION=1 tests."
        ) from exc


def _session_field(session_data: dict, *keys: str) -> str:
    for key in keys:
        value = session_data.get(key)
        if value is not None:
            return str(value)
    raise KeyError(f"Missing session field ({', '.join(keys)}) in {session_data}")


async def prime_portal_csrf_token(
    api_key: str,
    session_id: str,
    base_url: str = DEFAULT_API_BASE_URL,
) -> str:
    headers = {
        "x-api-key": api_key,
        "X-Finatic-Environment": "sandbox",
        **DEVICE_HEADERS,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{base_url}/api/v1/portal/{session_id}/institutions",
            headers=headers,
        ) as response:
            if response.status != 200:
                body = await response.text()
                raise RuntimeError(
                    f"Failed to prime portal CSRF: {response.status} {body}"
                )
            csrf_token = response.headers.get("x-csrf-token")
            if not csrf_token:
                raise RuntimeError(
                    "Expected x-csrf-token header from portal institutions GET"
                )
            return csrf_token


@dataclass(frozen=True)
class SandboxPortalSessionContext:
    session_id: str
    company_id: str
    csrf_token: str
    user_id: str


async def _portal_json_request(
    *,
    method: str,
    api_key: str,
    session_id: str,
    path_suffix: str,
    csrf_token: str,
    body: dict | None = None,
    base_url: str = DEFAULT_API_BASE_URL,
) -> dict:
    headers = {
        "x-api-key": api_key,
        "X-Finatic-Environment": "sandbox",
        "X-Session-ID": session_id,
        "x-csrf-token": csrf_token,
        "content-type": "application/json",
        **DEVICE_HEADERS,
    }
    url = f"{base_url}/api/v1/portal/{session_id}/{path_suffix}"
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method,
            url,
            headers=headers,
            json=body,
        ) as response:
            payload = await response.json()
            if response.status >= 400:
                raise RuntimeError(f"Portal {method} {path_suffix} failed: {payload}")
            return payload


async def list_portal_institutions_http(
    *,
    api_key: str,
    session_id: str,
    csrf_token: str,
    base_url: str = DEFAULT_API_BASE_URL,
) -> dict:
    headers = {
        "x-api-key": api_key,
        "X-Finatic-Environment": "sandbox",
        "X-Session-ID": session_id,
        "x-csrf-token": csrf_token,
        **DEVICE_HEADERS,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{base_url}/api/v1/portal/{session_id}/institutions",
            headers=headers,
        ) as response:
            payload = await response.json()
            if response.status != 200:
                raise RuntimeError(f"Failed to list portal institutions: {payload}")
            return payload


async def link_portal_user_http(
    *,
    api_key: str,
    session_id: str,
    user_id: str,
    csrf_token: str,
    base_url: str = DEFAULT_API_BASE_URL,
) -> dict:
    return await _portal_json_request(
        method="POST",
        api_key=api_key,
        session_id=session_id,
        path_suffix="user-link",
        csrf_token=csrf_token,
        body={"userId": user_id},
        base_url=base_url,
    )


async def create_sandbox_portal_session(
    v1_client: V1Client,
    api_key: str,
    link_email: str,
    base_url: str = DEFAULT_API_BASE_URL,
) -> SandboxPortalSessionContext:
    session_response = await v1_client.create_session()
    if session_response.get("errors"):
        raise RuntimeError(str(session_response["errors"]))
    session_data = session_response.get("data") or {}
    if not isinstance(session_data, dict):
        raise TypeError(f"Unexpected session payload: {session_data!r}")
    session_id = _session_field(session_data, "sessionId", "session_id")
    company_id = _session_field(session_data, "companyId", "company_id")
    csrf_token = await prime_portal_csrf_token(api_key, session_id, base_url)
    v1_client.set_session_context(
        session_id=session_id,
        company_id=company_id,
        csrf_token=csrf_token,
    )

    user_id = sandbox_user_id_from_email(link_email)
    link_response = await link_portal_user_http(
        api_key=api_key,
        session_id=session_id,
        user_id=user_id,
        csrf_token=csrf_token,
        base_url=base_url,
    )
    if link_response.get("errors"):
        raise RuntimeError(str(link_response["errors"]))

    return SandboxPortalSessionContext(
        session_id=session_id,
        company_id=company_id,
        csrf_token=csrf_token,
        user_id=user_id,
    )


def _first_present(record: dict, *keys: str):
    for key in keys:
        if record.get(key) is not None:
            return record.get(key)
    return None


async def create_sandbox_portal_auth_attempt(
    *,
    api_key: str,
    session_id: str,
    csrf_token: str,
    provider_id: str,
    base_url: str = DEFAULT_API_BASE_URL,
) -> dict:
    response = await _portal_json_request(
        method="POST",
        api_key=api_key,
        session_id=session_id,
        path_suffix="auth-attempts",
        csrf_token=csrf_token,
        body={"brokerId": provider_id},
        base_url=base_url,
    )
    if response.get("errors"):
        raise RuntimeError(str(response["errors"]))
    data = response.get("data")
    if not isinstance(data, dict):
        raise TypeError(f"Unexpected auth attempt payload: {data!r}")
    return data


async def create_sandbox_portal_account_grant(
    *,
    api_key: str,
    session_id: str,
    csrf_token: str,
    auth_attempt: dict,
    base_url: str = DEFAULT_API_BASE_URL,
) -> dict:
    auth_attempt_id = str(_first_present(auth_attempt, "id", "authAttemptId") or "")
    discovered_account_ids = (
        _first_present(auth_attempt, "discoveredAccountIds", "discovered_account_ids")
        or []
    )
    if not auth_attempt_id or not discovered_account_ids:
        raise RuntimeError(f"Auth attempt missing discovered accounts: {auth_attempt}")

    response = await _portal_json_request(
        method="POST",
        api_key=api_key,
        session_id=session_id,
        path_suffix="account-grants",
        csrf_token=csrf_token,
        body={
            "accountId": str(discovered_account_ids[0]),
            "authAttemptId": auth_attempt_id,
            "canRead": True,
            "canTrade": False,
        },
        base_url=base_url,
    )
    if response.get("errors"):
        raise RuntimeError(str(response["errors"]))
    data = response.get("data")
    if not isinstance(data, dict):
        raise TypeError(f"Unexpected grant payload: {data!r}")
    return data
