import json
from pathlib import Path

SCHEMA = 'flop.drift-conformance-handoff.v1'


def read_handoff(path):
    if not path:
        return {'schema': SCHEMA, 'state': 'disabled', 'items': [], 'claim': 'No drift handoff configured.'}
    p = Path(path)
    if not p.exists():
        return {'schema': SCHEMA, 'state': 'missing', 'items': [], 'claim': 'Configured drift handoff is unavailable.'}
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return {'schema': SCHEMA, 'state': 'invalid', 'items': [], 'claim': 'Configured drift handoff could not be parsed.'}
    if data.get('schema') != SCHEMA or not isinstance(data.get('items'), list):
        return {'schema': SCHEMA, 'state': 'invalid', 'items': [], 'claim': 'Configured drift handoff failed schema validation.'}
    return {
        'schema': SCHEMA,
        'state': 'observed',
        'created_at': data.get('createdAt'),
        'items': data['items'],
        'claim': 'Read-only Conformance Lab handoff. Control Center does not promote or modify conformance results.',
    }
