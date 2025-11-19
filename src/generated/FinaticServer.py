"""
Main client class for Finatic Server SDK (Python).

This file is regenerated on each run - do not edit directly.
For custom logic, extend this class or use custom wrappers.
"""

from __future__ import annotations

from typing import Optional, Dict, Any, List, Union
from .configuration import Configuration
from .api_client import ApiClient
from .config import SdkConfig, get_config
from .types import FinaticResponse
from .utils.url_utils import append_theme_to_url, append_broker_filter_to_url
from .utils.logger import get_logger
from .models.session_response_data import SessionResponseData
from .models.session_user_response import SessionUserResponse

from .api.brokers_api import BrokersApi
from .api.company_api import CompanyApi
from .api.session_api import SessionApi

from .wrappers.brokers import BrokersWrapper
from .wrappers.company import CompanyWrapper
from .wrappers.session import SessionWrapper

from .wrappers.brokers import GetOrdersParams
from .models.order_response import OrderResponse
from .wrappers.brokers import GetPositionsParams
from .models.position_response import PositionResponse
from .wrappers.brokers import GetBalancesParams
from .models.balances import Balances
from .wrappers.brokers import GetAccountsParams
from .models.accounts import Accounts
from .wrappers.brokers import GetOrderFillsParams
from .models.order_fill_response import OrderFillResponse
from .wrappers.brokers import GetOrderEventsParams
from .models.order_event_response import OrderEventResponse
from .wrappers.brokers import GetOrderGroupsParams
from .models.order_group_response import OrderGroupResponse
from .wrappers.brokers import GetPositionLotsParams
from .models.position_lot_response import PositionLotResponse
from .wrappers.brokers import GetPositionLotFillsParams
from .models.position_lot_fill_response import PositionLotFillResponse


