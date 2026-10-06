from pathlib import Path
import csv,json
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent/'workspace_change_audit'
def read(name):
    with (AUDIT/name).open(encoding='utf-8-sig',newline='') as f:return {r['path']:r for r in csv.DictReader(f)}
before=read('global_b03_start_files.csv');after=read('global_b03_finish_files.csv')
rows=[]
for p in sorted(before.keys()|after.keys()):
    state='ADDED' if p not in before else 'REMOVED' if p not in after else 'MODIFIED' if before[p]['sha256']!=after[p]['sha256'] else ''
    if state:rows.append(dict(path=p,state=state,category='UNTRACKED_RUNTIME_CHANGE_CAUSE_UNKNOWN' if p.startswith('.Rproj.user/') else 'B03_DELIVERY',before_sha256=before.get(p,{}).get('sha256',''),after_sha256=after.get(p,{}).get('sha256','')))
with (HERE/'workspace_delta.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['path','state','category','before_sha256','after_sha256']);w.writeheader();w.writerows(rows)
print(json.dumps({'added':sum(r['state']=='ADDED' for r in rows),'modified':sum(r['state']=='MODIFIED' for r in rows),'removed_runtime':sum(r['state']=='REMOVED' and r['category'].startswith('UNTRACKED') for r in rows)}))
