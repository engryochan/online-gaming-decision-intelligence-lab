"""Discover directory links on every host in B03, without selecting a few markets."""
from pathlib import Path
import csv,json,hashlib,urllib.request,urllib.error,time,re
from urllib.parse import urlparse,urljoin
from concurrent.futures import ThreadPoolExecutor,as_completed
from lxml import html
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/29_global_market_directories_b04_20261008';T.mkdir(parents=True,exist_ok=True)
B=R/'Reference/tables/28_global_market_sources_b03_20261008';sources=list(csv.DictReader((B/'registry_global_source_endpoints.csv').open(encoding='utf-8-sig')))
hosts={}
for row in sources:
    host=urlparse(row['url']).hostname
    if host:hosts.setdefault(host,[]).append(row['url'])
keywords=re.compile(r'listed|listing|issuer|securit|equities|company|companies|member|participant|broker|register|directory|download|open.?data|上市|名錄|名录|證券|证券|会员|會員|成員|成员|licen[cs]|cotiz|emisora|cotation|soci.t.s|empresas',re.I)
def crawl(host,urls):
    url='https://'+host+'/'
    result=dict(host=host,url=url,source_endpoint_count=len(urls),source_endpoints_json=json.dumps(urls),checked_on='2026-10-08')
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchDirectoryInventory/1.0'}),timeout=8) as response:
            # Bound page observations; do not present a prefix as a full-page archive.
            data=response.read(131073);result.update(http_status=response.status,final_url=response.url,observed_bytes=len(data),prefix_limited=len(data)>131072,sha256_observed=hashlib.sha256(data).hexdigest())
        tree=html.fromstring(data);links=[];seen=set()
        for a in tree.xpath('//a[@href]'):
            label=' '.join(a.text_content().split());target=urljoin(result['final_url'],a.get('href'))
            p=urlparse(target)
            if p.scheme not in ('http','https') or p.username or p.password:continue
            if not keywords.search(label+' '+target) or target in seen:continue
            seen.add(target);links.append(dict(host=host,observed_page=result['final_url'],target_url=target,anchor_text=label,
                keyword_matches='|'.join(sorted(set(m.group().lower() for m in keywords.finditer(label+' '+target)))),
                evidence='OBSERVED_LINK_NOT_DIRECTORY_CONTENT_VERIFIED',source_body_sha256_observed=result['sha256_observed']))
        result['directory_links']=len(links)
        return result,links
    except urllib.error.HTTPError as e:result.update(http_status=e.code,error='HTTP_ERROR')
    except Exception as e:result.update(http_status='',error=type(e).__name__)
    return result,[]
def write(name,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
checks=[];candidates=[]
print('hosts',len(hosts),'source endpoints',len(sources),flush=True)
with ThreadPoolExecutor(max_workers=16) as pool:
    futures=[pool.submit(crawl,h,u) for h,u in sorted(hosts.items())]
    with (O/'discovery_progress.jsonl').open('w',encoding='utf-8') as stream:
        for future in as_completed(futures):
            result,links=future.result();checks.append(result);candidates.extend(links)
            stream.write(json.dumps(dict(check=result,links=links),ensure_ascii=False)+'\n');stream.flush()
            if len(checks)%50==0:print('hosts inspected',len(checks),'links',len(candidates),flush=True)
write('registry_all_host_directory_discovery.csv',checks)
write('registry_observed_directory_links.csv',candidates)
missing=[dict(host=r['host'],http_status=r.get('http_status',''),gap='NO_MATCHING_LINK_IN_OBSERVED_PREFIX_NOT_PROOF_OF_NO_DIRECTORY',source_endpoint_count=r['source_endpoint_count']) for r in checks if not r.get('directory_links')]
write('registry_directory_discovery_gaps.csv',missing)
(O/'discovery_acceptance.json').write_text(json.dumps(dict(source_endpoints=len(sources),expected_hosts=len(hosts),observed_hosts=len(checks),directory_candidate_links=len(candidates),hosts_with_links=sum(bool(r.get('directory_links')) for r in checks),global_complete=False),indent=2)+'\n',encoding='utf-8')
print('complete',len(checks),len(candidates),flush=True)
