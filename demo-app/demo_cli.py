#!/usr/bin/env python3
"""
Finatic Server SDK Python Usage Example

This file demonstrates all public methods of the Finatic Server SDK.
"""

import asyncio
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

try:
    from rich.console import Console
    from rich.prompt import Confirm

    console = Console()
except ImportError:
    print("❌ Error: rich package is required. Install with: uv pip install rich")
    import sys

    sys.exit(1)

# Add parent directory to path to import SDK
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from finatic_server_python import FinaticServer

# Configuration from environment variables
API_URL = os.getenv("FINATIC_API_URL", "https://api.finatic.dev")
API_KEY = os.getenv("FINATIC_API_KEY")


async def wait_for_portal_authentication(portal_url: str) -> bool:
    """Wait for user to authenticate via portal."""
    console.print("\n[blue]🌐 Please visit this URL to authenticate:[/blue]")
    console.print(f"[cyan]{portal_url}[/cyan]")
    confirmed = Confirm.ask("Have you completed authentication in the portal?", default=False)

    if not confirmed:
        console.print("[red]Authentication not completed. Exiting...[/red]")
        return False

    return True


async def main():
    # Initialize SDK
    finatic = await FinaticServer.init(
        api_key=API_KEY,
        sdk_config={
            "base_url": API_URL,
            "log_level": "debug",
            "structured_logging": True,
        },
    )

    # Session methods
    token = await finatic.get_token()  # Optional: get_token(api_key="custom-key")
    session_result = await finatic.start_session()  # Optional: start_session(user_id="user-id")
    portal_url = (
        await finatic.get_portal_url()
    )  # Optional: get_portal_url(theme="dark", brokers=["broker1"], email="email", mode="dark")

    if not (await wait_for_portal_authentication(portal_url)):
        return

    session_user = await finatic.get_session_user()

    # Company methods
    company = await finatic.get_company(company_id="company-id")  # Required: company_id

    # Broker methods
    brokers = await finatic.get_brokers()  # Optional: get_brokers()
    broker_connections = (
        await finatic.get_broker_connections()
    )  # Optional: get_broker_connections()
    disconnect_result = await finatic.disconnect_company_from_broker(
        connection_id="connection-id"
    )  # Required: connection_id

    # Data methods - get_all_* (paginated, fetches all pages)
    all_accounts = (
        await finatic.get_all_accounts()
    )  # Optional: get_all_accounts(account_id="id", broker_id="id")
    all_orders = (
        await finatic.get_all_orders()
    )  # Optional: get_all_orders(account_id="id", broker_id="id", status="status")
    all_positions = (
        await finatic.get_all_positions()
    )  # Optional: get_all_positions(account_id="id", broker_id="id")
    all_balances = (
        await finatic.get_all_balances()
    )  # Optional: get_all_balances(account_id="id", broker_id="id")
    all_order_fills = await finatic.get_all_order_fills(order_id="order-id")  # Required: order_id
    all_order_events = await finatic.get_all_order_events(order_id="order-id")  # Required: order_id
    all_order_groups = (
        await finatic.get_all_order_groups()
    )  # Optional: get_all_order_groups(account_id="id", broker_id="id")
    all_position_lots = (
        await finatic.get_all_position_lots()
    )  # Optional: get_all_position_lots(account_id="id", broker_id="id")
    all_position_lot_fills = await finatic.get_all_position_lot_fills(
        lot_id="lot-id"
    )  # Required: lot_id

    # Data methods - get_* (single page)
    accounts = (
        await finatic.get_accounts()
    )  # Optional: get_accounts(account_id="id", broker_id="id", limit=10, offset=0)
    orders = (
        await finatic.get_orders()
    )  # Optional: get_orders(account_id="id", broker_id="id", status="status", limit=10, offset=0)
    positions = (
        await finatic.get_positions()
    )  # Optional: get_positions(account_id="id", broker_id="id", limit=10, offset=0)
    balances = (
        await finatic.get_balances()
    )  # Optional: get_balances(account_id="id", broker_id="id", limit=10, offset=0)
    order_fills = await finatic.get_order_fills(
        order_id="order-id"
    )  # Required: order_id, Optional: limit=10, offset=0
    order_events = await finatic.get_order_events(
        order_id="order-id"
    )  # Required: order_id, Optional: limit=10, offset=0
    order_groups = (
        await finatic.get_order_groups()
    )  # Optional: get_order_groups(account_id="id", broker_id="id", limit=10, offset=0)
    position_lots = (
        await finatic.get_position_lots()
    )  # Optional: get_position_lots(account_id="id", broker_id="id", limit=10, offset=0)
    position_lot_fills = await finatic.get_position_lot_fills(
        lot_id="lot-id"
    )  # Required: lot_id, Optional: limit=10, offset=0


if __name__ == "__main__":
    asyncio.run(main())
