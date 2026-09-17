# Durable Continuity Proof

`flop.continuity-proof.v1` summarizes an append-only observation journal. It is designed to make autonomous operation checkable without pretending that a process can prove its own uninterrupted uptime.

## What is measured

- delivered observation cycles
- expected cycles from the configured cadence
- duty cycle (`delivered / expected`, capped at 100%)
- worst observed gap
- freshness of the newest durable record
- boot-id transitions as a bounded restart signal

## What is not claimed

- perfect uptime
- causal explanation for a missed cycle
- signer availability unless separately observed
- protocol conformance
- settlement correctness
- FLOP eligibility or rewards

## Recording rule

The dashboard never appends continuity records. A supervisor or scheduler must execute `tools/record_continuity.py` exactly once per intended cycle. This prevents UI refreshes or API polling from manufacturing continuity evidence.

## Failure semantics

No journal: `unknown`.

Fresh evidence with >=90% delivered cycles: `observed`.

Fresh evidence with <90% delivered cycles: `degraded`.

Newest evidence older than two configured intervals: `stale`.

Malformed journal lines are ignored rather than promoted into evidence. The reader is bounded to the newest 5,000 valid records.

## Inspiration and attribution

The design is informed by Mariukasfak's FLOP Evidence Scout, particularly its emphasis on delivered-vs-requested scheduler cycles, freshness, worst-gap measurement, explicit limitations, and publishing failures rather than only success counters. This implementation is independent and intentionally smaller: it defines a generic Control Center evidence contract rather than copying Scout's runtime or identity architecture.
