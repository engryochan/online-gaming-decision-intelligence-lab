"""Guarded additive integration of a source appearing after the immutable start scan."""
from pathlib import Path
import csv, hashlib, json, re, sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
source='Reference/OpenSource_Ecosystem_Monetization_Blueprint_20261006.md'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(name): return list(csv.DictReader((OUT/name).open(encoding='utf-8-sig')))
def save(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
raw=(ROOT/source).read_bytes(); digest=sha(raw); s=raw.decode('utf-8-sig')
manifest=load('source_manifest.csv'); ledger=load('block_coverage.csv'); assets=load('asset_catalog.csv')
if any(m['path']==source for m in manifest): raise SystemExit('Already applied')
plan=json.loads((OUT/'delivery_plan.json').read_text(encoding='utf-8'))
parts=[]; buf=[]; start=1; fence=None
for n,line in enumerate(s.splitlines(keepends=True),1):
    if not buf: start=n
    buf.append(line); m=re.match(r'^\s*(`{3,}|~{3,})',line)
    if m:
        token=m.group(1)
        if fence is None: fence=token
        elif token[0]==fence[0] and len(token)>=len(fence): fence=None
    if not line.strip() and fence is None: parts.append((start,''.join(buf))); buf=[]
if buf: parts.append((start,''.join(buf)))
assert ''.join(b for _,b in parts)==s
snapshot=OUT/'originals'/(digest+'.md'); snapshot.write_bytes(raw)
updates={}
for target,meta in plan['families'].items():
    if not (target.startswith('Reference/Aerospace_') or target.startswith('Reference/Geostrategy_')): continue
    current=(ROOT/target).read_bytes()
    if sha(current)!=meta['output_sha256']: raise SystemExit('Target changed; stop '+target)
    family='aerospace' if 'Aerospace_Ecosystem' in target else 'geostrategy'
    text=current.decode('utf-8'); annex='\n### 起始基線後新增來源：商業化藍圖\n\n2026-10-07 收尾發現；來源 [OpenSource_Ecosystem_Monetization_Blueprint_20261006.md](OpenSource_Ecosystem_Monetization_Blueprint_20261006.md)。此為方案與收益假設，引用、授權與規則尚待逐項核實。原始快照 SHA256：`'+digest+'`。\n'; count=0
    for n,b in parts:
        covered=b in text; h=sha(b.encode())
        if not covered:
            token='`'*(max([len(x) for x in re.findall(r'`+',b)]+[2])+1)
            annex+='\n::: {.callout-note collapse="true"}\n來源第 '+str(n)+' 行；段落 '+h[:16]+'；UNKNOWN_INHERITED。\n\n'+token+'text\n'+b+('' if b.endswith('\n') else '\n')+token+'\n::: \n'; count+=1
        ledger.append(dict(family=family,source=source,source_line=n,block_sha256=h,characters=len(b),state='ALREADY_COVERED' if covered else 'APPENDED_SOURCE_BLOCK',target=target,source_snapshot=snapshot.relative_to(ROOT).as_posix(),redacted_display=False))
    manifest.append(dict(family=family,path=source,sha256=digest,bytes=len(raw),target=target,snapshot=snapshot.relative_to(ROOT).as_posix()))
    result=current.replace(b'\n<!-- SOURCE_ANNEX_20261007_END -->',annex.encode()+b'\n<!-- SOURCE_ANNEX_20261007_END -->')
    updates[target]=result; meta.update(output_sha256=sha(result),bytes=len(result),added_blocks=meta['added_blocks']+count)
# Source and all targets are rechecked before any target write.
if sha((ROOT/source).read_bytes())!=digest: raise SystemExit('Source changed')
for target in updates:
    old=json.loads((OUT/'delivery_plan.json').read_text(encoding='utf-8'))['families'][target]
    if sha((ROOT/target).read_bytes())!=old['output_sha256']: raise SystemExit('Concurrent target change')
for target,result in updates.items():
    (ROOT/target).write_bytes(result); (OUT/'preview'/target).write_bytes(result)
assets.append(dict(asset_id=sha(source.encode())[:24],path=source,sha256=digest,bytes=len(raw),role='source_document',family='geostrategy',canonical_target='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd',business_value_proposal='起始基線後新增商業化假設；收益與授權需核實',definition_status='PROPOSED_REVIEW_REQUIRED'))
save('source_manifest.csv',manifest); save('block_coverage.csv',ledger); save('asset_catalog.csv',assets)
plan.update(source_documents=len(manifest),block_records=len(ledger),assets=len(assets),late_source_baseline=dict(path=source,sha256=digest,bytes=len(raw)))
(OUT/'late_source_baseline.json').write_text(json.dumps(plan['late_source_baseline'],indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'delivery_plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
with sqlite3.connect(OUT/'project_information_catalog.sqlite') as db:
    for table,rows in [('assets',assets),('source_versions',manifest),('block_coverage',ledger)]:
        db.execute('DELETE FROM '+table); db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for _ in rows[0])+')',[tuple(str(v) for v in r.values()) for r in rows])
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
receipt=json.loads((OUT/'validation_receipt.json').read_text(encoding='utf-8'))
receipt.update(families=plan['families'],source_documents=len(manifest),blocks=len(ledger),assets=len(assets),late_source_baseline=plan['late_source_baseline'])
(OUT/'validation_receipt.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf-8')
index=ROOT/'Reference/Project_Information_Integration_20261007.qmd'
indextext=index.read_text(encoding='utf-8').replace('56 筆',str(len(manifest))+' 筆').replace('45,347 筆',f'{len(ledger):,} 筆').replace('3,711 個',f"{sum(m['added_blocks'] for m in plan['families'].values()):,} 個")
indextext+='\n## 收尾新增來源\n\n起始 577 件資產基線保持不變；另納入 1 件後續新增商業化藍圖，共 578 件原項目資產目錄。新增藍圖已增補至兩份主報告，保留原檔與獨立增量基線。新生成的交付與驗收資產另見收尾快照。\n'
index.write_text(indextext,encoding='utf-8')
print(json.dumps(dict(source_relations=len(manifest),blocks=len(ledger),assets=len(assets),added_blocks=sum(m['added_blocks'] for m in plan['families'].values())),ensure_ascii=False))
