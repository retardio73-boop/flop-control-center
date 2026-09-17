import json
import sys
from pathlib import Path

from core.adoption import validate_report


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python tools/validate_adopter_report.py report.json")
        return 2
    report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate_report(report)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2))
        return 1
    print(json.dumps({"ok": True, "classification": report["classification"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
