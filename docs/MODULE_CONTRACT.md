# Module contract

Every module must be read-only by default and return JSON-serializable data.

Required fields:
- id: stable module identifier.
- title: display name.
- status: ok | warn | error | unknown.
- summary: short operator-facing state.
- updated_at: observation timestamp.
- data: module-specific structured payload.
- alerts: zero or more structured alerts.
- actions: declared reversible actions only.

Action contract:
- id, label, risk, reversible, confirmation_required.
- Core must reject actions not explicitly declared by the module.
- Irreversible protocol actions are excluded from the generic action executor.

Health contract:
- health checks must distinguish unavailable, stale and contradictory evidence.
- Local state and public/network-visible state must remain separate fields.
- Unknown evidence must never be promoted to verified.
