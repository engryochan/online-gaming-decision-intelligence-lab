from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent
source=(O.parent/'global_directory_content_b06/deliver.py').read_text(encoding='utf-8')
source=source[:source.index("a=json.loads")].replace('31_global_directory_content_b06','35_global_directory_content_b10').replace('global_directory_content_b06.sqlite','global_directory_content_b10.sqlite')
exec(compile(source,str(O/'deliver.py'),'exec'))
a=json.loads((O/'fetch_manifest.json').read_text())['summary'];b=json.loads((O/'pagination_acceptance.json').read_text());c=json.loads((O/'download_acceptance.json').read_text());d=json.loads((O/'structure_acceptance.json').read_text());e=json.loads((O/'ledger_acceptance.json').read_text())
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for p,digest in baseline['protected'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest()
    if 'Inteligent' not in p:assert current==digest
    protected.append(dict(path=p,baseline_sha256=digest,current_sha256=current,batch_action='NO_WRITE'))
report=f'''---
title: "全球多市場施工 B10：未採集來源、歷史工具檔與逐國進度"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 本輪來源與實測

保留完整 4,849 項原始工作清單。排除 B05/B06/B07 已嘗試網址，依路徑及 query 名錄訊號重新排序 3,073 個候選，優先較少採集的主機，不以網站名稱的 stock／securities 字樣當作整站名錄證據。採集 220 個不同主機各一页，其中 {a['http200']} 個 HTTP 200，保存 {a['table_rows']} 條物理表格行。

從本輪及 B07 待審觀測中再採集 {b['fetched_additional_pages']} 個具明確頁碼訊號的連結，保存 {b['additional_table_rows']} 條行，合計 {d['all_table_rows']} 條行、{d['tables']} 個來源表格，投影 {d['structured_source_records']} 條具角色的來源觀測。原始表頭與所有行均保留；投影不是全球獨立公司的總量，頁面權威、業務範圍、動態資料與總數仍待核定。

## 下載工作清單

本輪觀測 1,911 條直接檔案連結、1,897 個唯一 URL；蒙特婁交易所頁面提供大量歷史 InstrumentsPreview 工具檔。全部 URL 與來源位置納入獨立工作清單。本輪選取全部其他下載主機的觀測連結、蒙特婁按 URL 排序兩端各10項及 options-summary，共 {c['selected_links']} 項；這是明确的分批採集，不等同全歷史文件已收齊，URL 字典序亦不保證嚴格時間序。

成功保存或重用 {c['saved_or_reused']} 項，其中 {c['new_saved']} 個新檔、{c['reused']} 個已取得且雜湊核對的舊檔；{c['remaining_errors']} 項失敗保留回執。尚有 {c['pending_unselected']} 個唯一 URL 未選下載。已有資料不重覆下載，也不以未下載項目填充虛構正文。

保存 {c['csv_rows']:,} 條 CSV 物理行、{c['workbook_rows']:,} 條工作簿物理行、{c['archive_members']} 個壓縮成員觀測。CSV 分隔符按來源樣本辨識，UTF8 不適用時保留可逆 Latin1 投影並標記來源編碼待核定。股票、衍生工具新增事件、基金申報、會員與技術 schema 需分別核定業務定義；不把歷史工具事件全部算成上市公司。壓縮內語義抽取及舊 XLS 等格式另待續。

## 累計工作進度

對 B05、B06、B07、B10 共 {e['total_attempt_receipts']} 份回應回執逐項對賬，涉及 {e['unique_attempted_urls']} 個不同網址；其中包含原始清單以外的補充與分頁 URL。原始 4,849 項清單中：{e['state_counts'].get('HTTP200_CONTENT_AND_UNIVERSE_SCOPE_REVIEW',0)} 項 HTTP 200 且仍待內容／範圍核查，{e['state_counts'].get('FETCH_ERROR_OR_NON200_REVIEW',0)} 項失敗或非200，{e['state_counts'].get('HTTP200_BODY_TRUNCATED_REVIEW',0)} 項200但正文截斷，{e['state_counts'].get('NOT_YET_ATTEMPTED',0)} 項尚未嘗試。不得將911個網址視為911個國家或交易所。

沿用現有 249 條國家／地區母表，新增與 MIC 登記網站、ANNA 前綴網站的來源關聯進度。{e['countries_with_source_association']} 條母表觀測到至少一項這兩類網站關聯；其他母表仍保留。關聯不是當地公司／發行人註冊地證明，也不是覆蓋完成：一個跨國網站可關聯多個國家，ANNA 前綴亦需核定政治／監管管轄語義。不把 ISO 母表當成歷史國家全集或品質認證。

## 可續作交付

[全部4,849項累計進度](tables/35_global_directory_content_b10_20261008/registry_all_4849_work_progress.csv)、[全部下載工作列](tables/35_global_directory_content_b10_20261008/registry_all_download_workqueue.csv)、[逐國來源關聯](tables/35_global_directory_content_b10_20261008/registry_all_country_cumulative_source_progress.csv)、[關聯證據](tables/35_global_directory_content_b10_20261008/registry_source_country_association_evidence.csv)、[CSV行](tables/35_global_directory_content_b10_20261008/registry_download_csv_rows.csv)、[SQLite](tables/35_global_directory_content_b10_20261008/global_directory_content_b10.sqlite)。資料庫共 {len(counts)} 表，完整性檢查通過。

待審分頁連結、新增下载工作與受阻來源均保留。全球每個上市公司、證券行、貨幣與歷史政治實體仍未收齊，完整性為 UNKNOWN。使用者提交 f5548b4 及施工中的任何 Inteligent 修改保留，兩份受保護報告未改寫。
'''
(R/'Reference/Global_Directory_Content_Expansion_B10_20261008.qmd').write_text(report,encoding='utf-8')
(O/'delivery_acceptance.json').write_text(json.dumps(dict(fetch=a,pagination=b,downloads=c,structure=d,ledger=e,database_tables=counts,integrity='ok',protected_files=protected,global_complete=False),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(tables=len(counts),rows=d['all_table_rows'],structured=d['structured_source_records'])))
