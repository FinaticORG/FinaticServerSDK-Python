"""
Main client class for Finatic Server SDK (Python).

This file is regenerated on each run - do not edit directly.
For custom logic, extend this class or use custom wrappers.
"""

from typing import Any, Dict, List, Optional

from .api.brokers_api import BrokersApi
from .api.session_api import SessionApi
from .api_client import ApiClient
from .config import SdkConfig, get_config
from .configuration import Configuration
from .models.session_start_request import SessionStartRequest
from .utils.logger import get_logger
from .utils.url_utils import append_broker_filter_to_url, append_theme_to_url
from .wrappers.brokers import BrokersWrapper
from .wrappers.session import InitSessionParams, SessionWrapper, StartSessionParams


class FinaticServer:
    """Main client class for Finatic Server SDK."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        sdk_config: Optional[SdkConfig] = None,
    ):
        """Initialize the client.

        Args:
            api_key: Company API key
            base_url: Base URL for API (defaults to https://api.finatic.dev)
            sdk_config: Optional SDK configuration overrides
        """
        self.config = Configuration(
            host=base_url or "https://api.finatic.dev",
            api_key={"X-API-Key": api_key},
        )
        # Create ApiClient from Configuration for API classes
        self.api_client = ApiClient(self.config)
        # Merge sdk_config with defaults
        if sdk_config:
            default = get_config()
            # If sdk_config is a SdkConfig instance, merge its attributes
            if isinstance(sdk_config, SdkConfig):
                for key in sdk_config.__dataclass_fields__:
                    if hasattr(sdk_config, key):
                        setattr(default, key, getattr(sdk_config, key))
            # If it's a dict, merge the values
            elif isinstance(sdk_config, dict):
                for key, value in sdk_config.items():
                    if hasattr(default, key):
                        setattr(default, key, value)
            self.sdk_config = default
        else:
            self.sdk_config = get_config()

        self.session_id: Optional[str] = None
        self.company_id: Optional[str] = None
        self.csrf_token: Optional[str] = None
        self.user_id: Optional[str] = None

        # Initialize logger
        self.logger = get_logger(self.sdk_config)

        self.brokers = BrokersWrapper(
            BrokersApi(self.api_client), self.config, self.sdk_config
        )
        self.session = SessionWrapper(
            SessionApi(self.api_client), self.config, self.sdk_config
        )

    async def initialize(self) -> None:
        """Initialize the client (no-op for now, can be extended)."""
        pass

    async def close(self) -> None:
        """Close the client and cleanup resources."""
        pass

    def set_session_context(
        self, session_id: str, company_id: str, csrf_token: str
    ) -> None:
        """Set session context for all wrappers.

        Args:
            session_id: Session ID
            company_id: Company ID
            csrf_token: CSRF token
        """
        self.session_id = session_id
        self.company_id = company_id
        self.csrf_token = csrf_token

        # Update all wrappers with session context
        self.brokers.set_session_context(session_id, company_id, csrf_token)
        self.session.set_session_context(session_id, company_id, csrf_token)

    def get_session_id(self) -> Optional[str]:
        """Get current session ID."""
        return self.session_id

    def get_company_id(self) -> Optional[str]:
        """Get current company ID."""
        return self.company_id

    def get_user_id(self) -> Optional[str]:
        """Get current user ID (set after portal authentication)."""
        return self.user_id

    async def _init_session(self, x_api_key: str) -> str:
        """Initialize a session by getting a one-time token (internal/private).

        Args:
            x_api_key: Company API key

        Returns:
            One-time token
        """
        response = await self.session.init_session(
            InitSessionParams(x_api_key=x_api_key)
        )
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to initialize session")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return (
            response.success.get("data", {}).get("one_time_token", "")
            if response.success and isinstance(response.success, dict)
            else ""
        )

    async def start_session(
        self, one_time_token: str, user_id: Optional[str] = None
    ) -> Dict[str, str]:
        """Start a session with a one-time token.

        Args:
            one_time_token: One-time token from init_session
            user_id: Optional user ID for direct authentication

        Returns:
            Dictionary with session_id and company_id
        """
        # Create SessionStartRequest with optional user_id
        session_start_request = (
            SessionStartRequest(user_id=user_id) if user_id else SessionStartRequest()
        )
        response = await self.session.start_session(
            StartSessionParams(
                one_time_token=one_time_token,
                session_start_request=session_start_request,
            )
        )
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to start session")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        session_data = (
            response.success.get("data", {})
            if response.success and isinstance(response.success, dict)
            else {}
        )
        session_id = (
            session_data.get("session_id", "") if isinstance(session_data, dict) else ""
        )
        company_id = (
            session_data.get("company_id", "") if isinstance(session_data, dict) else ""
        )

        # Note: csrf_token is not available in SessionResponseData
        # It should be obtained from session context or another source if needed
        csrf_token = ""

        if session_id and company_id:
            self.set_session_context(session_id, company_id, csrf_token)

        return {"session_id": session_id, "company_id": company_id}

    async def init_session(
        self, api_key: Optional[str] = None, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Convenience method that combines init_session and start_session (Phase 2C).

        This method:
        1. Gets a one-time token using the API key
        2. Starts a session with that token
        3. Sets the session context automatically
        4. Returns success/error information

        Args:
            api_key: Company API key (uses instance API key if not provided)
            user_id: Optional user ID for direct authentication

        Returns:
            Dictionary with:
            - success: bool - Whether the session was initialized successfully
            - session_id: str | None - Session ID if successful
            - company_id: str | None - Company ID if successful
            - error: str | None - Error message if failed
        """
        try:
            # Use provided API key or fall back to instance API key
            key_to_use = api_key or (
                self.config.api_key.get("X-API-Key") if self.config.api_key else None
            )
            if not key_to_use:
                return {
                    "success": False,
                    "session_id": None,
                    "company_id": None,
                    "error": "API key is required",
                }

            # Step 1: Get one-time token
            one_time_token = await self._init_session(key_to_use)

            if not one_time_token or not isinstance(one_time_token, str):
                return {
                    "success": False,
                    "session_id": None,
                    "company_id": None,
                    "error": "Failed to get one-time token",
                }

            # Step 2: Start session with the token
            session_result = await self.start_session(one_time_token, user_id)

            session_id = (
                session_result.get("session_id")
                if isinstance(session_result, dict)
                else None
            )
            company_id = (
                session_result.get("company_id")
                if isinstance(session_result, dict)
                else None
            )

            return {
                "success": True,
                "session_id": session_id,
                "company_id": company_id,
                "error": None,
            }
        except Exception as e:
            return {
                "success": False,
                "session_id": None,
                "company_id": None,
                "error": str(e),
            }

    async def get_portal_url(
        self,
        theme: Optional[str | Dict[str, Any]] = None,
        brokers: Optional[List[str]] = None,
        email: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> str:
        """Get portal URL with optional theme, broker filters, email, and mode.

        This is where URL manipulation happens (not in session wrapper).
        Returns the URL - app can use it as needed.

        Args:
            theme: Optional theme configuration (preset string or custom dict)
            brokers: Optional list of broker names/IDs to filter
            email: Optional email for pre-filling
            mode: Optional mode ('light' or 'dark')

        Returns:
            Portal URL with all parameters appended
        """
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # Get raw portal URL from session wrapper (requires GetPortalUrlParams object)
        from .wrappers.session import GetPortalUrlParams

        response = await self.session.get_portal_url(GetPortalUrlParams())

        # Check for errors
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get portal URL")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            self.logger.error(
                "Failed to get portal URL",
                extra={
                    "error": error_msg,
                    "code": (
                        response.Error.get("code")
                        if isinstance(response.Error, dict)
                        else None
                    ),
                    "status": (
                        response.Error.get("status")
                        if isinstance(response.Error, dict)
                        else None
                    ),
                },
            )
            raise Exception(error_msg)

        # Extract portal URL from standard response structure
        if response.success and isinstance(response.success, dict):
            data = response.success.get("data", {})
            portal_url = data.get("portal_url", "") if isinstance(data, dict) else ""
        else:
            self.logger.error("Invalid portal URL response: missing data", extra={})
            raise ValueError("Invalid portal URL response: missing portal_url")

        if not portal_url:
            self.logger.error("Empty portal URL from API", extra={})
            raise ValueError("Empty portal URL received from API")

        # Validate URL before manipulation
        from urllib.parse import urlparse

        try:
            parsed = urlparse(portal_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid portal URL format: {portal_url}")
        except Exception as e:
            self.logger.error(
                "Invalid portal URL from API",
                extra={"portal_url": portal_url, "error": str(e)},
            )
            raise ValueError(f"Invalid portal URL received from API: {portal_url}")

        # Append theme if provided
        if theme:
            portal_url = append_theme_to_url(portal_url, theme)

        # Append broker filter if provided
        if brokers:
            portal_url = append_broker_filter_to_url(portal_url, brokers)

        # Append email if provided
        if email:
            from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

            parsed = urlparse(portal_url)
            query_params = parse_qs(parsed.query)
            query_params["email"] = [email]
            new_query = urlencode(query_params, doseq=True)
            new_parsed = parsed._replace(query=new_query)
            portal_url = urlunparse(new_parsed)

        # Append mode if provided (light or dark)
        if mode:
            from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

            parsed = urlparse(portal_url)
            query_params = parse_qs(parsed.query)
            query_params["mode"] = [mode]
            new_query = urlencode(query_params, doseq=True)
            new_parsed = parsed._replace(query=new_query)
            portal_url = urlunparse(new_parsed)

        # Add session ID and company ID to URL
        from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

        parsed = urlparse(portal_url)
        query_params = parse_qs(parsed.query)
        if self.session_id:
            query_params["session_id"] = [self.session_id]
        if self.company_id:
            query_params["company_id"] = [self.company_id]
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        portal_url = urlunparse(new_parsed)

        self.logger.debug("Portal URL generated", extra={"portal_url": portal_url})
        return portal_url

    async def get_session_user(self) -> Dict[str, str]:
        """Get session user information after portal authentication.

        Returns:
            Dictionary with user_id, company_id, and token_type
        """
        if not self.session_id or not self.company_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # get_session_user uses session_id in the path and company_id from session context
        from .wrappers.session import GetSessionUserParams

        response = await self.session.get_session_user(
            GetSessionUserParams(session_id=self.session_id)
        )

        # Extract data from standard response structure
        if response.success and isinstance(response.success, dict):
            data = response.success.get("data", {})
            user_id = data.get("user_id", "") if isinstance(data, dict) else ""
            company_id = (
                data.get("company_id", self.company_id or "")
                if isinstance(data, dict)
                else (self.company_id or "")
            )
        else:
            user_id = ""
            company_id = self.company_id or ""

        # Store user_id for get_user_id() method
        if user_id:
            self.user_id = user_id

        # Extract token_type from data if available, otherwise default to 'Bearer'
        token_type = (
            data.get("token_type", "Bearer") if isinstance(data, dict) else "Bearer"
        )

        return {
            "user_id": user_id,
            "company_id": company_id,
            "token_type": token_type,
        }

    # Phase 2C: _convert_to_dict removed - now handled in generated methods via convert_to_plain_object utility

    async def get_broker_list(self) -> List[Any]:
        """Get list of supported brokers.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetBrokersParams

        response = await self.brokers.get_brokers(GetBrokersParams())
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get broker list")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_broker_connections(self) -> List[Any]:
        """Get user's broker connections.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import ListBrokerConnectionsParams

        response = await self.brokers.list_broker_connections(
            ListBrokerConnectionsParams()
        )
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get broker connections")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_all_accounts(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get all accounts across all pages.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetAccountsParams

        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            params = GetAccountsParams(limit=limit, offset=offset)
            response = await self.brokers.get_accounts(params)
            if response.Error:
                error_msg = (
                    response.Error.get("message", "Failed to get accounts")
                    if isinstance(response.Error, dict)
                    else str(response.Error)
                )
                raise Exception(error_msg)
            result = response.success.get("data", []) if response.success else []
            if not result or len(result) == 0:
                break
            all_data.extend(result)
            if len(result) < limit:
                break
            offset += limit

        return all_data

    async def get_all_orders(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get all orders across all pages.

        Phase 2C: Uses typed input objects and handles standard response structure.
        Enum coercion happens automatically via typed input objects.
        """
        from ..generated.wrappers.brokers import GetOrdersParams

        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            params = GetOrdersParams(
                symbol=filter.get("symbol") if filter else None,
                order_status=(
                    filter.get("order_status") if filter else None
                ),  # Will be coerced to enum
                side=filter.get("side") if filter else None,  # Will be coerced to enum
                asset_type=(
                    filter.get("asset_type") if filter else None
                ),  # Will be coerced to enum
                limit=limit,
                offset=offset,
            )
            response = await self.brokers.get_orders(params)
            result = response.success.get("data", []) if response.success else []
            if not result or len(result) == 0:
                break
            all_data.extend(result)
            if len(result) < limit:
                break
            offset += limit

        return all_data

    async def get_all_positions(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get all positions across all pages.

        Phase 2C: Uses typed input objects and handles standard response structure.
        Enum coercion happens automatically via typed input objects.
        """
        from ..generated.wrappers.brokers import GetPositionsParams

        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            params = GetPositionsParams(
                symbol=filter.get("symbol") if filter else None,
                side=filter.get("side") if filter else None,  # Will be coerced to enum
                asset_type=(
                    filter.get("asset_type") if filter else None
                ),  # Will be coerced to enum
                position_status=(
                    filter.get("position_status") if filter else None
                ),  # Will be coerced to enum
                limit=limit,
                offset=offset,
            )
            response = await self.brokers.get_positions(params)
            result = response.success.get("data", []) if response.success else []
            if not result or len(result) == 0:
                break
            all_data.extend(result)
            if len(result) < limit:
                break
            offset += limit

        return all_data

    async def get_all_balances(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get all balances across all pages.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetBalancesParams

        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            params = GetBalancesParams(
                is_end_of_day_snapshot=(
                    filter.get("is_end_of_day_snapshot") if filter else None
                ),
                limit=limit,
                offset=offset,
            )
            response = await self.brokers.get_balances(params)
            result = response.success.get("data", []) if response.success else []
            if not result or len(result) == 0:
                break
            all_data.extend(result)
            if len(result) < limit:
                break
            offset += limit

        return all_data

    async def get_accounts(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated accounts.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetAccountsParams

        offset = (page - 1) * per_page
        params = GetAccountsParams(limit=per_page, offset=offset)
        response = await self.brokers.get_accounts(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get accounts")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_orders(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated orders.

        Phase 2C: Uses typed input objects and handles standard response structure.
        Enum coercion happens automatically via typed input objects.
        """
        from ..generated.wrappers.brokers import GetOrdersParams

        offset = (page - 1) * per_page
        params = GetOrdersParams(
            symbol=filter.get("symbol") if filter else None,
            order_status=(
                filter.get("order_status") if filter else None
            ),  # Will be coerced to enum
            side=filter.get("side") if filter else None,  # Will be coerced to enum
            asset_type=(
                filter.get("asset_type") if filter else None
            ),  # Will be coerced to enum
            limit=per_page,
            offset=offset,
        )
        response = await self.brokers.get_orders(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get orders")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_positions(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated positions.

        Phase 2C: Uses typed input objects and handles standard response structure.
        Enum coercion happens automatically via typed input objects.
        """
        from ..generated.wrappers.brokers import GetPositionsParams

        offset = (page - 1) * per_page
        params = GetPositionsParams(
            symbol=filter.get("symbol") if filter else None,
            side=filter.get("side") if filter else None,  # Will be coerced to enum
            asset_type=(
                filter.get("asset_type") if filter else None
            ),  # Will be coerced to enum
            position_status=(
                filter.get("position_status") if filter else None
            ),  # Will be coerced to enum
            limit=per_page,
            offset=offset,
        )
        response = await self.brokers.get_positions(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get positions")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_balances(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated balances.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetBalancesParams

        offset = (page - 1) * per_page
        params = GetBalancesParams(
            is_end_of_day_snapshot=(
                filter.get("is_end_of_day_snapshot") if filter else None
            ),
            limit=per_page,
            offset=offset,
        )
        response = await self.brokers.get_balances(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get balances")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_open_positions(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get only open positions.

        Phase 2C: Uses enum coercion (case-insensitive string matching).
        """
        merged_filter = {**(filter or {}), "position_status": "active"}
        return await self.get_all_positions(merged_filter)

    async def get_filled_orders(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get only filled orders.

        Phase 2C: Uses enum coercion (case-insensitive string matching).
        """
        merged_filter = {**(filter or {}), "order_status": "filled"}
        return await self.get_all_orders(merged_filter)

    async def get_pending_orders(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get only pending orders.

        Phase 2C: Uses enum coercion (case-insensitive string matching).
        """
        merged_filter = {**(filter or {}), "order_status": "new"}
        return await self.get_all_orders(merged_filter)

    async def get_active_accounts(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get only active accounts.

        Phase 2C: Uses enum coercion (case-insensitive string matching).
        """
        merged_filter = {**(filter or {}), "status": "active"}
        return await self.get_all_accounts(merged_filter)

    async def get_orders_by_symbol(
        self, symbol: str, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get orders filtered by symbol."""
        merged_filter = {**(filter or {}), "symbol": symbol}
        return await self.get_all_orders(merged_filter)

    async def get_positions_by_symbol(
        self, symbol: str, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get positions filtered by symbol."""
        merged_filter = {**(filter or {}), "symbol": symbol}
        return await self.get_all_positions(merged_filter)

    async def get_orders_by_broker(
        self, broker_id: str, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get orders filtered by broker."""
        merged_filter = {**(filter or {}), "broker_id": broker_id}
        return await self.get_all_orders(merged_filter)

    async def get_positions_by_broker(
        self, broker_id: str, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get positions filtered by broker."""
        merged_filter = {**(filter or {}), "broker_id": broker_id}
        return await self.get_all_positions(merged_filter)

    async def get_all_order_groups(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get all order groups across all pages.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetOrderGroupsParams

        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            params = GetOrderGroupsParams(
                broker_id=filter.get("broker_id") if filter else None,
                connection_id=filter.get("connection_id") if filter else None,
                limit=limit,
                offset=offset,
                created_after=filter.get("created_after") if filter else None,
                created_before=filter.get("created_before") if filter else None,
            )
            response = await self.brokers.get_order_groups(params)
            result = response.success.get("data", []) if response.success else []
            if not result or len(result) == 0:
                break
            all_data.extend(result)
            if len(result) < limit:
                break
            offset += limit

        return all_data

    async def get_order_groups(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated order groups.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetOrderGroupsParams

        offset = (page - 1) * per_page
        params = GetOrderGroupsParams(
            broker_id=filter.get("broker_id") if filter else None,
            connection_id=filter.get("connection_id") if filter else None,
            limit=per_page,
            offset=offset,
            created_after=filter.get("created_after") if filter else None,
            created_before=filter.get("created_before") if filter else None,
        )
        response = await self.brokers.get_order_groups(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get order groups")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_all_position_lots(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get all position lots across all pages.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetPositionLotsParams

        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            params = GetPositionLotsParams(
                broker_id=filter.get("broker_id") if filter else None,
                connection_id=filter.get("connection_id") if filter else None,
                account_id=filter.get("account_id") if filter else None,
                symbol=filter.get("symbol") if filter else None,
                position_id=filter.get("position_id") if filter else None,
                limit=limit,
                offset=offset,
            )
            response = await self.brokers.get_position_lots(params)
            result = response.success.get("data", []) if response.success else []
            if not result or len(result) == 0:
                break
            all_data.extend(result)
            if len(result) < limit:
                break
            offset += limit

        return all_data

    async def get_position_lots(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated position lots.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetPositionLotsParams

        offset = (page - 1) * per_page
        params = GetPositionLotsParams(
            broker_id=filter.get("broker_id") if filter else None,
            connection_id=filter.get("connection_id") if filter else None,
            account_id=filter.get("account_id") if filter else None,
            symbol=filter.get("symbol") if filter else None,
            position_id=filter.get("position_id") if filter else None,
            limit=per_page,
            offset=offset,
        )
        response = await self.brokers.get_position_lots(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get position lots")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def disconnect_company(self, connection_id: str) -> Any:
        """Disconnect company from broker.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import DisconnectCompanyFromBrokerParams

        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")
        params = DisconnectCompanyFromBrokerParams(connection_id=connection_id)
        response = await self.brokers.disconnect_company_from_broker(params)
        return response.success.get("data") if response.success else None

    async def get_order_fills(
        self,
        order_id: str,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Get order fills for a specific order.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetOrderFillsParams

        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")
        offset = (page - 1) * per_page
        params = GetOrderFillsParams(
            order_id=order_id,
            connection_id=filter.get("connection_id") if filter else None,
            limit=per_page,
            offset=offset,
        )
        response = await self.brokers.get_order_fills(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get order fills")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_order_events(
        self,
        order_id: str,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Get order events for a specific order.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetOrderEventsParams

        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")
        offset = (page - 1) * per_page
        params = GetOrderEventsParams(
            order_id=order_id,
            connection_id=filter.get("connection_id") if filter else None,
            limit=per_page,
            offset=offset,
        )
        response = await self.brokers.get_order_events(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get order events")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def get_position_lot_fills(
        self,
        lot_id: str,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Get position lot fills for a specific lot.

        Phase 2C: Uses typed input objects and handles standard response structure.
        """
        from ..generated.wrappers.brokers import GetPositionLotFillsParams

        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")
        offset = (page - 1) * per_page
        params = GetPositionLotFillsParams(
            lot_id=lot_id,
            connection_id=filter.get("connection_id") if filter else None,
            limit=per_page,
            offset=offset,
        )
        response = await self.brokers.get_position_lot_fills(params)
        if response.Error:
            error_msg = (
                response.Error.get("message", "Failed to get position lot fills")
                if isinstance(response.Error, dict)
                else str(response.Error)
            )
            raise Exception(error_msg)
        return response.success.get("data", []) if response.success else []

    async def place_stock_market_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place a stock market order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Market",
            "asset_type": "equity",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": "day",
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
        }
        return await self.brokers.place_order(order_params)

    async def place_stock_limit_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        price: float,
        time_in_force: str = "gtc",
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place a stock limit order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Limit",
            "asset_type": "equity",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": time_in_force,
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
            "price": price,
        }
        return await self.brokers.place_order(order_params)

    async def place_stock_stop_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        stop_price: float,
        time_in_force: str = "gtc",
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place a stock stop order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Stop",
            "asset_type": "equity",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": time_in_force,
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
            "stop_price": stop_price,
        }
        return await self.brokers.place_order(order_params)

    async def place_crypto_market_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place a crypto market order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Market",
            "asset_type": "crypto",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": "day",
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
        }
        return await self.brokers.place_order(order_params)

    async def place_crypto_limit_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        price: float,
        time_in_force: str = "gtc",
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place a crypto limit order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Limit",
            "asset_type": "crypto",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": time_in_force,
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
            "price": price,
        }
        return await self.brokers.place_order(order_params)

    async def place_options_market_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place an options market order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Market",
            "asset_type": "equity_option",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": "day",
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
        }
        return await self.brokers.place_order(order_params)

    async def place_options_limit_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        price: float,
        time_in_force: str = "gtc",
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place an options limit order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Limit",
            "asset_type": "equity_option",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": time_in_force,
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
            "price": price,
        }
        return await self.brokers.place_order(order_params)

    async def place_futures_market_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place a futures market order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Market",
            "asset_type": "future",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": "day",
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
        }
        return await self.brokers.place_order(order_params)

    async def place_futures_limit_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        price: float,
        time_in_force: str = "gtc",
        broker: Optional[str] = None,
        account_number: Optional[str] = None,
    ) -> Any:
        """Place a futures limit order."""
        order_params: Dict[str, Any] = {
            "broker": broker or "robinhood",
            "order_type": "Limit",
            "asset_type": "future",
            "action": "Buy" if side == "buy" else "Sell",
            "time_in_force": time_in_force,
            "account_number": account_number or "",
            "symbol": symbol,
            "order_qty": quantity,
            "price": price,
        }
        return await self.brokers.place_order(order_params)

    async def place_order(
        self, order_params: Dict[str, Any], extras: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Place a generic order."""
        return await self.brokers.place_order(order_params, extras)

    async def modify_order(
        self,
        order_id: str,
        order_params: Dict[str, Any],
        extras: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Modify an existing order."""
        return await self.brokers.modify_order(order_id, order_params, extras)

    async def cancel_order(
        self,
        order_id: str,
        account_number: Optional[str] = None,
        connection_id: Optional[str] = None,
    ) -> Any:
        """Cancel an existing order."""
        # cancel_order signature: (order_id, cancel_order_request=None, account_number=None, connection_id=None)
        return await self.brokers.cancel_order(
            order_id, None, account_number, connection_id
        )
