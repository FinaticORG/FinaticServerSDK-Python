#!/usr/bin/env python3
"""
FastAPI server for Python Server SDK Demo
Provides API endpoints that match the Client SDK interface
"""

import os
import asyncio
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the Python SDK
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from finatic_server import FinaticServerClient

# Global SDK client instance
sdk_client: Optional[FinaticServerClient] = None


# Request/Response models
class ApiResponse(BaseModel):
    success: bool
    data: Any = None
    error: Optional[str] = None


class SessionAuthenticateRequest(BaseModel):
    user_id: str


class OrderRequest(BaseModel):
    symbol: str

    # Accept both naming conventions from client SDK and expected format
    # Client SDK sends: orderQty, action, orderType, accountNumber, timeInForce, assetType
    # We expect: quantity, side, order_type, account, time_in_force, asset_type
    quantity: Optional[float] = None
    side: Optional[str] = None
    order_type: Optional[str] = None
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: Optional[str] = None
    broker: Optional[str] = None
    account: Optional[str] = None
    asset_type: Optional[str] = None

    # Client SDK field names
    orderQty: Optional[float] = None
    action: Optional[str] = None
    orderType: Optional[str] = None
    accountNumber: Optional[str] = None
    timeInForce: Optional[str] = None
    assetType: Optional[str] = None


class OrderCancelRequest(BaseModel):
    order_id: str


class OrderModifyRequest(BaseModel):
    order_id: str
    modifications: Dict[str, Any]


class TradingContextRequest(BaseModel):
    broker: Optional[str] = None
    account: Optional[str] = None


