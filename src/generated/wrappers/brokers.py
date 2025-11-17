"""
Generated wrapper functions for brokers operations (Phase 2B).

This file is regenerated on each run - do not edit directly.
For custom logic, edit src/custom/wrappers/brokers.py instead.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..api.brokers_api import BrokersApi
from ..config import SdkConfig
from ..configuration import Configuration
from ..models.account_status import AccountStatus
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
from ..models.public_account_type_enum import PublicAccountTypeEnum
from ..models.public_asset_type_enum import PublicAssetTypeEnum
from ..models.public_order_side_enum import PublicOrderSideEnum
from ..models.public_order_status_enum import PublicOrderStatusEnum
from ..models.public_position_status_enum import PublicPositionStatusEnum
from ..models.user_broker_connections import UserBrokerConnections
from ..utils.cache import generate_cache_key, get_cache
from ..utils.enum_coercion import coerce_enum_value
from ..utils.error_handling import handle_error
from ..utils.interceptors import (
    apply_error_interceptors,
    apply_request_interceptors,
    apply_response_interceptors,
)
from ..utils.logger import get_logger
from ..utils.plain_object import convert_to_plain_object
from ..utils.request_id import generate_request_id
from ..utils.retry import retry_api_call


# Phase 2C: Input/Output type definitions
@dataclass
class GetBrokersParams:
    """Input parameters for get_brokers_api_v1_brokers__get."""

    pass


@dataclass
class GetBrokersResponse:
    """Output response for get_brokers_api_v1_brokers__get."""

    success: Dict[str, Any]  # {"data": list[BrokerInfo], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


@dataclass
class ListBrokerConnectionsParams:
    """Input parameters for list_broker_connections_api_v1_brokers_connections_get."""

    pass


@dataclass
class ListBrokerConnectionsResponse:
    """Output response for list_broker_connections_api_v1_brokers_connections_get."""

    success: Dict[
        str, Any
    ]  # {"data": list[UserBrokerConnections], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


@dataclass
class DisconnectCompanyFromBrokerParams:
    """Input parameters for disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete."""

    connection_id: str


@dataclass
class DisconnectCompanyFromBrokerResponse:
    """Output response for disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete."""

    success: Dict[str, Any]  # {"data": DisconnectActionResult, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


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
class GetOrdersResponse:
    """Output response for get_orders_api_v1_brokers_data_orders_get."""

    success: Dict[str, Any]  # {"data": list[OrderResponse], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


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
class GetPositionsResponse:
    """Output response for get_positions_api_v1_brokers_data_positions_get."""

    success: Dict[str, Any]  # {"data": list[PositionResponse], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


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
class GetBalancesResponse:
    """Output response for get_balances_api_v1_brokers_data_balances_get."""

    success: Dict[str, Any]  # {"data": list[Balances], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


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
class GetAccountsResponse:
    """Output response for get_accounts_api_v1_brokers_data_accounts_get."""

    success: Dict[str, Any]  # {"data": list[Accounts], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


@dataclass
class GetOrderFillsParams:
    """Input parameters for get_order_fills_api_v1_brokers_data_orders__order_id__fills_get."""

    order_id: str
    connection_id: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class GetOrderFillsResponse:
    """Output response for get_order_fills_api_v1_brokers_data_orders__order_id__fills_get."""

    success: Dict[
        str, Any
    ]  # {"data": list[OrderFillResponse], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


@dataclass
class GetOrderEventsParams:
    """Input parameters for get_order_events_api_v1_brokers_data_orders__order_id__events_get."""

    order_id: str
    connection_id: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class GetOrderEventsResponse:
    """Output response for get_order_events_api_v1_brokers_data_orders__order_id__events_get."""

    success: Dict[
        str, Any
    ]  # {"data": list[OrderEventResponse], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


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
class GetOrderGroupsResponse:
    """Output response for get_order_groups_api_v1_brokers_data_orders_groups_get."""

    success: Dict[
        str, Any
    ]  # {"data": list[OrderGroupResponse], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


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
class GetPositionLotsResponse:
    """Output response for get_position_lots_api_v1_brokers_data_positions_lots_get."""

    success: Dict[
        str, Any
    ]  # {"data": list[PositionLotResponse], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


@dataclass
class GetPositionLotFillsParams:
    """Input parameters for get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get."""

    lot_id: str
    connection_id: str = None
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class GetPositionLotFillsResponse:
    """Output response for get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get."""

    success: Dict[
        str, Any
    ]  # {"data": list[PositionLotFillResponse], "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


@dataclass
class PlaceOrderParams:
    """Input parameters for place_order_api_v1_brokers_orders_post."""

    place_order_api_v1_brokers_orders_post_request: Any = None
    connection_id: str = None


@dataclass
class PlaceOrderResponse:
    """Output response for place_order_api_v1_brokers_orders_post."""

    success: Dict[str, Any]  # {"data": OrderActionResult, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


@dataclass
class CancelOrderParams:
    """Input parameters for cancel_order_api_v1_brokers_orders__order_id__delete."""

    order_id: str
    cancel_order_api_v1_brokers_orders_order_id_delete_request: Any = None
    account_number: str = None
    connection_id: str = None


@dataclass
class CancelOrderResponse:
    """Output response for cancel_order_api_v1_brokers_orders__order_id__delete."""

    success: Dict[str, Any]  # {"data": OrderActionResult, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


@dataclass
class ModifyOrderParams:
    """Input parameters for modify_order_api_v1_brokers_orders__order_id__patch."""

    order_id: str
    modify_order_api_v1_brokers_orders_order_id_patch_request: Any = None
    account_number: str = None
    connection_id: str = None


@dataclass
class ModifyOrderResponse:
    """Output response for modify_order_api_v1_brokers_orders__order_id__patch."""

    success: Dict[str, Any]  # {"data": OrderActionResult, "meta"?: Dict[str, Any]}
    Error: Optional[Dict[str, Any]] = (
        None  # {"message": str, "code"?: str, "details"?: Dict[str, Any]}
    )
    Warning: Optional[List[Dict[str, Any]]] = (
        None  # [{"message": str, "code"?: str, "details"?: Dict[str, Any]}]
    )


class BrokersWrapper:
    """Brokers wrapper functions.

    Provides simplified method names and response unwrapping.
    """

    def __init__(
        self,
        api: BrokersApi,
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

    async def get_brokers(self, params: GetBrokersParams) -> GetBrokersResponse:
        """Get Brokers

        Get all available brokers.

        This is a fast operation that returns a cached list of available brokers.
        The list is loaded once at startup and never changes during runtime.

        Returns
        -------
        FinaticResponse[list[BrokerInfo]]
            list of available brokers with their metadata.

        Args:
        - params: GetBrokersParams - Input parameters object (empty for methods with no parameters)
        Returns:
        - GetBrokersResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/
        @methodId get_brokers_api_v1_brokers__get
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import GetBrokersParams

        result = await finatic.get_brokers(GetBrokersParams())

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET", "/api/v1/brokers/", params_dict, self.sdk_config
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Brokers",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/",
            params=params_dict,
            action="get_brokers",
        )

        try:

            async def api_call():
                response = await self.api.get_brokers_api_v1_brokers_get()

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetBrokersResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET", "/api/v1/brokers/", params_dict, self.sdk_config
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Brokers completed", request_id=request_id, action="get_brokers"
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Brokers failed",
                error=str(e),
                request_id=request_id,
                action="get_brokers",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetBrokersResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def list_broker_connections(
        self, params: ListBrokerConnectionsParams
    ) -> ListBrokerConnectionsResponse:
        """List Broker Connections

        List all broker connections for the current user.

        This endpoint is accessible from the portal and uses session-only authentication.
        Returns connections that the user has any permissions for.

        Args:
        - params: ListBrokerConnectionsParams - Input parameters object (empty for methods with no parameters)
        Returns:
        - ListBrokerConnectionsResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/connections
        @methodId list_broker_connections_api_v1_brokers_connections_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import ListBrokerConnectionsParams

        result = await finatic.list_broker_connections(ListBrokerConnectionsParams())

        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        """
        # Authentication check
        if not self.session_id:
            raise ValueError("Session not initialized. Call start_session() first.")

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET", "/api/v1/brokers/connections", params_dict, self.sdk_config
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "List Broker Connections",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/connections",
            params=params_dict,
            action="list_broker_connections",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.list_broker_connections_api_v1_brokers_connections_get(
                    _headers=headers
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = ListBrokerConnectionsResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET", "/api/v1/brokers/connections", params_dict, self.sdk_config
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "List Broker Connections completed",
                request_id=request_id,
                action="list_broker_connections",
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "List Broker Connections failed",
                error=str(e),
                request_id=request_id,
                action="list_broker_connections",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = ListBrokerConnectionsResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def disconnect_company_from_broker(
        self, params: DisconnectCompanyFromBrokerParams
    ) -> DisconnectCompanyFromBrokerResponse:
        """Disconnect Company From Broker

        Remove a company's access to a broker connection.

        If the company is the only one with access, the entire connection is deleted.
        If other companies have access, only the company's access is removed.

        Args:
        - params: DisconnectCompanyFromBrokerParams - Input parameters object
        Returns:
        - DisconnectCompanyFromBrokerResponse: Standard response with success/Error/Warning structure

        Generated from: DELETE /api/v1/brokers/disconnect-company/{connection_id}
        @methodId disconnect_company_from_broker_api_v1_brokers_disconnect_company__connection_id__delete
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.brokers import DisconnectCompanyFromBrokerParams

        result = await finatic.disconnect_company_from_broker(DisconnectCompanyFromBrokerParams(
            connection_id='id-123'
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
            raise ValueError("Session not initialized. Call start_session() first.")

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "DELETE",
                "/api/v1/brokers/disconnect-company/{connection_id}",
                params_dict,
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Disconnect Company From Broker",
            request_id=request_id,
            method="DELETE",
            path="/api/v1/brokers/disconnect-company/{connection_id}",
            params=params_dict,
            action="disconnect_company_from_broker",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.disconnect_company_from_broker_api_v1_brokers_disconnect_company_connection_id_delete(
                    connection_id=connection_id, _headers=headers
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = DisconnectCompanyFromBrokerResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "DELETE",
                    "/api/v1/brokers/disconnect-company/{connection_id}",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Disconnect Company From Broker completed",
                request_id=request_id,
                action="disconnect_company_from_broker",
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Disconnect Company From Broker failed",
                error=str(e),
                request_id=request_id,
                action="disconnect_company_from_broker",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = DisconnectCompanyFromBrokerResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_orders(self, params: GetOrdersParams) -> GetOrdersResponse:
        """Get Orders

        Get orders for all authorized broker connections.

        This endpoint is accessible from the portal and uses session-only authentication.
        Returns orders from connections the company has read access to.

        Args:
        - params: GetOrdersParams - Input parameters object
        Returns:
        - GetOrdersResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/orders
        @methodId get_orders_api_v1_brokers_data_orders_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import GetOrdersParams

        result = await finatic.get_orders(GetOrdersParams())

        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        from finatic_sdk.generated.wrappers.brokers import GetOrdersParams

        result = await finatic.get_orders(GetOrdersParams(
            broker_id='id-123',
            connection_id='id-123',
            account_id='id-123'
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, "broker_id", None)
        connection_id = getattr(params, "connection_id", None)
        account_id = getattr(params, "account_id", None)
        symbol = getattr(params, "symbol", None)
        order_status = (
            coerce_enum_value(
                getattr(params, "order_status", None),
                PublicOrderStatusEnum,
                "order_status",
            )
            if getattr(params, "order_status", None) is not None
            else None
        )
        side = (
            coerce_enum_value(
                getattr(params, "side", None), PublicOrderSideEnum, "side"
            )
            if getattr(params, "side", None) is not None
            else None
        )
        asset_type = (
            coerce_enum_value(
                getattr(params, "asset_type", None), PublicAssetTypeEnum, "asset_type"
            )
            if getattr(params, "asset_type", None) is not None
            else None
        )
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)
        created_after = getattr(params, "created_after", None)
        created_before = getattr(params, "created_before", None)
        with_metadata = getattr(params, "with_metadata", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET", "/api/v1/brokers/data/orders", params_dict, self.sdk_config
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Orders",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/orders",
            params=params_dict,
            action="get_orders",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_orders_api_v1_brokers_data_orders_get(
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
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetOrdersResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET", "/api/v1/brokers/data/orders", params_dict, self.sdk_config
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Orders completed", request_id=request_id, action="get_orders"
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Orders failed",
                error=str(e),
                request_id=request_id,
                action="get_orders",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetOrdersResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_positions(self, params: GetPositionsParams) -> GetPositionsResponse:
        """Get Positions

        Get positions for all authorized broker connections.

        This endpoint is accessible from the portal and uses session-only authentication.
        Returns positions from connections the company has read access to.

        Args:
        - params: GetPositionsParams - Input parameters object
        Returns:
        - GetPositionsResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/positions
        @methodId get_positions_api_v1_brokers_data_positions_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import GetPositionsParams

        result = await finatic.get_positions(GetPositionsParams())

        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        from finatic_sdk.generated.wrappers.brokers import GetPositionsParams

        result = await finatic.get_positions(GetPositionsParams(
            broker_id='id-123',
            connection_id='id-123',
            account_id='id-123'
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, "broker_id", None)
        connection_id = getattr(params, "connection_id", None)
        account_id = getattr(params, "account_id", None)
        symbol = getattr(params, "symbol", None)
        side = (
            coerce_enum_value(
                getattr(params, "side", None), PublicOrderSideEnum, "side"
            )
            if getattr(params, "side", None) is not None
            else None
        )
        asset_type = (
            coerce_enum_value(
                getattr(params, "asset_type", None), PublicAssetTypeEnum, "asset_type"
            )
            if getattr(params, "asset_type", None) is not None
            else None
        )
        position_status = (
            coerce_enum_value(
                getattr(params, "position_status", None),
                PublicPositionStatusEnum,
                "position_status",
            )
            if getattr(params, "position_status", None) is not None
            else None
        )
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)
        updated_after = getattr(params, "updated_after", None)
        updated_before = getattr(params, "updated_before", None)
        with_metadata = getattr(params, "with_metadata", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET", "/api/v1/brokers/data/positions", params_dict, self.sdk_config
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Positions",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/positions",
            params=params_dict,
            action="get_positions",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = (
                    await self.api.get_positions_api_v1_brokers_data_positions_get(
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
                        _headers=headers,
                    )
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetPositionsResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/brokers/data/positions",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Positions completed", request_id=request_id, action="get_positions"
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Positions failed",
                error=str(e),
                request_id=request_id,
                action="get_positions",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetPositionsResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_balances(self, params: GetBalancesParams) -> GetBalancesResponse:
        """Get Balances

        Get balances for all authorized broker connections.

        This endpoint is accessible from the portal and uses session-only authentication.
        Returns balances from connections the company has read access to.

        Args:
        - params: GetBalancesParams - Input parameters object
        Returns:
        - GetBalancesResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/balances
        @methodId get_balances_api_v1_brokers_data_balances_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import GetBalancesParams

        result = await finatic.get_balances(GetBalancesParams())

        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        from finatic_sdk.generated.wrappers.brokers import GetBalancesParams

        result = await finatic.get_balances(GetBalancesParams(
            broker_id='id-123',
            connection_id='id-123',
            account_id='id-123'
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, "broker_id", None)
        connection_id = getattr(params, "connection_id", None)
        account_id = getattr(params, "account_id", None)
        is_end_of_day_snapshot = getattr(params, "is_end_of_day_snapshot", None)
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)
        balance_created_after = getattr(params, "balance_created_after", None)
        balance_created_before = getattr(params, "balance_created_before", None)
        with_metadata = getattr(params, "with_metadata", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET", "/api/v1/brokers/data/balances", params_dict, self.sdk_config
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Balances",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/balances",
            params=params_dict,
            action="get_balances",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_balances_api_v1_brokers_data_balances_get(
                    broker_id=broker_id,
                    connection_id=connection_id,
                    account_id=account_id,
                    is_end_of_day_snapshot=is_end_of_day_snapshot,
                    limit=limit,
                    offset=offset,
                    balance_created_after=balance_created_after,
                    balance_created_before=balance_created_before,
                    with_metadata=with_metadata,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetBalancesResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET", "/api/v1/brokers/data/balances", params_dict, self.sdk_config
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Balances completed", request_id=request_id, action="get_balances"
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Balances failed",
                error=str(e),
                request_id=request_id,
                action="get_balances",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetBalancesResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_accounts(self, params: GetAccountsParams) -> GetAccountsResponse:
        """Get Accounts

        Get accounts for all authorized broker connections.

        This endpoint is accessible from the portal and uses session-only authentication.
        Returns accounts from connections the company has read access to.

        Args:
        - params: GetAccountsParams - Input parameters object
        Returns:
        - GetAccountsResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/accounts
        @methodId get_accounts_api_v1_brokers_data_accounts_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import GetAccountsParams

        result = await finatic.get_accounts(GetAccountsParams())

        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        from finatic_sdk.generated.wrappers.brokers import GetAccountsParams

        result = await finatic.get_accounts(GetAccountsParams(
            broker_id='id-123',
            connection_id='id-123',
            account_type='cash'
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, "broker_id", None)
        connection_id = getattr(params, "connection_id", None)
        account_type = (
            coerce_enum_value(
                getattr(params, "account_type", None),
                PublicAccountTypeEnum,
                "account_type",
            )
            if getattr(params, "account_type", None) is not None
            else None
        )
        status = getattr(params, "status", None)
        currency = getattr(params, "currency", None)
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)
        with_metadata = getattr(params, "with_metadata", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET", "/api/v1/brokers/data/accounts", params_dict, self.sdk_config
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Accounts",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/accounts",
            params=params_dict,
            action="get_accounts",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_accounts_api_v1_brokers_data_accounts_get(
                    broker_id=broker_id,
                    connection_id=connection_id,
                    account_type=account_type,
                    status=status,
                    currency=currency,
                    limit=limit,
                    offset=offset,
                    with_metadata=with_metadata,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetAccountsResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET", "/api/v1/brokers/data/accounts", params_dict, self.sdk_config
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Accounts completed", request_id=request_id, action="get_accounts"
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Accounts failed",
                error=str(e),
                request_id=request_id,
                action="get_accounts",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetAccountsResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_order_fills(
        self, params: GetOrderFillsParams
    ) -> GetOrderFillsResponse:
        """Get Order Fills

        Get order fills for a specific order.

        This endpoint returns all execution fills for the specified order.

        Args:
        - params: GetOrderFillsParams - Input parameters object
        Returns:
        - GetOrderFillsResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/orders/{order_id}/fills
        @methodId get_order_fills_api_v1_brokers_data_orders__order_id__fills_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.brokers import GetOrderFillsParams

        result = await finatic.get_order_fills(GetOrderFillsParams(
            order_id='id-123'
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
        from finatic_sdk.generated.wrappers.brokers import GetOrderFillsParams

        result = await finatic.get_order_fills(GetOrderFillsParams(
            order_id='id-123',
            connection_id='id-123',
            limit=10,
            offset=0
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        order_id = params.order_id
        connection_id = getattr(params, "connection_id", None)
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET",
                "/api/v1/brokers/data/orders/{order_id}/fills",
                params_dict,
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Order Fills",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/orders/{order_id}/fills",
            params=params_dict,
            action="get_order_fills",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_order_fills_api_v1_brokers_data_orders_order_id_fills_get(
                    order_id=order_id,
                    connection_id=connection_id,
                    limit=limit,
                    offset=offset,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetOrderFillsResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/brokers/data/orders/{order_id}/fills",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Order Fills completed",
                request_id=request_id,
                action="get_order_fills",
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Order Fills failed",
                error=str(e),
                request_id=request_id,
                action="get_order_fills",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetOrderFillsResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_order_events(
        self, params: GetOrderEventsParams
    ) -> GetOrderEventsResponse:
        """Get Order Events

        Get order events for a specific order.

        This endpoint returns all lifecycle events for the specified order.

        Args:
        - params: GetOrderEventsParams - Input parameters object
        Returns:
        - GetOrderEventsResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/orders/{order_id}/events
        @methodId get_order_events_api_v1_brokers_data_orders__order_id__events_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.brokers import GetOrderEventsParams

        result = await finatic.get_order_events(GetOrderEventsParams(
            order_id='id-123'
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
        from finatic_sdk.generated.wrappers.brokers import GetOrderEventsParams

        result = await finatic.get_order_events(GetOrderEventsParams(
            order_id='id-123',
            connection_id='id-123',
            limit=10,
            offset=0
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        order_id = params.order_id
        connection_id = getattr(params, "connection_id", None)
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET",
                "/api/v1/brokers/data/orders/{order_id}/events",
                params_dict,
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Order Events",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/orders/{order_id}/events",
            params=params_dict,
            action="get_order_events",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_order_events_api_v1_brokers_data_orders_order_id_events_get(
                    order_id=order_id,
                    connection_id=connection_id,
                    limit=limit,
                    offset=offset,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetOrderEventsResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/brokers/data/orders/{order_id}/events",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Order Events completed",
                request_id=request_id,
                action="get_order_events",
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Order Events failed",
                error=str(e),
                request_id=request_id,
                action="get_order_events",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetOrderEventsResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_order_groups(
        self, params: GetOrderGroupsParams
    ) -> GetOrderGroupsResponse:
        """Get Order Groups

        Get order groups.

        This endpoint returns order groups that contain multiple orders.

        Args:
        - params: GetOrderGroupsParams - Input parameters object
        Returns:
        - GetOrderGroupsResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/orders/groups
        @methodId get_order_groups_api_v1_brokers_data_orders_groups_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import GetOrderGroupsParams

        result = await finatic.get_order_groups(GetOrderGroupsParams())

        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        from finatic_sdk.generated.wrappers.brokers import GetOrderGroupsParams

        result = await finatic.get_order_groups(GetOrderGroupsParams(
            broker_id='id-123',
            connection_id='id-123',
            limit=10
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, "broker_id", None)
        connection_id = getattr(params, "connection_id", None)
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)
        created_after = getattr(params, "created_after", None)
        created_before = getattr(params, "created_before", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET",
                "/api/v1/brokers/data/orders/groups",
                params_dict,
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Order Groups",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/orders/groups",
            params=params_dict,
            action="get_order_groups",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_order_groups_api_v1_brokers_data_orders_groups_get(
                    broker_id=broker_id,
                    connection_id=connection_id,
                    limit=limit,
                    offset=offset,
                    created_after=created_after,
                    created_before=created_before,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetOrderGroupsResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/brokers/data/orders/groups",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Order Groups completed",
                request_id=request_id,
                action="get_order_groups",
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Order Groups failed",
                error=str(e),
                request_id=request_id,
                action="get_order_groups",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetOrderGroupsResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_position_lots(
        self, params: GetPositionLotsParams
    ) -> GetPositionLotsResponse:
        """Get Position Lots

        Get position lots (tax lots for positions).

        This endpoint returns tax lots for positions, which are used for tax reporting.
        Each lot tracks when a position was opened/closed and at what prices.

        Args:
        - params: GetPositionLotsParams - Input parameters object
        Returns:
        - GetPositionLotsResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/positions/lots
        @methodId get_position_lots_api_v1_brokers_data_positions_lots_get
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import GetPositionLotsParams

        result = await finatic.get_position_lots(GetPositionLotsParams())

        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        from finatic_sdk.generated.wrappers.brokers import GetPositionLotsParams

        result = await finatic.get_position_lots(GetPositionLotsParams(
            broker_id='id-123',
            connection_id='id-123',
            account_id='id-123'
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        broker_id = getattr(params, "broker_id", None)
        connection_id = getattr(params, "connection_id", None)
        account_id = getattr(params, "account_id", None)
        symbol = getattr(params, "symbol", None)
        position_id = getattr(params, "position_id", None)
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET",
                "/api/v1/brokers/data/positions/lots",
                params_dict,
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Position Lots",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/positions/lots",
            params=params_dict,
            action="get_position_lots",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_position_lots_api_v1_brokers_data_positions_lots_get(
                    broker_id=broker_id,
                    connection_id=connection_id,
                    account_id=account_id,
                    symbol=symbol,
                    position_id=position_id,
                    limit=limit,
                    offset=offset,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetPositionLotsResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/brokers/data/positions/lots",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Position Lots completed",
                request_id=request_id,
                action="get_position_lots",
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Position Lots failed",
                error=str(e),
                request_id=request_id,
                action="get_position_lots",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetPositionLotsResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def get_position_lot_fills(
        self, params: GetPositionLotFillsParams
    ) -> GetPositionLotFillsResponse:
        """Get Position Lot Fills

        Get position lot fills for a specific lot.

        This endpoint returns all fills associated with a specific position lot.

        Args:
        - params: GetPositionLotFillsParams - Input parameters object
        Returns:
        - GetPositionLotFillsResponse: Standard response with success/Error/Warning structure

        Generated from: GET /api/v1/brokers/data/positions/lots/{lot_id}/fills
        @methodId get_position_lot_fills_api_v1_brokers_data_positions_lots__lot_id__fills_get
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.brokers import GetPositionLotFillsParams

        result = await finatic.get_position_lot_fills(GetPositionLotFillsParams(
            lot_id='id-123'
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
        from finatic_sdk.generated.wrappers.brokers import GetPositionLotFillsParams

        result = await finatic.get_position_lot_fills(GetPositionLotFillsParams(
            lot_id='id-123',
            connection_id='id-123',
            limit=10,
            offset=0
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        lot_id = params.lot_id
        connection_id = getattr(params, "connection_id", None)
        limit = getattr(params, "limit", None)
        offset = getattr(params, "offset", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "GET",
                "/api/v1/brokers/data/positions/lots/{lot_id}/fills",
                params_dict,
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Get Position Lot Fills",
            request_id=request_id,
            method="GET",
            path="/api/v1/brokers/data/positions/lots/{lot_id}/fills",
            params=params_dict,
            action="get_position_lot_fills",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.get_position_lot_fills_api_v1_brokers_data_positions_lots_lot_id_fills_get(
                    lot_id=lot_id,
                    connection_id=connection_id,
                    limit=limit,
                    offset=offset,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = GetPositionLotFillsResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "GET",
                    "/api/v1/brokers/data/positions/lots/{lot_id}/fills",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Get Position Lot Fills completed",
                request_id=request_id,
                action="get_position_lot_fills",
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Get Position Lot Fills failed",
                error=str(e),
                request_id=request_id,
                action="get_position_lot_fills",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = GetPositionLotFillsResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def place_order(self, params: PlaceOrderParams) -> PlaceOrderResponse:
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
        - params: PlaceOrderParams - Input parameters object
        Returns:
        - PlaceOrderResponse: Standard response with success/Error/Warning structure

        Generated from: POST /api/v1/brokers/orders
        @methodId place_order_api_v1_brokers_orders_post
        @category brokers
        @example
        ```python
        # Example with no parameters
        from finatic_sdk.generated.wrappers.brokers import PlaceOrderParams

        result = await finatic.place_order(PlaceOrderParams())

        # Access the response data
        if result.success:
            print('Data:', result.success['data'])
        ```
        @example
        ```python
        # Full example with optional parameters
        from finatic_sdk.generated.wrappers.brokers import PlaceOrderParams

        result = await finatic.place_order(PlaceOrderParams(
            place_order_api_v1_brokers_orders_post_request={},
            connection_id='id-123'
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        place_order_api_v1_brokers_orders_post_request = getattr(
            params, "place_order_api_v1_brokers_orders_post_request", None
        )
        connection_id = getattr(params, "connection_id", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "POST", "/api/v1/brokers/orders", params_dict, self.sdk_config
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Place Order",
            request_id=request_id,
            method="POST",
            path="/api/v1/brokers/orders",
            params=params_dict,
            action="place_order",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.place_order_api_v1_brokers_orders_post(
                    connection_id=connection_id,
                    place_order_api_v1_brokers_orders_post_request=place_order_api_v1_brokers_orders_post_request,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = PlaceOrderResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "POST", "/api/v1/brokers/orders", params_dict, self.sdk_config
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Place Order completed", request_id=request_id, action="place_order"
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Place Order failed",
                error=str(e),
                request_id=request_id,
                action="place_order",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = PlaceOrderResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def cancel_order(self, params: CancelOrderParams) -> CancelOrderResponse:
        """Cancel Order

        Cancel an existing order.

        This endpoint is accessible from the portal and uses session-only authentication.
        Requires trading permissions for the company.

        Args:
        - params: CancelOrderParams - Input parameters object
        Returns:
        - CancelOrderResponse: Standard response with success/Error/Warning structure

        Generated from: DELETE /api/v1/brokers/orders/{order_id}
        @methodId cancel_order_api_v1_brokers_orders__order_id__delete
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.brokers import CancelOrderParams

        result = await finatic.cancel_order(CancelOrderParams(
            order_id='id-123'
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
        from finatic_sdk.generated.wrappers.brokers import CancelOrderParams

        result = await finatic.cancel_order(CancelOrderParams(
            order_id='id-123',
            cancel_order_api_v1_brokers_orders_order_id_delete_request={},
            account_number='example',
            connection_id='id-123'
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        order_id = params.order_id
        cancel_order_api_v1_brokers_orders_order_id_delete_request = getattr(
            params, "cancel_order_api_v1_brokers_orders_order_id_delete_request", None
        )
        account_number = getattr(params, "account_number", None)
        connection_id = getattr(params, "connection_id", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "DELETE",
                "/api/v1/brokers/orders/{order_id}",
                params_dict,
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Cancel Order",
            request_id=request_id,
            method="DELETE",
            path="/api/v1/brokers/orders/{order_id}",
            params=params_dict,
            action="cancel_order",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.cancel_order_api_v1_brokers_orders_order_id_delete(
                    order_id=order_id,
                    account_number=account_number,
                    connection_id=connection_id,
                    cancel_order_api_v1_brokers_orders_order_id_delete_request=cancel_order_api_v1_brokers_orders_order_id_delete_request,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = CancelOrderResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "DELETE",
                    "/api/v1/brokers/orders/{order_id}",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Cancel Order completed", request_id=request_id, action="cancel_order"
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Cancel Order failed",
                error=str(e),
                request_id=request_id,
                action="cancel_order",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = CancelOrderResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods

    async def modify_order(self, params: ModifyOrderParams) -> ModifyOrderResponse:
        """Modify Order

        Modify an existing order.

        This endpoint is accessible from the portal and uses session-only authentication.
        Requires trading permissions for the company.

        Args:
        - params: ModifyOrderParams - Input parameters object
        Returns:
        - ModifyOrderResponse: Standard response with success/Error/Warning structure

        Generated from: PATCH /api/v1/brokers/orders/{order_id}
        @methodId modify_order_api_v1_brokers_orders__order_id__patch
        @category brokers
        @example
        ```python
        # Minimal example with required parameters only
        from finatic_sdk.generated.wrappers.brokers import ModifyOrderParams

        result = await finatic.modify_order(ModifyOrderParams(
            order_id='id-123'
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
        from finatic_sdk.generated.wrappers.brokers import ModifyOrderParams

        result = await finatic.modify_order(ModifyOrderParams(
            order_id='id-123',
            modify_order_api_v1_brokers_orders_order_id_patch_request={},
            account_number='example',
            connection_id='id-123'
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
            raise ValueError("Session not initialized. Call start_session() first.")

        # Phase 2C: Extract individual params from input params object
        order_id = params.order_id
        modify_order_api_v1_brokers_orders_order_id_patch_request = getattr(
            params, "modify_order_api_v1_brokers_orders_order_id_patch_request", None
        )
        account_number = getattr(params, "account_number", None)
        connection_id = getattr(params, "connection_id", None)

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
            params_dict = (
                params.__dict__
                if hasattr(params, "__dict__")
                else (params if isinstance(params, dict) else {})
            )
            cache_key = generate_cache_key(
                "PATCH",
                "/api/v1/brokers/orders/{order_id}",
                params_dict,
                self.sdk_config,
            )
            cached = cache.get(cache_key)
            if cached:
                self.logger.debug(
                    "Cache hit", request_id=request_id, cache_key=cache_key
                )
                return cached

        # Structured logging (Phase 2B: structlog)
        # Get params dict safely (dataclass or dict)
        params_dict = (
            params.__dict__
            if hasattr(params, "__dict__")
            else (params if isinstance(params, dict) else {})
        )
        self.logger.debug(
            "Modify Order",
            request_id=request_id,
            method="PATCH",
            path="/api/v1/brokers/orders/{order_id}",
            params=params_dict,
            action="modify_order",
        )

        try:

            async def api_call():
                if not self.session_id or not self.company_id:
                    raise ValueError(
                        "Session context incomplete. Missing sessionId or companyId."
                    )
                headers = {
                    "x-session-id": self.session_id,
                    "x-company-id": self.company_id,
                    "x-request-id": request_id,
                }
                if self.csrf_token:
                    headers["x-csrf-token"] = self.csrf_token
                response = await self.api.modify_order_api_v1_brokers_orders_order_id_patch(
                    order_id=order_id,
                    account_number=account_number,
                    connection_id=connection_id,
                    modify_order_api_v1_brokers_orders_order_id_patch_request=modify_order_api_v1_brokers_orders_order_id_patch_request,
                    _headers=headers,
                )

                return await apply_response_interceptors(response, self.sdk_config)

            response = await retry_api_call(api_call, config=self.sdk_config)

            # Phase 2C: Unwrap API response and transform to standard response structure
            # OpenAPI generator returns response with .data attribute containing the actual response data
            if not (response and hasattr(response, "data")):
                raise ValueError("Unexpected response shape: missing data")

            # response.data is the actual API response data (not response.data.data)
            api_data = response.data
            warnings = (
                getattr(response, "warnings", None)
                if hasattr(response, "warnings")
                else None
            )
            meta = (
                getattr(response, "meta", None) if hasattr(response, "meta") else None
            )

            # Build standard response structure
            standard_response = ModifyOrderResponse(
                success={
                    "data": convert_to_plain_object(api_data),
                    **({"meta": meta} if meta else {}),
                },
                Error=None,
                Warning=(
                    [
                        {
                            "message": w.message if hasattr(w, "message") else str(w),
                            "code": getattr(w, "code", None),
                            "details": getattr(w, "details", w),
                        }
                        for w in warnings
                    ]
                    if warnings
                    else None
                ),
            )

            if (
                cache
                and self.sdk_config
                and self.sdk_config.cache_enabled
                and should_cache
            ):
                # Get params dict safely (dataclass or dict)
                params_dict = (
                    params.__dict__
                    if hasattr(params, "__dict__")
                    else (params if isinstance(params, dict) else {})
                )
                cache_key = generate_cache_key(
                    "PATCH",
                    "/api/v1/brokers/orders/{order_id}",
                    params_dict,
                    self.sdk_config,
                )
                cache[cache_key] = standard_response

            self.logger.debug(
                "Modify Order completed", request_id=request_id, action="modify_order"
            )

            # Phase 2C: Return standard response structure (already plain objects)
            return standard_response

        except Exception as e:
            try:
                await apply_error_interceptors(e, self.sdk_config)
            except Exception:
                pass

            self.logger.error(
                "Modify Order failed",
                error=str(e),
                request_id=request_id,
                action="modify_order",
                exc_info=True,
            )

            # Phase 2C: Extract error details from HTTP errors or generic errors
            error_message = str(e)
            error_code = getattr(e, "code", "UNKNOWN_ERROR")
            error_status = None
            error_details = {"error": str(e), "type": type(e).__name__}

            # Handle HTTP errors (from OpenAPI generator - httpx/requests)
            if hasattr(e, "status_code"):
                error_status = e.status_code
                error_code = getattr(e, "code", f"HTTP_{error_status}")
                error_message = (
                    getattr(e, "message", None) or getattr(e, "detail", None) or str(e)
                )
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e, "reason", None),
                    "responseData": getattr(e, "body", None)
                    or getattr(e, "response", None),
                    "requestUrl": (
                        getattr(e, "request", {}).get("url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e, "request", {}).get("method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            elif hasattr(e, "response") and hasattr(e.response, "status_code"):
                # Handle httpx/requests response errors
                error_status = e.response.status_code
                error_code = f"HTTP_{error_status}"
                error_message = getattr(e.response, "text", None) or str(e)
                try:
                    response_data = (
                        e.response.json() if hasattr(e.response, "json") else None
                    )
                except Exception:
                    response_data = getattr(e.response, "text", None)
                error_details = {
                    "status": error_status,
                    "statusText": getattr(e.response, "reason", None),
                    "responseData": response_data,
                    "requestUrl": (
                        getattr(e.request, "url", None)
                        if hasattr(e, "request")
                        else None
                    ),
                    "requestMethod": (
                        getattr(e.request, "method", None)
                        if hasattr(e, "request")
                        else None
                    ),
                }
            else:
                # Generic error - include stack trace if available
                import traceback

                error_details["traceback"] = traceback.format_exc()

            # Phase 2C: Return standard error response structure
            error_response = ModifyOrderResponse(
                success={"data": None},
                Error={
                    "message": error_message,
                    "code": error_code,
                    "status": error_status,
                    "details": error_details,
                },
                Warning=None,
            )

            return error_response

        # TODO Phase 2D: Add complex validation schemas (unions, enums, nested)
        # TODO Phase 2D: Add orphaned method detection
        # TODO Phase 2D: Add advanced convenience methods
