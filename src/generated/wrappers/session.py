"""
Generated wrapper functions for session operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/session.py instead.
"""

from typing import Optional, Any
from ..api.session_api import SessionApi
from ..configuration import Configuration
from ..config import SdkConfig
from ..models.direct_auth_request import DirectAuthRequest
from ..models.portal_url_response import PortalUrlResponse
from ..models.session_response_data import SessionResponseData
from ..models.session_start_request import SessionStartRequest
from ..models.session_user_response import SessionUserResponse
from ..models.test_webhook_response import TestWebhookResponse
from ..models.token_data import TokenData
from ..models.token_response_data import TokenResponseData
from ..models.finaticapi_api_v1_routers_session_session_router_test_webhook_request import FinaticapiApiV1RoutersSessionSessionRouterTestWebhookRequest
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


class SessionWrapper:
    """Session wrapper functions.
    
    Provides simplified method names and response unwrapping.
    """
    
    def __init__(self, api: SessionApi, config: Optional[Configuration] = None, sdk_config: Optional[SdkConfig] = None):
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

    async def init_session(self, x_api_key: str, with_envelope: bool = False) -> TokenResponseData:
        """Init Session
        
        Initialize a new session with company API key.

        Args:
        - x_api_key: str
        - with_envelope: bool
        
        Generated from: POST /api/v1/session/init
        @methodId init_session_api_v1_session_init_post
        @category session
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.init_session('example')
        ```
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {x_api_key}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('POST', '/api/v1/session/init', {"x_api_key": x_api_key}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Init Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/init',
            x_api_key=x_api_key,
            action='init_session'
        )

        try:
            async def api_call():
                response = await self.api.init_session_api_v1_session_init_post(x_api_key=x_api_key)

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
                cache_key = generate_cache_key('POST', '/api/v1/session/init', {"x_api_key": x_api_key}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Init Session completed',
                request_id=request_id,
                action='init_session'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Init Session failed',
                error=str(e),
                request_id=request_id,
                action='init_session',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def start_session(self, one_time_token: str, session_start_request: SessionStartRequest, with_envelope: bool = False) -> SessionResponseData:
        """Start Session
        
        Start a session with a one-time token.

        Args:
        - one_time_token: str
        - session_start_request: SessionStartRequest
        - with_envelope: bool
        
        Generated from: POST /api/v1/session/start
        @methodId start_session_api_v1_session_start_post
        @category session
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.start_session('example', {})
        ```
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {one_time_token, session_start_request}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('POST', '/api/v1/session/start', {"one_time_token": one_time_token, "session_start_request": session_start_request}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Start Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/start',
            one_time_token=one_time_token,
            session_start_request=session_start_request,
            action='start_session'
        )

        try:
            async def api_call():
                response = await self.api.start_session_api_v1_session_start_post(one_time_token=one_time_token, session_start_request=session_start_request)

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
                cache_key = generate_cache_key('POST', '/api/v1/session/start', {"one_time_token": one_time_token, "session_start_request": session_start_request}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Start Session completed',
                request_id=request_id,
                action='start_session'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Start Session failed',
                error=str(e),
                request_id=request_id,
                action='start_session',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_portal_url(self, with_envelope: bool = False) -> PortalUrlResponse:
        """Get Portal Url
        
        Get a portal URL with token for a session.
        
        The session must be in ACTIVE or AUTHENTICATING state and the request must come from the same device
        that initiated the session. Device info is automatically validated from the request.

        Args:
        - with_envelope: bool
        
        Generated from: GET /api/v1/session/portal
        @methodId get_portal_url_api_v1_session_portal_get
        @category session
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_portal_url()
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
            cache_key = generate_cache_key('GET', '/api/v1/session/portal', {}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Portal Url',
            request_id=request_id,
            method='GET',
            path='/api/v1/session/portal',
            action='get_portal_url'
        )

        try:
            async def api_call():
                response = await self.api.get_portal_url_api_v1_session_portal_get(session_id=self.session_id)

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
                cache_key = generate_cache_key('GET', '/api/v1/session/portal', {}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Portal Url completed',
                request_id=request_id,
                action='get_portal_url'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Portal Url failed',
                error=str(e),
                request_id=request_id,
                action='get_portal_url',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_session_user(self, session_id: str, with_envelope: bool = False) -> SessionUserResponse:
        """Get Session User
        
        Get user information and fresh tokens for a completed session.
        
        This endpoint is designed for server SDKs to retrieve user information
        and authentication tokens after successful OTP verification.
        
        
        Security:
        - Requires valid session in ACTIVE state
        - Validates device fingerprint binding
        - Generates fresh tokens (not returning stored ones)
        - Only accessible to authenticated sessions with user_id

        Args:
        - session_id: str
        - with_envelope: bool
        
        Generated from: GET /api/v1/session/{session_id}/user
        @methodId get_session_user_api_v1_session__session_id__user_get
        @category session
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.get_session_user('example')
        ```
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {session_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('GET', '/api/v1/session/{session_id}/user', {"session_id": session_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Get Session User',
            request_id=request_id,
            method='GET',
            path='/api/v1/session/{session_id}/user',
            session_id=session_id,
            action='get_session_user'
        )

        try:
            async def api_call():
                response = await self.api.get_session_user_api_v1_session_session_id_user_get(session_id=session_id, company_id=self.company_id)

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
                cache_key = generate_cache_key('GET', '/api/v1/session/{session_id}/user', {"session_id": session_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Get Session User completed',
                request_id=request_id,
                action='get_session_user'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Get Session User failed',
                error=str(e),
                request_id=request_id,
                action='get_session_user',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def authenticate_session(self, session_id: str, user_id: str, with_envelope: bool = False) -> TokenData:
        """Authenticate Session
        


        Args:
        - session_id: str
        - user_id: str
        - with_envelope: bool
        
        Generated from: POST /api/v1/session/authenticate
        @methodId authenticate_session_api_v1_session_authenticate_post
        @category session
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.authenticate_session('example', 'example')
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
            # validate_params(validation_model, {session_id, user_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('POST', '/api/v1/session/authenticate', {"session_id": session_id, "user_id": user_id}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Authenticate Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/authenticate',
            session_id=session_id,
            user_id=user_id,
            action='authenticate_session'
        )

        try:
            async def api_call():
                response = await self.api.authenticate_session_api_v1_session_authenticate_post(direct_auth_request={'session_id': session_id, 'user_id': user_id})

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
                cache_key = generate_cache_key('POST', '/api/v1/session/authenticate', {"session_id": session_id, "user_id": user_id}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Authenticate Session completed',
                request_id=request_id,
                action='authenticate_session'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Authenticate Session failed',
                error=str(e),
                request_id=request_id,
                action='authenticate_session',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def refresh_session(self, with_envelope: bool = False) -> SessionResponseData:
        """Refresh Session
        
        Refresh an existing session by extending its expiration time.
        
        This endpoint allows users to extend their session before it expires.
        The session will be extended by the default duration (24 hours).

        Args:
        - with_envelope: bool
        
        Generated from: POST /api/v1/session/refresh
        @methodId refresh_session_api_v1_session_refresh_post
        @category session
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.refresh_session()
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
            cache_key = generate_cache_key('POST', '/api/v1/session/refresh', {}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Refresh Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/refresh',
            action='refresh_session'
        )

        try:
            async def api_call():
                response = await self.api.refresh_session_api_v1_session_refresh_post()

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
                cache_key = generate_cache_key('POST', '/api/v1/session/refresh', {}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Refresh Session completed',
                request_id=request_id,
                action='refresh_session'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Refresh Session failed',
                error=str(e),
                request_id=request_id,
                action='refresh_session',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def test_webhook(self, event_type: str, sample_data: dict = None, with_envelope: bool = False) -> TestWebhookResponse:
        """Test Webhook
        
        Send a test webhook for the specified event type to the company's configured endpoints.

        Args:
        - event_type: str
        - sample_data: dict
        - with_envelope: bool
        
        Generated from: POST /api/v1/session/webhook/test
        @methodId test_webhook_api_v1_session_webhook_test_post
        @category session
        @example
        ```python
        # Example usage (auto-generated)
        result = await self.test_webhook('example')
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
            # validate_params(validation_model, {event_type, sample_data}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        should_cache = True
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
            cache_key = generate_cache_key('POST', '/api/v1/session/webhook/test', {"event_type": event_type, "sample_data": sample_data}, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug('Test Webhook',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/webhook/test',
            event_type=event_type,
            sample_data=sample_data,
            action='test_webhook'
        )

        try:
            async def api_call():
                response = await self.api.test_webhook_api_v1_session_webhook_test_post(finaticapi__api__v1__routers__session__session_router___test_webhook_request={**({'event_type': event_type} | ({'sample_data': sample_data} if sample_data is not None else {}))})

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
                cache_key = generate_cache_key('POST', '/api/v1/session/webhook/test', {"event_type": event_type, "sample_data": sample_data}, self.sdk_config)
                cache[cache_key] = final_result
            
            self.logger.debug('Test Webhook completed',
                request_id=request_id,
                action='test_webhook'
            )
            
            return final_result
            
        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass
            
            self.logger.error('Test Webhook failed',
                error=str(e),
                request_id=request_id,
                action='test_webhook',
                exc_info=True
            )
            
            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods
