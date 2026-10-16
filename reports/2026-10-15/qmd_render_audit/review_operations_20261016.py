"""Append scoped operations, benchmark and regulatory evidence adjudications."""
from pathlib import Path
import hashlib,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
rel='Reference/Baccarat-Ai-Automation-Report.qmd';p=ROOT/rel
prag='https://www.pragmaticplay.com/en/live-casino/bet-behind-pro-blackjack/'
mga='https://www.mga.org.mt/mga-launches-ai-gaming-charter-following-extensive-industry-collaboration/'
smart='https://www.smartico.ai/blog-post/the-complete-guide-to-player-churn-prevention-in-online-casinos-proven-strategies-to-boost-player-retention-in-2025'
acq='https://www.globenewswire.com/news-release/2026/04/06/3268555/0/en/optimove-to-acquire-smartico.html'
entries=[
 ('F091','Pragmatic Play 描述 Bet Behind Pro Blackjack 的七個席位由採基本策略的 bot 佔據。','SUPPORTED',prag,'Product introduction; Basic Strategy','限產品規則描述，不證明採用機器學習或強化學習。'),
 ('F092','原文將 Bet Behind Pro Blackjack 的自動化分類寫成 Bot 荷官。','CONTRADICTED',prag,'Instant Decisions: bots compete against a professionally trained live dealer','bot 扮演玩家，對面為真人荷官；不能因玩家自動決策而稱荷官自動化。'),
 ('F093','MGA 官網在2026-09-18公告與 MDIA 合作推出 AI Gaming Charter。','SUPPORTED',mga,'Publication date; opening paragraph','證實該公告日期與合作推出，不推導個別運營商已符合規範。'),
 ('F094','MGA 將 AI Gaming Charter 描述為自願、原則導向，補充既有法律框架。','SUPPORTED',mga,'Paragraph beginning As artificial intelligence','自願章程不解除其他法律義務，不能推導在特定年份前可任意選擇法律披露。'),
 ('F095','SOFTSWISS 自報2022年反欺詐團隊處理61,810項請求，協助客戶節省超過1,600萬歐元。','SUPPORTED','https://www.softswiss.com/news/softswiss-anti-fraud-results-2022/','2023-03-23 release, first two paragraphs','公司對人員及服務團隊的自報成果；未獨立審計，不能全歸因於AI或解讀為模型準確率。'),
 ('F096','SOFTSWISS 自報2023年處理超過100,000項 tasks，協助保障超過1,300萬歐元。','SUPPORTED','https://www.softswiss.com/news/softswiss-safeguards-13m-in-2023/','2024-01-05 release, opening paragraphs','tasks 包含多種請求、驗證與可疑活動，不應全改稱已確認欺詐案件或全自動攔截。'),
 ('F097','原文把 Smartico 75.94% 流失預測準確率列為可採用的實驗基線。','INSUFFICIENT_EVIDENCE',smart,'Current destination of the cited predictive-churn URL','目前跳轉頁未提供此數字、資料集、測試切分或可重現驗證；不證明歷史頁從未出現此數字，暫不作已驗證基線。'),
 ('F098','原文以所引文章證明 Smartico 已部署所述RL遊戲化與上下文多臂老虎機流程。','INSUFFICIENT_EVIDENCE',smart,'AI-Powered Churn Prediction Models; current article body','目前頁面未提供該具體生產部署的技術證據；第三方開發商文章亦不能自動當作 Smartico 系統文件。'),
 ('F099','Optimove 於2026-04-06公告已簽署收購 Smartico 協議，當時預期稍後完成交易。','SUPPORTED',acq,'Opening transaction paragraphs','僅證實公告當時的簽約及預期，不等同本次核實已交割或當前股權。'),
 ('F100','原文以 Smartico／Optimove 收購案證明RL產品的準確率與落地已獲驗證。','INSUFFICIENT_EVIDENCE',acq,'Transaction announcement','公告的產品／商業描述不是獨立技術驗收或RL效能驗證，不能據此確認75.94%或A/B效果。'),
 ('F101','歐盟官方 AI Act 導覽的 Article 6 按特定產品條件或 Annex III 用途分類高風險系統。','SUPPORTED','https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-6','Article 6 paragraphs 1-3; page version notice dated 2026-07-27','結構性判讀：不能只因博彩、聊天或個人化等詞便一概判高風險；個案、適用期限與其他義務仍需依正式法規及具體用途另查。'),
]
lp=OUT/'verified_facts.json';ledger=json.loads(lp.read_text(encoding='utf-8'))
for ident,claim,status,url,loc,bound in entries:
    if not any(x['id']==ident for x in ledger['facts']):ledger['facts'].append(dict(id=ident,claim=claim,status=status,source=url,locator=loc,boundary=bound,document=rel,checked_on='2026-10-16'))
ledger['last_updated']='2026-10-16';lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
raw=p.read_bytes();marker='<!-- OPERATIONS_ADJUDICATION_20261016 -->'
if marker.encode() not in raw:
    before=hashlib.sha256(raw).hexdigest();(OUT/'original_bytes'/f'{before}.bin').write_bytes(raw)
    text='\n\n'+marker+'\n\n## 2026-10-16 營運指標、Bot角色與監管文字續核\n\n'
    text+='本節延續上節裁決，保留原文與先前增補。公司自報、產品規則、正式交易公告及技術驗收分別判讀；未將沒有找到證據等同已證偽。\n\n'
    text+='| 編號 | 主張與裁決 | 來源與採用邊界 |\n| --- | --- | --- |\n'
    text+=''.join(f'| {ident} | **{status}**：{claim} | [{loc}]({url})；{bound} |\n' for ident,claim,status,url,loc,bound in entries)
    text+='\n採用修訂：Bet Behind Pro 的 bot 是玩家而非荷官；SOFTSWISS 數字以年份、原單位及「公司自報」標示，不作AI獨立效能指標。75.94%及所述RL／bandit流程暫不得作已驗證部署或對照基線，須補原始技術與試驗證據。MGA 自願章程不替代法律義務；高風險分類須逐系統對照正式適用條件，不從產業或功能名稱直接下結論。\n'
    with p.open('ab') as f:f.write(text.replace('\n','\r\n').encode())
    after=hashlib.sha256(p.read_bytes()).hexdigest();changes=json.loads((OUT/'source_changes.json').read_text(encoding='utf-8'))
    entry=next(x for x in changes if x['path']==rel);entry['after_sha256']=after
    entry['change']='Preserve embedded historical HTML; append bounded dealer, operations, benchmark and regulatory adjudications'
    (OUT/'source_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8',newline='')
    (OUT/'operations_20261016_receipt.json').write_text(json.dumps(dict(source=rel,before_sha256=before,after_sha256=after,
        original_bytes_preserved=p.read_bytes().startswith(raw),adjudications=[x[0] for x in entries],
        source_access_gaps=['PMC12189489 returned browser challenge; paper not substantively checked'],external_fact_review_complete=False),ensure_ascii=False,indent=2),encoding='utf-8',newline='')
print('facts',len(ledger['facts']))
