"""Type aliases for FDX broker payloads.

Hand-authored SDK annotations complement generated OpenAPI models under
``finatic_server.models``.
"""

from __future__ import annotations

from finatic_server.models.account_order_payload import AccountOrderPayload
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

from .finatic_fdx_typed_dicts import (
    FDXBrokerOrderCommandResultDict,
    FDXBrokerOrderDict,
    FDXBrokerOrderEventDict,
    FDXBrokerOrderFillDict,
    FDXBrokerPositionDict,
)

__all__ = [
    "AccountOrderPayload",
    "FDXBrokerOrder",
    "FDXBrokerOrderCommandResult",
    "FDXBrokerOrderEvent",
    "FDXBrokerOrderFill",
    "FDXBrokerOrderGroup",
    "FDXBrokerPosition",
    "FDXBrokerPositionLot",
    "FDXBrokerPositionLotFill",
    "FDXBrokerTransaction",
    "FDXFutureInstrumentDetails",
    "FDXInstrumentDescriptor",
    "FDXBrokerOrderCommandResultDict",
    "FDXBrokerOrderDict",
    "FDXBrokerOrderEventDict",
    "FDXBrokerOrderFillDict",
    "FDXBrokerPositionDict",
]
