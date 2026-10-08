from pathlib import Path
import csv,json,hashlib
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from lxml import html
from urllib.parse import urljoin
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/29_global_market_directories_b04_20261008'
url='https://anna-web.org/anna-members/'
try:
    with urlopen(Request(url,headers={'User-Agent':'ResearchDirectoryInventory/1.0'}),timeout=20) as response:
        b=response.read();status=response.status
except HTTPError as e:b=e.read();status=e.code
(O/'ANNA_members.response').write_bytes(b)
rows=[];metadata=dict(url=url,http_status=status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),checked_on='2026-10-08')
if status==200:
    tree=html.fromstring(b)
    for table in tree.xpath('//table'):
        heads=[' '.join(t.text_content().split()) for t in table.xpath('.//thead//th')]
        if 'ISIN Prefix' not in heads:continue
        for number,tr in enumerate(table.xpath('.//tbody/tr'),1):
            cells=[' '.join(td.text_content().split()) for td in tr.xpath('./td')]
            values=dict(zip(heads,cells))
            rows.append(dict(source_row=number,**values,raw_cells_json=json.dumps(cells,ensure_ascii=False),source_url=url,
                             semantic_status='SOURCE_PREFIX_JURISDICTION_NOT_AUTOMATICALLY_ISO_COUNTRY'))
def write(name,values):
    fields=list(dict.fromkeys(k for v in values for k in v))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(values)
write('registry_anna_prefix_numbering_agency_source.csv',rows)
mother=list(csv.DictReader((R/'Reference/tables/01_country_area/registry_country_area_iso3166_20261003.csv').open(encoding='utf-8-sig')))
coverage=[]
for country in mother:
    matching=[r for r in rows if r.get('ISIN Prefix')==country['iso_alpha2']]
    coverage.append(dict(iso_alpha2=country['iso_alpha2'],name_en=country['name_en'],anna_source_rows=len(matching),
                         source_agencies_json=json.dumps(matching,ensure_ascii=False),
                         evidence='EXACT_PREFIX_MATCH_JURISDICTION_REVIEW_PENDING' if matching else 'NO_EXACT_PREFIX_IN_SOURCE_REVIEW_ALIAS_OR_SUBSTITUTE',
                         all_instruments_complete='UNKNOWN'))
write('registry_all_country_anna_coverage.csv',coverage)
metadata.update(source_rows=len(rows),membership_status_counts={k:sum(r.get('Membership Status')==k for r in rows) for k in sorted({r.get('Membership Status','') for r in rows})},
                mother_rows=len(coverage),countries_with_prefix_match=sum(bool(int(r['anna_source_rows'])) for r in coverage))
(O/'anna_acceptance.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
print(json.dumps(metadata),flush=True)
