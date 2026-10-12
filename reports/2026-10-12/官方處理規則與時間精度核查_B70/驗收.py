from pathlib import Path
import json,csv,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));附=json.loads((工作/'附加收據.json').read_text(encoding='utf-8'))
for p,h in 基['既有正文'].items():
    b=(根/p).read_bytes()
    if p==附['主報告']:
        n=附['原文位元組'];assert H(b[:n])==h==附['原文雜湊'] and H(b[n:])==附['附加雜湊']
    else:assert H(b)==h,'既有正文變動：'+p
收=json.loads((工作/'來源收據.json').read_text(encoding='utf-8'));結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'))
assert len(收)==結['官方文件回應數']==4
for r in 收:
    b=(根/r['原始檔']).read_bytes();assert H(b)==r['來源雜湊'] and len(b)==r['實得位元組'] and r['狀態碼']==200
    assert r['觀測UTC'].startswith('2026-10-12')
固定=json.loads((工作/'原始來源/官方倉庫版本.json').read_text(encoding='utf-8'))['sha']
assert 固定==結['官方倉庫固定提交'] and any('/'+固定+'/README.md' in r['網址'] for r in 收)
表=根/'Reference/tables/92_官方處理規則與時間精度核查_B70_20261012'
with (表/'全量時間秒數分布.csv').open(encoding='utf-8-sig',newline='') as f:行=list(csv.DictReader(f))
assert len(行)==60 and {int(r['秒數']) for r in 行}==set(range(60))
assert sum(int(r['資料行']) for r in 行)==結['資料行']==10622482
assert int(行[0]['資料行'])==結['秒數為零行']==166476
assert sum(int(r['資料行']) for r in 行[1:])==結['秒數非零行']==10456006
assert 結['微秒非零行']==0 and 結['觀測日期分布']=={'2026-06-30':10622482}
前=json.loads((根/'reports/2026-10-11/最新完整日檔品質核查_B64/核查結果.json').read_text(encoding='utf-8'))
assert 結['來源SHA256']==前['來源雜湊'] and 結['資料行']==前['完整資料行']
with (表/'官方描述與全量實測對照.csv').open(encoding='utf-8-sig',newline='') as f:claims=list(csv.DictReader(f))
assert len(claims)==6 and sum(r['證據等級'].startswith('UNKNOWN') for r in claims)==1
assert not 結['同鍵合併規則已核'] and not 結['全年品質已核'] and not 結['全球覆蓋已核']
html=根/'Reference/官方處理規則與時間精度核查_B70_20261012.html';assert html.stat().st_size>1000
(工作/'交付驗收.json').write_text(json.dumps({'既有正文保留數':len(基['既有正文']),'主報告原文保留':True,'官方來源雜湊核對數':4,'完整日檔資料行':結['資料行'],'六十秒分布对賬':True,'固定倉庫版本核對':True,'成品雜湊':H(html.read_bytes()),'全量與來源規則邊界保留':True},ensure_ascii=False,indent=2),encoding='utf-8')
print('四份官方證據、秒數分布、來源血緣及正文保留驗收通過。')
