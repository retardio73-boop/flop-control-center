# FLOP Stack Evolution Master Plan

Purpose: improve the stack without losing existing behavior, evidence, or safety boundaries.

## Operating rule

Work topic by topic under one master program. Each topic gets its own branch/PR, acceptance criteria, regression checks, and explicit before/after evidence. No feature is removed or silently replaced merely to simplify implementation.

## No-loss protocol

Before changing a component:
1. Record current branch/head and working-tree state.
2. Capture the current public/API behavior that matters.
3. List existing features and safety boundaries affected by the change.
4. Add or identify tests that protect those behaviors.
5. Make the smallest reversible change.
6. Run component tests plus cross-stack smoke tests.
7. Compare before/after outputs.
8. Merge only when all intended old features still work or an intentional replacement is documented.

Deletion rule: functionality may only be removed when it is explicitly classified as obsolete, redundant, unsafe, or superseded, with the replacement named and regression coverage proving no required capability was lost.

## Master feature ledger

The ledger is cumulative. A completed gate does not erase earlier requirements.

### Foundation already present
- canonical DID continuity
- isolated signer / fail-closed identity boundary
- autonomous observer/probe path
- mailbox/social/room observation
- Sonnet participation support
- Session Router
- Conformance Lab
- cross-system fixtures and CI
- public Control Center
- trust-boundary separation between operational health and protocol conformance

### Gate A - Public autonomy evidence
Goal: make continuous operation externally legible without overstating uptime.
- machine-readable autonomy evidence schema
- exact observation timestamps
- runtime/network/repository observations
- freshness and UNKNOWN/DEGRADED states
- public UI surface
- explicit claim boundary: snapshot != continuous uptime proof
- peer attribution
Status: IN PROGRESS in PR #4.

### Gate B - Durable continuity proof
Goal: measure real continuity, not process self-reporting.
- persistent cycle journal
- expected-vs-delivered cycle accounting
- duty-cycle calculation
- worst-gap and freshness metrics
- restart counter and recovery evidence
- last successful signer/observer/mailbox events
- no fabricated success when an observation is unavailable

### Gate C - Common Evidence API
Goal: one bounded schema for our own evidence and external community evidence.
Every record must include:
- source
- source_class (official/community/local)
- claim_type
- observed_at
- freshness
- evidence/reference
- verification_state
- authority boundary
External evidence must never become protocol truth automatically.

### Gate D - Peer evidence adapters
Read-only adapters, source-attributed and fail-closed.
Priority peers:
- Mariukasfak / FLOP Evidence Scout: continuity, freshness, telemetry patterns
- ksk7777m / FLOP Agent Intelligence: observatory, spec drift, safety classifications
- UfukNode / Live Workstream: activity visualization patterns
- maragung / FLOP Toolkit: human onboarding and task-oriented UX patterns
Adapters produce ATTENTION/REVIEW signals only unless independently verified.

### Gate E - Drift -> Conformance handoff
Goal: turn upstream/community drift signals into reproducible tests.
Flow:
external or local drift signal -> affected artifact map -> regeneration required -> Conformance Lab reproduction -> PASS/FAIL/UNKNOWN -> evidence record.
- never auto-adopt normative changes
- preserve previous result
- record source and exact revision
- maintain before -> change -> result history

### Gate F - Human-first Control Center
Goal: open -> understand -> act safely.
- live status first
- plain-language summaries
- evidence drill-down second
- visual activity and freshness
- task-oriented actions rather than raw implementation details
- retain machine-readable APIs
- no remote signing/custody expansion

### Gate G - Empires public surface
Goal: make FLOP/Technocore legible to casual users through a persistent world.
- visual map
- visible territory and power
- alliances/NAPs/treaties
- trade routes
- conflict/recon/siege state
- fog of war
- reputation/standing
- human-readable event feed
- stable world-state evidence and replay
Do not sacrifice protocol correctness for visuals; the visual layer consumes deterministic state.

### Gate H - External adoption and collaboration
Goal: make independent use measurable.
- adopter reports
- public integration contract
- examples for consuming status/evidence APIs
- documented peer credits
- upstream issues/PRs linked to resulting fixtures
- external usage separated from stars/forks/self-tests

## Cross-stack regression matrix

Every substantial gate must preserve where applicable:
- DID identity continuity
- signer fail-closed behavior
- no private-key/passphrase exposure
- observer cursor persistence
- mailbox and room visibility
- anti-loop / dedupe / rate-limit behavior
- Sonnet-specific functionality
- Router deterministic eligibility/preflight/failover
- Conformance fixtures and expected verdicts
- Control Center public-safe boundary
- no automatic promotion of community claims to official/normative truth

## Branching discipline

One topic = one branch/PR. Avoid mixed refactors. If a topic touches multiple repositories, create a short integration note linking exact commits in each repository. Do not merge a cleanup into a feature PR unless the cleanup is required for that feature.

## Completion rule

A gate is DONE only when implementation, tests, public/machine-readable evidence, and no-loss checks are all complete. Partial work is recorded as PARTIAL rather than implicitly treated as complete.
