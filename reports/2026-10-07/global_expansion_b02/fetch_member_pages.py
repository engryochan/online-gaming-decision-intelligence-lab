from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import re,json,hashlib,math
O=Path(__file__).parent;D=O/'raw';m=json.loads((O/'source_manifest.json').read_text());t=html.fromstring((D/'members_iframe.html').read_bytes());foot=' '.join(t.itertext());match=re.search(r'Displaying\s+1\s*-\s*20\s+of\s+(\d+)',foot);assert match;total=int(match[1]);pages=math.ceil(total/20);base='https://connect2.euronext.com/en/intframe/trade/member-list'
def get(i):
 url=base+'?page='+str(i)
 with urlopen(url,timeout=60) as r:b=r.read()
 name=f'members_page_{i:02d}.html';p=D/name;assert not p.exists();p.write_bytes(b);return dict(url=url,file=name,http_status=200,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),page=i)
with ThreadPoolExecutor(max_workers=4) as ex:out=list(ex.map(get,range(1,pages)))
m.extend(out);(O/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');(O/'member_pagination.json').write_text(json.dumps(dict(expected_total=total,pages=pages,records_per_page=20,page_zero='members_iframe.html',other_pages=out),indent=2)+'\n',encoding='utf-8');print('All member pages received',pages,total)
