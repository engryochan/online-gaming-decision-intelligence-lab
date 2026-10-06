"""Inventory every regular workspace file, excluding Git internals and symlinks.
Only paths, metadata and hashes are recorded; no document or secret contents.
"""
from pathlib import Path
import argparse, csv, hashlib, json, os, subprocess
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
parser=argparse.ArgumentParser()
parser.add_argument('--label',default='current')
parser.add_argument('--base',default='4982fcc')
args=parser.parse_args()
assert args.label.replace('_','').isalnum()
def git(*a):
    return subprocess.check_output(['git',*a],cwd=ROOT).decode('utf-8',errors='replace')
tracked=set(filter(None,git('ls-files','-z').split('\0')))
rows=[]; skipped=[];references=[]
names=('Aerospace_Ecosystem_Report.qmd','Aerospace_Ecosystem_Report.md',
       'Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd')
def traversal_error(error):
    skipped.append({'path':str(Path(error.filename).relative_to(ROOT)), 'reason':type(error).__name__})
for directory, dirs, files in os.walk(ROOT,followlinks=False,onerror=traversal_error):
    dirs[:]=[d for d in dirs if d!='.git' and not (Path(directory)/d).is_symlink()]
    for name in files:
        p=Path(directory)/name
        rel=p.relative_to(ROOT).as_posix()
        # Exclude this scanner's changing receipts; its code remains inventoried.
        if p.parent==OUT and p.suffix in {'.csv','.json','.md'}:
            continue
        if p.is_symlink():
            skipped.append({'path':rel,'reason':'SYMLINK_NOT_FOLLOWED'});continue
        try:
            stat=p.stat();h=hashlib.sha256()
            with p.open('rb') as f:
                for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
            after=p.stat()
            rows.append(dict(path=rel,bytes=stat.st_size,mtime_ns=stat.st_mtime_ns,
                sha256=h.hexdigest(),tracked=rel in tracked,
                stable_during_scan=(stat.st_size,stat.st_mtime_ns)==(after.st_size,after.st_mtime_ns)))
            if p.suffix.lower() in {'.qmd','.md','.py','.json','.yml','.yaml','.toml'}:
                for line_no,line in enumerate(p.read_text(encoding='utf-8-sig',errors='replace').splitlines(),1):
                    for target in names:
                        if target in line:
                            references.append({'path':rel,'line':line_no,'target_name':target})
        except OSError as e:
            skipped.append({'path':rel,'reason':type(e).__name__})
rows.sort(key=lambda r:r['path'])
with (OUT/f'{args.label}_files.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (OUT/f'{args.label}_document_references.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['path','line','target_name']);w.writeheader();w.writerows(references)
changes=[]
tokens=git('diff','--name-status','--no-renames','-z',args.base,'HEAD').split('\0')
for i in range(0,len(tokens)-1,2):
    changes.append({'status':tokens[i],'path':tokens[i+1]})
with (OUT/f'{args.label}_committed_changes.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['status','path']);w.writeheader();w.writerows(changes)
previous=OUT/'before_files.csv'
delta=[]
if args.label!='before' and previous.exists():
    old={r['path']:r for r in csv.DictReader(previous.open(encoding='utf-8-sig'))}
    new={r['path']:r for r in rows}
    for path in sorted(old.keys()|new.keys()):
        state='ADDED' if path not in old else 'DELETED' if path not in new else 'MODIFIED' if old[path]['sha256']!=new[path]['sha256'] else ''
        if state:delta.append({'path':path,'status':state})
summary={'scanned_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
    'head':git('rev-parse','HEAD').strip(),'comparison_base':git('rev-parse',args.base).strip(),
    'regular_files_hashed':len(rows),'tracked_files_hashed':sum(r['tracked'] for r in rows),
    'bytes_hashed':sum(r['bytes'] for r in rows),'skipped':skipped,
    'unstable_files':[r['path'] for r in rows if not r['stable_during_scan']],
    'git_status_porcelain':git('status','--porcelain=v1','--untracked-files=all'),
    'committed_changed_paths':len(changes),'changed_since_before':delta,
    'scope':'All regular files including ignored files; .git internals and symlinks excluded. Audit receipts excluded to avoid self-reference.'}
(OUT/f'{args.label}_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['head','regular_files_hashed','tracked_files_hashed','bytes_hashed','committed_changed_paths','skipped','unstable_files']},ensure_ascii=False))
