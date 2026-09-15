import unittest
from core.operator_cockpit import build_operator_cockpit


class OperatorCockpitTests(unittest.TestCase):
    def test_clean_state_is_observational_only(self):
        data = {'repos': [{'name': 'router', 'dirty': False, 'behind': 0}], 'network': {'venue': {'ok': True}}}
        result = build_operator_cockpit(data, {'boundary': {}})
        self.assertEqual(result['repository_state'], 'CLEAN')
        self.assertEqual(result['network_state'], 'HEALTHY')
        self.assertEqual(result['tracked_trust_boundaries'], 1)
        self.assertIn('not protocol conformance', result['rule'])

    def test_drift_is_explicit_without_becoming_conformance(self):
        data = {'repos': [{'name': 'lab', 'dirty': True, 'behind': 2}], 'network': {'venue': {'ok': False}}}
        result = build_operator_cockpit(data, {})
        self.assertEqual(result['repository_state'], 'ATTENTION_REQUIRED')
        self.assertEqual(result['dirty_repositories'], ['lab'])
        self.assertEqual(result['behind_repositories'], ['lab'])
        self.assertEqual(result['network_failures'], ['venue'])


if __name__ == '__main__':
    unittest.main()
