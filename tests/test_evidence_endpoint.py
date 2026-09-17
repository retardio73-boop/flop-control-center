import json
import os
import subprocess
import sys
import time
import urllib.request
import unittest

class EvidenceEndpointTests(unittest.TestCase):
    def test_demo_evidence_endpoint(self):
        env = dict(os.environ)
        env['FLOP_CONTROL_CENTER_PORT'] = '8877'
        proc = subprocess.Popen(
            [sys.executable, 'server_public.py', '--demo'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
        try:
            data = None
            for _ in range(30):
                try:
                    with urllib.request.urlopen('http://127.0.0.1:8877/api/evidence', timeout=1) as r:
                        data = json.loads(r.read().decode())
                    break
                except Exception:
                    time.sleep(0.1)
            self.assertIsNotNone(data)
            self.assertEqual(data['schema'], 'flop.evidence-registry.v1')
            self.assertEqual(len(data['records']), 1)
            self.assertEqual(data['records'][0]['source_class'], 'community')
            self.assertEqual(data['records'][0]['operator_classification'], 'REVIEW')
            self.assertFalse(data['records'][0]['authority']['grants_action_authority'])
        finally:
            proc.terminate()
            proc.wait(timeout=5)

if __name__ == '__main__':
    unittest.main()
