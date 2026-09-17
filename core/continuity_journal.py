import json
from datetime import datetime, timezone
from pathlib import Path


def _parse_ts(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def read_records(path, limit=5000):
    if not path:
        return []
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        return []
    records = []
    with file_path.open('r', encoding='utf-8') as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict) and _parse_ts(item.get('observed_at')):
                records.append(item)
            if len(records) > limit:
                records = records[-limit:]
    return records


def append_record(path, record):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, sort_keys=True, separators=(',', ':'))
    with file_path.open('a', encoding='utf-8', newline='\n') as handle:
        handle.write(line + '\n')


def analyze(records, expected_interval_seconds=900, now=None):
    now = now or datetime.now(timezone.utc)
    expected_interval_seconds = max(1, int(expected_interval_seconds))
    parsed = []
    for item in records:
        ts = _parse_ts(item.get('observed_at'))
        if ts:
            parsed.append((ts, item))
    parsed.sort(key=lambda pair: pair[0])
    if not parsed:
        return {
            'schema': 'flop.continuity-proof.v1',
            'state': 'unknown',
            'delivered_cycles': 0,
            'expected_cycles': 0,
            'duty_cycle_pct': None,
            'worst_gap_seconds': None,
            'freshness_seconds': None,
            'restart_count': 0,
            'window_started_at': None,
            'window_ended_at': None,
            'claim': 'No durable continuity records are available; continuous operation is unknown.',
        }

    times = [ts for ts, _ in parsed]
    span = max(0.0, (times[-1] - times[0]).total_seconds())
    expected = max(1, int(span // expected_interval_seconds) + 1)
    delivered = len(parsed)
    gaps = [(b - a).total_seconds() for a, b in zip(times, times[1:])]
    freshness = max(0.0, (now - times[-1]).total_seconds())
    restarts = 0
    previous_boot = None
    for _, item in parsed:
        boot = item.get('boot_id')
        if boot and previous_boot and boot != previous_boot:
            restarts += 1
        if boot:
            previous_boot = boot

    duty = min(100.0, round((delivered / expected) * 100.0, 2)) if expected else None
    worst_gap = max(gaps) if gaps else 0.0
    stale_after = expected_interval_seconds * 2
    if freshness > stale_after:
        state = 'stale'
    elif duty is not None and duty < 90.0:
        state = 'degraded'
    else:
        state = 'observed'
    return {
        'schema': 'flop.continuity-proof.v1',
        'state': state,
        'delivered_cycles': delivered,
        'expected_cycles': expected,
        'duty_cycle_pct': duty,
        'worst_gap_seconds': round(worst_gap, 3),
        'freshness_seconds': round(freshness, 3),
        'restart_count': restarts,
        'window_started_at': times[0].isoformat(),
        'window_ended_at': times[-1].isoformat(),
        'claim': 'Duty cycle is derived from durable observation timestamps. It measures delivered evidence against the configured cadence; it is not a claim of perfect uptime.',
    }


def build_record(data, boot_id=None, observed_at=None):
    observed_at = observed_at or datetime.now(timezone.utc).isoformat()
    tasks = data.get('tasks', [])
    network = data.get('network', {})
    return {
        'schema': 'flop.continuity-cycle.v1',
        'observed_at': observed_at,
        'boot_id': boot_id,
        'running_tasks': sorted(t.get('TaskName') for t in tasks if str(t.get('State', '')).lower() == 'running' and t.get('TaskName')),
        'healthy_targets': sorted(name for name, state in network.items() if state.get('ok')),
    }
