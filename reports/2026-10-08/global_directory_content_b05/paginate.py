import csv,json,threading
from urllib.parse import urlparse,urldefrag
from concurrent.futures import ThreadPoolExecutor,as_completed
import intake
O=intake.O;T=intake.T
assert not (O/'pagination_progress.jsonl').exists()
def read(name):return list(csv.DictReader((T/name).open(encoding='utf-8-sig')))
seen={urldefrag(r['url'])[0] for r in read('directory_fetch_manifest.csv')}
pending=read('registry_directory_observed_pagination.csv');results=[];rows=[];downloads=[];observed=[];gaps=[]
with (O/'pagination_progress.jsonl').open('w',encoding='utf-8') as stream:
    while pending:
        batch=[]
        for p in pending:
            target=urldefrag(p['target_url'])[0]
            if target in seen:continue
            if urlparse(target).hostname!=urlparse(p['source_url']).hostname:
                gaps.append(dict(**p,reason='CROSS_HOST_PAGE_LINK_REVIEW'));continue
            seen.add(target)
            intake.locks.setdefault(urlparse(target).hostname,threading.Semaphore(2))
            batch.append(dict(work_id=p['work_id'],target_url=target,selection_evidence='OBSERVED_PAGINATION_FROM:'+p['source_url']))
        if not batch:break
        if len(results)+len(batch)>500:
            gaps.extend(dict(**item,reason='BATCH_PAGE_LIMIT_REVIEW_PENDING') for item in batch);break
        pending=[]
        with ThreadPoolExecutor(max_workers=6) as pool:
            for future in as_completed([pool.submit(intake.get,p) for p in batch]):
                result,r,d,p=future.result();results.append(result);rows.extend(r);downloads.extend(d);observed.extend(p);pending.extend(p)
                stream.write(json.dumps(dict(result=result,rows=r,downloads=d,pages=p),ensure_ascii=False)+'\n');stream.flush()
        print('pagination pages',len(results),flush=True)
intake.write('pagination_fetch_manifest.csv',results);intake.write('registry_pagination_all_table_rows.csv',rows)
intake.write('registry_pagination_download_links.csv',downloads);intake.write('registry_pagination_link_observations.csv',observed)
intake.write('registry_pagination_gaps.csv',gaps)
summary=dict(fetched_additional_pages=len(results),additional_table_rows=len(rows),observed_links=len(observed),pending_gap_records=len(gaps),
             all_observed_in_scope_page_links_attempted=not gaps,source_directory_total_completeness='UNKNOWN')
(O/'pagination_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))
