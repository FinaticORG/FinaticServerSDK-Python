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

The committed v1 artifact comes from FinaticAPI PR #748 at
`54eb17ac130af907f95318c1833ff8f6fb915712` and has SHA-256
`5c450a4e43aaad1e0f30d0bf0705183b0b882c86308ff78d9ff05cf2bde8054f`.
`artifacts/openapi/finaticapi-v1.provenance.json` is the machine-checked source
record.

The generated asyncio client uses OpenAPI Generator `7.18.0`, pinned in
`openapitools.json`. Regeneration is deliberately limited to the Accounts API,
its transitive generated model graph, the public FDX models, and the generated
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
commit the generated diff. The hand-authored public facade and aliases live in
`src/v1.py`, `src/types.py`, and `src/finatic_fdx_types.py`.
