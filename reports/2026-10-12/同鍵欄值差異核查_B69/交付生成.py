from pathlib import Path
import json,csv,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'))
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'))
assert all(H((根/p).read_bytes())==h for p,h in 基['既有正文'].items()),'既有文件已變更，停止'
with (根/'Reference/tables/91_同鍵欄值差異核查_B69_20261012/匿名欄位差異模式.csv').open(encoding='utf-8-sig',newline='') as f:模式=list(csv.DictReader(f))
摘要='\n'.join('- '+r['差異欄名中文']+'（'+r['差異欄名原值']+'）：'+r['同鍵不同值組數']+' 組。' for r in 模式)
報='''---
title: "第六十九批：完整日檔同鍵欄值差異核查"
lang: zh-TW
format: html
---

本輪接續第六十八批七組同鍵差異，重掃已取得的 2026 年 6 月 30 日完整 AIS（船舶自動識別系統）日檔；不是即時資料。本輪先核對 Git（版本控制系統）狀態、近期提交與現行文件，保留使用者正文。

## 全量核查與結果

重新核對壓縮來源 SHA256（安全雜湊算法），將全量 10,622,482 行按識別碼與基準日期時間分桶；雜湊只分桶，最終使用完整原字串鍵與全部 17 欄比對。再次得到 1,220 行精確重複額外記錄及七組同鍵不同欄值，與前批對賬一致。

七組的匿名差異模式如下。組數按差異欄位組合計數，不披露識別碼、位置或原始欄值：

'''+摘要+f"\n\n單欄差異 {結['單欄差異組數']} 組；多欄差異 {結['多欄差異組數']} 組。候選鍵不是來源保證唯一的主鍵，沒有根據本次差異直接刪除或改寫原始資料。\n\n"+'''## 業務含義與處置

精確重複額外行會影響按記錄數計量的統計；同鍵差異則可能影響按時間鍵合併或任取一行的分析。這裡核實的是差異欄位，不是來源錯誤根因，不能推定七組全部是錯誤或選定其中某行為真。

保留原始記錄。下游可另存完整欄值去重視圖，保留重複次數；同鍵不同值應保留多版本，待來源接收、时间精度或處理規則證據確認後再決定合併。字串差異不等於物理量有實質差異，本輪不自行轉數值或修剪空白。

## 保存證據與尚未完成事項

來源：[美國國家海洋與大氣管理局官方壓縮日檔](https://noaaocm.blob.core.windows.net/ais/csv2/csv2026/ais-2026-06-30.csv.zst)。本輪重用第六十四批完整下載，沒有宣稱今日重新取得来源。逐桶彙總及匿名差異模式見 `tables/91_同鍵欄值差異核查_B69_20261012/`；腳本、核查筆記本與回執見 `reports/2026-10-12/同鍵欄值差異核查_B69/`。

全球資料補齊、全年與跨日品質、逐用途授權及異常根因仍未完成。單一美國相關海域日檔不能代表全世界。下一步需要補核來源對同一識別碼、同一時間的處理規則；保留全項目的其他接續清單，不以本輪局部完成替代整體竣工。
'''
(根/'Reference/同鍵欄值差異核查_B69_20261012.qmd').write_text(報,encoding='utf-8')
源="from pathlib import Path\n__file__ = str(Path.cwd() / '全量差異核查.py')\n"+(工作/'全量差異核查.py').read_text(encoding='utf-8')
筆={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3（Python第三版）','language':'python','name':'python3'}},'cells':[{'cell_type':'markdown','metadata':{},'source':['# 同鍵欄值差異全量核查\n','在本筆記本所在目錄執行，需已有本機原始壓縮檔及解码依賴。重跑保留基線保護。']},{'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':源.splitlines(True)}]}
(工作/'全量差異核查筆記本.ipynb').write_text(json.dumps(筆,ensure_ascii=False,indent=2),encoding='utf-8')
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd';原=(根/主).read_bytes()
追加=('\n\n## 第六十九批有界增補：最新已取得完整日檔品質\n\n第六十八批全量核查10,622,482行，發現1,220行精確重複額外記錄；本批重新全量對賬七組同鍵差異，欄位模式如下：\n\n'+摘要+'\n\n保留原始資料及前批報告；同鍵差異不直接判作錯誤。詳見[第六十八批](最新日檔精確重複核查_B68_20261012.qmd)與[第六十九批](同鍵欄值差異核查_B69_20261012.qmd)。全年品質、逐用途授權與全球覆蓋仍待核實。\n').encode('utf-8')
(根/主).write_bytes(原+追加)
(工作/'附加收據.json').write_text(json.dumps({'主報告':主,'原文位元組':len(原),'原文雜湊':H(原),'附加雜湊':H(追加)},ensure_ascii=False,indent=2),encoding='utf-8')
提示={'redteam':'同鍵異值不可任選一行；單一地域日檔不推定全球覆蓋。','critic':'核實差異欄位與組數，不將字串差異直接等同實質物理差異或來源錯誤。','killcritic':'接受批評須有可重現證據；完整來源雜湊與256桶對賬保留，錯誤根因不臆測。','blindspot':'同鍵的時間精度、接收來源及處理規則仍待原始證據，不能由七組模式倒推根因。','blueprint':'原始層保留全部記錄；完整欄值去重視圖另存重複次數；同鍵不同值保留多版本。','cheatsheet':'核查範圍：2026年6月30日單檔、全部17欄；識別碼加時間只作候選鍵。','actionplan':'已完成七組差異欄位核查；待核來源合併規則、跨日品質、全年品質、逐用途授權及全球覆蓋。'}
for d,t in 提示.items():
    (根/d/'同鍵欄值差異核查_B69_20261012.md').write_text('# 第六十九批核查筆記\n\n'+t+'\n\n[報告](../Reference/同鍵欄值差異核查_B69_20261012.qmd)。\n',encoding='utf-8')
print('中文交付與主報告有界增補已生成。')
