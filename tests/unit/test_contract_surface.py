"""Contract tests for stable, hand-authored SDK surfaces (not generated internals).

See docs/sdk-public-api-inventory.md at the Finatic workspace root.
"""

from __future__ import annotations

import inspect
from pathlib import Path


def test_custom_finatic_server_preserves_subclass_marker() -> None:
    """Regen-safe: verifies hand-authored FinaticServer keeps subclass marker."""
    root = Path(__file__).resolve().parents[2]
    source_file = root / "src" / "FinaticServer.py"
    assert source_file.is_file(), f"Expected {source_file}"
    body = source_file.read_text(encoding="utf-8")
    assert "__CUSTOM_CLASS__" in body


def test_finatic_server_public_entrypoint() -> None:
    """Stable import path for the server SDK."""
    from finatic_server_python import FinaticServer

    assert FinaticServer is not None
    assert hasattr(FinaticServer, "init")
    assert inspect.iscoroutinefunction(FinaticServer.init)


def test_finatic_server_stable_instance_api_subset() -> None:
    """Minimal stable API on FinaticServer (expand inventory when adding contracts)."""
    from finatic_server_python import FinaticServer

    assert hasattr(FinaticServer, "start_session")
    assert inspect.iscoroutinefunction(FinaticServer.start_session)
    assert hasattr(FinaticServer, "get_session_id")
