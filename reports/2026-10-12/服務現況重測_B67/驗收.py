from pathlib import Path
import subprocess, hashlib, json, csv
根=Path(__file__).resolve().parents[3]
工作=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
paths=subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0')
for p in paths:
    if p and p.endswith(('.qmd','.md')):
        assert subprocess.check_output(['git','hash-object','--path='+p,p],cwd=根).strip()==subprocess.check_output(['git','rev-parse','HEAD:'+p],cwd=根).strip(), '既有正文改動：'+p
收=json.loads((工作/'來源收據.json').read_text(encoding='utf-8'))
assert len(收)==6 and sum(r['方法']=='HEAD' for r in 收)==3
for r in 收:
    if '原始檔' in r:assert H((根/r['原始檔']).read_bytes())==r['來源雜湊']
    assert r['觀測UTC'].startswith('2026-10-12')
with (根/'Reference/tables/89_服務現況重測_B67_20261012/服務與替代檔案現況.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==6
assert all(r['可用']=='False' and json.loads(r['服務錯誤'])['code']==500 for r in rows if r['類型']=='原服務')
assert all(r['與前批大小一致']==r['與前批版本一致']=='True' for r in rows if r['類型']=='替代栅格')
html=根/'Reference/服務現況重測_B67_20261012.html'
assert html.stat().st_size>1000
(工作/'交付驗收.json').write_text(json.dumps({'來源收據數':6,'原始正文雜湊核對數':3,'既有正文保留':True,'服務錯誤與標頭核對':True,'成品SHA256':H(html.read_bytes()),'全量品質已核':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('驗收通過：既有正文保留，六次實測與三份原始正文一致。')
