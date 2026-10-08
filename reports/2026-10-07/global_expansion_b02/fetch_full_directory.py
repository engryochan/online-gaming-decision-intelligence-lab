from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin
from lxml import html
import json,hashlib,csv
O=Path(__file__).parent;D=O/'raw';m=json.loads((O/'source_manifest.json').read_text())
def get(url,name):
 with urlopen(url,timeout=60) as r:b=r.read();code=r.status
 p=D/name;assert not p.exists();p.write_bytes(b);m.append(dict(url=url,file=name,http_status=code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()));(O/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');print(name,len(b),flush=True);return b
def walk(x,kind):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='jsongateway':
    url=urljoin('https://live.euronext.com',v);b=get(url+('&' if '?' in url else '?')+'iDisplayStart=0&iDisplayLength=5000',kind+'_full_directory.json');d=json.loads(b);print(json.dumps({k:len(v) if k=='aaData' else v for k,v in d.items() if k in ['iTotalRecords','iTotalDisplayRecords','aaData']}),flush=True)
   walk(v,kind)
 elif isinstance(x,list):
  for v in x:walk(v,kind)
walk(json.loads((O/'euronext_settings.json').read_text()),'equities')
walk(json.loads((O/'euronext_members_settings.json').read_text()),'members')
with (D/'euronext_full_download.response').open(encoding='utf-8-sig') as f:rs=list(csv.DictReader(f,delimiter=';'))
print('Null rows',json.dumps([r for r in rs if r['Market']=='null']),flush=True)
