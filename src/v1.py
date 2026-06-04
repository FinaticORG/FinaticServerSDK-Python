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
        user_id: str | None = None,
        device_info: dict[str, Any] | None = None,
    ) -> FinaticResponse:
        body: dict[str, Any] = {}
        if user_id is not None:
            body["user_id"] = user_id
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

    async def get_session_user(
        self, session_id: str | None = None
    ) -> FinaticResponse:
        resolved_session_id = session_id or self._require_session_id()
        return await self._request(
            "GET", f"/api/v1/sessions/{resolved_session_id}/user"
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

    async def revoke_account_grant(
        self, grant_id: str
    ) -> FinaticResponse:
        return await self._request("POST", f"/api/v1/account-grants/{grant_id}/revoke")

    async def list_consents(self) -> FinaticResponse:
        return await self._request("GET", "/api/v1/consents")

    async def get_consent(self, consent_id: str) -> FinaticResponse:
        return await self._request("GET", f"/api/v1/consents/{consent_id}")

    async def revoke_consent(self, consent_id: str) -> FinaticResponse:
        return await self._request("POST", f"/api/v1/consents/{consent_id}/revoke")

    async def get_webhook_catalog(self) -> FinaticResponse:
        return await self._request("GET", "/api/v1/webhooks")

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
        if isinstance(data, bytes):
            payload: Any = json.loads(data.decode("utf-8")) if data else {}
        elif isinstance(data, str):
            payload = json.loads(data) if data else {}
        else:
            payload = data if data is not None else {}

        if isinstance(status, int) and not 200 <= status <= 299:
            if isinstance(payload, dict):
                message = payload.get("message") or payload.get("detail") or payload
            else:
                message = payload
            return {
                "success": {"data": None, "meta": None},
                "error": {"message": str(message), "status": status},
                "warning": None,
            }

        return cast(FinaticResponse, payload)

    def _extract_data(self, response: FinaticResponse) -> Any:
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
