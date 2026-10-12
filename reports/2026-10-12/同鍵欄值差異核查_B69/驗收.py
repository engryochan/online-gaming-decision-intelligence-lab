from pathlib import Path
import json,csv,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));附=json.loads((工作/'附加收據.json').read_text(encoding='utf-8'))
for p,h in 基['既有正文'].items():
    b=(根/p).read_bytes()
    if p==附['主報告']:
        n=附['原文位元組'];assert H(b[:n])==h==附['原文雜湊'] and H(b[n:])==附['附加雜湊']
    else:assert H(b)==h,'既有正文已變動：'+p
結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'))
前=json.loads((根/'reports/2026-10-12/最新日檔精確重複核查_B68/核查結果.json').read_text(encoding='utf-8'))
def 表(n):
    with (根/'Reference/tables/91_同鍵欄值差異核查_B69_20261012'/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
行=表('分桶精確核查.csv');模式=表('匿名欄位差異模式.csv')
assert len(行)==256 and len({r['分桶編號'] for r in 行})==256
for k in 行[0]:
    if k=='分桶編號':continue
    v=max(int(r[k]) for r in 行) if k=='最大同鍵資料行' else sum(int(r[k]) for r in 行)
    assert v==結[k]==前[k]
assert 結['資料行']==10622482==結['完整欄值唯一數']+結['精確重複額外行']
assert sum(int(r['同鍵不同值組數']) for r in 模式)==結['差異模式組數']==7
assert len(模式)==結['差異模式數']
assert sum(int(r['同鍵不同值組數']) for r in 模式 if int(r['相異欄數'])==1)==結['單欄差異組數']
assert sum(int(r['同鍵不同值組數']) for r in 模式 if int(r['相異欄數'])>1)==結['多欄差異組數']
assert not 結['全年品質已核'] and not 結['全球覆蓋已核'] and not 結['識別碼位置與原始欄值披露']
assert 結['來源SHA256']==前['來源SHA256']
html=根/'Reference/同鍵欄值差異核查_B69_20261012.html';assert html.stat().st_size>1000
(工作/'交付驗收.json').write_text(json.dumps({'既有正文保留數':len(基['既有正文']),'主報告原文保留':True,'完整資料行':結['資料行'],'前批八項計數一致':True,'七組差異對賬':True,'成品雜湊':H(html.read_bytes()),'未披露船舶記錄':True},ensure_ascii=False,indent=2),encoding='utf-8')
print('來源、前批計數、七組欄位模式及主報告原文保留驗收通過。')
