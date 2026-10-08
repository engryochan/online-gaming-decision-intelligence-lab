from pathlib import Path
import sys,csv,json,hashlib,sqlite3,collections
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/42_global_directory_followup_b17_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
intake.write('directory_fetch_manifest.csv',[]);intake.write('registry_all_table_rows.csv',[])
s=(O.parent/'global_directory_content_b16/ledger.py').read_text(encoding='utf-8').replace("T=R/'Reference/tables/41_global_directory_content_b16_20261008'","T=R/'Reference/tables/42_global_directory_followup_b17_20261008'").replace("'41_global_directory_content_b16_20261008']","'41_global_directory_content_b16_20261008','42_global_directory_followup_b17_20261008']")
(O/'ledger.py').write_text(s,encoding='utf-8');exec(compile(s,str(O/'ledger.py'),'exec'))
reviews=[]
for r in read(T/'direct_file_fetch_manifest.csv'):
    u=r['url'];low=u.lower();role='SOURCE_FILE_SCOPE_REVIEW'
    if 'inf_mensal_ots' in low:role='BRAZIL_OTS_MONTHLY_REGULATORY_REPORT_OR_DICTIONARY_NOT_ALL_LISTED_COMPANIES'
    elif 'annual_report' in low:role='BULGARIA_CSD_SETTLEMENT_FAILURE_ANNUAL_REPORT'
    elif 'nodal_exchange_contracts' in low:role='DERIVATIVE_CONTRACT_DIRECTORY_NOT_LEGAL_ENTITY_DIRECTORY'
    elif 'limits_and_levels' in low:role='CONTRACT_REPORTING_AND_POSITION_LIMITS'
    elif 'designated_individuals' in low:role='HISTORICAL_DESIGNATED_INDIVIDUALS_AND_ENTITIES_NOT_LICENSEES'
    elif any(x in low for x in ['declaration','registration-format','sample-performance','contacts-list','forms_membership']):role='FORM_OR_TEMPLATE_NOT_REGISTERED_ENTITY_LIST'
    elif 'instructions' in low:role='PARTICIPANT_INSTRUCTIONS_ARCHIVE'
    elif 'etptier1' in low:role='EXCHANGE_TRADED_PRODUCT_CLASSIFICATION_SCOPE_REVIEW'
    elif 'bandwidthreport' in low:role='TECHNICAL_BANDWIDTH_REPORT'
    elif 'membership' in low and 'members.xlsx' in low:role='EXCHANGE_MEMBER_LIST_SCOPE_AND_DATE_REVIEW'
    elif 'monthly-funds-report' in low:role='HISTORICAL_MONTHLY_FUNDS_REPORT_NOT_COMPANY_DIRECTORY'
    elif 'cboe-listed-volume' in low:role='LISTED_INSTRUMENT_VOLUME_NOT_LEGAL_ENTITY_LIST'
    elif 'otc.nfmf.no' in low:role='HISTORICAL_COMPANY_FINANCIAL_WORKBOOK'
    elif 'guyanastockexchange' in low:role='INDIVIDUAL_SECURITY_HISTORICAL_TRADES'
    elif 'online-brokers' in low:role='HISTORICAL_ONLINE_ACCOUNT_OPENING_BROKER_SUBSET'
    elif 'samples' in low or 'form.xlsx' in low:role='FORM_OR_TEMPLATE_NOT_REGISTERED_ENTITY_LIST'
    reviews.append(dict(**r,business_role_review=role,content_verified='BODY_HASH_ONLY_SEMANTICS_PENDING',completeness='UNKNOWN'))
intake.write('registry_file_business_scope_review.csv',reviews)
intake.write('registry_file_acquisition_gaps.csv',[r for r in reviews if r.get('error') or r.get('truncated')=='True'])
s=(O.parent/'global_directory_content_b06/deliver.py').read_text(encoding='utf-8').split('a=json.loads')[0].replace('31_global_directory_content_b06','42_global_directory_followup_b17').replace('global_directory_content_b06.sqlite','global_directory_followup_b17.sqlite')
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
title: "全球清單續作 B17：分頁核查、直接檔案及業務用途"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 本輪完成範圍

