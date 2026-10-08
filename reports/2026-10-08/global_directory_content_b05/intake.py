from pathlib import Path
import csv,json,re,time,hashlib,urllib.request,urllib.error,threading
from urllib.parse import urlparse,urljoin
from concurrent.futures import ThreadPoolExecutor,as_completed
from lxml import html

O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/30_global_directory_content_b05_20261008';T.mkdir(parents=True,exist_ok=True)
D=O/'raw';D.mkdir(exist_ok=True)
INPUT=R/'Reference/tables/29_global_market_directories_b04_20261008/registry_all_directory_collection_workqueue.csv'
if __name__=='__main__':
    assert not (O/'intake_progress.jsonl').exists(), 'Use a new batch or preview directory; preserve existing output.'
queue=list(csv.DictReader(INPUT.open(encoding='utf-8-sig')))
priority=re.compile(r'listed[-_/ ]?(companies|company|issuers)|listing[-_/ ]?directory|company[-_/ ]?list|member[-_/ ]?(list|directory)|members[-_/ ]?list|list[-_/ ]?of[-_/ ]?(members|brokers|companies)|broker[-_/ ]?(list|directory)|licensed[-_/ ]?(firms|entities|institutions)|market[-_/ ]?participants',re.I)
excluded=re.compile(r'/(privacy|contact|terms|login|sign.?in|sign.?up)([/#?]|$)',re.I)
classified=[];selected=[]
for number,row in enumerate(queue,1):
    text=row['target_url']+' '+row['source_observations_json']
    matched=sorted(set(m.group().lower() for m in priority.finditer(text)))
    category='P1_NAMED_DIRECTORY_SIGNAL' if matched else 'P2_OTHER_CANDIDATE_REVIEW'
    if excluded.search(row['target_url']):category='P3_ACCESS_OR_ADMIN_PAGE_REVIEW'
    item=dict(work_id=f'B05:{number}',**row,priority=category,selection_evidence='|'.join(matched))
    classified.append(item)
    if category=='P1_NAMED_DIRECTORY_SIGNAL':selected.append(item)
for label,url in [('PSX_OFFICIAL_COMPANY_DATA','https://www.psx.com.pk/psx/resources-and-tools/listings/listed-companies-data'),
                  ('PSX_OFFICIAL_SCREENER','https://dps.psx.com.pk/screener/'),
                  ('LSE_OFFICIAL_REPORTS','https://www.londonstockexchange.com/reports?tab=issuers')]:
    if not any(r['target_url']==url for r in selected):
        selected.append(dict(work_id=label,target_url=url,priority='SUPPLEMENTAL_PRIMARY_SOURCE',selection_evidence='Official source lookup 2026-10-08; not claimed part of the original 4849'))
