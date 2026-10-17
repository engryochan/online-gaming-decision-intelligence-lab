"""Preserve source text and append narrow adjudications of evidence strength."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
rel='Reference/Baccarat-Ai-Automation-Report.qmd';p=ROOT/rel
evo24='https://www.evolution.com/wp-content/uploads/2025/04/Evolution-Annual-Report-2024.pdf'
evo25='https://www.evolution.com/wp-content/uploads/2026/04/Annual_Report_English_2026_04_01.pdf'
paper='https://www.mdpi.com/2076-328X/15/6/779'
entries=[
 ('F102','Playtech 官網自述 BetBuddy 被歐洲及美洲17個司法管轄區的運營商使用。','SUPPORTED','https://www.playtech.com/services/','Player Protection Services with BetBuddy','單位是司法管轄區，不是17家運營商、17份許可或獨立療效／干預驗證。'),
 ('F103','Evolution 2024年報描述以自動與人工控制共同監控桌台、遊戲及行為以防範欺詐。','SUPPORTED',evo24,'Mission Control Room / responsible gambling section','採官方PDF搜尋索引摘錄；直接PDF讀取失敗。只支持公司描述的混合控制，不證明特定AI模型認證或無人荷官。'),
 ('F104','Evolution 2025年報自報約三分之一的疑似問題博彩個案由AI工具發現。','SUPPORTED',evo25,'Printed page 64 / Uncertainty in the correlation','採官方PDF搜尋索引摘錄；直接PDF讀取失敗。分母為疑似個案，非全部玩家、欺詐確診率、模型準確率或實際傷害減少率。'),
 ('F105','原文將 Biometric Dealer Authentication 列為已獲 Evolution 官方證實的具體技術。','INSUFFICIENT_EVIDENCE',evo25,'Reviewed official indexed monitoring and AI descriptions','已讀官方監控摘錄不支持此具名生物識別實作；原列第三方連結不足以代替官方技術證據。不是斷言該功能不存在。'),
 ('F106','EZ Baccarat 官方品牌頁自述其以每小時手數衡量為市場最快。','SUPPORTED','https://ezbaccarat.com/','We Didn’t Invent Baccarat — We Made It Better!','只核對品牌方確有此宣稱，未獨立驗證樣本、比較範圍或實際發牌速度。'),
 ('F107','EZ Baccarat 市場最快的宣稱足以構成獨立性能驗證。','INSUFFICIENT_EVIDENCE','https://ezbaccarat.com/','Brand speed claim','所讀頁面未提供可重現的跨產品同條件測試；應寫品牌自述，不作已驗證排名。'),
 ('F108','所引 AI Personalization 論文明示未直接觀測或隔離AI干預，也沒有平台演算法投放日誌。','SUPPORTED',paper,'Sections 2.1, 3 and limitations','2016／2021行為比較為探索性與推論性；本次核對方法限制，不等於重算模型或認同所有論文解釋。'),
 ('F109','所引論文足以直接驗證特定RL發獎降低玩家控制的因果效果。','INSUFFICIENT_EVIDENCE',paper,'Abstract; limitations; no causal claims','論文明示不能對AI影響作因果推論；可討論風險假說，不能由此驗證特定RL部署或因果效果。'),
 ('F110','原文已證實 Octane／Sentient 個別遊戲具已認證 RNG 與可證明公平驗證。','INSUFFICIENT_EVIDENCE','https://octanestudios.ai/','Reviewed vendor product page; Sentient product page also reviewed','未取得對應遊戲版本的認證編號、測試報告或可重現證明；產品定位不等同技術認證，兩家廠商須分別查驗。'),
]
lp=OUT/'verified_facts.json';ledger=json.loads(lp.read_text(encoding='utf-8'))
for ident,claim,status,url,loc,bound in entries:
    if not any(x['id']==ident for x in ledger['facts']):ledger['facts'].append(dict(id=ident,claim=claim,status=status,source=url,locator=loc,boundary=bound,document=rel,checked_on='2026-10-17'))
ledger['last_updated']='2026-10-17';lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
raw=p.read_bytes();marker='<!-- EVIDENCE_STRENGTH_ADJUDICATION_20261017 -->'
if marker.encode() not in raw:
    before=hashlib.sha256(raw).hexdigest();(OUT/'original_bytes'/f'{before}.bin').write_bytes(raw)
    text='\n\n'+marker+'\n\n## 2026-10-17 官方自述、方法限制與認證證據續核\n\n'
    text+='以下區分「來源確有此描述」與「性能／因果／認證已驗證」。Evolution 年報僅取得官方PDF的搜尋索引摘錄，未冒充完整讀取；論文則已讀出版社正文的方法與限制段。\n\n'
    text+='| 編號 | 主張與裁決 | 來源與採用邊界 |\n| --- | --- | --- |\n'
    text+=''.join(f'| {ident} | **{status}**：{claim} | [{loc}]({url})；{bound} |\n' for ident,claim,status,url,loc,bound in entries)
    text+='\n採用修訂：17個司法管轄區保留原單位；AI發現疑似個案的比例不得換算模型準確率。生物識別荷官認證、最快速度與個別遊戲 RNG／可證明公平須另附對應證據。論文的方法限制必須一併保留，風險推論不能寫成已驗證的特定RL因果結果。\n'
    with p.open('ab') as f:f.write(text.replace('\n','\r\n').encode())
    after=hashlib.sha256(p.read_bytes()).hexdigest();changes=json.loads((OUT/'source_changes.json').read_text(encoding='utf-8'))
    entry=next(x for x in changes if x['path']==rel);entry['after_sha256']=after
    entry['change']='Preserve embedded historical HTML; append scoped dealer, operations, regulatory, causal and certification adjudications'
    (OUT/'source_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
    (OUT/'evidence_20261017_receipt.json').write_text(json.dumps(dict(source=rel,before_sha256=before,after_sha256=after,
        original_bytes_preserved=p.read_bytes().startswith(raw),adjudications=[x[0] for x in entries],external_fact_review_complete=False),ensure_ascii=False,indent=2),encoding='utf-8',newline='')
print('facts',len(ledger['facts']))
