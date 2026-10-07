from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urljoin
from lxml import html
import json,hashlib,datetime
O=Path(__file__).parent; D=O/'raw'; manifest=[]
def get(url,name):
 with urlopen(Request(url,headers={'User-Agent':'Research source archival'}),timeout=90) as r:
  b=r.read(); final=r.url; date=r.headers.get('Date')
 p=D/name; assert not p.exists();p.write_bytes(b)
 manifest.append(dict(url=url,final_url=final,file=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),server_date=date))
 (O/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 print(name,len(b),flush=True);return b
base='https://correlatesofwar.org/data-sets/state-system-membership/'
b=get(base,'cow_membership_page.html');tree=html.fromstring(b)
for a in tree.xpath('//a[@href]'):
 label=' '.join(a.itertext()).strip();href=urljoin(base,a.get('href'))
 if label in ['State System Membership Datasets','Major Powers Datasets','State System Datasets']:
  print(label,href,flush=True);get(href,label.replace(' ','_')+'.zip')
meta=json.loads(get('https://api.github.com/repos/Seshat-Global-History-Databank/cliopatria/commits/main','cliopatria_commit.json'))
sha=meta['sha'];(O/'pinned_commit.txt').write_text(sha+'\n')
for name in ['README.md','cliopatria.geojson.zip']:
 get('https://raw.githubusercontent.com/Seshat-Global-History-Databank/cliopatria/'+sha+'/'+name,name)
