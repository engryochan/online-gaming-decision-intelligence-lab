from pathlib import Path
import csv,json,hashlib,sqlite3
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;A=R/'reports/2026-10-06/workspace_change_audit'
def read(n):
 with (A/(n+'_files.csv')).open(encoding='utf-8-sig') as f:return {x['path']:x['sha256'] for x in csv.DictReader(f)}
b=read('listed_b05_start');e=read('listed_b05_finish');receipts=json.loads((O/'append_receipt.json').read_text(encoding='utf-8'));allowed={x['path'] for x in receipts}
deleted=sorted(b.keys()-e.keys());changed=sorted(p for p in b.keys()&e.keys() if b[p]!=e[p]);runtime=[p for p in changed if p.startswith('.Rproj.user/')];unexpected=[p for p in changed if p not in allowed and p not in runtime]
assert not deleted and not unexpected,(deleted,unexpected)
for x in receipts:
 old=(O/'originals'/Path(x['path']).name).read_bytes();assert hashlib.sha256(old).hexdigest()==b[x['path']] and (R/x['path']).read_bytes().startswith(old)
with (R/'Reference/tables/23_listed_universe_b05_20261007/integration_input_manifest.csv').open(encoding='utf-8-sig') as f:
 for x in csv.DictReader(f):assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
con=sqlite3.connect(O/'financial_universe_v2.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
result=dict(passed=True,original_prefixes_preserved=True,deleted_existing_files=deleted,changed_existing_files=changed,runtime_changes_not_attributed=runtime,prior_databases_unchanged=all(b[p]==e[p] for p in b if p.endswith('.sqlite')),original_aerospace_unchanged=b['Reference/Aerospace_Ecosystem_Report.qmd']==e['Reference/Aerospace_Ecosystem_Report.qmd'],html_exists=(R/'Reference/Global_Financial_Universe_B05_20261007.html').exists(),all_new_input_hashes_match=True,database_integrity='ok')
(O/'final_acceptance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
