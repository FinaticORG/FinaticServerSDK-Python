# Finatic Server SDK (Python)

Python SDK for embedding Finatic in **your backend**. Keep the company API key on the server. Mint a 90-second one-time token for the browser Client SDK, or start a session and redirect to Connect.

## Install

```bash
pip install finatic-server-python
```

## Quick start

```python
import os
from finatic_server_python import FinaticServer

finatic = FinaticServer(
    api_key=os.environ["FINATIC_API_KEY"],
    sdk_config={"environment": "sandbox"},
)

# Client iframe: 90-second token. Never send the API key to the browser.
one_time_token = await finatic.v1.get_token()

# Redirect flow: start a session first (get_portal_url requires it).
session = await finatic.v1.start_session()
if not session.get("session_id"):
    raise RuntimeError(session.get("error") or "Session start failed")
portal_url = await finatic.v1.get_portal_url(mode="dark")

# After account.grant.created, start a session for that portal user, then read.
portal_user_id = "user-from-connect-onSuccess"
authed = await finatic.v1.start_session(user_id=portal_user_id)
accounts = await finatic.v1.list_accounts(include_sync_status=True)
if accounts.get("errors"):
    raise RuntimeError(accounts["errors"])
if not accounts.get("data"):
    raise RuntimeError("No granted accounts yet")
account_id = accounts["data"][0]["accountId"]
positions = await finatic.v1.list_positions(account_id)
```

Server `v1` data methods return `{ "traceId", "data", "warnings", "errors" }`. Check `errors` before using `data`.

Use `sdk_config={"environment": "sandbox"}` for Finatic synthetic data (`fntc_sandbox_` keys). Broker paper/sim accounts stay `live`.

`FinaticServer.init(...)` is a shortcut that calls `start_session`. Use the constructor + `get_token()` when you only need to hand a token to the browser.

## Embed Connect

Connect UI lives in **FinaticConnect**. This SDK does not open an iframe.

1. `v1.get_token()` → pass the token to `@finatic/client` `FinaticConnect.init(token)` in the browser (token TTL is 90 seconds).
2. Or `v1.start_session()` then `v1.get_portal_url(...)` → redirect. Treat the full URL as secret.

Wait for HTTPS webhook `account.grant.created` (or poll `list_accounts` on an ACTIVE session) before account-scoped reads.

## Trading

Fetch the broker schema, then send an idempotent command:

```python
schema = await finatic.v1.get_account_order_schema(account_id, "place")
created = await finatic.v1.create_account_order(
    account_id,
    {"symbol": "AAPL", "quantity": 1, "side": "BUY", "type": "MARKET"},
    idempotency_key="partner-order-123",
)
```

Python wraps the dict as `{"order": ...}` on the wire. `idempotency_key` is required.

## Package layout

| Name | Role |
|------|------|
| `finatic-server-python` | PyPI package |
| `finatic_server_python` | Public import |
| `src` | Hand-written `FinaticServer` and `v1.V1Client` |
| `finatic_server` | Generated OpenAPI transport — prefer `FinaticServer.v1` |

## Common commands

| Task | Command |
|------|---------|
| Test | `pytest` |
| Type check | `mypy` |

## Documentation

This README is the Python SDK contract. Fetch the rest before writing a full integration:

- Quick start: [https://finatic.dev/docs/quick-start/quick-start](https://finatic.dev/docs/quick-start/quick-start)
- Client SDK README: [https://github.com/FinaticORG/FinaticClientSDK/blob/develop/README.md](https://github.com/FinaticORG/FinaticClientSDK/blob/develop/README.md)
- Node SDK README: [https://github.com/FinaticORG/FinaticServerSDK-Node/blob/develop/README.md](https://github.com/FinaticORG/FinaticServerSDK-Node/blob/develop/README.md)
- Embed Connect: [https://github.com/FinaticORG/FinaticConnect/blob/develop/docs/embedding.md](https://github.com/FinaticORG/FinaticConnect/blob/develop/docs/embedding.md)
- Demo apps: [https://github.com/FinaticORG/FinaticDemoApps/blob/develop/README.md](https://github.com/FinaticORG/FinaticDemoApps/blob/develop/README.md)
- API reference: [https://finatic.dev/docs/api-reference](https://finatic.dev/docs/api-reference)
- OpenAPI: [https://finatic.dev/openapi.json](https://finatic.dev/openapi.json)
- Agent index: [https://finatic.dev/llms.txt](https://finatic.dev/llms.txt)
- Agent notes: [https://finatic.dev/AGENTS.md](https://finatic.dev/AGENTS.md)
