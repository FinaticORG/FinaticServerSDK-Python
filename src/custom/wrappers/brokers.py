"""
Custom brokers wrapper - Extends generated wrapper.

This file is protected and will not be overwritten during regeneration.
Add your custom brokers logic here.
"""

from typing import Optional, Any, Dict
from src.generated.wrappers.brokers import BrokersWrapper
from src.generated.configuration import Configuration


class CustomBrokersWrapper(BrokersWrapper):
    """Custom wrapper for brokers operations.

    Automatically adds session headers to all API requests.
    """

    def _unwrap_response(self, response: Any) -> Any:
        """Helper method to unwrap response consistently.

        Handles different response structures:
        - Double-wrapped: response.data.data
        - Single-wrapped: response.data
        - Already unwrapped: response
        """
        if hasattr(response, "data"):
            if hasattr(response.data, "data"):
                # Double-wrapped: response.data.data
                return response.data.data
            else:
                # Single-wrapped: response.data
                return response.data
        else:
            # Already unwrapped
            return response

    def _ensure_session_headers(self) -> None:
        """Helper method to ensure session headers are set on the configuration.

        This is called both from set_session_context and can be called before API calls.
        """
        if not self.session_id or not self.company_id:
            return  # No session context to set

        config = self.config
        api = self.api

        # Update wrapper's config
        if config and hasattr(config, "default_headers"):
            if not config.default_headers:
                config.default_headers = {}
            config.default_headers["x-session-id"] = self.session_id
            config.default_headers["x-company-id"] = self.company_id
            if self.csrf_token:
                config.default_headers["x-csrf-token"] = self.csrf_token

        # Update API instance's configuration if it has one
        if api and hasattr(api, "api_client") and hasattr(api.api_client, "default_headers"):
            if not api.api_client.default_headers:
                api.api_client.default_headers = {}
            api.api_client.default_headers["x-session-id"] = self.session_id
            api.api_client.default_headers["x-company-id"] = self.company_id
            if self.csrf_token:
                api.api_client.default_headers["x-csrf-token"] = self.csrf_token

    def set_session_context(self, session_id: str, company_id: str, csrf_token: str) -> None:
        """Override setSessionContext to automatically add session headers to all API requests.

        This ensures all broker endpoints include authentication headers without overriding each method.
        """
        # Call parent to store values
        super().set_session_context(session_id, company_id, csrf_token)

        # Ensure headers are set on configuration
        self._ensure_session_headers()

    def _get_session_headers(self, request_id: str) -> Dict[str, str]:
        """Helper to get session headers for API requests.

        This ensures headers are always included even if default_headers isn't working as expected.
        """
        if not self.session_id or not self.company_id:
            raise ValueError("Session context incomplete. Missing sessionId or companyId.")

        headers: Dict[str, str] = {
            "x-session-id": self.session_id,
            "x-company-id": self.company_id,
            "x-request-id": request_id,
        }
        if self.csrf_token:
            headers["x-csrf-token"] = self.csrf_token

        return headers

    async def get_orders(
        self,
        broker_id: Any = None,
        connection_id: Any = None,
        account_id: Any = None,
        symbol: Any = None,
        order_status: Any = None,
        side: Any = None,
        asset_type: Any = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        created_after: Any = None,
        created_before: Any = None,
        with_metadata: Optional[bool] = None,
    ) -> list:
        """Override getOrders to ensure session headers are included."""
        # Authentication check
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        request_id = self._generate_request_id()
        headers = self._get_session_headers(request_id)

        # Call the API directly with session headers explicitly included
        response = await self.api.get_orders_api_v1_brokers_data_orders_get(
            broker_id=broker_id,
            connection_id=connection_id,
            account_id=account_id,
            symbol=symbol,
            order_status=order_status,
            side=side,
            asset_type=asset_type,
            limit=limit,
            offset=offset,
            created_after=created_after,
            created_before=created_before,
            with_metadata=with_metadata,
            _headers=headers,
        )

        # Apply response interceptors (same as parent)
        from src.generated.utils.interceptors import apply_response_interceptors

        response = await apply_response_interceptors(response, self.sdk_config)

        # Unwrap response using helper method
        result = self._unwrap_response(response)
        return result if isinstance(result, list) else []

    async def get_accounts(
        self,
        broker_id: Any = None,
        connection_id: Any = None,
        account_type: Any = None,
        status: Any = None,
        currency: Any = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        with_metadata: Any = None,
    ) -> list:
        """Override getAccounts to ensure session headers are included."""
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        request_id = self._generate_request_id()
        headers = self._get_session_headers(request_id)

        response = await self.api.get_accounts_api_v1_brokers_data_accounts_get(
            broker_id=broker_id,
            connection_id=connection_id,
            account_type=account_type,
            status=status,
            currency=currency,
            limit=limit,
            offset=offset,
            with_metadata=with_metadata,
            _headers=headers,
        )

        from src.generated.utils.interceptors import apply_response_interceptors

        response = await apply_response_interceptors(response, self.sdk_config)

        if response and isinstance(response, dict) and "data" in response:
            if isinstance(response["data"], dict) and "data" in response["data"]:
                return response["data"]["data"]
            return response["data"]
        return response if isinstance(response, list) else []

    async def get_positions(
        self,
        broker_id: Any = None,
        connection_id: Any = None,
        account_id: Any = None,
        symbol: Any = None,
        side: Any = None,
        asset_type: Any = None,
        position_status: Any = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        updated_after: Any = None,
        updated_before: Any = None,
        with_metadata: Optional[bool] = None,
    ) -> list:
        """Override getPositions to ensure session headers are included."""
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        request_id = self._generate_request_id()
        headers = self._get_session_headers(request_id)

        response = await self.api.get_positions_api_v1_brokers_data_positions_get(
            broker_id=broker_id,
            connection_id=connection_id,
            account_id=account_id,
            symbol=symbol,
            side=side,
            asset_type=asset_type,
            position_status=position_status,
            limit=limit,
            offset=offset,
            updated_after=updated_after,
            updated_before=updated_before,
            with_metadata=with_metadata,
            _headers=headers,
        )

        from src.generated.utils.interceptors import apply_response_interceptors

        response = await apply_response_interceptors(response, self.sdk_config)

        if response and isinstance(response, dict) and "data" in response:
            if isinstance(response["data"], dict) and "data" in response["data"]:
                return response["data"]["data"]
            return response["data"]
        return response if isinstance(response, list) else []

    async def get_balances(
        self,
        broker_id: Any = None,
        connection_id: Any = None,
        account_id: Any = None,
        is_end_of_day_snapshot: Any = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        balance_created_after: Any = None,
        balance_created_before: Any = None,
        with_metadata: Optional[bool] = None,
    ) -> list:
        """Override getBalances to ensure session headers are included."""
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        request_id = self._generate_request_id()
        headers = self._get_session_headers(request_id)

        response = await self.api.get_balances_api_v1_brokers_data_balances_get(
            broker_id=broker_id,
            connection_id=connection_id,
            account_id=account_id,
            is_end_of_day_snapshot=is_end_of_day_snapshot,
            limit=limit,
            offset=offset,
            balance_created_after=balance_created_after,
            balance_created_before=balance_created_before,
            with_metadata=with_metadata,
            _headers=headers,
        )

        from src.generated.utils.interceptors import apply_response_interceptors

        response = await apply_response_interceptors(response, self.sdk_config)

        if response and isinstance(response, dict) and "data" in response:
            if isinstance(response["data"], dict) and "data" in response["data"]:
                return response["data"]["data"]
            return response["data"]
        return response if isinstance(response, list) else []

    async def list_broker_connections(self) -> list:
        """Override listBrokerConnections to ensure session headers are included."""
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        request_id = self._generate_request_id()
        headers = self._get_session_headers(request_id)

        response = await self.api.list_broker_connections_api_v1_brokers_connections_get(
            _headers=headers
        )

        from src.generated.utils.interceptors import apply_response_interceptors

        response = await apply_response_interceptors(response, self.sdk_config)

        if response and isinstance(response, dict) and "data" in response:
            if isinstance(response["data"], dict) and "data" in response["data"]:
                return response["data"]["data"]
            return response["data"]
        return response if isinstance(response, list) else []
