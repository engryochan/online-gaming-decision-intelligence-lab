import intake,csv,json,sqlite3,hashlib,collections
O,T,R=intake.O,intake.T,intake.R
summaries={n:json.loads((O/n).read_text(encoding='utf-8')) for n in ['intake_acceptance.json','pagination_acceptance.json','structure_acceptance.json','completion_acceptance.json']}
db=T/'global_directory_content_b05.sqlite'
if db.exists():raise RuntimeError('Preserve existing database; inspect before rebuilding')
con=sqlite3.connect(db);counts={}
for path in sorted(T.glob('*.csv')):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames
        if not fields:continue
        rows=list(reader);name=path.stem
        quote=lambda s:'"'+s.replace('"','""')+'"'
        con.execute('CREATE TABLE '+quote(name)+' ('+','.join(quote(k)+' TEXT' for k in fields)+')')
        con.executemany('INSERT INTO '+quote(name)+' VALUES ('+','.join('?' for _ in fields)+')',[[r.get(k,'') for k in fields] for r in rows]);counts[name]=len(rows)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
report=R/'Reference/Global_Directory_Content_Expansion_B05_20261008.qmd'
text='''---
title: "全球官方名錄內容擴展 B05：全清單分級、逐表保留與監管類別對賬"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 範圍與驗證邊界

本輪承接 B04 的全部 4,849 個唯一 URL 工作項，逐项保留及分級；實際抓取 129 個具有名錄訊號的優先來源，以及 3 個補充官方來源。這是逐批採集，不能解讀為全球所有網站、公司、證券行或貨幣已完成。其餘工作仍在完整分級表中，並未刪除。ISO 母表表示國家／地區代碼，不是國家品質認證。

原始來源正文、表頭、物理行、連結、來源網址及 SHA256 均保留。不同網址的相同正文另列對賬；來源行與公司主體不是一對一。沒有將黑名單、基金、商品清算會員、新上市事件、退市證券或服務價目表合併算成現存上市公司。

## 本輪取得的證據

- 132 個來源中 128 個 HTTP 200；另跟進 14 個觀測到的同站分頁，共保留 4,186 條表格行、151 個來源表格。
- 表格轉成 2,809 條具角色標記的來源觀測；它們尚不是跨市場去重後的公司總數。另保存烏干達 CMA 93 張分類名錄卡片、19 個分類區塊的完整文字及 HTML。
- 9 個觀測到的唯一檔案連結全部保存，其中一項重用 B04 已保留的 PSX 2024 券商 ZIP；共核查 284 個壓縮成員，另保留 PSX 股份收購工作簿全部 247 行，包括空行與表頭。BMV 的 XBRL ZIP 是申報證據，不是上市公司全集；本輪保留檔案及成員雜湊，財務事實語義解析尚待完成。

## 多來源內容與業務定義

資料包含加納、巴巴多斯、巴布亞紐幾內亞、巴基斯坦、烏干達、澳洲 NSX、Nasdaq Baltic、歐洲商品清算及其他來源。加納固定收益發行人列為債務發行人；證券篩選器中的基金或其他證券保留其原始資料，未認定為普通股公司。

[PNGX 上市公司](https://www.pngx.com.pg/companies/listed-companies/)頁面觀測到 13 條公司記錄；HTTP 與 HTTPS 重複觀測均保留。[PSX 篩選器](https://dps.psx.com.pk/screener/)保留 748 條來源證券觀測，不能直接宣稱 748 家獨立公司。[烏干達證券交易所行情](https://www.use.or.ug/market-statistics/market-snapshot)保留 17 條來源記錄；空價格不填造數值。[CMA 官方持牌機構分類](https://cmauganda.co.ug/cma-licensed-firms/)逐區塊對賬，Stock Brokers 分類觀測到 6 張卡片；頁面記錄不等於已獨立核實本年度續牌。

## 缺口與後續清單

動態空表、HTTP 失敗、非表格頁面、頁面總量與範圍未確認、日期不明及分類數量不一致均保留於逐頁／逐區塊核查表。CMA 有 1 個區塊的標示數量與卡片數未一致，未任意修正來源。跟進所有已觀測的同站分頁不代表已發現所有隱藏分頁、API 或下載。全球唯一公司、證券行與貨幣完整性仍為 UNKNOWN。

## 可重現交付

[完整工作項分級](tables/30_global_directory_content_b05_20261008/registry_all_workqueue_priority_review.csv)、[表格來源記錄](tables/30_global_directory_content_b05_20261008/registry_structured_directory_records.csv)、[監管分類卡片](tables/30_global_directory_content_b05_20261008/registry_cma_all_licensed_category_cards.csv)、[分類對賬](tables/30_global_directory_content_b05_20261008/registry_cma_section_count_reconciliation.csv)、[SQLite 資料庫](tables/30_global_directory_content_b05_20261008/global_directory_content_b05.sqlite)。所有原始物理表格行另存 CSV，投影欄位歧義可回溯原始 cells_json，不依投影推定完整業務定義。

原宇航報告、先前批次與使用者正在修改的 Inteligent 文件均保留。本輪沒有覆寫它們。
'''
report.write_text(text,encoding='utf-8')
summary=dict(summaries=summaries,database_table_counts=counts,database_integrity='ok',global_complete=False)
(O/'delivery_acceptance.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(database_tables=len(counts),report=str(report))))
