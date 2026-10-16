"""Type aliases for FDX broker payloads.

Hand-authored SDK annotations complement generated OpenAPI models under
``finatic_server.models``.
"""

from __future__ import annotations

from finatic_server.models.account_order_command_request import (
    AccountOrderCommandRequest,
)
from finatic_server.models.account_order_payload import AccountOrderPayload
from finatic_server.models.account_order_schema_response import (
    AccountOrderSchemaResponse,
)
from finatic_server.models.event_contract_capability_response import (
    EventContractCapabilityResponse,
)
from finatic_server.models.fdx_asset_type import FDXAssetType
from finatic_server.models.fdx_broker_order import FDXBrokerOrder
from finatic_server.models.fdx_broker_order_command_result import (
    FDXBrokerOrderCommandResult,
)
from finatic_server.models.fdx_broker_order_event import FDXBrokerOrderEvent
from finatic_server.models.fdx_broker_order_fill import FDXBrokerOrderFill
from finatic_server.models.fdx_broker_order_group import FDXBrokerOrderGroup
from finatic_server.models.fdx_broker_position import FDXBrokerPosition
from finatic_server.models.fdx_broker_position_lot import FDXBrokerPositionLot
from finatic_server.models.fdx_broker_position_lot_fill import (
    FDXBrokerPositionLotFill,
)
from finatic_server.models.fdx_broker_transaction import FDXBrokerTransaction
from finatic_server.models.fdx_future_instrument_details import (
    FDXFutureInstrumentDetails,
)
from finatic_server.models.fdx_instrument_descriptor import FDXInstrumentDescriptor
from finatic_server.models.finatic_api_error_response import FinaticAPIErrorResponse
from finatic_server.models.finatic_v1_error import FinaticV1Error
from finatic_server.models.finatic_v1_error_category import FinaticV1ErrorCategory

from .finatic_fdx_typed_dicts import (
    AccountOrderSchemaResponseDict,
    EventContractCapabilityResponseDict,
    FDXBrokerOrderCommandResultDict,
    FDXBrokerOrderDict,
    FDXBrokerOrderEventDict,
    FDXBrokerOrderFillDict,
    FDXBrokerPositionDict,
    FinaticV1ErrorDict,
)

__all__ = [
    "AccountOrderCommandRequest",
    "AccountOrderPayload",
    "AccountOrderSchemaResponse",
    "AccountOrderSchemaResponseDict",
    "EventContractCapabilityResponse",
    "EventContractCapabilityResponseDict",
    "FDXAssetType",
    "FDXBrokerOrder",
    "FDXBrokerOrderCommandResult",
    "FDXBrokerOrderCommandResultDict",
    "FDXBrokerOrderDict",
    "FDXBrokerOrderEvent",
    "FDXBrokerOrderEventDict",
    "FDXBrokerOrderFill",
    "FDXBrokerOrderFillDict",
    "FDXBrokerOrderGroup",
    "FDXBrokerPosition",
    "FDXBrokerPositionDict",
    "FDXBrokerPositionLot",
    "FDXBrokerPositionLotFill",
    "FDXBrokerTransaction",
    "FDXFutureInstrumentDetails",
    "FDXInstrumentDescriptor",
    "FinaticAPIErrorResponse",
    "FinaticV1Error",
    "FinaticV1ErrorCategory",
    "FinaticV1ErrorDict",
]