def write(name,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
if __name__=='__main__':
    write('registry_all_workqueue_priority_review.csv',classified)
    write('registry_selected_directory_sources.csv',selected)
locks={urlparse(r['target_url']).hostname:threading.Semaphore(2) for r in selected}
def get(item):
    url=item['target_url'];result=dict(work_id=item['work_id'],url=url,checked_on='2026-10-08',selection_evidence=item['selection_evidence'])
    started=time.monotonic();data=b''
    try:
        with locks[urlparse(url).hostname]:
            req=urllib.request.Request(url,headers={'User-Agent':'ResearchDirectoryContent/1.0'})
            with urllib.request.urlopen(req,timeout=10) as response:
                chunks=[];size=0;limited=False
                while size<3000001:
                    chunk=response.read1(min(65536,3000001-size))
                    if not chunk:break
                    chunks.append(chunk);size+=len(chunk)
                    if time.monotonic()-started>30:limited=True;break
                data=b''.join(chunks)
                result.update(http_status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type',''),
                              bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),truncated=limited or size>3000000,
                              elapsed_seconds=round(time.monotonic()-started,2))
    except urllib.error.HTTPError as e:
        data=e.read(65536);result.update(http_status=e.code,final_url=e.url,error='HTTP_ERROR',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:result.update(http_status='',error=type(e).__name__)
    if data:
        name=hashlib.sha256(url.encode()).hexdigest()[:20]+'.response'
        path=D/name;path.write_bytes(data);result['file']=path.relative_to(R).as_posix()
    rows=[];downloads=[];pages=[]
    if result.get('http_status')==200 and data and ('html' in result.get('content_type','').lower() or data.lstrip().startswith((b'<html',b'<!DOCTYPE',b'<!doctype'))):
        try:
            tree=html.fromstring(data);result['title']=' '.join(tree.xpath('//title/text()'))
            for table_index,table in enumerate(tree.xpath('//table'),1):
                headers=[' '.join(n.text_content().split()) for n in table.xpath('.//thead//th')]
                for row_index,tr in enumerate(table.xpath('.//tr'),1):
                    cells=[' '.join(n.text_content().split()) for n in tr.xpath('./td|./th')]
                    if not cells:continue
                    rows.append(dict(work_id=item['work_id'],source_url=url,table=table_index,row=row_index,headers_json=json.dumps(headers,ensure_ascii=False),
                                     cells_json=json.dumps(cells,ensure_ascii=False),row_links_json=json.dumps([urljoin(result['final_url'],u) for u in tr.xpath('.//a/@href')],ensure_ascii=False),
                                     content_sha256=result['sha256'],semantic_status='SOURCE_TABLE_ROW_NOT_AUTOMATICALLY_ENTITY'))
            for a in tree.xpath('//a[@href]'):
                target=urljoin(result['final_url'],a.get('href'));label=' '.join(a.text_content().split());p=urlparse(target)
                if p.scheme not in ('http','https') or p.username or p.password:continue
                if re.search(r'[.](csv|xlsx?|zip)([?]|$)',target,re.I):
                    downloads.append(dict(work_id=item['work_id'],source_url=url,target_url=target,label=label,evidence='OBSERVED_DIRECT_FILE_LINK'))
            pagination=tree.xpath('//*[contains(@class,"pagination") or contains(@class,"pager") or contains(@aria-label,"Pagination")]//a[@href]')
            for a in pagination:
                target=urljoin(result['final_url'],a.get('href'));p=urlparse(target)
                if p.scheme in ('http','https') and not p.username and not p.password:
                    pages.append(dict(work_id=item['work_id'],source_url=url,target_url=target,label=' '.join(a.text_content().split()),status='OBSERVED_PAGE_LINK_NOT_YET_FETCHED'))
            result['source_table_rows']=len(rows)
            result['directory_completeness']='UNKNOWN_PAGINATION_AND_DYNAMIC_CONTENT_REVIEW'
        except Exception as e:result['parse_error']=type(e).__name__
    return result,rows,downloads,pages
def main():
    results=[];rows=[];downloads=[];pages=[]
    print('all work rows',len(classified),'selected',len(selected),flush=True)
    with ThreadPoolExecutor(max_workers=12) as pool:
        with (O/'intake_progress.jsonl').open('w',encoding='utf-8') as stream:
            for future in as_completed([pool.submit(get,r) for r in selected]):
                result,r,d,p=future.result();results.append(result);rows.extend(r);downloads.extend(d);pages.extend(p)
                stream.write(json.dumps(dict(result=result,rows=r,downloads=d,pages=p),ensure_ascii=False)+'\n');stream.flush()
                if len(results)%20==0:print('fetched',len(results),'rows',len(rows),flush=True)
    write('directory_fetch_manifest.csv',results);write('registry_directory_all_table_rows.csv',rows)
    write('registry_directory_observed_download_links.csv',downloads);write('registry_directory_observed_pagination.csv',pages)
    summary=dict(input_work_rows=len(classified),selected_sources=len(selected),checked_sources=len(results),HTTP200=sum(r.get('http_status')==200 for r in results),
                 source_table_rows=len(rows),download_link_observations=len(downloads),pagination_observations=len(pages),global_complete=False)
    (O/'intake_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