接續 B16 的 179 條頁面連結及 B15 的 3,024 條新連結，共覆核 {a['candidate_observations']} 條觀測。分類 `{json.dumps(a['candidate_review_reasons'])}`；去重後嘗試全部 {a['selected_pages']} 个合資格候選網址，HTTP 狀態分布 `{json.dumps(http)}`，保存 {a['additional_table_rows']} 條物理表格行、{d['tables']} 個表格及 {d['structured_source_records']} 條初步來源角色投影。數字、next 與 page 參數僅是分頁排程訊號，並非內容完整性的證明。

新增 {a['new_link_observations_pending_review']} 條連結留待下一輪核查；本轮候選未選數為零不等於全站或所有遞迴分頁完成。所有 4,849 項原始工作列及 249 條現行母表保留，累計工作狀態 `{json.dumps(e['state_counts'])}`。網站來源關係不代表企業註冊地，歷史政治實體仍沿用既有登記。

## 下載與業務定義

全部 {b['download_observations']} 條直接檔案觀測去重為 {b['unique_links']} 個網址，全部嘗試；{b['saved_or_reused']} 個保存或沿用已核對的原始檔，其中 {b['reused']} 個沿用、{b['new_saved']} 個新增，{b['remaining_errors']} 個失敗保留逐檔錯誤及 HTTP 狀態。保存 {b['archive_members']} 個壓縮成員雜湊、{b['workbook_rows']} 條 XLSX 行及 {b['csv_rows']} 條直接 CSV 邏輯行（含表頭與空行）。

來源觀測包括巴西 CVM OTS 月報與元數據、圭亞那單項證券歷史成交資料、監管網站歷史指定人士／實體清單及會員申請／聯絡表。它們服務於歷史申報、工具交易、合規證據及流程分析；逐檔內容、時點及監管範圍仍須核定。會員申請範本。分別服務於交易所參與者、產品交易、歷史申報與公司財務分析；名稱與網址僅作用途初步分類，逐檔內容、時點與監管範圍仍待核定。會員申請範本、技術頻寬報告、歷史制裁名單及產品分類不能合算為持牌券商或上市公司；逐檔業務用途寫入覆核表。

本輪額外展開 CVM 原始壓縮檔內全部 32 個 CSV 成員，保存 53,758 條邏輯來源行（包含表頭與空行），並保存 8 個文字／字典成員。逐成員雜湊、編碼策略、分隔符與行数已核對；可回溯 cells_json，不將申報行當作獨立公司數。UTF8 解碼失敗時採用可逆 Latin1 投影並標記來源編碼尚未核定。PDF、完整工作簿物件及字典語義仍待後續檢查。全球名錄完整性仍為 UNKNOWN。

## 可回溯交付

[分頁候選覆核](tables/42_global_directory_followup_b17_20261008/registry_pagination_candidate_review.csv)、[分頁收據](tables/42_global_directory_followup_b17_20261008/pagination_fetch_manifest.csv)、[逐檔用途](tables/42_global_directory_followup_b17_20261008/registry_file_business_scope_review.csv)、[下載缺口](tables/42_global_directory_followup_b17_20261008/registry_file_acquisition_gaps.csv)、[完整工作進度](tables/42_global_directory_followup_b17_20261008/registry_all_4849_work_progress.csv)、[SQLite](tables/42_global_directory_followup_b17_20261008/global_directory_followup_b17.sqlite)。

{verified} 個原始回應／下載收據位元組雜湊核對通過，SQLite 完整性檢查通過，來源 URL、原始行及內容雜湊可回溯。既有批次、兩份主報告及使用者文件修改未覆寫。
'''
(R/'Reference/Global_Directory_Followup_B17_20261008.qmd').write_text(report,encoding='utf-8')
(O/'delivery_acceptance.json').write_text(json.dumps(dict(pagination=a,downloads=b,structure=d,ledger=e,sqlite_counts=counts,raw_verified=verified,protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(pagination=a,downloads=b,structure=d,ledger=e),ensure_ascii=False))
