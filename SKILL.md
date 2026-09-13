---
name: flop-control-center
description: Inspect and operate a local FLOP-oriented development stack through the FLOP Control Center public-safe surface. Use when an agent needs repository health, checks, GitHub/upstream status, network reachability, bounded logs, or reversible allowlisted local controls. Never use it for signing, custody, protocol publication, roster consent, settlement, or other irreversible actions.
---

# FLOP Control Center

Use the public-safe Control Center as an observability and reversible-operations surface.

## Quick start
- Preview without local configuration: `python server_public.py --demo`.
- Real local use: copy `config/config.example.json` to `config/config.local.json`, set explicit allowlists, then run `python server_public.py`.
- Read `AGENTS.md` before automating actions.

## Agent rules
1. Treat `/api/status` as observational evidence, not protocol truth.
2. Use repository checks only for explicitly allowlisted repositories.
3. Use task start/stop only when the task is explicitly allowlisted and the operator requested a reversible control action.
4. Never infer signing, settlement, identity ownership, or protocol conformance from dashboard health alone.
5. Fail closed when a target is missing, unsupported, or returns unknown evidence.
