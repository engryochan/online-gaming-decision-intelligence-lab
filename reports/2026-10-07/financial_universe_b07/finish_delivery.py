from pathlib import Path
import csv,json,sqlite3
R=Path(__file__).resolve().parents[3]; O=Path(__file__).parent
csv.field_size_limit(32*1024*1024)
T=R/'Reference/tables/25_iso249_financial_universe_b07_20261007'
with (T/'registry_iso249_financial_coverage.csv').open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
assert len(rows)==249 and len({r['iso_alpha2'] for r in rows})==249
body='''---
title: "全球金融資料全集 B07：ISO 249 逐國覆蓋與 ESMA 完整接收"
date: 2026-10-07
format:
  html:
    toc: true
---

## 本輪交付與實際邊界

全部249個ISO 3166-1國家／地區均已列入覆蓋表，並分別展開上市公司、證券業者、貨幣三項工作，共747項。這是有來源與缺口的逐國清單；747項仍為OPEN，不能據此宣稱全球每家公司及每種實際使用貨幣均已收齊。ISO代碼不表示國家獲得認證。

本輪完整接收ESMA投資公司登記：7,162條公司／分支記錄，涵蓋31個來源母國標籤；來源狀態Active 5,861條、Inactive 1,301條，Head office 6,476條、Branch 686條。另收33,363條業務活動及42,005條活動歷史，合計82,530份來源文件。活動類型不等於全部當前有效授權；投資公司登記也不等於唯一證券行總數。英國來源只有一條Inactive記錄，不能當成當前市場完整覆蓋。

來源依[ESMA公開A2A文件及官方預定義查詢](https://registers.esma.europa.eu/publication/helpApp)下載。公司查詢8頁、公司與活動歷史查詢17頁，逐頁numFound穩定、來源ID無重複；兩個查詢的公司文件逐項相同，所有活動父ID均存在。這驗證此次查詢接收完整，不保證跨頁原子快照或來源所有授權均已更新。來源自身更新日期與HTTP接收日期分别保留。

登記中的42個主管機關名稱字串形成71個母國／名稱分組，尚未完成主管機關法律身份去重；母國分組不代表該機關所在地。所有原始欄位、陣列、狀態、日期、LEI及歷史均保留JSON，未以名稱合併公司。

## 資料與查詢

統一快照v4保留v3的所有79,207條原始列、43,410條上市工具／公司目錄來源列及2,883條MIC資料，新原始列累計162,933條。這些數字均不是全球唯一公司數。舊資料庫與原報告保留，新增查詢庫位於`../reports/2026-10-07/financial_universe_b07/financial_universe_v4.sqlite`。

上市來源目前覆蓋七個市場，其餘242個母表條目尚待接收或確認適用範圍。249條目均已連結既有貨幣來源關係，但名稱別名、法定地位及所有實際使用貨幣仍須核實。MIC來源網站是待查入口，未當成已逐站核實的交易所名單。日本FSA／JPX、台灣TWSE及紐西蘭NZX先前業者／參與者清單已納入來源盤點；不同清單重疊未去重，參與者不全是證券行。

'''
for p in sorted(T.glob('*.csv')): body+=f'- [{p.name}](tables/{T.name}/{p.name})\n'
body+='''
## ISO 249 全部條目的現況

下表的0表示尚未接收對應來源，不表示該地區沒有公司、市場或證券行。業者欄是來源記錄清單而非唯一券商數；ESMA含分支與失效記錄，FSA含多類金融工具業者，JPX／NZX含不同參與角色。貨幣代碼含來源定義的特殊用途項目；空碼須核實。完整母表欄位、網站、主管機關、狀態及缺口見上述CSV。

| ISO | 國家／地區來源名稱 | 上市來源列 | 業者／參與者來源盤點 | MIC來源列 | 貨幣來源代碼 |
|---|---|---:|---|---:|---|
'''
for r in rows:
 inv=json.loads(r['securities_firm_source_inventory_json']); desc='；'.join(f'{k}: {v}' for k,v in inv.items()) or '待接收／待核實'
 vals=[r['iso_alpha2'],r['name_en'],r['listing_source_records'],desc,r['MIC_source_rows'],r['current_codes'] or '來源空碼／待核實']
 body+='| '+' | '.join(str(v).replace('|','／').replace('\n',' ') for v in vals)+' |\n'
