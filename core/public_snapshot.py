from concurrent.futures import ThreadPoolExecutor
from adapters.git import status as git_status
from adapters.tasks import status as task_status
from adapters.github import summarize as github_summary
from modules.network import collect as network_collect
from modules.logs import collect as logs_collect
from core.config import root_path
from core.jobs import snapshot as jobs_snapshot
from core.trust_boundaries import public_trust_boundaries
from core.operator_cockpit import build_operator_cockpit
from core.continuity import build_continuity_evidence, peer_acknowledgements


def build(cfg):
    root = root_path(cfg)
    repos = cfg.get('repositories', [])
    tasks = cfg.get('tasks', [])
    github = cfg.get('github', {})
    network = cfg.get('network', {})
    log_roots = cfg.get('logs', {}).get('roots', [])

    with ThreadPoolExecutor(max_workers=8) as pool:
        repo_future = pool.submit(lambda: [git_status(root, x) for x in repos])
        task_future = pool.submit(lambda: [task_status(x) for x in tasks])
        github_future = pool.submit(lambda: {k: github_summary(v) for k, v in github.items()})
        network_future = pool.submit(network_collect, network)
        logs_future = pool.submit(logs_collect, root, log_roots)
        data = {
            'repos': repo_future.result(),
            'tasks': task_future.result(),
            'github': github_future.result(),
            'network': network_future.result(),
            'logs': logs_future.result(),
        }
    alerts = []
    for repo in data['repos']:
        if repo.get('dirty'):
            alerts.append({'level': 'warn', 'text': f"{repo['name']} has uncommitted changes"})
        if isinstance(repo.get('behind'), int) and repo['behind'] > 0:
            alerts.append({'level': 'warn', 'text': f"{repo['name']} is behind origin by {repo['behind']} commit(s)"})
    for name, state in data['network'].items():
        if not state.get('ok'):
            alerts.append({'level': 'warn', 'text': f'{name} connectivity failed'})

    trust = public_trust_boundaries()
    bad = sum(1 for item in alerts if item['level'] == 'bad')
    warn = sum(1 for item in alerts if item['level'] == 'warn')
    return {
        'product': 'FLOP Control Center',
        'mode': 'public-safe',
        'repos': data['repos'],
        'tasks': data['tasks'],
        'github': data['github'],
        'network': data['network'],
        'logs': data['logs'],
        'jobs': jobs_snapshot(),
        'trust_boundaries': trust,
        'evidence_cockpit': build_operator_cockpit(data, trust),
        'autonomy_evidence': build_continuity_evidence(data),
        'peer_acknowledgements': peer_acknowledgements(),
        'alerts': alerts,
        'health_score': max(0, 100 - 20 * bad - 7 * warn),
    }
