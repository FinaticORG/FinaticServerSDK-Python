"""Type aliases for FDX broker payloads.

Hand-authored SDK annotations complement generated OpenAPI models under
``finatic_server.models``.
"""

from __future__ import annotations

from typing import Any

from finatic_server.models.fdx_broker_order_command_result import (
    FDXBrokerOrderCommandResult,
)

FDXBrokerOrder = Any
FDXBrokerOrderEvent = Any
FDXBrokerOrderFill = Any
FDXBrokerOrderGroup = Any
FDXBrokerPosition = Any
FDXBrokerTransaction = Any

__all__ = [
    "FDXBrokerOrder",
    "FDXBrokerOrderCommandResult",
    "FDXBrokerOrderEvent",
    "FDXBrokerOrderFill",
    "FDXBrokerOrderGroup",
    "FDXBrokerPosition",
    "FDXBrokerTransaction",
]
