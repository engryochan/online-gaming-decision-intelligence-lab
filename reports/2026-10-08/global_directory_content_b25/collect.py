from pathlib import Path
import sys,csv,json,re,collections,threading,sqlite3,hashlib
from urllib.parse import urlparse,urldefrag
from concurrent.futures import ThreadPoolExecutor,as_completed
O=Path(__file__).resolve().parent;R=O.parents[2]
sys.path.insert(0,str(O.parent/'global_directory_content_b05'))
import intake
T=R/'Reference/tables/50_global_directory_content_b25_20261008';T.mkdir(parents=True,exist_ok=True)
intake.O=O;intake.T=T;intake.D=O/'raw';intake.D.mkdir(exist_ok=True)
assert not (O/'fetch_manifest.json').exists(),'Preserve completed batch'
def read(path):return list(csv.DictReader(path.open(encoding='utf-8-sig')))
queue=read(R/'Reference/tables/30_global_directory_content_b05_20261008/registry_all_workqueue_priority_review.csv')
previous=read(R/'Reference/tables/30_global_directory_content_b05_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/30_global_directory_content_b05_20261008/pagination_fetch_manifest.csv')
previous+=read(R/'Reference/tables/31_global_directory_content_b06_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/31_global_directory_content_b06_20261008/pagination_fetch_manifest.csv')
previous+=read(R/'Reference/tables/32_global_directory_content_b07_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/32_global_directory_content_b07_20261008/pagination_fetch_manifest.csv')
previous+=read(R/'Reference/tables/35_global_directory_content_b10_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/35_global_directory_content_b10_20261008/pagination_fetch_manifest.csv')
previous+=read(R/'Reference/tables/37_global_directory_content_b12_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/37_global_directory_content_b12_20261008/pagination_fetch_manifest.csv')+read(R/'Reference/tables/38_global_directory_followup_b13_20261008/pagination_fetch_manifest.csv')
previous+=read(R/'Reference/tables/39_global_directory_content_b14_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/39_global_directory_content_b14_20261008/pagination_fetch_manifest.csv')+read(R/'Reference/tables/40_global_directory_followup_b15_20261008/pagination_fetch_manifest.csv')
previous+=read(R/'Reference/tables/41_global_directory_content_b16_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/41_global_directory_content_b16_20261008/pagination_fetch_manifest.csv')+read(R/'Reference/tables/42_global_directory_followup_b17_20261008/pagination_fetch_manifest.csv')
previous+=read(R/'Reference/tables/43_global_directory_content_b18_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/44_global_directory_followup_b19_20261008/pagination_fetch_manifest.csv')
previous+=read(R/'Reference/tables/45_global_directory_content_b20_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/46_global_directory_followup_b21_20261008/pagination_fetch_manifest.csv')
previous=list({(r['url'],r.get('file','')):r for r in previous}.values())
previous+=read(R/'Reference/tables/47_global_directory_content_b22_20261008/directory_fetch_manifest.csv')+read(R/'Reference/tables/48_global_directory_followup_b23_20261008/pagination_fetch_manifest.csv')
coverage=collections.Counter(urlparse(r['url']).hostname for r in previous)
done={urldefrag(r['url'])[0] for r in previous};candidates=[]
for row in queue:
    url=row['target_url']
    if urldefrag(url)[0] in done or row['priority'].startswith('P3'):continue
    signals=re.findall(r'issuer|equit|securit|stock|compan|instrument|participant|register|licen|broker|member|listing|directory|empresas|emittent|notiert|titres|listed|dealing|admitted',urlparse(url).path+'?'+urlparse(url).query,re.I)
    if not signals:continue
    row=dict(row,score=len(signals)+(4 if any(s.lower() in ['directory','register','listing','listed'] for s in signals) else 0)-(8 if any(s in urlparse(url).path.lower() for s in ['/news/','/blog/','/press/','/login']) else 0),hostname=urlparse(url).hostname,selection_evidence='B25 pending path and query signals: '+'|'.join(signals))
    candidates.append(row)
# Round-robin hosts before taking second and third URLs: no single market dominates.
hosts=collections.defaultdict(list)
for row in sorted(candidates,key=lambda x:(-x['score'],x['target_url'])):hosts[row['hostname']].append(row)
selected=[]
for depth in range(max(map(len,hosts.values()),default=0)):
    for host in sorted(hosts,key=lambda h:(coverage[h],h)):
        if depth<len(hosts[host]):selected.append(hosts[host][depth])
    if len(selected)>=220:break
selected=selected[:220]
intake.locks={r['hostname']:threading.Semaphore(2) for r in selected}
intake.write('registry_pending_signal_candidates.csv',candidates);intake.write('registry_selected_sources.csv',selected)
results=[];rows=[];downloads=[];pages=[]
with ThreadPoolExecutor(max_workers=12) as pool:
    with (O/'progress.jsonl').open('w',encoding='utf-8') as f:
        for future in as_completed([pool.submit(intake.get,r) for r in selected]):
            result,a,b,c=future.result();results.append(result);rows.extend(a);downloads.extend(b);pages.extend(c)
            f.write(json.dumps(result,ensure_ascii=False)+'\n');f.flush()
            if len(results)%20==0:print('completed',len(results),'table rows',len(rows),flush=True)
intake.write('directory_fetch_manifest.csv',results);intake.write('registry_all_table_rows.csv',rows)
intake.write('registry_download_links.csv',downloads);intake.write('registry_pagination_links.csv',pages)
summary=dict(original_queue=len(queue),pending_signal_candidates=len(candidates),selected=len(selected),hosts=len({r['hostname'] for r in selected}),http200=sum(r.get('http_status')==200 for r in results),table_rows=len(rows),download_observations=len(downloads),pagination_observations=len(pages),global_complete=False)
(O/'fetch_manifest.json').write_text(json.dumps(dict(summary=summary,results=results),indent=2)+'\n',encoding='utf-8');print(json.dumps(summary),flush=True)
