def build_operator_cockpit(data, trust_boundaries):
    repos = data.get('repos', [])
    network = data.get('network', {})
    dirty = [item.get('name') for item in repos if item.get('dirty')]
    behind = [item.get('name') for item in repos if isinstance(item.get('behind'), int) and item['behind'] > 0]
    network_failures = [name for name, state in network.items() if not state.get('ok')]
    return {
        'schema': 'flop.operator-evidence-cockpit.v1',
        'repository_state': 'CLEAN' if not dirty and not behind else 'ATTENTION_REQUIRED',
        'dirty_repositories': dirty,
        'behind_repositories': behind,
        'network_state': 'HEALTHY' if not network_failures else 'DEGRADED',
        'network_failures': network_failures,
        'tracked_trust_boundaries': len(trust_boundaries),
        'rule': 'dashboard health is operational evidence, not protocol conformance',
    }
