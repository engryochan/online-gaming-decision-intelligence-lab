from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin
from lxml import html
from concurrent.futures import ThreadPoolExecutor
import json,hashlib
O=Path(__file__).parent;D=O/'raw';m=json.loads((O/'source_manifest.json').read_text());t=html.fromstring((D/'euronext_equities.html').read_bytes());urls=[urljoin('https://live.euronext.com',s.get('src')) for s in t.xpath('//script[@src]') if s.get('src').startswith('/assets/js/optimized/')]
def get(pair):
 i,url=pair
 with urlopen(url,timeout=60) as r:b=r.read()
 name=f'euronext_script_{i:02d}.js';p=D/name;assert not p.exists();p.write_bytes(b);return dict(url=url,file=name,http_status=200,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
with ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(get,enumerate(urls)))
m.extend(out);(O/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');print('Archived',len(out),'official scripts')
