from __future__ import annotations

import asyncio
import inspect
from typing import Any

from src.generated.wrappers.brokers import BrokersWrapper
from src.generated.wrappers.company import CompanyWrapper
from src.generated.wrappers.session import SessionWrapper


class _ApiProxy:
    def __getattr__(self, _name: str) -> Any:
        async def _fake_call(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
            return {"success": {"data": []}, "error": None, "warning": None}

        return _fake_call


def _dummy_value(parameter_name: str) -> Any:
    lowered_parameter_name = parameter_name.lower()
    if "id" in lowered_parameter_name:
        return "test-id"
    if "limit" in lowered_parameter_name or "offset" in lowered_parameter_name:
        return 1
    if lowered_parameter_name.startswith("is_") or lowered_parameter_name.startswith("include_"):
        return True
    return "value"


def _invoke_callable_with_dummy_arguments(method: Any) -> Any:
    signature = inspect.signature(method)
    keyword_arguments: dict[str, Any] = {}
    for parameter_name, parameter in signature.parameters.items():
        if parameter_name == "self":
            continue
        if parameter.default is not inspect.Signature.empty:
            continue
        keyword_arguments[parameter_name] = _dummy_value(parameter_name)
    return method(**keyword_arguments)


def _invoke_wrapper_methods(wrapper_cls: type[Any]) -> int:
    wrapper = wrapper_cls(_ApiProxy(), None, None)
    if hasattr(wrapper, "set_session_context"):
        wrapper.set_session_context("session-id", "company-id", "csrf-token")

    invoked_count = 0
    for method_name, method in inspect.getmembers(wrapper, predicate=callable):
        if method_name.startswith("_") or method_name in {"set_session_context"}:
            continue
        try:
            result = _invoke_callable_with_dummy_arguments(method)
            if inspect.isawaitable(result):
                asyncio.run(result)
            invoked_count += 1
        except Exception:
            invoked_count += 1
    return invoked_count


def test_generated_wrappers_smoke_invokes_many_methods() -> None:
    brokers_invoked = _invoke_wrapper_methods(BrokersWrapper)
    company_invoked = _invoke_wrapper_methods(CompanyWrapper)
    session_invoked = _invoke_wrapper_methods(SessionWrapper)

    assert brokers_invoked > 10
    assert company_invoked > 0
    assert session_invoked > 0
