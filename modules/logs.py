from pathlib import Path

def collect(root, relative_roots, max_files=10, max_bytes=2_000_000, tail_lines=8):
    root=Path(root); files=[]
    for rel in relative_roots:
        base=root/rel
        if not base.exists(): continue
        for p in base.rglob('*'):
            if p.is_file() and p.suffix.lower() in {'.json','.jsonl','.log'} and p.stat().st_size < max_bytes:
                files.append(p)
    out=[]
    for p in sorted(files,key=lambda x:x.stat().st_mtime,reverse=True)[:max_files]:
        try:
            lines=p.read_text(encoding='utf-8',errors='replace').splitlines()
            out.append({'path':str(p.relative_to(root)),'mtime':p.stat().st_mtime,'tail':'\n'.join(lines[-tail_lines:])[-3500:]})
        except Exception:
            pass
    return out