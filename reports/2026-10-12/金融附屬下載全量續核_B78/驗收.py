from pathlib import Path
import csv,json,hashlib
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/100_金融附屬下載全量續核_B78_20261012'
b=json.loads((W/'基線.json').read_text(encoding='utf-8'));s=json.loads((W/'結果.json').read_text(encoding='utf-8'))
for p,h in b['來源'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
rows=list(csv.DictReader((T/'下載與分頁收據.csv').open(encoding='utf-8-sig')))
assert len(rows)==s['唯一網址'] and sum(int(x['來源觀察數']) for x in rows)==s['原觀察']
for x in rows:
 if x.get('原始檔'):assert hashlib.sha256((R/x['原始檔']).read_bytes()).hexdigest()==x['SHA256']
assert all(x['完整性']=='UNKNOWN（未知）' for x in rows)
(W/'交付驗收.json').write_text(json.dumps({'全量來源觀察對賬':s['原觀察'],'唯一來源':len(rows),'來源雜湊通過':True,'完整性升級':0,'XLSX範圍修復沿用':True},ensure_ascii=False,indent=2),encoding='utf-8')
print('來源對賬及雜湊驗收通過')
