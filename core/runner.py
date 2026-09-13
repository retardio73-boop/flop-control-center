import subprocess


def run(cmd, cwd=None, timeout=12):
    try:
        p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout)
        return {'ok': p.returncode == 0, 'code': p.returncode, 'out': p.stdout.strip(), 'err': p.stderr.strip()}
    except Exception as exc:
        return {'ok': False, 'code': -1, 'out': '', 'err': str(exc)}
