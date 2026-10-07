from pathlib import Path
import json,urllib.request,urllib.parse,time
from lxml import html
O=Path(__file__).resolve().parent;P=O/'raw'
links=html.parse(str(P/'esma_help.html')).xpath('//a/@href')
official=next(u for u in links if '/solr/esma_registers_upreg/select?' in u and 'ae_entityTypeCode%3AMIF' in u and 'join' in u)
base='https://registers.esma.europa.eu/solr/esma_registers_upreg/select';params=dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(official).query));params.update(rows='5000',sort='id asc',wt='json')
docs=[];pages=[];expected=None
for start in range(0,500000,5000):
 params['start']=str(start);url=base+'?'+urllib.parse.urlencode(params)
 with urllib.request.urlopen(url,timeout=60) as response:body=response.read();server_date=response.headers.get('Date')
 path=P/f'esma_mif_join_{start:06d}.json';assert not path.exists();path.write_bytes(body);r=json.loads(body);total=r['response']['numFound'];batch=r['response']['docs']
 if expected is None:expected=total
 assert total==expected and r['response']['start']==start and batch
 docs.extend(batch);pages.append(dict(url=url,file=path.name,start=start,numFound=total,rows=len(batch),server_date=server_date));print(json.dumps(dict(start=start,rows=len(batch),numFound=total)),flush=True)
 if len(docs)>=expected:break
 time.sleep(0.25)
assert len(docs)==expected and len({x['id'] for x in docs})==expected
(P/'esma_mif_join_complete.json').write_text(json.dumps(docs,ensure_ascii=False),encoding='utf-8')
(O/'esma_activity_pagination.json').write_text(json.dumps(dict(official_query=official,stable_numFound=expected,unique_ids=expected,pages=pages,complete=True),indent=2)+'\n',encoding='utf-8')
