"""
Generated wrapper functions for market-data operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/market_data.py instead.
"""

from typing import Optional, Any
from ..api.market_data_api import MarketDataApi
from ..configuration import Configuration
from ..config import SdkConfig
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


class MarketDataWrapper:
    """MarketData wrapper functions.

    Provides simplified method names and response unwrapping.
    """

    def __init__(
        self,
        api: MarketDataApi,
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

    async def get_futures_historical(
        self,
        symbol: str,
        start_date: Any = None,
        end_date: Any = None,
        expiration: Any = None,
        provider: Any = None,
    ) -> list:
        """Get Futures Historical

                Return full futures historical dataset for the requested symbol(s).

        Generated from: GET /api/v1/market-data/futures/historical
        """
        # Generate request ID
        request_id = self._generate_request_id()

        # Input validation (Phase 2B: pydantic)
        if self.sdk_config and self.sdk_config.validation_enabled:
            # TODO: Generate validation model from endpoint parameters
            # validation_model = create_validation_model(...)
            # validate_params(validation_model, {symbol, start_date, end_date, expiration, provider}, self.sdk_config)
            pass  # Placeholder until validation is implemented

        # Check cache (Phase 2B: optional caching)
        cache = get_cache(self.sdk_config)
        if cache and self.sdk_config and self.sdk_config.cache_enabled:
            cache_key = generate_cache_key(
                "GET",
                "/api/v1/market-data/futures/historical",
                {
                    "symbol": symbol,
                    "start_date": start_date,
                    "end_date": end_date,
                    "expiration": expiration,
                    "provider": provider,
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
            "Get Futures Historical",
            request_id=request_id,
            method="GET",
            path="/api/v1/market-data/futures/historical",
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            expiration=expiration,
            provider=provider,
            action="get_futures_historical",
        )

        try:
            # Full retry logic (Phase 2B: tenacity)
            async def api_call():
                # Apply request interceptors (Phase 2B)
                response = await self.api.get_futures_historical_api_v1_market_data_futures_historical_get(
                    symbol=symbol,
                    start_date=start_date,
                    end_date=end_date,
                    expiration=expiration,
                    provider=provider,
                )
                # Apply response interceptors (Phase 2B)
                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            result = response.data.data  # Unwrap FinaticResponse

            # Store in cache (Phase 2B)
            if cache and self.sdk_config and self.sdk_config.cache_enabled:
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/market-data/futures/historical",
                    {
                        "symbol": symbol,
                        "start_date": start_date,
                        "end_date": end_date,
                        "expiration": expiration,
                        "provider": provider,
                    },
                    self.sdk_config,
                )
                cache[cache_key] = result

            # Structured logging (Phase 2B)
            self.logger.debug(
                "Get Futures Historical completed",
                request_id=request_id,
                action="get_futures_historical",
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
                "Get Futures Historical failed",
                error=str(e),
                request_id=request_id,
                action="get_futures_historical",
                exc_info=True,
            )

            raise self._handle_error(e, request_id)

        # TODO Phase 2C: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2C: Add orphaned method detection
        # TODO Phase 2C: Add advanced convenience methods
