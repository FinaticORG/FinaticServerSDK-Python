"""
Generated wrapper functions for brokers operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/brokers.py instead.
"""

from __future__ import annotations

from typing import Optional, Any, Dict, List
from dataclasses import dataclass
from ..api.brokers_api import BrokersApi
from ..configuration import Configuration
from ..config import SdkConfig
from ..types import FinaticResponse
from ..models.account_status import AccountStatus
from ..models.accounts import Accounts
from ..models.balances import Balances
from ..models.broker_info import BrokerInfo
from ..models.disconnect_action_result import DisconnectActionResult
from ..models.order_event_response import OrderEventResponse
from ..models.order_fill_response import OrderFillResponse
from ..models.order_group_response import OrderGroupResponse
from ..models.order_response import OrderResponse
from ..models.position_lot_fill_response import PositionLotFillResponse
from ..models.position_lot_response import PositionLotResponse
from ..models.position_response import PositionResponse
from ..models.public_account_type_enum import PublicAccountTypeEnum
from ..models.public_asset_type_enum import PublicAssetTypeEnum
from ..models.public_order_side_enum import PublicOrderSideEnum
from ..models.public_order_status_enum import PublicOrderStatusEnum
from ..models.public_position_status_enum import PublicPositionStatusEnum
from ..models.user_broker_connections import UserBrokerConnections
from ..utils.request_id import generate_request_id
from ..utils.retry import retry_api_call
from ..utils.logger import get_logger
from ..utils.error_handling import handle_error
from ..utils.cache import get_cache, generate_cache_key
from ..utils.interceptors import (
    apply_request_interceptors,
    apply_response_interceptors,
    apply_error_interceptors,
)
from ..utils.enum_coercion import coerce_enum_value

# Phase 2C: Input type definitions (output types use FinaticResponse[DataType] pattern - no models needed)
@dataclass
class GetBrokersParams:
    """Input parameters for get_brokers_api_v1_brokers__get."""
    pass

@dataclass
class GetBrokerConnectionsParams:
    """Input parameters for list_broker_connections_api_v1_brokers_connections_get."""
    pass

@dataclass
class DisconnectCompanyFromBrokerParams:
    """Input parameters for disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete."""
    connection_id: str

@dataclass
class GetOrdersParams:
    """Input parameters for get_orders_api_v1_brokers_data_orders_get."""
    broker_id: str = None
    connection_id: str = None
    account_id: str = None
    symbol: str = None
    order_status: PublicOrderStatusEnum = None
    side: PublicOrderSideEnum = None
    asset_type: PublicAssetTypeEnum = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    created_after: str = None
    created_before: str = None
    with_metadata: Optional[bool] = None

@dataclass
class GetPositionsParams:
    """Input parameters for get_positions_api_v1_brokers_data_positions_get."""
    broker_id: str = None
    connection_id: str = None
    account_id: str = None
    symbol: str = None
    side: PublicOrderSideEnum = None
    asset_type: PublicAssetTypeEnum = None
    position_status: PublicPositionStatusEnum = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    updated_after: str = None
    updated_before: str = None
    with_metadata: Optional[bool] = None

@dataclass
class GetBalancesParams:
    """Input parameters for get_balances_api_v1_brokers_data_balances_get."""
    broker_id: str = None
    connection_id: str = None
    account_id: str = None
    is_end_of_day_snapshot: Optional[bool] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    balance_created_after: str = None
    balance_created_before: str = None
    with_metadata: Optional[bool] = None

@dataclass
class GetAccountsParams:
    """Input parameters for get_accounts_api_v1_brokers_data_accounts_get."""
    broker_id: str = None
    connection_id: str = None
    account_type: PublicAccountTypeEnum = None
    status: AccountStatus = None
    currency: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    with_metadata: Optional[bool] = None

@dataclass
class GetOrderFillsParams:
    """Input parameters for get_order_fills_api_v1_brokers_data_orders__order_id__fills_get."""
    order_id: str
    connection_id: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None

@dataclass
class GetOrderEventsParams:
    """Input parameters for get_order_events_api_v1_brokers_data_orders__order_id__events_get."""
    order_id: str
    connection_id: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None

@dataclass
class GetOrderGroupsParams:
    """Input parameters for get_order_groups_api_v1_brokers_data_orders_groups_get."""
    broker_id: str = None
    connection_id: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    created_after: str = None
    created_before: str = None

