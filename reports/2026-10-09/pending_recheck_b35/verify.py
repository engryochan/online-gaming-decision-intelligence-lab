from pathlib import Path
import json,csv,sqlite3,hashlib,subprocess
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/59_pending_recheck_b35_20261009'
b=json.loads((O/'baseline.json').read_text(encoding='utf-8'));s=json.loads((O/'validation_receipt.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in b['protected'].items())
assert not (R/'Untitled.qmd').exists()
con=sqlite3.connect(T/'pending_recheck_b35.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for name,n in s['sqlite_counts'].items():
    with (T/(name+'.csv')).open(encoding='utf-8-sig') as f:assert sum(1 for r in csv.DictReader(f))==n
    assert con.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0]==n
assert con.execute("SELECT COUNT(*) FROM registry_new_station_normalized_values WHERE missing_state='DOCUMENTATION_SOURCE_SENTINEL_CONFLICT_REVIEW' AND normalized_value=''").fetchone()[0]==125
con.close();assert not json.loads((O/'credential_scan.json').read_text())['candidates']
names=[n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z']).decode('utf-8').split('\0') if n]
allowed=lambda n:n=='.gitattributes' or n.startswith(('reports/2026-10-09/pending_recheck_b35/','Reference/tables/59_pending_recheck_b35_20261009/')) or n in ['Reference/Pending_Recheck_B35_20261009.qmd','Reference/Pending_Recheck_B35_20261009.html'] or n in [d+'/pending_recheck_b35_20261009.md' for d in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]
assert names and all(allowed(n) for n in names)
assert hashlib.sha256(subprocess.check_output(['git','show',':reports/2026-10-09/pending_recheck_b35/raw/gsod_readme.txt'])).hexdigest()==json.loads((O/'documentation_receipt.json').read_text())['sha256']
(O/'staged_acceptance.json').write_text(json.dumps(dict(staged_files=len(names),original_documents_preserved=len(b['protected']),csv_sql_counts=s['sqlite_counts'],suspect_values_withheld=125,raw_staged_bytes_verified=True,credential_candidates=0),indent=2)+'\n',encoding='utf-8')
print('PASS: protected documents, CSV/SQLite, suspect-value exclusion, credential scan and exact staging scope')
