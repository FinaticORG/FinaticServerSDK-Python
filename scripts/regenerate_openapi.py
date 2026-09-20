#!/usr/bin/env python3
"""Regenerate and verify the curated account OpenAPI client surface."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/openapi/finaticapi-v1.json"
PROVENANCE = ROOT / "artifacts/openapi/finaticapi-v1.provenance.json"
MANIFEST = ROOT / "scripts/openapi-account-manifest.txt"
COMPLETE_MANIFEST = ROOT / "scripts/openapi-generated-tree-manifest.json"
GENERATED_ROOT = ROOT / "src/openapi"
PACKAGE_ROOT = Path("finatic_server")
GENERATOR_VERSION = "7.18.0"

IMPORT_RE = re.compile(
    r"^from finatic_server(?:(\.models|\.api))?\.([a-z0-9_]+) import ",
    re.MULTILINE,
)
PUBLIC_MODEL_RE = re.compile(
    r"^from finatic_server\.models\.([a-z0-9_]+) import ", re.MULTILINE
)

SUPPORTING_FILES = {
    PACKAGE_ROOT / "api_client.py",
    PACKAGE_ROOT / "api_response.py",
    PACKAGE_ROOT / "configuration.py",
    PACKAGE_ROOT / "exceptions.py",
    PACKAGE_ROOT / "rest.py",
}

# These schemas are not reachable from the curated Accounts/public FDX import
# closure, but retained legacy generated models import them.  Keep them pinned
# to and byte-compared with the current artifact instead of misclassifying new
# files as part of the legacy snapshot.
CURRENT_ARTIFACT_COMPATIBILITY_FILES = {
    PACKAGE_ROOT / "models/broker_data_option_type_enum.py",
    PACKAGE_ROOT / "models/broker_data_order_side_enum.py",
    PACKAGE_ROOT / "models/broker_data_order_status_enum.py",
}

LEGACY_PROVENANCE = "origin/develop@4451280121ebd9e29d0bd88e1adeadfad509a8d4"
LEGACY_REVISION = "4451280121ebd9e29d0bd88e1adeadfad509a8d4"


def normalize_generated(content: bytes) -> bytes:
    """Apply the repository's deterministic whitespace curation."""
    text = content.decode("utf-8")
    lines = [line.rstrip(" \t") for line in text.splitlines()]
    return ("\n".join(lines).rstrip("\n") + "\n").encode("utf-8")


def verify_inputs() -> None:
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    artifact_hash = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()
    if artifact_hash != provenance["sha256"]:
        raise RuntimeError(
            "OpenAPI artifact does not match its pinned provenance: "
            f"expected {provenance['sha256']}, got {artifact_hash}"
        )

    tools = json.loads((ROOT / "openapitools.json").read_text(encoding="utf-8"))
    actual_version = tools["generator-cli"]["version"]
    if actual_version != GENERATOR_VERSION:
        raise RuntimeError(
            f"expected OpenAPI Generator {GENERATOR_VERSION}, got {actual_version}"
        )


def generate_clean(output: Path) -> None:
    command = [
        "npx",
        "--yes",
        "@openapitools/openapi-generator-cli",
        "generate",
        "-g",
        "python",
        "-i",
        str(ARTIFACT.relative_to(ROOT)),
        "-o",
        str(output),
        "--library",
        "asyncio",
        "--additional-properties",
        (
            "packageName=finatic_server,projectName=finatic-server-python,"
            "packageVersion=0.1.0,generateSourceCodeOnly=true"
        ),
        "--global-property",
        (
            "apis=accounts,models,supportingFiles,apiDocs=false,modelDocs=false,"
            "apiTests=false,modelTests=false"
        ),
    ]
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        details = "\n".join((result.stdout + result.stderr).splitlines()[-80:])
        raise RuntimeError(f"OpenAPI generation failed:\n{details}")


def import_path(group: str | None, module: str) -> Path:
    if group == ".models":
        return PACKAGE_ROOT / "models" / f"{module}.py"
    if group == ".api":
        return PACKAGE_ROOT / "api" / f"{module}.py"
    return PACKAGE_ROOT / f"{module}.py"


