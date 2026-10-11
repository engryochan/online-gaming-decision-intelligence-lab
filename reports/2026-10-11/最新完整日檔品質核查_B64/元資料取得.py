from pathlib import Path
from urllib.request import urlopen,Request
from datetime import datetime,timezone
import json,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];原=工作/'原始來源';原.mkdir(exist_ok=True)
assert not (工作/'元資料收據.json').exists()
收=[]
for 名,url in [('2026年位置官方元資料','https://www.fisheries.noaa.gov/inport/item/80362'),('位置官方母項目','https://www.fisheries.noaa.gov/inport/item/55360')]:
    with urlopen(Request(url,headers={'User-Agent':'Public-current-metadata-audit/1.0'}),timeout=30) as r:b=r.read(4*1024*1024+1);碼=r.status
    assert len(b)<=4*1024*1024;f=原/(名+'.response');assert not f.exists();f.write_bytes(b)
    收.append({'中文來源':名,'網址':url,'取得時間':datetime.now(timezone.utc).isoformat(),'狀態碼':碼,'原始檔':f.relative_to(根).as_posix(),'來源雜湊':hashlib.sha256(b).hexdigest()})
(工作/'元資料收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8')
print('2026年官方元資料及母項目原回應已保留。')
