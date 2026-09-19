from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


def _load_generator():
    script = Path(__file__).resolve().parents[2] / "scripts" / "regenerate_openapi.py"
    spec = importlib.util.spec_from_file_location("regenerate_openapi", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _manifest(path: Path, content: bytes) -> dict[str, object]:
    return {
        "version": 1,
        "files": [
            {
                "path": path.as_posix(),
                "provenance": "legacy_snapshot",
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        ],
    }


@pytest.mark.parametrize("mutation", ["edit", "add", "remove"])
def test_complete_generated_tree_manifest_rejects_unmanaged_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    generator = _load_generator()
    generated_root = tmp_path / "src" / "openapi"
    legacy = generated_root / "finatic_server" / "models" / "legacy.py"
    legacy.parent.mkdir(parents=True)
    original = b"legacy = True\n"
    legacy.write_bytes(original)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(_manifest(legacy.relative_to(generated_root), original)),
        encoding="utf-8",
    )
    monkeypatch.setattr(generator, "GENERATED_ROOT", generated_root)
    monkeypatch.setattr(generator, "COMPLETE_MANIFEST", manifest)

    if mutation == "edit":
        legacy.write_text("legacy = False\n", encoding="utf-8")
    elif mutation == "add":
        (legacy.parent / "unexpected.py").write_text("value = 1\n", encoding="utf-8")
    else:
        legacy.unlink()

    assert not generator.verify_complete_manifest(set())
