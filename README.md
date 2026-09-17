# FLOP Control Center

See your FLOP-oriented development stack in one place.

- repository health and branch/head/dirty state
- background checks and bounded job output
- GitHub/upstream and network health
- recent bounded logs
- reversible allowlisted local controls
- no signing, custody, settlement, or protocol publication

## Try it in 30 seconds

```bash
python server_public.py --demo
```

Open `http://127.0.0.1:8765/`. Demo mode uses synthetic data, loads no local config, and rejects every POST action with `DEMO_READ_ONLY`.

![Demo dashboard](docs/assets/demo.png)

## Use it on a local stack

1. Copy `config/config.example.json` to `config/config.local.json`.
2. Or start from `config/presets/flop-stack.example.json` for a FLOP-oriented stack.
3. Set only your own stack root, repositories, optional targets, logs, and task allowlists.
4. Run `python server_public.py`.
5. Open `http://127.0.0.1:8765/`.

Python 3.11+ is recommended; the public-safe core has no third-party Python dependency.

## For agents

Start with [`AGENTS.md`](AGENTS.md), [`SKILL.md`](SKILL.md), and [`llms.txt`](llms.txt). The primary observational endpoint is `GET /api/status`. Reversible actions are allowlisted and intentionally narrow.

## Adoption

External use is tracked in [`ADOPTERS.md`](ADOPTERS.md), separately from stars/forks/self-tests. If you run this independently, submit the **External adopter report** issue template with reproducible bounded evidence and no secrets.

## Safety model

The public surface is deny-by-default. Unknown or unsupported evidence stays unknown/unsupported. Signing, key export, identity custody, protocol publication, autonomous replies, roster consent, settlement, and other irreversible protocol actions are out of scope.

## Maturity

Alpha. The focus is local operational visibility and reversible controls, not remote administration or protocol custody.

## Works with

- [FLOP Conformance Lab](https://github.com/retardio73-boop/flop-conformance-lab) — profile-scoped interoperability evidence. Dashboard health must never be treated as conformance.
- [FLOP Session Router](https://github.com/retardio73-boop/flop-session-router) — deterministic routing, preflight, failover and auditable decisions.

Control Center is the operator surface; Conformance Lab is the evidence surface; Session Router is the routing surface.

## License

Apache-2.0.


## Public autonomy evidence

`GET /api/status` includes a bounded `flop.autonomy-evidence.v1` section. It reports what this instance can actually observe (configured runtime tasks, network targets, and repository state) and explicitly does **not** claim uninterrupted uptime. Design influences and attribution are documented in [`docs/PEER_LEARNINGS.md`](docs/PEER_LEARNINGS.md).
