"""Inventory the pre-existing scan boundary, not recursively generated outputs."""
from pathlib import Path
import csv,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new scan batch'
scan=ROOT/'reports/2026-10-06/workspace_change_audit/incremental_catalogue_20261007_start_files.csv'
old=ROOT/'reports/2026-10-07/historical_metadata_review/field_semantics_v12.csv'
old_rows=read(old);known={r['path']:r['source_sha256'] for r in old_rows}
inventory=read(scan);new=[r for r in inventory if Path(r['path']).suffix.lower() in {'.csv','.tsv'} and r['path'] not in known]
assert len(new)==71
assets=[];fields=[];manifests=[]
no_header={'reports/2026-10-07/dgef_field_contracts/proposed_definitions.tsv':['column_name','proposed_definition'],
           'reports/2026-10-07/reference_field_contracts/definitions.tsv':['table','column_name','definition','source_code_path']}
for item in new:
    rel=item['path'];p=ROOT/rel;digest=sha(p);assert digest==item['sha256']
    delimiter='\t' if p.suffix=='.tsv' else ','
    with p.open(encoding='utf-8-sig',newline='') as f:
        cells=list(csv.reader(f,delimiter=delimiter))
    assert cells
    mode='EXPLICIT_HEADERLESS_LAYOUT' if rel in no_header else 'FIRST_ROW_HEADER'
    header=no_header[rel] if rel in no_header else cells[0];data=cells if rel in no_header else cells[1:]
    assert len(set(header))==len(header)
    bad=sum(len(row)!=len(header) for row in data);assert not bad,rel
    name=p.name
    role='DERIVED_REVIEW_ARTIFACT'
    if name.startswith('field_semantics') or name in {'column_catalog.csv','remaining_unresolved.csv'}:role='SEMANTIC_CATALOGUE_OR_VERSION'
    elif name=='official_evidence_queue.csv':role='PENDING_EVIDENCE_QUEUE'
    elif name in {'entity_country_candidates.csv','metric_numeric_projection.csv','country_evidence_coverage.csv'}:role='DERIVED_QUERY_PROJECTION'
    elif name=='proposed_definitions.tsv' or name=='definitions.tsv':role='PROPOSED_DEFINITION_INPUT'
    elif name=='source_manifest.csv' or 'workspace_delta' in name or name=='edit_manifest.csv':role='PROVENANCE_RECEIPT'
    assets.append(dict(path=rel,role=role,rows=len(data),columns=len(header),layout_mode=mode,sha256=digest,classification_status='PROPOSED_ROLE_REVIEW',is_new_primary_business_dataset=False))
    for i,c in enumerate(header):
        fields.append(dict(path=rel,column_index=i+1,column_name=c,role=role,layout_mode=mode,row_count=len(data),blank_count=sum(row[i]=='' for row in data),definition_status='INCREMENTAL_FIELD_REVIEW_PENDING',definition='',source_sha256=digest,owner='UNASSIGNED'))
    manifests.append(dict(path=rel,sha256=digest))
drift=[]
for rel,digest in known.items():
    p=ROOT/rel;state='MISSING' if not p.exists() else 'MATCH' if sha(p)==digest else 'CONTENT_CHANGED'
    drift.append(dict(path=rel,catalogued_sha256=digest,current_sha256=sha(p) if p.exists() else '',state=state))
for m in manifests:assert sha(ROOT/m['path'])==m['sha256']
write('new_artifact_inventory.csv',assets);write('incremental_column_catalogue.csv',fields);write('source_manifest.csv',manifests);write('original_catalogue_source_drift.csv',drift)
result=dict(pass_check=True,scan_boundary=scan.relative_to(ROOT).as_posix(),scan_sha256=sha(scan),old_catalogue_sha256=sha(old),old_catalogue_files=len(known),new_files=len(assets),new_primary_business_datasets=0,incremental_columns=len(fields),incremental_definition_status='REVIEW_PENDING',source_drift=dict(collections.Counter(r['state'] for r in drift)),new_roles=dict(collections.Counter(r['role'] for r in assets)),source_unchanged=True,recursive_outputs_excluded=True)
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
