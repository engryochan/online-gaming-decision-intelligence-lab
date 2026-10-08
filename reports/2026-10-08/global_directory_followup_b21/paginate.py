from pathlib import Path
import sys,csv,json,re,collections,threading
from urllib.parse import urlparse,urldefrag
from concurrent.futures import ThreadPoolExecutor,as_completed
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/46_global_directory_followup_b21_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
intake.O=O;intake.T=T;intake.D=O/'raw';intake.D.mkdir(exist_ok=True);intake.locks={}
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
assert not (O/'pagination_acceptance.json').exists()
observations=read(T/'registry_pagination_links.csv')+read(R/'Reference/tables/44_global_directory_followup_b19_20261008/registry_pagination_link_observations.csv')
seen=set()
for folder in ['30_global_directory_content_b05_20261008','31_global_directory_content_b06_20261008','32_global_directory_content_b07_20261008','35_global_directory_content_b10_20261008','37_global_directory_content_b12_20261008','38_global_directory_followup_b13_20261008','39_global_directory_content_b14_20261008','40_global_directory_followup_b15_20261008','41_global_directory_content_b16_20261008','42_global_directory_followup_b17_20261008','43_global_directory_content_b18_20261008','44_global_directory_followup_b19_20261008','45_global_directory_content_b20_20261008']:
    for name in ['directory_fetch_manifest.csv','pagination_fetch_manifest.csv']:
        path=R/'Reference/tables'/folder/name
        if path.exists():seen.update(urldefrag(r['url'])[0] for r in read(path))
review=[];unique={}
for r in observations:
    url=urldefrag(r['target_url'])[0];label=r.get('label','').strip();origin=r.get('source_url','')
    signal=bool(re.search(r'(?:[?&](?:page|p|start|offset|paged)=\d+|/page/\d+)',url,re.I) or re.fullmatch(r'\d+|next|previous|prev|下一頁|上一頁|›|»|‹|«',label,re.I))
    reason='PAGINATION_SIGNAL_REQUIRES_SOURCE_SCOPE_REVIEW'
    if url in seen:reason='ALREADY_ATTEMPTED_IN_PRIOR_OR_CURRENT_BATCH'
    elif not signal:reason='NAVIGATION_LINK_NOT_CONFIRMED_PAGINATION'
    elif origin and urlparse(origin).hostname!=urlparse(url).hostname:reason='CROSS_HOST_REVIEW'
    else:unique.setdefault(url,dict(r,target_url=url))
    review.append(dict(**r,pagination_signal=signal,review_reason=reason))
hosts=collections.defaultdict(list)
for r in unique.values():hosts[urlparse(r['target_url']).hostname].append(r)
selected=[]
for depth in range(max(map(len,hosts.values()),default=0)):
    for host in sorted(hosts):
        if depth<len(hosts[host]):selected.append(hosts[host][depth])
    if len(selected)>=100:break
selected=selected[:100];selectedurls={r['target_url'] for r in selected}
intake.write('registry_pagination_candidate_review.csv',review)
intake.write('registry_pagination_gaps.csv',[dict(r,status='PENDING_BODY_AND_SOURCE_SCOPE_REVIEW') for u,r in unique.items() if u not in selectedurls])
results=[];rows=[];downloads=[];newlinks=[]
for r in selected:intake.locks[urlparse(r['target_url']).hostname]=threading.Semaphore(2)
with ThreadPoolExecutor(max_workers=10) as pool:
    jobs=[dict(work_id=r['work_id'],target_url=r['target_url'],selection_evidence='B21 explicit pagination signal; lineage:'+r.get('source_url','PRIOR_GAP_SOURCE_UNKNOWN')) for r in selected]
    for future in as_completed([pool.submit(intake.get,r) for r in jobs]):
        result,a,b,c=future.result();results.append(result);rows.extend(a);downloads.extend(b);newlinks.extend(c)
intake.write('pagination_fetch_manifest.csv',results);intake.write('registry_pagination_all_table_rows.csv',rows);intake.write('registry_pagination_download_links.csv',downloads);intake.write('registry_pagination_link_observations.csv',newlinks)
summary=dict(candidate_observations=len(observations),candidate_review_reasons=dict(collections.Counter(r['review_reason'] for r in review)),selected_pages=len(selected),fetched_additional_pages=len(results),additional_table_rows=len(rows),pending_gap_records=len(unique)-len(selected),new_link_observations_pending_review=len(newlinks),all_observed_in_scope_page_links_attempted=False,source_directory_total_completeness='UNKNOWN')
(O/'pagination_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))
