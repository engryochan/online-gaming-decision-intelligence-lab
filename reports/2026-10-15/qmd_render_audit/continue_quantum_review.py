"""Append a bounded review without rewriting historical registry records."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[2]
p=ROOT/'Reference/Global_Technology_ISO249_Registry.qmd'
items=[
 ('GTO0025','Quantinuum','Quantinuum 官方列出量子電腦及 Nexus、TKET、InQuanto 等軟件。','https://www.quantinuum.com/','Discover our Quantum Computers; Build Quantum Applications; Accelerate Innovation'),
 ('GTO0026','IQM','IQM 官方描述其建造全棧超導量子電腦。','https://iqm.tech/','Quantum Computers. Delivered.'),
 ('GTO0027','IonQ','IonQ 官方技術頁描述離子阱及激光操作的量子計算。','https://www.ionq.com/technology','Trapping an ion; Computing with atoms'),
 ('GTO0028','Pasqal','Pasqal 官方描述中性原子量子處理器與量子計算系統。','https://www.pasqal.com/','Neutral-atom quantum computers; Pasqal powers transformation'),
 ('GTO0029','Quandela','Quandela 官方描述光子量子計算及 Perceval Python 開發框架。','https://www.quandela.com/','MOSAIQ; PERCEVAL'),
 ('GTO0030','QuEra','QuEra 官方描述正在建造中性原子量子系統，並以未來大規模糾錯系統為方向。','https://www.quera.com/vision-mission','A Practical Path To Quantum Advantage; Our Mission'),
 ('GTO0031','D-Wave','D-Wave 官方提供退火量子系統、Leap 雲服務及 Ocean 開發工具的描述。','https://www.dwavequantum.com/','Annealing Quantum Systems; Cloud Platform; Developer Tools'),
]
ledger=json.loads((OUT/'verified_facts.json').read_text(encoding='utf-8'))
for n,(row,name,claim,url,locator) in enumerate(items,35):
    ident=f'F{n:03}'
    if not any(f['id']==ident for f in ledger['facts']):
        ledger['facts'].append(dict(id=ident,claim=claim,status='SUPPORTED',source=url,locator=locator,
            document='Reference/Global_Technology_ISO249_Registry.qmd',registry_id=row,checked_on='2026-10-15',
            boundary='官方公開技術描述；未獨立測量性能、核實法人國籍／股權、確認全面容錯或接受世界領先等比較宣稱。'))
(OUT/'verified_facts.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
marker='<!-- QUANTUM_FACT_REVIEW_20261015 -->'
raw=p.read_bytes()
if marker.encode() not in raw:
    before=hashlib.sha256(raw).hexdigest(); (OUT/'original_bytes'/f'{before}.bin').write_bytes(raw)
    addition='\n\n'+marker+'\n\n## 2026-10-15 量子科技公開描述續核\n\n'
    addition+='本節重新對照現時官方頁面，保留上方歷史批次、數量及 UNKNOWN 狀態，不回寫舊 CSV。SUPPORTED 僅限以下公開描述；不證明性能排名、法人國籍／股權、商業成效或全面容錯已實現。\n\n'
    addition+='| 登記 ID | 本次核實的窄義主張 | 一手來源 |\n| --- | --- | --- |\n'
    addition+=''.join(f'| {row} | {claim} | [{name}]({url}) |\n' for row,name,claim,url,loc in items)
    addition+='\nGTO0032（Xanadu）：本次開啟官網仍未取得可讀正文，保留待查；不能由讀取失敗推斷機構或技術不存在。QuEra 頁面的未來糾錯方向亦不能視為已完成大型容錯系統。其餘科技、神經科技與跨文件主張仍需逐條查證。\n'
    with p.open('ab') as f:f.write(addition.replace('\n','\r\n').encode())
    (OUT/'quantum_review_receipt.json').write_text(json.dumps(dict(source=p.relative_to(ROOT).as_posix(),
        before_sha256=before,after_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        original_bytes_preserved=p.read_bytes().startswith(raw),new_supported_claims=7,
        unreadable_source='https://www.xanadu.ai/',external_fact_review_complete=False),ensure_ascii=False,indent=2),encoding='utf-8')
print('ledger facts',len(ledger['facts']))
