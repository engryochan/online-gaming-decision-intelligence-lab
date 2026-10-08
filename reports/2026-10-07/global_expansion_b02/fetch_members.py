from pathlib import Path
from urllib.request import urlopen
from lxml import html
import json,hashlib,csv
O=Path(__file__).parent;D=O/'raw';m=json.loads((O/'source_manifest.json').read_text());url='https://live.euronext.com/en/resources/members-list'
with urlopen(url,timeout=60) as r:b=r.read()
p=D/'euronext_members.html';assert not p.exists();p.write_bytes(b);m.append(dict(url=url,file=p.name,http_status=200,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()));(O/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
t=html.fromstring(b);settings=t.xpath('//script[@data-drupal-selector="drupal-settings-json"]');s=json.loads(settings[0].text);(O/'euronext_members_settings.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8');print('Tables',[(a.get('id'),len(a.xpath('.//tr'))) for a in t.xpath('//table')]);
for a in t.xpath('//a[@href]'):
 text=' '.join(a.itertext()).strip();href=a.get('href')
 if any(k in (text+' '+href).lower() for k in ['.csv','.xls','download','member-list','members-list']):print(json.dumps([text[:120],href]))
with (D/'euronext_full_download.response').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f,delimiter=';'))
print(json.dumps({'markets':dict(__import__('collections').Counter(r['Market'] for r in rows)),'last_rows':rows[-4:]}))
