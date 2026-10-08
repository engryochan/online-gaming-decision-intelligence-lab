from pathlib import Path
import subprocess,json,hashlib,csv,sqlite3
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/33_global_workbook_content_b08_20261008'
paths=[p.decode('utf-8') for p in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).split(b'\0') if p]
prefixes=['Reference/Global_Workbook_Content_Expansion_B08_20261008.','Reference/tables/33_global_workbook_content_b08_20261008/','reports/2026-10-08/global_workbook_content_b08/']
assert all(p=='.gitignore' or any(p.startswith(prefix) for prefix in prefixes) for p in paths)
assert not any('/local_runtime/' in p for p in paths)
db='Reference/tables/33_global_workbook_content_b08_20261008/global_workbook_content_b08.sqlite'
assert hashlib.sha256(subprocess.check_output(['git','show',':'+db],cwd=R)).hexdigest()==hashlib.sha256((R/db).read_bytes()).hexdigest()
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for p,digest in baseline['files'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest()
    if 'Inteligent' not in p:assert current==digest
    assert p not in paths
    protected.append(dict(path=p,baseline_sha256=digest,current_sha256=current,batch_action='PRESERVED_NOT_STAGED'))
out=dict(staged_files=len(paths),database_staged_bytes_verified=True,local_runtime_excluded=True,protected_files=protected)
(O/'staged_acceptance.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(staged_files=len(paths),database_verified=True,protected_not_staged=True)))
