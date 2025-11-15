"""
Generated wrapper functions for brokers operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/brokers.py instead.
"""

from typing import Optional, Any
from ..api.brokers_api import BrokersApi
from ..configuration import Configuration
from ..config import SdkConfig
from ..models.broker_connection_request import BrokerConnectionRequest
from ..models.broker_connection_update_request import BrokerConnectionUpdateRequest
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

    async def get_brokers(self, ) -> list:
        """Get Brokers
        
                Get all available brokers.
        
        This is a fast operation that returns a cached list of available brokers.
        The list is loaded once at startup and never changes during runtime.
        
        Returns
        -------
        FinaticResponse[list[BrokerInfo]]
            list of available brokers with their metadata.
        
        Generated from: GET /api/v1/brokers/
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.get_brokers_api_v1_brokers_get()

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/', {}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Brokers completed',
                request_id=request_id,
                action='get_brokers'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def connect_broker(self, broker_connection_request: BrokerConnectionRequest) -> Any:
        """Connect Broker
        
                Connect to a broker or reconnect to an existing connection.
        
        This endpoint handles both new connections and reconnections:
        - New connections: Provide broker_id, credentials, and permissions
        - Reconnections: Provide connection_id, broker_id, credentials, and permissions
        
        For reconnections, the connection must be in "needs_reauth" status.
        
        Generated from: POST /api/v1/brokers/connect
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
            # validate_params(validation_model, {broker_connection_request}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('POST', '/api/v1/brokers/connect', {"broker_connection_request": broker_connection_request}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Connect Broker',
            request_id=request_id,
            method='POST',
            path='/api/v1/brokers/connect',
            broker_connection_request=broker_connection_request,
            action='connect_broker'
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.connect_broker_api_v1_brokers_connect_post(broker_connection_request=broker_connection_request, _headers=headers)

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('POST', '/api/v1/brokers/connect', {"broker_connection_request": broker_connection_request}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Connect Broker completed',
                request_id=request_id,
                action='connect_broker'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass
            
            self.logger.error('Connect Broker failed',
                error=str(e),
                request_id=request_id,
                action='connect_broker',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def list_broker_connections(self, ) -> list:
        """List Broker Connections
        
                List all broker connections for the current user.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns connections that the user has any permissions for.
        
        Generated from: GET /api/v1/brokers/connections
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/connections', {}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('List Broker Connections completed',
                request_id=request_id,
                action='list_broker_connections'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def update_connection(self, connection_id: str, broker_connection_update_request: BrokerConnectionUpdateRequest) -> UserBrokerConnections:
        """Update Connection
        
                Update a broker connection's permissions.
        
        Generated from: PUT /api/v1/brokers/connections/{connection_id}
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
            # validate_params(validation_model, {connection_id, broker_connection_update_request}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('PUT', '/api/v1/brokers/connections/{connection_id}', {"connection_id": connection_id, "broker_connection_update_request": broker_connection_update_request}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Update Connection',
            request_id=request_id,
            method='PUT',
            path='/api/v1/brokers/connections/{connection_id}',
            connection_id=connection_id,
            broker_connection_update_request=broker_connection_update_request,
            action='update_connection'
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.update_connection_api_v1_brokers_connections_connection_id_put(connection_id=connection_id, broker_connection_update_request=broker_connection_update_request, _headers=headers)

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('PUT', '/api/v1/brokers/connections/{connection_id}', {"connection_id": connection_id, "broker_connection_update_request": broker_connection_update_request}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Update Connection completed',
                request_id=request_id,
                action='update_connection'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass
            
            self.logger.error('Update Connection failed',
                error=str(e),
                request_id=request_id,
                action='update_connection',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def delete_connection(self, connection_id: str) -> Any:
        """Delete Connection
        
                Delete a broker connection.
        
        Generated from: DELETE /api/v1/brokers/connections/{connection_id}
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('DELETE', '/api/v1/brokers/connections/{connection_id}', {"connection_id": connection_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Delete Connection',
            request_id=request_id,
            method='DELETE',
            path='/api/v1/brokers/connections/{connection_id}',
            connection_id=connection_id,
            action='delete_connection'
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.delete_connection_api_v1_brokers_connections_connection_id_delete(connection_id=connection_id, _headers=headers)

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('DELETE', '/api/v1/brokers/connections/{connection_id}', {"connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Delete Connection completed',
                request_id=request_id,
                action='delete_connection'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass
            
            self.logger.error('Delete Connection failed',
                error=str(e),
                request_id=request_id,
                action='delete_connection',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def disconnect_broker(self, connection_id: str) -> Any:
        """Disconnect Broker
        
                Disconnect a broker connection.
        
        Generated from: DELETE /api/v1/brokers/disconnect/{connection_id}
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect/{connection_id}', {"connection_id": connection_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Disconnect Broker',
            request_id=request_id,
            method='DELETE',
            path='/api/v1/brokers/disconnect/{connection_id}',
            connection_id=connection_id,
            action='disconnect_broker'
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
                if not self.session_id or not self.company_id:
                    raise ValueError("Session context incomplete. Missing sessionId or companyId.")
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.disconnect_broker_api_v1_brokers_disconnect_connection_id_delete(connection_id=connection_id, _headers=headers)

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect/{connection_id}', {"connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Disconnect Broker completed',
                request_id=request_id,
                action='disconnect_broker'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass
            
            self.logger.error('Disconnect Broker failed',
                error=str(e),
                request_id=request_id,
                action='disconnect_broker',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def disconnect_company_from_broker(self, connection_id: str) -> Any:
        """Disconnect Company From Broker
        
                Remove a company's access to a broker connection.
        
        If the company is the only one with access, the entire connection is deleted.
        If other companies have access, only the company's access is removed.
        
        Generated from: DELETE /api/v1/brokers/disconnect-company/{connection_id}
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('DELETE', '/api/v1/brokers/disconnect-company/{connection_id}', {"connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Disconnect Company From Broker completed',
                request_id=request_id,
                action='disconnect_company_from_broker'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_orders(self, broker_id: Any = None, connection_id: Any = None, account_id: Any = None, symbol: Any = None, order_status: Any = None, side: Any = None, asset_type: Any = None, limit: Optional[int] = None, offset: Optional[int] = None, created_after: Any = None, created_before: Any = None, with_metadata: Optional[bool] = None) -> list:
        """Get Orders
        
                Get orders for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns orders from connections the company has read access to.
        
        Generated from: GET /api/v1/brokers/data/orders
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            # Transform to metadata structure if with_metadata is True
            if with_metadata is True:
                # If result has response_data (snake_case from API), transform it
                if result and isinstance(result, dict) and 'response_data' in result:
                    data_array = result['response_data'] if isinstance(result.get('response_data'), list) else []
                    metadata = {}
                    
                    # Extract pagination if present
                    if result.get('pagination') and isinstance(result.get('pagination'), dict):
                        metadata['pagination'] = result['pagination']
                        if result['pagination'].get('has_more') is not None:
                            metadata['has_more'] = result['pagination']['has_more']
                    
                    # Extract warnings if present
                    if result.get('warnings') and isinstance(result.get('warnings'), list):
                        metadata['warnings'] = result['warnings']
                    
                    # Extract errors if present
                    if result.get('errors') and isinstance(result.get('errors'), list):
                        metadata['errors'] = result['errors']
                    
                    self.logger.debug('get_orders returning metadata structure from response_data',
                        data_length=len(data_array),
                        has_pagination=bool(metadata.get('pagination')),
                        has_warnings=bool(metadata.get('warnings')),
                        has_errors=bool(metadata.get('errors')),
                    )
                    
                    final_result = {'data': data_array, 'metadata': metadata}
                elif result and isinstance(result, dict) and 'data' in result and 'metadata' in result and isinstance(result.get('data'), list):
                    # If result already has data and metadata structure, return as-is
                    self.logger.debug('get_orders returning metadata structure from unwrapped result',
                        data_length=len(result.get('data', [])),
                        has_metadata=bool(result.get('metadata')),
                    )
                    final_result = result
                else:
                    # Otherwise, return list (or empty list if not a list)
                    final_result = result if isinstance(result, list) else []
                    self.logger.debug('get_orders returning list (no metadata structure found)',
                        list_length=len(final_result),
                        result_type=type(result).__name__,
                        result_keys=list(result.keys()) if isinstance(result, dict) else [],
                    )
            else:
                # If with_metadata is False or None, return list (or empty list if not a list)
                final_result = result if isinstance(result, list) else []
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "order_status": order_status, "side": side, "asset_type": asset_type, "limit": limit, "offset": offset, "created_after": created_after, "created_before": created_before, "with_metadata": with_metadata}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Orders completed',
                request_id=request_id,
                action='get_orders'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_positions(self, broker_id: Any = None, connection_id: Any = None, account_id: Any = None, symbol: Any = None, side: Any = None, asset_type: Any = None, position_status: Any = None, limit: Optional[int] = None, offset: Optional[int] = None, updated_after: Any = None, updated_before: Any = None, with_metadata: Optional[bool] = None) -> list:
        """Get Positions
        
                Get positions for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns positions from connections the company has read access to.
        
        Generated from: GET /api/v1/brokers/data/positions
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            # Transform to metadata structure if with_metadata is True
            if with_metadata is True:
                # If result has response_data (snake_case from API), transform it
                if result and isinstance(result, dict) and 'response_data' in result:
                    data_array = result['response_data'] if isinstance(result.get('response_data'), list) else []
                    metadata = {}
                    
                    # Extract pagination if present
                    if result.get('pagination') and isinstance(result.get('pagination'), dict):
                        metadata['pagination'] = result['pagination']
                        if result['pagination'].get('has_more') is not None:
                            metadata['has_more'] = result['pagination']['has_more']
                    
                    # Extract warnings if present
                    if result.get('warnings') and isinstance(result.get('warnings'), list):
                        metadata['warnings'] = result['warnings']
                    
                    # Extract errors if present
                    if result.get('errors') and isinstance(result.get('errors'), list):
                        metadata['errors'] = result['errors']
                    
                    self.logger.debug('get_positions returning metadata structure from response_data',
                        data_length=len(data_array),
                        has_pagination=bool(metadata.get('pagination')),
                        has_warnings=bool(metadata.get('warnings')),
                        has_errors=bool(metadata.get('errors')),
                    )
                    
                    final_result = {'data': data_array, 'metadata': metadata}
                elif result and isinstance(result, dict) and 'data' in result and 'metadata' in result and isinstance(result.get('data'), list):
                    # If result already has data and metadata structure, return as-is
                    self.logger.debug('get_positions returning metadata structure from unwrapped result',
                        data_length=len(result.get('data', [])),
                        has_metadata=bool(result.get('metadata')),
                    )
                    final_result = result
                else:
                    # Otherwise, return list (or empty list if not a list)
                    final_result = result if isinstance(result, list) else []
                    self.logger.debug('get_positions returning list (no metadata structure found)',
                        list_length=len(final_result),
                        result_type=type(result).__name__,
                        result_keys=list(result.keys()) if isinstance(result, dict) else [],
                    )
            else:
                # If with_metadata is False or None, return list (or empty list if not a list)
                final_result = result if isinstance(result, list) else []
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "side": side, "asset_type": asset_type, "position_status": position_status, "limit": limit, "offset": offset, "updated_after": updated_after, "updated_before": updated_before, "with_metadata": with_metadata}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Positions completed',
                request_id=request_id,
                action='get_positions'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_balances(self, broker_id: Any = None, connection_id: Any = None, account_id: Any = None, is_end_of_day_snapshot: Any = None, limit: Optional[int] = None, offset: Optional[int] = None, balance_created_after: Any = None, balance_created_before: Any = None, with_metadata: Optional[bool] = None) -> list:
        """Get Balances
        
                Get balances for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns balances from connections the company has read access to.
        
        Generated from: GET /api/v1/brokers/data/balances
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            # Transform to metadata structure if with_metadata is True
            if with_metadata is True:
                # If result has response_data (snake_case from API), transform it
                if result and isinstance(result, dict) and 'response_data' in result:
                    data_array = result['response_data'] if isinstance(result.get('response_data'), list) else []
                    metadata = {}
                    
                    # Extract pagination if present
                    if result.get('pagination') and isinstance(result.get('pagination'), dict):
                        metadata['pagination'] = result['pagination']
                        if result['pagination'].get('has_more') is not None:
                            metadata['has_more'] = result['pagination']['has_more']
                    
                    # Extract warnings if present
                    if result.get('warnings') and isinstance(result.get('warnings'), list):
                        metadata['warnings'] = result['warnings']
                    
                    # Extract errors if present
                    if result.get('errors') and isinstance(result.get('errors'), list):
                        metadata['errors'] = result['errors']
                    
                    self.logger.debug('get_balances returning metadata structure from response_data',
                        data_length=len(data_array),
                        has_pagination=bool(metadata.get('pagination')),
                        has_warnings=bool(metadata.get('warnings')),
                        has_errors=bool(metadata.get('errors')),
                    )
                    
                    final_result = {'data': data_array, 'metadata': metadata}
                elif result and isinstance(result, dict) and 'data' in result and 'metadata' in result and isinstance(result.get('data'), list):
                    # If result already has data and metadata structure, return as-is
                    self.logger.debug('get_balances returning metadata structure from unwrapped result',
                        data_length=len(result.get('data', [])),
                        has_metadata=bool(result.get('metadata')),
                    )
                    final_result = result
                else:
                    # Otherwise, return list (or empty list if not a list)
                    final_result = result if isinstance(result, list) else []
                    self.logger.debug('get_balances returning list (no metadata structure found)',
                        list_length=len(final_result),
                        result_type=type(result).__name__,
                        result_keys=list(result.keys()) if isinstance(result, dict) else [],
                    )
            else:
                # If with_metadata is False or None, return list (or empty list if not a list)
                final_result = result if isinstance(result, list) else []
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/balances', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "is_end_of_day_snapshot": is_end_of_day_snapshot, "limit": limit, "offset": offset, "balance_created_after": balance_created_after, "balance_created_before": balance_created_before, "with_metadata": with_metadata}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Balances completed',
                request_id=request_id,
                action='get_balances'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_accounts(self, broker_id: Any = None, connection_id: Any = None, account_type: Any = None, status: Any = None, currency: Any = None, limit: Optional[int] = None, offset: Optional[int] = None, with_metadata: Any = None) -> list:
        """Get Accounts
        
                Get accounts for all authorized broker connections.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Returns accounts from connections the company has read access to.
        
        Generated from: GET /api/v1/brokers/data/accounts
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            # Transform to metadata structure if with_metadata is True
            if with_metadata is True:
                # If result has response_data (snake_case from API), transform it
                if result and isinstance(result, dict) and 'response_data' in result:
                    data_array = result['response_data'] if isinstance(result.get('response_data'), list) else []
                    metadata = {}
                    
                    # Extract pagination if present
                    if result.get('pagination') and isinstance(result.get('pagination'), dict):
                        metadata['pagination'] = result['pagination']
                        if result['pagination'].get('has_more') is not None:
                            metadata['has_more'] = result['pagination']['has_more']
                    
                    # Extract warnings if present
                    if result.get('warnings') and isinstance(result.get('warnings'), list):
                        metadata['warnings'] = result['warnings']
                    
                    # Extract errors if present
                    if result.get('errors') and isinstance(result.get('errors'), list):
                        metadata['errors'] = result['errors']
                    
                    self.logger.debug('get_accounts returning metadata structure from response_data',
                        data_length=len(data_array),
                        has_pagination=bool(metadata.get('pagination')),
                        has_warnings=bool(metadata.get('warnings')),
                        has_errors=bool(metadata.get('errors')),
                    )
                    
                    final_result = {'data': data_array, 'metadata': metadata}
                elif result and isinstance(result, dict) and 'data' in result and 'metadata' in result and isinstance(result.get('data'), list):
                    # If result already has data and metadata structure, return as-is
                    self.logger.debug('get_accounts returning metadata structure from unwrapped result',
                        data_length=len(result.get('data', [])),
                        has_metadata=bool(result.get('metadata')),
                    )
                    final_result = result
                else:
                    # Otherwise, return list (or empty list if not a list)
                    final_result = result if isinstance(result, list) else []
                    self.logger.debug('get_accounts returning list (no metadata structure found)',
                        list_length=len(final_result),
                        result_type=type(result).__name__,
                        result_keys=list(result.keys()) if isinstance(result, dict) else [],
                    )
            else:
                # If with_metadata is False or None, return list (or empty list if not a list)
                final_result = result if isinstance(result, list) else []
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/accounts', {"broker_id": broker_id, "connection_id": connection_id, "account_type": account_type, "status": status, "currency": currency, "limit": limit, "offset": offset, "with_metadata": with_metadata}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Accounts completed',
                request_id=request_id,
                action='get_accounts'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_order_fills(self, order_id: str, connection_id: Any = None, limit: Optional[int] = None, offset: Optional[int] = None) -> list:
        """Get Order Fills
        
                Get order fills for a specific order.
        
        This endpoint returns all execution fills for the specified order.
        
        Generated from: GET /api/v1/brokers/data/orders/{order_id}/fills
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/fills', {"order_id": order_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Order Fills completed',
                request_id=request_id,
                action='get_order_fills'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_order_events(self, order_id: str, connection_id: Any = None, limit: Optional[int] = None, offset: Optional[int] = None) -> list:
        """Get Order Events
        
                Get order events for a specific order.
        
        This endpoint returns all lifecycle events for the specified order.
        
        Generated from: GET /api/v1/brokers/data/orders/{order_id}/events
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/{order_id}/events', {"order_id": order_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Order Events completed',
                request_id=request_id,
                action='get_order_events'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_order_groups(self, broker_id: Any = None, connection_id: Any = None, limit: Optional[int] = None, offset: Optional[int] = None, created_after: Any = None, created_before: Any = None) -> list:
        """Get Order Groups
        
                Get order groups.
        
        This endpoint returns order groups that contain multiple orders.
        
        Generated from: GET /api/v1/brokers/data/orders/groups
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/orders/groups', {"broker_id": broker_id, "connection_id": connection_id, "limit": limit, "offset": offset, "created_after": created_after, "created_before": created_before}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Order Groups completed',
                request_id=request_id,
                action='get_order_groups'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_position_lots(self, broker_id: Any = None, connection_id: Any = None, account_id: Any = None, symbol: Any = None, position_id: Any = None, limit: Optional[int] = None, offset: Optional[int] = None) -> list:
        """Get Position Lots
        
                Get position lots (tax lots for positions).
        
        This endpoint returns tax lots for positions, which are used for tax reporting.
        Each lot tracks when a position was opened/closed and at what prices.
        
        Generated from: GET /api/v1/brokers/data/positions/lots
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots', {"broker_id": broker_id, "connection_id": connection_id, "account_id": account_id, "symbol": symbol, "position_id": position_id, "limit": limit, "offset": offset}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Position Lots completed',
                request_id=request_id,
                action='get_position_lots'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def get_position_lot_fills(self, lot_id: str, connection_id: Any = None, limit: Optional[int] = None, offset: Optional[int] = None) -> list:
        """Get Position Lot Fills
        
                Get position lot fills for a specific lot.
        
        This endpoint returns all fills associated with a specific position lot.
        
        Generated from: GET /api/v1/brokers/data/positions/lots/{lot_id}/fills
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/data/positions/lots/{lot_id}/fills', {"lot_id": lot_id, "connection_id": connection_id, "limit": limit, "offset": offset}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Get Position Lot Fills completed',
                request_id=request_id,
                action='get_position_lot_fills'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def sandbox_callback(self, broker_id: str) -> Any:
        """Sandbox Callback
        
                Handle sandbox authentication callback.
        
        This endpoint handles the completion of sandbox authentication flows.
        It creates sandbox connections with mock data instead of real broker connections.
        
        Generated from: GET /api/v1/brokers/sandbox-callback/{broker_id}
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {broker_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/sandbox-callback/{broker_id}', {"broker_id": broker_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Sandbox Callback',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/sandbox-callback/{broker_id}',
            broker_id=broker_id,
            action='sandbox_callback'
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.sandbox_callback_api_v1_brokers_sandbox_callback_broker_id_get(broker_id=broker_id)

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/sandbox-callback/{broker_id}', {"broker_id": broker_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Sandbox Callback completed',
                request_id=request_id,
                action='sandbox_callback'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass
            
            self.logger.error('Sandbox Callback failed',
                error=str(e),
                request_id=request_id,
                action='sandbox_callback',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def oauth_callback_tastytrade(self, ) -> Any:
        """Oauth Callback Tastytrade
        
                Handle OAuth callback for TastyTrade sandbox authentication.
        
        This endpoint serves as the redirect URI for TastyTrade OAuth flows in sandbox mode.
        It captures all query parameters from the callback URL and completes the authentication
        process with TastyTrade. All authentication data is passed via URL query parameters
        as per OAuth 2.0 specification.
        
        Parameters
        ----------
        request : Request
            FastAPI request object containing the callback URL with OAuth parameters
        
        Returns
        -------
        HTMLResponse
            Returns HTML that closes the popup and notifies the parent window
        
        Generated from: GET /api/v1/brokers/callback/tastytrade
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/callback/tastytrade', {}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Oauth Callback Tastytrade',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/callback/tastytrade',
            action='oauth_callback_tastytrade'
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.oauth_callback_tastytrade_api_v1_brokers_callback_tastytrade_get()

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/callback/tastytrade', {}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Oauth Callback Tastytrade completed',
                request_id=request_id,
                action='oauth_callback_tastytrade'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass
            
            self.logger.error('Oauth Callback Tastytrade failed',
                error=str(e),
                request_id=request_id,
                action='oauth_callback_tastytrade',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def oauth_callback(self, broker_id: str) -> Any:
        """Oauth Callback
        
                Handle OAuth callback for broker authentication.
        
        This endpoint serves as the redirect URI for OAuth flows. It captures
        all query parameters from the callback URL and completes the authentication
        process with the specified broker. All authentication data is passed via
        URL query parameters as per OAuth 2.0 specification.
        
        Parameters
        ----------
        broker_id : str
            The ID of the broker handling the OAuth callback
        request : Request
            FastAPI request object containing the callback URL with OAuth parameters
        
        Returns
        -------
        HTMLResponse
            Returns HTML that closes the popup and notifies the parent window
        
        Generated from: GET /api/v1/brokers/callback/{broker_id}
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {broker_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/brokers/callback/{broker_id}', {"broker_id": broker_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Oauth Callback',
            request_id=request_id,
            method='GET',
            path='/api/v1/brokers/callback/{broker_id}',
            broker_id=broker_id,
            action='oauth_callback'
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.oauth_callback_api_v1_brokers_callback_broker_id_get(broker_id=broker_id)

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('GET', '/api/v1/brokers/callback/{broker_id}', {"broker_id": broker_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Oauth Callback completed',
                request_id=request_id,
                action='oauth_callback'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass
            
            self.logger.error('Oauth Callback failed',
                error=str(e),
                request_id=request_id,
                action='oauth_callback',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def place_order(self, place_order_api_v1_brokers_orders_post_request: Any = None, connection_id: Any = None) -> Any:
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
        
        Generated from: POST /api/v1/brokers/orders
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('POST', '/api/v1/brokers/orders', {"place_order_api_v1_brokers_orders_post_request": place_order_api_v1_brokers_orders_post_request, "connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Place Order completed',
                request_id=request_id,
                action='place_order'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def cancel_order(self, order_id: str, cancel_order_api_v1_brokers_orders_order_id_delete_request: Any = None, account_number: Any = None, connection_id: Any = None) -> Any:
        """Cancel Order
        
                Cancel an existing order.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Requires trading permissions for the company.
        
        Generated from: DELETE /api/v1/brokers/orders/{order_id}
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('DELETE', '/api/v1/brokers/orders/{order_id}', {"order_id": order_id, "cancel_order_api_v1_brokers_orders_order_id_delete_request": cancel_order_api_v1_brokers_orders_order_id_delete_request, "account_number": account_number, "connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Cancel Order completed',
                request_id=request_id,
                action='cancel_order'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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

    async def modify_order(self, order_id: str, modify_order_api_v1_brokers_orders_order_id_patch_request: Any = None, account_number: Any = None, connection_id: Any = None) -> Any:
        """Modify Order
        
                Modify an existing order.
        
        This endpoint is accessible from the portal and uses session-only authentication.
        Requires trading permissions for the company.
        
        Generated from: PATCH /api/v1/brokers/orders/{order_id}
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
        # Portal URLs are single-use tokens - must NOT be cached
        should_cache = not False
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
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                # Get session headers for broker endpoints
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

                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Unwrap FinaticResponse wrapper if present
            # The API might return FinaticResponse[Model] (with .data property) or FinaticResponseList[...] (with .response_data property)
            if response and hasattr(response, 'response_data') and response.response_data is not None:
                # Unwrap FinaticResponseList wrapper (e.g., FinaticResponseListUserBrokerConnections -> List[UserBrokerConnections])
                result = response.response_data
            elif response and hasattr(response, 'data') and response.data:
                # Unwrap FinaticResponse wrapper (e.g., FinaticResponseTokenResponseData -> TokenResponseData)
                result = response.data
            else:
                # Response is already unwrapped (e.g., TokenResponseData, List[...])
                result = response
            

            final_result = result
            

            # Store in cache (Phase 2B)
            # Portal URLs are single-use tokens - must NOT be cached
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                cache_key = generate_cache_key('PATCH', '/api/v1/brokers/orders/{order_id}', {"order_id": order_id, "modify_order_api_v1_brokers_orders_order_id_patch_request": modify_order_api_v1_brokers_orders_order_id_patch_request, "account_number": account_number, "connection_id": connection_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            # Structured logging (Phase 2B)
            self.logger.debug('Modify Order completed',
                request_id=request_id,
                action='modify_order'
            )
            
            return final_result
            
        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
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
