from pathlib import Path
import csv,json,hashlib,re,urllib.request,urllib.error
from urllib.parse import urlparse,urljoin
from concurrent.futures import ThreadPoolExecutor,as_completed
from lxml import html
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/29_global_market_directories_b04_20261008'
def read(name):return list(csv.DictReader((T/name).open(encoding='utf-8-sig')))
def write(name,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
existing={r['host'] for r in read('registry_all_host_directory_discovery.csv')}
sites=[];invalid=[]
for r in read('registry_anna_prefix_numbering_agency_source.csv'):
    value=r['Website'].strip()
    if not value:continue
    url=value if value.startswith(('http://','https://')) else 'https://'+value
    parsed=urlparse(url)
    if not parsed.hostname or ' ' in parsed.hostname or parsed.username or parsed.password:
        invalid.append(dict(source_row=r['source_row'],website_raw=value,status='URL_REVIEW_REQUIRED'));continue
    sites.append(dict(source_row=r['source_row'],ISIN_prefix=r['ISIN Prefix'],jurisdiction=r['Jurisdiction'],agency=r['Organization'],url=url,host=parsed.hostname,
                      substitute_agency=r['Substitute Agency'],source='https://anna-web.org/anna-members/'))
write('registry_anna_source_websites.csv',sites);write('registry_anna_website_review.csv',invalid)
new=sorted({r['host'] for r in sites}-existing);checks=[];links=[]
pattern=re.compile(r'listed|listing|issuer|securit|equities|company|companies|member|participant|broker|register|directory|download|open.?data|ISIN|FISN|CFI|上市|名錄|名录|證券|证券|会员|會員|licen[cs]',re.I)
def get(host):
    url='https://'+host+'/';result=dict(host=host,url=url,source='ANNA_NEW_HOST',checked_on='2026-10-08');found=[]
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchDirectoryInventory/1.0'}),timeout=8) as response:
            b=response.read(131073);result.update(http_status=response.status,final_url=response.url,observed_bytes=len(b),prefix_limited=len(b)>131072,sha256_observed=hashlib.sha256(b).hexdigest())
        tree=html.fromstring(b)
        for a in tree.xpath('//a[@href]'):
            text=' '.join(a.text_content().split());target=urljoin(result['final_url'],a.get('href'));p=urlparse(target)
            if p.scheme in ('http','https') and not p.username and not p.password and pattern.search(text+' '+target):
                found.append(dict(host=host,observed_page=result['final_url'],target_url=target,anchor_text=text,evidence='OBSERVED_LINK_NOT_DIRECTORY_CONTENT_VERIFIED',source_body_sha256_observed=result['sha256_observed']))
        result['directory_links']=len(found)
    except urllib.error.HTTPError as e:result.update(http_status=e.code,error='HTTP_ERROR')
    except Exception as e:result.update(http_status='',error=type(e).__name__)
    return result,found
print('new ANNA hosts',len(new),flush=True)
with ThreadPoolExecutor(max_workers=12) as pool:
    for job in as_completed([pool.submit(get,h) for h in new]):
        result,found=job.result();checks.append(result);links.extend(found)
write('registry_anna_new_host_checks.csv',checks);write('registry_anna_observed_directory_links.csv',links)
print(json.dumps(dict(anna_website_rows=len(sites),new_hosts=len(new),new_host_checks=len(checks),directory_candidate_links=len(links))),flush=True)