body+='''
## 驗收與下一階段缺口

來源分頁清單保留25頁的URL、SHA256、列數與伺服器日期。接收資料通過原始JSON往返、活動父子關係、旧列逐項保留及SQLite完整性檢查。驗收不等於所有249條目內容已完成實質核實。

下一階段需逐國核對主管機關完整持牌名冊、全部交易場所的公司與證券清單、跨境／跨市場掛牌身份與所有貨幣法律來源；每項完成必須有來源範圍、日期、接收總數、分頁對賬、唯一身份與排除規則。沒有來源或受限下載的條目保持UNKNOWN，不能改寫為零或VERIFIED。神經科技與技術成熟度依原證據流程另行核實，本輪金融資料不能代替其能力證據。
'''
(R/'Reference/Global_Financial_Universe_B07_20261007.qmd').write_text(body,encoding='utf-8')
queries={
 'esma_status':'SELECT source_status,COUNT(*) FROM esma_entities GROUP BY source_status',
 'esma_office':'SELECT office_type,COUNT(*) FROM esma_entities GROUP BY office_type',
 'workstreams':'SELECT stream,COUNT(*) FROM country_workstreams GROUP BY stream',
 'missing_activity_parent':'SELECT COUNT(*) FROM esma_activities a LEFT JOIN esma_entities e ON a.parent_record_id=e.record_id WHERE e.record_id IS NULL',
 'activity_types':'SELECT record_type,COUNT(*) FROM esma_activities GROUP BY record_type',
 'listing_count':'SELECT COUNT(*) FROM listing_records',
 'raw_count':'SELECT COUNT(*) FROM raw_records',
 'currency_count':'SELECT COUNT(*) FROM currency_entries',
 'fsa_count':'SELECT COUNT(*) FROM fsa_firms'}
(O/'queries.sql').write_text('\n'.join('-- '+k+'\n'+v+';' for k,v in queries.items())+'\n',encoding='utf-8')
c=sqlite3.connect(O/'financial_universe_v4.sqlite'); results={k:c.execute(q).fetchall() for k,q in queries.items()}; assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok';c.close()
assert results['missing_activity_parent']==[(0,)] and results['listing_count']==[(43410,)] and results['raw_count']==[(162933,)]
assert all(x[1]==249 for x in results['workstreams']) and len(results['workstreams'])==3
(O/'query_acceptance.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
old=R/'reports/2026-10-07/financial_universe_b06'
s=(old/'append_index.py').read_text(encoding='utf-8').replace('FINANCIAL_UNIVERSE_B06_20261007','FINANCIAL_UNIVERSE_B07_20261007')
addition='\n\n<!-- FINANCIAL_UNIVERSE_B07_20261007 -->\n\n## ISO 249 全球金融增補 B07\n\n[全部249條目覆蓋與ESMA完整登記](Global_Financial_Universe_B07_20261007.qmd)：747項逐國工作列保留實際來源與缺口；新增31個來源母國標籤的7,162條公司／分支記錄及75,368條活動／歷史。統一快照v4保留舊列，全球全部公司與券商仍待逐國完成，未宣稱收齊。\n'
a=s.index('addition='); b=s.index('\nsaved=',a); s=s[:a]+'addition='+repr(addition)+s[b:];(O/'append_index.py').write_text(s,encoding='utf-8')
s=(old/'validate_preservation.py').read_text(encoding='utf-8').replace('financial_b06_start','iso249_b07_start').replace('financial_b06_finish','iso249_b07_finish').replace('24_financial_universe_b06_20261007','25_iso249_financial_universe_b07_20261007').replace('financial_universe_v3.sqlite','financial_universe_v4.sqlite').replace('Global_Financial_Universe_B06','Global_Financial_Universe_B07')
(O/'validate_preservation.py').write_text(s,encoding='utf-8')
print('Report with all 249 rows and query acceptance created')
