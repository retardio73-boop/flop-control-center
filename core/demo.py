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
        'demo': True,
    }
