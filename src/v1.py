"""Hand-written v1 client (session, accounts, trading, grants, webhooks).

All versioned public API surface lives here under ``finatic.v1``.
"""

from __future__ import annotations

import asyncio
import inspect
import json
from dataclasses import dataclass
from typing import Any, Literal, cast
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from finatic_server.api_client import ApiClient
from finatic_server.configuration import Configuration

from .types import FinaticResponse
from .utils.url_utils import (
    append_asset_types_to_url,
    append_broker_filter_to_url,
    append_kind_to_url,
    append_stage_to_url,
    append_theme_to_url,
)

Environment = str
_ERROR_CODE_BY_STATUS = {
    400: "VALIDATION",
    401: "AUTHENTICATION",
    403: "AUTHORIZATION",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "VALIDATION",
    429: "RATE_LIMITED",
}
_STABLE_ERROR_CODES = {
    "AUTHENTICATION",
    "AUTHORIZATION",
    "VALIDATION",
    "RATE_LIMITED",
    "REAUTH_REQUIRED",
    "PROVIDER_ERROR",
    "CONFLICT",
    "NOT_FOUND",
    "INTERNAL",
}


@dataclass(frozen=True)
class AccountOrderCommand:
    """Account-scoped order command payload."""

    order: dict[str, Any]


def _read_session_field(data: dict[str, Any] | None, keys: tuple[str, ...]) -> str:
    if not data:
        return ""
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def _append_query_param(url: str, name: str, value: str) -> str:
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params[name] = [value]
    return urlunparse(parsed._replace(query=urlencode(query_params, doseq=True)))


