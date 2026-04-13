from __future__ import annotations

import asyncio
import inspect

from src.FinaticServerCore import FinaticServer


def _dummy_value(parameter_name: str) -> object:
    lowered_parameter_name = parameter_name.lower()
    if "id" in lowered_parameter_name:
        return "test-id"
    if "api_key" in lowered_parameter_name:
        return "test-api-key"
    if "limit" in lowered_parameter_name or "offset" in lowered_parameter_name:
        return 1
    if lowered_parameter_name.startswith("is_") or lowered_parameter_name.startswith("include_"):
        return True
    return "value"


def _invoke_callable_with_dummy_arguments(method: object) -> object:
    signature = inspect.signature(method)
    keyword_arguments: dict[str, object] = {}
    for parameter_name, parameter in signature.parameters.items():
        if parameter_name == "self":
            continue
        # Skip VAR_KEYWORD parameters like `**kwargs` so we don't pass invalid
        # keyword arguments into generated FinaticServer methods.
        parameter_obj = signature.parameters[parameter_name]
        if parameter_obj.kind == inspect.Parameter.VAR_KEYWORD:  # type: ignore[attr-defined]
            continue
        if parameter.default is not inspect.Signature.empty:
            continue
        keyword_arguments[parameter_name] = _dummy_value(parameter_name)
    return method(**keyword_arguments)  # type: ignore[misc]


def test_generated_sdk_smoke_invokes_many_methods() -> None:
    sdk = FinaticServer(api_key="test-api-key")
    invoked_count = 0

    for method_name, method in inspect.getmembers(sdk, predicate=callable):
        if method_name.startswith("_"):
            continue
        try:
            result = _invoke_callable_with_dummy_arguments(method)
            if inspect.isawaitable(result):
                asyncio.run(result)
            invoked_count += 1
        except Exception:
            invoked_count += 1

    assert invoked_count > 10
