"""
Custom session wrapper - Extends generated wrapper.

This file is protected and will not be overwritten during regeneration.
Add your custom session logic here.
"""

from typing import Optional, Dict, Any
from src.generated.wrappers.session import SessionWrapper
from src.generated.api.session_api import SessionApi
from src.generated.configuration import Configuration
from src.generated.config import SdkConfig
from src.generated.models.portal_url_response import PortalUrlResponse
from src.generated.models.token_response_data import TokenResponseData
from src.generated.models.session_start_request import SessionStartRequest
from src.generated.models.session_user_response import SessionUserResponse


class CustomSessionWrapper(SessionWrapper):
    """Custom wrapper for session operations.

    Extend or override generated functions as needed.
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

    async def init_session(self, x_api_key: str) -> TokenResponseData:
        """Override init_session to remove incorrect session_id check.

        The generated code incorrectly checks for session_id before init_session,
        but init_session is what CREATES the session, so it shouldn't require one.
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Structured logging
        self.logger.debug(
            "Init Session",
            request_id=request_id,
            method="POST",
            path="/api/v1/session/init",
            x_api_key=x_api_key,
            action="init_session",
        )

        # Call the API directly, bypassing the incorrect check in parent
        from src.generated.utils.interceptors import apply_response_interceptors
        from src.generated.utils.retry import retry_api_call

        async def api_call():
            response = await self.api.init_session_api_v1_session_init_post(x_api_key=x_api_key)
            return await apply_response_interceptors(response, self.sdk_config)

        response = await retry_api_call(api_call, config=self.sdk_config)
        return self._unwrap_response(response)

    async def start_session(
        self, one_time_token: str, session_start_request: SessionStartRequest
    ) -> Any:
        """Override start_session to remove incorrect session_id check.

        The generated code incorrectly checks for session_id before start_session,
        but start_session is what CREATES the session, so it shouldn't require one.
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Structured logging
        self.logger.debug(
            "Start Session",
            request_id=request_id,
            method="POST",
            path="/api/v1/session/start",
            action="start_session",
        )

        # Call the API directly, bypassing the incorrect check in parent
        from src.generated.utils.interceptors import apply_response_interceptors
        from src.generated.utils.retry import retry_api_call

        async def api_call():
            response = await self.api.start_session_api_v1_session_start_post(
                one_time_token=one_time_token, session_start_request=session_start_request
            )
            return await apply_response_interceptors(response, self.sdk_config)

        response = await retry_api_call(api_call, config=self.sdk_config)
        return self._unwrap_response(response)

    async def get_portal_url(self, session_id: str) -> PortalUrlResponse:
        """Override getPortalUrl to disable caching and fix response unwrapping.

        Portal tokens are single-use, so caching them causes "already used" errors.
        Each call must generate a fresh token.
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Structured logging
        self.logger.debug(
            "Get Portal Url",
            request_id=request_id,
            method="GET",
            path="/api/v1/session/portal",
            session_id=session_id,
            action="get_portal_url",
        )

        # Temporarily disable caching for this call
        original_cache_enabled = None
        if self.sdk_config:
            original_cache_enabled = getattr(self.sdk_config, "cache_enabled", None)
            self.sdk_config.cache_enabled = False

        try:
            # Call the API directly with proper unwrapping
            from src.generated.utils.interceptors import apply_response_interceptors
            from src.generated.utils.retry import retry_api_call

            async def api_call():
                response = await self.api.get_portal_url_api_v1_session_portal_get(
                    session_id=session_id
                )
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)
            return self._unwrap_response(response)
        finally:
            # Restore original cache setting
            if self.sdk_config and original_cache_enabled is not None:
                self.sdk_config.cache_enabled = original_cache_enabled

    async def get_session_user(self, company_id: str, session_id: str) -> SessionUserResponse:
        """Override get_session_user to fix response unwrapping."""
        # Generate request ID
        request_id = self._generate_request_id()

        # Structured logging
        self.logger.debug(
            "Get Session User",
            request_id=request_id,
            method="GET",
            path="/api/v1/session/{session_id}/user",
            company_id=company_id,
            session_id=session_id,
            action="get_session_user",
        )

        # Call the API directly with proper unwrapping
        from src.generated.utils.interceptors import apply_response_interceptors
        from src.generated.utils.retry import retry_api_call

        async def api_call():
            response = await self.api.get_session_user_api_v1_session_session_id_user_get(
                company_id=company_id, session_id=session_id
            )
            return await apply_response_interceptors(response, self.sdk_config)

        response = await retry_api_call(api_call, config=self.sdk_config)
        return self._unwrap_response(response)