class V1Client:
    """Versioned v1 client over generated transport."""

    def __init__(
        self,
        *,
        api_client: ApiClient,
        config: Configuration,
        api_key: str,
        environment: Environment = "live",
    ) -> None:
        self.api_client = api_client
        self.config = config
        self.api_key = api_key
        self.environment = self._validate_environment(environment)
        self.session_id: str | None = None
        self.company_id: str | None = None
        self.authorization: str | None = None
        self.csrf_token: str | None = None
        self.user_id: str | None = None

    def set_environment(self, environment: Environment) -> None:
        """Set the public v1 environment for subsequent requests."""
        self.environment = self._validate_environment(environment)

    def set_session_context(
        self,
        session_id: str,
        company_id: str | None = None,
        authorization: str | None = None,
        csrf_token: str | None = None,
    ) -> None:
        """Set session headers used by account-first v1 routes."""
        self.session_id = session_id
        self.company_id = company_id
        self.authorization = authorization
        if csrf_token is not None:
            self.csrf_token = csrf_token

    def get_session_id(self) -> str | None:
        return self.session_id

    def get_company_id(self) -> str | None:
        return self.company_id

    def get_user_id(self) -> str | None:
        return self.user_id

    def is_authed(self) -> bool:
        return bool(self.user_id)

    async def init_session(self, api_key: str | None = None) -> FinaticResponse:
        return await self._request(
            "POST",
            "/api/v1/session/init",
            headers={"X-API-Key": api_key or self.api_key},
        )

    async def get_token(self, api_key: str | None = None) -> str:
        response = await self.init_session(api_key)
        if response.get("errors"):
            errors = response["errors"]
            message = (
                errors[0].get("message") if errors else "Failed to initialize session"
            )
            raise ValueError(str(message))
        session_data = response.get("data")
        token = _read_session_field(
            session_data if isinstance(session_data, dict) else None,
            ("one_time_token", "oneTimeToken"),
        )
        if not token:
            raise ValueError("Failed to get one-time token from /api/v1/session/init")
        return token

    async def start_session(
        self,
        *,
        one_time_token: str | None = None,
        user_id: str | None = None,
    ) -> dict[str, Any]:
        if not one_time_token:
            if not self.api_key:
                return {
                    "success": False,
                    "session_id": None,
                    "company_id": None,
                    "error": "API key is required in the constructor.",
                }
            try:
                token = await self.get_token()
                started = await self._start_session_with_token(token, user_id)
                return {
                    "success": True,
                    "session_id": started["session_id"],
                    "company_id": started["company_id"],
                    "error": None,
                }
            except Exception as error:
                return {
                    "success": False,
                    "session_id": None,
                    "company_id": None,
                    "error": str(error),
                }
        return await self._start_session_with_token(one_time_token, user_id)

    async def _start_session_with_token(
        self,
        one_time_token: str,
        user_id: str | None = None,
    ) -> dict[str, str]:
        body = {"user_id": user_id} if user_id else None
        response = await self._request(
            "POST",
            "/api/v1/session/start",
            body=body,
            headers={"One-Time-Token": one_time_token},
        )
        if response.get("errors"):
            errors = response["errors"]
            message = errors[0].get("message") if errors else "Failed to start session"
            raise ValueError(str(message))

        session_data = response.get("data")
        session_data_dict = session_data if isinstance(session_data, dict) else {}
        session_id = _read_session_field(session_data_dict, ("session_id", "sessionId"))
        company_id = _read_session_field(session_data_dict, ("company_id", "companyId"))
        csrf_token = _read_session_field(session_data_dict, ("csrf_token", "csrfToken"))
        response_user_id = _read_session_field(session_data_dict, ("user_id", "userId"))

        if session_id and company_id:
            self.set_session_context(session_id, company_id, csrf_token=csrf_token)

        final_user_id = response_user_id or user_id
        if final_user_id:
            self.user_id = final_user_id

        return {"session_id": session_id, "company_id": company_id}

    async def get_portal_url(
        self,
        *,
        theme: str | dict[str, Any] | None = None,
        brokers: list[str] | None = None,
        kind: Literal["broker", "exchange"] | None = None,
        asset_types: list[str] | None = None,
        stage: list[Literal["production", "beta", "alpha"]] | None = None,
        email: str | None = None,
        mode: Literal["light", "dark"] | None = None,
    ) -> str:
        if not self.session_id:
            raise ValueError("Session not initialized. Call v1.start_session() first.")

        response = await self._request("GET", "/api/v1/session/portal")
        if response.get("errors"):
            errors = response["errors"]
            message = errors[0].get("message") if errors else "Failed to get portal URL"
            raise ValueError(str(message))

        portal_data = response.get("data")
        portal_url = _read_session_field(
            portal_data if isinstance(portal_data, dict) else None,
            ("portal_url", "portalUrl"),
        )
        if not portal_url:
            raise ValueError("Invalid portal URL response: missing portal_url")

        parsed_url = urlparse(portal_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Invalid portal URL received from API: {portal_url}")

        if theme:
            portal_url = append_theme_to_url(portal_url, theme)
        if brokers:
            portal_url = append_broker_filter_to_url(portal_url, brokers)
        if kind:
            portal_url = append_kind_to_url(portal_url, kind)
        if asset_types:
            portal_url = append_asset_types_to_url(portal_url, asset_types)
        if stage:
            portal_url = append_stage_to_url(portal_url, list(stage))
        if email:
            portal_url = _append_query_param(portal_url, "email", email)
        if mode:
            portal_url = _append_query_param(portal_url, "mode", mode)
        return portal_url

    async def get_session_user(self) -> dict[str, str]:
        if not self.session_id:
            raise ValueError("Session not initialized. Call v1.start_session() first.")

        response = await self._request("GET", f"/api/v1/session/{self.session_id}/user")
        if response.get("errors"):
            errors = response["errors"]
            message = (
                errors[0].get("message") if errors else "Failed to get session user"
            )
            raise ValueError(str(message))

        user_data = response.get("data")
        user_data_dict = user_data if isinstance(user_data, dict) else {}
        resolved_user_id = _read_session_field(user_data_dict, ("user_id", "userId"))
        if resolved_user_id:
            self.user_id = resolved_user_id

        return {
            "user_id": resolved_user_id,
            "company_id": self.company_id or "",
        }

    async def list_accounts(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
        include_sync_status: bool | None = None,
    ) -> FinaticResponse:
        return await self._request(
            "GET",
            "/api/v1/accounts",
            query=self._compact_query(
                {
                    "limit": limit,
                    "offset": offset,
                    "include_sync_status": include_sync_status,
                }
            ),
        )

    async def get_account(self, account_id: str) -> FinaticResponse:
        return await self._request("GET", f"/api/v1/accounts/{account_id}")

    async def list_account_resource(
        self,
        account_id: str,
        resource: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> FinaticResponse:
        self._validate_resource(resource)
        return await self._request(
            "GET",
            f"/api/v1/accounts/{account_id}/{resource}",
            query=self._compact_query({"limit": limit, "offset": offset}),
        )

    async def list_balances(
        self, account_id: str, *, limit: int | None = None, offset: int | None = None
    ) -> FinaticResponse:
        return await self.list_account_resource(
            account_id, "balances", limit=limit, offset=offset
        )

    async def list_positions(
        self, account_id: str, *, limit: int | None = None, offset: int | None = None
    ) -> FinaticResponse:
        return await self.list_account_resource(
            account_id, "positions", limit=limit, offset=offset
        )

    async def list_transactions(
        self, account_id: str, *, limit: int | None = None, offset: int | None = None
    ) -> FinaticResponse:
        return await self.list_account_resource(
            account_id, "transactions", limit=limit, offset=offset
        )

    async def list_orders(
        self, account_id: str, *, limit: int | None = None, offset: int | None = None
    ) -> FinaticResponse:
        return await self.list_account_resource(
            account_id, "orders", limit=limit, offset=offset
        )

    async def get_account_order(
        self, account_id: str, order_id: str
    ) -> FinaticResponse:
        return await self._request(
            "GET", f"/api/v1/accounts/{account_id}/orders/{order_id}"
        )

    async def get_account_order_fills(
        self, account_id: str, order_id: str
    ) -> FinaticResponse:
        return await self._request(
            "GET", f"/api/v1/accounts/{account_id}/orders/{order_id}/fills"
        )

    async def get_account_order_events(
        self, account_id: str, order_id: str
    ) -> FinaticResponse:
        return await self._request(
            "GET", f"/api/v1/accounts/{account_id}/orders/{order_id}/events"
        )

    async def create_account_order(
        self,
        account_id: str,
        order: dict[str, Any],
        *,
        idempotency_key: str,
    ) -> FinaticResponse:
        return await self._account_order_request(
            "POST", f"/api/v1/accounts/{account_id}/orders", order, idempotency_key
        )

    async def modify_account_order(
        self,
        account_id: str,
        order_id: str,
        order: dict[str, Any],
        *,
        idempotency_key: str,
    ) -> FinaticResponse:
        return await self._account_order_request(
            "PATCH",
            f"/api/v1/accounts/{account_id}/orders/{order_id}",
            order,
            idempotency_key,
        )

    async def cancel_account_order(
        self,
        account_id: str,
        order_id: str,
        *,
        idempotency_key: str,
    ) -> FinaticResponse:
        return await self._account_order_request(
            "DELETE",
            f"/api/v1/accounts/{account_id}/orders/{order_id}",
            None,
            idempotency_key,
        )

    async def list_account_grants(self) -> FinaticResponse:
        return await self._request("GET", "/api/v1/account-grants")

    async def get_account_grant(self, grant_id: str) -> FinaticResponse:
        return await self._request("GET", f"/api/v1/account-grants/{grant_id}")

    async def update_account_grant(
        self, grant_id: str, update: dict[str, Any]
    ) -> FinaticResponse:
        return await self._request(
            "PATCH", f"/api/v1/account-grants/{grant_id}", body=update
        )

    async def revoke_account_grant(self, grant_id: str) -> FinaticResponse:
        return await self._request("POST", f"/api/v1/account-grants/{grant_id}/revoke")

    async def get_webhook_catalog(self) -> FinaticResponse:
        return await self._request("GET", "/api/v1/webhooks/catalog")

    async def get_webhook_payload_schema(self) -> FinaticResponse:
        return await self._request("GET", "/api/v1/webhooks/payload-schema")

    async def list_webhook_subscriptions(
        self,
    ) -> FinaticResponse:
        return await self._request("GET", "/api/v1/webhooks/subscriptions")

    async def create_webhook_subscription(
        self, subscription: dict[str, Any]
    ) -> FinaticResponse:
        return await self._request(
            "POST", "/api/v1/webhooks/subscriptions", body=subscription
        )

    async def update_webhook_subscription(
        self, subscription_id: str, update: dict[str, Any]
    ) -> FinaticResponse:
        return await self._request(
            "PATCH",
            f"/api/v1/webhooks/subscriptions/{subscription_id}",
            body=update,
        )

    async def revoke_webhook_subscription(
        self, subscription_id: str
    ) -> FinaticResponse:
        return await self._request(
            "POST", f"/api/v1/webhooks/subscriptions/{subscription_id}/revoke"
        )

    async def _account_order_request(
        self,
        method: str,
        path: str,
        order: dict[str, Any] | None,
        idempotency_key: str,
    ) -> FinaticResponse:
        if not idempotency_key:
            raise ValueError("idempotency_key is required for account order commands")
        headers = {"Idempotency-Key": idempotency_key}
        body = {"order": order} if order is not None else None
        return await self._request(method, path, body=body, headers=headers)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> FinaticResponse:
        url = self._url(path, query)
        header_params = self._headers(headers)
        call_api = self.api_client.call_api
        if inspect.iscoroutinefunction(call_api):
            response = await call_api(
                method,
                url,
                header_params=header_params,
                body=body,
            )
        else:
            response = await asyncio.to_thread(
                call_api,
                method,
                url,
                header_params=header_params,
                body=body,
            )
        read = getattr(response, "read", None)
        if read is not None:
            if inspect.iscoroutinefunction(read):
                await read()
            else:
                await asyncio.to_thread(read)
        return self._deserialize_response(response)

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "X-API-Key": self.api_key,
            "X-Finatic-Environment": self.environment,
        }
        if self.session_id:
            headers["X-Session-ID"] = self.session_id
        if self.company_id:
            headers["X-Company-ID"] = self.company_id
        if self.authorization:
            headers["Authorization"] = self.authorization
        if self.csrf_token:
            headers["X-CSRF-Token"] = self.csrf_token
        if extra:
            headers.update({key: value for key, value in extra.items() if value})
        return headers

    def _url(self, path: str, query: dict[str, Any] | None = None) -> str:
        host = self.config.host.rstrip("/")
        url = f"{host}{path}"
        if query:
            url = f"{url}?{urlencode(query, doseq=True)}"
        return url

    def _deserialize_response(self, response: Any) -> FinaticResponse:
        status = getattr(response, "status", None)
        data = getattr(response, "data", None)
        headers = self._response_headers(response)
        if isinstance(data, bytes):
            payload: Any = json.loads(data.decode("utf-8")) if data else {}
        elif isinstance(data, str):
            payload = json.loads(data) if data else {}
        else:
            payload = data if data is not None else {}

        if isinstance(status, int) and not 200 <= status <= 299:
            return self._error_envelope(
                payload=payload,
                status=status,
                trace_id=self._trace_id(payload, headers),
            )

        return self._success_envelope(
            payload=payload,
            trace_id=self._trace_id(payload, headers),
        )

    def _success_envelope(self, payload: Any, trace_id: str | None) -> FinaticResponse:
        if isinstance(payload, dict) and (
            "traceId" in payload or "data" in payload or "errors" in payload
        ):
            envelope = dict(payload)
            if trace_id and not envelope.get("traceId"):
                envelope["traceId"] = trace_id
            envelope.setdefault("data", None)
            envelope.setdefault("warnings", [])
            envelope.setdefault("errors", [])
            return cast(FinaticResponse, envelope)

        if isinstance(payload, dict) and (
            "success" in payload or "error" in payload or "warning" in payload
        ):
            success = payload.get("success")
            data = success.get("data") if isinstance(success, dict) else None
            errors = self._errors_from_legacy_error(payload.get("error"))
            warnings = payload.get("warnings", payload.get("warning")) or []
            return cast(
                FinaticResponse,
                {
                    "traceId": self._trace_id(payload, None) or trace_id,
                    "data": data,
                    "warnings": warnings,
                    "errors": errors,
                },
            )

        return cast(
            FinaticResponse,
            {
                "traceId": trace_id,
                "data": payload,
                "warnings": [],
                "errors": [],
            },
        )

    def _error_envelope(
        self, *, payload: Any, status: int, trace_id: str | None
    ) -> FinaticResponse:
        if isinstance(payload, dict):
            error_payload = payload.get("error")
            errors_payload = payload.get("errors")
            if isinstance(errors_payload, list) and errors_payload:
                error = self._normalize_error(errors_payload[0], status)
            elif isinstance(error_payload, dict):
                error = self._normalize_error(error_payload, status)
            else:
                message = (
                    payload.get("message")
                    or payload.get("detail")
                    or payload.get("title")
                    or payload
                )
                error = {"message": str(message)}
            warnings = payload.get("warnings", payload.get("warning")) or []
        else:
            error = {"message": str(payload)}
            warnings = []

        error = self._normalize_error(error, status)

        return {
            "traceId": trace_id,
            "data": None,
            "warnings": warnings,
            "errors": [error],
        }

    def _errors_from_legacy_error(self, error: Any) -> list[dict[str, Any]]:
        if error is None:
            return []
        if isinstance(error, list):
            return [
                self._normalize_error(item, None)
                for item in error
                if isinstance(item, dict)
            ]
        if isinstance(error, dict):
            return [self._normalize_error(error, None)]
        return [self._normalize_error({"message": str(error)}, None)]

    def _normalize_error(self, error: Any, status: int | None) -> dict[str, Any]:
        if isinstance(error, dict):
            normalized = dict(error)
        else:
            normalized = {"message": str(error)}
        if status is not None:
            normalized["status"] = status
        category = normalized.get("category")
        code = normalized.get("code")
        if category not in _STABLE_ERROR_CODES:
            category = self._error_category_for_status(status, normalized)
            normalized["category"] = category
        if not isinstance(code, str) or not code:
            normalized["code"] = str(category)
        normalized.setdefault("message", "")
        return normalized

    def _error_category_for_status(
        self, status: int | None, error: dict[str, Any]
    ) -> str:
        raw_message = str(error.get("message", "")).lower()
        if "reauth" in raw_message or "re-authoriz" in raw_message:
            return "REAUTH_REQUIRED"
        if "provider" in raw_message or "broker" in raw_message:
            return "PROVIDER_ERROR"
        if status is None:
            return "INTERNAL"
        return _ERROR_CODE_BY_STATUS.get(status, "INTERNAL")

    def _trace_id(self, payload: Any, headers: Any) -> str | None:
        if isinstance(payload, dict):
            trace_id = (
                payload.get("traceId") or payload.get("trace_id") or payload.get("_id")
            )
            if isinstance(trace_id, str):
                return trace_id
        if headers is not None:
            for name in ("x-trace-id", "X-Trace-ID", "x-request-id", "X-Request-ID"):
                value = headers.get(name) if hasattr(headers, "get") else None
                if isinstance(value, str):
                    return value
        return None

    def _response_headers(self, response: Any) -> Any:
        headers = getattr(response, "headers", None)
        if headers is not None:
            return headers
        getheaders = getattr(response, "getheaders", None)
        if callable(getheaders):
            return getheaders()
        return None

    def _extract_data(self, response: FinaticResponse) -> Any:
        if isinstance(response, dict) and "data" in response:
            return response.get("data")
        success = response.get("success") if isinstance(response, dict) else None
        if isinstance(success, dict):
            return success.get("data")
        return None

    def _require_session_id(self) -> str:
        if not self.session_id:
            raise ValueError("Session not initialized. Call v1.start_session() first.")
        return self.session_id

    def _compact_query(self, query: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in query.items() if value is not None}

    def _validate_environment(self, environment: Environment) -> Environment:
        if environment not in {"live", "sandbox"}:
            raise ValueError("environment must be either 'live' or 'sandbox'")
        return environment

    def _validate_resource(self, resource: str) -> None:
        allowed = {
            "balances",
            "positions",
            "transactions",
            "orders",
        }
        if resource not in allowed:
            raise ValueError(f"Unsupported account resource: {resource}")
