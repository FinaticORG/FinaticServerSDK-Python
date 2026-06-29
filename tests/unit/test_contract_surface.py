"""Contract tests for stable, hand-authored SDK surfaces (not generated internals)."""

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


def test_finatic_server_root_is_bootstrap_only() -> None:
    """Root exposes bootstrap lifecycle; session state lives on finatic.v1."""
    from finatic_server_python import FinaticServer

    sdk = FinaticServer(api_key="test-api-key")
    assert hasattr(sdk, "v1")
    assert hasattr(sdk, "close")
    assert not hasattr(sdk, "get_session_id")
    assert hasattr(sdk.v1, "get_session_id")
    assert inspect.iscoroutinefunction(sdk.v1.start_session)
    assert hasattr(sdk.v1, "list_accounts")
    assert inspect.iscoroutinefunction(sdk.v1.list_accounts)
    assert hasattr(sdk.v1, "list_balances")
    assert hasattr(sdk.v1, "list_positions")
