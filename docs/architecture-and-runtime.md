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
`a7e80ac708d34f20cb241b8152b3c672674022b5` and has SHA-256
`5c450a4e43aaad1e0f30d0bf0705183b0b882c86308ff78d9ff05cf2bde8054f`.
`artifacts/openapi/finaticapi-v1.provenance.json` is the machine-checked source
record.

The generated asyncio client uses OpenAPI Generator `7.18.0`, pinned in
`openapitools.json`. The generation command is:

```bash
npx --yes @openapitools/openapi-generator-cli generate -g python -i artifacts/openapi/finaticapi-v1.json -o src/openapi --library asyncio --additional-properties=packageName=finatic_server,projectName=finatic-server-python,packageVersion=0.1.0,generateSourceCodeOnly=true --global-property=apiDocs=false,modelDocs=false,apiTests=false,modelTests=false --ignore-file-override src/openapi/.openapi-generator-ignore
```

Generated models are not edited by hand. The hand-authored public facade and
aliases live in `src/v1.py`, `src/types.py`, and `src/finatic_fdx_types.py`.
