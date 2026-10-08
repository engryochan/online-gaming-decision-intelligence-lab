from pathlib import Path
import json,subprocess,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2];v=json.loads((O/'validation_receipt.json').read_text(encoding='utf-8'));allowed=set(v['delivery_files'])|{'.gitignore','reports/2026-10-08/downloads_essence_review/validation_receipt.json','reports/2026-10-08/downloads_essence_review/verify_staged.py'}
paths=[p.decode('utf-8') for p in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).split(b'\0') if p]
assert set(paths)<=allowed,sorted(set(paths)-allowed)
a=json.loads((O/'audit.json').read_text(encoding='utf-8'));sourcehash={r['sha256'] for r in a['files']}
for p in paths:
    staged=subprocess.check_output(['git','show',':'+p],cwd=R);working=(R/p).read_bytes()
    assert staged.replace(b'\r\n',b'\n')==working.replace(b'\r\n',b'\n'),p
    assert hashlib.sha256(staged).hexdigest() not in sourcehash,p
    assert not p.lower().endswith(('.zip','.rar','.iso','.sqlite','.xlsx')),p
print(json.dumps({'staged_files_verified':len(paths),'original_download_files_staged':0,'database_or_business_records_staged':0,'only_authorized_review_and_essence_changes':True}))
