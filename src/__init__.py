"""Main SDK entry point."""

from .openapi import path_bootstrap  # noqa: F401

try:
    from .FinaticServer import FinaticServer
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

# Bind the hand-written facade exports after the generated wildcard import so
# generated model names cannot replace the public v1 contract aliases.
try:
    from .v1 import (
        AccountOrderCommand,
        SessionStartResult,
        SessionStatus,
        SessionSyncAccountStatus,
        SessionSyncStatusResponse,
        V1Client,
    )
except ModuleNotFoundError:
    pass
