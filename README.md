# Finatic Server SDK (Python)

Python SDK for server-side Finatic integrations.

Use this package to authenticate with Finatic from Python services, generate client tokens, and retrieve standardized broker-domain data.

## Install

```bash
pip install finatic-server-python
```

## Quick Start

```python
from finatic_server_python import FinaticServer

finatic = await FinaticServer.init(api_key="your-api-key")
token = await finatic.get_token()
positions = await finatic.get_all_positions()
```

## Account-First v1 Preview

The v1 facade targets the account-first FinaticAPI contract and sends
`X-Finatic-Environment` on every request.

```python
from finatic_server_python import FinaticServer

finatic = FinaticServer(
    api_key="fntc_live_your_key",
    sdk_config={"environment": "live"},
)

session = await finatic.v1.create_session()
await finatic.v1.link_portal_user("user-id")
institutions = await finatic.v1.list_portal_institutions()
auth_attempt = await finatic.v1.create_portal_auth_attempt("alpaca")
discovered = await finatic.v1.list_discovered_accounts(
    auth_attempt_id=auth_attempt["data"]["id"],
    include_sync_status=True,
)
grant = await finatic.v1.create_portal_account_grant(
    {
        "accountId": "broker-account-id",
        "authAttemptId": auth_attempt["data"]["id"],
        "canRead": True,
        "canTrade": False,
        "dataClusters": ["accounts", "balances"],
    }
)
accounts = await finatic.v1.list_accounts()
orders = await finatic.v1.list_account_orders("broker-account-id")
created = await finatic.v1.create_account_order(
    "broker-account-id",
    {"symbol": "AAPL", "quantity": 1, "side": "BUY", "type": "MARKET"},
    idempotency_key="partner-order-123",
)
```

Use `sdk_config={"environment": "sandbox"}` for Finatic synthetic sandbox data.
Broker paper or simulated accounts remain `live` environment accounts.

### OpenAPI Contract Artifact

The v1 facade is validated against `artifacts/openapi/finaticapi-v1.json`, which
is exported from the FinaticAPI account-first branch. Refresh it with:

```bash
env PYTHONPATH=/home/claw/.openclaw/workspace/worktrees/FinaticAPI-pr174-openapi/src:/home/claw/.openclaw/workspace/worktrees/FinaticCore-pr171-openapi/src /home/claw/.openclaw/workspace/repos/FinaticAPI/.venv/bin/python /home/claw/.openclaw/workspace/worktrees/FinaticAPI-pr174-openapi/scripts/export_openapi.py --output /home/claw/.openclaw/workspace/repos/FinaticServerSDK-Python/artifacts/openapi/finaticapi-v1.json
```

PR #25 currently uses FinaticAPI PR #174 head `4ca17320` and finaticCore PR
#171 head `0a126bed` as branch-ready dependency inputs. The package version is
prepared as `1.0.0` for the API v1 semver lane, but the coordinated FDX
account-consent operator hold still controls merge and release timing.

## Common Commands

| Task | Command |
|---|---|
| Install in editable mode | `uv pip install -e .` |
| Run tests | `pytest` |
| Build package | `python -m build` |
| Lint | `ruff check .` |
| Format | `ruff format .` |

## Core Capabilities

- API-key initialization and session management.
- Portal URL generation for end-user authentication.
- One-time token generation for client SDK sessions.
- Typed access to orders, positions, accounts, and balances.
- Consistent response/error structures across endpoints.

## Documentation

- Product docs: [https://finatic.dev/docs](https://finatic.dev/docs)
- API reference: [https://finatic.dev/docs/api-reference](https://finatic.dev/docs/api-reference)
- LLM context doc: [https://finatic.dev/llms.txt](https://finatic.dev/llms.txt)

## Using Finatic with AI

Use this SDK in Python AI/data systems to:

- query balances, positions, and orders across connected brokers
- normalize broker interactions behind one SDK surface
- feed structured brokerage data into analytics or model workflows

MCP support is coming soon.
