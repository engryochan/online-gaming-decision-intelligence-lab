from pathlib import Path
import json,sys,hashlib,csv,sqlite3
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/33_global_workbook_content_b08_20261008'
a=json.loads((O/'extraction_acceptance.json').read_text());b=json.loads((O/'review_acceptance.json').read_text())
qmd=R/'Reference/Global_Workbook_Content_Expansion_B08_20261008.qmd'
text=f'''---
title: "全球工作簿內容補齊 B08：舊 XLS、壓縮工作簿與儲存格對賬"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 本輪結果與來源邊界

承接 B05、B06、B07 已保存的 82 條直接下載回執，逐檔驗證 SHA256，保留全部來源觀測。辨識直接 XLS／OOXML 與壓縮成員，讀取 62 個不同雜湊的工作簿：11 個舊 XLS、51 個 OOXML，98 張工作表。這是既有下載檔的內容補齊，沒有新增交易所來源，也沒有宣稱全球所有公司、券商或貨幣已完成。

保存 {a['rows']:,} 條矩形工作表行、{a['cells']:,} 個儲存格位置。{b['nonempty_rows']:,} 行至少有一個非空值，{b['blank_rows']:,} 行為空行；數字零與空值分開。兩張空工作表的讀取器尺寸是 1×1、迭代器卻沒有行，經重讀原始檔確認後明確保存 null 空行並標記 IMPLICIT_EMPTY_WORKSHEET_RECTANGLE。這兩行不是新增業務記錄。

## 業務類別與價值

莫桑比克央行資料有 3 份歷史微貸營運者工作簿及 8 份歷史金融機構工作簿，保留原始年份與來源網址。它們支持跨年度機構／牌照研究，不能一律認定為證券行或當前有效牌照。另有 PSX 2024 網上券商表、股份收購表、單一證券歷史成交、排除證券表與 SIX 技術代碼表；其他 46 份工作簿的業務範圍仍待核定。分類以明確網址訊號為初步線索，不替代逐欄語義核實。

每個工作簿保留來源雜湊、工作表名稱、位置、可見性、合併範圍、行列尺寸；每行保留原始值、資料類型與數字格式。XLS 日期保留原始序號及日期基準，沒有把識別碼或未核定日期自行轉換。檔案仍保留在原批次，不寫入、另存或重算原工作簿。

## 公式與完整性限制

OOXML 保留 {b['ooxml_formula_cells']} 個公式儲存格的公式文字，另保留讀取器可見的超連結與註解。未執行公式或巨集，未聲稱公式計算值已核定。XLS 使用固定版本 xlrd 2.0.2，僅提取公式快取結果；公式文字、巨集、圖表與不受支援的物件仍須回溯原始檔。[xlrd 官方說明](https://xlrd.readthedocs.io/en/latest/)明確列出這些讀取限制。

98 張工作表逐項對賬通過，行號連續、每行列數與讀取器回報尺寸一致，原始型別中的錯誤儲存格數為 {b['error_typed_cells']}。這是機械抽取核查，不代表每個數值、公司名稱或牌照狀態已實質核實。壓縮深度、成員尺寸上限与非工作簿成員另列審核表，PDF／XML 等其他內容不在本輪解碼範圍。

## 可查詢交付與待續清單

[工作簿回執](tables/33_global_workbook_content_b08_20261008/registry_workbook_manifest.csv)、[來源觀測](tables/33_global_workbook_content_b08_20261008/registry_workbook_observations.csv)、[儲存格行](tables/33_global_workbook_content_b08_20261008/registry_workbook_rows.csv)、[工作表對賬](tables/33_global_workbook_content_b08_20261008/registry_worksheet_reconciliation.csv)、[業務範圍](tables/33_global_workbook_content_b08_20261008/registry_workbook_business_scope.csv)、[SQLite](tables/33_global_workbook_content_b08_20261008/global_workbook_content_b08.sqlite)。資料庫有 8 表，PRAGMA integrity_check 通過。原始資料、型別陣列及格式陣列均可查詢，不把公式／空行計入公司總數。

全球逐國金融清單與 B07 待審分頁仍保留。後續需核定各表欄位、行的業務粒度、年度重複、實體識別與當前監管狀態，再接續未取得的官方名錄。全球完整性仍為 UNKNOWN。兩份受保護報告未改寫；Inteligent 文件現有修改完整保留並排除本輪提交。
'''
qmd.write_text(text,encoding='utf-8')
ignore=R/'.gitignore';old=ignore.read_text(encoding='utf-8');rule='/reports/2026-10-08/global_workbook_content_b08/local_runtime/'
if rule not in old:ignore.write_text(old+'\n# B08 isolated local XLS reader; reproducible via pinned requirements\n'+rule+'\n',encoding='utf-8')
(O/'requirements-local.txt').write_text('xlrd==2.0.2\n',encoding='utf-8')
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
source=(O.parent/'global_directory_content_b05/security.py').read_text(encoding='utf-8')
source=source.replace("and '__pycache__' not in path.parts","and '__pycache__' not in path.parts and 'local_runtime' not in path.parts").replace('Global_Directory_Content_Expansion_B05','Global_Workbook_Content_Expansion_B08')
exec(compile(source,str(O/'deliver.py'),'exec'))
assert not findings,'Review derivative credential candidates before publication'
with (T/'registry_workbook_rows.csv').open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f);csvcount=0
    for row in reader:
        assert len(json.loads(row['values_json']))==len(json.loads(row['types_json']))==len(json.loads(row['formats_json']));csvcount+=1
assert csvcount==a['rows']
con=sqlite3.connect(T/'global_workbook_content_b08.sqlite');assert con.execute('SELECT count(*) FROM workbook_rows').fetchone()[0]==csvcount;assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
(O/'delivery_acceptance.json').write_text(json.dumps(dict(extraction=a,review=b,csv_database_rows_reconciled=csvcount,credential_candidates=0,global_complete=False),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(rows=csvcount,credential_candidates=0)))
