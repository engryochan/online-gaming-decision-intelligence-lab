from pathlib import Path
import sys,json,csv,hashlib,sqlite3
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/37_global_directory_content_b12_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
intake.write('pagination_fetch_manifest.csv',[]);intake.write('registry_pagination_all_table_rows.csv',[])
for src,dest,kind in [('registry_download_links.csv','registry_download_observations_pending_review.csv','DOWNLOAD_URL_OBSERVATION_NOT_YET_ACQUIRED'),('registry_pagination_links.csv','registry_page_link_observations_pending_review.csv','LINK_OBSERVATION_PAGINATION_NOT_YET_VERIFIED')]:
    rows=list(csv.DictReader((T/src).open(encoding='utf-8-sig')))
    intake.write(dest,[dict(**r,review_status=kind) for r in rows])
exec(compile((O/'ledger.py').read_text(encoding='utf-8'),str(O/'ledger.py'),'exec'))
s=(O.parent/'global_directory_content_b06/deliver.py').read_text(encoding='utf-8').split('a=json.loads')[0].replace('31_global_directory_content_b06','37_global_directory_content_b12').replace('global_directory_content_b06.sqlite','global_directory_content_b12.sqlite')
exec(compile(s,str(O/'deliver.py'),'exec'))
a=json.loads((O/'fetch_manifest.json').read_text())['summary'];d=json.loads((O/'structure_acceptance.json').read_text());e=json.loads((O/'ledger_acceptance.json').read_text())
verified=0
for row in csv.DictReader((T/'directory_fetch_manifest.csv').open(encoding='utf-8-sig')):
    if row.get('file'):
        assert hashlib.sha256((R/row['file']).read_bytes()).hexdigest()==row['sha256'];verified+=1
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for p,h in baseline['protected'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest()
    if 'Inteligent' not in p:assert current==h
    protected.append(dict(path=p,baseline_sha256=h,current_sha256=current,action='NO_WRITE'))
assert e['original_queue']==4849 and e['country_mother_rows']==249
report=f'''---
title: "全球多市場施工 B12：續採未處理網站及完整工作進度"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 實測交付

承接全部 4,849 項原始工作列，排除 B05、B06、B07、B10 已嘗試的網址，依路徑與查詢參數名錄訊號排序，優先先前較少採集的主機。本輪嘗試 {a['selected']} 個網址、{a['hosts']} 個不同主機，其中 {a['http200']} 個 HTTP 200；保留 {d['all_table_rows']} 條物理表格行、{d['tables']} 個表格、{d['structured_source_records']} 條初步角色投影。投影不是獨立上市公司或持牌券商數，網址訊號不是權威性證明。

## 全清單與逐國進度

所有 4,849 項工作列與 249 條現行國家／地區母表完整保留。累計狀態為 `{json.dumps(e['state_counts'],ensure_ascii=False)}`。逐國表沿用 MIC 網站與 ANNA 前綴來源關係，不將主機等同公司註冊地或國家完整覆蓋；歷史政治實體沿用既有資料，249 並非歷史國家總量上限。

新觀測 {a['download_observations']} 條下載連結及 {a['pagination_observations']} 條頁面連結，全部列入後續核查表。本輪未宣稱這些下載已取得或所有連結都是分頁；須核定重複、來源用途、完整範圍及實際頁碼。B11 已交付的 1,848 個歷史 CSV 保留，不用重複下載增加覆蓋數。

## 可回溯數據及價值

[來源收據](tables/37_global_directory_content_b12_20261008/directory_fetch_manifest.csv)、[全部工作進度](tables/37_global_directory_content_b12_20261008/registry_all_4849_work_progress.csv)、[逐國來源進度](tables/37_global_directory_content_b12_20261008/registry_all_country_cumulative_source_progress.csv)、[原始表格行](tables/37_global_directory_content_b12_20261008/registry_all_table_rows.csv)、[來源語義覆核](tables/37_global_directory_content_b12_20261008/registry_source_table_semantic_review.csv)、[SQLite](tables/37_global_directory_content_b12_20261008/global_directory_content_b12.sqlite)。逐頁來源 URL、原始 cells_json、HTTP 狀態、截斷標記與 SHA256 保留，用於公司、證券、會員或牌照資料的後續辨識及去重，動態空表與非名錄內容仍待判定。

SQLite 完整性及 CSV 行數入庫核對通過；{verified} 個已保存回應的原始位元組雜湊核對通過。舊批次、兩份主報告與使用者修改均未覆寫。全球所有上市公司、券商、貨幣與科技資料完整性仍為 UNKNOWN，不能以 HTTP 200 代替內容完整性驗收。
'''
(R/'Reference/Global_Directory_Content_Expansion_B12_20261008.qmd').write_text(report,encoding='utf-8')
(O/'delivery_acceptance.json').write_text(json.dumps(dict(fetch=a,structure=d,ledger=e,sqlite_counts=counts,raw_verified=verified,protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(fetch=a,structure=d,ledger=e),ensure_ascii=False))
