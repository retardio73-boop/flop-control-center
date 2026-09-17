import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from core.continuity_journal import analyze, append_record, read_records


class ContinuityJournalTests(unittest.TestCase):
    def test_unknown_without_records(self):
        out = analyze([], expected_interval_seconds=60, now=datetime(2026, 9, 17, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(out['state'], 'unknown')
        self.assertIsNone(out['duty_cycle_pct'])

    def test_measures_duty_gap_freshness_and_restarts(self):
        records = [
            {'observed_at': '2026-09-17T00:00:00+00:00', 'boot_id': 'a'},
            {'observed_at': '2026-09-17T00:01:00+00:00', 'boot_id': 'a'},
            {'observed_at': '2026-09-17T00:03:00+00:00', 'boot_id': 'b'},
        ]
        out = analyze(records, expected_interval_seconds=60, now=datetime(2026, 9, 17, 0, 3, 30, tzinfo=timezone.utc))
        self.assertEqual(out['expected_cycles'], 4)
        self.assertEqual(out['delivered_cycles'], 3)
        self.assertEqual(out['duty_cycle_pct'], 75.0)
        self.assertEqual(out['worst_gap_seconds'], 120.0)
        self.assertEqual(out['freshness_seconds'], 30.0)
        self.assertEqual(out['restart_count'], 1)
        self.assertEqual(out['state'], 'degraded')

    def test_append_and_read_are_bounded_and_ignore_bad_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'continuity.jsonl'
            append_record(path, {'observed_at': '2026-09-17T00:00:00+00:00', 'boot_id': 'a'})
            with path.open('a', encoding='utf-8') as handle:
                handle.write('not json\n')
            append_record(path, {'observed_at': '2026-09-17T00:01:00+00:00', 'boot_id': 'a'})
            records = read_records(path)
            self.assertEqual(len(records), 2)


if __name__ == '__main__':
    unittest.main()
