from pathlib import Path
import subprocess,json,hashlib,re
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/34_global_workbook_semantics_b09_20261008'
paths=[p.decode('utf-8') for p in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).split(b'\0') if p]
prefixes=['Reference/Global_Workbook_Semantics_Expansion_B09_20261008.','Reference/tables/34_global_workbook_semantics_b09_20261008/','reports/2026-10-08/global_workbook_semantics_b09/']
assert all(p=='.gitattributes' or any(p.startswith(prefix) for prefix in prefixes) for p in paths)
checks=[]
for path in [T/'global_workbook_semantics_b09.sqlite',T/'registry_source_business_records.csv']:
    relative=path.relative_to(R).as_posix();pointer=subprocess.check_output(['git','show',':'+relative],cwd=R).decode();sha=hashlib.sha256(path.read_bytes()).hexdigest()
    assert 'oid sha256:'+sha in pointer and 'size '+str(path.stat().st_size) in pointer
    checks.append(dict(path=relative,sha256=sha,bytes=path.stat().st_size,lfs_pointer_verified=True))
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for p,digest in baseline['protected'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest()
    if 'Inteligent' not in p:assert current==digest
    assert p not in paths;protected.append(dict(path=p,baseline_sha256=digest,current_sha256=current,batch_action='PRESERVED_NOT_STAGED'))
(O/'staged_acceptance.json').write_text(json.dumps(dict(staged_files=len(paths),lfs_checks=checks,protected_files=protected),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(staged_files=len(paths),lfs_pointers_verified=len(checks),user_changes_not_staged=True)))
