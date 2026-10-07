from pathlib import Path
import json,urllib.request,urllib.parse,time
from lxml import html
O=Path(__file__).resolve().parent;P=O/'raw';P.mkdir(exist_ok=True)
doc=html.parse(str(P/'esma_help.html'))
links=doc.xpath('//a/@href')
official=next(u for u in links if '/solr/esma_registers_upreg/select?' in u and 'ae_entityTypeCode%3AMIF' in u and 'join' in u)
base='https://registers.esma.europa.eu/solr/esma_registers_upreg/select'
params=dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(official).query))
params.update(rows='1',start='0',sort='id asc',wt='json')
url=base+'?'+urllib.parse.urlencode(params)
with urllib.request.urlopen(url,timeout=45) as response: body=response.read()
(P/'esma_mif_join_probe.json').write_bytes(body)
probe=json.loads(body);print(json.dumps(dict(join_numFound=probe['response']['numFound'],first_doc=probe['response']['docs'][0]),ensure_ascii=True),flush=True)
all_docs=[];pages=[];expected=None
for start in range(0,100000,1000):
 url=base+'?'+urllib.parse.urlencode(dict(q='ae_entityTypeCode:MIF',rows=1000,start=start,wt='json',sort='id asc'))
 with urllib.request.urlopen(url,timeout=45) as response: body=response.read();server_date=response.headers.get('Date')
 path=P/f'esma_mif_parents_{start:06d}.json';path.write_bytes(body);r=json.loads(body);total=r['response']['numFound'];docs=r['response']['docs']
 if expected is None:expected=total
 assert total==expected and r['response']['start']==start and docs
 all_docs.extend(docs);pages.append(dict(url=url,file=path.name,start=start,numFound=total,rows=len(docs),server_date=server_date));print(json.dumps(dict(start=start,rows=len(docs),numFound=total)),flush=True)
 if len(all_docs)>=expected:break
 time.sleep(0.25)
assert len(all_docs)==expected and len({x['id'] for x in all_docs})==expected
(P/'esma_mif_parents_complete.json').write_text(json.dumps(all_docs,ensure_ascii=False),encoding='utf-8')
(O/'esma_parent_pagination.json').write_text(json.dumps(dict(query='ae_entityTypeCode:MIF',stable_numFound=expected,unique_ids=expected,pages=pages,complete=True),indent=2)+'\n',encoding='utf-8')
