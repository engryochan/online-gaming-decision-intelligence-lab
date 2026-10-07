"""Contextual definitions from existing generators; no source generator execution."""
from pathlib import Path
import csv,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new batch for revisions'
old=ROOT/'reports/2026-10-07/dgef_field_contracts/field_semantics_v3.csv'
rows=read(old);manifest={old:sha(old)};definitions={}
for line in (OUT/'definitions.tsv').read_text(encoding='utf-8').splitlines():
    table,column,definition,source=line.split('\t');source=source.strip();p=ROOT/source
    manifest[p]=sha(p);lines=p.read_text(encoding='utf-8-sig').splitlines()
    matches=[i+1 for i,l in enumerate(lines) if column in l]
    assert matches,(table,column)
    assert (table,column) not in definitions
    definitions[table,column]=(definition,source+':'+str(matches[0]))
changes=[];used=set()
for r in rows:
    key=r['table'],r['column_name']
    if r['role']!='REFERENCE_DATA' or r['definition_status']!='UNRESOLVED' or key not in definitions:continue
    p=ROOT/r['path'];manifest[p]=sha(p);assert sha(p)==r['source_sha256'],r['path']
    data=read(p);assert len(data)==int(r['row_count'])
    old_definition=r['definition'];definition,locator=definitions[key]
    r['definition']=definition;r['definition_status']='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED';r['definition_locator']=locator
    changes.append(dict(path=r['path'],table=r['table'],column_name=r['column_name'],previous_definition=old_definition,definition=definition,definition_locator=locator,row_count=r['row_count'],blank_count=r['blank_count'],source_sha256=r['source_sha256'],business_approval='PENDING',business_value='支持正確解讀歷史批次與查詢口徑；非已測 ROI',fact_reverification='NOT_PERFORMED_IN_THIS_BATCH'))
    used.add(key)
assert used==set(definitions),set(definitions)-used
assert len(changes)==49
for p,h in manifest.items():assert sha(p)==h
write('field_semantics_v4.csv',rows);write('definition_changes.csv',changes)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in manifest.items()])
unresolved=[r for r in rows if r['definition_status']=='UNRESOLVED']
write('remaining_unresolved.csv',unresolved)
result=dict(records=len(rows),definitions_added=len(changes),tables=len({r['table'] for r in changes}),unresolved_before=424,unresolved_after=len(unresolved),reference_unresolved_after=sum(r['role']=='REFERENCE_DATA' for r in unresolved),source_files_unchanged=len(manifest),status_counts=dict(collections.Counter(r['definition_status'] for r in rows)),business_approval='PENDING',source_fact_reverification=False)
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
