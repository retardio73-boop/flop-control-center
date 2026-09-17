# Peer integration map

This file tracks complementary community projects and the safest integration direction for FLOP Control Center.

## Mariukasfak / FLOP Evidence Scout

Complement: consume public status, freshness, telemetry, and evidence URLs as external evidence sources. Do not duplicate its autonomous-agent implementation. Preserve attribution and source URLs.

Potential adapter: read-only evidence ingestion into Control Center with source, observed_at, freshness, and claim boundary.

## maragung / FLOP Toolkit

Complement: link from the operator-oriented Control Center to user-facing onboarding/toolkit surfaces instead of duplicating identity or contribution UX. Control Center should expose a small machine-readable status contract that consumer apps can embed.

Potential adapter: `/api/status` subset suitable for external dashboards.

## UfukNode / Technocore Live Workstream

Complement: pair our evidence/control layer with a visual activity layer. We should expose bounded agent/runtime events, while visualization remains a separate concern.

Potential adapter: normalized, read-only activity feed with no signing or posting capability.

## ksk7777m / FLOP Agent Intelligence

Complement: consume observatory/spec-drift/safety classifications as external evidence while retaining Conformance Lab as the independent protocol verifier.

Potential adapter: external evidence registry with provenance and trust classification. Never promote community intelligence into protocol truth automatically.

## Rule

Integration must be read-only by default, source-attributed, bounded, and fail closed. External community signals may inform operator attention but cannot authorize signing, settlement, protocol publication, or conformance claims.
