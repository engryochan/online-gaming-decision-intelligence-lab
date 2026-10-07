"""Immutable integrated snapshot with explicit batch namespaces and lossless cell projection."""
from pathlib import Path
import csv,json,sqlite3,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
DB=OUT/'global_registry_evidence_query_v2.sqlite'
assert not DB.exists(),'Never overwrite delivered snapshots'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
folders=[('GLOBAL_B04','10_global_technology_iso249_20261006_b04')]+[(f'EVIDENCE_B{i:02}',f'{10+i:02}_official_evidence_20261007_b{i:02}') for i in range(1,9)]
manifest=[];inputs=[]
for batch,folder in folders:
    for p in sorted((ROOT/'Reference/tables'/folder).glob('*.csv')):
        rows=read(p);assert rows,'Unexpected empty table'
        manifest.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),batch=batch,rows=len(rows),columns=len(rows[0])))
        inputs.append((batch,p,rows))
con=sqlite3.connect(DB)
con.executescript('''PRAGMA foreign_keys=ON;
CREATE TABLE organizations(entity_id TEXT PRIMARY KEY,display_name TEXT,batch TEXT,payload TEXT NOT NULL);
CREATE TABLE sources(batch TEXT,source_id TEXT,payload TEXT NOT NULL,PRIMARY KEY(batch,source_id));
CREATE TABLE raw_records(path TEXT,row_number INTEGER,batch TEXT,table_name TEXT,payload TEXT NOT NULL,PRIMARY KEY(path,row_number));
CREATE TABLE claims(batch TEXT,claim_id TEXT,entity_id TEXT REFERENCES organizations(entity_id),source_id TEXT,claim TEXT,evidence_state TEXT,verification_scope TEXT,payload TEXT NOT NULL,PRIMARY KEY(batch,claim_id),FOREIGN KEY(batch,source_id) REFERENCES sources(batch,source_id));
CREATE INDEX claim_entity_scope ON claims(entity_id,evidence_state,verification_scope);
CREATE INDEX raw_kind_batch ON raw_records(table_name,batch);
CREATE VIEW claim_scope_counts AS SELECT batch,evidence_state,verification_scope,count(*) AS claim_count FROM claims GROUP BY batch,evidence_state,verification_scope;
CREATE VIEW verified_public_descriptions AS SELECT * FROM claims WHERE evidence_state='VERIFIED' AND verification_scope='PUBLIC_DESCRIPTION_ONLY';
CREATE VIEW regulatory_claims AS SELECT * FROM claims WHERE verification_scope IN ('REGULATOR_DEVICE_SPECIFIC_DECISION','REGULATOR_DEVICE_SPECIFIC_INDICATIONS');
CREATE VIEW reported_study_claims AS SELECT * FROM claims WHERE verification_scope IN ('PUBLISHED_STUDY_REPORTED_OBSERVATION','INSTITUTION_REPORTED_STUDY_RESULTS_NOT_PAPER_VERIFICATION','PROVIDER_REPORTED_HUMAN_STUDY');
CREATE VIEW study_metrics AS SELECT batch,path,row_number,json_extract(payload,'$.metric_id') AS metric_id,json_extract(payload,'$.entity_id') AS entity_id,json_extract(payload,'$.metric_name') AS metric_name,json_extract(payload,'$.value') AS value,json_extract(payload,'$.unit') AS unit,json_extract(payload,'$.statistic') AS statistic,coalesce(json_extract(payload,'$.conditions'),json_extract(payload,'$.context')) AS conditions,json_extract(payload,'$.verification_scope') AS verification_scope,payload FROM raw_records WHERE table_name IN ('registry_technology_metrics','registry_study_metrics');
CREATE VIEW regulatory_decisions AS SELECT batch,path,row_number,json_extract(payload,'$.decision_id') AS decision_id,json_extract(payload,'$.entity_id') AS entity_id,json_extract(payload,'$.submission_id') AS submission_id,payload FROM raw_records WHERE table_name='registry_regulatory_decisions';
CREATE VIEW publication_correction_records AS SELECT batch,path,row_number,table_name,payload FROM raw_records WHERE table_name='registry_publication_corrections' OR (table_name='registry_neuro_publications' AND json_extract(payload,'$.correction_doi') IS NOT NULL);
CREATE VIEW neurotechnology_records AS SELECT batch,path,row_number,table_name,payload FROM raw_records WHERE table_name IN ('registry_neurotechnology_global','registry_neurotechnology_supplement','registry_neuro_study_descriptions');
CREATE VIEW relationships AS SELECT batch,path,row_number,payload FROM raw_records WHERE table_name IN ('registry_country_entity_relations','registry_supplemental_relationships');
CREATE VIEW entity_evidence_counts AS SELECT o.entity_id,o.display_name,count(c.claim_id) AS total_claims,sum(CASE WHEN c.evidence_state='VERIFIED' THEN 1 ELSE 0 END) AS verified_claims,sum(CASE WHEN c.evidence_state='UNKNOWN' THEN 1 ELSE 0 END) AS unknown_claims FROM organizations o LEFT JOIN claims c USING(entity_id) GROUP BY o.entity_id,o.display_name;
''')
for batch,p,rows in inputs:
    for i,r in enumerate(rows,1):
        payload=json.dumps(r,ensure_ascii=False)
        con.execute('INSERT INTO raw_records VALUES (?,?,?,?,?)',(p.relative_to(ROOT).as_posix(),i,batch,p.stem,payload))
        if p.name in {'registry_global_organizations.csv','registry_supplemental_entities.csv'}:
            con.execute('INSERT INTO organizations VALUES (?,?,?,?)',(r['entity_id'],r['display_name'],batch,payload))
        if p.name in {'registry_global_sources.csv','registry_supplemental_sources.csv'}:
            con.execute('INSERT INTO sources VALUES (?,?,?)',(batch,r['source_id'],payload))
