"""Render failed large documents with short paths and static code presentation."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,time
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
BASE=ROOT/'_qr_20261015'
BASE.mkdir(exist_ok=True)
(BASE/'.gitignore').write_text('*\n',encoding='utf-8')
rows=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
for r in rows:
    if r['exit_code']==0 and r['html_exists']:continue
    key=hashlib.sha256(r['path'].encode()).hexdigest()[:8]
    src=BASE/key/(key+'.qmd');src.parent.mkdir(exist_ok=True)
    data=(ROOT/r['path']).read_bytes();s=data.decode('utf-8-sig')
    fm=re.match(r'\A---\r?\n.*?\r?\n---',s,re.S)
    assert fm
    header=re.sub(r'((?:embed-resources|code-fold|code-tools):\s*)true',r'\1false',fm[0])
    src.write_text(header+s[fm.end():],encoding='utf-8')
    started=time.monotonic()
    run=subprocess.run(['quarto','render',str(src),'--to','html','--no-execute','-M','engine:markdown',
        '--syntax-highlighting=none','--resource-path='+str((ROOT/r['path']).parent)],
        cwd=src.parent,env=dict(os.environ,QUARTO_ESBUILD='C:/work/tools/bin/tools/x86_64/esbuild.exe'),
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
    log=run.stdout.decode('utf-8',errors='replace');logrel='logs/'+key+'_static_retry.log'
    (OUT/logrel).write_text(log,encoding='utf-8')
    target=OUT/'rendered'/Path(r['path']).with_suffix('.html')
    if run.returncode==0:
        target.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(src.with_suffix('.html'),target)
        assets=src.parent/(key+'_files')
        if assets.exists():shutil.copytree(assets,target.parent/assets.name,dirs_exist_ok=True)
    r.update(exit_code=run.returncode,html_exists=target.exists(),source_sha256=hashlib.sha256(data).hexdigest(),
        log=logrel,seconds=round(time.monotonic()-started,1),renderer='Quarto HTML; short path; static code; no syntax highlighting',
        warnings=[line for line in log.splitlines() if 'WARN' in line or 'ERROR' in line])
    (OUT/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(path=r['path'],exit_code=r['exit_code']),ensure_ascii=True),flush=True)
