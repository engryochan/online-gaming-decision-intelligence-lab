from pathlib import Path
import sys,csv,json,urllib.request,hashlib
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/32_global_directory_content_b07_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.T=T
path=T/'direct_file_fetch_manifest.csv';rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))
(O/'download_initial_receipts.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
def retry(row):
    original=row['url'];out=dict(row,acquisition='PERCENT_ENCODED_UNICODE_URL_RETRY',requested_url=quote(original,safe=':/?=&%#'))
    try:
        with urllib.request.urlopen(urllib.request.Request(out['requested_url'],headers={'User-Agent':'ResearchDirectory/1.0'}),timeout=30) as response:
            data=response.read(20000001);out.update(http_status=response.status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),truncated=len(data)>20000000,error='')
        target=O/'downloads'/(hashlib.sha256(original.encode()).hexdigest()[:20]+'.response');target.write_bytes(data);out['file']=target.relative_to(R).as_posix()
    except Exception as e:out['error']=type(e).__name__
    return out
failed=[r for r in rows if r.get('error')=='UnicodeEncodeError']
with ThreadPoolExecutor(max_workers=5) as pool:fixed={r['url']:r for r in pool.map(retry,failed)}
rows=[fixed.get(r['url'],r) for r in rows];intake.write('direct_file_fetch_manifest.csv',rows)
summary=json.loads((O/'download_acceptance.json').read_text());summary.update(saved=sum(bool(r.get('file')) for r in rows),unicode_retries=len(failed),remaining_errors=sum(bool(r.get('error')) for r in rows))
(O/'download_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))