class FinaticServer:
    """Main client class for Finatic Server SDK."""

    @classmethod
    async def init(
        cls,
        api_key: str,
        user_id: Optional[str] = None,
        sdk_config: Optional[SdkConfig] = None,
    ):
        """Initialize and create a FinaticServer instance with session started.
        
        This is the recommended way to initialize the SDK. It creates an instance
        and automatically starts a session using the provided API key.
        
        Args:
            api_key: Company API key (required)
            user_id: Optional user ID for direct authentication
            sdk_config: Optional SDK configuration overrides (includes base_url)
        
        Returns:
            FinaticServer instance with session already initialized
        
        Example:
            client = await FinaticServer.init(
                api_key="fntc_live_your_key",
                user_id="optional_user_id",
                sdk_config={'base_url': 'https://api.finatic.dev', 'log_level': 'debug'}
            )
            # Session is already started, ready to use
            orders = await client.get_all_orders()
        """
        # Create instance - extract base_url from sdk_config if provided
        base_url = sdk_config.get('base_url') if isinstance(sdk_config, dict) else (sdk_config.base_url if sdk_config and hasattr(sdk_config, 'base_url') else None)
        instance = cls(api_key, base_url, sdk_config)
        
        # Initialize session automatically
        try:
            # Start session using the instance's start_session method
            # This will use the API key from constructor and get token internally
            # Returns FinaticResponse[SessionResponseData] format
            session_result = await instance.start_session(user_id=user_id) if user_id else await instance.start_session()
            
            # Check if session was started successfully (FinaticResponse[SessionResponseData] format)
            if session_result.get('error'):
                error_data = session_result.get('error', {})
                if isinstance(error_data, dict):
                    error_msg = error_data.get('message', 'Unknown error')
                else:
                    error_msg = str(error_data)
                raise ValueError(
                    f"Session initialization failed: {error_msg}. "
                    "Please check that the API endpoint returned a valid session response and ensure the API key is valid."
                )
            
            # Verify session was initialized correctly
            session_id = instance.get_session_id()
            if not session_id:
                raise ValueError(
                    "Session initialization failed: start_session() did not return a session_id. "
                    "Please check that the API endpoint returned a valid session response."
                )
            
            return instance
        except ValueError:
            # Re-raise ValueError as-is (already has good error message)
            raise
        except Exception as e:
            # Re-raise with more context if it's a session initialization error
            # Safely convert exception to string to avoid type formatting issues
            try:
                error_str = str(e) if e else 'Unknown error'
            except Exception:
                error_str = f'Exception of type {type(e).__name__}'
            
            if "Session not initialized" in error_str or "session_id" in error_str.lower():
                raise ValueError(
                    f"Failed to initialize Finatic session: {error_str}. "
                    "This may indicate that start_session() was called but did not successfully create a session. "
                    "Please check the API response and ensure the API key is valid."
                ) from e
            raise ValueError(
                f"Session initialization failed: {error_str}. "
                "Please check that the API endpoint returned a valid session response and ensure the API key is valid."
            ) from e

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        sdk_config: Optional[SdkConfig] = None,
    ):
        """Initialize the client.
        
        Note: For automatic session initialization, use FinaticServer.init() instead.
        This constructor creates an instance but does not start a session.
        
        Args:
            api_key: Company API key
            base_url: Base URL for API (defaults to https://api.finatic.dev)
            sdk_config: Optional SDK configuration overrides
        """
        self.api_key = api_key
        self.config = Configuration(
            host=base_url or 'https://api.finatic.dev',
            api_key={'X-API-Key': api_key},
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

        self._brokers = BrokersWrapper(BrokersApi(self.api_client), self.config, self.sdk_config)
        self._company = CompanyWrapper(CompanyApi(self.api_client), self.config, self.sdk_config)
        self._session = SessionWrapper(SessionApi(self.api_client), self.config, self.sdk_config)

    async def initialize(self) -> None:
        """Initialize the client (no-op for now, can be extended)."""
        pass

    async def close(self) -> None:
        """Close the client and cleanup resources."""
        pass

    def set_session_context(self, session_id: str, company_id: str, csrf_token: str) -> None:
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
        self._brokers.set_session_context(session_id, company_id, csrf_token)
        self._company.set_session_context(session_id, company_id, csrf_token)
        self._session.set_session_context(session_id, company_id, csrf_token)

    def get_session_id(self) -> Optional[str]:
        """Get current session ID."""
        return self.session_id

    def get_company_id(self) -> Optional[str]:
        """Get current company ID."""
        return self.company_id

    def get_user_id(self) -> Optional[str]:
        """Get current user ID (set after portal authentication)."""
        return self.user_id

    def is_authed(self) -> bool:
        """Check if user is authenticated (has userId)."""
        return bool(self.user_id)

    async def _init_session(self, x_api_key: str) -> str:
        """Initialize a session by getting a one-time token (internal/private).
        
        Args:
            x_api_key: Company API key
        
        Returns:
            One-time token
        """
        # Call wrapper method with keyword arguments (standardized format)
        # Returns dict (FinaticResponse[TokenResponseData])
        response = await self._session.init_session(x_api_key=x_api_key)
        if response.get('error'):
            error_msg = response.get('error', {}).get('message', 'Failed to initialize session') if isinstance(response.get('error'), dict) else str(response.get('error'))
            raise Exception(error_msg)
        success_data = response.get('success', {})
        return success_data.get('data', {}).get('one_time_token', '') if isinstance(success_data, dict) else ''

    async def get_token(self, api_key: Optional[str] = None) -> str:
        """Get a one-time token from an API key.
        
        This method only retrieves the token and returns it - it does NOT start a session
        or set any session context. Useful for generating tokens to pass to clients.
        
        Args:
            api_key: Company API key (uses instance API key if not provided)
        
        Returns:
            One-time token string
        
        Raises:
            Exception: If API key is missing or token generation fails
        """
        key_to_use = api_key or self.api_key
        if not key_to_use:
            raise Exception('API key is required. Provide it as a parameter or in the constructor.')
        return await self._init_session(key_to_use)

    async def start_session(
        self,
        user_id: Optional[str] = None
    ) -> FinaticResponse[SessionResponseData]:
        """Start a session using the API key from constructor.
        
        Gets a one-time token using the API key from constructor, then starts the session.
        This method is exposed for advanced use cases. For most use cases, use FinaticServer.init() instead.
        
        Args:
            user_id: Optional user ID for direct authentication
        
        Returns:
            Dict[str, Any]: FinaticResponse[SessionResponseData] format
                success: {data: SessionResponseData, meta: dict | None}
                error: dict | None
                warning: list[dict] | None
        
        Raises:
            Exception: If API key is missing or session start fails
        """
        if not self.api_key:
            return {
                'success': {'data': None, 'meta': None},
                'error': {'message': 'API key is required. Provide it in the constructor.'},
                'warning': None
            }

        try:
            # Step 1: Get one-time token using API key from constructor
            one_time_token = await self._init_session(self.api_key)
            
            if not one_time_token or not isinstance(one_time_token, str):
                return {
                    'success': {'data': None, 'meta': None},
                    'error': {'message': 'Failed to get one-time token'},
                    'warning': None
                }

            # Step 2: Start session with the token - returns FinaticResponse[SessionResponseData]
            session_start_request = {"user_id": user_id} if user_id else {}
            response = await self._session.start_session(
                one_time_token=one_time_token,
                session_start_request=session_start_request
            )
            
            # Extract session data and set context if successful
            if response.get('success') and not response.get('error'):
                session_data = response['success'].get('data', {}) if isinstance(response.get('success'), dict) else {}
                session_id = session_data.get('session_id', '') if isinstance(session_data, dict) else ''
                company_id = session_data.get('company_id', '') if isinstance(session_data, dict) else ''
                csrf_token = ''
                
                if session_id and company_id:
                    self.set_session_context(session_id, company_id, csrf_token)
            
            # Return the standard response format (already FinaticResponse[SessionResponseData])
            return response
        except Exception as e:
            return {
                'success': {'data': None, 'meta': None},
                'error': {'message': str(e)},
                'warning': None
            }

    async def get_portal_url(
        self,
        theme: Optional[str | Dict[str, Any]] = None,
        brokers: Optional[List[str]] = None,
        email: Optional[str] = None,
        mode: Optional[str] = None
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
            raise ValueError('Session not initialized. Call start_session() first.')

        # Get raw portal URL from session wrapper (using keyword arguments)
        # Returns dict (FinaticResponse[PortalUrlResponse])
        response = await self._session.get_portal_url()
        
        # Check for errors
        if response.get('error'):
            error_msg = response.get('error', {}).get('message', 'Failed to get portal URL') if isinstance(response.get('error'), dict) else str(response.get('error'))
            self.logger.error('Failed to get portal URL', extra={
                'error': error_msg,
                'code': response.get('error', {}).get('code') if isinstance(response.get('error'), dict) else None,
                'status': response.get('error', {}).get('status') if isinstance(response.get('error'), dict) else None,
            })
            raise Exception(error_msg)
        
        # Extract portal URL from standard response structure
        success_data = response.get('success', {})
        if success_data and isinstance(success_data, dict):
            data = success_data.get('data', {})
            portal_url = data.get('portal_url', '') if isinstance(data, dict) else ''
        else:
            self.logger.error('Invalid portal URL response: missing data', extra={})
            raise ValueError('Invalid portal URL response: missing portal_url')
        
        if not portal_url:
            self.logger.error('Empty portal URL from API', extra={})
            raise ValueError('Empty portal URL received from API')

        # Validate URL before manipulation
        from urllib.parse import urlparse
        try:
            parsed = urlparse(portal_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f'Invalid portal URL format: {portal_url}')
        except Exception as e:
            self.logger.error('Invalid portal URL from API', extra={'portal_url': portal_url, 'error': str(e)})
            raise ValueError(f'Invalid portal URL received from API: {portal_url}')

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
            query_params['email'] = [email]
            new_query = urlencode(query_params, doseq=True)
            new_parsed = parsed._replace(query=new_query)
            portal_url = urlunparse(new_parsed)

        # Append mode if provided (light or dark)
        if mode:
            from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
            parsed = urlparse(portal_url)
            query_params = parse_qs(parsed.query)
            query_params['mode'] = [mode]
            new_query = urlencode(query_params, doseq=True)
            new_parsed = parsed._replace(query=new_query)
            portal_url = urlunparse(new_parsed)

        # Add session ID and company ID to URL
        from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
        parsed = urlparse(portal_url)
        query_params = parse_qs(parsed.query)
        if self.session_id:
            query_params['session_id'] = [self.session_id]
        if self.company_id:
            query_params['company_id'] = [self.company_id]
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        portal_url = urlunparse(new_parsed)

        self.logger.debug('Portal URL generated', extra={'portal_url': portal_url})
        return portal_url

    async def get_session_user(self) -> FinaticResponse[SessionUserResponse]:
        """Get session user information after portal authentication.
        
        Returns:
            Dict[str, Any]: FinaticResponse[SessionUserResponse] format
                success: {data: SessionUserResponse, meta: dict | None}
                error: dict | None
                warning: list[dict] | None
        """
        if not self.session_id or not self.company_id:
            raise ValueError('Session not initialized. Call start_session() first.')
        
        # get_session_user uses session_id in the path and company_id from session context
        # Call wrapper method with keyword arguments (standardized format)
        # Returns FinaticResponse[SessionUserResponse] - maintain the structure
        response = await self._session.get_session_user(session_id=self.session_id)
        
        # Extract user_id from response for internal state management
        if response.get('success') and isinstance(response.get('success'), dict):
            data = response['success'].get('data', {})
            user_id = data.get('user_id', '') if isinstance(data, dict) else ''
            # Store user_id for get_user_id() method
            if user_id:
                self.user_id = user_id
        
        # Return the full FinaticResponse[SessionUserResponse] structure
        return response


    async def get_all_orders(self, **kwargs) -> FinaticResponse[list[OrderResponse]]:
        """Get all orders across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetOrdersParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetOrdersParams(**filtered_kwargs) if filtered_kwargs else GetOrdersParams()
        else:
            params = GetOrdersParams()
        
        all_data: list[OrderResponse] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_orders(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_positions(self, **kwargs) -> FinaticResponse[list[PositionResponse]]:
        """Get all positions across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetPositionsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetPositionsParams(**filtered_kwargs) if filtered_kwargs else GetPositionsParams()
        else:
            params = GetPositionsParams()
        
        all_data: list[PositionResponse] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_positions(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_balances(self, **kwargs) -> FinaticResponse[list[Balances]]:
        """Get all balances across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetBalancesParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetBalancesParams(**filtered_kwargs) if filtered_kwargs else GetBalancesParams()
        else:
            params = GetBalancesParams()
        
        all_data: list[Balances] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_balances(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_accounts(self, **kwargs) -> FinaticResponse[list[Accounts]]:
        """Get all accounts across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetAccountsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetAccountsParams(**filtered_kwargs) if filtered_kwargs else GetAccountsParams()
        else:
            params = GetAccountsParams()
        
        all_data: list[Accounts] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_accounts(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_order_fills(self, **kwargs) -> FinaticResponse[list[OrderFillResponse]]:
        """Get all order_fills across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetOrderFillsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetOrderFillsParams(**filtered_kwargs) if filtered_kwargs else GetOrderFillsParams()
        else:
            params = GetOrderFillsParams()
        
        all_data: list[OrderFillResponse] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_order_fills(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_order_events(self, **kwargs) -> FinaticResponse[list[OrderEventResponse]]:
        """Get all order_events across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetOrderEventsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetOrderEventsParams(**filtered_kwargs) if filtered_kwargs else GetOrderEventsParams()
        else:
            params = GetOrderEventsParams()
        
        all_data: list[OrderEventResponse] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_order_events(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_order_groups(self, **kwargs) -> FinaticResponse[list[OrderGroupResponse]]:
        """Get all order_groups across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetOrderGroupsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetOrderGroupsParams(**filtered_kwargs) if filtered_kwargs else GetOrderGroupsParams()
        else:
            params = GetOrderGroupsParams()
        
        all_data: list[OrderGroupResponse] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_order_groups(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_position_lots(self, **kwargs) -> FinaticResponse[list[PositionLotResponse]]:
        """Get all position_lots across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetPositionLotsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetPositionLotsParams(**filtered_kwargs) if filtered_kwargs else GetPositionLotsParams()
        else:
            params = GetPositionLotsParams()
        
        all_data: list[PositionLotResponse] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_position_lots(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }

    async def get_all_position_lot_fills(self, **kwargs) -> FinaticResponse[list[PositionLotFillResponse]]:
        """Get all position_lot_fills across all pages.
        
        Auto-generated from paginated endpoint.
        
        Args:
            **kwargs: Optional keyword arguments that will be converted to params object.
                     Example: get_all_orders(account_id="123", symbol="AAPL")
        
        Returns:
            FinaticResponse with success, error, and warning fields containing list of all items across all pages
        """
        from dataclasses import replace, fields
        
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            valid_field_names = {f.name for f in fields(GetPositionLotFillsParams)}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
            params = GetPositionLotFillsParams(**filtered_kwargs) if filtered_kwargs else GetPositionLotFillsParams()
        else:
            params = GetPositionLotFillsParams()
        
        all_data: list[PositionLotFillResponse] = []
        offset = 0
        limit = 1000
        last_error = None
        warnings = []
        
        while True:
            # Create new params with limit and offset
            paginated_params = replace(params, limit=limit, offset=offset)
            # Convert params dataclass to dict and unpack as kwargs
            # Wrapper methods expect **kwargs, not a params object
            params_dict = paginated_params.__dict__ if hasattr(paginated_params, '__dict__') else (paginated_params if isinstance(paginated_params, dict) else {})
            # Unpack params dict as kwargs to wrapper method
            # Note: Wrapper methods accept **kwargs, so we can unpack the params dict directly
            # Use private wrapper (self._brokers, self._company) since wrappers are private
            response = await self._brokers.get_position_lot_fills(**params_dict)
            
            # Collect warnings from each page
            if response.get('warning') and isinstance(response.get('warning'), list):
                warnings.extend(response.get('warning', []))
            
            if response.get('error'):
                last_error = response.get('error')
                break
            
            success_data = response.get('success', {})
            result = success_data.get('data', []) if isinstance(success_data, dict) else []
            if not result or len(result) == 0:
                break
            all_data.extend(result if isinstance(result, list) else [result])
            if len(result) < limit:
                break
            offset += limit
        
        # Return FinaticResponse with accumulated data
        if last_error:
            return {
                'success': None,
                'error': last_error,
                'warning': warnings if warnings else None,
            }
        
        return {
            'success': {
                'data': all_data,
            },
            'error': None,
            'warning': warnings if warnings else None,
        }


    async def get_company(self, **kwargs) -> FinaticResponse[CompanyResponse]:
        """Get Company
        
        Convenience method that delegates to company wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[CompanyResponse]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetCompanyParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._company.get_company(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._company.get_company(**kwargs)
        else:
            return await self._company.get_company()

    async def get_brokers(self, **kwargs) -> FinaticResponse[list[BrokerInfo]]:
        """Get Brokers
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[BrokerInfo]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetBrokersParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_brokers(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_brokers(**kwargs)
        else:
            return await self._brokers.get_brokers()

    async def get_broker_connections(self, **kwargs) -> FinaticResponse[list[UserBrokerConnections]]:
        """List Broker Connections
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[UserBrokerConnections]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetBrokerConnectionsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_broker_connections(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_broker_connections(**kwargs)
        else:
            return await self._brokers.get_broker_connections()

    async def disconnect_company_from_broker(self, **kwargs) -> FinaticResponse[DisconnectActionResult]:
        """Disconnect Company From Broker
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[DisconnectActionResult]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(DisconnectCompanyFromBrokerParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.disconnect_company_from_broker(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.disconnect_company_from_broker(**kwargs)
        else:
            return await self._brokers.disconnect_company_from_broker()

    async def get_orders(self, **kwargs) -> FinaticResponse[list[OrderResponse]]:
        """Get Orders
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[OrderResponse]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetOrdersParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_orders(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_orders(**kwargs)
        else:
            return await self._brokers.get_orders()

    async def get_positions(self, **kwargs) -> FinaticResponse[list[PositionResponse]]:
        """Get Positions
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[PositionResponse]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetPositionsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_positions(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_positions(**kwargs)
        else:
            return await self._brokers.get_positions()

    async def get_balances(self, **kwargs) -> FinaticResponse[list[Balances]]:
        """Get Balances
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[Balances]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetBalancesParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_balances(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_balances(**kwargs)
        else:
            return await self._brokers.get_balances()

    async def get_accounts(self, **kwargs) -> FinaticResponse[list[Accounts]]:
        """Get Accounts
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[Accounts]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetAccountsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_accounts(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_accounts(**kwargs)
        else:
            return await self._brokers.get_accounts()

    async def get_order_fills(self, **kwargs) -> FinaticResponse[list[OrderFillResponse]]:
        """Get Order Fills
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[OrderFillResponse]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetOrderFillsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_order_fills(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_order_fills(**kwargs)
        else:
            return await self._brokers.get_order_fills()

    async def get_order_events(self, **kwargs) -> FinaticResponse[list[OrderEventResponse]]:
        """Get Order Events
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[OrderEventResponse]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetOrderEventsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_order_events(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_order_events(**kwargs)
        else:
            return await self._brokers.get_order_events()

    async def get_order_groups(self, **kwargs) -> FinaticResponse[list[OrderGroupResponse]]:
        """Get Order Groups
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[OrderGroupResponse]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetOrderGroupsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_order_groups(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_order_groups(**kwargs)
        else:
            return await self._brokers.get_order_groups()

    async def get_position_lots(self, **kwargs) -> FinaticResponse[list[PositionLotResponse]]:
        """Get Position Lots
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[PositionLotResponse]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetPositionLotsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_position_lots(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_position_lots(**kwargs)
        else:
            return await self._brokers.get_position_lots()

    async def get_position_lot_fills(self, **kwargs) -> FinaticResponse[list[PositionLotFillResponse]]:
        """Get Position Lot Fills
        
        Convenience method that delegates to brokers wrapper.
        
        Args:
            **kwargs: Optional keyword arguments passed to wrapper method.
                     Only valid parameter fields are passed through (invalid keys are filtered out).
        
        Returns:
            FinaticResponse[list[PositionLotFillResponse]]: Standard FinaticResponse format
        """
        from dataclasses import fields
        # Filter kwargs to only include valid dataclass fields (exclude wrapper-specific params like with_envelope)
        if kwargs:
            try:
                valid_field_names = {f.name for f in fields(GetPositionLotFillsParams)}
                filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_field_names}
                return await self._brokers.get_position_lot_fills(**filtered_kwargs)
            except (TypeError, AttributeError):
                # If params type doesn't exist or isn't a dataclass, pass kwargs as-is
                # This handles edge cases where the type might not be available
                return await self._brokers.get_position_lot_fills(**kwargs)
        else:
            return await self._brokers.get_position_lot_fills()
