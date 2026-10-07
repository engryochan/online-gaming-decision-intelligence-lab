"""Consequential evidence/constraint checks on an in-memory copy, never source files."""
from pathlib import Path
import sqlite3,json,sys
sys.stdout.reconfigure(encoding='utf-8')
OUT=Path(__file__).resolve().parent
source=sqlite3.connect((OUT/'global_registry_b04_query.sqlite').as_uri()+'?mode=ro',uri=True)
memory=sqlite3.connect(':memory:');source.backup(memory);source.close();memory.execute('pragma foreign_keys=ON')
entity,code,claim=memory.execute("select b.entity_id,b.iso_alpha2,a.claim_id from entity_country_candidates b join registry_global_claims a using(entity_id) where a.evidence_state='VERIFIED' and a.verification_scope='PUBLIC_DESCRIPTION_ONLY' limit 1").fetchone()
def counts():return memory.execute('select candidate_any_scope_verified_count,candidate_public_description_only_count from v_country_evidence_coverage where iso_alpha2=?',(code,)).fetchone()
before=counts();memory.execute('savepoint evidence_case');memory.execute("update registry_global_claims set evidence_state='UNKNOWN' where claim_id=?",(claim,));after=counts();assert after==(before[0]-1,before[1]-1);memory.execute('rollback to evidence_case');memory.execute('release evidence_case');assert counts()==before
row=memory.execute('select * from registry_country_entity_relations limit 1').fetchone();unknown=list(row);unknown[0]='TEST_ONLY_UNKNOWN_RELATION';unknown[5]='UNKNOWN';relation_code=row[2]
before=memory.execute('select verified_country_relation_count from v_country_evidence_coverage where iso_alpha2=?',(relation_code,)).fetchone()[0]
memory.execute('savepoint relation_case');memory.execute('insert into registry_country_entity_relations values ('+','.join('?' for _ in row)+')',unknown)
assert memory.execute('select verified_country_relation_count from v_country_evidence_coverage where iso_alpha2=?',(relation_code,)).fetchone()[0]==before
memory.execute('rollback to relation_case');memory.execute('release relation_case')
blocked=False
try:memory.execute('insert into entity_country_candidates values (?,?,?,?)',(entity,'ZZ','TEST_ONLY','ZZ'))
except sqlite3.IntegrityError:blocked=True
assert blocked
assert memory.execute("select count(*) from v_claims_with_source where source_id='' and evidence_url is null").fetchone()[0]==7
receipt=dict(status='PASS',test_storage='IN_MEMORY_COPY_ONLY',checks=['VERIFIED to UNKNOWN removes claim from both scoped counts','UNKNOWN relation does not increase verified-country count','invalid ISO bridge rejected by foreign key','missing-source claims retained by left join'],source_files_modified=False)
(OUT/'control_checks.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(receipt,ensure_ascii=False))
