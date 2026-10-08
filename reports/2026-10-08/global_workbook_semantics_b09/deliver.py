from pathlib import Path
import json,sys,sqlite3,csv,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/34_global_workbook_semantics_b09_20261008';P=R/'Reference/tables/33_global_workbook_content_b08_20261008'
a=json.loads((O/'build_acceptance.json').read_text());qmd=R/'Reference/Global_Workbook_Semantics_Expansion_B09_20261008.qmd'
text=f'''---
title: "全球工作簿語義施工 B09：業務粒度、重複候選與日期核查"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 本輪結果

承接 B08 全部 62 份工作簿、98 張工作表，保留 27,825 條原始行及型別／格式資料。新增逐行語義側表，投影 {a['business_records']:,} 條來源業務觀測；它們包含機構、產品、交易、技術代碼與歷史名錄，不能解讀成同等數量的公司、券商或當前牌照。

新整合庫複製 B08 的全部 8 表並新增 7 表，共 15 表；B08 庫與 CSV 不覆寫。原始行數逐項對賬，未投影行仍可查詢。源表中的空白字串與僅含空白的字串按語義側表分類，原始值不更改；因此語義空行數與 B08 機械非空計數的口徑不同。

## 修正業務分類

原先 8 份初步「金融機構」工作簿，實際分成 5 份機構名錄、1 份銀行代理網點及 2 份銀行分布矩陣；銀行網點、地區統計不能當成獨立金融公司。原先 46 份待定工作簿，按網址、表頭與正文進一步標為 44 份 PRIIPs 基金份額情境表、1 份指定個人／實體歷史名錄、1 份空白會員 GST 登記模板。舊初步分類仍保留作歷史回溯，新側表記錄修正。

微貸工作簿按工作表拆分：歷史營運者表、拒批申請、黑名單、地區彙總與註解。未找到可靠表頭的黑名單行保留於未投影區，不從其他表猜填欄名。源檔寫有黑名單或拒批，只表示該歷史來源記錄，未認定今天的監管或法律狀態。[莫桑比克央行牌照入口](https://www.bancomoc.mz/en/areas-of-expertise/licensing/licensing-of-institutions/)亦區分機構及微貸相關資料。

[Goodbody 基金頁](https://www.goodbody.ie/asset-management/dividend-income-balanced-fund/)的情境資料與 [BDCB 指定名錄入口](https://www.bdcb.gov.bn/aml-cft/information-for-reporting-institutions)用途不同。本輪分別保存 343 條情境觀測及 476 條指定名錄來源觀測，不併入持牌公司表，也不重新斷言任何個人的當前狀態。

## 重複與機構識別

保留 {a['candidate_groups']:,} 個文字匹配候選組，其中 {a['repeated_candidate_groups']:,} 組有多次觀測；另標記 {a['exact_repeat_groups']:,} 組原始值及型別完全重複的來源行。所有來源位置與重複行均保留，沒有刪除重複或建立已核定法律實體 ID。

候選鍵使用業務角色、名稱、商號與來源識別碼。名稱只做 Unicode 相容正規化、大小寫與空白整理，不移除名稱中的重音、不模糊合併。基金 ISIN、券商來源代碼、制裁參考碼、技術代碼及交易助記碼仍屬不同業務粒度；候選組數不是公司總數。跨年度相同名称只是待核對線索，不能證明法律實體、延續牌照或同一分支。

## 日期與欄位

逐欄保留原始表頭、儲存格位置、原始值與型別，重複表頭不壓成單一字典。工作簿名年份、網址年份與工作表歷史年份分別保存；例如 2025 下載檔可含 2023 歷史表，不能一律套用網址年份作有效日期。

抽取 {a['date_fields']:,} 個日期欄位觀測，按明確格式或 Excel 日期型別／工作簿基準生成 {a['parsed_dates']:,} 個 ISO 日期投影；其餘 {a['date_fields']-a['parsed_dates']} 個保留原值待審。Excel 虛構的 1900-02-29 不轉成真實日期。數字識別碼不按日期欄外推。日期投影是格式核查，不是事件日期真實性驗證。

多行表頭與無表頭資料仍須專項核對，本輪以已觀測到的精確表頭詞識別作初步投影。公式、統計值及單一證券成交觀測保留原業務角色，未評估未取得證據的真偽。

## 交付與後續

[工作簿分類修正](tables/34_global_workbook_semantics_b09_20261008/registry_workbook_scope_review.csv)、[工作表表頭](tables/34_global_workbook_semantics_b09_20261008/registry_sheet_schema_review.csv)、[逐行語義](tables/34_global_workbook_semantics_b09_20261008/registry_row_semantic_classification.csv)、[來源業務觀測](tables/34_global_workbook_semantics_b09_20261008/registry_source_business_records.csv)、[候選身份組](tables/34_global_workbook_semantics_b09_20261008/registry_candidate_identity_groups.csv)、[日期投影](tables/34_global_workbook_semantics_b09_20261008/registry_date_projections.csv)、[SQLite](tables/34_global_workbook_semantics_b09_20261008/global_workbook_semantics_b09.sqlite)。

全球逐國名錄、B07 分頁與尚未取得來源的清單仍待續；本輪沒有新增交易所來源。全球所有國家／歷史政治實體、公司、券商及貨幣的完整性仍為 UNKNOWN。兩份受保護報告不改寫，Inteligent 文件修改保留並排除提交。
'''
qmd.write_text(text,encoding='utf-8')
con=sqlite3.connect(T/'global_workbook_semantics_b09.sqlite');old=sqlite3.connect('file:'+str(P/'global_workbook_content_b08.sqlite')+'?mode=ro',uri=True)
checks=[]
for (name,) in old.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    before=hashlib.sha256();after=hashlib.sha256();count=0
    for row in old.execute('SELECT * FROM "'+name+'" ORDER BY rowid'):before.update((json.dumps(row,ensure_ascii=False,default=str)+'\n').encode());count+=1
    for row in con.execute('SELECT * FROM "'+name+'" ORDER BY rowid'):after.update((json.dumps(row,ensure_ascii=False,default=str)+'\n').encode())
    assert before.digest()==after.digest(),name;checks.append(dict(table=name,rows=count,logical_sha256=before.hexdigest(),preserved=True))
newcounts={}
for path in T.glob('*.csv'):
    with path.open(encoding='utf-8-sig',newline='') as f:count=sum(1 for row in csv.DictReader(f))
    assert con.execute('SELECT count(*) FROM "'+path.stem+'"').fetchone()[0]==count;newcounts[path.stem]=count
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close();old.close()
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
source=(O.parent/'global_directory_content_b05/security.py').read_text(encoding='utf-8').replace('Global_Directory_Content_Expansion_B05','Global_Workbook_Semantics_Expansion_B09')
exec(compile(source,str(O/'deliver.py'),'exec'));assert not findings,'Review credential candidates'
(O/'delivery_acceptance.json').write_text(json.dumps(dict(summary=a,inherited_table_checks=checks,new_csv_database_counts=newcounts,integrity='ok',credential_candidates=0),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(inherited_tables_verified=len(checks),new_tables_reconciled=len(newcounts))))
