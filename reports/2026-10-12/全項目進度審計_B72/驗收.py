from pathlib import Path
from collections import Counter
import json,csv,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));附=json.loads((工作/'附加收據.json').read_text(encoding='utf-8'));結=json.loads((工作/'審計結果.json').read_text(encoding='utf-8'))
for p,h in 基['既有正文'].items():
    b=(根/p).read_bytes()
    if p==附['主報告']:
        n=附['原文位元組'];assert H(b[:n])==h==附['原文雜湊'] and H(b[n:])==附['附加雜湊']
    else:assert H(b)==h,'既有正文變更：'+p
表=根/'Reference/tables/94_全項目進度審計_B72_20261012'
def 讀(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
快=讀(表/'全項目文件雜湊快照.csv');assert len(快)==結['文件快照行'] and len({r['路徑'] for r in 快})==len(快)
assert sum(r['掃描期間穩定']=='False' for r in 快)==結['文件快照不穩定數']==0
assert len(讀(表/'跳過與讀取失敗.csv'))==結['文件跳過或失敗數']==0
index={r['路徑']:r['SHA256'] for r in 快}
inputs=['Reference/tables/50_global_directory_content_b25_20261008/registry_all_4849_work_progress.csv','Reference/tables/50_global_directory_content_b25_20261008/registry_all_country_cumulative_source_progress.csv','Reference/tables/07_global_technology_iso249_20261006/registry_country_technology_coverage.csv','Reference/tables/07_global_technology_iso249_20261006/registry_neurotechnology_global.csv','Reference/tables/93_全球貨幣與市場代碼全量續核_B71_20261012/未關聯貨幣來源記錄.csv']
for p in inputs:assert H((根/p).read_bytes())==index[p],'審計輸入已變更'
f=讀(根/inputs[0]);assert len(f)==結['金融工作總項']==4849
assert sum(int(r['attempt_observations'] or 0)>0 for r in f)==結['金融已嘗試工作']
assert sum(r['last_http_status']=='200' for r in f)==結['金融末次HTTP200工作']
assert dict(Counter(r['directory_completeness'] for r in f))==結['金融完整性狀態']
分=讀(表/'未關聯貨幣來源全量分流.csv');原=讀(根/inputs[-1])
ids=[x for r in 分 for x in json.loads(r['記錄識別碼JSON'])]
assert len(分)==35 and len(ids)==len(原)==42 and Counter(ids)==Counter(r['記錄識別碼'] for r in 原)
assert all(r['國別關聯已提升']=='False' for r in 分)
assert 結['金融資料庫快速檢查']==[['ok']] and not 結['整體完成率可計算']
assert 結['歷史重建清單行']==66 and 結['歷史重建QMD缺失數']==0 and 結['歷史重建HTML較當時快照不同數']==0
html=根/'Reference/全項目進度審計_B72_20261012.html';assert html.stat().st_size>1000
(工作/'交付驗收.json').write_text(json.dumps({'既有正文保留數':len(基['既有正文']),'主報告原文保留':True,'文件快照行':len(快),'審計輸入雜湊核對':True,'金融進度對賬':True,'42項來源全量分流對賬':True,'未提升未知證據':True,'成品雜湊':H(html.read_bytes()),'全項目內容實質核實已完成':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('文件快照、審計來源、進度與分流對賬、正文保留驗收通過。')
