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
from ..models.session_link_request import SessionLinkRequest
from ..models.session_response_data import SessionResponseData
from ..models.session_start_request import SessionStartRequest
from ..models.session_user_response import SessionUserResponse
from ..models.test_webhook_response import TestWebhookResponse
from ..models.token_data import TokenData
from ..models.token_response_data import TokenResponseData
from ..models.finaticapi_api_v1_routers_session_session_router_test_webhook_request import (
    FinaticapiApiV1RoutersSessionSessionRouterTestWebhookRequest,
)
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

    def __init__(
        self,
        api: SessionApi,
        config: Optional[Configuration] = None,
        sdk_config: Optional[SdkConfig] = None,
    ):
        self.api = api
        self.config = config
        self.sdk_config = sdk_config
        self.logger = get_logger(sdk_config)
        self.session_id: Optional[str] = None
        self.company_id: Optional[str] = None
        self.csrf_token: Optional[str] = None

    # Session context setters (called by session management)
    def set_session_context(
        self, session_id: str, company_id: str, csrf_token: str
    ) -> None:
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

    def _handle_error(
        self, error: Exception, request_id: Optional[str] = None
    ) -> Exception:
        """Handle and transform errors from API calls."""
        return handle_error(error, request_id)

    async def init_session(self, x_api_key: str) -> TokenResponseData:
        """Init Session

                Initialize a new session with company API key.

        Generated from: POST /api/v1/session/init
        """
        # Authentication check
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {x_api_key}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "POST",
                "/api/v1/session/init",
                {"x_api_key": x_api_key},
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug(
            "Init Session",
            request_id=request_id,
            method="POST",
            path="/api/v1/session/init",
            x_api_key=x_api_key,
            action="init_session",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.init_session_api_v1_session_init_post(
                    x_api_key=x_api_key
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "POST",
                    "/api/v1/session/init",
                    {"x_api_key": x_api_key},
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Init Session completed", request_id=request_id, action="init_session"
            )

            return result

        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass

            self.logger.error(
                "Init Session failed",
                error=str(e),
                request_id=request_id,
                action="init_session",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def start_session(
        self, one_time_token: str, session_start_request: SessionStartRequest
    ) -> SessionResponseData:
        """Start Session

                Start a session with a one-time token.

        Generated from: POST /api/v1/session/start
        """
        # Authentication check
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {one_time_token, session_start_request}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "POST",
                "/api/v1/session/start",
                {
                    "one_time_token": one_time_token,
                    "session_start_request": session_start_request,
                },
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug(
            "Start Session",
            request_id=request_id,
            method="POST",
            path="/api/v1/session/start",
            one_time_token=one_time_token,
            session_start_request=session_start_request,
            action="start_session",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.start_session_api_v1_session_start_post(
                    one_time_token=one_time_token,
                    session_start_request=session_start_request,
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "POST",
                    "/api/v1/session/start",
                    {
                        "one_time_token": one_time_token,
                        "session_start_request": session_start_request,
                    },
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Start Session completed", request_id=request_id, action="start_session"
            )

            return result

        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass

            self.logger.error(
                "Start Session failed",
                error=str(e),
                request_id=request_id,
                action="start_session",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_portal_url(self, session_id: str) -> PortalUrlResponse:
        """Get Portal Url

                Get a portal URL with token for a session.

        The session must be in ACTIVE or AUTHENTICATING state and the request must come from the same device
        that initiated the session. Device info is automatically validated from the request.

        Generated from: GET /api/v1/session/portal
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
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "GET",
                "/api/v1/session/portal",
                {"session_id": session_id},
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug(
            "Get Portal Url",
            request_id=request_id,
            method="GET",
            path="/api/v1/session/portal",
            session_id=session_id,
            action="get_portal_url",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.get_portal_url_api_v1_session_portal_get(
                    session_id=session_id
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/session/portal",
                    {"session_id": session_id},
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Get Portal Url completed",
                request_id=request_id,
                action="get_portal_url",
            )

            return result

        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass

            self.logger.error(
                "Get Portal Url failed",
                error=str(e),
                request_id=request_id,
                action="get_portal_url",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def get_session_user(
        self, company_id: str, session_id: str
    ) -> SessionUserResponse:
        """Get Session User

                Get user information and fresh tokens for a completed session.

        This endpoint is designed for server SDKs to retrieve user information
        and authentication tokens after successful OTP verification.


        Security:
        - Requires valid session in ACTIVE state
        - Validates device fingerprint binding
        - Generates fresh tokens (not returning stored ones)
        - Only accessible to authenticated sessions with user_id

        Generated from: GET /api/v1/session/{session_id}/user
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {company_id, session_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "GET",
                "/api/v1/session/{session_id}/user",
                {"company_id": company_id, "session_id": session_id},
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug(
            "Get Session User",
            request_id=request_id,
            method="GET",
            path="/api/v1/session/{session_id}/user",
            company_id=company_id,
            session_id=session_id,
            action="get_session_user",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = (
                    await self.api.get_session_user_api_v1_session_session_id_user_get(
                        company_id=company_id, session_id=session_id
                    )
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/session/{session_id}/user",
                    {"company_id": company_id, "session_id": session_id},
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Get Session User completed",
                request_id=request_id,
                action="get_session_user",
            )

            return result

        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass

            self.logger.error(
                "Get Session User failed",
                error=str(e),
                request_id=request_id,
                action="get_session_user",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def authenticate_session(
        self, direct_auth_request: DirectAuthRequest
    ) -> TokenData:
        """Authenticate Session



        Generated from: POST /api/v1/session/authenticate
        """
        # Authentication check
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {direct_auth_request}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "POST",
                "/api/v1/session/authenticate",
                {"direct_auth_request": direct_auth_request},
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug(
            "Authenticate Session",
            request_id=request_id,
            method="POST",
            path="/api/v1/session/authenticate",
            direct_auth_request=direct_auth_request,
            action="authenticate_session",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.authenticate_session_api_v1_session_authenticate_post(
                    direct_auth_request=direct_auth_request
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "POST",
                    "/api/v1/session/authenticate",
                    {"direct_auth_request": direct_auth_request},
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Authenticate Session completed",
                request_id=request_id,
                action="authenticate_session",
            )

            return result

        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass

            self.logger.error(
                "Authenticate Session failed",
                error=str(e),
                request_id=request_id,
                action="authenticate_session",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def refresh_session(
        self, session_id: str, company_id: str
    ) -> SessionResponseData:
        """Refresh Session

                Refresh an existing session by extending its expiration time.

        This endpoint allows users to extend their session before it expires.
        The session will be extended by the default duration (24 hours).

        Generated from: POST /api/v1/session/refresh
        """
        # Authentication check
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {session_id, company_id}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "POST",
                "/api/v1/session/refresh",
                {"session_id": session_id, "company_id": company_id},
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug(
            "Refresh Session",
            request_id=request_id,
            method="POST",
            path="/api/v1/session/refresh",
            session_id=session_id,
            company_id=company_id,
            action="refresh_session",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.refresh_session_api_v1_session_refresh_post(
                    session_id=session_id, company_id=company_id
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "POST",
                    "/api/v1/session/refresh",
                    {"session_id": session_id, "company_id": company_id},
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Refresh Session completed",
                request_id=request_id,
                action="refresh_session",
            )

            return result

        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass

            self.logger.error(
                "Refresh Session failed",
                error=str(e),
                request_id=request_id,
                action="refresh_session",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def test_webhook(
        self,
        finaticapi_api_v1_routers_session_session_router_test_webhook_request: FinaticapiApiV1RoutersSessionSessionRouterTestWebhookRequest,
    ) -> TestWebhookResponse:
        """Test Webhook

                Send a test webhook for the specified event type to the company's configured endpoints.

        Generated from: POST /api/v1/session/webhook/test
        """
        # Authentication check
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {finaticapi_api_v1_routers_session_session_router_test_webhook_request}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "POST",
                "/api/v1/session/webhook/test",
                {
                    "finaticapi_api_v1_routers_session_session_router_test_webhook_request": finaticapi_api_v1_routers_session_session_router_test_webhook_request
                },
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug(
            "Test Webhook",
            request_id=request_id,
            method="POST",
            path="/api/v1/session/webhook/test",
            finaticapi_api_v1_routers_session_session_router_test_webhook_request=finaticapi_api_v1_routers_session_session_router_test_webhook_request,
            action="test_webhook",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.test_webhook_api_v1_session_webhook_test_post(
                    finaticapi_api_v1_routers_session_session_router_test_webhook_request=finaticapi_api_v1_routers_session_session_router_test_webhook_request
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "POST",
                    "/api/v1/session/webhook/test",
                    {
                        "finaticapi_api_v1_routers_session_session_router_test_webhook_request": finaticapi_api_v1_routers_session_session_router_test_webhook_request
                    },
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Test Webhook completed", request_id=request_id, action="test_webhook"
            )

            return result

        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass

            self.logger.error(
                "Test Webhook failed",
                error=str(e),
                request_id=request_id,
                action="test_webhook",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods

    async def link_user_to_session(
        self, session_id: str, session_link_request: SessionLinkRequest
    ) -> Any:
        """Link User To Session

                Link Supabase user to existing session.

        This endpoint is called after successful Supabase OTP authentication
        to associate the authenticated user with the portal session.

        Generated from: POST /api/v1/session/link-user
        """
        # Authentication check
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {session_id, session_link_request}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "POST",
                "/api/v1/session/link-user",
                {
                    "session_id": session_id,
                    "session_link_request": session_link_request,
                },
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        self.logger.debug(
            "Link User To Session",
            request_id=request_id,
            method="POST",
            path="/api/v1/session/link-user",
            session_id=session_id,
            session_link_request=session_link_request,
            action="link_user_to_session",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = (
                    await self.api.link_user_to_session_api_v1_session_link_user_post(
                        session_id=session_id, session_link_request=session_link_request
                    )
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "POST",
                    "/api/v1/session/link-user",
                    {
                        "session_id": session_id,
                        "session_link_request": session_link_request,
                    },
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Link User To Session completed",
                request_id=request_id,
                action="link_user_to_session",
            )

            return result

        except Exception as e:
            # Error handling with interceptors (Phase 2B)
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                # If interceptor throws, use original error
                pass

            self.logger.error(
                "Link User To Session failed",
                error=str(e),
                request_id=request_id,
                action="link_user_to_session",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods
