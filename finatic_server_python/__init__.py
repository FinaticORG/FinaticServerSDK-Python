"""Public import path for the Finatic Server Python SDK.

Install: ``pip install finatic-server-python``

Import::

    from finatic_server_python import FinaticServer

    finatic = FinaticServer(
        api_key="fntc_sandbox_your_key",
        sdk_config={"environment": "sandbox"},
    )
    token = await finatic.v1.get_token()  # 90 seconds; send to the browser only

Package layout:

- ``finatic_server_python`` — stable public import name (this shim re-exports ``src``).
- ``src`` — hand-written SDK: ``FinaticServer``, ``FinaticServerCore``, ``v1.V1Client``.
- ``finatic_server`` — generated OpenAPI transport client (``src/openapi/finatic_server``).
  Prefer ``FinaticServer.v1``.

Portal auth UX runs in **FinaticConnect**. This SDK mints one-time tokens and portal URLs
and exposes post-grant account, order, grant, and webhook APIs.
"""

from __future__ import annotations

import sys
from pathlib import Path

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src import *  # noqa: F403, F401
