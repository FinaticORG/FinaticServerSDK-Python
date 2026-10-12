from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import tarfile
import zipfile
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


def _configure_surface_guard(
    generator, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, artifact: dict
) -> tuple[Path, Path]:
    artifact_path = tmp_path / "artifact.json"
    artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
    generated_root = tmp_path / "src" / "openapi"
    generated_root.mkdir(parents=True)
    manifest = tmp_path / "openapi-generated-tree-manifest.json"
    manifest.write_text('{"files": []}', encoding="utf-8")
    shipped_root = tmp_path / "public-package"
    shipped_root.mkdir()
    monkeypatch.setattr(generator, "ARTIFACT", artifact_path)
    monkeypatch.setattr(generator, "GENERATED_ROOT", generated_root)
    monkeypatch.setattr(generator, "COMPLETE_MANIFEST", manifest)
    monkeypatch.setattr(generator, "SHIPPED_PACKAGE_ROOTS", (shipped_root,))
    return generated_root, shipped_root


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


@pytest.mark.parametrize(
    "forbidden_path",
    ["/api/v1/session/mcp/bootstrap", "/api/v1/session/mcp/link-user"],
)
def test_public_surface_guard_rejects_mcp_path_family(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    forbidden_path: str,
) -> None:
    generator = _load_generator()
    _configure_surface_guard(
        generator,
        tmp_path,
        monkeypatch,
        {"paths": {forbidden_path: {"post": {}}}, "components": {"schemas": {}}},
    )

    with pytest.raises(RuntimeError, match="MCP bootstrap/link surface"):
        generator.verify_no_forbidden_mcp_public_surface()


def test_public_surface_guard_rejects_forbidden_operation_id(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generator = _load_generator()
    _configure_surface_guard(
        generator,
        tmp_path,
        monkeypatch,
        {
            "paths": {
                "/api/v1/example": {"post": {"operationId": "link_user_to_mcp_session"}}
            },
            "components": {"schemas": {}},
        },
    )

    with pytest.raises(RuntimeError, match="operationId"):
        generator.verify_no_forbidden_mcp_public_surface()


def test_public_surface_guard_rejects_generated_module(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generator = _load_generator()
    generated_root, _ = _configure_surface_guard(
        generator,
        tmp_path,
        monkeypatch,
        {"paths": {}, "components": {"schemas": {}}},
    )
    module = generated_root / "finatic_server/models/mcp_bootstrap_request.py"
    module.parent.mkdir(parents=True)
    module.write_text("class MCPBootstrapRequest: pass\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="mcp_bootstrap_request"):
        generator.verify_no_forbidden_mcp_public_surface()


def test_public_surface_guard_rejects_complete_manifest_entry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generator = _load_generator()
    _configure_surface_guard(
        generator,
        tmp_path,
        monkeypatch,
        {"paths": {}, "components": {"schemas": {}}},
    )
    generator.COMPLETE_MANIFEST.write_text(
        json.dumps(
            {"files": [{"path": "finatic_server/models/link_user_to_mcp_session.py"}]}
        ),
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="openapi-generated-tree-manifest"):
        generator.verify_no_forbidden_mcp_public_surface()


def test_public_surface_guard_rejects_public_import_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    generator = _load_generator()
    _, shipped_root = _configure_surface_guard(
        generator,
        tmp_path,
        monkeypatch,
        {"paths": {}, "components": {"schemas": {}}},
    )
    public_import = shipped_root / "__init__.py"
    public_import.write_text(
        "from finatic_server.models.mcp_bootstrap_request import MCPBootstrapRequest\n",
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="public-package"):
        generator.verify_no_forbidden_mcp_public_surface()


@pytest.mark.parametrize("archive_kind", ["wheel", "sdist"])
def test_distribution_guard_rejects_forbidden_archive_member(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    archive_kind: str,
) -> None:
    generator = _load_generator()
    monkeypatch.setattr(generator, "DISTRIBUTION_ROOT", tmp_path)
    member_name = "finatic_server/models/link_user_to_mcp_session.py"
    content = b"class LinkUserToMCPSessionRequest: pass\n"
    if archive_kind == "wheel":
        archive = tmp_path / "package.whl"
        with zipfile.ZipFile(archive, "w") as package:
            package.writestr(member_name, content)
    else:
        archive = tmp_path / "package.tar.gz"
        with tarfile.open(archive, "w:gz") as package:
            info = tarfile.TarInfo(member_name)
            info.size = len(content)
            package.addfile(info, io.BytesIO(content))

    with pytest.raises(RuntimeError, match="built distributions"):
        generator.verify_built_distributions()
