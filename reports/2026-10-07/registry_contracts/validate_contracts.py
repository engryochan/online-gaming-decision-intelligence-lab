"""Independently check raw cells, country arithmetic, nulls and untouched baselines."""
from pathlib import Path
import csv,json,hashlib,sqlite3,re,collections,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
manifest=list(csv.DictReader((OUT/'source_manifest.csv').open(encoding='utf-8-sig')))
raw={};count=0
with sqlite3.connect((OUT/'global_registry_b04_query.sqlite').as_uri()+'?mode=ro',uri=True) as db:
    db.row_factory=sqlite3.Row
    assert db.execute('pragma integrity_check').fetchone()[0]=='ok';assert not db.execute('pragma foreign_key_check').fetchall()
    for m in manifest:
        p=ROOT/m['path'];assert sha(p.read_bytes())==m['sha256']
        with p.open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);rows=list(reader);header=reader.fieldnames
        table=p.stem;raw[table]=rows
        got=[dict(r) for r in db.execute('select * from '+table+' order by rowid')];assert rows==got,'Raw cells differ '+table
        assert len(rows)==int(m['rows']);count+=len(header)
    assert count==135
    orgs=raw['registry_global_organizations'];claims={r['entity_id']:r for r in raw['registry_global_claims']};assert len(claims)==371
    candidate_counts=collections.Counter();any_verified=collections.Counter();description_only=collections.Counter();country_relations=collections.Counter()
    for r in orgs:
        codes=set(x.strip() for x in re.split('[;,]',r['country_candidate_iso_alpha2']) if x.strip())
        for code in codes:
            candidate_counts[code]+=1
            if claims[r['entity_id']]['evidence_state']=='VERIFIED':
                any_verified[code]+=1
                if claims[r['entity_id']]['verification_scope']=='PUBLIC_DESCRIPTION_ONLY':description_only[code]+=1
    for r in raw['registry_country_entity_relations']:
        if r['evidence_state']=='VERIFIED':country_relations[r['iso_alpha2']]+=1
    coverage=list(db.execute('select * from v_country_evidence_coverage'));assert len(coverage)==249
    for r in coverage:
        c=r['iso_alpha2'];assert r['candidate_entity_count']==candidate_counts[c];assert r['candidate_any_scope_verified_count']==any_verified[c];assert r['candidate_public_description_only_count']==description_only[c];assert r['verified_country_relation_count']==country_relations[c]
    for r in raw['registry_country_technology_coverage']:
        c=r['iso_alpha2'];assert int(r['editorial_entity_candidate_count'])==candidate_counts[c];assert int(r['candidate_public_descriptions_verified'])==any_verified[c];assert int(r['country_relation_verified_count'])==country_relations[c]
    assert db.execute("select count(*) from v_claims_with_source where source_id='' and evidence_url is null").fetchone()[0]==7
    assert db.execute('select count(*) from v_neuro_bandwidth_missing').fetchone()[0]==16
    assert sum(candidate_counts.values())==341 and len(candidate_counts)==103
    assert len(db.execute('select * from v_metrics_with_context').fetchall())==17
    assert len(db.execute('select * from entity_country_candidates').fetchall())==341
contracts=list(csv.DictReader((OUT/'field_contracts.csv').open(encoding='utf-8-sig')))
assert {(r['table'],r['column']) for r in contracts}=={(t,k) for t,rows in raw.items() for k in rows[0]}
semantics=list(csv.DictReader((OUT/'field_semantics_v2.csv').open(encoding='utf-8-sig')));assert len(semantics)==1989 and sum(r['definition_status']=='UNRESOLVED' for r in semantics)==424
append=json.loads((OUT/'append_manifest.json').read_text(encoding='utf-8')) if (OUT/'append_manifest.json').exists() else []
allowed={m['path'] for m in append}
for m in append:
    b=(ROOT/m['path']).read_bytes();assert sha(b)==m['after_sha256'];assert sha(b[:m['before_bytes']])==m['before_sha256'];assert sha((ROOT/m['snapshot']).read_bytes())==m['before_sha256']
runtime=[];unchanged=0
for row in csv.DictReader((ROOT/'reports/2026-10-06/workspace_change_audit/registry_contracts_20261007_start_files.csv').open(encoding='utf-8-sig')):
    p=ROOT/row['path'];current=sha(p.read_bytes()) if p.exists() else ''
    if current==row['sha256']:unchanged+=1
    elif row['path'].startswith('.Rproj.user/'):runtime.append(row['path'])
    else:assert row['path'] in allowed,'Unexpected baseline change '+row['path']
receipt=dict(status='PASS',source_tables_checked=len(raw),raw_cells_roundtrip='ALL_EQUAL',field_contracts=count,iso_coverage_rows_checked=249,country_memberships_checked=341,scope_counts_checked=True,missing_source_claims_preserved=7,neuro_bandwidth_blanks_preserved=16,unresolved_remaining=424,baseline_files_unchanged=unchanged,runtime_changes=runtime,original_prefixes_preserved=len(append),owner_review='PENDING',external_verification='SCOPED_TO_TWO_IMAGERY_DEFINITIONS')
(OUT/'independent_validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False,indent=2))
