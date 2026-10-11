from pathlib import Path
import json,csv,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/88_未啟動服務替代來源核查_B65_20261011';名='未啟動服務替代來源核查_B65_20261011';H=lambda b:hashlib.sha256(b).hexdigest()
assert not (工作/'附加收據.json').exists();結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'))
文='''## 三項缺口實際補核

第六十三批證实2020至2022年船舶通行次數地圖服務未啟動。本批沿官方母項目取得各年份產品元資料，確認其直接列出的同年地理栅格下載網址，再實測檔案存在與元資料標籤。觀測年份仍為2020至2022年；目前是2026年10月11日的可用性核查，沒有擴大2019年度下載。

三個同年官方替代檔均可取得，第一影像目錄均通過解析。三者完整檔宣告長度合計1,255,855,479位元組，本批僅取得3,942位元組的指定範圍元資料；沒有完整下載或讀取像元。27項產品元資料／範圍回應及兩項標準來源各保留原位元組與安全雜湊。

限定範圍請求必須回應206及精確的Content-Range（回應位元組範圍），取得長度與要求一致。全部範圍以If-Match（指定來源版本條件）固定同一ETag（來源版本標籤），避免混用版本。來源版本標籤不冒稱為完整檔內容雜湊。

三個檔案是BigTIFF（大檔標籤影像格式），單樣本32位元無符號整數，像元投影坐標比例100米。2020年栅格尺寸133581列、101951行；2021与2022年均126318列、51893行。這是影像矩形尺寸，不能計作有效觀測像元數或全球覆蓋。

## 發現需校訂的結構差異

三個產品的GDAL_NODATA（栅格無資料值標籤）原值均為0。因此不能把全部0直接解釋成無船交通或地域沒有接收，也不能在重採樣時默默把無資料填為有效零值。

官方元資料坐標參考列NAD83（北美大地基準1983）、原代碼4269；實際產品地理鍵及投影文字列WGS84（世界大地坐標系1984）及網頁墨卡托投影。投影鍵32767是使用者自訂，而地理基準鍵4326不是整個投影栅格的坐標代碼。保留原鍵與完整文字，不只讀4326便把投影坐標當成經緯度，也不擅自以某個標準代碼覆寫原參數。

[開放地理空間聯盟標準](https://docs.ogc.org/is/19-008r4/19-008r4.html)區分模型類型、地理基準及投影鍵；本批按原鍵判讀。100米為投影坐標步長，不能据此宣稱各緯度地面像元都是等面積。只驗第一影像目錄，不把其他影像目錄或金字塔概覽當作已核。

## 逐產品用途與地域

[2020產品元資料](https://www.fisheries.noaa.gov/inport/item/64828)、[2021產品元資料](https://www.fisheries.noaa.gov/inport/item/67463)及[2022產品元資料](https://www.fisheries.noaa.gov/inport/item/69555)用途文字均為海岸及海洋規劃，且精度狀態均列未測試。設計精度說明不是獨立驗收結果。

三年份產品完整性文字涉及美國本土、夏威夷、美屬維爾京群島及波多黎各，並说明源航跡建構的時間／距離篩選及拼接間隙。不是所有國家與地區的全量交通資料。這些特定限制與[上一批核實的一般條款](公開服務逐圖層核查_B63_20261011.qmd)並列，不以一般網站許可取消產品用途文字。

## 驗收狀態

完成三項「同年官方替代來源存在及結構可核」缺口；原地圖服務是否恢復没有本批新證據，不能把替代檔可讀填成原服務已恢復。逐像元品質、其他圖像目錄、重投影一致性、所有用途授權及全球完整性仍待核。

下一步以已固定版本的完整檔分塊验收像元与無資料分布；比較年份前先分清投影、影像範圍、來源時段及有效像元掩膜。原圖層、原文及使用者修改全部保留。

## 數據表

- [官方替代來源與栅格結構](tables/88_未啟動服務替代來源核查_B65_20261011/官方替代來源與栅格結構.csv)。
- [投影、無資料值與元資料差異](tables/88_未啟動服務替代來源核查_B65_20261011/投影無資料值與來源差異.csv)。
'''
(根/'Reference'/f'{名}.qmd').write_text('---\ntitle: "未啟動服務替代來源與投影核查：第六十五批"\ndate: 2026-10-11\nlang: zh-TW\nformat:\n  html:\n    toc: true\n    embed-resources: true\n---\n\n'+文,encoding='utf-8')
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));p=根/基['主報告'];b=p.read_bytes();assert len(b)==基['原文位元組'] and H(b)==基['原文雜湊'];附=f'\n\n## 2026-10-11 未啟動服務替代來源核查：第六十五批\n\n[報告]({名}.qmd)：三項未啟動服務的同年官方栅格替代檔已核存在，指定範圍共3942位元組，三者元資料均可解析。實測發現無資料值0及投影與目錄坐標參考差異，逐像元及服務恢復状态不冒稱已核。\n'.encode();p.write_bytes(b+附);(工作/'附加收據.json').write_text(json.dumps({'附加雜湊':H(附)},ensure_ascii=False),encoding='utf-8')
屬=根/'.gitattributes';屬.write_bytes(屬.read_bytes()+('\nreports/2026-10-11/未啟動服務替代來源核查_B65/原始來源/** -text\n').encode())
for d in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:
    (根/d/f'{名}.md').write_text(f'# 替代來源與投影核查｜第六十五批\n\n替代檔存在與原地圖服務恢復分列；無資料值0不推定為零交通。實際投影鍵与目錄參考不同，轉換前保留原參數核對。限定範圍元資料不冒稱完整像元品質。\n\n[報告](../Reference/{名}.qmd)。\n',encoding='utf-8')
