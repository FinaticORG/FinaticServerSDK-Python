"""Public import path for the Finatic Server Python SDK.

Install: ``pip install finatic-server-python``

Import::

    from finatic_server_python import FinaticServer

    finatic = FinaticServer(api_key="...")
    await finatic.v1.create_session()
    await finatic.v1.create_portal_link()

Package layout:

- ``finatic_server_python`` — stable public import name (this shim re-exports ``src``).
- ``src`` — hand-written SDK: ``FinaticServer``, ``FinaticServerCore``, ``v1.V1Client``.
- ``finatic_server`` — generated OpenAPI transport client (``src/openapi/finatic_server``).
  Use ``finatic_server`` only for low-level generated APIs; prefer ``FinaticServer.v1``.

Portal auth flows (institutions, auth-attempts, discovered accounts, grant consent UI)
run in **FinaticConnect**, not the server SDK. The server SDK exposes session +
``portal-links`` creation and post-consent account/grant/webhook APIs.
"""

from __future__ import annotations

import sys
from pathlib import Path

parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src import *  # noqa: F403, F401
