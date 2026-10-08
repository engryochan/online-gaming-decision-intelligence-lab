from pathlib import Path
import sys
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/"Reference/tables/45_global_directory_content_b20_20261008"
sys.path.insert(0,str(O.parent/"global_directory_content_b05"));import intake
intake.O=O;intake.T=T
import intake,subprocess,json,hashlib
O,T,R=intake.O,intake.T,intake.R
paths=[p.decode('utf-8') for p in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).split(b'\0') if p]
allowed=['Reference/Global_Directory_Content_Expansion_B20_20261008.','Reference/tables/45_global_directory_content_b20_20261008/','reports/2026-10-08/global_directory_content_b20/']
assert all(p in ['.gitignore','.gitattributes'] or any(p.startswith(prefix) for prefix in allowed) for p in paths)
excluded={r['path'] for r in json.loads((O/'credential_scan.json').read_text())['candidates']}
assert not excluded.intersection(paths)
raw=[p for p in paths if p.endswith('.response')]
for p in raw:
    staged=subprocess.check_output(['git','show',':'+p],cwd=R)
    assert hashlib.sha256(staged).digest()==hashlib.sha256((R/p).read_bytes()).digest(),p
out=dict(staged_files=len(paths),staged_raw_bytes_verified=len(raw),excluded_credential_candidates=len(excluded),user_changes_not_staged=True)
(O/'staged_acceptance.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))
