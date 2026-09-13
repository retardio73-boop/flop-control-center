import threading
import time
from pathlib import Path

from core.runner import run

_JOBS = {}
_LOCK = threading.Lock()


def check_command(path: Path):
    if (path / 'package.json').exists():
        return ['npm.cmd', 'run', 'check']
    python = path / '.venv' / 'Scripts' / 'python.exe'
    if python.exists() and (path / 'tests').exists():
        return [str(python), '-m', 'unittest', 'discover', '-s', 'tests', '-v']
    raise ValueError('NO_CHECK_COMMAND')


def snapshot():
    with _LOCK:
        return {key: dict(value) for key, value in _JOBS.items()}


def _run_job(job_id, repo, path):
    with _LOCK:
        _JOBS[job_id] = {'state': 'running', 'repo': repo, 'started': time.time()}
    try:
        cmd = check_command(path)
        result = run(cmd, path, 240)
        state = 'passed' if result['ok'] else 'failed'
        output = (result.get('out', '') + '\n' + result.get('err', ''))[-16000:]
    except Exception as exc:
        state = 'failed'
        result = {'code': -1}
        output = str(exc)
    with _LOCK:
        _JOBS[job_id].update({'state': state, 'code': result['code'], 'output': output, 'finished': time.time()})


def start(root: Path, repo: str, allowed):
    if repo not in allowed:
        raise ValueError('INVALID_REPOSITORY')
    path = root / repo
    if not path.exists():
        raise ValueError('REPOSITORY_MISSING')
    job_id = f'{repo}-{int(time.time() * 1000)}'
    threading.Thread(target=_run_job, args=(job_id, repo, path), daemon=True).start()
    return job_id
