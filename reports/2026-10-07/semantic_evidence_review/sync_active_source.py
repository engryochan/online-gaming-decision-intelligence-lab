"""Append an actively edited source version; never rewrite an accepted baseline."""
from pathlib import Path
import csv,json,hashlib,difflib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
events=json.loads((OUT/'source_sync_events.json').read_text(encoding='utf-8')) if (OUT/'source_sync_events.json').exists() else []
previous=events[-1] if events else json.loads((OUT/'subsequent_source_baseline.json').read_text(encoding='utf-8'))
path=previous['path'];raw=(ROOT/path).read_bytes();h=sha(raw)
if h==previous['sha256']: print('SOURCE_ALREADY_SYNCED');raise SystemExit(0)
old=(ROOT/previous['snapshot']).read_bytes().decode('utf-8-sig').splitlines(keepends=True);new=raw.decode('utf-8-sig').splitlines(keepends=True)
delta=''.join(''.join(new[k:l]) for op,i,j,k,l in difflib.SequenceMatcher(None,old,new,autojunk=False).get_opcodes() if op!='equal')
snapshot=OUT/'originals'/(h+'.md');snapshot.write_bytes(raw)
shown=re.sub(r'https?://[^\s<>\]\)]+',lambda m:m.group(0).split('?')[0]+'?[SIGNED_QUERY_REDACTED]' if re.search(r'(?i)(signature=|x-amz-|sig=|token=|credential=)',m.group(0)) else m.group(0),delta)
token='`'*(max([len(x) for x in re.findall(r'`+',shown)]+[2])+1)
man=list(csv.DictReader((OUT/'edit_manifest.csv').open(encoding='utf-8-sig')));latest={m['path']:m['after_sha256'] for m in man};updates={}
for target in [x for x in latest if 'Aerospace_Ecosystem_Report.qmd' in x or 'Geostrategy_Defense_' in x]:
    before=(ROOT/target).read_bytes();assert sha(before)==latest[target],'Target changed; refuse overwrite'
    copy=OUT/'originals'/(sha(before)+'.qmd');copy.write_bytes(before)
    note='\n## 來源續寫版本 '+h[:16]+'\n\n承接來源版本 '+previous['sha256'][:16]+'；本段為新增／替換文字，UNKNOWN_INHERITED。刪除或替換前的說法仍在歷史快照，當期完整源檔依雜湊另存；不把新增答覆自動核實。\n\n'+token+'text\n'+shown+'\n'+token+'\n'
    after=before+note.encode();updates[target]=after
    man.append(dict(path=target,before_sha256=sha(before),after_sha256=sha(after),before_snapshot=copy.relative_to(ROOT).as_posix(),untargeted_text_preserved=True))
assert sha((ROOT/path).read_bytes())==h,'Source changed while capturing; targets unchanged'
for target,data in updates.items():assert sha((ROOT/target).read_bytes())==latest[target]
for target,data in updates.items():(ROOT/target).write_bytes(data)
with (OUT/'edit_manifest.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(man[0]));w.writeheader();w.writerows(man)
event=dict(path=path,sha256=h,previous_sha256=previous['sha256'],snapshot=snapshot.relative_to(ROOT).as_posix(),delta_characters=len(delta),integrated_to_two_main_reports=True)
events.append(event);(OUT/'source_sync_events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(event,ensure_ascii=False))
