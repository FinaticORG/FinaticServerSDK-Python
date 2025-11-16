#!/usr/bin/env python3
"""
Finatic Server SDK Python Demo Application

This demo showcases the main features of the Finatic Server SDK:
- Authentication (Portal and Direct)
- Portfolio Management
- Trading Operations
- Broker Management
"""

import asyncio
import os
import sys
from typing import Any, Dict, List, Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # dotenv is optional - will use system environment variables if not available
    pass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Confirm
except ImportError:
    print("❌ Error: rich package is required. Install with: uv pip install rich")
    sys.exit(1)

try:
    import questionary
except ImportError:
    print("❌ Error: questionary package is required. Install with: uv pip install questionary")
    sys.exit(1)

# Add parent directory to path to import SDK
# We add the parent directory so finatic_server_python can be imported as a package
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import SDK - matches pattern: @finatic/server-node and @finatic/client
# Package: finatic-server-python (pip install)
# Import: finatic_server_python (from finatic_server_python import ...)
from finatic_server_python import FinaticServer

# Configuration
API_URL = os.getenv("FINATIC_API_URL", "https://api.finatic.dev")
API_KEY = os.getenv("FINATIC_API_KEY")
DEMO_EMAIL = os.getenv("DEMO_EMAIL", "demo@finatic.dev")
ACCOUNT_ID_FILTER = "1c0e6a5e-f6d7-4af8-b69d-09aa17f73762"

# Feature flags
ENABLE_DISCONNECT = os.getenv("ENABLE_DISCONNECT", "false").lower() == "true"

console = Console()


