from pathlib import Path
import sys,json,csv,sqlite3,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/31_global_directory_content_b06_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T
source=(O.parent/'global_directory_content_b05/structure.py').read_text(encoding='utf-8').replace('registry_directory_all_table_rows.csv','registry_all_table_rows.csv')
exec(compile(source,str(O/'deliver.py'),'exec'))
db=T/'global_directory_content_b06.sqlite';assert not db.exists(),'Preserve completed delivery'
con=sqlite3.connect(db);counts={}
for path in sorted(T.glob('*.csv')):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames
        if not fields:continue
        rows=list(reader);name=path.stem;quote=lambda s:'"'+s.replace('"','""')+'"'
        con.execute('CREATE TABLE '+quote(name)+' ('+','.join(quote(k)+' TEXT' for k in fields)+')')
        con.executemany('INSERT INTO '+quote(name)+' VALUES ('+','.join('?' for _ in fields)+')',[[r.get(k,'') for k in fields] for r in rows]);counts[name]=len(rows)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
a=json.loads((O/'fetch_manifest.json').read_text())['summary'];b=json.loads((O/'pagination_acceptance.json').read_text());c=json.loads((O/'download_acceptance.json').read_text());d=json.loads((O/'structure_acceptance.json').read_text())
report=f'''---
title: "全球多市場名錄採集 B06：160 個網站輪替、分頁與下載證據"
date: 2026-10-08
format:
  html:
    toc: true
    embed-resources: true
---

## 清單進度與邊界

承接全部 4,849 項工作，本輪排除 B05 已抓取網址，對其中 3,705 個仍具公司、證券、會員、牌照等網址訊號的候選來源排序，以網站輪替選取 160 個不同主機各一頁。訊號僅用於排程，不證明內容是完整名錄或官方機構；原始 B04 發現鏈及出處保留，逐頁用途仍須核定。未將每個主機當成一個國家，也未將全球覆蓋數固定為 249。

160 頁中 {a['http200']} 頁 HTTP 200，原始頁面保留 {a['table_rows']} 條物理表格行。額外嘗試 {b['fetched_additional_pages']} 個觀測到的同站分頁，取得 {b['additional_table_rows']} 條行；{b['pending_gap_records']} 條分頁缺口保留。批次最多 100 個追加分頁，跨站與超額項目明確待續，不宣稱所有分頁完成。

## 資料保留與業務價值

共保存 {d['all_table_rows']} 條物理表格行、{d['tables']} 個來源表格，投影 {d['structured_source_records']} 條具角色的來源觀測。公司、證券、基金、清算參與者、法規、價目表及新闻不能混為同一業務實體。表頭歧義、重複表頭、跨網址相同正文、動態空表及錯誤回應可回溯原始 cells_json 或原始回應；投影數量不是全球獨立公司的數量。

本輪 9 個已觀測唯一直接下載連結全部保存：巴西 CVM CRA 證券化申報年度資料 2021–2026、圭亞那 DTC 歷史成交工作簿，以及 SIX XML schema 與 IBT 類型代碼工作簿。共保留 {c['csv_rows']} 條 CSV 物理行（包含表頭）、{c['workbook_rows']} 條 XLSX 行與 {c['archive_members']} 個壓縮成員雜湊。舊 XLS 格式尚未轉成語義表，完整檔案保留。CSV 以分號解析；無法 UTF8 解碼時使用可逆 Latin1 投影並標記來源編碼未核定。

申報資料有助於歷史監管事件和債務工具分析；成交資料有助於單項證券時間序列；技術 schema／代碼資料有助於交換介面與欄位治理。以上均不等於交易所完整發行人或持牌券商母表。來源包括 [CVM CRA 申報目錄](https://dados.cvm.gov.br/dataset/securit-doc-dfin_cra)、[Guyana DTC 證券頁](https://guyanastockexchangeinc.com/security/demerara-tobacco-company-limited/)；保存觀測日期與逐檔 SHA256，不將年度 2026 自動判成全年已完整。

## 交付與後續

[下一批候選](tables/31_global_directory_content_b06_20261008/registry_pending_signal_candidates.csv)、[逐頁核查](tables/31_global_directory_content_b06_20261008/registry_all_page_content_review.csv)、[分頁缺口](tables/31_global_directory_content_b06_20261008/registry_pagination_gaps.csv)、[申報行](tables/31_global_directory_content_b06_20261008/registry_download_csv_rows.csv)、[SQLite](tables/31_global_directory_content_b06_20261008/global_directory_content_b06.sqlite)。SQLite 完整性檢查通過，所有來源回應按雜湊核查；全球所有上市公司、券商與貨幣完整性仍為 UNKNOWN。

原宇航報告、歷史批次及使用者的 Inteligent 文件修改保留。後續需核定來源權威、名錄業務範圍、分頁總數與實體識別，並繼續全部工作列。
'''
(R/'Reference/Global_Directory_Content_Expansion_B06_20261008.qmd').write_text(report,encoding='utf-8')
(O/'delivery_acceptance.json').write_text(json.dumps(dict(fetch=a,pagination=b,downloads=c,structure=d,database_tables=counts,integrity='ok',global_complete=False),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(tables=len(counts),rows=d['all_table_rows'],structured=d['structured_source_records'])))
