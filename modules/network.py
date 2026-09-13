import time, urllib.request

def check(url, timeout=5):
    started=time.time()
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'flop-control-center'})
        with urllib.request.urlopen(req,timeout=timeout) as r:
            code=r.status
        return {'ok':True,'status':code,'ms':int((time.time()-started)*1000)}
    except Exception as e:
        return {'ok':False,'error':str(e),'ms':int((time.time()-started)*1000)}

def collect(targets):
    return {name:check(url) for name,url in targets.items()}