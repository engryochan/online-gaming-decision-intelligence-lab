from pathlib import Path
import csv,json,hashlib,io,re,time,urllib.request,urllib.error
from urllib.parse import urlparse,urljoin
from concurrent.futures import ThreadPoolExecutor,as_completed
from lxml import html

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
TABLE=ROOT/'Reference/tables/28_global_market_sources_b03_20261008'
TABLE.mkdir(parents=True,exist_ok=True)
RAW=OUT/'raw';RAW.mkdir(exist_ok=True)
STAMP='2026-10-08'
def digest(b):return hashlib.sha256(b).hexdigest()
def fetch(url,limit=2000000):
    started=time.monotonic()
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'ResearchSourceInventory/1.0'})
        with urllib.request.urlopen(req,timeout=12) as response:
            data=response.read(limit+1)
            return dict(url=url,final_url=response.url,http_status=response.status,bytes_observed=len(data),
                        truncated=len(data)>limit,sha256_observed=digest(data),elapsed_seconds=round(time.monotonic()-started,2),
                        checked_on=STAMP,status='HTTP_RESPONSE_NOT_DIRECTORY_COMPLETENESS'),data
    except urllib.error.HTTPError as error:
        return dict(url=url,final_url=error.url,http_status=error.code,status='HTTP_ERROR',checked_on=STAMP),b''
    except Exception as error:
        return dict(url=url,http_status='',status='NETWORK_ERROR',error_type=type(error).__name__,checked_on=STAMP),b''

def write(name,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (TABLE/name).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)

catalogs=[('ISO10383','https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv'),
          ('WFE','https://www.world-exchanges.org/membership-events'),
          ('IOSCO','https://www.iosco.org/about/?subsection=membership')]
catalog_results=[];payload={}
for label,url in catalogs:
    record,data=fetch(url,10000000);record['catalog']=label
    if data:
        (RAW/(label+'.response')).write_bytes(data)
    catalog_results.append(record);payload[label]=data
write('catalog_fetch_manifest.csv',catalog_results)
if payload['ISO10383'] and catalog_results[0].get('http_status')==200:
    mic=list(csv.DictReader(io.StringIO(payload['ISO10383'].decode('utf-8-sig'))))
    mic_origin='LIVE_ISO10383_DOWNLOAD'
else:
    original=ROOT/'Reference/tables/24_financial_universe_b06_20261007/registry_iso10383_mic.csv'
    mic=[json.loads(r['raw_fields_json']) for r in csv.DictReader(original.open(encoding='utf-8-sig'))]
    mic_origin='PRESERVED_20261007_SOURCE_LIVE_FETCH_FAILED'
sources=[];relations=[];unusable=[]
def normalize(value):
    value=value.strip()
    if not value:return ''
    if not value.lower().startswith(('http://','https://')):value='https://'+value
    parsed=urlparse(value)
    if not parsed.hostname or '.' not in parsed.hostname or parsed.username or parsed.password:return ''
    return value
for r in mic:
    website=r.get('WEBSITE','');url=normalize(website)
    relations.append(dict(MIC=r.get('MIC',''),operating_MIC=r.get('OPERATING MIC',''),market=r.get('MARKET NAME-INSTITUTION DESCRIPTION',''),
                          country_iso=r.get('ISO COUNTRY CODE (ISO 3166)',''),market_category=r.get('MARKET CATEGORY CODE',''),
                          market_status=r.get('STATUS',''),website_raw=website,url=url,source=mic_origin))
    if url:sources.append(dict(url=url,kind='MIC_REGISTERED_SITE',discovery_source=mic_origin))
    else:unusable.append(dict(MIC=r.get('MIC',''),website_raw=website,reason='NO_USABLE_WEBSITE_IN_SOURCE'))
wfe=[]
if payload['WFE'] and catalog_results[1].get('http_status')==200:
    tree=html.fromstring(payload['WFE'])
    # Keep every named list item in the membership section, including missing links.
    headings=tree.xpath('//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5]')
    anchor=next((h for h in headings if 'Full list of Members' in h.text_content()),None)
    if anchor is not None:
        for node in tree.xpath('//section[@id="member-list"]//li'):
            text=' '.join(node.text_content().split())
            links=node.xpath('.//a[@href]/@href')
            external=[urljoin(catalogs[1][1],u) for u in links if urlparse(urljoin(catalogs[1][1],u)).hostname not in ('www.world-exchanges.org','world-exchanges.org')]
            if text and (external or not links):
                for url in external or ['']:
                    wfe.append(dict(name=text,url=url,source=catalogs[1][1],country_status='UNASSIGNED_PENDING_ENTITY_MATCH'))
                    if url:sources.append(dict(url=url,kind='WFE_DIRECTORY_SITE',discovery_source=catalogs[1][1]))
