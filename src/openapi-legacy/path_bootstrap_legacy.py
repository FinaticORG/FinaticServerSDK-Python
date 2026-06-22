"""Ensure ``src/openapi-legacy`` is on ``sys.path`` for ``finatic_server_legacy`` imports."""

from __future__ import annotations

import sys
from pathlib import Path

_openapi_legacy_root_directory = Path(__file__).resolve().parent.parent / "openapi-legacy"
_openapi_legacy_root_path = str(_openapi_legacy_root_directory)
if _openapi_legacy_root_path not in sys.path:
    sys.path.insert(0, _openapi_legacy_root_path)
