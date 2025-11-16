"""
Custom FinaticServer extension.

This file is protected and will not be overwritten during regeneration.
Add custom logic to extend or override generated FinaticServer behavior.
"""

from typing import Optional, Dict, Any
from src.generated.FinaticServer import FinaticServer as GeneratedFinaticServer
from src.generated.config import SdkConfig


class FinaticServer(GeneratedFinaticServer):
    """Custom FinaticServer class that extends the generated class.

    Use this to add custom initialization logic or override methods.

    NOTE: Session headers, portal URL caching, and metadata transformation
    are now handled by the generator. No wrapper replacements needed.
    """

    # Marker to verify custom class is being used
    __CUSTOM_CLASS__ = True

    # Generator now handles:
    # - Session headers for broker endpoints (via _headers parameter)
    # - Portal URL no-cache handling
    # - Metadata transformation for with_metadata parameter
    # No custom wrapper replacements needed

    async def init_session(
        self, api_key: Optional[str] = None, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Convenience method that combines init_session and start_session.

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
            token_response = await self.session.init_session(key_to_use)

            # Unwrap FinaticResponse wrapper if needed
            # The response might be FinaticResponseTokenResponseData (with .data property) or TokenResponseData
            if hasattr(token_response, "data") and token_response.data:
                # Unwrap FinaticResponse wrapper
                token_response_data = token_response.data
            else:
                token_response_data = token_response

            # Extract one_time_token from TokenResponseData object
            if hasattr(token_response_data, "one_time_token"):
                one_time_token = token_response_data.one_time_token
            elif isinstance(token_response_data, dict) and "one_time_token" in token_response_data:
                one_time_token = token_response_data["one_time_token"]
            else:
                # If we can't extract the token, return error
                return {
                    "success": False,
                    "session_id": None,
                    "company_id": None,
                    "error": f"Failed to extract one-time token from response. Response type: {type(token_response).__name__}, Unwrapped type: {type(token_response_data).__name__}",
                }

            if not one_time_token or not isinstance(one_time_token, str):
                return {
                    "success": False,
                    "session_id": None,
                    "company_id": None,
                    "error": "Failed to get one-time token",
                }

            # Step 2: Start session with the token
            from src.generated.models.session_start_request import SessionStartRequest

            session_start_request = (
                SessionStartRequest(user_id=user_id) if user_id else SessionStartRequest()
            )
            session_response = await self.session.start_session(
                one_time_token, session_start_request
            )

            # Extract session_id and company_id from response
            session_id = (
                session_response.session_id
                if hasattr(session_response, "session_id")
                else (
                    session_response.get("session_id")
                    if isinstance(session_response, dict)
                    else None
                )
            )
            company_id = (
                session_response.company_id
                if hasattr(session_response, "company_id")
                else (
                    session_response.get("company_id")
                    if isinstance(session_response, dict)
                    else None
                )
            )

            # Set session context if we got valid IDs
            if session_id and company_id:
                # Note: csrf_token is not available in SessionResponseData
                self.set_session_context(session_id, company_id, "")

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
