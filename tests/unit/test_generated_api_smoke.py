from __future__ import annotations

import asyncio
import inspect
import json
import types
from types import UnionType
from typing import Annotated, Any, Union, get_args, get_origin
from uuid import UUID

from pydantic import BaseModel
from src.openapi.generated import rest
from src.openapi.generated.api.brokers_api import BrokersApi
from src.openapi.generated.api.company_api import CompanyApi
from src.openapi.generated.api.session_api import SessionApi
from src.openapi.generated.api_client import ApiClient
from src.openapi.generated.configuration import Configuration


class _FakeAiohttpLikeResponse:
    """Minimal stand-in for aiohttp.ClientResponse; wrapped by rest.RESTResponse in production."""

    def __init__(self) -> None:
        self.status = 200
        self.reason = "OK"
        self.headers: dict[str, str] = {
            "content-type": "application/json; charset=utf-8",
        }

    async def read(self) -> bytes:
        payload = {
            "success": {"data": [], "meta": None},
            "error": None,
            "warning": None,
        }
        return json.dumps(payload).encode("utf-8")


def _minimal_valid_order_request() -> Any:
    """Smallest valid OrderRequest for generated API validate_call (Webull modify delta)."""
    from src.openapi.generated.models.accountnumber import Accountnumber
    from src.openapi.generated.models.order7 import Order7
    from src.openapi.generated.models.order_request import OrderRequest
    from src.openapi.generated.models.webull_market_order_modify_query_params import (
        WebullMarketOrderModifyQueryParams,
    )
    from src.openapi.generated.models.webull_order_modify_request import (
        WebullOrderModifyRequest,
    )

    order_delta = WebullMarketOrderModifyQueryParams(order_type="market")
    return OrderRequest(
        WebullOrderModifyRequest(
            broker="webull",
            account_number=Accountnumber("acct"),
            order=Order7(order_delta),
        )
    )


def _inner_non_optional(annotation: Any) -> Any:
    """Resolve Optional / Annotated to the concrete type used for dummy values."""
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin in (Union, UnionType) and args:
        non_none = [item for item in args if item is not type(None)]
        if len(non_none) == 1:
            return _inner_non_optional(non_none[0])
        return annotation
    if origin is Annotated and args:
        return _inner_non_optional(args[0])
    return annotation


def _dummy_value(parameter_name: str, annotation: Any) -> Any:
    lowered = parameter_name.lower()
    inner = _inner_non_optional(annotation)
    if inner is UUID:
        return UUID("00000000-0000-4000-8000-000000000001")

    if inspect.isclass(inner) and issubclass(inner, BaseModel):
        from src.openapi.generated.models.order_request import OrderRequest
        from src.openapi.generated.models.session_start_request import (
            SessionStartRequest,
        )

        if inner is OrderRequest or inner.__name__ == "OrderRequest":
            return _minimal_valid_order_request()
        if inner is SessionStartRequest or inner.__name__ == "SessionStartRequest":
            return SessionStartRequest()

    # For openapi generator, IDs and keys are typically strings.
    if "id" in lowered or "key" in lowered or "token" in lowered:
        return "test-id"

    # For pagination params.
    if "limit" in lowered or "offset" in lowered:
        return 1

    # Booleans
    if "include" in lowered or lowered.startswith("is_"):
        return True

    # Best-effort: choose by annotation when it is obvious.
    ann_str = str(annotation)
    if "StrictInt" in ann_str or "int" in ann_str:
        return 1
    if "StrictFloat" in ann_str or "float" in ann_str:
        return 1.0

    return "value"


async def _invoke_callable_with_dummy_arguments(method: Any) -> None:
    signature = inspect.signature(method)
    keyword_arguments: dict[str, Any] = {}

    for parameter_name, parameter in signature.parameters.items():
        if parameter_name == "self":
            continue

        if parameter.kind in (inspect.Parameter.VAR_KEYWORD, inspect.Parameter.VAR_POSITIONAL):
            # Generated API methods don't usually use these; skip to avoid passing invalid kwargs.
            continue

        if parameter.default is not inspect.Signature.empty:
            continue

        keyword_arguments[parameter_name] = _dummy_value(parameter_name, parameter.annotation)

    result = method(**keyword_arguments)
    if inspect.isawaitable(result):
        await result


async def _run_api_smoke(api: Any) -> int:
    error_count = 0
    invoked = 0
    first_error_method: str | None = None
    first_error: BaseException | None = None

    for method_name, method in inspect.getmembers(api, predicate=callable):
        if method_name.startswith("_"):
            continue

        try:
            await _invoke_callable_with_dummy_arguments(method)
            invoked += 1
        except Exception as e:
            error_count += 1
            if first_error_method is None:
                first_error_method = method_name
                first_error = e

    assert error_count == 0, f"First error: {first_error_method}: {first_error!r}"
    return invoked


def test_generated_api_smoke_invokes_many_endpoints() -> None:
    configuration = Configuration.get_default()
    api_client = ApiClient(configuration)

    # Stub the underlying HTTP transport: execute request-building code, but avoid real network.
    async def _stub_request(
        method: str,
        url: str,
        headers: Any = None,
        body: Any = None,
        post_params: Any = None,
        _request_timeout: Any = None,
    ) -> rest.RESTResponse:
        return rest.RESTResponse(_FakeAiohttpLikeResponse())

    api_client.rest_client.request = _stub_request  # type: ignore[method-assign]

    # Patch ApiClient.deserialize to bypass pydantic schema validation; we only need execution coverage.
    def _fake_deserialize(self: ApiClient, response_text: str, response_type: Any, content_type: Any = None) -> Any:
        return json.loads(response_text)

    api_client.deserialize = types.MethodType(_fake_deserialize, api_client)  # type: ignore[method-assign]

    brokers_invoked = asyncio.run(_run_api_smoke(BrokersApi(api_client)))
    company_invoked = asyncio.run(_run_api_smoke(CompanyApi(api_client)))
    session_invoked = asyncio.run(_run_api_smoke(SessionApi(api_client)))

    assert brokers_invoked > 10
    assert company_invoked >= 1
    assert session_invoked > 8

