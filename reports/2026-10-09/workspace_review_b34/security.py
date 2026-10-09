from pathlib import Path
import sys,json,hashlib,subprocess
O=Path(__file__).resolve().parent;R=O.parents[2];T=O
sys.path.insert(0,str(R/'reports/2026-10-08/global_directory_content_b05'))
import intake
intake.O=O;intake.T=T
s=(R/'reports/2026-10-08/global_directory_content_b05/security.py').read_text(encoding='utf-8')
s=s[:s.index('for root in [O,T]:')]
exec(compile(s,str(O/'security.py'),'exec'))
paths=list(O.glob('*'))+list((R/'reports/2026-10-06/workspace_change_audit').glob('review_b34_20261009*'))+[R/'Reference/Workspace_Review_B34_20261009.qmd',R/'Reference/Workspace_Review_B34_20261009.html']+[R/n/'workspace_review_b34_20261009.md' for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]
for p in paths:
    if p.is_file() and p.name!='credential_scan.json':scan(p.read_bytes(),p.relative_to(R).as_posix())
assert not findings,'Credential candidate: hold publication'
(O/'credential_scan.json').write_text(json.dumps(dict(objects_scanned=scanned,candidates=findings,values_disclosed=False),indent=2)+'\n',encoding='utf-8')
receipt=json.loads((O/'validation_receipt.json').read_text(encoding='utf-8'))
for row in receipt['protected_comparison']:
    p=R/row['path']
    if row['sha256_current']:assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256_current']
    else:assert not p.exists()
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==receipt['head']
print('PASS: publication candidates scan and current user-file baseline')
