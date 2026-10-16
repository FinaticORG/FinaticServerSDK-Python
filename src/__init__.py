"""Main SDK entry point."""

from .openapi import path_bootstrap  # noqa: F401

try:
    from .FinaticServer import FinaticServer
except ModuleNotFoundError:
    pass

try:
    from .v1 import AccountOrderCommand, V1Client
except ModuleNotFoundError:
    pass

try:
    from .finatic_fdx_types import (
        AccountOrderCommandRequest,
        AccountOrderPayload,
        AccountOrderSchemaResponse,
        AccountOrderSchemaResponseDict,
        EventContractCapabilityResponse,
        EventContractCapabilityResponseDict,
        FDXAssetType,
        FDXBrokerOrder,
        FDXBrokerOrderCommandResult,
        FDXBrokerOrderCommandResultDict,
        FDXBrokerOrderDict,
        FDXBrokerOrderEvent,
        FDXBrokerOrderEventDict,
        FDXBrokerOrderFill,
        FDXBrokerOrderFillDict,
        FDXBrokerOrderGroup,
        FDXBrokerPosition,
        FDXBrokerPositionDict,
        FDXBrokerPositionLot,
        FDXBrokerPositionLotFill,
        FDXBrokerTransaction,
        FDXFutureInstrumentDetails,
        FDXInstrumentDescriptor,
        FinaticAPIErrorResponse,
        FinaticV1Error,
        FinaticV1ErrorCategory,
        FinaticV1ErrorDict,
    )
except ModuleNotFoundError:
    pass

try:
    from finatic_server import *  # type: ignore[F401,F403]
except ModuleNotFoundError:
    pass
