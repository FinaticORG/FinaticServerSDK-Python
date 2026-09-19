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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="replace managed files")
    mode.add_argument(
        "--print-manifest",
        action="store_true",
        help="print the generated transitive file manifest",
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
            expected = manifest_files()
            if not verify_manifest(actual, expected):
                return 1
            if not synchronize(output, actual, args.write):
                return 1
    except (KeyError, OSError, RuntimeError, ValueError) as error:
        print(f"OpenAPI generation check failed: {error}", file=sys.stderr)
        return 1
    print("OpenAPI generated account surface is reproducible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
