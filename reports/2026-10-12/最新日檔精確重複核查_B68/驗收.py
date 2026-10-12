from pathlib import Path
import json,csv,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2]
H=lambda b:hashlib.sha256(b).hexdigest()
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'))
assert all(H((根/p).read_bytes())==h for p,h in 基['既有正文'].items()),'既有正文被更改'
結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'))
with (根/'Reference/tables/90_最新日檔精確重複核查_B68_20261012/分桶精確核查.csv').open(encoding='utf-8-sig',newline='') as f:行=list(csv.DictReader(f))
assert len(行)==256 and len({int(r['分桶編號']) for r in 行})==256
for k in 行[0]:
    if k=='分桶編號':continue
    n=max(int(r[k]) for r in 行) if k=='最大同鍵資料行' else sum(int(r[k]) for r in 行)
    assert 結[k]==n
assert 結['資料行']==10622482==結['完整欄值唯一數']+結['精確重複額外行']
assert not 結['全年品質已核'] and not 結['全球覆蓋已核']
收=json.loads((根/'reports/2026-10-11/最新完整日檔品質核查_B64/取得收據.json').read_text(encoding='utf-8'))
assert 結['來源SHA256']==收['来源雜湊']
html=根/'Reference/最新日檔精確重複核查_B68_20261012.html';assert html.stat().st_size>1000
(工作/'交付驗收.json').write_text(json.dumps({'既有正文保留數':len(基['既有正文']),'完整資料行':結['資料行'],'分桶數':256,'彙總對賬通過':True,'成品雜湊':H(html.read_bytes()),'舊批次未覆寫':True},ensure_ascii=False,indent=2),encoding='utf-8')
print('全量彙總、來源血緣與既有正文保留驗收通過。')
