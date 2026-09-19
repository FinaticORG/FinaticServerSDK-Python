from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

from finatic_server_python import (
    AccountOrderPayload,
    FDXBrokerOrderEvent,
    FDXInstrumentDescriptor,
)


def _descriptor(symbol: str, quality: str) -> dict[str, object]:
    future: dict[str, object] = {
        "identityQuality": quality,
        "productRoot": "MGC",
    }
    if quality == "EXACT":
        future.update(
            {
                "contractCode": "MGCZ6",
                "contractMonth": "2026-12-01",
                "exchangeMic": "XCEC",
                "expirationDate": "2026-12-29",
            }
        )
    return {
        "version": "1.0",
        "finaticInstrumentId": f"finatic:future:{symbol}",
        "assetType": "FUTURE",
        "displaySymbol": symbol,
        "providerNativeId": "611092087",
        "providerSymbol": symbol,
        "future": future,
    }


def test_committed_openapi_artifact_matches_pinned_provenance() -> None:
    root = Path(__file__).resolve().parents[2]
    provenance = json.loads(
        (root / "artifacts/openapi/finaticapi-v1.provenance.json").read_text(
            encoding="utf-8"
        )
    )
    artifact = root / provenance["artifact_path"]

    assert provenance["source_sha"] == "54eb17ac130af907f95318c1833ff8f6fb915712"
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == provenance["sha256"]


def test_exact_and_root_only_descriptors_remain_distinct() -> None:
    exact = FDXInstrumentDescriptor.model_validate(_descriptor("MGCZ6", "EXACT"))
    root_only = FDXInstrumentDescriptor.model_validate(_descriptor("MGC", "ROOT_ONLY"))

    assert exact is not None
    assert root_only is not None
    assert exact.to_dict()["future"] == {
        "contractCode": "MGCZ6",
        "contractMonth": date(2026, 12, 1),
        "exchangeMic": "XCEC",
        "expirationDate": date(2026, 12, 29),
        "identityQuality": "EXACT",
        "productRoot": "MGC",
    }
    assert root_only.to_dict()["future"] == {
        "identityQuality": "ROOT_ONLY",
        "productRoot": "MGC",
    }
    assert exact.finatic_instrument_id != root_only.finatic_instrument_id


def test_multileg_event_preserves_pairwise_instrument_order() -> None:
    event = FDXBrokerOrderEvent.from_dict(
        {
            "eventId": "event-1",
            "eventTime": "2026-09-19T12:00:00Z",
            "eventType": "FILL",
            "orderId": "order-1",
            "affectedLegs": [2, 7],
            "affectedInstruments": [
                _descriptor("MGCZ6", "EXACT"),
                _descriptor("MGC", "ROOT_ONLY"),
            ],
        }
    )

    assert event is not None
    serialized = event.to_dict()
    assert serialized["affectedLegs"] == [2, 7]
    assert [
        descriptor["displaySymbol"] for descriptor in serialized["affectedInstruments"]
    ] == ["MGCZ6", "MGC"]


def test_placement_payload_preserves_canonical_and_provider_identity() -> None:
    payload = AccountOrderPayload.from_dict(
        {
            "finaticInstrumentId": "finatic:future:MGCZ6",
            "instrumentId": 611092087,
            "symbol": "MGCZ6",
        }
    )

    assert payload is not None
    assert payload.to_dict() == {
        "finaticInstrumentId": "finatic:future:MGCZ6",
        "instrumentId": 611092087,
        "symbol": "MGCZ6",
    }