# Global trading context storage (in production, use proper session management)
trading_context = {"broker": None, "account": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup SDK client"""
    global sdk_client

    # Initialize SDK client with API from env (defaults to local)
    api_key = os.getenv("FINATIC_API_KEY", "demo_key_123")
    api_url = os.getenv("FINATIC_API_URL", "http://localhost:8000")

    print(f"🚀 Initializing Python Server SDK with mock data...")
    print(f"   API URL: {api_url}")
    print(f"   API Key: {api_key}")

    sdk_client = FinaticServerClient(api_key=api_key, base_url=api_url)

    print("✅ Python Server SDK initialized successfully")

    yield

    # Cleanup
    if sdk_client:
        print("🔄 Cleaning up Python Server SDK...")
        # SDK cleanup if needed


# Create FastAPI app
app = FastAPI(
    title="Finatic Python Server SDK API",
    description="API server for Python Server SDK demo",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Client demo app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "sdk": "python", "port": 8002}


# Session endpoints
class SessionStartRequest(BaseModel):
    user_id: Optional[str] = None


@app.post("/api/session/start")
async def start_session(request: SessionStartRequest = None):
    """Start a new session"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        print(f"🔄 Starting session with Python SDK...")
        print(f"   SDK client type: {type(sdk_client)}")
        print(
            f"   SDK client API key: {sdk_client.api_key[:15] if hasattr(sdk_client, 'api_key') and sdk_client.api_key else 'No API key'}..."
        )
        print(
            f"   SDK client base URL: {sdk_client._api_client.base_url if hasattr(sdk_client, '_api_client') else 'No API client'}"
        )

        # Extract user_id from request if provided
        user_id = request.user_id if request else None
        print(f"🔍 Starting session with user_id: {user_id}")
        print(f"🔍 Request object: {request}")
        print(f"🔍 Request body: {request.dict() if request else 'None'}")

        session_response = await sdk_client.start_session(user_id=user_id)
        print(f"✅ Session started successfully: {session_response}")

        # Debug: Check the response structure
        if hasattr(session_response, "data"):
            print(f"🔍 Session response has data: {session_response.data}")
        print(f"🔍 Session response session_id: {getattr(session_response, 'session_id', 'None')}")
        print(f"🔍 Session response company_id: {getattr(session_response, 'company_id', 'None')}")

        # Debug: Check what session info is stored
        print(f"🔍 SDK Session ID after start: {sdk_client.get_session_id()}")
        print(f"🔍 SDK Company ID after start: {sdk_client.get_company_id()}")

        # Return only essential information to the client, not internal session data
        # Don't expose session_id or company_id to the client
        return ApiResponse(
            success=True,
            data={
                "status": "started",
                "user_id": user_id,  # Return the user_id that was passed in
            },
        )
    except Exception as e:
        print(f"❌ Failed to start session: {e}")
        print(f"   Error type: {type(e)}")
        import traceback

        print(f"   Traceback: {traceback.format_exc()}")
        return ApiResponse(success=False, error=str(e))


@app.get("/api/session/user-id")
async def get_user_id():
    """Get current user ID"""
    try:
        if not sdk_client:
            return ApiResponse(success=False, data=None)

        # Get the user ID from the session by calling the main API
        session_id = sdk_client.get_session_id()
        company_id = sdk_client.get_company_id()

        if not session_id or not company_id:
            return ApiResponse(success=True, data=None)

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://localhost:8000/api/v1/session/{session_id}/user",
                    headers={
                        "Session-ID": session_id,
                        "Company-ID": company_id,
                    },
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        user_id = data.get("data", {}).get("user_id")
                        print(f"🔍 Get user ID: {user_id}")
                        return ApiResponse(success=True, data=user_id)
                    else:
                        print(f"❌ Get user ID failed with status: {response.status}")
                        return ApiResponse(success=True, data=None)
        except Exception as e:
            print(f"❌ Could not get user ID: {e}")
            return ApiResponse(success=True, data=None)
    except Exception as e:
        return ApiResponse(success=False, data=None)


@app.get("/api/session/is-authed")
async def is_authenticated():
    """Check if user is authenticated"""
    try:
        if not sdk_client:
            return ApiResponse(success=False, data=False)

        # Check if user is linked to the session by calling the main API
        session_id = sdk_client.get_session_id()
        company_id = sdk_client.get_company_id()

        if not session_id or not company_id:
            return ApiResponse(success=True, data=False)

        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://localhost:8000/api/v1/session/{session_id}/user",
                    headers={
                        "Session-ID": session_id,
                        "Company-ID": company_id,
                    },
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        user_id = data.get("data", {}).get("user_id")
                        # User is authenticated if they have a user_id in the session
                        is_authenticated = user_id is not None
                        print(
                            f"🔍 Session authentication check: user_id={user_id}, authenticated={is_authenticated}"
                        )
                        return ApiResponse(success=True, data=is_authenticated)
                    else:
                        return ApiResponse(success=True, data=False)
        except Exception as e:
            print(f"❌ Could not check session authentication: {e}")
            return ApiResponse(success=True, data=False)
    except Exception as e:
        return ApiResponse(success=False, data=False)


@app.get("/api/session/portal-url")
async def get_portal_url(
    brokers: Optional[str] = None, email: Optional[str] = None, theme_preset: Optional[str] = None
):
    """Get portal URL for authentication with optional parameters"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Parse brokers if provided (comma-separated list)
        broker_list = None
        if brokers:
            broker_list = [b.strip() for b in brokers.split(",") if b.strip()]

        # Build theme object if preset is provided
        theme_obj = None
        if theme_preset:
            theme_obj = {"preset": theme_preset}

        portal_url = await sdk_client.get_portal_url(
            theme=theme_obj, brokers=broker_list, email=email
        )
        return ApiResponse(success=True, data={"portal_url": portal_url})
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/session/confirm-auth")
async def confirm_auth():
    """Confirm authentication"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Check session data to see if user is logged in
        session_id = sdk_client.get_session_id()
        company_id = sdk_client.get_company_id()
        user_id = None

        print(f"🔍 Session ID: {session_id}")
        print(f"🔍 Company ID: {company_id}")

        if session_id:
            try:
                # Check the session data to see if user is linked by calling the main API
                import aiohttp

                async with aiohttp.ClientSession() as session:
                    # Call the main API to check session status
                    async with session.get(
                        f"http://localhost:8000/api/v1/session/{session_id}/user",
                        headers={
                            "Session-ID": session_id,
                            "Company-ID": company_id or "",
                        },
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            print(f"🔍 API Response: {data}")

                            # Extract user_id from the nested data structure
                            user_id = data.get("data", {}).get("user_id")
                            print(f"🔍 Extracted user_id: {user_id}")

                            if user_id:
                                # User is logged in - populate the SDK client with auth data
                                # Get the full token data from the API response
                                token_data = data.get("data", {})
                                access_token = token_data.get("access_token")
                                refresh_token = token_data.get("refresh_token")
                                expires_in = token_data.get("expires_in", 3600)

                                # Create proper UserToken object
                                from finatic_server.types import UserToken

                                sdk_client._user_token = UserToken(
                                    access_token=access_token,
                                    refresh_token=refresh_token,
                                    expires_in=expires_in,
                                    user_id=user_id,
                                    token_type=token_data.get("token_type", "Bearer"),
                                    scope=token_data.get("scope", "api:access"),
                                )
                                print(f"✅ User authenticated: {user_id}")
                                print(
                                    f"✅ Tokens set: access_token={access_token[:20] if access_token else 'None'}..."
                                )
                            else:
                                print("❌ No user linked to session")
                        else:
                            print(f"❌ Session check failed: {response.status}")
                            # Try to get response text for debugging
                            try:
                                error_text = await response.text()
                                print(f"   Error response: {error_text}")
                            except:
                                pass
            except Exception as e:
                print(f"❌ Could not check session: {e}")
                return ApiResponse(success=False, data=None, error="Session check failed")

        # Return success/failure based on whether user is authenticated
        if user_id:
            user_info = {"user_id": user_id, "success": True}
        else:
            user_info = {"user_id": None, "success": False}
        return ApiResponse(
            success=True,
            data=user_info,
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


# Broker endpoints
@app.get("/api/broker/list")
async def get_broker_list():
    """Get list of available brokers"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        brokers = await sdk_client.get_brokers()
        return ApiResponse(
            success=True,
            data=[
                broker.model_dump() if hasattr(broker, "model_dump") else broker
                for broker in brokers
            ],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/broker/connections")
async def get_broker_connections():
    """Get broker connections"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        connections = await sdk_client.get_connections()
        return ApiResponse(
            success=True,
            data=[
                conn.model_dump() if hasattr(conn, "model_dump") else conn for conn in connections
            ],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/broker/accounts")
async def get_accounts(page: int = 1, per_page: int = 100, filter: Optional[str] = None):
    """Get broker accounts with pagination"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Use the new get_accounts method with built-in pagination
        result = await sdk_client.get_accounts(page=page, per_page=per_page)

        return ApiResponse(
            success=True,
            data={
                "data": [
                    acc.model_dump() if hasattr(acc, "model_dump") else acc for acc in result.data
                ],
                "pagination": {
                    "page": result.current_page,
                    "per_page": per_page,
                    "has_next": result.has_next,
                    "has_previous": result.has_previous,
                },
            },
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/broker/accounts/all")
async def get_all_accounts(filter: Optional[str] = None):
    """Get all broker accounts"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        accounts = await sdk_client.get_all_accounts()
        return ApiResponse(
            success=True,
            data=[acc.model_dump() if hasattr(acc, "model_dump") else acc for acc in accounts],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/broker/disconnect")
async def disconnect_company(request: Dict[str, str]):
    """Disconnect a company/broker connection"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        connection_id = request.get("connection_id")
        if not connection_id or not connection_id.strip():
            # In demo environment, don't fail if no connection_id provided
            print(
                f"🔍 disconnect_company called with empty connection_id - returning success for demo"
            )
            return ApiResponse(
                success=True,
                data={"message": "No connection_id provided - demo mode", "disconnected": False},
            )

        result = await sdk_client.disconnect_company(connection_id)
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        # In demo environment, return success even if the connection doesn't exist
        error_msg = str(e)
        if "not found" in error_msg.lower() or "400" in error_msg or "404" in error_msg:
            print(f"🔍 disconnect_company failed but returning success for demo: {error_msg}")
            return ApiResponse(
                success=True,
                data={
                    "message": f"Connection not found or invalid: {error_msg}",
                    "disconnected": False,
                },
            )
        # Re-raise unexpected errors
        return ApiResponse(success=False, error=str(e))


# Trading endpoints
@app.get("/api/trading/orders")
async def get_orders(page: int = 1, per_page: int = 100, filter: Optional[str] = None):
    """Get orders with pagination"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Use the new get_orders method with built-in pagination
        result = await sdk_client.get_orders(page=page, per_page=per_page)

        return ApiResponse(
            success=True,
            data={
                "data": [
                    order.model_dump() if hasattr(order, "model_dump") else order
                    for order in result.data
                ],
                "pagination": {
                    "page": result.current_page,
                    "per_page": per_page,
                    "has_next": result.has_next,
                    "has_previous": result.has_previous,
                },
            },
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/orders/all")
async def get_all_orders(filter: Optional[str] = None):
    """Get all orders"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Use the new get_all_broker_orders method
        orders = await sdk_client.get_all_orders()

        return ApiResponse(
            success=True,
            data=[
                order.model_dump() if hasattr(order, "model_dump") else order for order in orders
            ],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/positions")
async def get_positions(page: int = 1, per_page: int = 100, filter: Optional[str] = None):
    """Get positions with pagination"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Use the new get_positions method with built-in pagination
        result = await sdk_client.get_positions(page=page, per_page=per_page)

        return ApiResponse(
            success=True,
            data={
                "data": [
                    pos.model_dump() if hasattr(pos, "model_dump") else pos for pos in result.data
                ],
                "pagination": {
                    "page": result.current_page,
                    "per_page": per_page,
                    "has_next": result.has_next,
                    "has_previous": result.has_previous,
                },
            },
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/positions/all")
async def get_all_positions(filter: Optional[str] = None):
    """Get all positions"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Use the new get_all_broker_positions method
        positions = await sdk_client.get_all_positions()

        return ApiResponse(
            success=True,
            data=[pos.model_dump() if hasattr(pos, "model_dump") else pos for pos in positions],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/balances")
async def get_balances(page: int = 1, per_page: int = 100, filter: Optional[str] = None):
    """Get balances with pagination"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Use the new get_balances method with built-in pagination
        result = await sdk_client.get_balances(page=page, per_page=per_page)

        return ApiResponse(
            success=True,
            data={
                "data": [
                    bal.model_dump() if hasattr(bal, "model_dump") else bal for bal in result.data
                ],
                "pagination": {
                    "page": result.current_page,
                    "per_page": per_page,
                    "has_next": result.has_next,
                    "has_previous": result.has_previous,
                },
            },
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/balances/all")
async def get_all_balances(filter: Optional[str] = None):
    """Get all balances"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Use the new get_all_broker_balances method
        balances = await sdk_client.get_all_balances()

        return ApiResponse(
            success=True,
            data=[bal.model_dump() if hasattr(bal, "model_dump") else bal for bal in balances],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


# Trading context endpoints removed - pass broker/account as parameters instead


# Order management endpoints
@app.post("/api/trading/order")
async def place_order(request: OrderRequest):
    """Place a new order"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # Debug: Print the incoming request data
        print(f"🔍 OrderRequest received: {request}")
        print(f"🔍 Request dict: {request.dict() if hasattr(request, 'dict') else request}")

        # Handle field mapping from client SDK to expected format - convert to dict first for safer access
        request_dict = request.dict() if hasattr(request, "dict") else request.__dict__

        # Get values from either field naming convention
        quantity = request_dict.get("quantity") or request_dict.get("orderQty")
        side = request_dict.get("side") or request_dict.get("action")
        order_type = request_dict.get("order_type") or request_dict.get("orderType")
        account = request_dict.get("account") or request_dict.get("accountNumber")
        time_in_force = (
            request_dict.get("time_in_force") or request_dict.get("timeInForce") or "day"
        )
        raw_asset_type = request_dict.get("asset_type") or request_dict.get("assetType") or "equity"

        # Use asset type directly - no mapping needed since we standardized on backend format
        asset_type = raw_asset_type.lower() if raw_asset_type else "equity"

        # Handle some common aliases but keep the standardized format
        if asset_type == "stock":
            asset_type = "equity"
        elif asset_type in ["option", "options"]:
            asset_type = "equity_option"
        elif asset_type in ["crypto", "cryptocurrency"]:
            asset_type = "crypto"
        elif asset_type in ["future", "futures"]:
            asset_type = "future"
        elif asset_type == "forex":
            asset_type = "forex"

        print(f"🔍 Asset type: '{raw_asset_type}' -> '{asset_type}'")

        # Validate required fields
        if not quantity:
            raise HTTPException(status_code=400, detail="Field required: quantity (or orderQty)")
        if not side:
            raise HTTPException(status_code=400, detail="Field required: side (or action)")
        if not order_type:
            raise HTTPException(status_code=400, detail="Field required: order_type (or orderType)")

        # Convert request to SDK format - use field names expected by the SDK client
        order_params = {
            "symbol": request.symbol,
            "quantity": quantity,  # SDK client expects "quantity", not "order_qty"
            "side": side,  # SDK client expects "side", not "action"
            "order_type": order_type,
            "asset_type": asset_type,
            "time_in_force": time_in_force,
        }

        if request.price:
            order_params["price"] = request.price
        if request.stop_price:
            order_params["stop_price"] = request.stop_price
        if request.broker:
            order_params["broker"] = request.broker
        if account:
            order_params["account_number"] = account

        print(f"🔍 Order params being sent to SDK: {order_params}")
        result = await sdk_client.place_order(order_params)
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        print(f"🔍 Error in place_order: {e}")
        print(f"🔍 Error type: {type(e)}")
        import traceback

        print(f"🔍 Traceback: {traceback.format_exc()}")
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/cancel")
async def cancel_order(request: OrderCancelRequest):
    """Cancel an order"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.cancel_order(request.order_id)
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/modify")
async def modify_order(request: OrderModifyRequest):
    """Modify an order"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.modify_order(request.order_id, request.modifications)
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


# Convenience filter endpoints
@app.get("/api/trading/positions/open")
async def get_open_positions():
    """Get only open positions."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        positions = await sdk_client.get_open_positions()
        return ApiResponse(
            success=True,
            data=[pos.model_dump() if hasattr(pos, "model_dump") else pos for pos in positions],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/orders/filled")
async def get_filled_orders():
    """Get only filled orders."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        orders = await sdk_client.get_filled_orders()
        return ApiResponse(
            success=True,
            data=[
                order.model_dump() if hasattr(order, "model_dump") else order for order in orders
            ],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/orders/pending")
async def get_pending_orders():
    """Get only pending orders."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        orders = await sdk_client.get_pending_orders()
        return ApiResponse(
            success=True,
            data=[
                order.model_dump() if hasattr(order, "model_dump") else order for order in orders
            ],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/accounts/active")
async def get_active_accounts():
    """Get only active accounts."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        accounts = await sdk_client.get_active_accounts()
        return ApiResponse(
            success=True,
            data=[acc.model_dump() if hasattr(acc, "model_dump") else acc for acc in accounts],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/orders/by-symbol/{symbol}")
async def get_orders_by_symbol(symbol: str):
    """Get orders filtered by symbol."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        orders = await sdk_client.get_orders_by_symbol(symbol)
        return ApiResponse(
            success=True,
            data=[
                order.model_dump() if hasattr(order, "model_dump") else order for order in orders
            ],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/positions/by-symbol/{symbol}")
async def get_positions_by_symbol(symbol: str):
    """Get positions filtered by symbol."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        positions = await sdk_client.get_positions_by_symbol(symbol)
        return ApiResponse(
            success=True,
            data=[pos.model_dump() if hasattr(pos, "model_dump") else pos for pos in positions],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/orders/by-broker/{broker}")
async def get_orders_by_broker(broker: str):
    """Get orders filtered by broker."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        orders = await sdk_client.get_orders_by_broker(broker)
        return ApiResponse(
            success=True,
            data=[
                order.model_dump() if hasattr(order, "model_dump") else order for order in orders
            ],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/positions/by-broker/{broker}")
async def get_positions_by_broker(broker: str):
    """Get positions filtered by broker."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        positions = await sdk_client.get_positions_by_broker(broker)
        return ApiResponse(
            success=True,
            data=[pos.model_dump() if hasattr(pos, "model_dump") else pos for pos in positions],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


# Asset-specific order endpoints
@app.post("/api/trading/order/stock/market")
async def place_stock_market_order(request: OrderRequest):
    """Place a stock market order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_stock_market_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/stock/limit")
async def place_stock_limit_order(request: OrderRequest):
    """Place a stock limit order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_stock_limit_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.price or 0,
            request.time_in_force or request.timeInForce or "gtc",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/stock/stop")
async def place_stock_stop_order(request: OrderRequest):
    """Place a stock stop order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_stock_stop_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.stop_price or request.stopPrice or 0,
            request.time_in_force or request.timeInForce or "gtc",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/crypto/market")
async def place_crypto_market_order(request: OrderRequest):
    """Place a crypto market order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_crypto_market_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/crypto/limit")
async def place_crypto_limit_order(request: OrderRequest):
    """Place a crypto limit order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_crypto_limit_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.price or 0,
            request.time_in_force or request.timeInForce or "gtc",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/options/market")
async def place_options_market_order(request: OrderRequest):
    """Place an options market order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_options_market_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/options/limit")
async def place_options_limit_order(request: OrderRequest):
    """Place an options limit order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_options_limit_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.price or 0,
            request.time_in_force or request.timeInForce or "gtc",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/futures/market")
async def place_futures_market_order(request: OrderRequest):
    """Place a futures market order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_futures_market_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/order/futures/limit")
async def place_futures_limit_order(request: OrderRequest):
    """Place a futures limit order."""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        result = await sdk_client.place_futures_limit_order(
            request.symbol,
            request.quantity or request.orderQty or 0,
            request.side or request.action or "buy",
            request.price or 0,
            request.time_in_force or request.timeInForce or "gtc",
            request.broker,
            request.account or request.accountNumber,
        )
        return ApiResponse(
            success=True, data=result.model_dump() if hasattr(result, "model_dump") else result
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


if __name__ == "__main__":
    print("🚀 Starting Finatic Python Server SDK API...")
    print("   Port: 8002")
    print("   CORS enabled for: http://localhost:3000")
    print("   Make sure FINATIC_API_KEY is set in your environment")

    uvicorn.run("api_server:app", host="0.0.0.0", port=8002, reload=True, log_level="info")
