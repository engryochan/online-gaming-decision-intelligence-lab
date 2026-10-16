"""Preserve the historical HTML and add explicit source-backed adjudications."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
rel='Reference/Baccarat-Ai-Automation-Report.qmd';p=ROOT/rel
release='https://www.globenewswire.com/news-release/2026/04/22/3278934/0/en/bethog-raises-10m-series-a-to-bring-ai-powered-live-dealers-to-operators.html'
entries=[
 ('F087','BetHog 於2026-04-22發布公告，宣布推出 B2B 供應商 Sentient Studios。','SUPPORTED',release,'Announcement opening paragraph','公告支持推出 B2B 供應商；不能單憑此推斷同一法律實體正式改名。'),
 ('F088','原文稱 Sentient Studios 以百家樂為首發品類。','CONTRADICTED',release,'Paragraph beginning The launch builds on BetHog’s first AI-powered blackjack dealer','公告明述首個 AI 荷官 Sunny 為2025年10月推出的 blackjack，百家樂與輪盤在2026年4月仍為後續擴充計畫；現時提供百家樂不能倒推首發時間。'),
 ('F089','原文稱全球公開宣稱並落地 AI Dealer 取代人力的廠商僅有 Octane 與 Sentient 兩家。','INSUFFICIENT_EVIDENCE','https://www.sentientstudios.ai/','Reviewed vendor product description','所讀廠商頁不能證明全球排他名單或全部已落地；應改為本次具名案例，不作僅此兩家的結論。'),
 ('F090','Octane Studios 官網介紹可品牌化、可程式化的 AI dealer games。','SUPPORTED','https://octanestudios.ai/','Intro; Today/Next/Then/Coming roadmap','限廠商公開產品定位；頁面把多語即時語音、記憶辨識及完整互動分列後續階段，未獨立證實部署與成效。'),
]
lp=OUT/'verified_facts.json';ledger=json.loads(lp.read_text(encoding='utf-8'))
for ident,claim,status,url,loc,bound in entries:
    if not any(x['id']==ident for x in ledger['facts']):ledger['facts'].append(dict(id=ident,claim=claim,status=status,source=url,locator=loc,boundary=bound,document=rel,checked_on='2026-10-16'))
ledger['last_updated']='2026-10-16';lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
raw=p.read_bytes();marker='<!-- AI_DEALER_ADJUDICATION_20261016 -->'
if marker.encode() not in raw:
    before=hashlib.sha256(raw).hexdigest();(OUT/'original_bytes'/f'{before}.bin').write_bytes(raw)
    updated=raw.replace(b'recovery-kind: lossless-html-snapshot',b'recovery-kind: html-snapshot-with-markdown-appendix',1)
    text='\n\n'+marker+'\n\n## 2026-10-16 原文主張裁決與採用限制\n\n'
    text+='上方保留歷史 HTML 原文；以下裁決適用於採用原文結論時，不以原文自稱「查證」代表所有主張已獲證實。\n\n'
    text+='| 編號 | 主張與裁決 | 來源及限定 |\n| --- | --- | --- |\n'
    text+=''.join(f'| {ident} | **{status}**：{claim} | [{loc}]({url})；{bound} |\n' for ident,claim,status,url,loc,bound in entries)
    text+='\n採用時應寫為：本次具名查閱 Octane 與 Sentient 的 AI 荷官案例，並不構成全球唯一供應商名單。Sentient 的 B2B 推出與 BetHog 的法律改名不可混同；Sunny 的歷史首發為 blackjack，現時百家樂產品存在不代表以百家樂首發。廠商自報使用率、語言數或商業成果仍須另驗，不能由本節支持的產品定位推導。\n'
    updated+=text.replace('\n','\r\n').encode();p.write_bytes(updated)
    after=hashlib.sha256(updated).hexdigest()
    changes=json.loads((OUT/'source_changes.json').read_text(encoding='utf-8'))
    changes.append(dict(path=rel,before_sha256=before,after_sha256=after,change='Preserve embedded historical HTML bytes; change snapshot metadata for Markdown adjudication appendix and append bounded corrections'))
    (OUT/'source_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
    (OUT/'ai_dealer_20261016_receipt.json').write_text(json.dumps(dict(source=rel,before_sha256=before,after_sha256=after,embedded_html_unchanged=True,adjudications=[x[0] for x in entries],external_fact_review_complete=False),ensure_ascii=False,indent=2),encoding='utf-8',newline='')
print('ledger facts',len(ledger['facts']))