class FinaticDemo:
    """Demo application for Finatic Server SDK."""

    def __init__(self) -> None:
        """Initialize the demo client."""
        if not API_KEY:
            console.print("[red]❌ Error: FINATIC_API_KEY environment variable is required[/red]")
            console.print("\n[yellow]📝 Please create a .env file with:[/yellow]")
            console.print("[dim]FINATIC_API_URL=https://api.finatic.dev[/dim]")
            console.print("[dim]FINATIC_API_KEY=your_api_key_here[/dim]")
            console.print("\n[dim]For localhost testing:[/dim]")
            console.print("[dim]FINATIC_API_URL=http://localhost:8000[/dim]")
            sys.exit(1)

        # Initialize client like Node SDK - only API key required
        # baseUrl is optional and defaults to https://api.finatic.dev
        # For localhost testing, pass the API_URL as second parameter
        # Enable debug logging in dev mode
        self.is_dev = os.getenv("NODE_ENV") != "production" or "localhost" in API_URL
        self.client = FinaticServer(
            api_key=API_KEY,
            base_url=API_URL,
            sdk_config={
                "log_level": "debug" if self.is_dev else "error",
                "structured_logging": True,
            },
        )

    async def run(self) -> None:
        """Run the demo application."""
        console.print("\n[bold blue]🚀 Finatic Server SDK Python Demo[/bold blue]\n")
        console.print("[dim]This demo follows the actual Python SDK authentication flow.\n[/dim]")

        # Show configuration
        console.print("[dim]Configuration:[/dim]")
        console.print(f"[dim]  API URL: {API_URL}[/dim]")
        console.print(f"[dim]  API Key: {API_KEY[:10]}...\n[/dim]")

        try:
            # Step 1: Initialize SDK
            console.print("[yellow]Step 1: Initializing SDK...[/yellow]")
            await self.client.initialize()
            console.print("[green]✅ SDK initialized successfully[/green]")

            # Step 2: Initialize session (convenience method that does init + start)
            console.print("\n[yellow]Step 2: Initializing session...[/yellow]")
            try:
                # Use the convenience method that combines init_session and start_session
                # This takes the API key (optional, uses instance key) and optional user_id
                result = await self.client.init_session(api_key=API_KEY, user_id=None)

                if not result.get("success"):
                    console.print(
                        f"[red]❌ Failed to initialize session: {result.get('error')}[/red]"
                    )
                    return

                session_id = result.get("session_id")
                company_id = result.get("company_id")
                console.print(f"[green]✅ Session initialized successfully[/green]")
                console.print(f"[dim]Session ID: {session_id}[/dim]")
                console.print(f"[dim]Company ID: {company_id}[/dim]")

                # Step 3: Get portal URL
                console.print("\n[yellow]Step 3: Getting portal URL...[/yellow]")
                portal_url = await self.client.get_portal_url()
                console.print("[green]✅ Portal URL retrieved[/green]")
                console.print("\n[blue]🌐 Please visit this URL to authenticate:[/blue]")
                console.print(f"[cyan]{portal_url}[/cyan]")
            except Exception as e:
                error_msg = str(e)
                error_type = type(e).__name__
                console.print(f"[red]❌ Error: {error_type}: {error_msg}[/red]")

                # Print full traceback in debug mode
                import traceback

                if self.is_dev:
                    console.print("\n[dim]Full traceback:[/dim]")
                    console.print(f"[dim]{traceback.format_exc()}[/dim]")

                if "401" in error_msg or "Unauthorized" in error_msg:
                    console.print("[red]❌ Authentication failed (401)[/red]")
                    console.print("[yellow]💡 This usually means:[/yellow]")
                    console.print("[dim]  • Invalid API key[/dim]")
                    console.print("[dim]  • API endpoint not accessible[/dim]")
                    console.print("[dim]  • Network connectivity issues[/dim]")
                    console.print("\n[yellow]🔧 To fix this:[/yellow]")
                    console.print(
                        "[dim]  1. Check your .env file has a valid FINATIC_API_KEY[/dim]"
                    )
                    console.print("[dim]  2. Verify the API_URL is correct[/dim]")
                    console.print(
                        "[dim]  3. For localhost testing, ensure your local API is running[/dim]"
                    )
                    return
                elif "Session not initialized" in error_msg:
                    console.print("[red]❌ Session initialization error[/red]")
                    console.print("[yellow]💡 This usually means:[/yellow]")
                    console.print("[dim]  • Session context was not set properly[/dim]")
                    console.print("[dim]  • start_session() did not complete successfully[/dim]")
                    console.print(
                        f"[dim]  • Current session_id: {self.client.get_session_id()}[/dim]"
                    )
                    return
                raise

            # Step 4: Wait for user confirmation
            console.print("\n[yellow]Step 4: Waiting for authentication...[/yellow]")
            confirmed = Confirm.ask(
                "Have you completed authentication in the portal?", default=False
            )

            if not confirmed:
                console.print("[red]❌ Authentication not completed. Exiting...[/red]")
                return

            # Step 5: Get session user (this completes authentication)
            console.print("\n[yellow]Step 5: Getting authenticated user...[/yellow]")
            user_info = await self.client.get_session_user()
            console.print("[green]✅ User authenticated successfully![/green]")
            console.print(f"[dim]User ID: {user_info.get('user_id')}[/dim]")
            console.print(f"[dim]Company ID: {user_info.get('company_id')}[/dim]")
            console.print(f"[dim]Token Type: {user_info.get('token_type')}[/dim]")

            # Test session/auth methods
            console.print("\n[yellow]Step 5.1: Testing session/auth methods...[/yellow]")
            session_results = {"passed": 0, "failed": 0, "total": 0}

            async def test_session(name: str, fn, expected_type: str = "object") -> None:
                session_results["total"] += 1
                try:
                    # Always await fn() - if it's not a coroutine, this will work fine
                    # If it returns a coroutine, we need to await it
                    coro_or_result = fn()
                    if asyncio.iscoroutine(coro_or_result):
                        result = await coro_or_result
                    else:
                        result = coro_or_result
                    is_valid = (
                        isinstance(result, dict)
                        if expected_type == "object"
                        else isinstance(result, str)
                        if expected_type == "string"
                        else isinstance(result, list)
                        if expected_type == "array"
                        else result is not None
                    )
                    if is_valid:
                        session_results["passed"] += 1
                        console.print(f"[dim]  ✅ {name}[/dim]")
                    else:
                        session_results["failed"] += 1
                        console.print(f"[red]  ❌ {name} (invalid return type)[/red]")
                except Exception as e:
                    session_results["failed"] += 1
                    error_msg = str(e)[:50] if str(e) else "error"
                    console.print(f"[red]  ❌ {name} ({error_msg})[/red]")

            await test_session("getSessionId", lambda: self.client.get_session_id(), "string")
            await test_session("getCompanyId", lambda: self.client.get_company_id(), "string")
            await test_session("getUserId", lambda: self.client.get_user_id(), "string")
            await test_session("getPortalUrl", lambda: self.client.get_portal_url(), "string")

            console.print(
                f"[dim]  Session Methods Summary: {session_results['passed']}/{session_results['total']} passed[/dim]"
            )

            # Track core method results
            core_results = {"passed": 0, "failed": 0, "total": 0}

            # Helper to test core methods and track results
            async def test_core(name: str, fn, show_details: bool = True) -> Any:
                core_results["total"] += 1
                try:
                    result = await fn()
                    core_results["passed"] += 1
                    if show_details:
                        console.print(f"[dim]  ✅ {name}[/dim]")
                    return result
                except Exception as e:
                    core_results["failed"] += 1
                    error_msg = str(e)[:50] if str(e) else "error"
                    console.print(f"[red]  ❌ {name} ({error_msg})[/red]")
                    raise

            # Step 5.1: Fetch orders for a specific Finatic account id
            console.print("\n[yellow]Step 5.1: Testing core methods...[/yellow]")
            try:
                filtered_orders = await test_core(
                    "getAllOrders (filtered)",
                    lambda: self.client.get_all_orders({"account_id": ACCOUNT_ID_FILTER}),
                    show_details=False,
                )
                console.print(
                    f"[green]✅ Retrieved {len(filtered_orders)} orders for account {ACCOUNT_ID_FILTER}[/green]"
                )
                if len(filtered_orders) > 0:
                    console.print("[dim]Filtered order details:[/dim]")
                    for index, order in enumerate(filtered_orders[:3], 1):
                        order_id = order.get("id") or order.get("order_id") or "Unknown"
                        symbol = order.get("symbol") or "Unknown"
                        status = order.get("status") or order.get("order_status") or "Unknown"
                        console.print(
                            f"[dim]  {index}. Order ID: {order_id} - Symbol: {symbol} - Status: {status}[/dim]"
                        )
            except Exception:
                # Error already logged by test_core
                pass

            # Step 6: Test get_connections immediately after portal auth
            console.print("\n[yellow]Step 6: Testing getBrokerConnections...[/yellow]")
            connections: List[Any] = []
            try:
                console.print(
                    f"[dim]  Session ID: {self.client.get_session_id() or 'Not set'}[/dim]"
                )
                console.print(
                    f"[dim]  Company ID: {self.client.get_company_id() or 'Not set'}[/dim]"
                )
                connections = await test_core(
                    "getBrokerConnections",
                    lambda: self.client.get_broker_connections(),
                    show_details=False,
                )
                console.print(
                    f"[green]✅ Successfully retrieved {len(connections)} broker connections[/green]"
                )
                if len(connections) > 0:
                    console.print("[dim]Connection details:[/dim]")
                    for index, conn in enumerate(connections[:3], 1):
                        # Handle both Pydantic models and dicts
                        if hasattr(conn, "broker_id"):
                            broker_id = conn.broker_id or "Unknown"
                            status = str(conn.status) if conn.status else "Unknown"
                        else:
                            broker_id = conn.get("broker_id") or "Unknown"
                            status = conn.get("status") or "Unknown"
                        console.print(
                            f"[dim]  {index}. Broker ID: {broker_id} - Status: {status}[/dim]"
                        )
            except Exception:
                # Error already logged by test_core
                pass

            # Step 7: Test get_accounts
            console.print("\n[yellow]Step 7: Testing getAccounts...[/yellow]")
            accounts_result: Optional[List[Any]] = None
            try:
                accounts_result = await test_core(
                    "getAccounts (paginated)",
                    lambda: self.client.get_accounts(page=1, per_page=10),
                    show_details=False,
                )
                # Python SDK returns list directly, not paginated result
                data = accounts_result if isinstance(accounts_result, list) else []
                console.print(f"[green]✅ Successfully retrieved {len(data)} accounts[/green]")
                if len(data) > 0:
                    console.print("[dim]Account details:[/dim]")
                    for index, account in enumerate(data[:3], 1):
                        account_number = (
                            account.get("account_number") or account.get("id") or "Unknown"
                        )
                        broker_id = account.get("broker_id") or "Unknown"
                        console.print(
                            f"[dim]  {index}. Account: {account_number} - Broker: {broker_id}[/dim]"
                        )
            except Exception:
                # Error already logged by test_core
                pass

            # Step 8: Test get_orders
            console.print("\n[yellow]Step 8: Testing getOrders...[/yellow]")
            orders_result: Optional[List[Any]] = None
            try:
                orders_result = await test_core(
                    "getOrders (paginated)",
                    lambda: self.client.get_orders(page=1, per_page=10),
                    show_details=False,
                )
                # Python SDK returns list directly, not paginated result
                data = orders_result if isinstance(orders_result, list) else []
                console.print(f"[green]✅ Successfully retrieved {len(data)} orders[/green]")
                if len(data) > 0:
                    console.print("[dim]Order details:[/dim]")
                    for index, order in enumerate(data[:3], 1):
                        symbol = order.get("symbol") or "Unknown"
                        status = order.get("status") or order.get("order_status") or "Unknown"
                        quantity = order.get("quantity") or order.get("order_qty") or "Unknown"
                        console.print(
                            f"[dim]  {index}. Symbol: {symbol} - Status: {status} - Quantity: {quantity}[/dim]"
                        )
            except Exception:
                # Error already logged by test_core
                pass

            # Step 9: Test get_balances
            console.print("\n[yellow]Step 9: Testing getBalances...[/yellow]")
            try:
                balances_result = await test_core(
                    "getBalances (paginated)",
                    lambda: self.client.get_balances(page=1, per_page=10),
                    show_details=False,
                )
                # Python SDK returns list directly, not paginated result
                data = balances_result if isinstance(balances_result, list) else []
                console.print(f"[green]✅ Successfully retrieved {len(data)} balances[/green]")
                if len(data) > 0:
                    console.print("[dim]Balance details:[/dim]")
                    for index, balance in enumerate(data[:3], 1):
                        cash_balance = (
                            balance.get("cash")
                            or balance.get("buying_power")
                            or balance.get("account_value")
                            or "Unknown"
                        )
                        account_number = (
                            balance.get("account_number") or balance.get("account_id") or "Unknown"
                        )
                        console.print(
                            f"[dim]  {index}. Account: {account_number} - Balance: {cash_balance}[/dim]"
                        )
            except Exception:
                # Error already logged by test_core
                pass

            # Step 10: Test get_positions
            console.print("\n[yellow]Step 10: Testing getPositions...[/yellow]")
            try:
                positions_result = await test_core(
                    "getPositions (paginated)",
                    lambda: self.client.get_positions(page=1, per_page=10),
                    show_details=False,
                )
                # Python SDK returns list directly, not paginated result
                data = positions_result if isinstance(positions_result, list) else []
                console.print(f"[green]✅ Successfully retrieved {len(data)} positions[/green]")
                if len(data) > 0:
                    console.print("[dim]Position details:[/dim]")
                    for index, position in enumerate(data[:3], 1):
                        symbol = position.get("symbol") or "Unknown"
                        quantity = position.get("quantity") or position.get("qty") or "Unknown"
                        side = position.get("side") or "Unknown"
                        console.print(
                            f"[dim]  {index}. Symbol: {symbol} - Quantity: {quantity} - Side: {side}[/dim]"
                        )
            except Exception:
                # Error already logged by test_core
                pass

            # Core methods summary
            console.print(
                f"\n[dim]  Core Methods Summary: {core_results['passed']}/{core_results['total']} passed[/dim]"
            )
            if core_results["failed"] > 0:
                console.print(
                    f"[yellow]  {core_results['failed']} core method(s) failed (see details above)[/yellow]"
                )
            else:
                console.print("[green]  ✅ All core methods passed![/green]")

            # Step 11: Test helper methods
            console.print("\n[yellow]Step 11: Testing helper methods...[/yellow]")
            helper_results = {"passed": 0, "failed": 0, "total": 0}

            # Helper to test a method and track results
            async def test_helper(name: str, fn, expected_type: str = "array") -> None:
                helper_results["total"] += 1
                try:
                    result = await fn()
                    is_valid = (
                        isinstance(result, list)
                        if expected_type == "array"
                        else (result and isinstance(result, dict))
                    )

                    if is_valid:
                        helper_results["passed"] += 1
                        console.print(f"[dim]  ✅ {name}[/dim]")
                    else:
                        helper_results["failed"] += 1
                        console.print(f"[red]  ❌ {name} (invalid return type)[/red]")
                except Exception as e:
                    helper_results["failed"] += 1
                    error_msg = str(e)[:50] if str(e) else "error"
                    console.print(f"[red]  ❌ {name} ({error_msg})[/red]")

            # Test broker list (getBrokerConnections is already tested in core methods)
            await test_helper("getBrokerList", lambda: self.client.get_broker_list())

            # Test getAll* methods (fetch all data across pages)
            await test_helper("getAllAccounts", lambda: self.client.get_all_accounts())
            await test_helper("getAllOrders", lambda: self.client.get_all_orders())
            await test_helper("getAllPositions", lambda: self.client.get_all_positions())
            await test_helper("getAllBalances", lambda: self.client.get_all_balances())
            await test_helper("getAllOrderGroups", lambda: self.client.get_all_order_groups())
            await test_helper("getAllPositionLots", lambda: self.client.get_all_position_lots())

            # Test filtered helper methods (use symbols/statuses from earlier results if available)
            sample_symbol = (
                orders_result[0].get("symbol")
                if orders_result and len(orders_result) > 0
                else "AAPL"
            )
            # Handle both Pydantic models and dicts
            sample_broker_id = None
            if connections and len(connections) > 0:
                conn = connections[0]
                if hasattr(conn, "broker_id"):
                    sample_broker_id = conn.broker_id
                else:
                    sample_broker_id = conn.get("broker_id")

            await test_helper("getOpenPositions", lambda: self.client.get_open_positions())
            await test_helper("getFilledOrders", lambda: self.client.get_filled_orders())
            await test_helper("getPendingOrders", lambda: self.client.get_pending_orders())
            await test_helper("getActiveAccounts", lambda: self.client.get_active_accounts())

            if sample_symbol:
                await test_helper(
                    f'getOrdersBySymbol("{sample_symbol}")',
                    lambda: self.client.get_orders_by_symbol(sample_symbol),
                )
                await test_helper(
                    f'getPositionsBySymbol("{sample_symbol}")',
                    lambda: self.client.get_positions_by_symbol(sample_symbol),
                )

            if sample_broker_id:
                await test_helper(
                    f'getOrdersByBroker("{sample_broker_id}")',
                    lambda: self.client.get_orders_by_broker(sample_broker_id),
                )
                await test_helper(
                    f'getPositionsByBroker("{sample_broker_id}")',
                    lambda: self.client.get_positions_by_broker(sample_broker_id),
                )

            # Test paginated methods (these return lists, not objects)
            await test_helper(
                "getAccounts",
                lambda: self.client.get_accounts(page=1, per_page=10),
                expected_type="array",
            )
            await test_helper(
                "getOrders",
                lambda: self.client.get_orders(page=1, per_page=10),
                expected_type="array",
            )
            await test_helper(
                "getPositions",
                lambda: self.client.get_positions(page=1, per_page=10),
                expected_type="array",
            )
            await test_helper(
                "getBalances",
                lambda: self.client.get_balances(page=1, per_page=10),
                expected_type="array",
            )
            await test_helper(
                "getOrderGroups",
                lambda: self.client.get_order_groups(page=1, per_page=10),
                expected_type="array",
            )
            await test_helper(
                "getPositionLots",
                lambda: self.client.get_position_lots(page=1, per_page=10),
                expected_type="array",
            )

            # Test order/position detail methods (require IDs from earlier results)
            if orders_result and len(orders_result) > 0:
                sample_order_id = orders_result[0].get("id") or orders_result[0].get("order_id")
                if sample_order_id:
                    await test_helper(
                        f'getOrderFills("{sample_order_id}")',
                        lambda: self.client.get_order_fills(
                            order_id=sample_order_id, page=1, per_page=10
                        ),
                        expected_type="array",
                    )
                    await test_helper(
                        f'getOrderEvents("{sample_order_id}")',
                        lambda: self.client.get_order_events(
                            order_id=sample_order_id, page=1, per_page=10
                        ),
                        expected_type="array",
                    )

            # Get position lots to find a lot ID for getPositionLotFills
            try:
                position_lots_result = await self.client.get_position_lots(page=1, per_page=10)
                if position_lots_result and len(position_lots_result) > 0:
                    sample_lot_id = (
                        position_lots_result[0].get("id")
                        or position_lots_result[0].get("lot_id")
                        or position_lots_result[0].get("position_lot_id")
                    )
                    if sample_lot_id:
                        await test_helper(
                            f'getPositionLotFills("{sample_lot_id}")',
                            lambda: self.client.get_position_lot_fills(
                                lot_id=sample_lot_id, page=1, per_page=10
                            ),
                            expected_type="array",
                        )
            except Exception:
                # If getPositionLots fails, skip getPositionLotFills test
                pass

            # Test disconnect (if enabled)
            if ENABLE_DISCONNECT and connections and len(connections) > 0:
                console.print("\n[yellow]Step 11.1: Testing disconnectCompany...[/yellow]")
                try:
                    conn = connections[0]
                    connection_id = (
                        conn.get("id")
                        if isinstance(conn, dict)
                        else (conn.id if hasattr(conn, "id") else None)
                    )
                    if connection_id:
                        await test_helper(
                            "disconnectCompany",
                            lambda: self.client.disconnect_company(connection_id),
                        )
                        console.print("[green]✅ Disconnect test completed[/green]")
                    else:
                        console.print(
                            "[yellow]⚠️  No connection ID available for disconnect test[/yellow]"
                        )
                except Exception as e:
                    console.print(f"[red]❌ Disconnect test failed: {str(e)[:50]}[/red]")
            elif ENABLE_DISCONNECT:
                console.print(
                    "[yellow]⚠️  ENABLE_DISCONNECT is true but no connections available[/yellow]"
                )

            # Summary
            console.print(
                f"\n[dim]  Helper Methods Summary: {helper_results['passed']}/{helper_results['total']} passed[/dim]"
            )
            if helper_results["failed"] > 0:
                console.print(
                    f"[yellow]  {helper_results['failed']} helper method(s) failed (see details above)[/yellow]"
                )
            else:
                console.print("[green]  ✅ All helper methods passed![/green]")

            # Step 12: Disconnect the first connection
            # if connections and len(connections) > 0:
            #     console.print("\n[yellow]Step 12: Disconnecting first connection...[/yellow]")
            #     try:
            #         first_connection = connections[0]
            #         # Handle both Pydantic models and dicts
            #         if hasattr(first_connection, "id"):
            #             connection_id = (
            #                 str(first_connection.id)
            #                 if first_connection.id
            #                 else (
            #                     str(first_connection.connection_id)
            #                     if hasattr(first_connection, "connection_id")
            #                     else None
            #                 )
            #             )
            #             broker_id = (
            #                 first_connection.broker_id
            #                 if hasattr(first_connection, "broker_id")
            #                 else "Unknown"
            #             )
            #         else:
            #             connection_id = first_connection.get("id") or first_connection.get(
            #                 "connection_id"
            #             )
            #             broker_id = first_connection.get("broker_id") or "Unknown"
            #         console.print(f"[dim]  Disconnecting connection: {connection_id}[/dim]")
            #         console.print(f"[dim]  Broker: {broker_id}[/dim]")

            #         await self.client.brokers.disconnect_company_from_broker(connection_id)
            #         console.print(
            #             f"[green]✅ Successfully disconnected connection {connection_id}[/green]"
            #         )
            #     except Exception as e:
            #         console.print(f"[red]❌ Failed to disconnect connection: {str(e)}[/red]")
            #         raise
            # else:
            #     console.print(
            #         "\n[yellow]Step 12: Skipping disconnect - no connections available[/yellow]"
            #     )

            console.print("\n[green]🎉 Demo completed successfully![/green]")
            console.print("\n[dim]📊 Test Summary:[/dim]")
            console.print(
                f"[dim]  Session methods: {session_results['passed']}/{session_results['total']} passed[/dim]"
            )
            console.print(
                f"[dim]  Core methods: {core_results['passed']}/{core_results['total']} passed[/dim]"
            )
            console.print(
                f"[dim]  Helper methods: {helper_results['passed']}/{helper_results['total']} passed[/dim]"
            )
            total_passed = (
                session_results["passed"] + core_results["passed"] + helper_results["passed"]
            )
            total_tests = session_results["total"] + core_results["total"] + helper_results["total"]
            if total_passed == total_tests:
                console.print(f"[green]  Total: {total_passed}/{total_tests} passed ✅[/green]")
            else:
                console.print(f"[yellow]  Total: {total_passed}/{total_tests} passed[/yellow]")
            console.print("\n[dim]You are now authenticated and can use all SDK methods.[/dim]")

        except Exception as e:
            console.print(f"\n[red]❌ Error:[/red] {e}")
            import traceback

            if os.getenv("DEBUG"):
                traceback.print_exc()
            sys.exit(1)


async def main() -> None:
    """Main entry point."""
    demo = FinaticDemo()
    await demo.run()


if __name__ == "__main__":
    asyncio.run(main())
