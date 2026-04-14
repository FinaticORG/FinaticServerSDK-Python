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
