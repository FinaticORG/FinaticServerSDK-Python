"""Account-first v1 SDK facade.

This module is hand-maintained until the generated OpenAPI surface exposes
stable methods for every v1 SDK-audience route.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, cast
from urllib.parse import urlencode

from finatic_server.api_client import ApiClient
from finatic_server.configuration import Configuration

from .types import FinaticResponse

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


class V1Client:
    """Thin account-first v1 client over the generated transport."""

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

    def set_environment(self, environment: Environment) -> None:
        """Set the public v1 environment for subsequent requests."""
        self.environment = self._validate_environment(environment)

    def set_session_context(
        self,
        session_id: str,
        company_id: str | None = None,
        authorization: str | None = None,
    ) -> None:
        """Set session headers used by account-first v1 routes."""
        self.session_id = session_id
        self.company_id = company_id
        self.authorization = authorization

    async def create_session(
        self,
        *,
        device_info: dict[str, Any] | None = None,
    ) -> FinaticResponse:
        body: dict[str, Any] = {}
        if device_info is not None:
            body["device_info"] = device_info
        response = await self._request("POST", "/api/v1/sessions", body=body or None)
        session_data = self._extract_data(response)
        if isinstance(session_data, dict):
            session_id = session_data.get("session_id") or session_data.get("sessionId")
            company_id = session_data.get("company_id") or session_data.get("companyId")
            if isinstance(session_id, str):
                self.set_session_context(
                    session_id=session_id,
                    company_id=company_id if isinstance(company_id, str) else None,
                )
        return response

    async def get_session(self, session_id: str) -> FinaticResponse:
        return await self._request("GET", f"/api/v1/sessions/{session_id}")

    async def create_portal_link(
        self, session_id: str | None = None
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "POST", f"/api/v1/sessions/{resolved_session_id}/portal-links"
        )

    async def get_session_user(self, session_id: str | None = None) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "GET", f"/api/v1/sessions/{resolved_session_id}/user"
        )

    async def link_portal_user(
        self, user_id: str, session_id: str | None = None
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "POST",
            f"/api/v1/portal/{resolved_session_id}/user-link",
            body={"userId": user_id},
        )

    async def list_portal_institutions(
        self, session_id: str | None = None
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "GET", f"/api/v1/portal/{resolved_session_id}/institutions"
        )

    async def create_portal_auth_attempt(
        self, broker_id: str, session_id: str | None = None
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "POST",
            f"/api/v1/portal/{resolved_session_id}/auth-attempts",
            body={"brokerId": broker_id},
        )

    async def get_portal_auth_attempt(
        self, auth_attempt_id: str, session_id: str | None = None
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "GET",
            f"/api/v1/portal/{resolved_session_id}/auth-attempts/{auth_attempt_id}",
        )

    async def list_discovered_accounts(
        self, session_id: str | None = None
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "GET", f"/api/v1/portal/{resolved_session_id}/discovered-accounts"
        )

    async def create_portal_account_grant(
        self,
        grant: dict[str, Any],
        session_id: str | None = None,
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "POST",
            f"/api/v1/portal/{resolved_session_id}/account-grants",
            body=grant,
        )

    async def complete_portal_session(
        self, session_id: str | None = None
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "POST", f"/api/v1/portal/{resolved_session_id}/complete"
        )

    async def list_accounts(self) -> FinaticResponse:
        return await self._request("GET", "/api/v1/accounts")

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

    async def list_account_balances(
        self, account_id: str, **query: Any
    ) -> FinaticResponse:
        return await self.list_account_resource(account_id, "balances", **query)

    async def list_account_positions(
        self, account_id: str, **query: Any
    ) -> FinaticResponse:
        return await self.list_account_resource(account_id, "positions", **query)

    async def list_account_transactions(
        self, account_id: str, **query: Any
    ) -> FinaticResponse:
        return await self.list_account_resource(account_id, "transactions", **query)

    async def list_account_orders(
        self, account_id: str, **query: Any
    ) -> FinaticResponse:
        return await self.list_account_resource(account_id, "orders", **query)

    async def list_account_position_lots(
        self, account_id: str, **query: Any
    ) -> FinaticResponse:
        return await self.list_account_resource(account_id, "position-lots", **query)

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

    async def get_account_position_lot_fills(
        self, account_id: str, lot_id: str
    ) -> FinaticResponse:
        return await self._request(
            "GET", f"/api/v1/accounts/{account_id}/position-lots/{lot_id}/fills"
        )

    async def create_account_order(
        self,
        account_id: str,
        order: dict[str, Any],
        *,
        idempotency_key: str | None = None,
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
        idempotency_key: str | None = None,
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
        idempotency_key: str | None = None,
    ) -> FinaticResponse:
        return await self._account_order_request(
            "DELETE",
            f"/api/v1/accounts/{account_id}/orders/{order_id}",
            {"orderId": order_id},
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

    async def list_consents(self) -> FinaticResponse:
        return await self._request("GET", "/api/v1/consents")

    async def get_consent(self, consent_id: str) -> FinaticResponse:
        return await self._request("GET", f"/api/v1/consents/{consent_id}")

    async def revoke_consent(self, consent_id: str) -> FinaticResponse:
        return await self._request("POST", f"/api/v1/consents/{consent_id}/revoke")

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
        order: dict[str, Any],
        idempotency_key: str | None,
    ) -> FinaticResponse:
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return await self._request(method, path, body={"order": order}, headers=headers)

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
        response = await self.api_client.call_api(
            method,
            url,
            header_params=header_params,
            body=body,
        )
        if hasattr(response, "read"):
            await response.read()
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
        headers = getattr(response, "headers", None)
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

    def _extract_data(self, response: FinaticResponse) -> Any:
        if isinstance(response, dict) and "data" in response:
            return response.get("data")
        success = response.get("success") if isinstance(response, dict) else None
        if isinstance(success, dict):
            return success.get("data")
        return None

    def _require_session_id(self) -> str:
        if not self.session_id:
            raise ValueError("Session not initialized. Call v1.create_session() first.")
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
            "position-lots",
        }
        if resource not in allowed:
            raise ValueError(f"Unsupported account resource: {resource}")
