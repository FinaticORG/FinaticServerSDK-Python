"""
Generated wrapper functions for session operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/session.py instead.
"""

from typing import Optional, Any, Dict, List
from dataclasses import dataclass
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
from ..utils.enum_coercion import coerce_enum_value
from ..utils.plain_object import convert_to_plain_object

# Phase 2C: Input/Output type definitions
@dataclass
class InitSessionParams:
    """Input parameters for init_session_api_v1_session_init_post."""
    x_api_key: str

@dataclass
class InitSessionResponse:
    """Output response for init_session_api_v1_session_init_post."""
    success: Dict[str, Any]  # {"data": TokenResponseData, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    Warning: Optional[List[Dict[str, Any]]] = None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]

@dataclass
class StartSessionParams:
    """Input parameters for start_session_api_v1_session_start_post."""
    one_time_token: str
    session_start_request: SessionStartRequest

@dataclass
class StartSessionResponse:
    """Output response for start_session_api_v1_session_start_post."""
    success: Dict[str, Any]  # {"data": SessionResponseData, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    Warning: Optional[List[Dict[str, Any]]] = None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]

@dataclass
class GetPortalUrlParams:
    """Input parameters for get_portal_url_api_v1_session_portal_get."""
    pass

@dataclass
class GetPortalUrlResponse:
    """Output response for get_portal_url_api_v1_session_portal_get."""
    success: Dict[str, Any]  # {"data": PortalUrlResponse, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    Warning: Optional[List[Dict[str, Any]]] = None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]

@dataclass
class GetSessionUserParams:
    """Input parameters for get_session_user_api_v1_session__session_id__user_get."""
    session_id: str

@dataclass
class GetSessionUserResponse:
    """Output response for get_session_user_api_v1_session__session_id__user_get."""
    success: Dict[str, Any]  # {"data": SessionUserResponse, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    Warning: Optional[List[Dict[str, Any]]] = None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]

@dataclass
class AuthenticateSessionParams:
    """Input parameters for authenticate_session_api_v1_session_authenticate_post."""
    session_id: str
    user_id: str

@dataclass
class AuthenticateSessionResponse:
    """Output response for authenticate_session_api_v1_session_authenticate_post."""
    success: Dict[str, Any]  # {"data": TokenData, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    Warning: Optional[List[Dict[str, Any]]] = None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]

@dataclass
class RefreshSessionParams:
    """Input parameters for refresh_session_api_v1_session_refresh_post."""
    pass

@dataclass
class RefreshSessionResponse:
    """Output response for refresh_session_api_v1_session_refresh_post."""
    success: Dict[str, Any]  # {"data": SessionResponseData, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    Warning: Optional[List[Dict[str, Any]]] = None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]

@dataclass
class TestWebhookParams:
    """Input parameters for test_webhook_api_v1_session_webhook_test_post."""
    event_type: str
    sample_data: dict = None

