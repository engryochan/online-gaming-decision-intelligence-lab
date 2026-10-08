from pathlib import Path
import sys,csv,json,collections
from urllib.parse import urlparse,urldefrag
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/47_global_directory_content_b22_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.T=T
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def host(url):return (urlparse(url).hostname or '').lower().removeprefix('www.')
receipts=collections.defaultdict(list)
batches=['30_global_directory_content_b05_20261008','31_global_directory_content_b06_20261008','32_global_directory_content_b07_20261008','35_global_directory_content_b10_20261008','37_global_directory_content_b12_20261008','38_global_directory_followup_b13_20261008','39_global_directory_content_b14_20261008','40_global_directory_followup_b15_20261008','41_global_directory_content_b16_20261008','42_global_directory_followup_b17_20261008','43_global_directory_content_b18_20261008','44_global_directory_followup_b19_20261008','45_global_directory_content_b20_20261008','46_global_directory_followup_b21_20261008','47_global_directory_content_b22_20261008']
for batch in batches:
    for n in ['directory_fetch_manifest.csv','pagination_fetch_manifest.csv']:
        for row in read(R/'Reference/tables'/batch/n):receipts[urldefrag(row['url'])[0]].append(dict(batch=batch,**row))
queue=read(R/'Reference/tables/30_global_directory_content_b05_20261008/registry_all_workqueue_priority_review.csv');ledger=[]
for r in queue:
    observations=receipts.get(urldefrag(r['target_url'])[0],[]);last=observations[-1] if observations else {}
    status='NOT_YET_ATTEMPTED'
    if observations:
        if last.get('http_status')=='200':status='HTTP200_BODY_TRUNCATED_REVIEW' if last.get('truncated')=='True' else 'HTTP200_CONTENT_AND_UNIVERSE_SCOPE_REVIEW'
        else:status='FETCH_ERROR_OR_NON200_REVIEW'
    ledger.append(dict(**r,attempt_observations=len(observations),last_http_status=last.get('http_status',''),acquisition_status=status,receipts_json=json.dumps(observations,ensure_ascii=False),directory_completeness='UNKNOWN'))
intake.write('registry_all_4849_work_progress.csv',ledger)
mother=read(R/'Reference/tables/28_global_market_sources_b03_20261008/registry_all_country_source_coverage.csv');codes={r['iso_alpha2'] for r in mother};associations=[]
for r in read(R/'Reference/tables/28_global_market_sources_b03_20261008/registry_all_MIC_source_relations.csv'):
    if r['country_iso'] in codes and r.get('url'):associations.append(dict(iso_alpha2=r['country_iso'],host=host(r['url']),source='ISO10383_MIC_REGISTERED_WEBSITE',source_key=r['MIC'],source_url=r['url'],meaning='REGISTERED_SOURCE_ASSOCIATION_NOT_ISSUER_DOMICILE_OR_DIRECTORY_COMPLETENESS'))
for r in read(R/'Reference/tables/29_global_market_directories_b04_20261008/registry_anna_source_websites.csv'):
    if r['ISIN_prefix'] in codes:associations.append(dict(iso_alpha2=r['ISIN_prefix'],host=host(r['url']),source='ANNA_EXACT_PREFIX_COUNTRY_ASSOCIATION_REVIEW',source_key=r['source_row'],source_url=r['url'],meaning='PREFIX_JURISDICTION_SEMANTIC_REVIEW_NOT_AUTOMATIC_COUNTRY_CERTIFICATION'))
byhost=collections.defaultdict(list)
for r in ledger:
    hosts={host(r['target_url'])}|{h.lower().removeprefix('www.') for h in r.get('discovery_hosts','').split('|') if h}
    for h in hosts:byhost[h].append(r)
country=[]
for m in mother:
    linked=[r for r in associations if r['iso_alpha2']==m['iso_alpha2']];work={r['target_url']:r for a in linked for r in byhost.get(a['host'],[])}
    states=collections.Counter(r['acquisition_status'] for r in work.values())
    country.append(dict(**m,source_association_rows=len(linked),associated_hosts=len({r['host'] for r in linked}),associated_queue_items=len(work),attempted_associated_items=sum(r['attempt_observations']>0 for r in work.values()),unattempted_associated_items=states['NOT_YET_ATTEMPTED'],association_states_json=json.dumps(states),association_meaning='WEBSITE_SOURCE_RELATION_ONLY_NOT_PROOF_OF_COMPANY_DOMICILE_OR_FULL_COVERAGE'))
intake.write('registry_all_country_cumulative_source_progress.csv',country);intake.write('registry_source_country_association_evidence.csv',associations)
summary=dict(original_queue=len(ledger),state_counts=dict(collections.Counter(r['acquisition_status'] for r in ledger)),total_attempt_receipts=sum(len(v) for v in receipts.values()),unique_attempted_urls=len(receipts),country_mother_rows=len(country),countries_with_source_association=sum(int(r['source_association_rows'])>0 for r in country),global_complete=False)
(O/'ledger_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))
