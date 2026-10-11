from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone
import json,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];原=工作/'原始來源';f=原/'甲類位置報文官方語義.response';assert not f.exists()
url='https://www.navcen.uscg.gov/ais-class-a-reports'
with urlopen(Request(url,headers={'User-Agent':'Public-schema-meaning-audit/1.0'}),timeout=30) as r:b=r.read(2*1024*1024+1);碼=r.status
assert len(b)<=2*1024*1024 and b'under way using engine' in b;f.write_bytes(b)
(工作/'協議語義收據.json').write_text(json.dumps([{'網址':url,'中文來源':'美國海岸警衛隊甲類位置報文語義','取得時間':datetime.now(timezone.utc).isoformat(),'狀態碼':碼,'原始檔':f.relative_to(根).as_posix(),'來源雜湊':hashlib.sha256(b).hexdigest()}],ensure_ascii=False,indent=2),encoding='utf-8')
