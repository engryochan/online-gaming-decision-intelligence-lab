"""Inventory and render all existing QMDs in an isolated workspace mirror."""
from pathlib import Path
import concurrent.futures as cf
import hashlib, json, os, re, shutil, subprocess, time

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
STAGE = OUT / 'staging'
RESULT = OUT / 'rendered'
PYTHON = __import__('sys').executable

def digest(p):
    h=hashlib.sha256()
    try:
        with p.open('rb') as f:
            for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
        return h.hexdigest()
    except OSError as e:
        return 'UNREADABLE:'+type(e).__name__

def inventory():
    rows = []
    for directory, dirs, files in os.walk(ROOT, followlinks=False):
        dirs[:] = [d for d in dirs if d != '.git' and not (Path(directory)/d).is_symlink()
                   and (Path(directory)/d) != OUT]
        for name in files:
            p = Path(directory)/name
            if not p.is_symlink():
                if p.suffix.lower() not in {'.qmd','.html','.js','.css','.scss','.yml','.yaml','.bib','.csl','.png','.jpg','.jpeg','.svg','.webp','.gif','.csv','.tex','.lua'}:
                    continue
                rows.append({'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                             'sha256': digest(p) if p.suffix.lower() != '.csv' else 'DEPENDENCY_METADATA_ONLY'})
    return rows

def main():
    OUT.mkdir(exist_ok=True, parents=True)
    baseline = OUT/'before.json'
    if baseline.exists():
        rows = json.loads(baseline.read_text(encoding='utf-8'))['files']
    else:
        rows = inventory()
        baseline.write_text(json.dumps({'head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'status': subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT,text=True),
            'files': rows}, ensure_ascii=False, indent=2),encoding='utf-8')
    late_path=OUT/'late_inputs.json'
    late=json.loads(late_path.read_text(encoding='utf-8')) if late_path.exists() else []
    known={r['path'] for r in rows}|{r['path'] for r in late}
    untracked=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=ROOT).decode('utf-8').split('\0'))
    for directory,dirs,files in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if d!='.git' and not (Path(directory)/d).is_symlink() and (Path(directory)/d)!=OUT]
        untracked.update((Path(directory)/name).relative_to(ROOT).as_posix() for name in files if name.lower().endswith('.qmd'))
    for rel in untracked:
        if rel and rel not in known and not rel.startswith(OUT.relative_to(ROOT).as_posix()+'/') and (ROOT/rel).is_file() and not (ROOT/rel).is_symlink():
            p=ROOT/rel
            late.append(dict(path=rel,bytes=p.stat().st_size,sha256=digest(p),
                             observed_on='2026-10-15',scope='Added during this task; separate from immutable before.json baseline'))
    late_path.write_text(json.dumps(late,ensure_ascii=False,indent=2),encoding='utf-8')
    combined=rows+[r for r in late if r['path'] not in {x['path'] for x in rows}]
    sources = [r for r in combined if r['path'].lower().endswith('.qmd')]
    # Copy resources too, preserving relative dependencies without touching originals.
    for r in combined:
        p = ROOT/r['path']
        if p.suffix.lower() in {'.qmd','.yml','.yaml','.css','.scss','.bib','.csl','.png','.jpg','.jpeg','.svg','.webp','.gif','.csv','.tex','.lua'}:
            dest = STAGE/r['path']
            dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists() or (dest.stat().st_size,dest.stat().st_mtime_ns)!=(p.stat().st_size,p.stat().st_mtime_ns): shutil.copy2(p,dest)
    (OUT/'logs').mkdir(exist_ok=True)
    prior=json.loads((OUT/'results.json').read_text(encoding='utf-8')) if (OUT/'results.json').exists() else []
    cached={r['path']:r for r in prior if r['exit_code']==0 and r['html_exists']
            and (RESULT/Path(r['path']).with_suffix('.html')).is_file()}
    def render(r):
        rel = r['path']; src = STAGE/rel
        if rel in cached and cached[rel]['source_sha256']==digest(ROOT/rel): return cached[rel]
        shutil.copy2(ROOT/rel,src)
        r=dict(r,sha256=digest(src))
        data = src.read_text(encoding='utf-8-sig')
        issues=[]
        if '\ufffd' in data: issues.append('replacement_character')
        if re.search(r'^(<<<<<<< |=======\s*$|>>>>>>> )',data,re.M): issues.append('possible_merge_marker')
        target = RESULT/Path(rel).parent
        target.mkdir(parents=True,exist_ok=True)
        start=time.monotonic()
        if len(str(src))>220:
            short=OUT/'jobs'/hashlib.sha256(rel.encode()).hexdigest()[:8]/Path(rel).name
            short.parent.mkdir(parents=True,exist_ok=True)
            short.write_bytes(src.read_bytes())
            src=short
        cmd=['quarto','render',str(src),'--to','html','--no-execute','--embed-resources=false',
             '--resource-path='+str((STAGE/rel).parent),'-M','engine:markdown']
        env=dict(os.environ,QUARTO_ESBUILD='C:/work/tools/bin/tools/x86_64/esbuild.exe')
        if re.search(r'recovery-kind: (lossless-html-snapshot|html-snapshot-with-markdown-appendix)',data[:2000]):
            raw=src.read_bytes()
            match=re.search(rb'(?m)^(`{3,})\{=html\}\r?\n',raw)
            if not match: raise ValueError('Missing HTML snapshot fence: '+rel)
            ending=re.search(rb'(?m)^'+re.escape(match[1])+rb'\r?$',raw[match.end():])
            if not ending: raise ValueError('Missing closing HTML snapshot fence: '+rel)
            end_start=match.end()+ending.start()
            payload=raw[match.end():end_start]
            if payload.endswith(b'\r\n'):payload=payload[:-2]
            elif payload.endswith(b'\n'):payload=payload[:-1]
            tail=raw[match.end()+ending.end():].strip()
            mode='lossless-html-snapshot'
            if tail:
                fragment=subprocess.run(['quarto','pandoc','--from','markdown','--to','html','--wrap=none'],
                    input=tail,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
                section=b'\n<section id="integrated-markdown-appendix">\n'+fragment+b'\n</section>\n'
                closing=list(re.finditer(rb'</body\s*>',payload,re.I))
                if closing:
                    at=closing[-1].start();payload=payload[:at]+section+payload[at:]
                else:payload+=section
                mode='html-snapshot-with-markdown-appendix'
            html=target/(Path(rel).stem+'.html')
            html.write_bytes(payload)
            return {'path':rel,'source_sha256':r['sha256'],'exit_code':0,'html_exists':True,
                    'seconds':0,'issues':issues,'renderer':mode,'warnings':[]}
        # Offline HTML delivery profile: only the disposable copy is changed.
        fm=re.match(r'\A---\r?\n.*?\r?\n---(?:\r?\n|$)',data,re.S)
        if fm:
            header=re.sub(r'(embed-resources:\s*)true',r'\1false',fm[0])
            src.write_text(header+data[fm.end():],encoding='utf-8',newline='')
        try:
            run=subprocess.run(cmd,cwd=src.parent,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240,env=env)
            log=run.stdout.decode('utf-8',errors='replace'); code=run.returncode
        except subprocess.TimeoutExpired as e:
            log=(e.stdout or b'').decode('utf-8',errors='replace')+'\nTIMEOUT';code=124
        logpath=OUT/'logs'/(hashlib.sha256(rel.encode()).hexdigest()[:16]+'.log')
        logpath.write_text(log,encoding='utf-8')
        html=target/(Path(rel).stem+'.html')
        produced=src.with_suffix('.html')
        if produced.exists(): shutil.copy2(produced,html)
        assets=src.parent/(src.stem+'_files')
        if assets.exists(): shutil.copytree(assets,target/assets.name,dirs_exist_ok=True)
        return {'path':rel,'source_sha256':r['sha256'],'exit_code':code,'html_exists':html.exists(),
                'seconds':round(time.monotonic()-start,1),'issues':issues,
                'log':logpath.relative_to(OUT).as_posix(),
                'warnings':[s[:1000] for s in log.splitlines() if 'WARN' in s or 'ERROR' in s]}
    results=[]
    with cf.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(render,sources):
            results.append(result)
            (OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
            if len(results)%50==0 or len(results)==len(sources) or cached.get(result['path'],{}).get('source_sha256')!=result['source_sha256']:
                print(json.dumps({'done':len(results),'total':len(sources),'path':result['path'],
                                  'code':result['exit_code'],'warnings':len(result['warnings'])},ensure_ascii=True),flush=True)
    after=inventory(); old={r['path']:r for r in rows};new={r['path']:r for r in after}
    delta=[{'path':p,'state':'added' if p not in old else 'deleted' if p not in new else 'modified'}
           for p in sorted(old.keys()|new.keys()) if p not in old or p not in new or old[p]['sha256']!=new[p]['sha256']]
    (OUT/'after_delta.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2),encoding='utf-8')
    print('COMPLETE',len(results),'FAILED',sum(r['exit_code']!=0 or not r['html_exists'] for r in results),flush=True)

if __name__=='__main__': main()
