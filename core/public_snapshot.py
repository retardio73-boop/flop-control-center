from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
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
from core.continuity_journal import read_records, analyze
from core.evidence_api import make_record
from core.evidence_registry import build_registry


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

    continuity_cfg = cfg.get('continuity', {})
    journal = continuity_cfg.get('journal')
    if journal and not Path(journal).is_absolute():
        journal = str(root / journal)
    continuity_metrics = analyze(
        read_records(journal),
        expected_interval_seconds=int(continuity_cfg.get('expected_interval_seconds', 900)),
    )

    local_evidence = []
    if continuity_metrics.get('state') != 'unknown':
        local_evidence.append(make_record(
            source='flop-control-center', source_class='local', claim_type='continuity',
            observed_at=continuity_metrics.get('last_observed_at'),
            freshness={'state': continuity_metrics.get('freshness_state'), 'age_seconds': continuity_metrics.get('freshness_seconds')},
            evidence={'schema': continuity_metrics.get('schema'), 'delivered_cycles': continuity_metrics.get('delivered_cycles'), 'expected_cycles': continuity_metrics.get('expected_cycles'), 'duty_cycle': continuity_metrics.get('duty_cycle'), 'worst_gap_seconds': continuity_metrics.get('worst_gap_seconds')},
            verification_state='observed',
            authority={'official': False, 'normative': False, 'grants_action_authority': False},
            summary='locally measured continuity evidence'))
    evidence_registry = build_registry(local_evidence)

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
        'continuity_proof': continuity_metrics,
        'evidence_registry': evidence_registry,
        'peer_acknowledgements': peer_acknowledgements(),
        'alerts': alerts,
        'health_score': max(0, 100 - 20 * bad - 7 * warn),
    }