碼=(工作.parent/'最新完整日檔品質核查_B64/驗證與提交.py').read_text(encoding='utf-8').replace('最新完整日檔品質核查_B64','未啟動服務替代來源核查_B65').replace('87_','88_').replace('第六十四批：完成2026最新完整日檔全欄品質及地域限制核查','第六十五批：補核三項未啟動服務官方替代檔及投影差異')
a=碼.index("    收=json.loads");b=碼.index('    if 暫存:',a)
碼=碼[:a]+'''    收=json.loads((工作/'來源收據.json').read_text(encoding='utf-8'))+json.loads((工作/'標準來源收據.json').read_text(encoding='utf-8'))
    for r in 收:assert 雜湊((根/r['原始檔']).read_bytes())==r['來源雜湊']
    產品=讀表('官方替代來源與栅格結構.csv');差=讀表('投影無資料值與來源差異.csv')
    assert len(產品)==len(差)==結['同年官方替代來源數']==3
    assert all(r['栅格標籤解析通過']=='True' and r['原服務已恢復']=='False' for r in 產品)
    assert sum(int(r['完整檔宣告位元組']) for r in 產品)==1255855479
    assert sum(int(r['限定範圍取得位元組']) for r in 產品)==結['範圍實得總位元組']==3942
    assert len(收)==結['原始來源回應數']+2==29
    from 栅格標籤解析 import 解析
    for row in 產品:
        年=row['觀測年份'];片=[r for r in 收 if r['中文來源']==年+'年栅格元資料範圍']
        assert all(r['狀態碼']==206 and (根/r['原始檔']).stat().st_size==r['實得位元組'] for r in 片)
        def 讀(o,n):
            for r in 片:
                lo=r['請求起點'];hi=lo+r['實得位元組']
                if lo<=o and o+n<=hi:return (根/r['原始檔']).read_bytes()[o-lo:o-lo+n]
            raise AssertionError('保存片段不足以重現元資料')
        assert 解析(讀)==json.loads(row['第一影像目錄標籤JSON'])
    assert not 結['完整產品已取得'] and not 結['逐像元品質已核'] and not 結['全球覆蓋已核']
'''+碼[b:]
(工作/'驗證與提交.py').write_text(碼,encoding='utf-8');(工作/'發布阻斷測試.py').write_text((工作.parent/'最新完整日檔品質核查_B64/發布阻斷測試.py').read_text(encoding='utf-8'),encoding='utf-8')
