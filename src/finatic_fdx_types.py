"""Type aliases for FDX broker payloads.

The OpenAPI Python client does not emit separate Pydantic model modules for these
schemas (list endpoints use ``List[Any]`` in generated ``SuccessPayload*`` models).
Hand-authored SDK code keeps these names for readable annotations.
"""

from __future__ import annotations

from typing import Any

FDXBrokerOrder = Any
FDXBrokerOrderEvent = Any
FDXBrokerOrderFill = Any
FDXBrokerOrderGroup = Any
FDXBrokerPosition = Any
FDXBrokerPositionLot = Any
FDXBrokerPositionLotFill = Any
FDXBrokerTransaction = Any
