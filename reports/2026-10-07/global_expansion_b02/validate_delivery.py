from pathlib import Path
import csv,json,hashlib,sqlite3
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;A=R/'reports/2026-10-06/workspace_change_audit';T=R/'Reference/tables/27_global_expansion_b02_20261007';csv.field_size_limit(32*1024*1024)
def scan(label):
 with (A/(label+'_files.csv')).open(encoding='utf-8-sig') as f:return {x['path']:x['sha256'] for x in csv.DictReader(f)}
b=scan('global_expansion_b02_start');e=scan('global_expansion_b02_finish');receipt=json.loads((O/'append_receipt.json').read_text());allowed={x['path'] for x in receipt};changed=sorted(p for p in b.keys()&e.keys() if b[p]!=e[p]);deleted=sorted(b.keys()-e.keys());outside=[p for p in changed if p not in allowed and not p.startswith('.Rproj.user/')];assert not deleted
for x in receipt:
 old=(O/'originals'/Path(x['path']).name).read_bytes();assert hashlib.sha256(old).hexdigest()==b[x['path']] and (R/x['path']).read_bytes().startswith(old)
for p in b:
 if p.endswith('.sqlite') or p=='Reference/Aerospace_Ecosystem_Report.qmd':assert b[p]==e[p]
for m in json.loads((O/'source_manifest.json').read_text()):assert hashlib.sha256((O/'raw'/m['file']).read_bytes()).hexdigest()==m['sha256']
for m in json.loads((O/'dependency_manifest.json').read_text()):assert hashlib.sha256((R/m['path']).read_bytes()).hexdigest()==m['sha256']
with (T/'integration_input_manifest.csv').open(encoding='utf-8-sig') as f:
 for m in csv.DictReader(f):assert hashlib.sha256((R/m['path']).read_bytes()).hexdigest()==m['sha256']
c=sqlite3.connect(O/'global_universe_v5.sqlite');assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for p in T.glob('*.csv'):
 if p.name=='integration_input_manifest.csv':continue
 with p.open(encoding='utf-8-sig') as f:expected=list(csv.DictReader(f))
 actual=[json.loads(r[0]) for r in c.execute('SELECT fields_json FROM raw_records WHERE namespace=? AND source_table=? ORDER BY source_row',('GLOBAL_EXPANSION_B02',p.stem))];assert actual==expected,p.name
assert c.execute('SELECT COUNT(*) FROM listing_records').fetchone()[0]==47244 and c.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0]==185008;assert c.execute('SELECT COUNT(*) FROM historical_feature_snapshots').fetchone()[0]==13797;c.close()
result=dict(agent_delivery_scope_passed=True,whole_workspace_only_expected_changes=not outside,original_prefixes_preserved=True,deleted_existing_files=deleted,changed_existing_files=changed,changes_outside_delivery_scope=[dict(path=p,baseline_sha256=b[p],finish_sha256=e[p],attribution='NOT_IN_DELIVERY_WRITE_SCOPE_AUTHOR_NOT_INFERRED',action='PRESERVED') for p in outside],prior_databases_unchanged=True,original_aerospace_unchanged=True,all_dependency_and_input_hashes_match=True,all_new_csv_fields_roundtrip=True,database_integrity='ok',html_exists=(R/'Reference/Global_Universe_Expansion_B02_20261007.html').exists(),baseline_not_refreshed=True,global_complete=False)
(O/'final_acceptance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
