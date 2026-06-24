# Finatic Server SDK (Python)

Python SDK for server-side Finatic integrations.

Use this package to authenticate with Finatic from Python services, generate client tokens, and retrieve standardized broker-domain data.

## Version lines (FDX v1)

| Version | API surface | Use when |
|---------|-------------|----------|
| **1.0.0** | `/api/v1/*` via `FinaticServer.v1` | New account-grant integrations |
| **0.9.x** | `/api/beta/*` via legacy wrappers | Existing apps until migrated |

Legacy beta clients live under `src/openapi-legacy/` (`finatic_server_legacy`); v1 output is under `src/openapi/` (`finatic_server`).

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

## Package layout

| Name | Role |
|------|------|
| `finatic-server-python` | PyPI package (`pip install finatic-server-python`) |
| `finatic_server_python` | Public import path (`from finatic_server_python import FinaticServer`) |
| `src` | Hand-written SDK (`FinaticServer`, `v1.V1Client`) |
| `finatic_server` | Generated OpenAPI transport client (`src/openapi/finatic_server`) |

Portal connect flows (institutions, auth-attempts, discovered accounts, grant UI)
run in **FinaticConnect**, not the server SDK. The server SDK exposes session
management, `portal-links` creation, and post-consent account/grant/webhook APIs.

## Account-First v1 Preview

The v1 facade targets the SDK OpenAPI contract (`spec-sdk.yaml`) and sends
`X-Finatic-Environment` on every request.

```python
from finatic_server_python import FinaticServer

finatic = FinaticServer(
    api_key="fntc_live_your_key",
    sdk_config={"environment": "live"},
)

session = await finatic.v1.create_session()
portal_link = await finatic.v1.create_portal_link()
# Open portal_link URL in FinaticConnect for user auth + grant consent

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