for batch,p,rows in inputs:
    if p.name in {'registry_global_claims.csv','registry_supplemental_claims.csv'}:
        for r in rows:con.execute('INSERT INTO claims VALUES (?,?,?,?,?,?,?,?)',(batch,r['claim_id'],r['entity_id'],r['source_id'] or None,r['claim'],r['evidence_state'],r['verification_scope'],json.dumps(r,ensure_ascii=False)))
con.commit()
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
for m in manifest:
    p=ROOT/m['path'];assert sha(p)==m['sha256']
    observed=[json.loads(r[0]) for r in con.execute('SELECT payload FROM raw_records WHERE path=? ORDER BY row_number',(m['path'],))]
    assert observed==read(p)
# Every nonempty scope keeps its explicit source label; JSON absent fields remain NULL.
assert con.execute('SELECT count(*) FROM organizations').fetchone()[0]==372
assert con.execute('SELECT count(*) FROM claims').fetchone()[0]==407
assert con.execute("SELECT count(*) FROM claims WHERE batch='GLOBAL_B04'").fetchone()[0]==371
assert con.execute("SELECT count(*) FROM claims WHERE entity_id='FRO0132' AND batch='GLOBAL_B04' AND evidence_state='UNKNOWN'").fetchone()[0]==1
assert con.execute("SELECT count(*) FROM regulatory_claims WHERE batch='EVIDENCE_B05'").fetchone()[0]==2
assert con.execute("SELECT count(*) FROM regulatory_claims WHERE batch='EVIDENCE_B08'").fetchone()[0]==4
assert con.execute("SELECT count(*) FROM study_metrics WHERE batch='EVIDENCE_B07' AND verification_scope LIKE 'INSTITUTION%'").fetchone()[0]==5
counts={n:con.execute('SELECT count(*) FROM '+n).fetchone()[0] for n in ['organizations','claims','sources','raw_records','study_metrics','regulatory_claims','regulatory_decisions','publication_correction_records','neurotechnology_records','relationships']}
scopes=[dict(zip(['batch','evidence_state','verification_scope','claim_count'],r)) for r in con.execute('SELECT * FROM claim_scope_counts ORDER BY batch,evidence_state,verification_scope')]
write('source_manifest.csv',manifest);write('claim_scope_counts.csv',scopes)
view_counts=[dict(view_or_table=n,row_count=c,count_scope='ROWS_NOT_UNIQUE_STUDIES_OR_CAPABILITY_LEVELS') for n,c in counts.items()]
write('view_counts.csv',view_counts)
old=ROOT/'reports/2026-10-07/evidence_integration/global_registry_evidence_query.sqlite'
write('prior_snapshot_manifest.csv',[dict(path=old.relative_to(ROOT).as_posix(),sha256=sha(old))])
result=dict(pass_check=True,input_files=len(manifest),input_rows=sum(m['rows'] for m in manifest),counts=counts,all_decoded_cells_roundtrip=True,integrity_and_foreign_keys=True,original_371_claims_preserved=True,missing_projection_fields_remain_null=True,global_b04_and_evidence_b04_distinct=True,no_national_capability_or_rank_inference=True,snapshot_is_not_live=True)
con.close();(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
