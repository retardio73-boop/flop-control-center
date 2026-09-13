# FLOP Control Center

A small local operator dashboard for FLOP-oriented development stacks.

It gives builders one place to inspect repository state, GitHub/upstream targets, network health, recent logs, background checks, and explicitly allowlisted local controls.

## Why

Multi-repository agent stacks become hard to operate before they become hard to build. Control Center keeps operational evidence visible without becoming a signing or protocol-execution surface.

## Public-safe surface

- repository branch/head/dirty/ahead-behind state
- background repository checks
- GitHub target summaries
- network reachability and latency
- recent bounded log tails
- allowlisted folder opening
- allowlisted task start/stop on Windows
- health score and operator alerts

Signing, key export, protocol publication and other irreversible protocol actions are intentionally out of scope.

## Run locally

1. Copy `config/config.example.json` to `config/config.local.json`.
2. Set your stack root, repositories and optional targets.
3. Run `python server_public.py`.
4. Open `http://127.0.0.1:8765/`.

Python 3.11+ is recommended. No third-party Python package is required for the public-safe core.

## Configuration

`config.local.json` stays local and should contain machine-specific paths and allowlists. Empty task, GitHub, network and log sections are valid.

## Safety model

The public surface is deny-by-default. Repository and task actions require explicit allowlisting. Unsupported task control outside Windows fails closed. Unknown evidence is not promoted to verified state.

## Maturity

Alpha. The current focus is local operational visibility and reversible controls, not remote administration or protocol custody.

## License

Apache-2.0.
