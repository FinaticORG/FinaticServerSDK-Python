from __future__ import annotations

import asyncio
import inspect
from typing import Any

from src.generated.wrappers.brokers import BrokersWrapper
from src.generated.wrappers.company import CompanyWrapper
from src.generated.wrappers.session import SessionWrapper


class _ApiProxy:
    def __getattr__(self, _name: str) -> Any:
        class _FinaticResponseLike:
            def __init__(self) -> None:
                self.success = {"data": []}
                self.error = None
                self.warning = None

        async def _fake_call(*_args: Any, **_kwargs: Any) -> Any:
            return _FinaticResponseLike()

        return _fake_call


async def _invoke_awaitable(maybe_awaitable: Any) -> None:
    if inspect.isawaitable(maybe_awaitable):
        await maybe_awaitable


def _build_brokers_wrapper() -> BrokersWrapper:
    wrapper = BrokersWrapper(_ApiProxy(), None, None)
    wrapper.set_session_context("session-id", "company-id", "csrf-token")
    return wrapper


def _build_company_wrapper() -> CompanyWrapper:
    return CompanyWrapper(_ApiProxy(), None, None)


def _build_session_wrapper() -> SessionWrapper:
    return SessionWrapper(_ApiProxy(), None, None)


def test_generated_wrappers_smoke_invokes_many_methods() -> None:
    brokers = _build_brokers_wrapper()
    company = _build_company_wrapper()
    session = _build_session_wrapper()

    # Brokers wrapper: hit the most commonly used broker browsing/disconnect paths.
    async def _run() -> None:
        await brokers.get_accounts()
        await brokers.get_balances()
        await brokers.get_broker_connections()
        await brokers.get_brokers()
        await brokers.disconnect_company_from_broker(connection_id="test-id")

        # Company wrapper
        await company.get_company(company_id="test-id")

        # Session wrapper: keep it local (mocked API), but provide required x_api_key.
        await session.init_session(x_api_key="test-api-key")

    asyncio.run(_run())
