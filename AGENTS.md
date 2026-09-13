# Agent integration

Start with `python server_public.py --demo` to inspect the surface without touching local state.

For a real stack, copy `config/config.example.json` or `config/presets/flop-stack.example.json` to `config/config.local.json`, then edit only your own paths and explicit allowlists.

Primary read endpoint:
- `GET /api/status`

Reversible write endpoints:
- `POST /api/check` with an allowlisted repository
- `POST /api/open` with an allowlisted repository
- `POST /api/task` with an allowlisted task and `start` or `stop`

`--demo` disables all POST actions and returns `DEMO_READ_ONLY`.

Do not use this project for signing, custody, settlement, protocol publication, autonomous replies, roster consent, or other irreversible actions. Treat dashboard health as operational evidence only, not protocol conformance or settlement proof.
