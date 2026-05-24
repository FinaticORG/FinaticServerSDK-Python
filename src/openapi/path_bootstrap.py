"""Ensure ``src/openapi`` is on ``sys.path`` so ``from finatic_server…`` imports resolve.

OpenAPI Generator emits absolute imports for ``packageName: finatic_server``. That package
lives under this directory; adding the directory to ``sys.path`` keeps imports working
for both ``src.*`` and direct test imports without vendoring the client elsewhere.
"""

from __future__ import annotations

import sys
from pathlib import Path

_openapi_root_directory = Path(__file__).resolve().parent
_openapi_root_path = str(_openapi_root_directory)
if _openapi_root_path not in sys.path:
    sys.path.insert(0, _openapi_root_path)
