from __future__ import annotations

from typing import Any

SCHEMA = "flop.adopter-report.v1"
MODES = {"demo", "public-safe-local", "embedded-integrated"}
CLASSIFICATIONS = {"SELF_TEST", "EXTERNAL_REPORTED", "EXTERNAL_VERIFIED"}


def validate_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"schema", "project", "platform", "mode", "classification", "evidence"}
    missing = sorted(required - set(report))
    if missing:
        errors.append("missing:" + ",".join(missing))
    if report.get("schema") != SCHEMA:
        errors.append("invalid_schema")
    if report.get("mode") not in MODES:
        errors.append("invalid_mode")
    if report.get("classification") not in CLASSIFICATIONS:
        errors.append("invalid_classification")
    for field in ("project", "platform"):
        if not isinstance(report.get(field), str) or not report.get(field, "").strip():
            errors.append(f"invalid_{field}")
    evidence = report.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x.strip() for x in evidence):
        errors.append("invalid_evidence")
    return errors
