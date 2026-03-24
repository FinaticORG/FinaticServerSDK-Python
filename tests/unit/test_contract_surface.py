"""Contract tests for stable, hand-authored SDK surfaces (not generated internals)."""

from __future__ import annotations

from pathlib import Path


def test_custom_finatic_server_preserves_subclass_marker() -> None:
    """Regen-safe: verifies protected custom class still declares the subclass marker."""
    root = Path(__file__).resolve().parents[2]
    custom_file = root / "src" / "custom" / "FinaticServer.py"
    assert custom_file.is_file(), f"Expected {custom_file}"
    body = custom_file.read_text(encoding="utf-8")
    assert "__CUSTOM_CLASS__" in body
