# Peer evidence adapters

Gate D adds bounded, read-only adapters for complementary community projects.

## FLOP Evidence Scout — Mariukasfak

Source: public `docs/freshness.json`.

Imported fields are limited to freshness/duty observations such as artefact state, age, duty ratio, and worst gap. The adapter preserves the source as community-reported evidence and does not reinterpret it as protocol truth.

Credit: the continuity/freshness model and explicit duty-cycle reporting are learned from FLOP Evidence Scout.

## FLOP Agent Intelligence — ksk7777m

Source: public `api/status.json`.

Imported fields are limited to snapshot classification, compatibility/currentness, warnings, source status, and external-write count. Historical/currentness caveats are preserved.

Credit: the observatory/currentness boundaries and explicit warning surface are learned from FLOP Agent Intelligence.

## Safety and authority

- disabled by default;
- fixed HTTPS source URLs only;
- redirects blocked;
- bounded timeout and payload size;
- malformed/unavailable sources become adapter errors;
- all imported records are `source_class=community`;
- imported records never set official/normative/action authority;
- peer signals are for operator review and later independent Conformance Lab reproduction.
