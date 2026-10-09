from pathlib import Path
import json,csv,hashlib,subprocess
O=Path(__file__).resolve().parent;R=O.parents[2]
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in json.loads((O/'baseline.json').read_text(encoding='utf-8'))['protected'].items())
assert not json.loads((O/'credential_scan.json').read_text())['candidates']
names=[n for n in subprocess.check_output(['git','diff','--cached','--name-only','-z']).decode().split('\0') if n]
allowed=lambda n:n=='.gitattributes' or n.startswith(('reports/2026-10-09/ssod_schema_b38/','Reference/tables/62_ssod_schema_b38_20261009/')) or n in ['Reference/SSOD_Schema_B38_20261009.qmd','Reference/SSOD_Schema_B38_20261009.html'] or n in [d+'/ssod_schema_b38_20261009.md' for d in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]
assert names and all(allowed(n) for n in names)
for r in csv.DictReader((R/'Reference/tables/62_ssod_schema_b38_20261009/registry_source_receipts.csv').open(encoding='utf-8-sig')):
    if r['file']:assert hashlib.sha256(subprocess.check_output(['git','show',':'+r['file']])).hexdigest()==r['sha256']
(O/'staged_acceptance.json').write_text(json.dumps(dict(staged_files=len(names),protected_hashes_unchanged=True,raw_staged_bytes_verified=True,credential_candidates=0),indent=2)+'\n',encoding='utf-8')
print('PASS: protected documents, staging scope, raw bytes and credential scan')