@dataclass
class TestWebhookResponse:
    """Output response for test_webhook_api_v1_session_webhook_test_post."""
    success: Dict[str, Any]  # {"data": TestWebhookResponse, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    Warning: Optional[List[Dict[str, Any]]] = None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]


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

    async def init_session(self, params: InitSessionParams) -> InitSessionResponse:
        """Init Session
        
        Initialize a new session with company API key.

        Args:
        - params: InitSessionParams - Input parameters object
        Returns:
        - InitSessionResponse: Standard response with success/Error/Warning structure
        
        Generated from: POST /api/v1/session/init
        @methodId init_session_api_v1_session_init_post
        @category session
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.session import InitSessionParams
        
        result = await finatic.init_session(InitSessionParams(
            x_api_key='example'
        ))
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.Error:
            print('Error:', result.Error['message'])
        ```
        """
        # Phase 2C: Extract individual params from input params object
        x_api_key = params.x_api_key

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
            cache_key = generate_cache_key('POST', '/api/v1/session/init', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Init Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/init',
            params=params_dict,
            action='init_session'
        )

        try:
            async def api_call():
                response = await self.api.init_session_api_v1_session_init_post(x_api_key=x_api_key)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            
            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = getattr(response, 'warnings', None) if hasattr(response, 'warnings') else None
            meta = getattr(response, 'meta', None) if hasattr(response, 'meta') else None
            
            # Build standard response structure
            standard_response = InitSessionResponse(
                success={
                    'data': convert_to_plain_object(api_data),
                    **({'meta': meta} if meta else {}),
                },
                Error=None,
                Warning=[{'message': w.message if hasattr(w, 'message') else str(w), 'code': getattr(w, 'code', None), 'details': getattr(w, 'details', w)} for w in warnings] if warnings else None,
            )
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('POST', '/api/v1/session/init', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Init Session completed',
                request_id=request_id,
                action='init_session'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
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
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
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
                error_message = getattr(e.response, 'text', None) or str(e)
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                except Exception:
                    response_data = getattr(e.response, 'text', None)
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
            error_response = InitSessionResponse(
                success={'data': None},
                Error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                Warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def start_session(self, params: StartSessionParams) -> StartSessionResponse:
        """Start Session
        
        Start a session with a one-time token.

        Args:
        - params: StartSessionParams - Input parameters object
        Returns:
        - StartSessionResponse: Standard response with success/Error/Warning structure
        
        Generated from: POST /api/v1/session/start
        @methodId start_session_api_v1_session_start_post
        @category session
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.session import StartSessionParams
        
        result = await finatic.start_session(StartSessionParams(
            one_time_token='example',
            session_start_request={}
        ))
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.Error:
            print('Error:', result.Error['message'])
        ```
        """
        # Phase 2C: Extract individual params from input params object
        one_time_token = params.one_time_token
        session_start_request = params.session_start_request

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
            cache_key = generate_cache_key('POST', '/api/v1/session/start', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Start Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/start',
            params=params_dict,
            action='start_session'
        )

        try:
            async def api_call():
                response = await self.api.start_session_api_v1_session_start_post(session_start_request=session_start_request, one_time_token=one_time_token)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            
            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = getattr(response, 'warnings', None) if hasattr(response, 'warnings') else None
            meta = getattr(response, 'meta', None) if hasattr(response, 'meta') else None
            
            # Build standard response structure
            standard_response = StartSessionResponse(
                success={
                    'data': convert_to_plain_object(api_data),
                    **({'meta': meta} if meta else {}),
                },
                Error=None,
                Warning=[{'message': w.message if hasattr(w, 'message') else str(w), 'code': getattr(w, 'code', None), 'details': getattr(w, 'details', w)} for w in warnings] if warnings else None,
            )
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('POST', '/api/v1/session/start', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Start Session completed',
                request_id=request_id,
                action='start_session'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
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
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
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
                error_message = getattr(e.response, 'text', None) or str(e)
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                except Exception:
                    response_data = getattr(e.response, 'text', None)
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
            error_response = StartSessionResponse(
                success={'data': None},
                Error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                Warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_portal_url(self, params: GetPortalUrlParams) -> GetPortalUrlResponse:
        """Get Portal Url
        
        Get a portal URL with token for a session.
        
        The session must be in ACTIVE or AUTHENTICATING state and the request must come from the same device
        that initiated the session. Device info is automatically validated from the request.

        Args:
        - params: GetPortalUrlParams - Input parameters object (empty for methods with no parameters)
        Returns:
        - GetPortalUrlResponse: Standard response with success/Error/Warning structure
        
        Generated from: GET /api/v1/session/portal
        @methodId get_portal_url_api_v1_session_portal_get
        @category session
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.session import GetPortalUrlParams
        
        result = await finatic.get_portal_url(GetPortalUrlParams())
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
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
            cache_key = generate_cache_key('GET', '/api/v1/session/portal', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Portal Url',
            request_id=request_id,
            method='GET',
            path='/api/v1/session/portal',
            params=params_dict,
            action='get_portal_url'
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
                response = await self.api.get_portal_url_api_v1_session_portal_get(session_id=self.session_id, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            
            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = getattr(response, 'warnings', None) if hasattr(response, 'warnings') else None
            meta = getattr(response, 'meta', None) if hasattr(response, 'meta') else None
            
            # Build standard response structure
            standard_response = GetPortalUrlResponse(
                success={
                    'data': convert_to_plain_object(api_data),
                    **({'meta': meta} if meta else {}),
                },
                Error=None,
                Warning=[{'message': w.message if hasattr(w, 'message') else str(w), 'code': getattr(w, 'code', None), 'details': getattr(w, 'details', w)} for w in warnings] if warnings else None,
            )
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/session/portal', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Portal Url completed',
                request_id=request_id,
                action='get_portal_url'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
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
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
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
                error_message = getattr(e.response, 'text', None) or str(e)
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                except Exception:
                    response_data = getattr(e.response, 'text', None)
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
            error_response = GetPortalUrlResponse(
                success={'data': None},
                Error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                Warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_session_user(self, params: GetSessionUserParams) -> GetSessionUserResponse:
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
        - params: GetSessionUserParams - Input parameters object
        Returns:
        - GetSessionUserResponse: Standard response with success/Error/Warning structure
        
        Generated from: GET /api/v1/session/{session_id}/user
        @methodId get_session_user_api_v1_session__session_id__user_get
        @category session
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.session import GetSessionUserParams
        
        result = await finatic.get_session_user(GetSessionUserParams(
            session_id='id-123'
        ))
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.Error:
            print('Error:', result.Error['message'])
        ```
        """
        # Phase 2C: Extract individual params from input params object
        session_id = params.session_id

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
            cache_key = generate_cache_key('GET', '/api/v1/session/{session_id}/user', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Get Session User',
            request_id=request_id,
            method='GET',
            path='/api/v1/session/{session_id}/user',
            params=params_dict,
            action='get_session_user'
        )

        try:
            async def api_call():
                response = await self.api.get_session_user_api_v1_session_session_id_user_get(session_id=session_id, company_id=self.company_id)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            
            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = getattr(response, 'warnings', None) if hasattr(response, 'warnings') else None
            meta = getattr(response, 'meta', None) if hasattr(response, 'meta') else None
            
            # Build standard response structure
            standard_response = GetSessionUserResponse(
                success={
                    'data': convert_to_plain_object(api_data),
                    **({'meta': meta} if meta else {}),
                },
                Error=None,
                Warning=[{'message': w.message if hasattr(w, 'message') else str(w), 'code': getattr(w, 'code', None), 'details': getattr(w, 'details', w)} for w in warnings] if warnings else None,
            )
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('GET', '/api/v1/session/{session_id}/user', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Get Session User completed',
                request_id=request_id,
                action='get_session_user'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
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
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
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
                error_message = getattr(e.response, 'text', None) or str(e)
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                except Exception:
                    response_data = getattr(e.response, 'text', None)
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
            error_response = GetSessionUserResponse(
                success={'data': None},
                Error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                Warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def authenticate_session(self, params: AuthenticateSessionParams) -> AuthenticateSessionResponse:
        """Authenticate Session
        


        Args:
        - params: AuthenticateSessionParams - Input parameters object
        Returns:
        - AuthenticateSessionResponse: Standard response with success/Error/Warning structure
        
        Generated from: POST /api/v1/session/authenticate
        @methodId authenticate_session_api_v1_session_authenticate_post
        @category session
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.session import AuthenticateSessionParams
        
        result = await finatic.authenticate_session(AuthenticateSessionParams(
            session_id='id-123',
            user_id='id-123'
        ))
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.Error:
            print('Error:', result.Error['message'])
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        session_id = params.session_id
        user_id = params.user_id

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
            cache_key = generate_cache_key('POST', '/api/v1/session/authenticate', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Authenticate Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/authenticate',
            params=params_dict,
            action='authenticate_session'
        )

        try:
            async def api_call():
                response = await self.api.authenticate_session_api_v1_session_authenticate_post()

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            
            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = getattr(response, 'warnings', None) if hasattr(response, 'warnings') else None
            meta = getattr(response, 'meta', None) if hasattr(response, 'meta') else None
            
            # Build standard response structure
            standard_response = AuthenticateSessionResponse(
                success={
                    'data': convert_to_plain_object(api_data),
                    **({'meta': meta} if meta else {}),
                },
                Error=None,
                Warning=[{'message': w.message if hasattr(w, 'message') else str(w), 'code': getattr(w, 'code', None), 'details': getattr(w, 'details', w)} for w in warnings] if warnings else None,
            )
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('POST', '/api/v1/session/authenticate', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Authenticate Session completed',
                request_id=request_id,
                action='authenticate_session'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
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
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
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
                error_message = getattr(e.response, 'text', None) or str(e)
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                except Exception:
                    response_data = getattr(e.response, 'text', None)
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
            error_response = AuthenticateSessionResponse(
                success={'data': None},
                Error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                Warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def refresh_session(self, params: RefreshSessionParams) -> RefreshSessionResponse:
        """Refresh Session
        
        Refresh an existing session by extending its expiration time.
        
        This endpoint allows users to extend their session before it expires.
        The session will be extended by the default duration (24 hours).

        Args:
        - params: RefreshSessionParams - Input parameters object (empty for methods with no parameters)
        Returns:
        - RefreshSessionResponse: Standard response with success/Error/Warning structure
        
        Generated from: POST /api/v1/session/refresh
        @methodId refresh_session_api_v1_session_refresh_post
        @category session
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.session import RefreshSessionParams
        
        result = await finatic.refresh_session(RefreshSessionParams())
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
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
            cache_key = generate_cache_key('POST', '/api/v1/session/refresh', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Refresh Session',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/refresh',
            params=params_dict,
            action='refresh_session'
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
                response = await self.api.refresh_session_api_v1_session_refresh_post(session_id=self.session_id, company_id=self.company_id, _headers=headers)

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            
            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = getattr(response, 'warnings', None) if hasattr(response, 'warnings') else None
            meta = getattr(response, 'meta', None) if hasattr(response, 'meta') else None
            
            # Build standard response structure
            standard_response = RefreshSessionResponse(
                success={
                    'data': convert_to_plain_object(api_data),
                    **({'meta': meta} if meta else {}),
                },
                Error=None,
                Warning=[{'message': w.message if hasattr(w, 'message') else str(w), 'code': getattr(w, 'code', None), 'details': getattr(w, 'details', w)} for w in warnings] if warnings else None,
            )
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('POST', '/api/v1/session/refresh', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Refresh Session completed',
                request_id=request_id,
                action='refresh_session'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
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
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
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
                error_message = getattr(e.response, 'text', None) or str(e)
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                except Exception:
                    response_data = getattr(e.response, 'text', None)
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
            error_response = RefreshSessionResponse(
                success={'data': None},
                Error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                Warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def test_webhook(self, params: TestWebhookParams) -> TestWebhookResponse:
        """Test Webhook
        
        Send a test webhook for the specified event type to the company's configured endpoints.

        Args:
        - params: TestWebhookParams - Input parameters object
        Returns:
        - TestWebhookResponse: Standard response with success/Error/Warning structure
        
        Generated from: POST /api/v1/session/webhook/test
        @methodId test_webhook_api_v1_session_webhook_test_post
        @category session
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.session import TestWebhookParams
        
        result = await finatic.test_webhook(TestWebhookParams(
            event_type='example'
        ))
        
        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        elif result.Error:
            print('Error:', result.Error['message'])
        ```
        @example
        ```python
        # Full example with optional parameters
        from finatic_sdk.generated.wrappers.session import TestWebhookParams
        
        result = await finatic.test_webhook(TestWebhookParams(
            event_type='example',
            sample_data={}
        ))
        
        # Handle response with warnings
        if result.success:
            print('Data:', result.success['data'])
            if result.Warning:
                print('Warnings:', result.Warning)
        elif result.Error:
            print('Error:', result.Error['message'], result.Error['code'])
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError('Session not initialized. Call start_session() first.')

        # Phase 2C: Extract individual params from input params object
        event_type = params.event_type
        sample_data = getattr(params, 'sample_data', None)

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
            cache_key = generate_cache_key('POST', '/api/v1/session/webhook/test', params_dict, self.sdk_config)
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug('Cache hit', request_id=request_id, cache_key=cache_key)
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
        self.logger.debug('Test Webhook',
            request_id=request_id,
            method='POST',
            path='/api/v1/session/webhook/test',
            params=params_dict,
            action='test_webhook'
        )

        try:
            async def api_call():
                response = await self.api.test_webhook_api_v1_session_webhook_test_post()

                return await apply_response_interceptors(response, self.sdk_config)
            
            response = await retry_api_call(api_call, config=self.sdk_config)
            
            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, 'data')):
                raise ValueError('Unexpected response shape: missing data')
            
            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = getattr(response, 'warnings', None) if hasattr(response, 'warnings') else None
            meta = getattr(response, 'meta', None) if hasattr(response, 'meta') else None
            
            # Build standard response structure
            standard_response = TestWebhookResponse(
                success={
                    'data': convert_to_plain_object(api_data),
                    **({'meta': meta} if meta else {}),
                },
                Error=None,
                Warning=[{'message': w.message if hasattr(w, 'message') else str(w), 'code': getattr(w, 'code', None), 'details': getattr(w, 'details', w)} for w in warnings] if warnings else None,
            )
            
            if cache and self.sdk_config and self.sdk_config.cache_enabled and should_cache:
                # Get params dict safely (dataclass or dict)
                params_dict = params.__dict__ if hasattr(params, '__dict__') else (params if isinstance(params, dict) else {})
                cache_key = generate_cache_key('POST', '/api/v1/session/webhook/test', params_dict, self.sdk_config)
                cache[cache_key] = standard_response
            
            self.logger.debug('Test Webhook completed',
                request_id=request_id,
                action='test_webhook'
            )
            
            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response
            
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
            
            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, 'code', 'UNKNOWN_ERROR')
            error_status = None
            error_details = {'error': str(e), 'type': type(e).__name__}
            
            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, 'status_code'):
                error_status = e.status_code
                error_code = getattr(e, 'code', f'HTTP_{error_status}')
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
                error_message = getattr(e.response, 'text', None) or str(e)
                try:
                    response_data = e.response.json() if hasattr(e.response, 'json') else None
                except Exception:
                    response_data = getattr(e.response, 'text', None)
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
            error_response = TestWebhookResponse(
                success={'data': None},
                Error={
                    'message': error_message,
                    'code': error_code,
                    'status': error_status,
                    'details': error_details,
                },
                Warning=None,
            )
            
            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods
