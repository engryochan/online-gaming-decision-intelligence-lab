from pathlib import Path
import sys,csv,json,hashlib,sqlite3,collections
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/38_global_directory_followup_b13_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
intake.write('directory_fetch_manifest.csv',[]);intake.write('registry_all_table_rows.csv',[])
s=(O.parent/'global_directory_content_b12/ledger.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/37_global_directory_content_b12_20261008'","T=R/'Reference/tables/38_global_directory_followup_b13_20261008'").replace("'37_global_directory_content_b12_20261008']","'37_global_directory_content_b12_20261008','38_global_directory_followup_b13_20261008']")
(O/'ledger.py').write_text(s,encoding='utf-8');exec(compile(s,str(O/'ledger.py'),'exec'))
reviews=[]
for r in read(T/'direct_file_fetch_manifest.csv'):
    u=r['url'];low=u.lower();role='SOURCE_FILE_SCOPE_REVIEW'
    if 'inf_mensal_cra' in low:role='BRAZIL_CRA_MONTHLY_REGULATORY_REPORT_OR_DICTIONARY_NOT_ALL_LISTED_COMPANIES'
    elif 'annual_report' in low:role='BULGARIA_CSD_SETTLEMENT_FAILURE_ANNUAL_REPORT'
    elif 'nodal_exchange_contracts' in low:role='DERIVATIVE_CONTRACT_DIRECTORY_NOT_LEGAL_ENTITY_DIRECTORY'
    elif 'limits_and_levels' in low:role='CONTRACT_REPORTING_AND_POSITION_LIMITS'
    elif 'designated_individuals' in low:role='HISTORICAL_DESIGNATED_INDIVIDUALS_AND_ENTITIES_NOT_LICENSEES'
    elif any(x in low for x in ['declaration','registration-format','sample-performance','contacts-list','forms_membership']):role='FORM_OR_TEMPLATE_NOT_REGISTERED_ENTITY_LIST'
    elif 'instructions' in low:role='PARTICIPANT_INSTRUCTIONS_ARCHIVE'
    elif 'etptier1' in low:role='EXCHANGE_TRADED_PRODUCT_CLASSIFICATION_SCOPE_REVIEW'
    elif 'bandwidthreport' in low:role='TECHNICAL_BANDWIDTH_REPORT'
    reviews.append(dict(**r,business_role_review=role,content_verified='BODY_HASH_ONLY_SEMANTICS_PENDING',completeness='UNKNOWN'))
intake.write('registry_file_business_scope_review.csv',reviews)
intake.write('registry_file_acquisition_gaps.csv',[r for r in reviews if r.get('error') or r.get('truncated')=='True'])
s=(O.parent/'global_directory_content_b06/deliver.py').read_text(encoding='utf-8').split('a=json.loads')[0].replace('31_global_directory_content_b06','38_global_directory_followup_b13').replace('global_directory_content_b06.sqlite','global_directory_followup_b13.sqlite')
exec(compile(s,str(O/'deliver.py'),'exec'))
verified=0
for name in ['pagination_fetch_manifest.csv','direct_file_fetch_manifest.csv']:
    for row in read(T/name):
        if row.get('file'):assert hashlib.sha256((R/row['file']).read_bytes()).hexdigest()==row['sha256'];verified+=1
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for p,h in baseline['protected'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest();assert h==current
    protected.append(dict(path=p,sha256=current,batch_action='NO_WRITE'))
a=json.loads((O/'pagination_acceptance.json').read_text());b=json.loads((O/'download_acceptance.json').read_text());d=json.loads((O/'structure_acceptance.json').read_text());e=json.loads((O/'ledger_acceptance.json').read_text())
http=collections.Counter(r['http_status'] for r in read(T/'pagination_fetch_manifest.csv'))
report=f'''---
title: "全球清單續作 B13：分頁核查、直接檔案及業務用途"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 本輪完成範圍

接續 B12 的 232 條頁面連結及 B10 的 3,785 條新連結，共覆核 {a['candidate_observations']} 條觀測。分類 `{json.dumps(a['candidate_review_reasons'])}`；去重後嘗試全部 {a['selected_pages']} 个合資格候選網址，HTTP 狀態分布 `{json.dumps(http)}`，保存 {a['additional_table_rows']} 條物理表格行、{d['tables']} 個表格及 {d['structured_source_records']} 條初步來源角色投影。數字、next 與 page 參數僅是分頁排程訊號，並非內容完整性的證明。

新增 {a['new_link_observations_pending_review']} 條連結留待下一輪核查；本轮候選未選數為零不等於全站或所有遞迴分頁完成。所有 4,849 項原始工作列及 249 條現行母表保留，累計工作狀態 `{json.dumps(e['state_counts'])}`。網站來源關係不代表企業註冊地，歷史政治實體仍沿用既有登記。

## 下載與業務定義

全部 {b['download_observations']} 條直接檔案觀測去重為 {b['unique_links']} 個網址，全部嘗試；{b['saved_or_reused']} 個保存或沿用已核對的原始檔，其中 {b['reused']} 個沿用、{b['new_saved']} 個新增，{b['remaining_errors']} 個失敗保留逐檔錯誤及 HTTP 狀態。保存 {b['archive_members']} 個壓縮成員雜湊、{b['workbook_rows']} 條 XLSX 行及 {b['csv_rows']} 條直接 CSV 邏輯行（含表頭與空行）。

來源包括保加利亞 CSD 結算失敗年報、巴西 CVM CRA 月報與元數據、Nodal 衍生工具合約及持倉限制。它們分別服務於歷史結算風險、监管申報、工具條款及交易限制分析。會員申請範本、技術頻寬報告、歷史制裁名單及產品分類不能合算為持牌券商或上市公司；逐檔業務用途寫入覆核表。

ZIP 成員原始內容留在原始壓縮檔，本輪核對成員雜湊，尚未把所有內嵌 CSV/PDF/XML 解析為業務表。舊 XLS 本輪保留原始檔，尚未抽取所有單元格；XLSX 保留可讀行及公式文字，完整工作簿物件仍需後續檢查。全球名錄完整性仍為 UNKNOWN。

## 可回溯交付

[分頁候選覆核](tables/38_global_directory_followup_b13_20261008/registry_pagination_candidate_review.csv)、[分頁收據](tables/38_global_directory_followup_b13_20261008/pagination_fetch_manifest.csv)、[逐檔用途](tables/38_global_directory_followup_b13_20261008/registry_file_business_scope_review.csv)、[下載缺口](tables/38_global_directory_followup_b13_20261008/registry_file_acquisition_gaps.csv)、[完整工作進度](tables/38_global_directory_followup_b13_20261008/registry_all_4849_work_progress.csv)、[SQLite](tables/38_global_directory_followup_b13_20261008/global_directory_followup_b13.sqlite)。

{verified} 個原始回應／下載收據位元組雜湊核對通過，SQLite 完整性檢查通過，來源 URL、原始行及內容雜湊可回溯。既有批次、兩份主報告及使用者文件修改未覆寫。
'''
(R/'Reference/Global_Directory_Followup_B13_20261008.qmd').write_text(report,encoding='utf-8')
(O/'delivery_acceptance.json').write_text(json.dumps(dict(pagination=a,downloads=b,structure=d,ledger=e,sqlite_counts=counts,raw_verified=verified,protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(pagination=a,downloads=b,structure=d,ledger=e),ensure_ascii=False))
