"""Independent catalogue delta, locator and source preservation checks."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
manifest=read(OUT/'source_manifest.csv')
for m in manifest:assert hashlib.sha256((ROOT/m['path']).read_bytes()).hexdigest()==m['sha256']
a=read(ROOT/'reports/2026-10-07/dgef_field_contracts/field_semantics_v3.csv');b=read(OUT/'field_semantics_v4.csv')
assert len(a)==len(b)==1989
changes=read(OUT/'definition_changes.csv');keys={(r['path'],r['column_name']) for r in changes};assert len(keys)==49
changed=0
for old,new in zip(a,b):
    if old==new:continue
    assert (old['path'],old['column_name']) in keys
    assert old['definition_status']=='UNRESOLVED' and old['role']=='REFERENCE_DATA'
    assert new['definition_status']=='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED'
    assert {k for k in old if old[k]!=new[k]}=={'definition','definition_status','definition_locator'}
    source,line=new['definition_locator'].rsplit(':',1)
    content=(ROOT/source).read_text(encoding='utf-8-sig').splitlines()[int(line)-1]
    assert new['column_name'] in content
    changed+=1
remaining=read(OUT/'remaining_unresolved.csv')
assert remaining==[r for r in b if r['definition_status']=='UNRESOLVED']
assert len(remaining)==375 and changed==49
assert sum(r['role']=='REFERENCE_DATA' for r in remaining)==111
result=dict(pass_check=True,definitions_added=changed,unchanged_records=1940,source_hashes_checked=len(manifest),unresolved=375,reference_unresolved=111,business_approval='PENDING',external_facts_reverified=False)
(OUT/'independent_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
