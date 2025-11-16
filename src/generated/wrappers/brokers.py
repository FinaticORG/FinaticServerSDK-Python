"""
Generated wrapper functions for brokers operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/brokers.py instead.
"""

from typing import Optional, Any
from ..api.brokers_api import BrokersApi
from ..configuration import Configuration
from ..config import SdkConfig
from ..models.accounts import Accounts
from ..models.balances import Balances
from ..models.broker_info import BrokerInfo
from ..models.disconnect_action_result import DisconnectActionResult
from ..models.order_action_result import OrderActionResult
from ..models.order_event_response import OrderEventResponse
from ..models.order_fill_response import OrderFillResponse
from ..models.order_group_response import OrderGroupResponse
from ..models.order_response import OrderResponse
from ..models.position_lot_fill_response import PositionLotFillResponse
from ..models.position_lot_response import PositionLotResponse
from ..models.position_response import PositionResponse
from ..models.user_broker_connections import UserBrokerConnections
from ..models.order_status import OrderStatus
from ..models.order_side import OrderSide
from ..models.asset_type import AssetType
from ..models.position_status import PositionStatus
from ..models.account_type import AccountType
from ..models.account_status import AccountStatus
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

    async def get_brokers(self, with_envelope: bool = False) -> list[BrokerInfo]:
        """Get Brokers
        
        Get all available brokers.
        
        This is a fast operation that returns a cached list of available brokers.
        The list is loaded once at startup and never changes during runtime.
        
        Returns
        -------
        FinaticResponse[list[BrokerInfo]]
            list of available brokers with their metadata.

        Args:
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/
        @methodId get_brokers_api_v1_brokers__get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_brokers()
        ```
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/', {}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Brokers',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/',
            action='get_brokers'
        )

        try:
            async def api_call():
                response = await self.api.get_brokers_api_v1_brokers_get()

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/', {}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Brokers completed',
                request_id=request_id,
                action='get_brokers'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def list_broker_connections(self, with_envelope: bool = False) -> list[UserBrokerConnections]:
        """List Broker Connections
        
        List all broker connections for the current user.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns connections that the user has any permissions for.

        Args:
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/connections
        @methodId list_broker_connections_api_v1_brokers_connections_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.list_broker_connections()
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/connections', {}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('List Broker Connections',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/connections',
            action='list_broker_connections'
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/connections', {}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('List Broker Connections completed',
                request_id=request_id,
                action='list_broker_connections'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('List Broker Connections failed',
                error=str(e),
                request_id=request_id,
                action='list_broker_connections',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def disconnect_company_from_broker(self, connection_id: str, with_envelope: bool = False) -> DisconnectActionResult:
        """Disconnect Company From Broker
        
        Remove a company's access to a broker connection.
        
        If the company is the only one with access, the entire connection is deleted.
        If other companies have access, only the company's access is removed.

        Args:
        - connection_id: str
        - with_envelope: bool
        
        Generated from: DELETE /api/v1/brokers/disconnect-company/{connection_id}
        @methodId disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.disconnect_company_from_broker('example')
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {connection_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect-company/{connection_id}', {"connection_id": connection_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Disconnect Company From Broker',
            request_id=request_id,
            method='DELETE',
            path='/api/v1/brokers/disconnect-company/{connection_id}',
            connection_id=connection_id,
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect-company/{connection_id}', {"connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Disconnect Company From Broker completed',
                request_id=request_id,
                action='disconnect_company_from_broker'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_orders(self, broker_id: str = None, connection_id: str = None, account_id: str = None, symbol: str = None, order_status: OrderStatus = None, side: OrderSide = None, asset_type: AssetType = None, limit: Optional[int] = None, offset: Optional[int] = None, created_after: str = None, created_before: str = None, with_metadata: Optional[bool] = None, with_envelope: bool = False) -> list[OrderResponse]:
        """Get Orders
        
        Get orders for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns orders from connections the company has read access to.

        Args:
        - broker_id: str
        - connection_id: str
        - account_id: str
        - symbol: str
        - order_status: OrderStatus
        - side: OrderSide
        - asset_type: AssetType
        - limit: int
        - offset: int
        - created_after: str
        - created_before: str
        - with_metadata: bool
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/orders
        @methodId get_orders_api_v1_brokers_data_orders_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_orders()
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {broker_id, connection_id, account_id, symbol, order_status, side, asset_type, limit, offset, created_after, created_before, with_metadata}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "order_status": order_status, "side": side, "asset_type": asset_type, "limit": limit, "offset": offset, "created_after": created_after, "created_before": created_before, "with_metadata": with_metadata}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Orders',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders',
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "order_status": order_status, "side": side, "asset_type": asset_type, "limit": limit, "offset": offset, "created_after": created_after, "created_before": created_before, "with_metadata": with_metadata}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Orders completed',
                request_id=request_id,
                action='get_orders'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_positions(self, broker_id: str = None, connection_id: str = None, account_id: str = None, symbol: str = None, side: OrderSide = None, asset_type: AssetType = None, position_status: PositionStatus = None, limit: Optional[int] = None, offset: Optional[int] = None, updated_after: str = None, updated_before: str = None, with_metadata: Optional[bool] = None, with_envelope: bool = False) -> list[PositionResponse]:
        """Get Positions
        
        Get positions for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns positions from connections the company has read access to.

        Args:
        - broker_id: str
        - connection_id: str
        - account_id: str
        - symbol: str
        - side: OrderSide
        - asset_type: AssetType
        - position_status: PositionStatus
        - limit: int
        - offset: int
        - updated_after: str
        - updated_before: str
        - with_metadata: bool
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/positions
        @methodId get_positions_api_v1_brokers_data_positions_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_positions()
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {broker_id, connection_id, account_id, symbol, side, asset_type, position_status, limit, offset, updated_after, updated_before, with_metadata}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "side": side, "asset_type": asset_type, "position_status": position_status, "limit": limit, "offset": offset, "updated_after": updated_after, "updated_before": updated_before, "with_metadata": with_metadata}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Positions',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions',
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "side": side, "asset_type": asset_type, "position_status": position_status, "limit": limit, "offset": offset, "updated_after": updated_after, "updated_before": updated_before, "with_metadata": with_metadata}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Positions completed',
                request_id=request_id,
                action='get_positions'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_balances(self, broker_id: str = None, connection_id: str = None, account_id: str = None, is_end_of_day_snapshot: Optional[bool] = None, limit: Optional[int] = None, offset: Optional[int] = None, balance_created_after: str = None, balance_created_before: str = None, with_metadata: Optional[bool] = None, with_envelope: bool = False) -> list[Balances]:
        """Get Balances
        
        Get balances for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns balances from connections the company has read access to.

        Args:
        - broker_id: str
        - connection_id: str
        - account_id: str
        - is_end_of_day_snapshot: bool
        - limit: int
        - offset: int
        - balance_created_after: str
        - balance_created_before: str
        - with_metadata: bool
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/balances
        @methodId get_balances_api_v1_brokers_data_balances_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_balances()
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {broker_id, connection_id, account_id, is_end_of_day_snapshot, limit, offset, balance_created_after, balance_created_before, with_metadata}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/balances', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "is_end_of_day_snapshot": is_end_of_day_snapshot, "limit": limit, "offset": offset, "balance_created_after": balance_created_after, "balance_created_before": balance_created_before, "with_metadata": with_metadata}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Balances',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/balances',
            broker_id=broker_id,
            connection_id=connection_id,
            account_id=account_id,
            is_end_of_day_snapshot=is_end_of_day_snapshot,
            limit=limit,
            offset=offset,
            balance_created_after=balance_created_after,
            balance_created_before=balance_created_before,
            with_metadata=with_metadata,
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/balances', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "is_end_of_day_snapshot": is_end_of_day_snapshot, "limit": limit, "offset": offset, "balance_created_after": balance_created_after, "balance_created_before": balance_created_before, "with_metadata": with_metadata}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Balances completed',
                request_id=request_id,
                action='get_balances'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_accounts(self, broker_id: str = None, connection_id: str = None, account_type: AccountType = None, status: AccountStatus = None, currency: str = None, limit: Optional[int] = None, offset: Optional[int] = None, with_metadata: Optional[bool] = None, with_envelope: bool = False) -> list[Accounts]:
        """Get Accounts
        
        Get accounts for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns accounts from connections the company has read access to.

        Args:
        - broker_id: str
        - connection_id: str
        - account_type: AccountType
        - status: AccountStatus
        - currency: str
        - limit: int
        - offset: int
        - with_metadata: bool
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/accounts
        @methodId get_accounts_api_v1_brokers_data_accounts_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_accounts()
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {broker_id, connection_id, account_type, status, currency, limit, offset, with_metadata}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/accounts', {"broker_id": broker_id, "connection_id": connection_id, "account_type": account_type, "status": status, "currency": currency, "limit": limit, "offset": offset, "with_metadata": with_metadata}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Accounts',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/accounts',
            broker_id=broker_id,
            connection_id=connection_id,
            account_type=account_type,
            status=status,
            currency=currency,
            limit=limit,
            offset=offset,
            with_metadata=with_metadata,
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/accounts', {"broker_id": broker_id, "connection_id": connection_id, "account_type": account_type, "status": status, "currency": currency, "limit": limit, "offset": offset, "with_metadata": with_metadata}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Accounts completed',
                request_id=request_id,
                action='get_accounts'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_order_fills(self, order_id: str, connection_id: str = None, limit: Optional[int] = None, offset: Optional[int] = None, with_envelope: bool = False) -> list[OrderFillResponse]:
        """Get Order Fills
        
        Get order fills for a specific order.
        
        This endpoint returns all execution fills for the specified order.

        Args:
        - order_id: str
        - connection_id: str
        - limit: int
        - offset: int
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/orders/{order_id}/fills
        @methodId get_order_fills_api_v1_brokers_data_orders__order_id__fills_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_order_fills('example')
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {order_id, connection_id, limit, offset}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/fills', {"order_id": order_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Order Fills',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/{order_id}/fills',
            order_id=order_id,
            connection_id=connection_id,
            limit=limit,
            offset=offset,
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/fills', {"order_id": order_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Order Fills completed',
                request_id=request_id,
                action='get_order_fills'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_order_events(self, order_id: str, connection_id: str = None, limit: Optional[int] = None, offset: Optional[int] = None, with_envelope: bool = False) -> list[OrderEventResponse]:
        """Get Order Events
        
        Get order events for a specific order.
        
        This endpoint returns all lifecycle events for the specified order.

        Args:
        - order_id: str
        - connection_id: str
        - limit: int
        - offset: int
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/orders/{order_id}/events
        @methodId get_order_events_api_v1_brokers_data_orders__order_id__events_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_order_events('example')
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {order_id, connection_id, limit, offset}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/events', {"order_id": order_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Order Events',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/{order_id}/events',
            order_id=order_id,
            connection_id=connection_id,
            limit=limit,
            offset=offset,
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/events', {"order_id": order_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Order Events completed',
                request_id=request_id,
                action='get_order_events'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_order_groups(self, broker_id: str = None, connection_id: str = None, limit: Optional[int] = None, offset: Optional[int] = None, created_after: str = None, created_before: str = None, with_envelope: bool = False) -> list[OrderGroupResponse]:
        """Get Order Groups
        
        Get order groups.
        
        This endpoint returns order groups that contain multiple orders.

        Args:
        - broker_id: str
        - connection_id: str
        - limit: int
        - offset: int
        - created_after: str
        - created_before: str
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/orders/groups
        @methodId get_order_groups_api_v1_brokers_data_orders_groups_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_order_groups()
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {broker_id, connection_id, limit, offset, created_after, created_before}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/groups', {"broker_id": broker_id, "connection_id": connection_id, "limit": limit, "offset": offset, "created_after": created_after, "created_before": created_before}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Order Groups',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/orders/groups',
            broker_id=broker_id,
            connection_id=connection_id,
            limit=limit,
            offset=offset,
            created_after=created_after,
            created_before=created_before,
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/groups', {"broker_id": broker_id, "connection_id": connection_id, "limit": limit, "offset": offset, "created_after": created_after, "created_before": created_before}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Order Groups completed',
                request_id=request_id,
                action='get_order_groups'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_position_lots(self, broker_id: str = None, connection_id: str = None, account_id: str = None, symbol: str = None, position_id: str = None, limit: Optional[int] = None, offset: Optional[int] = None, with_envelope: bool = False) -> list[PositionLotResponse]:
        """Get Position Lots
        
        Get position lots (tax lots for positions).
        
        This endpoint returns tax lots for positions, which are used for tax reporting.
        Each lot tracks when a position was opened/closed and at what prices.

        Args:
        - broker_id: str
        - connection_id: str
        - account_id: str
        - symbol: str
        - position_id: str
        - limit: int
        - offset: int
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/positions/lots
        @methodId get_position_lots_api_v1_brokers_data_positions_lots_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_position_lots()
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {broker_id, connection_id, account_id, symbol, position_id, limit, offset}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "position_id": position_id, "limit": limit, "offset": offset}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Position Lots',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions/lots',
            broker_id=broker_id,
            connection_id=connection_id,
            account_id=account_id,
            symbol=symbol,
            position_id=position_id,
            limit=limit,
            offset=offset,
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "position_id": position_id, "limit": limit, "offset": offset}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Position Lots completed',
                request_id=request_id,
                action='get_position_lots'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_position_lot_fills(self, lot_id: str, connection_id: str = None, limit: Optional[int] = None, offset: Optional[int] = None, with_envelope: bool = False) -> list[PositionLotFillResponse]:
        """Get Position Lot Fills
        
        Get position lot fills for a specific lot.
        
        This endpoint returns all fills associated with a specific position lot.

        Args:
        - lot_id: str
        - connection_id: str
        - limit: int
        - offset: int
        - with_envelope: bool
        
        Generated from: GET /api/v1/brokers/data/positions/lots/{lot_id}/fills
        @methodId get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_position_lot_fills('example')
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {lot_id, connection_id, limit, offset}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots/{lot_id}/fills', {"lot_id": lot_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Position Lot Fills',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/data/positions/lots/{lot_id}/fills',
            lot_id=lot_id,
            connection_id=connection_id,
            limit=limit,
            offset=offset,
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
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots/{lot_id}/fills', {"lot_id": lot_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Position Lot Fills completed',
                request_id=request_id,
                action='get_position_lot_fills'
            )
            
            return final_result
            
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
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def place_order(self, place_order_api_v1_brokers_orders_post_request: Any = None, connection_id: str = None, with_envelope: bool = False) -> OrderActionResult:
        """Place Order
        
        Create a new order via the specified broker connection.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Requires trading permissions for the company.
        
        Standard parameters
        -------------------
        The following fields constitute the unified Finatic *common order schema* and
        therefore appear individually as query parameters in the autogenerated
        OpenAPI documentation:
        
        - ``broker``
        - ``account_number``
        - ``order_type``
        - ``asset_type``
        - ``action``
        - ``time_in_force``
        - ``symbol``
        - ``order_qty``
        
        They are surfaced as *query* parameters **only to make the accepted fields
        obvious in the interactive docs**. In production usage you should send these
        fields inside the JSON body (see ``order_request``) so that the entire order
        specification travels in one payload. (Nothing will break if you send both, but there is no need to do so.)
        
        Body payload & broker-specific extras
        -------------------------------------
        
        Put the standard parameters plus any broker-specific extensions under the
        ``order`` key of the body. Refer to the bundled OpenAPI examples below to
        see complete payloads for common order types (market, limit, spreads, etc.)
        across supported brokers.
        
        For a formal reference of broker-specific extensions inspect the
        ``BrokerOrderPlaceExtras`` schema.
        
        The endpoint resolves the active ``user_broker_connection`` by calling the
        ``get_user_broker_connection_ids_for_broker`` RPC in Supabase. If no active
        connection exists it returns a list of *available* brokers so your client
        can guide the user accordingly.
        
        Broker Notes
        ------------
        - The responses that you get back from the broker are not always the same.
        The response models are validated for each broker, but we do not standardize the repsonses.
        
        - Tasty Trade: If you want to trade options for a particular stock, first fetch the full
        option chain via the GET https://api.tastyworks.com/option-chains/{stock_symbol}/nested endpoint.
        This endpoint returns all available expirations that tastytrade offers for that equity symbol.
        Each expiration contains a list of strikes, where each strike has a call and put field representing
        the call symbol and put symbol respectively.
        
        We are planning to add a new endpoint to fetch the option chain for a particular stock and
        handle this logic for you, but for now you need to fetch the option chain manually.

        Args:
        - place_order_api_v1_brokers_orders_post_request: Any
        - connection_id: str
        - with_envelope: bool
        
        Generated from: POST /api/v1/brokers/orders
        @methodId place_order_api_v1_brokers_orders_post
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.place_order()
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {place_order_api_v1_brokers_orders_post_request, connection_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('POST', '/api/v1/brokers/orders', {"place_order_api_v1_brokers_orders_post_request": place_order_api_v1_brokers_orders_post_request, "connection_id": connection_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Place Order',
            request_id=request_id,
            method='POST',
            path='/api/v1/brokers/orders',
            place_order_api_v1_brokers_orders_post_request=place_order_api_v1_brokers_orders_post_request,
            connection_id=connection_id,
            action='place_order'
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
                response = await self.api.place_order_api_v1_brokers_orders_post(place_order_api_v1_brokers_orders_post_request=place_order_api_v1_brokers_orders_post_request, connection_id=connection_id, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('POST', '/api/v1/brokers/orders', {"place_order_api_v1_brokers_orders_post_request": place_order_api_v1_brokers_orders_post_request, "connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Place Order completed',
                request_id=request_id,
                action='place_order'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Place Order failed',
                error=str(e),
                request_id=request_id,
                action='place_order',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def cancel_order(self, order_id: str, cancel_order_api_v1_brokers_orders_order_id_delete_request: Any = None, account_number: str = None, connection_id: str = None, with_envelope: bool = False) -> OrderActionResult:
        """Cancel Order
        
        Cancel an existing order.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Requires trading permissions for the company.

        Args:
        - order_id: str
        - cancel_order_api_v1_brokers_orders_order_id_delete_request: Any
        - account_number: str
        - connection_id: str
        - with_envelope: bool
        
        Generated from: DELETE /api/v1/brokers/orders/{order_id}
        @methodId cancel_order_api_v1_brokers_orders__order_id__delete
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.cancel_order('example')
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {order_id, cancel_order_api_v1_brokers_orders_order_id_delete_request, account_number, connection_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('DELETE', '/api/v1/brokers/orders/{order_id}', {"order_id": order_id, "cancel_order_api_v1_brokers_orders_order_id_delete_request": cancel_order_api_v1_brokers_orders_order_id_delete_request, "account_number": account_number, "connection_id": connection_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Cancel Order',
            request_id=request_id,
            method='DELETE',
            path='/api/v1/brokers/orders/{order_id}',
            order_id=order_id,
            cancel_order_api_v1_brokers_orders_order_id_delete_request=cancel_order_api_v1_brokers_orders_order_id_delete_request,
            account_number=account_number,
            connection_id=connection_id,
            action='cancel_order'
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
                response = await self.api.cancel_order_api_v1_brokers_orders_order_id_delete(order_id=order_id, cancel_order_api_v1_brokers_orders_order_id_delete_request=cancel_order_api_v1_brokers_orders_order_id_delete_request, account_number=account_number, connection_id=connection_id, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('DELETE', '/api/v1/brokers/orders/{order_id}', {"order_id": order_id, "cancel_order_api_v1_brokers_orders_order_id_delete_request": cancel_order_api_v1_brokers_orders_order_id_delete_request, "account_number": account_number, "connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Cancel Order completed',
                request_id=request_id,
                action='cancel_order'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Cancel Order failed',
                error=str(e),
                request_id=request_id,
                action='cancel_order',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def modify_order(self, order_id: str, modify_order_api_v1_brokers_orders_order_id_patch_request: Any = None, account_number: str = None, connection_id: str = None, with_envelope: bool = False) -> OrderActionResult:
        """Modify Order
        
        Modify an existing order.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Requires trading permissions for the company.

        Args:
        - order_id: str
        - modify_order_api_v1_brokers_orders_order_id_patch_request: Any
        - account_number: str
        - connection_id: str
        - with_envelope: bool
        
        Generated from: PATCH /api/v1/brokers/orders/{order_id}
        @methodId modify_order_api_v1_brokers_orders__order_id__patch
        @category brokers
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.modify_order('example')
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {order_id, modify_order_api_v1_brokers_orders_order_id_patch_request, account_number, connection_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('PATCH', '/api/v1/brokers/orders/{order_id}', {"order_id": order_id, "modify_order_api_v1_brokers_orders_order_id_patch_request": modify_order_api_v1_brokers_orders_order_id_patch_request, "account_number": account_number, "connection_id": connection_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Modify Order',
            request_id=request_id,
            method='PATCH',
            path='/api/v1/brokers/orders/{order_id}',
            order_id=order_id,
            modify_order_api_v1_brokers_orders_order_id_patch_request=modify_order_api_v1_brokers_orders_order_id_patch_request,
            account_number=account_number,
            connection_id=connection_id,
            action='modify_order'
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
                response = await self.api.modify_order_api_v1_brokers_orders_order_id_patch(order_id=order_id, modify_order_api_v1_brokers_orders_order_id_patch_request=modify_order_api_v1_brokers_orders_order_id_patch_request, account_number=account_number, connection_id=connection_id, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Canonical unwrap: expect .data on response
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            result = response.data
            
            if with_envelope is True:
                warnings = response.warnings if hasattr(response, 'warnings') else None
                meta = response.meta if hasattr(response, 'meta') else None
                envelope = {'data': result}
                if warnings:
                    envelope['warnings'] = warnings
                if meta:
                    envelope['meta'] = meta
                return envelope
            
            final_result = result
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('PATCH', '/api/v1/brokers/orders/{order_id}', {"order_id": order_id, "modify_order_api_v1_brokers_orders_order_id_patch_request": modify_order_api_v1_brokers_orders_order_id_patch_request, "account_number": account_number, "connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Modify Order completed',
                request_id=request_id,
                action='modify_order'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Modify Order failed',
                error=str(e),
                request_id=request_id,
                action='modify_order',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods
