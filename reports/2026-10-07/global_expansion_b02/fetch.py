from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from lxml import html
from urllib.parse import urljoin
import json,hashlib
O=Path(__file__).parent;D=O/'raw';D.mkdir(parents=True,exist_ok=True);manifest=[]
def get(url,name):
 try:
  with urlopen(url,timeout=60) as r:b=r.read();code=r.status;final=r.url
 except HTTPError as e:b=e.read();code=e.code;final=e.url
 p=D/name;assert not p.exists();p.write_bytes(b);manifest.append(dict(url=url,final_url=final,file=name,http_status=code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()));(O/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');print(name,code,len(b),flush=True)
 return b,code
for url,name in [('https://seshat-db.com/core/polities-light/','seshat_polities.html'),('https://live.euronext.com/en/products/equities/list','euronext_equities.html'),('https://dados.cvm.gov.br/dataset/cia_aberta-cad','cvm_company_catalog.html')]:
 b,code=get(url,name)
 if code==200:
  t=html.fromstring(b)
  for a in t.xpath('//a[@href]'):
   text=' '.join(a.itertext()).strip();href=urljoin(url,a.get('href'))
   if any(k in (text+' '+href).lower() for k in ['download','csv','.zip','export','cadastral']):print(text[:100],href,flush=True)
  print('scripts',[(a.get('src') or '') for a in t.xpath('//script[@src]')][-12:],flush=True)
