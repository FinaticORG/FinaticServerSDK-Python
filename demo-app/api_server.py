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

    # Initialize SDK client
    api_key = os.getenv("FINATIC_API_KEY", "demo_key_123")
    api_url = os.getenv("FINATIC_API_URL", "https://api.finatic.dev")

    print(f"🚀 Initializing Python Server SDK...")
    print(f"   API URL: {api_url}")
    print(f"   API Key: {api_key[:10]}...")
    print(f"   API Key length: {len(api_key)}")
    print(f"   Environment FINATIC_API_KEY exists: {'FINATIC_API_KEY' in os.environ}")

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
@app.post("/api/session/start")
async def start_session():
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

        session_response = await sdk_client.start_session()
        print(f"✅ Session started successfully: {session_response}")

        return ApiResponse(
            success=True,
            data=session_response.model_dump()
            if hasattr(session_response, "model_dump")
            else session_response,
        )
    except Exception as e:
        print(f"❌ Failed to start session: {e}")
        print(f"   Error type: {type(e)}")
        import traceback

        print(f"   Traceback: {traceback.format_exc()}")
        return ApiResponse(success=False, error=str(e))


@app.post("/api/session/authenticate")
async def authenticate_session(request: SessionAuthenticateRequest):
    """Authenticate session with user ID"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        # In a real implementation, this would authenticate the user
        # For demo purposes, we'll just store the user ID
        return ApiResponse(success=True, data={"user_id": request.user_id, "authenticated": True})
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/session/user")
async def get_session_user():
    """Get session user information"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        user_info = await sdk_client.get_session_user()
        return ApiResponse(
            success=True,
            data=user_info.model_dump() if hasattr(user_info, "model_dump") else user_info,
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/session/user-id")
async def get_user_id():
    """Get current user ID"""
    try:
        if not sdk_client:
            return ApiResponse(success=False, data=None)

        # Get the user ID from the session user data
        try:
            user_info = await sdk_client.get_session_user()
            user_id = (
                user_info.get("user_id")
                if isinstance(user_info, dict)
                else getattr(user_info, "user_id", None)
            )
            return ApiResponse(success=True, data=user_id)
        except Exception:
            # If we can't get session user, return null
            return ApiResponse(success=True, data=None)
    except Exception as e:
        return ApiResponse(success=False, data=None)


@app.get("/api/session/is-authed")
async def is_authenticated():
    """Check if user is authenticated"""
    try:
        if not sdk_client:
            return ApiResponse(success=False, data=False)

        # Check if we can get session user - if successful, user is authenticated
        try:
            await sdk_client.get_session_user()
            return ApiResponse(success=True, data=True)
        except Exception:
            # If get_session_user fails, user is not authenticated
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
    """Confirm authentication by getting session user"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        user_info = await sdk_client.get_session_user()
        return ApiResponse(
            success=True,
            data=user_info.model_dump() if hasattr(user_info, "model_dump") else user_info,
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

        brokers = await sdk_client.get_broker_list()
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

        connections = await sdk_client.get_broker_connections()
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

        accounts = await sdk_client.get_all_broker_accounts()

        # Simple pagination (in production, implement proper pagination)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_accounts = accounts[start:end]

        return ApiResponse(
            success=True,
            data={
                "data": [
                    acc.model_dump() if hasattr(acc, "model_dump") else acc
                    for acc in paginated_accounts
                ],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(accounts),
                    "total_pages": (len(accounts) + per_page - 1) // per_page,
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

        accounts = await sdk_client.get_all_broker_accounts()
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

        orders = await sdk_client.get_orders()

        # Simple pagination - get_orders() returns a list directly
        order_list = orders if isinstance(orders, list) else []

        start = (page - 1) * per_page
        end = start + per_page
        paginated_orders = order_list[start:end]

        return ApiResponse(
            success=True,
            data={
                "data": [
                    order.model_dump() if hasattr(order, "model_dump") else order
                    for order in paginated_orders
                ],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(order_list),
                    "total_pages": (len(order_list) + per_page - 1) // per_page,
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

        orders = await sdk_client.get_orders()
        # get_orders() returns a list directly, not an object with .data property
        order_list = orders if isinstance(orders, list) else []

        return ApiResponse(
            success=True,
            data=[
                order.model_dump() if hasattr(order, "model_dump") else order
                for order in order_list
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

        positions = await sdk_client.get_positions()

        # Simple pagination - get_positions() returns a list directly
        position_list = positions if isinstance(positions, list) else []

        start = (page - 1) * per_page
        end = start + per_page
        paginated_positions = position_list[start:end]

        return ApiResponse(
            success=True,
            data={
                "data": [
                    pos.model_dump() if hasattr(pos, "model_dump") else pos
                    for pos in paginated_positions
                ],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(position_list),
                    "total_pages": (len(position_list) + per_page - 1) // per_page,
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

        positions = await sdk_client.get_positions()
        # get_positions() returns a list directly, not an object with .data property
        position_list = positions if isinstance(positions, list) else []

        return ApiResponse(
            success=True,
            data=[pos.model_dump() if hasattr(pos, "model_dump") else pos for pos in position_list],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/balances")
async def get_balances(page: int = 1, per_page: int = 100, filter: Optional[str] = None):
    """Get balances with pagination"""
    try:
        if not sdk_client:
            raise HTTPException(status_code=500, detail="SDK client not initialized")

        balances = await sdk_client.get_balances()

        # Simple pagination
        balance_list = balances or []

        start = (page - 1) * per_page
        end = start + per_page
        paginated_balances = balance_list[start:end]

        return ApiResponse(
            success=True,
            data={
                "data": [
                    bal.model_dump() if hasattr(bal, "model_dump") else bal
                    for bal in paginated_balances
                ],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(balance_list),
                    "total_pages": (len(balance_list) + per_page - 1) // per_page,
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

        balances = await sdk_client.get_balances()

        return ApiResponse(
            success=True,
            data=[bal.model_dump() if hasattr(bal, "model_dump") else bal for bal in balances],
        )
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


# Trading context endpoints
@app.post("/api/trading/context/broker")
async def set_trading_broker(request: TradingContextRequest):
    """Set trading context broker"""
    try:
        trading_context["broker"] = request.broker
        return ApiResponse(success=True, data=trading_context)
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.post("/api/trading/context/account")
async def set_trading_account(request: TradingContextRequest):
    """Set trading context account"""
    try:
        trading_context["account"] = request.account
        return ApiResponse(success=True, data=trading_context)
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


@app.get("/api/trading/context")
async def get_trading_context():
    """Get current trading context"""
    try:
        return ApiResponse(success=True, data=trading_context)
    except Exception as e:
        return ApiResponse(success=False, error=str(e))


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


if __name__ == "__main__":
    print("🚀 Starting Finatic Python Server SDK API...")
    print("   Port: 8002")
    print("   CORS enabled for: http://localhost:3000")
    print("   Make sure FINATIC_API_KEY is set in your environment")

    uvicorn.run("api_server:app", host="0.0.0.0", port=8002, reload=True, log_level="info")
