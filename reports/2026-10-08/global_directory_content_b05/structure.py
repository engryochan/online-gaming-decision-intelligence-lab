from pathlib import Path
import csv,json,re,collections,hashlib
from urllib.parse import urlparse
from lxml import html
import intake
O=intake.O;T=intake.T
def read(name):return list(csv.DictReader((T/name).open(encoding='utf-8-sig')))
all_rows=read('registry_directory_all_table_rows.csv')+read('registry_pagination_all_table_rows.csv')
groups=collections.defaultdict(list)
for r in all_rows:groups[(r['source_url'],r['table'])].append(r)
name_fields={'company','company name','name of issuer','issuer','member name','name','firm','entity','member','broker','name of participant'}
symbol_fields={'symbol','stock code','pngx code','code','member code','participant code in dss'}
entities=[];analyses=[]
for (url,table),rows in groups.items():
    first=json.loads(rows[0]['cells_json']);headers=json.loads(rows[0]['headers_json']) or first
    normalized=[' '.join(s.lower().split()) for s in headers]
    role='DIRECTORY_RECORD_REVIEW'
    if '/blacklist' in url:role='BLACKLIST_SOURCE_RECORD_NOT_ACTIVE_LICENSE'
    elif 'delisted' in url or 'suspended' in url:role='DELISTED_OR_SUSPENDED_SOURCE_RECORD'
    elif 'non-listed' in url:role='NON_LISTED_ISSUER_OR_PARTICIPANT_REVIEW'
    elif 'ecc.de' in url:role='COMMODITY_CLEARING_PARTICIPANT_NOT_EQUITY_BROKER_LICENSE'
    elif 'funds/brokers' in url:role='FUND_MARKET_BROKER_SOURCE_RECORD'
    elif 'new-company-listings' in url or 'new-listed-issuers' in url:role='NEW_LISTING_EVENT_NOT_CURRENT_UNIVERSE'
    elif '/screener' in url:role='SECURITY_SCREEN_RECORD_NOT_VERIFIED_UNIQUE_COMPANY'
    elif 'market-snapshot' in url:role='MARKET_SNAPSHOT_SECURITY_RECORD'
    elif 'Type of Fund'.lower() in normalized:role='PENSION_FUND_SOURCE_RECORD_NOT_BROKER'
    elif 'participant' in url or 'member' in url or 'broker' in url:role='MEMBER_OR_PARTICIPANT_SOURCE_RECORD'
    elif 'listed-compan' in url:role='LISTED_COMPANY_SOURCE_RECORD_SCOPE_PENDING'
    name_index=next((i for i,h in enumerate(normalized) if h in name_fields),None)
    symbol_index=next((i for i,h in enumerate(normalized) if h in symbol_fields),None)
    if 'gse.com.gh' in url and 'name of issuer' in normalized:role='DEBT_ISSUER_SOURCE_RECORD_NOT_COMMON_SHARE_UNIVERSE'
    count=0
    # Transposed Ghana profiles are retained as profiles, not header/body rows.
    if len(first)==2 and first[0].lower().strip()=='company name' and rows[0]['headers_json']=='[]':
        entities.append(dict(source_url=url,table=table,row=rows[0]['row'],name=first[1],symbol='',role='TRANSPOSED_PARTICIPANT_PROFILE',
            fields_json=json.dumps({json.loads(r['cells_json'])[0]:json.loads(r['cells_json'])[1:] for r in rows if json.loads(r['cells_json'])},ensure_ascii=False),
            raw_source_rows_json=json.dumps(rows,ensure_ascii=False),evidence='SOURCE_PROFILE_PRESERVED_ENTITY_AND_CURRENT_STATUS_UNVERIFIED'))
        count=1
    elif name_index is not None or symbol_index is not None:
        for row in rows:
            cells=json.loads(row['cells_json'])
            if cells==headers or cells==first or len(cells)!=len(headers):continue
            name=cells[name_index] if name_index is not None else ''
            symbol=cells[symbol_index] if symbol_index is not None else ''
            if not name and not symbol:continue
            entities.append(dict(source_url=url,table=table,row=row['row'],name=name,symbol=symbol,role=role,
                fields_json=json.dumps(dict(zip(headers,cells)),ensure_ascii=False),raw_source_rows_json=json.dumps([row],ensure_ascii=False),
                evidence='SOURCE_TABLE_RECORD_NOT_GLOBAL_OR_UNIQUE_COMPANY_VERIFICATION'))
            count+=1
    analyses.append(dict(source_url=url,table=table,physical_source_rows=len(rows),headers_json=json.dumps(headers,ensure_ascii=False),
                         structured_records=count,role=role if count else 'NO_ENTITY_PROJECTION_HEADER_OR_CONTENT_REVIEW',all_rows_preserved=True))
intake.write('registry_structured_directory_records.csv',entities)
intake.write('registry_source_table_semantic_review.csv',analyses)
# Every page remains visible, including empty/dynamic tables and non-directory PDFs.
manifest=read('directory_fetch_manifest.csv')+read('pagination_fetch_manifest.csv');page_reviews=[]
for result in manifest:
    tables=[r for r in analyses if r['source_url']==result['url']]
    page_reviews.append(dict(source_url=result['url'],http_status=result.get('http_status',''),
        observed_table_rows=sum(int(r['physical_source_rows']) for r in tables),structured_records=sum(int(r['structured_records']) for r in tables),
        gap='DYNAMIC_EMPTY_OR_NON_TABULAR_DIRECTORY_REVIEW' if not any(int(r['structured_records']) for r in tables) else 'PAGE_SCOPE_AND_TOTAL_RECONCILIATION_PENDING',
        body_truncated=result.get('truncated','UNKNOWN'),
        full_body_observed='TRUE' if result.get('http_status')=='200' and result.get('truncated')=='False' else 'UNKNOWN',global_directory_completeness='UNKNOWN'))
intake.write('registry_all_page_content_review.csv',page_reviews)
by_hash=collections.defaultdict(list)
for result in manifest:
    if result.get('sha256'):by_hash[result['sha256']].append(result['url'])
intake.write('registry_identical_body_source_observations.csv',[dict(sha256=k,source_urls_json=json.dumps(v),url_observations=len(v),
    decision='KEEP_ALL_URL_OBSERVATIONS_REVIEW_CANONICAL_OR_FALLBACK_CONTENT') for k,v in by_hash.items() if len(v)>1])
summary=dict(all_table_rows=len(all_rows),tables=len(groups),structured_source_records=len(entities),source_urls_with_structured_records=len({r['source_url'] for r in entities}),
    role_counts=dict(collections.Counter(r['role'] for r in entities)),distinct_company_count='UNKNOWN',source_rows_not_dropped=True)
(O/'structure_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary),flush=True)
# Save only DOM selector diagnostics for a non-tabular regulator page.
for r in manifest:
    if 'cmauganda.co.ug/cma-licensed-firms' in r['url'] and r.get('file'):
        tree=html.fromstring((intake.R/r['file']).read_bytes())
        diagnostics=[dict(tag=n.tag,classes=n.get('class',''),text=' '.join(n.text_content().split())) for n in tree.xpath('//h2|//h3|//h4')]
        (O/'cma_heading_review.json').write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
