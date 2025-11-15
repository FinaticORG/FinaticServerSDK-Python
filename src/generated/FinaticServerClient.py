"""
Main client class for Finatic Server SDK (Python).

This file is regenerated on each run - do not edit directly.
For custom logic, extend this class or use custom wrappers.
"""

from typing import Optional, Dict, Any, List
from .configuration import Configuration
from .config import SdkConfig, get_config
from .utils.url_utils import append_theme_to_url, append_broker_filter_to_url
from .models.session_start_request import SessionStartRequest

from .api.brokers_api import BrokersApi
from .api.market_data_api import MarketDataApi
from .api.session_api import SessionApi

from .wrappers.brokers import BrokersWrapper
from .wrappers.market_data import MarketDataWrapper
from .wrappers.session import SessionWrapper


class FinaticServerClient:
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

        self.brokers = BrokersWrapper(
            BrokersApi(self.config), self.config, self.sdk_config
        )
        self.market_data = MarketDataWrapper(
            MarketDataApi(self.config), self.config, self.sdk_config
        )
        self.session = SessionWrapper(
            SessionApi(self.config), self.config, self.sdk_config
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
        self.market_data.set_session_context(session_id, company_id, csrf_token)
        self.session.set_session_context(session_id, company_id, csrf_token)

    def get_session_id(self) -> Optional[str]:
        """Get current session ID."""
        return self.session_id

    def get_company_id(self) -> Optional[str]:
        """Get current company ID."""
        return self.company_id

    async def init_session(self, x_api_key: str) -> str:
        """Initialize a session by getting a one-time token.

        Args:
            x_api_key: Company API key

        Returns:
            One-time token
        """
        response = await self.session.init_session(x_api_key)
        return response.one_time_token or ""

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
            one_time_token, session_start_request
        )
        session_id = response.session_id or ""
        company_id = response.company_id or ""

        # Note: csrf_token is not available in SessionResponseData
        # It should be obtained from session context or another source if needed
        csrf_token = ""

        if session_id and company_id:
            self.set_session_context(session_id, company_id, csrf_token)

        return {"session_id": session_id, "company_id": company_id}

    async def get_portal_url(
        self,
        theme: Optional[str | Dict[str, Any]] = None,
        brokers: Optional[List[str]] = None,
        email: Optional[str] = None,
    ) -> str:
        """Get portal URL with optional theme and broker filters.

        This is where URL manipulation happens (not in session wrapper).
        Returns the URL - app can use it as needed.

        Args:
            theme: Optional theme configuration (preset string or custom dict)
            brokers: Optional list of broker names/IDs to filter
            email: Optional email for pre-filling

        Returns:
            Portal URL with all parameters appended
        """
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # Get raw portal URL from session wrapper (requires session_id parameter)
        response = await self.session.get_portal_url(self.session_id)
        portal_url = response.portal_url or ""

        # Append theme if provided
        if theme:
            portal_url = append_theme_to_url(portal_url, theme)

        # Append broker filter if provided
        if brokers:
            portal_url = append_broker_filter_to_url(portal_url, brokers)

        # Append email if provided
        if email:
            from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

            parsed = urlparse(portal_url)
            query_params = parse_qs(parsed.query)
            query_params["email"] = [email]
            new_query = urlencode(query_params, doseq=True)
            new_parsed = parsed._replace(query=new_query)
            portal_url = urlunparse(new_parsed)

        # Add session ID and company ID to URL
        from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

        parsed = urlparse(portal_url)
        query_params = parse_qs(parsed.query)
        if self.session_id:
            query_params["session_id"] = [self.session_id]
        if self.company_id:
            query_params["company_id"] = [self.company_id]
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        portal_url = urlunparse(new_parsed)

        return portal_url

    async def get_session_user(self) -> Dict[str, str]:
        """Get session user information after portal authentication.

        Returns:
            Dictionary with user_id, company_id, and token_type
        """
        if not self.session_id or not self.company_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # get_session_user requires both company_id and session_id (in that order)
        response = await self.session.get_session_user(self.company_id, self.session_id)
        return {
            "user_id": response.user_id or "",
            "company_id": response.company_id or self.company_id or "",
            "token_type": response.token_type or "Bearer",
        }

    async def get_broker_list(self) -> List[Any]:
        """Get list of supported brokers."""
        return await self.brokers.get_brokers()

    async def get_broker_connections(self) -> List[Any]:
        """Get user's broker connections."""
        return await self.brokers.list_broker_connections()

    async def get_all_accounts(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get all accounts across all pages."""
        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            result = await self.brokers.get_accounts(limit=limit, offset=offset)
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
        """Get all orders across all pages."""
        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            result = await self.brokers.get_orders(
                symbol=filter.get("symbol") if filter else None,
                order_status=filter.get("order_status") if filter else None,
                side=filter.get("side") if filter else None,
                asset_type=filter.get("asset_type") if filter else None,
                limit=limit,
                offset=offset,
            )
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
        """Get all positions across all pages."""
        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            result = await self.brokers.get_positions(
                symbol=filter.get("symbol") if filter else None,
                side=filter.get("side") if filter else None,
                asset_type=filter.get("asset_type") if filter else None,
                position_status=filter.get("position_status") if filter else None,
                limit=limit,
                offset=offset,
            )
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
        """Get all balances across all pages."""
        all_data: List[Any] = []
        offset = 0
        limit = 100

        while True:
            result = await self.brokers.get_balances(
                is_end_of_day_snapshot=(
                    filter.get("is_end_of_day_snapshot") if filter else None
                ),
                limit=limit,
                offset=offset,
            )
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
        """Get paginated accounts."""
        offset = (page - 1) * per_page
        return await self.brokers.get_accounts(limit=per_page, offset=offset)

    async def get_orders(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated orders."""
        offset = (page - 1) * per_page
        return await self.brokers.get_orders(
            symbol=filter.get("symbol") if filter else None,
            order_status=filter.get("order_status") if filter else None,
            side=filter.get("side") if filter else None,
            asset_type=filter.get("asset_type") if filter else None,
            limit=per_page,
            offset=offset,
        )

    async def get_positions(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated positions."""
        offset = (page - 1) * per_page
        return await self.brokers.get_positions(
            symbol=filter.get("symbol") if filter else None,
            side=filter.get("side") if filter else None,
            asset_type=filter.get("asset_type") if filter else None,
            position_status=filter.get("position_status") if filter else None,
            limit=per_page,
            offset=offset,
        )

    async def get_balances(
        self,
        page: int = 1,
        per_page: int = 100,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Get paginated balances."""
        offset = (page - 1) * per_page
        return await self.brokers.get_balances(
            is_end_of_day_snapshot=(
                filter.get("is_end_of_day_snapshot") if filter else None
            ),
            limit=per_page,
            offset=offset,
        )

    async def get_open_positions(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get only open positions."""
        merged_filter = {**(filter or {}), "position_status": "open"}
        return await self.get_all_positions(merged_filter)

    async def get_filled_orders(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get only filled orders."""
        merged_filter = {**(filter or {}), "order_status": "filled"}
        return await self.get_all_orders(merged_filter)

    async def get_pending_orders(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get only pending orders."""
        merged_filter = {**(filter or {}), "order_status": "pending"}
        return await self.get_all_orders(merged_filter)

    async def get_active_accounts(
        self, filter: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """Get only active accounts."""
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
