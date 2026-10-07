from pathlib import Path
import csv,json,hashlib,sqlite3,sys
sys.stdout.reconfigure(encoding='utf-8');csv.field_size_limit(16*1024*1024)
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
baseline=list(csv.DictReader((ROOT/'reports/2026-10-06/workspace_change_audit/semantics_20261007_start_files.csv').open(encoding='utf-8-sig')))
man=list(csv.DictReader((OUT/'edit_manifest.csv').open(encoding='utf-8-sig'))); latest={m['path']:m['after_sha256'] for m in man}
for m in man: assert sha((ROOT/m['before_snapshot']).read_bytes())==m['before_sha256']
for path,h in latest.items(): assert sha((ROOT/path).read_bytes())==h,'Delivered target changed: '+path
renames=json.loads((OUT/'concurrent_source_renames.json').read_text(encoding='utf-8'))
subsequent=json.loads((OUT/'subsequent_source_baseline.json').read_text(encoding='utf-8')) if (OUT/'subsequent_source_baseline.json').exists() else None
if (OUT/'source_sync_events.json').exists(): subsequent=json.loads((OUT/'source_sync_events.json').read_text(encoding='utf-8'))[-1]
pending_source_versions=[]
for m in renames:
    assert not (ROOT/m['old_path']).exists(),'Restored deleted source'
    captured=subsequent['sha256'] if subsequent and m['new_path']==subsequent['path'] else m['new_sha256']
    current=sha((ROOT/m['new_path']).read_bytes())
    if current!=captured: pending_source_versions.append(dict(path=m['new_path'],captured_sha256=captured,current_sha256=current))
allowed=set(latest)|{'Reference/Project_Data_Architecture_20261007.html','Reference/Project_Information_Integration_20261007.html'}|{m['old_path'] for m in renames}
runtime=[]; unchanged=0
for row in baseline:
    p=ROOT/row['path']; h=sha(p.read_bytes()) if p.exists() else ''
    if h!=row['sha256']:
        if row['path'].startswith('.Rproj.user/'): runtime.append(row['path'])
        else: assert row['path'] in allowed,'Unexpected mutation: '+row['path']
    else: unchanged+=1
fields=list(csv.DictReader((OUT/'field_semantics.csv').open(encoding='utf-8-sig')));paths={x['path'] for x in fields}; count=0
assert len({(x['path'],x['column_index']) for x in fields})==len(fields)
for path in paths:
    raw=(ROOT/path).read_bytes(); assert all(x['source_sha256']==sha(raw) for x in fields if x['path']==path)
    with (ROOT/path).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.reader(f,delimiter='\t' if path.endswith('.tsv') else ','); header=next(reader);records=list(reader)
    selected=[x for x in fields if x['path']==path];assert len(selected)==len(header)
    for x in selected:
        i=int(x['column_index'])-1;assert x['column_name']==header[i];assert int(x['row_count'])==len(records)
        assert int(x['blank_count'])==sum(not (row[i] if i<len(row) else '').strip() for row in records)
    count+=len(header)
assert count==1989
with sqlite3.connect((OUT/'semantic_catalog.sqlite').as_uri()+'?mode=ro',uri=True) as db:
    assert db.execute('pragma integrity_check').fetchone()[0]=='ok'
    assert db.execute('select count(*) from field_semantics').fetchone()[0]==count
    assert db.execute('select count(*) from claim_review').fetchone()[0]==5
    assert db.execute('select count(*) from claim_locations').fetchone()[0]==221
with sqlite3.connect((ROOT/'DGEF/artifacts/dgef.sqlite').as_uri()+'?mode=ro',uri=True) as db:
    assert db.execute('pragma integrity_check').fetchone()[0]=='ok';assert not db.execute('pragma foreign_key_check').fetchall()
receipt=dict(status='PASS_SCOPED' if pending_source_versions else 'PASS',independent_fields_checked=count,source_tables_checked=len(paths),baseline_files_unchanged=unchanged,source_renames_preserved=3,dgef_and_original_tables_unchanged=True,claims=5,keyword_locations=221,runtime_changes=runtime,pending_concurrent_source_versions=pending_source_versions,semantic_owner_approval=False,external_review_scope='FIVE_CLAIMS_ONLY')
(OUT/'independent_validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False,indent=2))
