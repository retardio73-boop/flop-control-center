from datetime import datetime, timezone


def build_continuity_evidence(data):
    tasks = data.get("tasks", [])
    network = data.get("network", {})
    repos = data.get("repos", [])
    running = [t.get("TaskName") for t in tasks if str(t.get("State", "")).lower() == "running"]
    healthy_targets = [name for name, state in network.items() if state.get("ok")]
    clean_repos = [r.get("name") for r in repos if not r.get("dirty") and not (isinstance(r.get("behind"), int) and r.get("behind") > 0)]
    signals = []
    signals.append({"name": "runtime", "state": "observed" if running else "unknown", "detail": f"{len(running)} configured task(s) running" if running else "no configured running task observed"})
    signals.append({"name": "network", "state": "observed" if network and len(healthy_targets) == len(network) else ("degraded" if network else "unknown"), "detail": f"{len(healthy_targets)}/{len(network)} configured targets healthy" if network else "no public network targets configured"})
    if repos:
        signals.append({"name": "repository", "state": "observed" if len(clean_repos) == len(repos) else "attention", "detail": f"{len(clean_repos)}/{len(repos)} repositories clean and not behind"})
    return {
        "schema": "flop.autonomy-evidence.v1",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "signals": signals,
        "running_tasks": running,
        "healthy_targets": healthy_targets,
        "claim": "These are bounded observations from this control surface; they do not prove uninterrupted uptime.",
    }


def peer_acknowledgements():
    return [
        {"project": "FLOP Evidence Scout", "author": "Mariukasfak", "lesson": "publish checkable continuity evidence, freshness, unknowns, and failure history", "applied_as": "bounded autonomy evidence and explicit evidence limitations"},
        {"project": "FLOP Toolkit", "author": "maragung", "lesson": "make the first useful action obvious to non-protocol users", "applied_as": "compact public status surface and progressive disclosure"},
        {"project": "Technocore Live Workstream", "author": "UfukNode", "lesson": "make abstract agent activity visually legible", "applied_as": "human-readable runtime and network signals"},
        {"project": "FLOP Agent Intelligence", "author": "ksk7777m", "lesson": "separate observability, evidence, safety boundaries, and drift signals", "applied_as": "evidence cockpit plus explicit trust boundaries"},
    ]
