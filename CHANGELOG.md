# Changelog

## Unreleased

- Regenerate the account-resource client from FinaticAPI PR #748 and expose
  typed instrument descriptors for orders, fills, events, positions, lots, and
  lot fills.
- Add typed canonical `finaticInstrumentId` placement while preserving the
  provider-native `instrumentId`, arbitrary provider fields, raw dictionaries,
  account scoping, and idempotency behavior.

## 1.0.4

- Release from 1f12f4e6b4f0eba77d315913d338d90aef8adfd9.

## 1.0.3

- Release sync after PyPI publish.

## 1.0.2

- Release from 6e6639c3189421d195165575ba08f571817f6c6c.

## 1.0.1

- Release from 9d9cd9ca5ab93037a171a1131f288806885a093e.

## 1.0.0

- Align the Python server SDK release lane with the FinaticAPI account-first v1
  contract.
- Add the account-first v1 facade, environment header support, and route
  coverage validation against `artifacts/openapi/finaticapi-v1.json`.
- Remove generated beta broker/company clients, connection-first models, and
  inactive position-lot types from the 1.0 SDK source.

## 0.9.14

- Release from 7ce410c4f9bbcdc148bbec0d5eb4a307b123a719.

## 0.9.13

- Release from 1d035a761af0c9b05c619a1abe2760693da70b57.
