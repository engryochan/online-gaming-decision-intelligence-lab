from pathlib import Path
O=Path(__file__).resolve().parent
source=(O.parent/'global_directory_content_b06/deliver.py').read_text(encoding='utf-8')
source=source[:source.index("a=json.loads")].replace('31_global_directory_content_b06','32_global_directory_content_b07').replace('global_directory_content_b06.sqlite','global_directory_content_b07.sqlite')
if (O.parents[2]/'Reference/tables/32_global_directory_content_b07_20261008/global_directory_content_b07.sqlite').exists():
    source=source[:source.index("db=T/")]+'''\ncon=sqlite3.connect(T/'global_directory_content_b07.sqlite')
counts={}
for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    counts[name]=con.execute('SELECT count(*) FROM "'+name+'"').fetchone()[0]
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
con.close()
'''
exec(compile(source,str(O/'deliver.py'),'exec'))
a=json.loads((O/'fetch_manifest.json').read_text())['summary'];b=json.loads((O/'pagination_acceptance.json').read_text());c=json.loads((O/'download_acceptance.json').read_text());d=json.loads((O/'structure_acceptance.json').read_text())
baseline=json.loads((O/'baseline.json').read_text())
protected_review=[]
for p,digest in baseline['protected'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest()
    if 'Inteligent_' not in p:assert current==digest,p
    protected_review.append(dict(path=p,baseline_sha256=digest,current_sha256=current,unchanged=current==digest,action='PRESERVED_NO_BATCH_WRITE'))
(O/'protected_file_review.json').write_text(json.dumps(protected_review,indent=2)+'\n',encoding='utf-8')
report=f'''---
title: "全球名錄施工 B07：未處理網站、分頁辨識與多語下載"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 本轮施工範圍

承接完整 4,849 項工作，排除 B05/B06 已嘗試網址，排序 3,545 個仍具名錄關鍵詞訊號的候選，優先先前採集较少的網站，選取 180 個不同主機。取得 {a['http200']} 個 HTTP 200 回應及 {a['table_rows']} 條來源表格行。主機不是國家；關鍵詞不證明來源權威或名錄完整，原始來源發現鏈均保留供核定。HTTP 200 不代表已收齊內容。

## 分頁候選校對

上一批寬泛的 pager／pagination CSS 容器可能包含一般導覽與社群連結，不能直接當成待採集的真正分頁。本輪合併既有缺口與新候選共 {b['candidate_observations']} 條觀測；保留所有舊記錄並新增逐項判定，{b['candidate_review_reasons'].get('NAVIGATION_LINK_NOT_CONFIRMED_PAGINATION',0)} 條標為尚未確認分頁的導覽，{b['candidate_review_reasons'].get('ALREADY_ATTEMPTED_IN_PRIOR_OR_CURRENT_BATCH',0)} 條已嘗試過。

本輪採集 {b['fetched_additional_pages']} 條含明確頁碼／下一頁訊號的連結，保留 {b['additional_table_rows']} 條行。明確訊號仍不證明它是公司名錄，須核定來源用途。這些新頁又產生 {b['new_link_observations_pending_review']} 條容器連結觀測，另存待審，未宣稱分頁已全部完成，也不把舊的 3,084 條缺口整批認定為有效分頁。

## 下載證據與資料類型

觀測到 65 條下載連結、64 個唯一 URL，全部保存。莫桑比克央行歷年金融機構名錄等 11 個重音檔名網址曾失敗，百分比編碼後成功；保留初次失敗與重試回執。不同年份名錄不等於本年度牌照完整表。共有 {c['workbook_rows']} 條 XLSX 工作簿物理行（含表頭與空行），{c['archive_members']} 個已檢查 ZIP 成員雜湊；舊 XLS、壓縮內工作簿與其他格式的語義抽取仍待處理，原始檔保留，不聲稱全部檔案均已完成內容核實。

## 結構與業務定義

本輪合計 {d['all_table_rows']} 條表格物理行、{d['tables']} 個來源表格，投影 {d['structured_source_records']} 條來源記錄。投影是表頭辨識後的初步欄位整理，並非核定上市公司數；基金、牌照、監管事件、新聞、技術字典、清算會員及歷史記錄需分別確認業務定義。原始 cells_json、表頭、連結與回應保留，重複表頭及翻譯差異可回溯。

## 可續作交付

[逐項候選](tables/32_global_directory_content_b07_20261008/registry_pending_signal_candidates.csv)、[分頁校對](tables/32_global_directory_content_b07_20261008/registry_pagination_candidate_review.csv)、[新分頁連結待審](tables/32_global_directory_content_b07_20261008/registry_pagination_link_observations.csv)、[逐檔回執](tables/32_global_directory_content_b07_20261008/direct_file_fetch_manifest.csv)、[SQLite](tables/32_global_directory_content_b07_20261008/global_directory_content_b07.sqlite)。資料庫有 {len(counts)} 表，完整性核查通過。

您的提交 7137580 保留；施工期間偵測到 Inteligent 文件另有修改，已記錄基線及現行雜湊，不覆写或納入本輪提交。兩份宇航／地緣報告基線雜湊核對通過。本輪新增獨立交付，不覆寫原批次。全球每個國家／歷史政治實體、上市公司、券商與貨幣仍未收齊；完整性為 UNKNOWN，下一步仍需逐來源總量、格式解碼、日期與實體對賬。
'''
(R/'Reference/Global_Directory_Content_Expansion_B07_20261008.qmd').write_text(report,encoding='utf-8')
(O/'delivery_acceptance.json').write_text(json.dumps(dict(fetch=a,pagination=b,downloads=c,structure=d,database_tables=counts,integrity='ok',protected_file_review=protected_review,global_complete=False),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(tables=len(counts),rows=d['all_table_rows'],structured=d['structured_source_records'])))
