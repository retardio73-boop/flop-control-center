import json
import os

from core.runner import run


def status(name):
    if os.name != 'nt':
        return {'TaskName': name, 'State': 'Unsupported', 'platform': os.name}
    ps = "$t=Get-ScheduledTask -TaskName '" + name + "' -ErrorAction SilentlyContinue; if($t){[PSCustomObject]@{TaskName=$t.TaskName;State=$t.State.ToString()}|ConvertTo-Json -Compress}"
    result = run(['powershell', '-NoProfile', '-Command', ps])
    try:
        return json.loads(result['out']) if result['out'] else {'TaskName': name, 'State': 'Missing'}
    except Exception:
        return {'TaskName': name, 'State': 'Unknown'}


def control(name, action):
    if action not in {'start', 'stop'}:
        return {'ok': False, 'code': -1, 'out': '', 'err': 'INVALID_ACTION'}
    if os.name != 'nt':
        return {'ok': False, 'code': -1, 'out': '', 'err': 'UNSUPPORTED_PLATFORM'}
    verb = 'Start-ScheduledTask' if action == 'start' else 'Stop-ScheduledTask'
    return run(['powershell', '-NoProfile', '-Command', f"{verb} -TaskName '{name}'"])
