import os
import subprocess
from pathlib import Path

from core.runner import run


def open_repo(root: Path, name: str, allowed):
    if name not in allowed:
        return {'ok': False, 'code': -1, 'out': '', 'err': 'INVALID_REPOSITORY'}
    path = (root / name).resolve()
    if not path.exists() or not path.is_dir():
        return {'ok': False, 'code': -1, 'out': '', 'err': 'REPOSITORY_MISSING'}
    if os.name == 'nt':
        return run(['explorer.exe', str(path)], timeout=8)
    opener = 'open' if subprocess.run(['uname'], capture_output=True, text=True).stdout.strip() == 'Darwin' else 'xdg-open'
    return run([opener, str(path)], timeout=8)
