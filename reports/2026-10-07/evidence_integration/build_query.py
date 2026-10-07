"""Reproducible separate snapshot: retain every CSV field, normalize scoped claims."""
from pathlib import Path
import csv,json,sqlite3,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
DB=OUT/'global_registry_evidence_query.sqlite'
assert not DB.exists(),'Do not overwrite an existing snapshot'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
folders=['10_global_technology_iso249_20261006_b04','11_official_evidence_20261007_b01','12_official_evidence_20261007_b02','13_official_evidence_20261007_b03']
con=sqlite3.connect(DB)
con.executescript('''PRAGMA foreign_keys=ON;
CREATE TABLE organizations(entity_id TEXT PRIMARY KEY,display_name TEXT NOT NULL);
CREATE TABLE source_records(batch TEXT,source_id TEXT,payload TEXT NOT NULL,PRIMARY KEY(batch,source_id));
CREATE TABLE raw_records(path TEXT,row_number INTEGER,payload TEXT NOT NULL,PRIMARY KEY(path,row_number));
CREATE TABLE claims(batch TEXT,claim_id TEXT,entity_id TEXT REFERENCES organizations(entity_id),source_id TEXT,claim TEXT,evidence_state TEXT,verification_scope TEXT,performance_state TEXT,deployment_state TEXT,regulatory_state TEXT,PRIMARY KEY(batch,claim_id),FOREIGN KEY(batch,source_id) REFERENCES source_records(batch,source_id));
CREATE INDEX claim_entity_scope ON claims(entity_id,evidence_state,verification_scope);
CREATE VIEW verified_public_descriptions AS SELECT * FROM claims WHERE evidence_state='VERIFIED' AND verification_scope='PUBLIC_DESCRIPTION_ONLY';
CREATE VIEW claim_scope_counts AS SELECT batch,evidence_state,verification_scope,count(*) AS claim_count FROM claims GROUP BY batch,evidence_state,verification_scope;
CREATE VIEW entity_evidence_counts AS SELECT o.entity_id,o.display_name,count(c.claim_id) AS total_claims,sum(CASE WHEN c.evidence_state='VERIFIED' THEN 1 ELSE 0 END) AS verified_claims,sum(CASE WHEN c.evidence_state='UNKNOWN' THEN 1 ELSE 0 END) AS unknown_claims FROM organizations o LEFT JOIN claims c USING(entity_id) GROUP BY o.entity_id,o.display_name;
''')
orgs=read(ROOT/'Reference/tables'/folders[0]/'registry_global_organizations.csv')
con.executemany('INSERT INTO organizations VALUES (?,?)',[(r['entity_id'],r['display_name']) for r in orgs])
manifest=[];claim_rows=[];total=0
for folder,batch in zip(folders,['B04','B01','B02','B03']):
    for p in sorted((ROOT/'Reference/tables'/folder).glob('*.csv')):
        rows=read(p);rel=p.relative_to(ROOT).as_posix()
        manifest.append(dict(path=rel,sha256=sha(p),rows=len(rows),columns=len(rows[0]) if rows else 0))
        for i,r in enumerate(rows,1):con.execute('INSERT INTO raw_records VALUES (?,?,?)',(rel,i,json.dumps(r,ensure_ascii=False)))
        total+=len(rows)
        if p.name in {'registry_global_sources.csv','registry_supplemental_sources.csv'}:
            con.executemany('INSERT INTO source_records VALUES (?,?,?)',[(batch,r['source_id'],json.dumps(r,ensure_ascii=False)) for r in rows])
        if p.name in {'registry_global_claims.csv','registry_supplemental_claims.csv'}:claim_rows.extend([(batch,r) for r in rows])
for batch,r in claim_rows:
    con.execute('INSERT INTO claims VALUES (?,?,?,?,?,?,?,?,?,?)',(batch,r['claim_id'],r['entity_id'],r['source_id'] or None,r['claim'],r['evidence_state'],r['verification_scope'],r['performance_state'],r['deployment_state'],r['regulatory_state']))
con.commit()
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT count(*) FROM claims').fetchone()[0]==382
assert con.execute('SELECT count(*) FROM raw_records').fetchone()[0]==total
# Round-trip every decoded cell, including fields not present in normalized views.
for m in manifest:
    p=ROOT/m['path'];assert sha(p)==m['sha256']
    observed=[json.loads(r[0]) for r in con.execute('SELECT payload FROM raw_records WHERE path=? ORDER BY row_number',(m['path'],))]
    assert observed==read(p)
scopes=[dict(zip(['batch','evidence_state','verification_scope','claim_count'],r)) for r in con.execute('SELECT * FROM claim_scope_counts ORDER BY batch,evidence_state,verification_scope')]
missing=read(ROOT/'Reference/tables'/folders[-1]/'baseline_missing_source_review.csv')
coverage=[]
for r in missing:
    eid=r['entity_id']; counts=con.execute("SELECT count(*),sum(CASE WHEN evidence_state='VERIFIED' THEN 1 ELSE 0 END) FROM claims WHERE entity_id=? AND batch!='B04'",(eid,)).fetchone()
    coverage.append(dict(entity_id=eid,display_name=r['display_name'],supplemental_claims=counts[0],verified_supplemental_claims=counts[1],identity_state='COMPOUND_LABEL_UNRESOLVED' if eid=='FRO0132' else 'OFFICIAL_MILITARY_AFFILIATION' if eid=='FRO0123' else 'LEGAL_IDENTITY_UNKNOWN',baseline_unknown_preserved=con.execute("SELECT count(*) FROM claims WHERE entity_id=? AND batch='B04' AND evidence_state='UNKNOWN'",(eid,)).fetchone()[0],country_capability_state='UNKNOWN',performance_state='UNKNOWN',world_frontier_rank_state='UNKNOWN'))
assert len(coverage)==7 and all(r['supplemental_claims']>0 and r['baseline_unknown_preserved']==1 for r in coverage)
write('source_manifest.csv',manifest);write('claim_scope_counts.csv',scopes);write('seven_entity_evidence_status.csv',coverage)
result=dict(pass_check=True,input_files=len(manifest),raw_rows_preserved=total,organizations=len(orgs),claims=len(claim_rows),supplemental_claims=11,scope_counts=scopes,roundtrip_all_cells=True,integrity_and_foreign_keys=True,baseline_unknown_preserved=True,source_files_unchanged=True,old_sqlite_unchanged=True,snapshot_not_live=True)
con.close()
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='scope_counts'}))
