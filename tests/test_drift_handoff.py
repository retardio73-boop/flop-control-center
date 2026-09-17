import json
import tempfile
import unittest
from pathlib import Path

from core.drift_handoff import read_handoff


class DriftHandoffTests(unittest.TestCase):
    def test_missing_handoff_fails_closed(self):
        data = read_handoff('Z:/definitely-missing/handoff.json')
        self.assertEqual(data['state'], 'missing')
        self.assertEqual(data['items'], [])

    def test_valid_handoff_is_read_only_observation(self):
        payload = {
            'schema': 'flop.drift-conformance-handoff.v1',
            'createdAt': '2026-09-17T06:00:00Z',
            'items': [{'id': 'yellowpaper-main:0', 'reproduction': {'status': 'PENDING'}}],
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'handoff.json'
            path.write_text(json.dumps(payload), encoding='utf-8')
            data = read_handoff(path)
        self.assertEqual(data['state'], 'observed')
        self.assertEqual(data['items'][0]['reproduction']['status'], 'PENDING')
        self.assertIn('does not promote', data['claim'])

    def test_wrong_schema_is_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'handoff.json'
            path.write_text(json.dumps({'schema': 'wrong', 'items': []}), encoding='utf-8')
            data = read_handoff(path)
        self.assertEqual(data['state'], 'invalid')


if __name__ == '__main__':
    unittest.main()
