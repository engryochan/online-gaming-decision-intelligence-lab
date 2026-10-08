from pathlib import Path
import csv,json,hashlib,urllib.request,urllib.error
from urllib.parse import urljoin,urlparse,parse_qs
from concurrent.futures import ThreadPoolExecutor,as_completed
from lxml import html
OUT=Path(__file__).parent;ROOT=OUT.parents[2]
TABLE=ROOT/'Reference/tables/28_global_market_sources_b03_20261008'
def write(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (TABLE/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchSourceInventory/1.0'}),timeout=12) as r:
            b=r.read(2000001)
            return dict(url=url,final_url=r.url,http_status=r.status,bytes_observed=len(b),truncated=len(b)>2000000,
                        sha256_observed=hashlib.sha256(b).hexdigest(),checked_on='2026-10-08'),b
    except urllib.error.HTTPError as e:return dict(url=url,http_status=e.code,checked_on='2026-10-08'),b''
    except Exception as e:return dict(url=url,http_status='',error_type=type(e).__name__,checked_on='2026-10-08'),b''
records=[];manifest=[]
for number,category in [(1,'ORDINARY'),(2,'ASSOCIATE'),(3,'AFFILIATE')]:
    queue=[(1,f'https://www.iosco.org/about/?subsection=membership&memid={number}')];seen=set()
    while queue:
        page,url=queue.pop(0)
        if page in seen:continue
        seen.add(page)
        result,b=get(url);result.update(category=category,page=page);manifest.append(result)
        if result.get('http_status')!=200:continue
        (OUT/'raw'/f'IOSCO_{category}_page_{page:02d}.response').write_bytes(b)
        tree=html.fromstring(b)
        nodes=tree.xpath('//ol[contains(@class,"list-group")]/li')
        result['entries']=len(nodes)
        for index,node in enumerate(nodes,1):
            text=' '.join(node.text_content().split())
            links=[urljoin(url,u.strip()) for u in node.xpath('.//a[@href]/@href')]
            external=[u for u in links if urlparse(u).scheme in ('http','https') and urlparse(u).hostname not in ('www.iosco.org','iosco.org')]
            records.append(dict(category=category,page=page,source_row=index,entry_text=text,websites_json=json.dumps(external,ensure_ascii=False),
                                raw_entry_html=html.tostring(node,encoding='unicode'),source_url=url,
                                semantic_status='SOURCE_ENTRY_PRESERVED_COUNTRY_ENTITY_NORMALIZATION_PENDING'))
        for link in tree.xpath('//*[contains(@class,"pagination")]//a/@href'):
            target=urljoin(url,link.strip());args=parse_qs(urlparse(target).query)
            if args.get('memid')==[str(number)] and args.get('page'):
                next_page=int(args['page'][0])
                if next_page not in seen:queue.append((next_page,target))
write('registry_iosco_members_source_entries.csv',records)
write('iosco_category_fetch_manifest.csv',manifest)
# Audit the bounded WFE member section, excluding footer privacy/navigation links.
tree=html.fromstring((OUT/'raw/WFE.response').read_bytes());wfe=[]
for index,node in enumerate(tree.xpath('//section[@id="member-list"]//li'),1):
    name=' '.join(node.text_content().split());all_links=node.xpath('.//a[@href]/@href')
    links=[u for u in all_links if urlparse(urljoin('https://www.world-exchanges.org/membership-events',u)).hostname not in ('www.world-exchanges.org','world-exchanges.org')]
    if all_links and not links:continue
    for link in links or ['']:
        wfe.append(dict(source_row=index,name=name,url=urljoin('https://www.world-exchanges.org/membership-events',link) if link else '',
                        source='https://www.world-exchanges.org/membership-events',country_status='UNASSIGNED_PENDING_ENTITY_MATCH'))
write('registry_wfe_directory_entries.csv',wfe)
urls=sorted({u for r in records for u in json.loads(r['websites_json'])})
print(json.dumps(dict(iosco_entries=len(records),regulator_endpoints=len(urls),WFE_entries=len(wfe))),flush=True)
checks=[]
with ThreadPoolExecutor(max_workers=12) as pool:
    for future in as_completed([pool.submit(get,u) for u in urls]):
        result,_=future.result();checks.append(result)
write('registry_regulator_endpoint_checks.csv',checks)
(OUT/'regulator_validation.json').write_text(json.dumps(dict(iosco_entries=len(records),
    category_counts={c:sum(r['category']==c for r in records) for c in ('ORDINARY','ASSOCIATE','AFFILIATE')},
    unique_regulator_endpoints=len(urls),checked_regulator_endpoints=len(checks),WFE_entries=len(wfe)),indent=2)+'\n',encoding='utf-8')
