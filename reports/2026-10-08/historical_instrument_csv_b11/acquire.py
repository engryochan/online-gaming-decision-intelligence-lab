from pathlib import Path
import csv,json,hashlib,gzip,io,sqlite3,urllib.request,urllib.error,re,subprocess,time,collections
from concurrent.futures import ThreadPoolExecutor,wait,FIRST_COMPLETED
O=Path(__file__).resolve().parent;R=O.parents[2];P=R/'Reference/tables/35_global_directory_content_b10_20261008';T=R/'Reference/tables/36_historical_instrument_csv_b11_20261008';T.mkdir(parents=True,exist_ok=True);D=O/'raw_gzip';D.mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
queue=read(P/'registry_all_download_workqueue.csv');pending=[r for r in queue if r['action']=='PENDING_FULL_HISTORICAL_FILE_ACQUISITION'];assert len(pending)==1848
baseline=O/'baseline.json'
if not baseline.exists():
    protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in ['Reference/Aerospace_Ecosystem_Report.qmd','Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']}
    baseline.write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected),indent=2)+'\n',encoding='utf-8')
db=T/'historical_instrument_csv_b11.sqlite';con=sqlite3.connect(db)
con.execute('CREATE TABLE IF NOT EXISTS file_manifest(url TEXT PRIMARY KEY,receipt_json TEXT)')
con.execute('CREATE TABLE IF NOT EXISTS csv_blocks(content_sha256 TEXT,first_row INTEGER,row_count INTEGER,payload_gzip BLOB,payload_sha256 TEXT,PRIMARY KEY(content_sha256,first_row))')
con.commit()
done={u for (u,) in con.execute('SELECT url FROM file_manifest')};todo=[r for r in pending if r['target_url'] not in done]
source=(R/'reports/2026-10-07/git_publish_and_html_recovery/audit.py').read_text(encoding='utf-8');namespace={'re':re};exec(source[source.index('patterns='):source.index('for name in paths:')],namespace)
def credentials(data):
    hits=set()
    for kind,pattern in namespace['patterns']:
        for match in pattern.finditer(data):
            value=match[1] if kind=='CREDENTIAL_LITERAL' else match[0];s=value.decode('utf-8','ignore').lower().strip()
            if kind=='CREDENTIAL_LITERAL' and (s in namespace['placeholders'] or s.startswith(('your_','your-','${','{{','<','process.env','os.environ')) or len(s)>256):continue
            hits.add(kind)
    return sorted(hits)
