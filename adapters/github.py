import json, time, urllib.request

def fetch_json(url, timeout=6):
    started=time.time()
    try:
        req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'flop-control-center'})
        with urllib.request.urlopen(req,timeout=timeout) as r:
            data=json.loads(r.read().decode())
        return {'ok':True,'ms':int((time.time()-started)*1000),'data':data}
    except Exception as e:
        return {'ok':False,'ms':int((time.time()-started)*1000),'error':str(e)}

def summarize(url, timeout=6):
    r=fetch_json(url,timeout)
    if not r.get('ok'): return r
    o=r.pop('data')
    r.update({'name':o.get('full_name') or o.get('title'),'updated_at':o.get('updated_at'),'state':o.get('state'),'comments':o.get('comments'),'stars':o.get('stargazers_count'),'forks':o.get('forks_count'),'html_url':o.get('html_url')})
    return r