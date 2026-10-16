"""Contract tests for stable, hand-authored SDK surfaces (not generated internals)."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest


def test_custom_finatic_server_preserves_subclass_marker() -> None:
    """Regen-safe: verifies hand-authored FinaticServer keeps subclass marker."""
    root = Path(__file__).resolve().parents[2]
    source_file = root / "src" / "FinaticServer.py"
    assert source_file.is_file(), f"Expected {source_file}"
    body = source_file.read_text(encoding="utf-8")
    assert "__CUSTOM_CLASS__" in body


def test_finatic_server_public_entrypoint() -> None:
    """Stable import path for the server SDK."""
    from finatic_server_python import FinaticServer

    assert FinaticServer is not None
    assert hasattr(FinaticServer, "init")
    assert inspect.iscoroutinefunction(FinaticServer.init)


def test_finatic_server_root_is_bootstrap_only() -> None:
    """Root exposes bootstrap lifecycle; session state lives on finatic.v1."""
    from finatic_server_python import FinaticServer

    sdk = FinaticServer(api_key="test-api-key")
    assert hasattr(sdk, "v1")
    assert hasattr(sdk, "close")
    assert not hasattr(sdk, "get_session_id")
    assert hasattr(sdk.v1, "get_session_id")
    assert inspect.iscoroutinefunction(sdk.v1.start_session)
    assert hasattr(sdk.v1, "list_accounts")
    assert inspect.iscoroutinefunction(sdk.v1.list_accounts)
    assert hasattr(sdk.v1, "list_balances")
    assert hasattr(sdk.v1, "list_positions")


def test_event_contract_models_are_public_and_fail_closed() -> None:
    from finatic_server_python import (
        AccountOrderCommandRequest,
        AccountOrderSchemaResponse,
        EventContractCapabilityResponse,
        FDXAssetType,
    )

    assert FDXAssetType.BOND.value == "BOND"
    assert FDXAssetType.CFD.value == "CFD"
    assert FDXAssetType.EVENT_CONTRACT.value == "EVENT_CONTRACT"
    with pytest.raises(ValueError):
        FDXAssetType("UNSUPPORTED_EVENT_CONTRACT")

    request = AccountOrderCommandRequest.from_dict(
        {
            "order": {
                "finaticInstrumentId": "finatic:event-contract:series-1:yes",
                "instrumentId": "provider-contract-1",
            }
        }
    )
    assert request is not None
    assert request.to_dict()["order"]["finaticInstrumentId"] == (
        "finatic:event-contract:series-1:yes"
    )

    capability = EventContractCapabilityResponse.from_dict(
        {
            "providerOffered": True,
            "implementationEvidenced": True,
            "publicEnabled": False,
            "accountEntitled": True,
            "closingOnly": False,
            "observedAt": "2026-10-16T10:00:00Z",
            "implementationRef": "core-sha",
            "provenanceSource": "provider-capability-observation",
        }
    )
    assert capability is not None
    schema = AccountOrderSchemaResponse.from_dict(
        {
            "brokerId": "tastytrade",
            "action": "PLACE",
            "orderSchema": {"type": "object"},
            "brokerWireSchema": None,
            "supportedOrderTypesByAssetClass": {"EVENT_CONTRACT": ["MARKET"]},
            "eventContract": capability.to_dict(),
        }
    )
    assert schema is not None
    serialized = schema.to_dict()
    assert serialized["supportedOrderTypesByAssetClass"]["EVENT_CONTRACT"] == ["MARKET"]
    assert serialized["eventContract"]["accountEntitled"] is True
    assert serialized["eventContract"]["closingOnly"] is False
    assert serialized["eventContract"]["publicEnabled"] is False


def test_stable_public_error_models_are_reachable() -> None:
    from finatic_server_python import (
        FinaticAPIErrorResponse,
        FinaticV1Error,
        FinaticV1ErrorCategory,
    )

    error = FinaticV1Error.from_dict(
        {
            "category": "VALIDATION",
            "code": "EVENT_CONTRACT_IDENTITY_INVALID",
            "message": "Event Contract identity is invalid",
            "details": {"field": "assetType"},
        }
    )
    assert error is not None
    assert error.category == FinaticV1ErrorCategory.VALIDATION
    assert error.to_dict()["code"] == "EVENT_CONTRACT_IDENTITY_INVALID"
    assert FinaticAPIErrorResponse is not None
