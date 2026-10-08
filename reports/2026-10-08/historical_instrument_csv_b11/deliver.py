from pathlib import Path
import json,csv,sqlite3,hashlib,sys,gzip
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/36_historical_instrument_csv_b11_20261008';P=R/'Reference/tables/35_global_directory_content_b10_20261008'
a=json.loads((O/'acquisition_acceptance.json').read_text());v=json.loads((O/'validation_receipt.json').read_text());ratio=100*a['raw_gzip_bytes']/a['raw_bytes'] if a['raw_bytes'] else 0
qmd=R/'Reference/Global_Historical_Instrument_CSV_B11_20261008.qmd'
text=f'''---
title: "歷史工具檔施工 B11：全批次採集、無損壓縮與可查詢行"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 已觀測批次的全量嘗試

承接 B10 下載清單全部 1,848 個未選項，本輪逐項嘗試，沒有只挑少數日期。它們是蒙特婁交易所 InstrumentsPreview 歷史 CSV，来源發現鏈、網址、檔案日期訊號及觀測日期分別保存。這是已發現連結批次的採集，不是證明已發現交易所全部歷史檔案，更不是全球市場完成。

共取得 {a['http200']:,} 個 HTTP 200、保存 {a['saved_bodies']:,} 份正文，{a['parsed_files']:,} 份按觀測 CSV 格式解析完成；{v['gaps']} 項仍需取得／解析核查。所有待續 URL 均有回執。解析資料共 {a['logical_csv_rows']:,} 條邏輯 CSV 行（包含表頭及空行），涉及 {v['unique_parsed_body_hashes']:,} 個不同正文雜湊、{v['schema_variants']} 種表頭版本。不同網址相同正文只共用壓縮區塊，來源觀測不合併或刪除。

## 無損儲存与可查詢性

原始正文合計 {a['raw_bytes']:,} 位元組，以 gzip 保存為 {a['raw_gzip_bytes']:,} 位元組，約為原大小 {ratio:.2f}%。每份保存未壓縮 SHA256、gzip SHA256、原始與壓縮大小。全批次解壓還原後雜湊對賬通過；原始分號、引號、BOM、換行與空欄均存在原始位元組中，解析不覆寫源檔。

SQLite 將每最多1,000行的原始欄位陣列存為可逆 gzip JSON 區塊，保存開始行、行數與未壓縮 payload 雜湊；全區塊連續行號、來源重解析與儲存行序列逐檔核對。資料庫並非只留下載清單，完整解析行也在其中。

一般 SQLite 客戶端可以查詢回執及区塊索引；直接查詢區塊內容需註冊 csv_block_json 函數。本輪提供 [只讀查詢器](../reports/2026-10-08/historical_instrument_csv_b11/query_rows.py)，連線以 mode=ro 開啟，建立暫存 csv_rows 視圖，解壓後透過 JSON 展開，不改資料庫。例：`query_rows.py --url-contains 202609 --limit 10`。這項壓縮取捨降低重複儲存，但未宣稱任意 SQL 客戶端可直接查詢未解壓欄位。

## 業務定義與證據邊界

原始表頭含工具識別碼、外部符號、工具類型、合約日期、行使價及相關工具等來源欄位。本輪按原始欄名保存並列出來源代碼頻次；沒有未經字典核定就將 InstrumentType、CallPutCode 或 MarketFlowIndicator 的代碼解釋為某種產品。

來源工具ID可能在不同日期或市場環境有不同用途，未核定其全歷史唯一性。合約／系列新增事件、存續日期及檔案日期不等於公司成立日、上市公司數或現存合約全集。所有 CSV 值保持原始字串，識別碼、空值、日期及數字精度不自行轉型。檔案解析與雜湊驗證不等於公司身分、監管或金融事實的實質核定。

## 累計清單與全球缺口

本輪對 B10 全部 1,897 個下載 URL 更新進度：本輪1,848項與此前49項都保留，舊批次檔案及回執不覆寫。此前 Nasdaq bandwidth XLS 的失敗、已下載工作簿的語義缺口及其他網站來源仍可回溯 B10，不把這次 CSV 施工標為它們已完成。

全球原始4,849項網站工作、249條現行母表與歷史政治實體工作仍保留。B10 中4,152項未嘗試的網站工作没有被本輪CSV下載消除；逐國所有公司、券商、貨幣與歷史政治實體的完整性仍為 UNKNOWN。

## 交付

[逐檔回執](tables/36_historical_instrument_csv_b11_20261008/registry_file_fetch_manifest.csv)、[全部1,897項進度](tables/36_historical_instrument_csv_b11_20261008/registry_all_1897_download_progress.csv)、[區塊索引](tables/36_historical_instrument_csv_b11_20261008/registry_csv_block_index.csv)、[表頭版本](tables/36_historical_instrument_csv_b11_20261008/registry_schema_fingerprints.csv)、[來源代碼頻次](tables/36_historical_instrument_csv_b11_20261008/registry_source_code_observations.csv)、[缺口](tables/36_historical_instrument_csv_b11_20261008/registry_fetch_parse_gaps.csv)、[SQLite](tables/36_historical_instrument_csv_b11_20261008/historical_instrument_csv_b11.sqlite)。

兩份受保護報告不改寫，Inteligent 文件现有修改保留且不納入提交。逐檔壓縮前進行憑證模式掃描，檢出候選 {a['credential_candidate_files']} 份；不輸出候選值，候選原始檔僅留本機且不解析入發佈資料庫。掃描不是所有可能機密形式的完整證明。
'''
qmd.write_text(text,encoding='utf-8')
receipts=list(csv.DictReader((T/'registry_file_fetch_manifest.csv').open(encoding='utf-8-sig')))
excluded=[r['file'] for r in receipts if r.get('publication')=='LOCAL_ONLY_CREDENTIAL_CANDIDATE']
if excluded:
    ignore=R/'.gitignore';old=ignore.read_text(encoding='utf-8');marker='# B11 credential candidates: local only'
    if marker not in old:ignore.write_text(old+'\n'+marker+'\n'+'\n'.join('/'+p for p in excluded)+'\n',encoding='utf-8')
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
source=(O.parent/'global_directory_content_b05/security.py').read_text(encoding='utf-8').replace('Global_Directory_Content_Expansion_B05','Global_Historical_Instrument_CSV_B11')
exec(compile(source,str(O/'deliver.py'),'exec'))
extra=[r for r in findings if r['path'].split('::')[0] not in excluded];assert not extra,'Review derivative credential candidates'
con=sqlite3.connect(T/'historical_instrument_csv_b11.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';count=con.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0];con.close()
(O/'delivery_acceptance.json').write_text(json.dumps(dict(acquisition=a,validation=v,tables=count,derivative_credential_candidates=len(extra),local_only_candidates=excluded,global_complete=False),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(tables=count,credential_candidates=len(extra))))
