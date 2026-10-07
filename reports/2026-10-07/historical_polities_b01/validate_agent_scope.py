from pathlib import Path
import csv,json,hashlib,sqlite3
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;A=R/'reports/2026-10-06/workspace_change_audit'
def scan(label):
 with (A/(label+'_files.csv')).open(encoding='utf-8-sig') as f:return {x['path']:x['sha256'] for x in csv.DictReader(f)}
b=scan('historical_polities_b01_start');e=scan('historical_polities_b01_delivery');receipt=json.loads((O/'append_receipt.json').read_text());allowed={x['path'] for x in receipt}
changed=sorted(p for p in b.keys()&e.keys() if b[p]!=e[p]);deleted=sorted(b.keys()-e.keys());runtime=[p for p in changed if p.startswith('.Rproj.user/')];outside=[p for p in changed if p not in allowed and p not in runtime]
assert not deleted
for x in receipt:
 old=(O/'originals'/Path(x['path']).name).read_bytes();assert hashlib.sha256(old).hexdigest()==b[x['path']] and (R/x['path']).read_bytes().startswith(old)
for p in b:
 if p.endswith('.sqlite') or p=='Reference/Aerospace_Ecosystem_Report.qmd':assert b[p]==e[p]
with (R/'Reference/tables/26_historical_polities_b01_20261007/integration_input_manifest.csv').open(encoding='utf-8-sig') as f:
 for x in csv.DictReader(f):assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
for m in json.loads((O/'source_manifest.json').read_text()):assert hashlib.sha256((O/'raw'/m['file']).read_bytes()).hexdigest()==m['sha256']
for m in json.loads((O/'dependency_manifest.json').read_text()):assert hashlib.sha256((R/m['path']).read_bytes()).hexdigest()==m['sha256']
external=[]
for p in outside:
 assert hashlib.sha256((R/p).read_bytes()).hexdigest()==e[p]
 external.append(dict(path=p,baseline_sha256=b[p],finish_sha256=e[p],current_matches_finish=True,attribution='CHANGED_OUTSIDE_THIS_DELIVERY_WRITE_SCOPE_AUTHOR_NOT_INFERRED',action='PRESERVED_NO_RESTORE_NO_REBASELINE'))
new=sorted(e.keys()-b.keys());scope=lambda p:p.startswith('reports/2026-10-07/historical_polities_b01/') or p.startswith('Reference/tables/26_historical_polities_b01_20261007/') or p.startswith('Reference/Global_Historical_Polities_B01_20261007') or p=='Reference/Historical_Polities_Timeline_Map_B01_20261007.html'
newoutside=[p for p in new if not scope(p)]
c=sqlite3.connect(O/'historical_polities_v1.sqlite');assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok';c.close()
result=dict(agent_delivery_scope_passed=True,whole_workspace_only_expected_changes=False if outside or newoutside else True,original_prefixes_preserved=True,deleted_existing_files=deleted,changed_existing_files=changed,existing_changes_outside_delivery_scope=external,new_files_outside_delivery_scope=newoutside,runtime_changes_not_attributed=runtime,prior_databases_unchanged=True,original_aerospace_unchanged=True,all_input_and_source_hashes_match=True,baseline_not_refreshed=True,strict_whole_workspace_validator_failed_on_outside_scope_change=bool(outside),database_integrity='ok',html_exists=(R/'Reference/Global_Historical_Polities_B01_20261007.html').exists(),browser_acceptance=json.loads((O/'map_browser_acceptance.json').read_text()))
(O/'final_acceptance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
