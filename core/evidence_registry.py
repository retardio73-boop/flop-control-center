from core.evidence_api import validate_record, classify_for_operator


def build_registry(records):
    accepted = []
    rejected = []
    for item in records or []:
        verdict = validate_record(item)
        if verdict.get('ok'):
            accepted.append({**item, 'operator_classification': classify_for_operator(item)})
        else:
            rejected.append({'source': item.get('source'), 'error': verdict.get('error')})
    return {
        'schema': 'flop.evidence-registry.v1',
        'records': accepted,
        'rejected': rejected,
        'claim': 'Registry entries are evidence records, not automatic protocol truth or action authority.',
    }
