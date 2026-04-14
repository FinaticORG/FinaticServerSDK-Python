# FinaticServerSDK-Python Architecture and Runtime

## Package Role

`FinaticServerSDK-Python` provides server-side Python integration with API-key/session flows and broker-domain operations.

## Internal Structure

- **Public entrypoints**: `src/__init__.py`, `src/FinaticServer.py`
- **Core runtime**: `src/FinaticServerCore.py`
- **Generated API client**: `src/openapi/generated`
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
