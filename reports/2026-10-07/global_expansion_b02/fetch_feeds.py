from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from lxml import html
from urllib.parse import urljoin
import json,hashlib
O=Path(__file__).parent;D=O/'raw';manifest=json.loads((O/'source_manifest.json').read_text())
def get(url,name):
 try:
  with urlopen(url,timeout=60) as r:b=r.read();code=r.status;final=r.url
 except HTTPError as e:b=e.read();code=e.code;final=e.url
 p=D/name;assert not p.exists();p.write_bytes(b);manifest.append(dict(url=url,final_url=final,file=name,http_status=code,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()));(O/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');print(name,code,len(b),b[:180],flush=True);return b,code
t=html.fromstring((D/'euronext_equities.html').read_bytes());settings=json.loads(t.xpath('//script[@data-drupal-selector="drupal-settings-json"]')[0].text)
(O/'euronext_settings.json').write_text(json.dumps(settings,indent=2)+'\n',encoding='utf-8')
def walk(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['jsongateway','jsongateway_download']:print(k,v,flush=True)
   if k=='jsongateway_download' and isinstance(v,str):get(urljoin('https://live.euronext.com',v),'euronext_full_download.response')
   walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(settings)
get('https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv','cvm_companies.csv')
get('https://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/META/meta_cad_cia_aberta.txt','cvm_companies_dictionary.txt')
