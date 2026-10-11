from pathlib import Path
import json,hashlib,subprocess
工作=Path(__file__).resolve().parent;根=工作.parents[2];名='最新官方資料時效核查_B62_20261011';主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
assert not (工作/'基線.json').exists(),'禁止刷新基線'
H=lambda b:hashlib.sha256(b).hexdigest();原=(根/主).read_bytes();paths=subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0')
基={'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'主報告':主,'原文位元組':len(原),'原文雜湊':H(原),'原有文件':{p:H((根/p).read_bytes()) for p in paths if p.endswith(('.md','.qmd')) and (根/p).is_file()}}
(工作/'基線.json').write_text(json.dumps(基,ensure_ascii=False,indent=2),encoding='utf-8')
文='''## 日期與時效校訂

2019年是前批歷史樣本的觀測年份，不是本次查證年份。本批改為核對截至2026年10月11日實際可取得的官方目錄；沒有擴大2019年度下載。原歷史核查、原始收據及使用者修改均保留。

|資料|觀測時段或檔名日期範圍|來源更新／發布日期|本次實測|
|---|---|---|---|
|[2025年位置目錄](https://noaaocm.blob.core.windows.net/ais/csv2/csv2025/index.html)|2025年1月1日至12月31日，檔名日期|2026年3月24日，目錄顯示檔案修改時間|365個日檔連結、365個不同日期，全年目錄日期無缺失或重複|
|[2026年位置目錄](https://noaaocm.blob.core.windows.net/ais/csv2/csv2026/index.html)|2026年1月1日至6月30日，檔名日期|2026年8月26日至9月18日，目錄顯示檔案修改時間|181個日檔連結、181個不同日期，列出區間內無缺失或重複|
|[2026年航跡元資料](https://www.fisheries.noaa.gov/inport/item/80415)|2026年1月1日至3月31日，來源宣告|2026年9月30日，來源發布／更新|元資料與現行目錄第一季三個月檔名相符，尚未下載產品內容|

2025與2026年位置檔案採CSV（逗號分隔資料）及Zstandard（Z標準壓縮格式），副檔名為.csv.zst。檔名日期不是逐行觀測日期已核的證據。本批沒有以181日推定2026全年完成，也沒有以目錄365日推定2025全量資料品質通過。

第五十三批「2025年273日」來自當時取得、2026年1月22日更新的摘要快照。保留這個有日期的歷史證據；目前目錄365日是更新後的不同快照，不能繼續把舊快照的273日當作目前目錄上限。

## 多路徑與公開服務

九項公開來源均取得狀態碼200，共保存609條產品連結原項；它們包含跨來源及同頁重複，不能稱作609個唯一產品。現行航跡目錄有重複的2018年連結，保留原目錄而不默默刪除。新舊兩個航跡目錄路徑分別保存，不機械合併或視為同一產品版本。

[地理資訊公開目錄](https://coast.noaa.gov/arcgismc/rest/services/marinecadastre?f=pjson)返回17項服務且未返回服務錯誤。本次僅核服務目錄；不能據此覆蓋先前另一服務路徑要求權杖的證據，也未證明每個圖層可讀、具備逐用途許可或部署性能達標。[關島區域目錄](https://ocmgeodatastor1.blob.core.windows.net/marinecadastre/data/ais/guam/index-guam.html)另列2025年產品，不能外推所有國家及地區都有同類資料。

2026年航跡來源說明使用美國海岸警衛隊陸基接收網絡，時空篩選及操作員狀態輸入會影響航跡。來源列一海里、30分鐘及航行狀態等建軌條件，並按曆日拆分。這些是來源处理規則；位置精度、地理範圍及使用條款尚未由全量資料實測核定，不能升格為全球覆蓋或任意商業用途批准。

## 證據與接續驗收

[逐日目錄日期對賬](tables/85_最新官方資料時效核查_B62_20261011/位置目錄日期對賬.csv)、[全部產品連結原項](tables/85_最新官方資料時效核查_B62_20261011/產品目錄連結.csv)、[17項公開服務登記](tables/85_最新官方資料時效核查_B62_20261011/公開地理資訊服務.csv)。九個小型原始回應保存於本批原始來源目錄，各有安全雜湊及取得時間；沒有下載大型全量產品或推送逐船記錄。

接續清單：核2026位置元資料與壓縮及欄位版本；核17項服務逐圖層結構與來源條款；對航跡現行／舊路徑比較日期與格式；規劃容量足夠時的最新完整檔品質驗收。異常根因、全量品質、逐用途授權及全球覆蓋仍列未完成，不以目錄回應成功代替實質驗收。
'''
(根/'Reference'/f'{名}.qmd').write_text('---\ntitle: "最新官方資料時效核查：第六十二批"\ndate: 2026-10-11\nlang: zh-TW\nformat:\n  html:\n    toc: true\n    embed-resources: true\n---\n\n'+文,encoding='utf-8')
附=f'\n\n## 2026-10-11 最新官方資料時效核查：第六十二批\n\n[報告]({名}.qmd)：2025年目錄365日；2026年目錄181日、列到6月30日；2026年航跡元資料觀測第一季、9月30日發布。九來源、609條產品連結原項與17項公開服務登記保留證據；全量品质及全球覆蓋未完成。\n'.encode()
assert (根/主).read_bytes()==原;(根/主).write_bytes(原+附);(工作/'附加收據.json').write_text(json.dumps({'附加雜湊':H(附)},ensure_ascii=False),encoding='utf-8')
屬=根/'.gitattributes';屬.write_bytes(屬.read_bytes()+b'\n'+('reports/2026-10-11/最新官方資料時效核查_B62/原始來源/** -text\n').encode())
for d in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:
    (根/d/f'{名}.md').write_text(f'# 最新資料時效核查｜第六十二批\n\n分列觀測時段、發布／修改日期及查證日期。目錄連結不是完整下載；來源更新不是新觀測。優先核2026欄位版本與17項服務圖層結構，原歷史證據保留。\n\n[中文報告](../Reference/{名}.qmd)。\n',encoding='utf-8')
碼=(工作.parent/'時間粒度與異常分層核查_B60/驗證與提交.py').read_text(encoding='utf-8').replace('時間粒度與異常分層核查_B60','最新官方資料時效核查_B62').replace('83_','85_').replace('第六十批：核實完整單日時間鍵、原值異常分層及秒分布','第六十二批：核實2025與2026官方目錄及資料時效')
a=碼.index("    收=json.loads");b=碼.index('    if 暫存:',a)
碼=碼[:a]+'''    收=json.loads((工作/'來源收據.json').read_text(encoding='utf-8'))
    assert len(收)==9 and all(r['狀態碼']==200 for r in 收)
    for r in 收:
        assert 雜湊((根/r['原始檔']).read_bytes())==r['來源雜湊']
    對=讀表('位置目錄日期對賬.csv')
    assert len(對)==2 and [int(r['唯一日期']) for r in 對]==[365,181]
    assert all(not r['已列區間缺失日期'] and int(r['重複日期'])==0 for r in 對)
    assert 對[1]['最晚檔名日期']=='2026-06-30'
    assert len(讀表('產品目錄連結.csv'))==結['產品目錄連結總數']==609
    assert len(讀表('公開地理資訊服務.csv'))==17
    assert not 結['全量產品品質已核'] and not 結['全球覆蓋已核']
'''+碼[b:]
碼=碼.replace("        (工作/'交付驗收.json').write_text", "        for r in 收:\n            assert subprocess.check_output(['git','show',':'+r['原始檔']],cwd=根)==(根/r['原始檔']).read_bytes(),'原始回應暫存位元組不一致'\n        (工作/'交付驗收.json').write_text")
(工作/'驗證與提交.py').write_text(碼,encoding='utf-8');(工作/'發布阻斷測試.py').write_text((工作.parent/'時間粒度與異常分層核查_B60/發布阻斷測試.py').read_text(encoding='utf-8'),encoding='utf-8')
