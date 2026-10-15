"""Record this continuation separately from immutable first-pass acceptance."""
from pathlib import Path
import hashlib,json,subprocess
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[2]
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(name,value):(OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
ledger=read('verified_facts.json')
fda='https://www.accessdata.fda.gov/cdrh_docs/pdf24/K242618.pdf'
entries=[
 ('GTO0001','ASML 官方產品頁列出 EUV／DUV 光刻、量測檢查及計算光刻。','https://www.asml.com/en/products','Products overview'),
 ('GTO0003','imec 官方介紹描述其奈米電子與數碼技術研究。','https://www.imec-int.com/en/about-us','About imec'),
 ('GTO0005','Fraunhofer 官方介紹描述其應用研究組織及研究單位網絡。','https://www.fraunhofer.de/en/about-fraunhofer.html','The Fraunhofer-Gesellschaft'),
 ('GTO0006','RIKEN 官方介紹描述其綜合科學研究機構及研究中心網絡。','https://www.riken.jp/en/about/','About RIKEN'),
 ('GTT0026','FDA K242618 文件列明 Layer 7-T 電極用於少於30天的腦表面電訊號記錄、監測與刺激。',fda,'PDF page 4, Indications for Use'),
 ('GTT0026','FDA K242618 文件描述 Layer 7-T 為1024電極陣列。',fda,'PDF page 6, Device Description; page 9 contacts table'),
 ('GTT0026','FDA K242618 文件描述 Layer 7-T 沒有無線能力，僅用於專業醫療環境。',fda,'PDF page 6, Device Description'),
]
for n,(registry,claim,url,loc) in enumerate(entries,42):
    if not any(f['id']==f'F{n:03}' for f in ledger['facts']):
        ledger['facts'].append(dict(id=f'F{n:03}',claim=claim,status='SUPPORTED',source=url,locator=loc,
            checked_on='2026-10-15',document='Reference/Global_Technology_ISO249_Registry.qmd',registry_id=registry,
            boundary='限所引官方介紹／特定器材文件；不延伸至世界排名、最新數量、獨立性能或其他長期無線 BCI 系統獲准。'))
write('verified_facts.json',ledger)
change=read('quantum_review_receipt.json'); changes=read('source_changes.json')
if not any(r['path']==change['source'] for r in changes):
    changes.append(dict(path=change['source'],before_sha256=change['before_sha256'],after_sha256=change['after_sha256'],change='bounded quantum public-description review; all pre-existing bytes preserved'))
write('source_changes.json',changes)
results=read('results.json'); mismatches=[]
for r in results:
    if hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()!=r['source_sha256']:mismatches.append(r['path'])
accept=dict(head_at_rescan='d1f93f37b433aea74c722f49ff28161046f0dd2b',
    successful_render_records=sum(r['exit_code']==0 and r['html_exists'] for r in results),
    source_hash_mismatches=mismatches,source_change_records=len(changes),
    external_fact_checks=len(ledger['facts']),external_fact_review_complete=False,
    original_registry_bytes_preserved=change['original_bytes_preserved'],
    full_file_scan='../'+'../2026-10-06/workspace_change_audit/rescan20261015b_summary.json',
    earlier_final_acceptance='final_acceptance.json is the first-pass historical receipt; this receipt supersedes its current-state assertions',
    caveats=['One RStudio session lock could not be read','Scan records file hashes, not semantic certification of every file','Xanadu page had no readable body','Historical resource and unresolved-link gaps remain'])
write('current_acceptance.json',accept)
print(json.dumps(accept,ensure_ascii=True))
