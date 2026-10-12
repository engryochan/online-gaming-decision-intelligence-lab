from pathlib import Path
import json, hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2]
結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'))
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((根/p).read_bytes()).hexdigest()==h for p,h in 基['既有正文'].items())
率=100*結['精確重複額外行']/結['資料行']
報='''---
title: "第六十八批：2026年最新已取得完整日檔精確重複核查"
lang: zh-TW
format: html
---

本輪補查已取得的 2026 年 6 月 30 日官方 AIS（船舶自動識別系統）日檔；「最新」僅指前批目錄快照中最新已取得的完整日檔，不代表即時資料。本輪沒有重新探測官方目錄，也沒有新增歷史年度下載。

## 完整日檔與核查粒度

'''+f"共 {結['資料行']:,} 行、17 欄；重新核對既有壓縮檔 SHA256（安全雜湊算法）一致。候選鍵是識別碼與基準日期時間，並非來源已保證唯一的主鍵。以全部 17 欄解析後的原字串逐項相等判定精確重複，不修剪空白、不轉數值，也不改時間精度。\n\n"+'''雜湊僅將候選鍵分配至 256 個暫存桶；最終比較完整鍵與全部欄值字串，不依賴雜湊碰撞假設。每桶逐項計數後彙總，原始資料與中間桶不推送；完成後只清除本腳本新建的中間桶，保留原始壓縮檔。

## 全量結果

'''+ '\n'.join('- '+k+'：'+f'{結[k]:,}' for k in ['資料行','候選鍵數','完整欄值唯一數','精確重複額外行','精確重複組','候選鍵多行組','同鍵不同完整欄值組','最大同鍵資料行'])+f'\n- 精確重複額外行比例：{率:.8f}%（分母為全部資料行）。\n'+'''
## 影響、修復與未完成事項

重複額外行可能使直接按原始記錄數累加的統計偏高；同鍵不同欄值則需確認接收來源、時間精度及資料處理規則，不能直接刪成一行。這些核查結果證明本檔的字串重複情況，不證明來源異常根因，也不把候選鍵多行一律定為錯誤。

資料保留原樣。分析時可建立另存的完整欄值去重視圖，並保留重複次數；以時間鍵取一行的規則必須另行驗證。全年、跨日連續性、全球覆蓋與逐用途授權仍未完成核實。單一美國相關海域日檔不能代表全世界。

## 可審閱證據

逐桶數據見 `tables/90_最新日檔精確重複核查_B68_20261012/分桶精確核查.csv`；腳本、可執行核查筆記本、來源雜湊與驗收回執見 `reports/2026-10-12/最新日檔精確重複核查_B68/`。前批結果保留，不把前批尚未核查的旗標改寫為當時已完成。

來源：[美國國家海洋與大氣管理局官方壓縮日檔](https://noaaocm.blob.core.windows.net/ais/csv2/csv2026/ais-2026-06-30.csv.zst)，取得時間及完整下載回執保存在第六十四批；本輪重用該檔。
'''
(根/'Reference/最新日檔精確重複核查_B68_20261012.qmd').write_text(報,encoding='utf-8')
源=(工作/'全量核查.py').read_text(encoding='utf-8')
源="from pathlib import Path\n__file__ = str(Path.cwd() / '全量核查.py')\n"+源
筆={'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3（Python第三版）','language':'python','name':'python3'}},'cells':[{'cell_type':'markdown','metadata':{},'source':['# 第六十八批完整日檔精確重複核查\n','下列為实际核查腳本全文；重跑前須在脚本目錄執行並保留來源依賴與本機原始檔。報告只收錄彙總，不披露船舶記錄。']},{'cell_type':'code','metadata':{},'execution_count':None,'outputs':[],'source':源.splitlines(True)}]}
(工作/'全量核查筆記本.ipynb').write_text(json.dumps(筆,ensure_ascii=False,indent=2),encoding='utf-8')
print('中文報告與核查筆記本已生成。')
