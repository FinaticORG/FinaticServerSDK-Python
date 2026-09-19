"""Static consumer contract for raw v1 descriptor responses."""

from typing import Literal

from typing_extensions import assert_type

from src.v1 import V1Client


async def consume_raw_descriptors(client: V1Client) -> None:
    orders = (await client.list_orders("account-1"))["data"] or []
    order_instrument = orders[0]["legs"][0]["instrument"]
    if order_instrument is not None:
        assert_type(order_instrument["finaticInstrumentId"], str)
        future = order_instrument["future"]
        if future is not None:
            assert_type(future["identityQuality"], Literal["EXACT", "ROOT_ONLY"])

    fills = (await client.get_account_order_fills("account-1", "order-1"))["data"] or []
    fill_instrument = fills[0]["instrument"]
    if fill_instrument is not None:
        assert_type(fill_instrument["displaySymbol"], str)

    events = (await client.get_account_order_events("account-1", "order-1"))[
        "data"
    ] or []
    affected = events[0]["affectedInstruments"] or []
    assert_type(affected[0]["finaticInstrumentId"], str)

    positions = (await client.list_positions("account-1"))["data"] or []
    position_instrument = positions[0]["instrument"]
    if position_instrument is not None:
        assert_type(position_instrument["providerSymbol"], str | None)