def fetch(r):
    url=r['target_url'];receipt=dict(url=url,checked_on='2026-10-08',source_observations_json=r['source_observations_json']);data=b'';started=time.monotonic()
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchDirectoryArchive/1.0'}),timeout=20) as response:
            data=response.read(20000001);receipt.update(http_status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type',''),truncated=len(data)>20000000)
    except urllib.error.HTTPError as e:data=e.read(65536);receipt.update(http_status=e.code,error='HTTPError',truncated=True)
    except Exception as e:receipt.update(http_status='',error=type(e).__name__)
    receipt['elapsed_seconds']=round(time.monotonic()-started,3)
    if data:
        receipt.update(bytes=len(data),content_sha256=hashlib.sha256(data).hexdigest(),credential_candidates=credentials(data))
        packed=gzip.compress(data,compresslevel=6,mtime=0);path=D/(hashlib.sha256(url.encode()).hexdigest()[:20]+'.response.gz');path.write_bytes(packed)
        receipt.update(file=path.relative_to(R).as_posix(),gzip_bytes=len(packed),gzip_sha256=hashlib.sha256(packed).hexdigest(),publication='LOCAL_ONLY_CREDENTIAL_CANDIDATE' if receipt['credential_candidates'] else 'ELIGIBLE_AFTER_SCAN')
    return receipt,data
finished=len(done);started=time.monotonic()
with (O/'progress.jsonl').open('a',encoding='utf-8') as log:
    with ThreadPoolExecutor(max_workers=4) as pool:
        iterator=iter(todo);active={}
        for r in list(next(iterator,None) for _ in range(4)):
            if r is not None:active[pool.submit(fetch,r)]=r
        while active:
            ready,_=wait(active,return_when=FIRST_COMPLETED)
            for future in ready:
                active.pop(future);receipt,data=future.result();row_count=0;blocks=0
                if receipt.get('http_status')==200 and not receipt.get('truncated') and not receipt.get('credential_candidates'):
                    try:
                        try:text=data.decode('utf-8-sig');encoding='UTF8'
                        except UnicodeDecodeError:text=data.decode('latin1');encoding='LATIN1_REVERSIBLE_SOURCE_ENCODING_UNCONFIRMED'
                        try:delimiter=csv.Sniffer().sniff(text[:8192],delimiters=',;\t|').delimiter
                        except csv.Error:delimiter=','
                        receipt.update(encoding=encoding,delimiter=delimiter,physical_text_lines=len(text.splitlines()));block=[];first=1;widths=collections.Counter();header=[]
                        for cells in csv.reader(io.StringIO(text,newline=''),delimiter=delimiter):
                            row_count+=1;widths[len(cells)]+=1
                            if row_count==1:header=cells
                            block.append(cells)
                            if len(block)==1000:
                                payload=json.dumps(block,ensure_ascii=False,separators=(',',':')).encode();con.execute('INSERT OR REPLACE INTO csv_blocks VALUES (?,?,?,?,?)',(receipt['content_sha256'],first,len(block),gzip.compress(payload,mtime=0),hashlib.sha256(payload).hexdigest()));blocks+=1;first=row_count+1;block=[]
                        if block:
                            payload=json.dumps(block,ensure_ascii=False,separators=(',',':')).encode();con.execute('INSERT OR REPLACE INTO csv_blocks VALUES (?,?,?,?,?)',(receipt['content_sha256'],first,len(block),gzip.compress(payload,mtime=0),hashlib.sha256(payload).hexdigest()));blocks+=1
                        receipt.update(logical_csv_rows=row_count,header_json=json.dumps(header,ensure_ascii=False),column_width_counts_json=json.dumps(widths),header_sha256=hashlib.sha256(json.dumps(header,ensure_ascii=False).encode()).hexdigest(),blocks=blocks,parse_status='ALL_CSV_RECORDS_IN_OBSERVED_BODY_PARSED_SCOPE_UNKNOWN')
                    except Exception as e:receipt.update(parse_status='PARSE_ERROR_PARTIAL_BLOCKS_REVIEW',parse_error=type(e).__name__)
                else:receipt['parse_status']='FETCH_TRUNCATION_CREDENTIAL_OR_STATUS_REVIEW'
                con.execute('INSERT OR REPLACE INTO file_manifest VALUES (?,?)',(receipt['url'],json.dumps(receipt,ensure_ascii=False)));con.commit();log.write(json.dumps(receipt,ensure_ascii=False)+'\n');log.flush();finished+=1
                if finished%25==0:print(json.dumps(dict(completed=finished,total=len(pending),minutes=round((time.monotonic()-started)/60,1))),flush=True)
                r=next(iterator,None)
                if r is not None:active[pool.submit(fetch,r)]=r
receipts=[json.loads(s) for (s,) in con.execute('SELECT receipt_json FROM file_manifest ORDER BY url')]
def write(n,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([{k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in rows])
write('registry_file_fetch_manifest.csv',receipts)
write('registry_csv_block_index.csv',[dict(content_sha256=sha,first_row=first,row_count=n,compressed_bytes=size,payload_sha256=digest) for sha,first,n,size,digest in con.execute('SELECT content_sha256,first_row,row_count,length(payload_gzip),payload_sha256 FROM csv_blocks ORDER BY content_sha256,first_row')])
summary=dict(selected_all_pending=len(pending),attempted=len(receipts),http200=sum(r.get('http_status')==200 for r in receipts),saved_bodies=sum(bool(r.get('file')) for r in receipts),parsed_files=sum(r.get('parse_status')=='ALL_CSV_RECORDS_IN_OBSERVED_BODY_PARSED_SCOPE_UNKNOWN' for r in receipts),logical_csv_rows=sum(r.get('logical_csv_rows',0) for r in receipts),raw_bytes=sum(r.get('bytes',0) for r in receipts),raw_gzip_bytes=sum(r.get('gzip_bytes',0) for r in receipts),credential_candidate_files=sum(bool(r.get('credential_candidates')) for r in receipts),global_complete=False)
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close();(O/'acquisition_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps(summary),flush=True)
