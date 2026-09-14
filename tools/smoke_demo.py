import json, os, subprocess, sys, time, urllib.error, urllib.request

PORT = '8877'
env = os.environ.copy()
env['FLOP_CONTROL_CENTER_PORT'] = PORT
proc = subprocess.Popen([sys.executable, 'server_public.py', '--demo'], env=env)
try:
    deadline = time.time() + 10
    data = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/api/status', timeout=1) as response:
                data = json.loads(response.read().decode())
            break
        except Exception:
            time.sleep(0.2)
    assert data and data.get('mode') == 'demo' and data.get('demo') is True
    boundary = data.get('trust_boundaries', {}).get('tclk_issue_96', {})
    policy = boundary.get('policy', {})
    assert boundary.get('classification') == 'OFFICIAL_BUT_TBD'
    assert policy.get('status') == 'UNTRUSTED_VENUE_TIME'
    assert policy.get('fail_closed') is True
    assert policy.get('allow_settlement_claim') is False
    request = urllib.request.Request(f'http://127.0.0.1:{PORT}/api/check', data=b'{}', method='POST', headers={'Content-Type':'application/json'})
    try:
        urllib.request.urlopen(request, timeout=2)
        raise AssertionError('demo POST unexpectedly succeeded')
    except urllib.error.HTTPError as exc:
        assert exc.code == 403
        body = json.loads(exc.read().decode())
        assert body.get('error') == 'DEMO_READ_ONLY'
    print('DEMO_SMOKE_PASS')
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
