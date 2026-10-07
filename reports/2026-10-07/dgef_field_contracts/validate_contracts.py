"""Independent source and catalogue preservation checks; writes only a receipt."""
from pathlib import Path
import csv,json,sqlite3,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
manifest=read(OUT/'source_manifest.csv')
for r in manifest:assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256']
old=read(ROOT/'reports/2026-10-07/registry_contracts/field_semantics_v2.csv');new=read(OUT/'field_semantics_v3.csv')
assert len(old)==len(new)==1989
changes=0
for a,b in zip(old,new):
    if a==b:continue
    assert a['role']=='DGEF_EXPORT' and a['definition_status']=='DOCUMENTED_GENERIC_REVIEW'
    assert b['definition_status']=='PROPOSED_TABLE_CONTRACT_REVIEW'
    assert set(k for k in a if a[k]!=b[k])=={'definition','definition_status','definition_locator'}
    changes+=1
assert changes==148
contracts=read(OUT/'field_contracts.csv')
with sqlite3.connect((ROOT/'DGEF/artifacts/dgef.sqlite').as_uri()+'?mode=ro',uri=True) as db:
    names=[r[0] for r in db.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
    expected={(t,c[1]):c for t in names for c in db.execute(f'pragma table_info("{t}")')}
    assert set(expected)=={(r['table'],r['column_name']) for r in contracts}
    assert len(contracts)==len(expected)==411
    for r in contracts:
        c=expected[r['table'],r['column_name']]
        assert (r['sql_type'],r['declared_not_null'],r['primary_key_position'])==(c[2],str(c[3]),str(c[5]))
        actual=[{'table':f[2],'column':f[4]} for f in db.execute(f'pragma foreign_key_list("{r["table"]}")') if f[3]==r['column_name']]
        assert json.loads(r['foreign_key_targets'])==actual
    assert db.execute('select count(*) from v_model_features_approved').fetchone()[0]==0
result=dict(pass_check=True,source_hashes_checked=len(manifest),all_sql_columns_checked=411,table_count=44,changed_definitions=changes,unchanged_semantic_records=1989-changes,unresolved=sum(r['definition_status']=='UNRESOLVED' for r in new),training_rows=0,business_approval='PENDING')
(OUT/'independent_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