write('registry_wfe_directory_entries.csv',wfe)
prior=[]
for folder in sorted((ROOT/'Reference/tables').iterdir()):
    if not any(folder.name.startswith(prefix) for prefix in ('19_','20_','21_','22_','23_','24_','25_','26_','27_')):continue
    for path in folder.glob('*manifest.csv'):
        for r in csv.DictReader(path.open(encoding='utf-8-sig')):
            url=r.get('url') or r.get('source_url')
            if url and normalize(url):
                prior.append(dict(manifest=path.relative_to(ROOT).as_posix(),**r))
                sources.append(dict(url=url,kind='PREVIOUS_COLLECTION_ENDPOINT',discovery_source=path.relative_to(ROOT).as_posix()))
write('prior_collection_source_audit.csv',prior)
supplement=[('GLOBAL_REGULATOR','https://www.iosco.org/'),('US_REGULATOR','https://www.sec.gov/'),
('US_BROKER_REGULATOR','https://www.finra.org/'),('BRAZIL_REGULATOR','https://dados.cvm.gov.br/'),
('GLOBAL_ENTITY_IDENTIFIERS','https://www.gleif.org/'),('GLOBAL_INSTRUMENT_IDENTIFIERS','https://www.openfigi.com/'),
('CURRENCY_REGISTRATION_AUTHORITY','https://www.six-group.com/en/products-services/financial-information/data-standards.html'),
('LICENSED_VENDOR','https://www.bloomberg.com/professional/'),('LICENSED_VENDOR','https://www.lseg.com/en/data-analytics'),
('LICENSED_VENDOR','https://www.factset.com/'),('LICENSED_VENDOR','https://www.spglobal.com/marketintelligence/'),
('LICENSED_VENDOR','https://www.msci.com/'),('LICENSED_VENDOR','https://www.ice.com/market-data'),
('LICENSED_VENDOR','https://www.moodys.com/web/en/us/capabilities/company-reference-data/orbis.html')]
sources.extend(dict(url=u,kind=k,discovery_source='SUPPLEMENTAL_CANDIDATE_NOT_EXHAUSTIVE') for k,u in supplement)
unique={}
for r in sources:
    unique.setdefault(r['url'],[]).append(r)
registry=[dict(url=url,discovery_kinds='|'.join(sorted(set(r['kind'] for r in rows))),
               provenance_json=json.dumps(rows,ensure_ascii=False),evidence='DISCOVERED_NOT_FULL_DIRECTORY_VERIFIED') for url,rows in sorted(unique.items())]
write('registry_global_source_endpoints.csv',registry)
write('registry_all_MIC_source_relations.csv',relations)
write('registry_MIC_missing_websites.csv',unusable)
countries=list(csv.DictReader((ROOT/'Reference/tables/01_country_area/registry_country_area_iso3166_20261003.csv').open(encoding='utf-8-sig')))
coverage=[]
for country in countries:
    code=country['iso_alpha2'];rows=[r for r in relations if r['country_iso']==code]
    coverage.append(dict(iso_alpha2=code,name_en=country['name_en'],MIC_rows=len(rows),
                         website_endpoints=len(set(r['url'] for r in rows if r['url'])),
                         listed_company_completeness='UNKNOWN',broker_completeness='UNKNOWN',currency_completeness='UNKNOWN',
                         gap='DIRECTORY_ENUMERATION_AND_REGULATOR_CROSSCHECK_PENDING' if rows else 'NO_MIC_ROW_OBSERVED_NOT_PROOF_OF_NO_MARKET'))
write('registry_all_country_source_coverage.csv',coverage)
print(json.dumps(dict(MIC_rows=len(mic),endpoints=len(registry),country_rows=len(coverage),WFE_entries=len(wfe),prior_sources=len(prior))),flush=True)
probes=[]
with ThreadPoolExecutor(max_workers=12) as pool:
    jobs={pool.submit(fetch,r['url']):r['url'] for r in registry}
    with (OUT/'probe_progress.jsonl').open('w',encoding='utf-8') as f:
        for job in as_completed(jobs):
            record,_=job.result();probes.append(record);f.write(json.dumps(record,ensure_ascii=False)+'\n');f.flush()
            if len(probes)%50==0:print('probed',len(probes),'of',len(registry),flush=True)
write('registry_endpoint_live_checks.csv',sorted(probes,key=lambda r:r['url']))
summary=dict(MIC_rows=len(mic),MIC_origin=mic_origin,source_endpoints=len(registry),probed_endpoints=len(probes),
             HTTP_200=sum(r.get('http_status')==200 for r in probes),WFE_entries=len(wfe),country_rows=len(coverage),
             countries_with_MIC=len(set(r['country_iso'] for r in relations)),prior_collection_manifest_rows=len(prior),
             all_countries_complete=False,all_global_websites_enumerated=False)
(OUT/'validation.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary),flush=True)
