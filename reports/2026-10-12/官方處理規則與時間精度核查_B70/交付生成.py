from pathlib import Path
from pypdf import PdfReader
import json,csv,hashlib,re
工作=Path(__file__).resolve().parent;根=工作.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'))
assert all(H((根/p).read_bytes())==h for p,h in 基['既有正文'].items()),'既有正文已變更'
結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'));pdf=PdfReader(工作/'原始來源/2026年官方常見問題.pdf')
assert len(pdf.pages)==11 and 'May 2026' in pdf.pages[0].extract_text()
assert 'nearest whole minute' in pdf.pages[2].extract_text()
html=(工作/'原始來源/2026年官方元資料.html').read_text(encoding='utf-8');assert 'one-minute sample rate' in html
readme=(工作/'原始來源/官方倉庫固定版本說明.md').read_text(encoding='utf-8');assert 'experimental' in readme.lower()
表=根/'Reference/tables/92_官方處理規則與時間精度核查_B70_20261012'
行=[
 {'核查項':'官方FAQ封面日期','來源':'官方常見問題第1頁','中譯判定':'封面為2026年5月；不以網頁索引題名代替文件實際日期','證據等級':'VERIFIED（已核實文件文字）','限制':'封面日期不是本次取得日期'},
 {'核查項':'降採樣描述','來源':'官方常見問題第3頁','中譯判定':'來源描述按接近整分鐘降採樣；未在本段明定如何選取並列記錄或是否改寫輸出時間','證據等級':'VERIFIED（已核實文件文字）','限制':'不可推定全部輸出秒數為零'},
 {'核查項':'元資料處理步驟','來源':'2026年元資料80362','中譯判定':'描述一分鐘採樣、欄位篩選、資料庫載入、屬性補核及逐日輸出；輸出時間轉為協調世界時字串','證據等級':'VERIFIED（已核實文件文字）','限制':'沒有據此確定並列鍵選取或合併規則'},
 {'核查項':'輸出時間精度實測','來源':'2026年6月30日完整日檔','中譯判定':f"全部{結['資料行']}行中{結['秒數非零行']}行秒數非零，微秒非零0行；不支持輸出全部取整分鐘",'證據等級':'VERIFIED（全量實測）','限制':'不證明具體採樣算法，也不直接判定時間錯誤'},
 {'核查項':'官方倉庫資料產品區別','來源':'固定版本官方README（倉庫說明）','中譯判定':'實驗地理列式資料產品另有額外清理；不推定其規則等同2026年壓縮逗號分隔日檔','證據等級':'VERIFIED（已核實文件文字）','限制':'未取得2026年日檔處理程式與設定'},
 {'核查項':'同鍵異值合併方式','來源':'本輪審閱的官方FAQ、元資料及倉庫說明','中譯判定':'尚未取得適用本日檔、可重現的同鍵並列選取或合併規則','證據等級':'UNKNOWN（待核實）','限制':'只限本輪已審閱文件；不是宣告所有官方來源皆無規則'}]
with (表/'官方描述與全量實測對照.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(行[0]));w.writeheader();w.writerows(行)
報='''---
title: "第七十批：官方處理規則與完整日檔時間精度核查"
lang: zh-TW
format: html
---

本輪核對最新提交後，以當前官方文件與已取得的2026年6月30日完整 AIS（船舶自動識別系統）日檔對照，不覆寫前批結果，也不修改原始時間值。

## 全量時間精度

'''+f"完整核查 {結['資料行']:,} 行：秒數為零 {結['秒數為零行']:,} 行，非零 {結['秒數非零行']:,} 行（{100*結['秒數非零行']/結['資料行']:.6f}%），微秒非零 0 行。來源 SHA256（安全雜湊算法）與第六十四批完整下载回執一致。\n\n"+'''一分鐘採樣率、選取接近整分鐘的觀測、以及把輸出時間戳取整，是不同操作。本次結果不支持「所有輸出時間戳秒數為零」；不能因秒數非零而直接把資料判作錯誤，也不能據此推定真實採樣程式。

## 官方文件對照

[官方常見問題](https://coast.noaa.gov/data/marinecadastre/ais/faq.pdf)共11頁，封面為2026年5月，第3頁的降採樣文字涉及接近整分鐘；本輪保留這項描述，將其與實際輸出時間分開記錄。

[2026年元資料](https://www.fisheries.noaa.gov/inport/item/80362)描述一分鐘採樣、欄位篩選、資料庫載入及逐日輸出，時間轉為 UTC（協調世界時）字串；這些文字未使本輪取得可重現的同鍵並列選取規則。

[官方倉庫](https://github.com/ocm-marinecadastre/ais-vessel-traffic)區分實驗 GeoParquet（地理列式儲存格式）產品的额外清理；其說明不應自動套用到不同版本的壓縮日檔。本輪固定倉庫提交保存說明，避免以浮動分支引用取代版本證據。

## 保留與待完成事項

前兩批的1,220行精確重複額外記錄、七組同鍵異值仍保留。這次澄清了整分鐘時間戳假設的適用限制，沒有查明異值根因，沒有取得選取真實版本的規則；不任意選取一行、不修剪或取整原時間。

逐秒彙總、六項官方描述對照見 `tables/92_官方處理規則與時間精度核查_B70_20261012/`；四份原始回應與取得時間、標頭、雜湊、固定倉庫版本見 `reports/2026-10-12/官方處理規則與時間精度核查_B70/`。全年品質、逐用途授權及全球覆蓋仍待核實。
'''
(根/'Reference/官方處理規則與時間精度核查_B70_20261012.qmd').write_text(報,encoding='utf-8')
源="from pathlib import Path\n__file__ = str(Path.cwd() / '取得與核查.py')\n"+(工作/'取得與核查.py').read_text(encoding='utf-8')
筆={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3（Python第三版）','language':'python','name':'python3'}},'cells':[{'cell_type':'markdown','metadata':{},'source':['# 官方規則與全量時間精度\n','下列保存本輪實際脚本。原脚本禁止刷新基線；重新取得須另立新批次，不能覆寫本輪證據。']},{'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':源.splitlines(True)}]}
(工作/'時間精度核查筆記本.ipynb').write_text(json.dumps(筆,ensure_ascii=False,indent=2),encoding='utf-8')
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd';原=(根/主).read_bytes()
追加=('\n\n## 第七十批有界增補：採樣頻率與輸出時間精度\n\n完整核查2026年6月30日10,622,482行，其中10,456,006行秒數非零、166,476行為零、微秒非零0行。一分鐘採樣不直接等於输出時間全部取整；官方文件與全量實測分開保存，不改原時間。尚未核定同鍵合併規則、異值根因及全球覆蓋。詳見[第七十批報告](官方處理規則與時間精度核查_B70_20261012.qmd)。\n').encode('utf-8')
(根/主).write_bytes(原+追加)
(工作/'附加收據.json').write_text(json.dumps({'主報告':主,'原文位元組':len(原),'原文雜湊':H(原),'附加雜湊':H(追加)},ensure_ascii=False,indent=2),encoding='utf-8')
print('官方文件對照、中文報告與有界增補已生成。')
