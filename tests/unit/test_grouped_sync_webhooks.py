from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import get_args, get_type_hints
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from pydantic import ValidationError

from finatic_server_python import (
    FDXOrdersSyncSummaryChangeCounts,
    FDXOrdersSyncSummaryChangeCountsDict,
    FDXSyncSummaryChangeCounts,
    FDXSyncSummaryChangeCountsDict,
    FDXSyncSummaryData,
    FDXSyncSummaryDataDict,
    FDXSyncSummaryResult,
    FDXSyncSummaryResultDict,
    FDXWebhookPayload,
    FDXWebhookPayloadDict,
    FDXWebhookPayloadResource,
    FDXWebhookPayloadResourceDict,
    FDXWebhookSubscriptionCreate,
    FDXWebhookSubscriptionCreateDict,
    FDXWebhookSubscriptionUpdate,
    FDXWebhookSubscriptionUpdateDict,
    FinaticServer,
)

EVENTS = ("account.orders.updated", "account.transactions.updated")
BATCH_ID = "b34e0c2a-4f83-44ea-b268-0f360911268e"


def payload(event_type: str, origin: str = "poll") -> dict:
    resource = "orders" if event_type == EVENTS[0] else "transactions"
    counts = {"created": 2, "updated": 1, "deleted": 0, "unchanged": 3}
    if resource == "orders":
        counts["fillsCreated"] = 4
    return {
        "schemaVersion": "v1",
        "eventId": "event-1",
        "eventType": event_type,
        "createdAt": "2026-11-12T11:00:00Z",
        "environment": "sandbox",
        "companyAccountId": "company-1",
        "accountId": "account-1",
        "grantId": "grant-1",
        "resource": {
            "resourceType": resource,
            "resourceId": "account-1",
            "accountId": "account-1",
            "grantId": "grant-1",
        },
        "data": {
            "contractVersion": "account.resource.sync-summary.v1",
            "batchId": BATCH_ID,
            "origin": origin,
            "completedAt": "2026-11-12T11:00:00Z",
            "changeCounts": counts,
            "result": {
                "resourceUrl": f"/api/v1/accounts/account-1/{resource}",
                "cursor": "opaque-result-cursor",
            },
        },
    }


@pytest.mark.parametrize("event_type", EVENTS)
@pytest.mark.asyncio
async def test_subscribe_and_update_grouped_event(event_type: str) -> None:
    subscription: FDXWebhookSubscriptionCreateDict = {
        "url": "https://partner.example/webhooks",
        "eventTypes": [event_type],
        "environment": "sandbox",
    }
    model = FDXWebhookSubscriptionCreate.from_dict(subscription)
    assert model.event_types == [event_type]
    update: FDXWebhookSubscriptionUpdateDict = {"eventTypes": [event_type]}
    assert FDXWebhookSubscriptionUpdate.from_dict(update).event_types == [event_type]

    sdk = FinaticServer(api_key="fntc_sandbox_test")
    sdk.v1._request = AsyncMock(return_value={"data": {"id": "sub-1"}})
    await sdk.v1.create_webhook_subscription(subscription)
    sdk.v1._request.assert_awaited_once_with(
        "POST", "/api/v1/webhooks/subscriptions", body=subscription
    )
    sdk.v1._request.reset_mock()
    await sdk.v1.update_webhook_subscription("sub-1", update)
    sdk.v1._request.assert_awaited_once_with(
        "PATCH", "/api/v1/webhooks/subscriptions/sub-1", body=update
    )


@pytest.mark.parametrize("event_type", EVENTS)
@pytest.mark.parametrize("origin", ["initialSync", "poll"])
def test_decode_grouped_event_with_typed_summary(event_type: str, origin: str) -> None:
    raw = payload(event_type, origin)
    envelope = FDXWebhookPayload.from_json(json.dumps(raw))
    assert envelope.event_type == event_type
    assert isinstance(envelope.resource, FDXWebhookPayloadResource)
    # OpenAPI permits arbitrary data for legacy events. Explicitly decode the
    # grouped contract rather than claiming the generic union is discriminated.
    summary = FDXSyncSummaryData.from_dict(envelope.data.to_dict())
    assert summary.contract_version == "account.resource.sync-summary.v1"
    assert summary.batch_id == UUID(BATCH_ID)
    assert summary.origin == origin
    assert summary.completed_at == datetime(2026, 11, 12, 11, tzinfo=timezone.utc)
    assert isinstance(summary.result, FDXSyncSummaryResult)
    assert summary.result.to_dict() == raw["data"]["result"]
    counts = summary.change_counts.actual_instance
    expected = (
        FDXOrdersSyncSummaryChangeCounts
        if event_type == EVENTS[0]
        else FDXSyncSummaryChangeCounts
    )
    assert isinstance(counts, expected)
    assert counts.to_dict() == raw["data"]["changeCounts"]
    assert envelope.to_dict()["data"] == raw["data"]


def test_public_mapping_types_retain_contract_literals_and_nested_types() -> None:
    payload_types = get_type_hints(FDXWebhookPayloadDict)
    subscription_types = get_type_hints(FDXWebhookSubscriptionCreateDict)
    for event_type in EVENTS:
        assert event_type in get_args(payload_types["eventType"])
        assert event_type in get_args(get_args(subscription_types["eventTypes"])[0])
    assert FDXSyncSummaryDataDict in get_args(payload_types["data"])
    assert payload_types["resource"] is FDXWebhookPayloadResourceDict
    summary_types = get_type_hints(FDXSyncSummaryDataDict)
    assert get_args(summary_types["contractVersion"]) == (
        "account.resource.sync-summary.v1",
    )
    assert summary_types["result"] is FDXSyncSummaryResultDict
    assert set(get_args(summary_types["changeCounts"])) == {
        FDXOrdersSyncSummaryChangeCountsDict,
        FDXSyncSummaryChangeCountsDict,
    }
    assert get_type_hints(FDXOrdersSyncSummaryChangeCountsDict)["fillsCreated"] is int


@pytest.mark.parametrize(
    "field,value",
    [
        ("contractVersion", "account.resource.sync-summary.v2"),
        ("origin", "unknown"),
        ("batchId", "not-a-uuid"),
        ("completedAt", "not-a-date"),
        ("result", {"resourceUrl": "", "cursor": ""}),
        ("changeCounts", {"created": -1, "updated": 0, "deleted": 0, "unchanged": 0}),
    ],
)
def test_explicit_summary_decode_rejects_invalid_fields(
    field: str, value: object
) -> None:
    data = payload(EVENTS[1])["data"]
    data[field] = value
    with pytest.raises(ValueError):
        FDXSyncSummaryData.from_dict(data)


def test_unknown_subscription_event_is_rejected() -> None:
    with pytest.raises(ValidationError):
        FDXWebhookSubscriptionCreate.from_dict(
            {
                "url": "https://partner.example/webhooks",
                "eventTypes": ["account.unknown.updated"],
            }
        )
