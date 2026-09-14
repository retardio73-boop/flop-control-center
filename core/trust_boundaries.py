def tclk_venue_time_boundary(signature_valid, deadline_sensitive, venue_timestamp_authenticated):
    if not signature_valid:
        return {
            'status': 'INVALID_SIGNATURE',
            'fail_closed': True,
            'allow_settlement_claim': False,
            'reason': 'signature verification failed',
        }
    if deadline_sensitive and not venue_timestamp_authenticated:
        return {
            'status': 'UNTRUSTED_VENUE_TIME',
            'fail_closed': True,
            'allow_settlement_claim': False,
            'reason': 'deadline verdict depends on unsigned venue timestamp metadata',
        }
    return {
        'status': 'NO_UNSIGNED_TIME_DEPENDENCY',
        'fail_closed': False,
        'allow_settlement_claim': True,
        'reason': 'no deadline dependency on unauthenticated venue time detected',
    }


def public_trust_boundaries():
    return {
        'tclk_issue_96': {
            'classification': 'OFFICIAL_BUT_TBD',
            'upstream_issue': 'https://github.com/flop-labs/tclk/issues/96',
            'policy': tclk_venue_time_boundary(True, True, False),
            'display_rule': 'Never present a deadline-sensitive TCLK transcript as settlement proof while venue time remains unauthenticated.',
        }
    }
