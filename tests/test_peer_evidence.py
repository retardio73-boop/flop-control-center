import io
import json
import unittest

from adapters.peer_evidence import collect


class _Response:
    def __init__(self, payload):
        self._raw = json.dumps(payload).encode('utf-8')
        self.headers = {'Content-Length': str(len(self._raw))}
    def read(self, size=-1):
        return self._raw[:size] if size >= 0 else self._raw
    def close(self):
        pass


class _Opener:
    def __init__(self, payloads):
        self.payloads = payloads
    def open(self, req, timeout=None):
        url = req.full_url
        if 'flop-evidence-scout' in url:
            return _Response(self.payloads['evidence_scout'])
        return _Response(self.payloads['agent_intelligence'])


class PeerEvidenceTests(unittest.TestCase):
    def test_peer_records_are_review_only(self):
        payloads = {
            'evidence_scout': {
                'checkedAt': '2026-09-14T14:05:12.334Z',
                'stale': 1,
                'artefacts': [{'id':'daemon','state':'STALE','ageMin':205.2,'duty':{'ratio':0.06,'worstGapMin':2813.6}}],
            },
            'agent_intelligence': {
                'schema':'technocore-observatory-status-v1',
                'reviewed_at':'2026-09-11T03:29:35Z',
                'snapshot_classification':'HISTORICAL_SNAPSHOT',
                'source_status':'OFFICIAL',
                'official_spec_status':'HISTORICAL_SNAPSHOT_NOT_CURRENT',
                'compatibility':{'action':'NO_LIVE_ACTION'},
                'warnings':['historical'],
                'external_writes':0,
            },
        }
        out = collect(opener=_Opener(payloads))
        self.assertEqual(len(out['records']), 2)
        for record in out['records']:
            self.assertEqual(record['source_class'], 'community')
            self.assertFalse(record['authority']['official'])
            self.assertFalse(record['authority']['normative'])
            self.assertFalse(record['authority']['grants_action_authority'])