@dataclass
class GetPositionLotsParams:
    """Input parameters for get_position_lots_api_v1_brokers_data_positions_lots_get."""
    broker_id: str = None
    connection_id: str = None
    account_id: str = None
    symbol: str = None
    position_id: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None

@dataclass
class GetPositionLotFillsParams:
    """Input parameters for get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get."""
    lot_id: str
    connection_id: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class BrokersWrapper:
    """Brokers wrapper functions.
    
    Provides simplified method names and response unwrapping.
    """
    
    def __init__(self, api: BrokersApi, config: Optional[Configuration] = None, sdk_config: Optional[SdkConfig] = None):
        self.api = api
        self.config = config
        self.sdk_config = sdk_config
        self.logger = get_logger(sdk_config)
        self.session_id: Optional[str] = None
        self.company_id: Optional[str] = None
        self.csrf_token: Optional[str] = None
    
    # Session context setters (called by session management)
    def set_session_context(self, session_id: str, company_id: str, csrf_token: str) -> None:
        """Set session context for API calls."""
        self.session_id = session_id
        self.company_id = company_id
        self.csrf_token = csrf_token
    
    # Utility methods (Phase 2B)
    def _generate_request_id(self) -> str:
        """Generate a unique request ID."""
        return generate_request_id()
    
    async def _retry_api_call(self, fn):
        """Retry an API call with exponential backoff."""
        return await retry_api_call(fn)
    
    def _handle_error(self, error: Exception, request_id: Optional[str] = None) -> Exception:
        """Handle and transform errors from API calls."""
        return handle_error(error, request_id)

    async def get_brokers(self, **kwargs) -> FinaticResponse[list[BrokerInfo]]:
        """Get Brokers
        
        Get all available brokers.
        
        This is a fast operation that returns a cached list of available brokers.
        The list is loaded once at startup and never changes during runtime.
        
        Returns
        -------
        FinaticResponse[list[BrokerInfo]]
            list of available brokers with their metadata.

        Args:
        - **kwargs: No parameters required for this method
        Returns:
        - Dict[str, Any]: FinaticResponse[list[BrokerInfo]] format
                     success: {data: list[BrokerInfo], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/
        @methodId get_brokers_api_v1_brokers__get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_brokers()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
        # Convert kwargs to params object
        params = GetBrokersParams(**kwargs) if kwargs else GetBrokersParams()
        # Phase 2C: Extract individual params from input params object
        # No parameters to extract

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Brokers',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/',
            params=params_dict,
            action='get_brokers'
        )

        try:
            async def api_call():
                response = await self.api.get_brokers_api_v1_brokers_get()

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Brokers completed',
                request_id=request_id,
                action='get_brokers'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Brokers failed',
                error=str(e),
                request_id=request_id,
                action='get_brokers',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[BrokerInfo]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_broker_connections(self, **kwargs) -> FinaticResponse[list[UserBrokerConnections]]:
        """List Broker Connections
        
        List all broker connections for the current user.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns connections that the user has any permissions for.

        Args:
        - **kwargs: No parameters required for this method
        Returns:
        - Dict[str, Any]: FinaticResponse[list[UserBrokerConnections]] format
                     success: {data: list[UserBrokerConnections], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/connections
        @methodId list_broker_connections_api_v1_brokers_connections_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_broker_connections()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
        # Convert kwargs to params object
        params = GetBrokerConnectionsParams(**kwargs) if kwargs else GetBrokerConnectionsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        # No parameters to extract

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/connections', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('List Broker Connections',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/connections',
            params=params_dict,
            action='get_broker_connections'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.list_broker_connections_api_v1_brokers_connections_get(_headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/connections', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('List Broker Connections completed',
                request_id=request_id,
                action='get_broker_connections'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('List Broker Connections failed',
                error=str(e),
                request_id=request_id,
                action='get_broker_connections',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[UserBrokerConnections]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def disconnect_company_from_broker(self, **kwargs) -> FinaticResponse[DisconnectActionResult]:
        """Disconnect Company From Broker
        
        Remove a company's access to a broker connection.
        
        If the company is the only one with access, the entire connection is deleted.
        If other companies have access, only the company's access is removed.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to DisconnectCompanyFromBrokerParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[DisconnectActionResult] format
                     success: {data: DisconnectActionResult, meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: DELETE /api/v1/brokers/disconnect-company/{connection_id}
        @methodId disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.disconnect_company_from_broker(
            connection_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        """
        # Convert kwargs to params object
        params = DisconnectCompanyFromBrokerParams(**kwargs) if kwargs else DisconnectCompanyFromBrokerParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        connection_id = params.connection_id

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect-company/{connection_id}', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Disconnect Company From Broker',
            request_id=request_id,
            method='DELETE',
            path='/api/v1/brokers/disconnect-company/{connection_id}',
            params=params_dict,
            action='disconnect_company_from_broker'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.disconnect_company_from_broker_api_v1_brokers_disconnect_company_connection_id_delete(connection_id=connection_id, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect-company/{connection_id}', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Disconnect Company From Broker completed',
                request_id=request_id,
                action='disconnect_company_from_broker'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Disconnect Company From Broker failed',
                error=str(e),
                request_id=request_id,
                action='disconnect_company_from_broker',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[DisconnectActionResult](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_orders(self, **kwargs) -> FinaticResponse[list[OrderResponse]]:
        """Get Orders
        
        Get orders for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns orders from connections the company has read access to.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetOrdersParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[OrderResponse]] format
                     success: {data: list[OrderResponse], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/orders
        @methodId get_orders_api_v1_brokers_data_orders_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_orders()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_orders(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_id='123456789'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetOrdersParams(**kwargs) if kwargs else GetOrdersParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_id = getattr(params, 'account_id', None)
        symbol = getattr(params, 'symbol', None)
        order_status = coerce_enum_value(getattr(params, 'order_status', None), PublicOrderStatusEnum, 'order_status') if getattr(params, 'order_status', None) is not None else None
        side = coerce_enum_value(getattr(params, 'side', None), PublicOrderSideEnum, 'side') if getattr(params, 'side', None) is not None else None
        asset_type = coerce_enum_value(getattr(params, 'asset_type', None), PublicAssetTypeEnum, 'asset_type') if getattr(params, 'asset_type', None) is not None else None
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        created_after = getattr(params, 'created_after', None)
        created_before = getattr(params, 'created_before', None)
        with_metadata = getattr(params, 'with_metadata', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Orders',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders',
            params=params_dict,
            action='get_orders'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_orders_api_v1_brokers_data_orders_get(broker_id=broker_id, connection_id=connection_id, account_id=account_id, symbol=symbol, order_status=order_status, side=side, asset_type=asset_type, limit=limit, offset=offset, created_after=created_after, created_before=created_before, with_metadata=with_metadata, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Orders completed',
                request_id=request_id,
                action='get_orders'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Orders failed',
                error=str(e),
                request_id=request_id,
                action='get_orders',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[OrderResponse]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_positions(self, **kwargs) -> FinaticResponse[list[PositionResponse]]:
        """Get Positions
        
        Get positions for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns positions from connections the company has read access to.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetPositionsParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[PositionResponse]] format
                     success: {data: list[PositionResponse], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/positions
        @methodId get_positions_api_v1_brokers_data_positions_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_positions()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_positions(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_id='123456789'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetPositionsParams(**kwargs) if kwargs else GetPositionsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_id = getattr(params, 'account_id', None)
        symbol = getattr(params, 'symbol', None)
        side = coerce_enum_value(getattr(params, 'side', None), PublicOrderSideEnum, 'side') if getattr(params, 'side', None) is not None else None
        asset_type = coerce_enum_value(getattr(params, 'asset_type', None), PublicAssetTypeEnum, 'asset_type') if getattr(params, 'asset_type', None) is not None else None
        position_status = coerce_enum_value(getattr(params, 'position_status', None), PublicPositionStatusEnum, 'position_status') if getattr(params, 'position_status', None) is not None else None
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        updated_after = getattr(params, 'updated_after', None)
        updated_before = getattr(params, 'updated_before', None)
        with_metadata = getattr(params, 'with_metadata', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Positions',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions',
            params=params_dict,
            action='get_positions'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_positions_api_v1_brokers_data_positions_get(broker_id=broker_id, connection_id=connection_id, account_id=account_id, symbol=symbol, side=side, asset_type=asset_type, position_status=position_status, limit=limit, offset=offset, updated_after=updated_after, updated_before=updated_before, with_metadata=with_metadata, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Positions completed',
                request_id=request_id,
                action='get_positions'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Positions failed',
                error=str(e),
                request_id=request_id,
                action='get_positions',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[PositionResponse]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_balances(self, **kwargs) -> FinaticResponse[list[Balances]]:
        """Get Balances
        
        Get balances for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns balances from connections the company has read access to.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetBalancesParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[Balances]] format
                     success: {data: list[Balances], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/balances
        @methodId get_balances_api_v1_brokers_data_balances_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_balances()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_balances(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_id='123456789'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetBalancesParams(**kwargs) if kwargs else GetBalancesParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_id = getattr(params, 'account_id', None)
        is_end_of_day_snapshot = getattr(params, 'is_end_of_day_snapshot', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        balance_created_after = getattr(params, 'balance_created_after', None)
        balance_created_before = getattr(params, 'balance_created_before', None)
        with_metadata = getattr(params, 'with_metadata', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/balances', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Balances',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/balances',
            params=params_dict,
            action='get_balances'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_balances_api_v1_brokers_data_balances_get(broker_id=broker_id, connection_id=connection_id, account_id=account_id, is_end_of_day_snapshot=is_end_of_day_snapshot, limit=limit, offset=offset, balance_created_after=balance_created_after, balance_created_before=balance_created_before, with_metadata=with_metadata, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/balances', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Balances completed',
                request_id=request_id,
                action='get_balances'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Balances failed',
                error=str(e),
                request_id=request_id,
                action='get_balances',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[Balances]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_accounts(self, **kwargs) -> FinaticResponse[list[Accounts]]:
        """Get Accounts
        
        Get accounts for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns accounts from connections the company has read access to.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetAccountsParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[Accounts]] format
                     success: {data: list[Accounts], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/accounts
        @methodId get_accounts_api_v1_brokers_data_accounts_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_accounts()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_accounts(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_type='margin'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetAccountsParams(**kwargs) if kwargs else GetAccountsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_type = coerce_enum_value(getattr(params, 'account_type', None), PublicAccountTypeEnum, 'account_type') if getattr(params, 'account_type', None) is not None else None
        status = getattr(params, 'status', None)
        currency = getattr(params, 'currency', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        with_metadata = getattr(params, 'with_metadata', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/accounts', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Accounts',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/accounts',
            params=params_dict,
            action='get_accounts'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_accounts_api_v1_brokers_data_accounts_get(broker_id=broker_id, connection_id=connection_id, account_type=account_type, status=status, currency=currency, limit=limit, offset=offset, with_metadata=with_metadata, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/accounts', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Accounts completed',
                request_id=request_id,
                action='get_accounts'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Accounts failed',
                error=str(e),
                request_id=request_id,
                action='get_accounts',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[Accounts]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_order_fills(self, **kwargs) -> FinaticResponse[list[OrderFillResponse]]:
        """Get Order Fills
        
        Get order fills for a specific order.
        
        This endpoint returns all execution fills for the specified order.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetOrderFillsParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[OrderFillResponse]] format
                     success: {data: list[OrderFillResponse], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/orders/{order_id}/fills
        @methodId get_order_fills_api_v1_brokers_data_orders__order_id__fills_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.get_order_fills(
            order_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_order_fills(
            order_id='00000000-0000-0000-0000-000000000000',
            connection_id='00000000-0000-0000-0000-000000000000',
            limit=100,
            offset=0
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetOrderFillsParams(**kwargs) if kwargs else GetOrderFillsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        order_id = params.order_id
        connection_id = getattr(params, 'connection_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/fills', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Order Fills',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/{order_id}/fills',
            params=params_dict,
            action='get_order_fills'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_order_fills_api_v1_brokers_data_orders_order_id_fills_get(order_id=order_id, connection_id=connection_id, limit=limit, offset=offset, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/fills', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Order Fills completed',
                request_id=request_id,
                action='get_order_fills'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Order Fills failed',
                error=str(e),
                request_id=request_id,
                action='get_order_fills',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[OrderFillResponse]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_order_events(self, **kwargs) -> FinaticResponse[list[OrderEventResponse]]:
        """Get Order Events
        
        Get order events for a specific order.
        
        This endpoint returns all lifecycle events for the specified order.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetOrderEventsParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[OrderEventResponse]] format
                     success: {data: list[OrderEventResponse], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/orders/{order_id}/events
        @methodId get_order_events_api_v1_brokers_data_orders__order_id__events_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.get_order_events(
            order_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_order_events(
            order_id='00000000-0000-0000-0000-000000000000',
            connection_id='00000000-0000-0000-0000-000000000000',
            limit=100,
            offset=0
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetOrderEventsParams(**kwargs) if kwargs else GetOrderEventsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        order_id = params.order_id
        connection_id = getattr(params, 'connection_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/events', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Order Events',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/{order_id}/events',
            params=params_dict,
            action='get_order_events'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_order_events_api_v1_brokers_data_orders_order_id_events_get(order_id=order_id, connection_id=connection_id, limit=limit, offset=offset, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/events', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Order Events completed',
                request_id=request_id,
                action='get_order_events'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Order Events failed',
                error=str(e),
                request_id=request_id,
                action='get_order_events',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[OrderEventResponse]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_order_groups(self, **kwargs) -> FinaticResponse[list[OrderGroupResponse]]:
        """Get Order Groups
        
        Get order groups.
        
        This endpoint returns order groups that contain multiple orders.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetOrderGroupsParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[OrderGroupResponse]] format
                     success: {data: list[OrderGroupResponse], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/orders/groups
        @methodId get_order_groups_api_v1_brokers_data_orders_groups_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_order_groups()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_order_groups(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            limit=100
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetOrderGroupsParams(**kwargs) if kwargs else GetOrderGroupsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)
        created_after = getattr(params, 'created_after', None)
        created_before = getattr(params, 'created_before', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/groups', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Order Groups',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/groups',
            params=params_dict,
            action='get_order_groups'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_order_groups_api_v1_brokers_data_orders_groups_get(broker_id=broker_id, connection_id=connection_id, limit=limit, offset=offset, created_after=created_after, created_before=created_before, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/groups', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Order Groups completed',
                request_id=request_id,
                action='get_order_groups'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Order Groups failed',
                error=str(e),
                request_id=request_id,
                action='get_order_groups',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[OrderGroupResponse]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_position_lots(self, **kwargs) -> FinaticResponse[list[PositionLotResponse]]:
        """Get Position Lots
        
        Get position lots (tax lots for positions).
        
        This endpoint returns tax lots for positions, which are used for tax reporting.
        Each lot tracks when a position was opened/closed and at what prices.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetPositionLotsParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[PositionLotResponse]] format
                     success: {data: list[PositionLotResponse], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/positions/lots
        @methodId get_position_lots_api_v1_brokers_data_positions_lots_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        result = await finatic.get_position_lots()
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_position_lots(
            broker_id='alpaca',
            connection_id='00000000-0000-0000-0000-000000000000',
            account_id='123456789'
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetPositionLotsParams(**kwargs) if kwargs else GetPositionLotsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, 'broker_id', None)
        connection_id = getattr(params, 'connection_id', None)
        account_id = getattr(params, 'account_id', None)
        symbol = getattr(params, 'symbol', None)
        position_id = getattr(params, 'position_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Position Lots',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions/lots',
            params=params_dict,
            action='get_position_lots'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_position_lots_api_v1_brokers_data_positions_lots_get(broker_id=broker_id, connection_id=connection_id, account_id=account_id, symbol=symbol, position_id=position_id, limit=limit, offset=offset, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Position Lots completed',
                request_id=request_id,
                action='get_position_lots'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Position Lots failed',
                error=str(e),
                request_id=request_id,
                action='get_position_lots',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[PositionLotResponse]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_position_lot_fills(self, **kwargs) -> FinaticResponse[list[PositionLotFillResponse]]:
        """Get Position Lot Fills
        
        Get position lot fills for a specific lot.
        
        This endpoint returns all fills associated with a specific position lot.

        Args:
        - **kwargs: Optional keyword arguments that will be converted to GetPositionLotFillsParams object.
                     Example: get_orders(account_id="123", symbol="AAPL")
        Returns:
        - Dict[str, Any]: FinaticResponse[list[PositionLotFillResponse]] format
                     success: {data: list[PositionLotFillResponse], meta: dict | None}
                     error: dict | None
                     warning: list[dict] | None
        
        Generated from: GET /api/v1/brokers/data/positions/lots/{lot_id}/fills
        @methodId get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        result = await finatic.get_position_lot_fills(
            lot_id='00000000-0000-0000-0000-000000000000'
        )
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.error:
            print('Error:', result.error['message'])
        ```
        @example
        ```python
        # Full example with optional parameters
        result = await finatic.get_position_lot_fills(
            lot_id='00000000-0000-0000-0000-000000000000',
            connection_id='00000000-0000-0000-0000-000000000000',
            limit=100,
            offset=0
        )
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.warning:
                print('Warnings:', result.warning)
        elif result.error:
            print('Error:', result.error['message'], result.error['code'])
        ```
        """
        # Convert kwargs to params object
        params = GetPositionLotFillsParams(**kwargs) if kwargs else GetPositionLotFillsParams()
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        lot_id = params.lot_id
        connection_id = getattr(params, 'connection_id', None)
        limit = getattr(params, 'limit', None)
        offset = getattr(params, 'offset', None)

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, params, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            # Get params dict safely (dataclass or dict)
            params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots/{lot_id}/fills', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Position Lot Fills',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions/lots/{lot_id}/fills',
            params=params_dict,
            action='get_position_lot_fills'
        )

        try:
            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_position_lot_fills_api_v1_brokers_data_positions_lots_lot_id_fills_get(lot_id=lot_id, connection_id=connection_id, limit=limit, offset=offset, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # OpenAPI generator returns response - check if it's the FinaticResponse directly or wrapped in .data
            if not response:
                raise ValueError('Unexpected response shape: response is None')
            
            # Check if response has .data attribute (wrapped response) or is the FinaticResponse directly
            if hasattr(response, 'data'):
                # Response is wrapped - extract .data which contains the FinaticResponse
                response_data = response.data
                if not response_data:
                    raise ValueError('Unexpected response shape: response.data is None')
                # Serialize Pydantic model to dict
                if hasattr(response_data, 'model_dump'):
                    standard_response = response_data.model_dump(mode='json')
                elif isinstance(response_data, dict):
                    standard_response = response_data
                else:
                    raise ValueError(f'Unexpected response shape: response.data is not a Pydantic model or dict, got {type(response_data).__name__}')
            elif hasattr(response, 'success') and hasattr(response, 'error') and hasattr(response, 'warning'):
                # Response IS the FinaticResponse directly - serialize it
                if hasattr(response, 'model_dump'):
                    standard_response = response.model_dump(mode='json')
                elif isinstance(response, dict):
                    standard_response = response
                else:
                    # Fallback: try to access attributes directly
                    standard_response = {
                        'success': getattr(response, 'success', None),
                        'error': getattr(response, 'error', None),
                        'warning': getattr(response, 'warning', None),
                    }
            else:
                # Unknown response structure
                error_info = f"Response type: {type(response).__name__}, attributes: {dir(response)}"
                if hasattr(response, 'status_code'):
                    error_info += f", status_code: {response.status_code}"
                if hasattr(response, 'text'):
                    error_info += f", text: {response.text}"
                raise ValueError(f'Unexpected response shape: response is not a FinaticResponse. {error_info}')
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots/{lot_id}/fills', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Position Lot Fills completed',
                request_id=request_id,
                action='get_position_lot_fills'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Position Lot Fills failed',
                error=str(e),
                request_id=request_id,
                action='get_position_lot_fills',
                exc_info=True
            )
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
                # Try to extract error from FinaticResponse Error field
                error_response_data = getattr(e, 'body', None) or getattr(e, 'response', None)
                if error_response_data and isinstance(error_response_data, dict) and 'error' in error_response_data:
                    error_obj = error_response_data.get('error', {})
                    error_message = error_obj.get('message') or getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                    error_code = error_obj.get('code') or error_code
                    error_status = error_obj.get('status') or error_status
                else:
                    error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e, 'reason', None),
                    'responseData': getattr(e, 'body', None) or getattr(e, 'response', None),
                    'requestUrl': getattr(e, 'request', {}).get('url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e, 'request', {}).get('method', None) if hasattr(e, 'request') else None,
                }
            elif hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f'HTTP_{error_status}'
                # Try to extract error from FinaticResponse Error field
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                    if response_data and isinstance(response_data, dict) and 'error' in response_data:
                        error_obj = response_data.get('error', {})
                        error_message = error_obj.get('message') or getattr(e.response, 'text', None) or str(e)
                        error_code = error_obj.get('code') or error_code
                        error_status = error_obj.get('status') or error_status
                    else:
                        error_message = getattr(e.response, 'text', None) or str(e)
                except Exception:
                    response_data = getattr(e.response, 'text', None)
                    error_message = response_data or str(e)
                error_details = {
                    'status': error_status,
                    'statusText': getattr(e.response, 'reason', None),
                    'responseData': response_data,
                    'requestUrl': getattr(e.request, 'url', None) if hasattr(e, 'request') else None,
                    'requestMethod': getattr(e.request, 'method', None) if hasattr(e, 'request') else None,
                }
            else:
                # Generic error - include stack trace if available
                import traceback
                error_details['traceback'] = traceback.format_exc()
            
            # Phase 2C: Return standard error response structure
            error_response = FinaticResponse[list[PositionLotFillResponse]](
                success={'data': None},
                error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods
