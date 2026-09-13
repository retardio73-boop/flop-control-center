from core.runner import run


def status(root, name):
    p = root / name
    if not (p / '.git').exists():
        return {'name': name, 'git': False}
    branch = run(['git','branch','--show-current'], p)['out']
    head = run(['git','rev-parse','--short','HEAD'], p)['out']
    raw = run(['git','status','--porcelain'], p)['out']
    remote = run(['git','remote','get-url','origin'], p)['out']
    last = run(['git','log','-1','--format=%cI|%s'], p)['out']
    ahead = behind = None
    if remote and branch:
        run(['git','fetch','origin','--quiet'], p, 20)
        ab = run(['git','rev-list','--left-right','--count',f'HEAD...origin/{branch}'], p)['out'].split()
        if len(ab) == 2:
            ahead, behind = map(int, ab)
    return {'name':name,'git':True,'branch':branch,'head':head,'dirty':bool(raw),'changes':len(raw.splitlines()) if raw else 0,'remote':remote,'last':last,'diff':raw.splitlines()[:20],'ahead':ahead,'behind':behind}
