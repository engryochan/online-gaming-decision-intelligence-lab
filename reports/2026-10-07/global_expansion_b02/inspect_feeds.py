from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urljoin
from collections import Counter
from lxml import html
import json,csv,hashlib
O=Path(__file__).parent;D=O/'raw';m=json.loads((O/'source_manifest.json').read_text());s=json.loads((O/'euronext_settings.json').read_text())
def get(url,name):
 try:
  with urlopen(url,timeout=60) as r:b=r.read();code=r.status;final=r.url
 except HTTPError as e:b=e.read();code=e.code;final=e.url
 p=D/name;assert not p.exists();p.write_bytes(b);m.append(dict(url=url,final_url=final,file=name,http_status=code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()));(O/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');print(name,code,len(b),b[:300],flush=True);return b,code
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='jsongateway':get(urljoin('https://live.euronext.com',v),'euronext_directory.response')
   walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(s)
with (D/'euronext_full_download.response').open(encoding='utf-8-sig') as f:
 rows=list(csv.DictReader(f,delimiter=';'));print('CSV records',len(rows),'markets',Counter(r['Market'] for r in rows),'currencies',Counter(r['Currency'] for r in rows),flush=True);print(rows[:2],flush=True)
get('https://live.euronext.com/en/resources/members-list','euronext_members.html')
