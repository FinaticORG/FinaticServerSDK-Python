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


def _manifest(
    path: Path, content: bytes, *, legacy_provenance: str
) -> dict[str, object]:
    return {
        "version": 1,
        "current_artifact": {},
        "legacy_snapshot": legacy_provenance,
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
        json.dumps(
            _manifest(
                legacy.relative_to(generated_root),
                original,
                legacy_provenance=generator.LEGACY_PROVENANCE,
            )
        ),
        encoding="utf-8",
    )
    provenance = tmp_path / "provenance.json"
    provenance.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(generator, "GENERATED_ROOT", generated_root)
    monkeypatch.setattr(generator, "COMPLETE_MANIFEST", manifest)
    monkeypatch.setattr(generator, "PROVENANCE", provenance)
    monkeypatch.setattr(
        generator,
        "legacy_snapshot_content",
        lambda relative: (
            original if relative == legacy.relative_to(generated_root) else None
        ),
    )

    assert generator.verify_complete_manifest(set())

    if mutation == "edit":
        legacy.write_text("legacy = False\n", encoding="utf-8")
    elif mutation == "add":
        (legacy.parent / "unexpected.py").write_text("value = 1\n", encoding="utf-8")
    else:
        legacy.unlink()

    assert not generator.verify_complete_manifest(set())


def test_complete_manifest_rejects_new_file_mislabeled_as_legacy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generator = _load_generator()
    generated_root = tmp_path / "src" / "openapi"
    generated = generated_root / "finatic_server" / "models" / "new_model.py"
    generated.parent.mkdir(parents=True)
    generated_content = b"new_model = True\n"
    generated.write_bytes(generated_content)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            _manifest(
                generated.relative_to(generated_root),
                generated_content,
                legacy_provenance=generator.LEGACY_PROVENANCE,
            )
        ),
        encoding="utf-8",
    )
    provenance = tmp_path / "provenance.json"
    provenance.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(generator, "GENERATED_ROOT", generated_root)
    monkeypatch.setattr(generator, "COMPLETE_MANIFEST", manifest)
    monkeypatch.setattr(generator, "PROVENANCE", provenance)
    monkeypatch.setattr(generator, "legacy_snapshot_content", lambda relative: None)

    assert not generator.verify_complete_manifest(set())
