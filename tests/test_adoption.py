import unittest

from core.adoption import validate_report


def valid_report(classification="EXTERNAL_REPORTED"):
    return {
        "schema": "flop.adopter-report.v1",
        "project": "example/project",
        "repository": "https://github.com/example/project",
        "platform": "Ubuntu 24.04",
        "mode": "public-safe-local",
        "classification": classification,
        "control_center_ref": "main",
        "evidence": ["https://github.com/example/project/actions/runs/1"],
        "notes": None,
    }


class AdoptionTests(unittest.TestCase):
    def test_valid_external_report(self):
        self.assertEqual(validate_report(valid_report()), [])

    def test_self_test_is_explicit_not_external_verified(self):
        report = valid_report("SELF_TEST")
        self.assertEqual(validate_report(report), [])
        self.assertNotEqual(report["classification"], "EXTERNAL_VERIFIED")

    def test_report_requires_evidence_and_known_schema(self):
        report = valid_report()
        report["evidence"] = []
        report["schema"] = "unknown"
        errors = validate_report(report)
        self.assertIn("invalid_evidence", errors)
        self.assertIn("invalid_schema", errors)
