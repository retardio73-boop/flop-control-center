import unittest
from core.evidence_api import make_record, validate_record, classify_for_operator


class EvidenceApiTests(unittest.TestCase):
    def test_community_cannot_be_normative(self):
        record = {
            'source': 'peer', 'source_class': 'community', 'claim_type': 'drift',
            'observed_at': '2026-09-17T04:00:00+00:00', 'freshness': {'state': 'fresh'},
            'evidence': {'url': 'https://example.test'}, 'verification_state': 'observed',
            'authority': {'official': False, 'normative': True, 'grants_action_authority': False},
        }
        self.assertEqual(validate_record(record)['error'], 'community_cannot_be_normative')

    def test_local_source_cannot_claim_official(self):
        record = {
            'source': 'local', 'source_class': 'local', 'claim_type': 'runtime',
            'observed_at': '2026-09-17T04:00:00+00:00', 'freshness': {'state': 'fresh'},
            'evidence': {}, 'verification_state': 'observed',
            'authority': {'official': True, 'normative': False, 'grants_action_authority': False},
        }
        self.assertEqual(validate_record(record)['error'], 'non_official_source_cannot_claim_official')

    def test_community_signal_is_review_only(self):
        record = make_record(
            source='ksk7777m/flop-agent-intelligence', source_class='community', claim_type='spec_drift',
            observed_at='2026-09-17T04:00:00+00:00', freshness={'state': 'fresh', 'age_seconds': 30},
            evidence={'ref': 'example'}, summary='possible drift')
        self.assertEqual(classify_for_operator(record), 'REVIEW')
        self.assertFalse(record['authority']['grants_action_authority'])

    def test_verified_official_still_requires_review(self):
        record = make_record(
            source='flop-labs', source_class='official', claim_type='spec_revision',
            observed_at='2026-09-17T04:00:00+00:00', freshness={'state': 'fresh'},
            evidence={'revision': 'abc'}, verification_state='verified',
            authority={'official': True, 'normative': False, 'grants_action_authority': False})
        self.assertEqual(classify_for_operator(record), 'REVIEW_OFFICIAL')


if __name__ == '__main__':
    unittest.main()
