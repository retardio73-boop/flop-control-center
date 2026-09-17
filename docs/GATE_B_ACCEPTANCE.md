# Gate B Acceptance

Gate B is complete only if all of the following remain true:

- Gate A autonomy evidence is still present.
- Missing continuity history reports `unknown`.
- Durable records are append-only JSONL observations.
- Duty cycle is computed from timestamps, not an internal success counter.
- Worst gap, freshness, and boot-id transitions are exposed.
- UI refresh does not create a continuity record.
- Demo mode remains read-only.
- Existing public-safe boundaries remain unchanged.
- Unit tests and demo smoke pass on supported CI platforms.

The continuity proof is operational evidence only. It must never be interpreted as protocol conformance, settlement proof, FLOP eligibility, or guaranteed uptime.
