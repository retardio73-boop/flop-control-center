import unittest
from core.continuity import build_continuity_evidence, peer_acknowledgements

class ContinuityEvidenceTests(unittest.TestCase):
    def test_bounded_evidence(self):
        data={"tasks":[{"TaskName":"AgentA","State":"Running"}],"network":{"technocore":{"ok":True}},"repos":[{"name":"router","dirty":False,"behind":0}]}
        result=build_continuity_evidence(data)
        self.assertEqual(result["schema"],"flop.autonomy-evidence.v1")
        self.assertEqual(result["running_tasks"],["AgentA"])
        self.assertIn("do not prove uninterrupted uptime", result["claim"])
    def test_peer_credit_is_explicit(self):
        names={x["author"] for x in peer_acknowledgements()}
        self.assertTrue({"Mariukasfak","maragung","UfukNode","ksk7777m"}.issubset(names))

if __name__ == "__main__":
    unittest.main()
