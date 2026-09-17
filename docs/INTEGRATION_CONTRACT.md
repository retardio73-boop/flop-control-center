# FLOP public integration contract v1

This contract defines how independent tools may consume FLOP Control Center public-safe data without inheriting operator authority.

## Endpoints

- `GET /api/status` returns the current public-safe operational snapshot.
- `GET /api/evidence` returns `flop.evidence-registry.v1` records and rejections.

Consumers MUST treat both endpoints as observational data. Neither endpoint grants signing, settlement, publication, roster consent, custody, or protocol authority.

## Evidence semantics

Every evidence record carries source class, verification state, and explicit authority fields. Community or local evidence cannot become official or normative merely because it is displayed by Control Center.

Unknown, stale, unsupported, invalid, or missing evidence must remain visibly unresolved. Consumers must not upgrade those states to success.

## Compatibility

Consumers should key behavior to schema identifiers rather than UI text. Unknown schema versions must fail closed or be ignored explicitly.

The public surface may add fields. Existing fields are not silently repurposed across schema versions.

## Independent adoption

Independent users can submit an adopter report conforming to `schemas/flop-adopter-report-v1.schema.json`. Stars, forks, self-tests, local maintainer runs, and synthetic demos are not external adoption.
