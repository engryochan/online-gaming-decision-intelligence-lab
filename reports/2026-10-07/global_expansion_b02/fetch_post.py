from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urljoin,urlencode
from lxml import html
import json,hashlib,csv
O=Path(__file__).parent;D=O/'raw';m=json.loads((O/'source_manifest.json').read_text());s=json.loads((O/'euronext_settings.json').read_text())
params={'length':5000,'start':0,'iDisplayLength':5000,'iDisplayStart':0,'args[display_datapoints]':','.join(s['datapoints'])}
u=urljoin('https://live.euronext.com',s['jsongateway']);req=Request(u,data=urlencode(params).encode(),headers={'Content-Type':'application/x-www-form-urlencoded'})
with urlopen(req,timeout=90) as r:b=r.read()
p=D/'equities_full_post.json';assert not p.exists();p.write_bytes(b);m.append(dict(url=u,method='POST_READ_QUERY',query=params,file=p.name,http_status=200,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()));print(json.dumps({k:len(v) if k=='aaData' else v for k,v in json.loads(b).items() if k in ['iTotalRecords','iTotalDisplayRecords','aaData']}),flush=True)
t=html.fromstring((D/'euronext_members.html').read_bytes());u=t.xpath('//iframe[@id="awl_member_list_iframe"]')[0].get('src')
with urlopen(u,timeout=60) as r:b=r.read()
p=D/'members_iframe.html';assert not p.exists();p.write_bytes(b);m.append(dict(url=u,file=p.name,http_status=200,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()));(O/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');t=html.fromstring(b);print('member tables',[(x.get('id'),len(x.xpath('.//tr'))) for x in t.xpath('//table')]);print('member scripts',[x.get('src') for x in t.xpath('//script[@src]')][-5:])
with (D/'euronext_full_download.response').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f,delimiter=';'))
print('Rows without market',json.dumps([r for r in rows if not r.get('Market')]),flush=True)
