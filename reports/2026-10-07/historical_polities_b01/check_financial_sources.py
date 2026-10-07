from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError
from lxml import html
from urllib.parse import urljoin
import json,hashlib,csv
O=Path(__file__).parent;D=O/'raw';T=O.parents[2]/'Reference/tables/26_historical_polities_b01_20261007';results=[]
url='https://catalog.data.gov/dataset/company-information-about-active-broker-dealers'
with urlopen(url,timeout=60) as r:b=r.read()
(D/'sec_datagov_catalog.html').write_bytes(b);t=html.fromstring(b)
links=[urljoin(url,a.get('href')) for a in t.xpath('//a[@href]') if a.get('href').endswith('/bd090126.txt')];assert links
u=links[0]
try:
 with urlopen(u,timeout=60) as r:raw=r.read();code=r.status
 (D/'sec_broker_dealers_20260901.txt').write_bytes(raw);results.append(dict(country='US',source_url=u,status='DOWNLOADED_REQUIRES_PARSE_AND_SCOPE_REVIEW',http_status=code,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),source_period='2026-09',all_brokers_complete='UNKNOWN'))
except HTTPError as e:
 raw=e.read();(D/'sec_broker_download_error.html').write_bytes(raw);results.append(dict(country='US',source_url=u,status='SOURCE_ACCESS_DENIED_NO_ROWS_INGESTED',http_status=e.code,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),source_period='2026-09',all_brokers_complete='UNKNOWN'))
(O/'financial_source_checks.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8');print(json.dumps(results))
