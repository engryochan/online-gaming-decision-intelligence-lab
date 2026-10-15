"""Check generated HTML and copy existing local dependencies into delivery tree."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, shutil, re
from lxml import html

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
DELIVERY=OUT/'rendered'
results=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
missing=[]; copied=[]; checked=[]
for r in results:
    p=DELIVERY/Path(r['path']).with_suffix('.html')
    if not p.exists(): continue
    tree=html.fromstring(p.read_bytes())
    queue=[(p,s) for s in tree.xpath('//@src | //link/@href | //object/@data | //video/@poster')]
    seen=set()
    while queue:
        origin,ref=queue.pop()
        if not ref or ref in seen:continue
        seen.add(ref)
        parts=urlsplit(ref)
        if parts.scheme or parts.netloc or not parts.path or parts.path.startswith('/'):continue
        dest=(origin.parent/unquote(parts.path)).resolve()
        if not dest.is_relative_to(DELIVERY):
            missing.append(dict(document=r['path'],resource=ref,reason='outside_delivery_tree'));continue
        rel=dest.relative_to(DELIVERY)
        src=ROOT/rel
        if not dest.exists() and src.is_file():
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
            copied.append(rel.as_posix())
        if not dest.is_file():
            missing.append(dict(document=r['path'],resource=ref,reason='not_found'));continue
        if dest.suffix.lower()=='.css':
            queue.extend((dest,x.strip(' \"\'')) for x in re.findall(r'url\(([^)]+)\)',dest.read_text(encoding='utf-8',errors='replace')))
    checked.append(dict(path=r['path'],html=p.relative_to(OUT).as_posix(),
                        bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(OUT/'output_validation.json').write_text(json.dumps(dict(checked=checked,copied_dependencies=sorted(set(copied)),
    missing_dependencies=missing),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(checked=len(checked),copied=len(set(copied)),missing=len(missing))))
