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

        # Store config for later use in async init
        self.is_dev = os.getenv("NODE_ENV") != "production" or "localhost" in API_URL
        self.api_key = API_KEY
        self.api_url = API_URL
        self.sdk_config = {
            "log_level": "debug" if self.is_dev else "error",
            "structured_logging": True,
        }
        self.client = None  # Will be initialized in run()

    async def run(self) -> None:
        """Run the demo application."""
        console.print("\n[bold blue]🚀 Finatic Server SDK Python Demo[/bold blue]\n")
        console.print("[dim]This demo follows the actual Python SDK authentication flow.\n[/dim]")

        # Show configuration
        console.print("[dim]Configuration:[/dim]")
        console.print(f"[dim]  API URL: {API_URL}[/dim]")
        console.print(f"[dim]  API Key: {API_KEY[:10]}...\n[/dim]")

        try:
            # Step 1: Initialize SDK with session (single call - creates instance and starts session)
            console.print("[yellow]Step 1: Initializing SDK and starting session...[/yellow]")
            try:
                # Use the classmethod init() - creates instance AND starts session automatically
                # This matches the client SDK pattern: FinaticConnect.init()
                # Update sdk_config to include base_url
                sdk_config_with_url = {**self.sdk_config, 'base_url': API_URL}
                self.client = await FinaticServer.init(
                    api_key=API_KEY,
                    user_id=None,
                    sdk_config=sdk_config_with_url
                )
                
                session_id = self.client.get_session_id()
                company_id = self.client.get_company_id()
                console.print(f"[green]✅ SDK initialized and session started successfully[/green]")
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
                elif "Session not initialized" in error_msg or "session" in error_msg.lower():
                    console.print("[red]❌ Session initialization error[/red]")
                    console.print("[yellow]💡 This usually means:[/yellow]")
                    console.print("[dim]  • Session context was not set properly[/dim]")
                    console.print("[dim]  • start_session() did not complete successfully[/dim]")
                    if self.client:
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
                    # token_type removed - no longer returned

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

            # Helper to convert Pydantic models to dicts
            def to_dict(obj):
                """Convert Pydantic model or object to dict."""
                if isinstance(obj, dict):
                    return obj
                if hasattr(obj, 'model_dump'):
                    return obj.model_dump()
                if hasattr(obj, '__dict__'):
                    return {k: to_dict(v) for k, v in obj.__dict__.items() if not k.startswith('_')}
                return obj
            
            # Helper to safely get value from dict or object
            def safe_get(obj, key, default=None):
                """Safely get value from dict or object attribute."""
                if isinstance(obj, dict):
                    return obj.get(key, default)
                return getattr(obj, key, default)
            
            # Helper to extract data from FinaticResponse
            def extract_data(response):
                """Extract data from FinaticResponse dict or object."""
                # Convert to dict if it's an object
                if not isinstance(response, dict):
                    response = to_dict(response)
                
                if isinstance(response, dict) and 'success' in response:
                    data = response.get('success', {}).get('data', []) if isinstance(response.get('success'), dict) else []
                    # Convert list items to dicts if they're objects
                    return [to_dict(item) if not isinstance(item, dict) else item for item in data]
                # Fallback for direct data (backward compatibility)
                data = response if isinstance(response, list) else []
                return [to_dict(item) if not isinstance(item, dict) else item for item in data]

            # Step 5.1: Fetch orders for a specific Finatic account id
            console.print("\n[yellow]Step 5.1: Testing core methods...[/yellow]")
            try:
                # Use dict or kwargs - SDK converts to params object internally
                # get_all_orders returns FinaticResponse[list[OrderResponse]], extract data
                filtered_orders_response = await test_core(
                    "getAllOrders (filtered)",
                    lambda: self.client.get_all_orders(account_id=ACCOUNT_ID_FILTER),
                    show_details=False,
                )
                filtered_orders = extract_data(filtered_orders_response)
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
                # get_broker_connections returns FinaticResponse[list[UserBrokerConnections]], extract data
                broker_connections_response = await test_core(
                    "getBrokerConnections",
                    lambda: self.client.get_broker_connections(),
                    show_details=False,
                )
                connections = broker_connections_response.get('success', {}).get('data', []) if isinstance(broker_connections_response, dict) else []
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
                # get_accounts returns FinaticResponse[list[Accounts]], extract data
                # Use limit/offset instead of page/per_page
                accounts_response = await test_core(
                    "getAccounts",
                    lambda: self.client.get_accounts(limit=10, offset=0),
                    show_details=False,
                )
                data = accounts_response.get('success', {}).get('data', []) if isinstance(accounts_response, dict) else []
                console.print(f"[green]✅ Successfully retrieved {len(data)} accounts[/green]")
                if len(data) > 0:
                    # Show full response structure for first account
                    import json
                    first_account = data[0]
                    console.print(f"[dim]First account structure (keys): {list(first_account.keys()) if isinstance(first_account, dict) else type(first_account)}[/dim]")
                    console.print(f"[dim]First account (full JSON):[/dim]")
                    console.print(Panel(json.dumps(first_account, indent=2, default=str), title="Account Response", border_style="dim"))
                    
                    console.print("[dim]Account details:[/dim]")
                    for index, account in enumerate(data[:3], 1):
                        # Ensure account is a dict
                        account_dict = to_dict(account) if not isinstance(account, dict) else account
                        
                        # Python SDK converts camelCase to snake_case: accountId -> account_id
                        account_number = (
                            account_dict.get("account_id")
                            or account_dict.get("account_number")
                            or account_dict.get("accountId")
                            or account_dict.get("accountNumber")
                            or account_dict.get("id")
                            or "Unknown"
                        )
                        broker_id = account_dict.get("broker_id") or account_dict.get("brokerId") or "Unknown"
                        console.print(
                            f"[dim]  {index}. Account: {account_number} - Broker: {broker_id}[/dim]"
                        )
            except Exception:
                # Error already logged by test_core
                pass

            # Step 8: Test get_orders
            console.print("\n[yellow]Step 8: Testing getOrders...[/yellow]")
            orders_result: Optional[List[Any]] = None
            orders_response = None
            try:
                # get_orders returns FinaticResponse[list[OrderResponse]], extract data
                # Use limit/offset instead of page/per_page
                orders_response = await test_core(
                    "getOrders",
                    lambda: self.client.get_orders(limit=10, offset=0),
                    show_details=False,
                )
                data = orders_response.get('success', {}).get('data', []) if isinstance(orders_response, dict) else []
                orders_result = data  # Store for later use
                console.print(f"[green]✅ Successfully retrieved {len(data)} orders[/green]")
                if len(data) > 0:
                    # Show full response structure for first order
                    import json
                    first_order = data[0]
                    console.print(f"[dim]First order structure (keys): {list(first_order.keys()) if isinstance(first_order, dict) else type(first_order)}[/dim]")
                    console.print(f"[dim]First order (full JSON):[/dim]")
                    console.print(Panel(json.dumps(first_order, indent=2, default=str), title="Order Response", border_style="dim"))
                    
                    console.print("[dim]Order details:[/dim]")
                    for index, order in enumerate(data[:3], 1):
                        # Ensure order is a dict (extract_data should handle this, but double-check)
                        order_dict = to_dict(order) if not isinstance(order, dict) else order
                        
                        # Python SDK converts camelCase to snake_case: securityId -> security_id
                        # FDX orders have symbol in legs[0].security_id
                        symbol = "Unknown"
                        legs = order_dict.get("legs") or []
                        if len(legs) > 0:
                            leg = to_dict(legs[0]) if not isinstance(legs[0], dict) else legs[0]
                            symbol = leg.get("security_id") or leg.get("securityId") or "Unknown"
                        else:
                            symbol = order_dict.get("security_id") or order_dict.get("securityId") or "Unknown"
                        
                        # Status is at top level (snake_case in Python SDK)
                        status = "Unknown"
                        status_val = order_dict.get("status")
                        # Handle anyOf union types (extract actual_instance if present)
                        if isinstance(status_val, dict) and "actual_instance" in status_val:
                            status = status_val["actual_instance"]
                        elif status_val is not None:
                            status = status_val
                        
                        # Quantity is in legs[0].quantity (snake_case)
                        quantity = "Unknown"
                        if len(legs) > 0:
                            leg = to_dict(legs[0]) if not isinstance(legs[0], dict) else legs[0]
                            qty_val = leg.get("quantity")
                            if isinstance(qty_val, dict) and "actual_instance" in qty_val:
                                quantity = qty_val["actual_instance"]
                            elif qty_val is not None:
                                quantity = qty_val
                        
                        console.print(
                            f"[dim]  {index}. Symbol: {symbol} - Status: {status} - Quantity: {quantity}[/dim]"
                        )
            except Exception:
                # Error already logged by test_core
                pass

            # Step 9: Test get_balances
            console.print("\n[yellow]Step 9: Testing getBalances...[/yellow]")
            try:
                # get_balances returns FinaticResponse[list[Balances]], extract data
                # Use limit/offset instead of page/per_page
                balances_response = await test_core(
                    "getBalances",
                    lambda: self.client.get_balances(limit=10, offset=0),
                    show_details=False,
                )
                data = balances_response.get('success', {}).get('data', []) if isinstance(balances_response, dict) else []
                console.print(f"[green]✅ Successfully retrieved {len(data)} balances[/green]")
                if len(data) > 0:
                    # Show full response structure for first balance
                    import json
                    first_balance = data[0]
                    console.print(f"[dim]First balance structure (keys): {list(first_balance.keys()) if isinstance(first_balance, dict) else type(first_balance)}[/dim]")
                    console.print(f"[dim]First balance (full JSON):[/dim]")
                    console.print(Panel(json.dumps(first_balance, indent=2, default=str), title="Balance Response", border_style="dim"))
                    
                    console.print("[dim]Balance details:[/dim]")
                    for index, balance in enumerate(data[:3], 1):
                        # Ensure balance is a dict
                        balance_dict = to_dict(balance) if not isinstance(balance, dict) else balance
                        
                        # Extract actual_instance from anyOf union types
                        def extract_value(val):
                            if isinstance(val, dict) and "actual_instance" in val:
                                return val["actual_instance"]
                            return val
                        
                        cash_balance_val = (
                            balance_dict.get("current_balance")
                            or balance_dict.get("available_balance")
                            or balance_dict.get("cash_balance")
                            or balance_dict.get("currentBalance")
                            or balance_dict.get("availableBalance")
                            or balance_dict.get("cashBalance")
                            or balance_dict.get("buying_power")
                            or balance_dict.get("buyingPower")
                            or balance_dict.get("cash")
                            or balance_dict.get("account_value")
                        )
                        cash_balance = extract_value(cash_balance_val) if cash_balance_val is not None else "Unknown"
                        
                        account_number = (
                            balance_dict.get("account_id")
                            or balance_dict.get("accountId")
                            or balance_dict.get("account_number")
                            or "Unknown"
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
                # get_positions returns FinaticResponse[list[PositionResponse]], extract data
                # Use limit/offset instead of page/per_page
                positions_response = await test_core(
                    "getPositions",
                    lambda: self.client.get_positions(limit=10, offset=0),
                    show_details=False,
                )
                data = positions_response.get('success', {}).get('data', []) if isinstance(positions_response, dict) else []
                console.print(f"[green]✅ Successfully retrieved {len(data)} positions[/green]")
                if len(data) > 0:
                    # Show full response structure for first position
                    import json
                    first_position = data[0]
                    console.print(f"[dim]First position structure (keys): {list(first_position.keys()) if isinstance(first_position, dict) else type(first_position)}[/dim]")
                    console.print(f"[dim]First position (full JSON):[/dim]")
                    console.print(Panel(json.dumps(first_position, indent=2, default=str), title="Position Response", border_style="dim"))
                    
                    console.print("[dim]Position details:[/dim]")
                    for index, position in enumerate(data[:3], 1):
                        # Ensure position is a dict
                        position_dict = to_dict(position) if not isinstance(position, dict) else position
                        
                        # Extract actual_instance from anyOf union types
                        def extract_value(val):
                            if isinstance(val, dict) and "actual_instance" in val:
                                return val["actual_instance"]
                            return val
                        
                        # Python SDK converts camelCase to snake_case: securityId -> security_id
                        symbol = (
                            position_dict.get("security_id")
                            or position_dict.get("securityId")
                            or position_dict.get("symbol")
                            or "Unknown"
                        )
                        
                        qty_val = position_dict.get("quantity") or position_dict.get("qty")
                        quantity = extract_value(qty_val) if qty_val is not None else "Unknown"
                        
                        side_val = position_dict.get("side")
                        side = extract_value(side_val) if side_val is not None else "Unknown"
                        
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
                    response = await fn()
                    # Extract data from FinaticResponse if present
                    result = extract_data(response)
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
            # get_brokers returns FinaticResponse[list[BrokerInfo]], extract data from response
            async def get_brokers_data():
                response = await self.client.get_brokers()
                return response.get('success', {}).get('data', []) if isinstance(response, dict) else []
            await test_helper("getBrokers", get_brokers_data)

            # Test getAll* methods (fetch all data across pages)
            # These return FinaticResponse[list[...]], test_helper will extract data
            await test_helper("getAllAccounts", lambda: self.client.get_all_accounts())
            await test_helper("getAllOrders", lambda: self.client.get_all_orders())
            await test_helper("getAllPositions", lambda: self.client.get_all_positions())
            await test_helper("getAllBalances", lambda: self.client.get_all_balances())
            await test_helper("getAllOrderGroups", lambda: self.client.get_all_order_groups())
            
            # Test getAllPositionLots and use result for getAllPositionLotFills
            all_position_lots_result: List[Any] = []
            try:
                all_position_lots_response = await self.client.get_all_position_lots()
                all_position_lots_result = extract_data(all_position_lots_response)
            except Exception:
                # Error will be logged by test_helper below
                pass
            await test_helper("getAllPositionLots", lambda: self.client.get_all_position_lots())

            # Test order/position detail methods (require IDs from earlier results)
            # Extract orders data from response if available (from getAllOrders call earlier)
            orders_data = orders_result if orders_result else (orders_response.get('success', {}).get('data', []) if isinstance(orders_response, dict) else [])
            if orders_data and len(orders_data) > 0:
                sample_order_id = orders_data[0].get("id") or orders_data[0].get("order_id")
                if sample_order_id:
                    async def get_all_order_fills_data():
                        response = await self.client.get_all_order_fills(order_id=sample_order_id)
                        return extract_data(response)
                    await test_helper(f'getAllOrderFills("{sample_order_id}")', get_all_order_fills_data)
                    
                    async def get_all_order_events_data():
                        response = await self.client.get_all_order_events(order_id=sample_order_id)
                        return extract_data(response)
                    await test_helper(f'getAllOrderEvents("{sample_order_id}")', get_all_order_events_data)

            # Test getAllPositionLotFills (use all_position_lots_result if available)
            if all_position_lots_result and len(all_position_lots_result) > 0:
                sample_lot_id = (
                    all_position_lots_result[0].get("id")
                    or all_position_lots_result[0].get("lot_id")
                    or all_position_lots_result[0].get("position_lot_id")
                )
                if sample_lot_id:
                    async def get_all_position_lot_fills_data():
                        response = await self.client.get_all_position_lot_fills(lot_id=sample_lot_id)
                        return extract_data(response)
                    await test_helper(f'getAllPositionLotFills("{sample_lot_id}")', get_all_position_lot_fills_data)

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
                            lambda: self.client.disconnect_company_from_broker(connection_id=connection_id),
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