def managed_files(output: Path) -> set[Path]:
    public_types = (ROOT / "src/finatic_fdx_types.py").read_text(encoding="utf-8")
    seeds = {
        PACKAGE_ROOT / "api/accounts_api.py",
        *SUPPORTING_FILES,
        *CURRENT_ARTIFACT_COMPATIBILITY_FILES,
        *(
            PACKAGE_ROOT / "models" / f"{module}.py"
            for module in PUBLIC_MODEL_RE.findall(public_types)
        ),
    }

    managed: set[Path] = set()
    queue = deque(sorted(seeds))
    while queue:
        relative = queue.popleft()
        if relative in managed:
            continue
        source = output / relative
        if not source.is_file():
            raise RuntimeError(f"generator did not emit required file: {relative}")
        managed.add(relative)
        content = source.read_text(encoding="utf-8")
        for group, module in IMPORT_RE.findall(content):
            dependency = import_path(group or None, module)
            if dependency not in managed:
                queue.append(dependency)
    return managed


def manifest_files() -> set[Path]:
    return {
        Path(line.strip()).relative_to("src/openapi")
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def show_manifest(files: set[Path]) -> None:
    for relative in sorted(files):
        print((Path("src/openapi") / relative).as_posix())


def verify_manifest(actual: set[Path], expected: set[Path]) -> bool:
    if actual == expected:
        return True
    print("Curated generated file manifest is stale.", file=sys.stderr)
    for missing in sorted(actual - expected):
        print(f"  add: src/openapi/{missing}", file=sys.stderr)
    for extra in sorted(expected - actual):
        print(f"  remove: src/openapi/{extra}", file=sys.stderr)
    return False


def synchronize(output: Path, files: set[Path], write: bool) -> bool:
    clean = True
    for relative in sorted(files):
        generated = normalize_generated((output / relative).read_bytes())
        committed_path = GENERATED_ROOT / relative
        committed = committed_path.read_bytes() if committed_path.exists() else b""
        if committed == generated:
            continue
        clean = False
        if write:
            committed_path.parent.mkdir(parents=True, exist_ok=True)
            committed_path.write_bytes(generated)
            print(f"updated {committed_path.relative_to(ROOT)}")
            continue
        print(f"generated drift: {committed_path.relative_to(ROOT)}", file=sys.stderr)
        before = committed.decode("utf-8", errors="replace").splitlines()
        after = generated.decode("utf-8", errors="replace").splitlines()
        for line in list(
            difflib.unified_diff(
                before, after, fromfile="committed", tofile="generated"
            )
        )[:40]:
            print(line, file=sys.stderr)
    return clean or write


def committed_generated_files() -> set[Path]:
    package = GENERATED_ROOT / PACKAGE_ROOT
    return {
        path.relative_to(GENERATED_ROOT)
        for path in package.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    }


def legacy_snapshot_content(relative: Path) -> bytes | None:
    """Read a generated file from the pinned legacy Git tree, if it exists."""
    repository_path = (Path("src/openapi") / relative).as_posix()
    result = subprocess.run(
        ["git", "show", f"{LEGACY_REVISION}:{repository_path}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout
    return None


def write_complete_manifest(current_files: set[Path]) -> None:
    files = []
    for relative in sorted(committed_generated_files()):
        content = (GENERATED_ROOT / relative).read_bytes()
        provenance = "current_artifact"
        if relative not in current_files:
            legacy_content = legacy_snapshot_content(relative)
            if legacy_content is None:
                raise RuntimeError(
                    "generated file is neither current-artifact managed nor present "
                    f"in {LEGACY_PROVENANCE}: src/openapi/{relative}"
                )
            if content != legacy_content:
                raise RuntimeError(
                    "legacy generated file differs from its pinned snapshot: "
                    f"src/openapi/{relative}"
                )
            provenance = "legacy_snapshot"
        files.append(
            {
                "path": relative.as_posix(),
                "provenance": provenance,
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    payload = {
        "version": 1,
        "current_artifact": json.loads(PROVENANCE.read_text(encoding="utf-8")),
        "legacy_snapshot": LEGACY_PROVENANCE,
        "files": files,
    }
    COMPLETE_MANIFEST.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"updated {COMPLETE_MANIFEST.relative_to(ROOT)}")


def verify_complete_manifest(current_files: set[Path]) -> bool:
    payload = json.loads(COMPLETE_MANIFEST.read_text(encoding="utf-8"))
    entries = {Path(item["path"]): item for item in payload["files"]}
    committed = committed_generated_files()
    clean = True
    if payload.get("legacy_snapshot") != LEGACY_PROVENANCE:
        clean = False
        print("Complete manifest legacy provenance is stale.", file=sys.stderr)
    if payload.get("current_artifact") != json.loads(
        PROVENANCE.read_text(encoding="utf-8")
    ):
        clean = False
        print("Complete manifest current-artifact provenance is stale.", file=sys.stderr)
    if committed != set(entries):
        clean = False
        print("Complete generated-tree file manifest is stale.", file=sys.stderr)
        for missing in sorted(committed - set(entries)):
            print(f"  add: src/openapi/{missing}", file=sys.stderr)
        for extra in sorted(set(entries) - committed):
            print(f"  remove: src/openapi/{extra}", file=sys.stderr)
    manifest_current = {
        path
        for path, item in entries.items()
        if item["provenance"] == "current_artifact"
    }
    if manifest_current != current_files:
        clean = False
        print(
            "Complete manifest current-artifact classification is stale.",
            file=sys.stderr,
        )
    unknown_provenance = {
        path
        for path, item in entries.items()
        if item.get("provenance") not in {"current_artifact", "legacy_snapshot"}
    }
    for relative in sorted(unknown_provenance):
        clean = False
        print(
            f"unknown generated provenance: src/openapi/{relative}", file=sys.stderr
        )
    for relative in sorted(committed & set(entries)):
        digest = hashlib.sha256((GENERATED_ROOT / relative).read_bytes()).hexdigest()
        if digest != entries[relative]["sha256"]:
            clean = False
            print(f"generated tree drift: src/openapi/{relative}", file=sys.stderr)
        if entries[relative].get("provenance") != "legacy_snapshot":
            continue
        legacy_content = legacy_snapshot_content(relative)
        if legacy_content is None:
            clean = False
            print(
                "legacy provenance path missing from pinned snapshot: "
                f"src/openapi/{relative}",
                file=sys.stderr,
            )
            continue
        legacy_digest = hashlib.sha256(legacy_content).hexdigest()
        if legacy_digest != entries[relative]["sha256"]:
            clean = False
            print(
                "legacy provenance digest mismatch: "
                f"src/openapi/{relative}",
                file=sys.stderr,
            )
    return clean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="replace managed files")
    mode.add_argument(
        "--print-manifest",
        action="store_true",
        help="print the generated transitive file manifest",
    )
    mode.add_argument(
        "--write-complete-manifest",
        action="store_true",
        help="record checksums and provenance for the complete committed generated tree",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        verify_inputs()
        with tempfile.TemporaryDirectory(prefix="finatic-openapi-") as temporary:
            output = Path(temporary)
            generate_clean(output)
            actual = managed_files(output)
            if args.print_manifest:
                show_manifest(actual)
                return 0
            if args.write_complete_manifest:
                write_complete_manifest(actual)
                return 0
            expected = manifest_files()
            if not verify_manifest(actual, expected):
                return 1
            if not synchronize(output, actual, args.write):
                return 1
            if not verify_complete_manifest(actual):
                return 1
            typed_dict_check = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/generate_fdx_typeddicts.py"),
                    "--check",
                ],
                cwd=ROOT,
                check=False,
            )
            if typed_dict_check.returncode != 0:
                return 1
    except (KeyError, OSError, RuntimeError, ValueError) as error:
        print(f"OpenAPI generation check failed: {error}", file=sys.stderr)
        return 1
    print("OpenAPI generated account surface is reproducible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
