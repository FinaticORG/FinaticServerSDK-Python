"""Compatibility package for the generated OpenAPI client.

The generated client lives under ``src/openapi/finatic_server`` so the SDK can
keep generated code separate from hand-written wrappers. This shim preserves the
direct ``finatic_server`` import path without packaging the generated files
twice in the wheel.
"""

from __future__ import annotations

from pathlib import Path

_generated_package_directory = (
    Path(__file__).resolve().parent.parent / "src" / "openapi" / "finatic_server"
)
_generated_package_path = str(_generated_package_directory)
_package_search_path = globals().setdefault("__path__", [])

if _generated_package_path not in _package_search_path:
    _package_search_path.append(_generated_package_path)

_generated_init_file = _generated_package_directory / "__init__.py"
exec(
    compile(
        _generated_init_file.read_text(encoding="utf-8"),
        str(_generated_init_file),
        "exec",
    ),
    globals(),
)
