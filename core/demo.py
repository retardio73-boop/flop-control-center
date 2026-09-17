from core.trust_boundaries import public_trust_boundaries
from core.continuity import build_continuity_evidence, peer_acknowledgements


def snapshot():
    return {
        'product': 'FLOP Control Center',
        'mode': 'demo',
        'health_score': 93,
        'alerts': [{'level': 'warn', 'text': 'router-fixture has uncommitted changes'}],
        'repos': [
            {'name':'flop-session-router','git':True,'branch':'main','head':'a1b2c3d','dirty':False,'ahead':0,'behind':0,'last':'feat: deterministic failover'},
            {'name':'flop-conformance-lab','git':True,'branch':'main','head':'d4e5f6a','dirty':False,'ahead':0,'behind':0,'last':'test: portable evidence profile'},
            {'name':'router-fixture','git':True,'branch':'experiment','head':'f7a8b9c','dirty':True,'ahead':1,'behind':0,'last':'wip: candidate adapter'},
        ],
        'tasks': [{'TaskName':'ExampleAgent','State':'Running'}],
        'network': {'technocore': {'ok':True,'status':200,'ms':84}, 'github': {'ok':True,'status':200,'ms':47}},
        'github': {'yellow-paper': {'ok':True,'name':'FLOP Yellow Paper','state':'open','comments':12,'ms':52}},
        'logs': [{'path':'runtime/agent.log','tail':'INFO observer active\nINFO cursor restored\nINFO no pending work'}],
        'jobs': {'flop-conformance-lab-demo': {'repo':'flop-conformance-lab','state':'passed','code':0,'output':'19 checks passed'}},
        'trust_boundaries': public_trust_boundaries(),
        'autonomy_evidence': build_continuity_evidence({'tasks':[{'TaskName':'ExampleAgent','State':'Running'}],'network':{'technocore':{'ok':True},'github':{'ok':True}},'repos':[{'name':'flop-session-router','dirty':False,'behind':0},{'name':'flop-conformance-lab','dirty':False,'behind':0}]}),
        'continuity_proof': {
            'schema': 'flop.continuity-proof.v1',
            'state': 'observed',
            'delivered_cycles': 95,
            'expected_cycles': 96,
            'duty_cycle_pct': 98.96,
            'worst_gap_seconds': 1800.0,
            'freshness_seconds': 120.0,
            'restart_count': 2,
            'window_started_at': '2026-09-16T00:00:00+00:00',
            'window_ended_at': '2026-09-17T00:00:00+00:00',
            'claim': 'Demo continuity values are synthetic. Production values come only from durable observation timestamps.',
        },
        'peer_acknowledgements': peer_acknowledgements(),
        'demo': True,
    }