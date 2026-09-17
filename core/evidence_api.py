from datetime import datetime, timezone

ALLOWED_SOURCE_CLASSES = {'official', 'community', 'local'}
ALLOWED_VERIFICATION_STATES = {'verified', 'observed', 'reported', 'unknown', 'invalid'}


def _iso(value):
    if not value:
        return None
    if isinstance(value, str):
        return value
    return value.astimezone(timezone.utc).isoformat()


def validate_record(record):
    required = ['source', 'source_class', 'claim_type', 'observed_at', 'freshness', 'evidence', 'verification_state', 'authority']
    missing = [key for key in required if key not in record]
    if missing:
        return {'ok': False, 'error': 'missing_fields', 'fields': missing}
    if record['source_class'] not in ALLOWED_SOURCE_CLASSES:
        return {'ok': False, 'error': 'invalid_source_class'}
    if record['verification_state'] not in ALLOWED_VERIFICATION_STATES:
        return {'ok': False, 'error': 'invalid_verification_state'}
    authority = record.get('authority') or {}
    if record['source_class'] == 'community' and authority.get('normative') is True:
        return {'ok': False, 'error': 'community_cannot_be_normative'}
    if record['source_class'] != 'official' and authority.get('official') is True:
        return {'ok': False, 'error': 'non_official_source_cannot_claim_official'}
    return {'ok': True}


def make_record(*, source, source_class, claim_type, observed_at, freshness, evidence, verification_state='observed', authority=None, summary=None, tags=None):
    record = {
        'schema': 'flop.evidence.v1',
        'source': source,
        'source_class': source_class,
        'claim_type': claim_type,
        'observed_at': _iso(observed_at),
        'freshness': freshness,
        'evidence': evidence,
        'verification_state': verification_state,
        'authority': authority or {'official': source_class == 'official', 'normative': False, 'grants_action_authority': False},
        'summary': summary,
        'tags': tags or [],
    }
    verdict = validate_record(record)
    if not verdict['ok']:
        raise ValueError(verdict['error'])
    return record


def classify_for_operator(record):
    verdict = validate_record(record)
    if not verdict['ok']:
        return 'REJECT'
    if record['source_class'] == 'official' and record['verification_state'] == 'verified':
        return 'REVIEW_OFFICIAL'
    if record['verification_state'] in {'invalid', 'unknown'}:
        return 'ATTENTION'
    return 'REVIEW'
