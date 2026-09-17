import json
import sys
from urllib.request import urlopen


def fetch_json(url: str) -> dict:
    with urlopen(url, timeout=5) as response:
        return json.load(response)


def main() -> int:
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8765"
    status = fetch_json(base + "/api/status")
    evidence = fetch_json(base + "/api/evidence")
    print(json.dumps({
        "health_score": status.get("health_score"),
        "alerts": status.get("alerts", []),
        "continuity_schema": status.get("continuity_proof", {}).get("schema"),
        "evidence_schema": evidence.get("schema"),
        "accepted_evidence": len(evidence.get("records", [])),
        "rejected_evidence": len(evidence.get("rejected", [])),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
