"""Read-only source audit; hypothetical mutations exist only in memory."""
from pathlib import Path
import sqlite3, hashlib, json, csv

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'DGEF/artifacts/dgef.sqlite'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

before = digest(SOURCE)
source = sqlite3.connect(SOURCE.as_uri() + '?mode=ro', uri=True)
source.row_factory = sqlite3.Row
assert source.execute('pragma integrity_check').fetchone()[0] == 'ok'
assert not source.execute('pragma foreign_key_check').fetchall()
tables = [r[0] for r in source.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%' order by name")]
counts = {t: source.execute(f'select count(*) from "{t}"').fetchone()[0] for t in tables}
actual = source.execute('select count(*) from v_model_features_approved').fetchone()[0]
obs = dict(source.execute('select * from registry_observation order by observation_id limit 1').fetchone())
policy = source.execute('select policy_id from registry_source where source_id=?', (obs['source_id'],)).fetchone()[0]
tests = []
cases = [
    ('known_zero', 'observation', 'value', 0.0, True),
    ('null_value', 'observation', 'value', None, False),
    ('empty_method', 'observation', 'method_id', '', False),
    ('whitespace_method', 'observation', 'method_id', '   ', False),
    ('lowercase_unknown_method', 'observation', 'method_id', 'unknown', False),
    ('padded_unknown_method', 'observation', 'method_id', ' UNKNOWN ', False),
    ('empty_unit', 'observation', 'unit', '', False),
    ('unknown_claim', 'claim', 'claim_status', 'UNKNOWN', False),
    ('unknown_claim_evidence', 'claim', 'evidence_state', 'UNKNOWN', False),
    ('simulation_entity', 'entity', 'world_domain', 'SIM', False),
    ('restricted_source', 'source', 'access_class', 'RESTRICTED', False),
    ('unknown_training_license', 'license_policy', 'ml_training_allowed', None, False),
]
# A review query, not an authorization mechanism or production replacement.
review_sql = '''SELECT o.observation_id FROM registry_observation o
 JOIN registry_entity e USING(entity_id)
 JOIN registry_source s ON s.source_id=o.source_id
 JOIN registry_license_policy p ON p.policy_id=s.policy_id
 JOIN registry_claim c ON c.claim_id=o.claim_id
 WHERE e.world_domain='REAL-TWIN' AND o.evidence_state IN ('VERIFIED','OBSERVED')
 AND o.value IS NOT NULL AND trim(o.unit)<>''
 AND trim(o.method_id)<>'' AND upper(trim(o.method_id))<>'UNKNOWN'
 AND p.ml_training_allowed=1 AND s.access_class='PUBLIC'
 AND c.claim_status IN ('VERIFIED','OBSERVED')
 AND c.evidence_state IN ('VERIFIED','OBSERVED')
 AND c.subject_entity_id=o.entity_id AND c.source_id=o.source_id
 AND o.observation_id=?'''
for name, table, column, value, expected in cases:
    db = sqlite3.connect(':memory:')
    source.backup(db)
    db.execute('pragma foreign_keys=on')
    # Explicit hypothetical permission; never persisted to the source or outputs.
    db.execute('update registry_license_policy set ml_training_allowed=1 where policy_id=?', (policy,))
    key = {'observation': ('observation_id', obs['observation_id']),
           'claim': ('claim_id', obs['claim_id']),
           'entity': ('entity_id', obs['entity_id']),
           'source': ('source_id', obs['source_id']),
           'license_policy': ('policy_id', policy)}[table]
    db.execute(f'update registry_{table} set {column}=? where {key[0]}=?', (value, key[1]))
    legacy = bool(db.execute('select 1 from v_model_features_approved where observation_id=?', (obs['observation_id'],)).fetchone())
    reviewed = bool(db.execute(review_sql, (obs['observation_id'],)).fetchone())
    assert reviewed == expected, name
    tests.append(dict(case=name, legacy_selected=legacy, review_selected=reviewed, expected_review=expected, pass_check=True))
    db.close()
source.close()
assert digest(SOURCE) == before
(OUT/'review_candidate.sql').write_text('-- Read-only candidate filter; not training authorization. Bind observation_id.\n'+review_sql+';\n', encoding='utf-8')
with (OUT/'control_tests.csv').open('w', encoding='utf-8-sig', newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(tests[0])); w.writeheader(); w.writerows(tests)
result = dict(source_path=str(SOURCE.relative_to(ROOT)), source_sha256=before,
              source_unchanged=True, tables=counts, current_training_rows=actual,
              hypothetical_controls=tests, review_is_training_authorization=False)
(OUT/'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(dict(tables=len(tables), observations=counts['registry_observation'], current_training_rows=actual,
                     controls=len(tests), legacy_gaps=sum(t['legacy_selected'] and not t['expected_review'] for t in tests), source_unchanged=True)))
