# FinaticServerSDK-Python Architecture and Runtime

## Package Role

`FinaticServerSDK-Python` provides server-side Python integration with API-key/session flows and broker-domain operations.

## Internal Structure

- **Public entrypoints**: `src/__init__.py`, `src/FinaticServer.py`
- **Core runtime**: `src/FinaticServerCore.py`
- **Generated API client**: `src/openapi/finatic_server`
- **Domain wrappers**: `src/wrappers`
- **Cross-cutting utilities**: `src/utils`

## Runtime Flow (High Level)

1. SDK initializes with API key and runtime config.
2. Session and token methods establish API call context.
3. Wrapper methods perform domain operations via generated clients.
4. Utility layers handle retries, validation, and response normalization.

## Operational Boundaries

- Browser-focused portal UX ownership is outside this package.
- Backend service authority remains in `finaticAPI`.

## OpenAPI provenance

The committed v1 artifact comes from FinaticAPI PR #972 at
`f314d21c12fe903a67b56bb4fb973c3f6ceca189` and has SHA-256
`3e214865c34bfdf7735561fe8a4d0989feeba664901f59b7525614e601d11470`.
`artifacts/openapi/finaticapi-v1.provenance.json` is the machine-checked source
record. The exact artifact also contains `/api/v1/account-grants/batch-revoke`;
that destructive operation remains outside the hand-written Python facade in
this grouped-webhook change. Its omission is explicitly inventoried in the
facade coverage test, rather than mutating the pinned artifact.

The generated asyncio client uses OpenAPI Generator `7.18.0`, pinned in
`openapitools.json`. Regeneration is deliberately limited to the Accounts API,
its transitive generated model graph, the public FDX models (including grouped
webhook subscription/payload models), and the generated
runtime support files. This prevents unrelated broker/Core/MCP/telemetry
surfaces from entering the packaged client.

```bash
uv run python scripts/regenerate_openapi.py --write
uv run python scripts/regenerate_openapi.py
```

The wrapper always generates into a clean temporary directory, verifies the
pinned artifact checksum and generator version, derives the selected model
dependency graph, checks its committed file manifest, and byte-compares the
curated output after deterministic whitespace normalization. CI runs the
check-only form. Generated files are not edited by hand; rerun `--write` and
commit the generated diff.

`scripts/openapi-generated-tree-manifest.json` also inventories every shipped
file under `src/openapi/finatic_server`. Files reproduced by the current
artifact are classified as `current_artifact`; retained legacy surfaces are
classified against the explicit `origin/develop@4451280...` snapshot and
SHA-256 pinned. The check fails for an added, removed, or edited file in either
class, so no generated package surface sits outside provenance enforcement.
Only an intentional provenance migration should run
`scripts/regenerate_openapi.py --write-complete-manifest`.

The public v1 facade intentionally returns ordinary dictionaries. Static
mapping types in `src/finatic_fdx_typed_dicts.py` are generated directly from
the same pinned artifact by `scripts/generate_fdx_typeddicts.py`; the OpenAPI
check verifies that output too. Generated Pydantic classes remain available
for explicit construction and validation, but the raw facade does not claim to
return those model instances. The hand-authored public facade and aliases live
in `src/v1.py`, `src/types.py`, and `src/finatic_fdx_types.py`.
