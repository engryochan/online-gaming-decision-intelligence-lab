from pathlib import Path
import json,csv,sqlite3,gzip,hashlib,collections
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/36_historical_instrument_csv_b11_20261008';P=R/'Reference/tables/35_global_directory_content_b10_20261008'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
con=sqlite3.connect(T/'historical_instrument_csv_b11.sqlite');receipts=[json.loads(s) for (s,) in con.execute('SELECT receipt_json FROM file_manifest ORDER BY url')]
queue=read(P/'registry_all_download_workqueue.csv');expected={r['target_url'] for r in queue if r['action']=='PENDING_FULL_HISTORICAL_FILE_ACQUISITION'};assert expected=={r['url'] for r in receipts}
block_checks={};valuecounts=collections.Counter();schemas=collections.Counter();gaps=[]
for sha in {r.get('content_sha256') for r in receipts if r.get('parse_status')=='ALL_CSV_RECORDS_IN_OBSERVED_BODY_PARSED_SCOPE_UNKNOWN'}:
    representative=next(r for r in receipts if r.get('content_sha256')==sha);header=json.loads(representative['header_json']);indices={name:header.index(name) for name in ['InstrumentType','CallPutCode','MarketFlowIndicator'] if name in header};expectedfirst=1;count=0;blocks=0
    for first,n,compressed,digest in con.execute('SELECT first_row,row_count,payload_gzip,payload_sha256 FROM csv_blocks WHERE content_sha256=? ORDER BY first_row',(sha,)):
        assert first==expectedfirst;payload=gzip.decompress(compressed);assert hashlib.sha256(payload).hexdigest()==digest;rows=json.loads(payload);assert len(rows)==n
        for offset,cells in enumerate(rows):
            if first+offset==1:continue
            for name,i in indices.items():
                if i<len(cells):valuecounts[(name,cells[i])]+=1
        count+=n;blocks+=1;expectedfirst+=n
    assert count==representative['logical_csv_rows'];block_checks[sha]=dict(logical_rows=count,blocks=blocks)
for r in receipts:
    if r.get('file'):
        packed=(R/r['file']).read_bytes();assert hashlib.sha256(packed).hexdigest()==r['gzip_sha256'];data=gzip.decompress(packed);assert len(data)==r['bytes'];assert hashlib.sha256(data).hexdigest()==r['content_sha256']
        if r.get('parse_status')=='ALL_CSV_RECORDS_IN_OBSERVED_BODY_PARSED_SCOPE_UNKNOWN':
            try:text=data.decode('utf-8-sig') if r['encoding']=='UTF8' else data.decode('latin1')
            except Exception:raise
            fresh=list(csv.reader(__import__('io').StringIO(text,newline=''),delimiter=r['delimiter']))
            assert len(fresh)==r['logical_csv_rows'];assert fresh[0]==json.loads(r['header_json']) if fresh else r['logical_csv_rows']==0
            reread=hashlib.sha256()
            for row in fresh:reread.update((json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n').encode())
            stored=hashlib.sha256()
            for (compressed,) in con.execute('SELECT payload_gzip FROM csv_blocks WHERE content_sha256=? ORDER BY first_row',(r['content_sha256'],)):
                for row in json.loads(gzip.decompress(compressed)):stored.update((json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n').encode())
            assert reread.digest()==stored.digest();r['row_sequence_sha256']=reread.hexdigest();schemas[r['header_sha256']]+=1
    if r.get('parse_status')!='ALL_CSV_RECORDS_IN_OBSERVED_BODY_PARSED_SCOPE_UNKNOWN':gaps.append(dict(url=r['url'],http_status=r.get('http_status',''),error=r.get('error',''),parse_status=r.get('parse_status',''),body_saved=bool(r.get('file'))))
def write(n,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
prior={r['url']:r for r in read(P/'direct_file_fetch_manifest.csv')};byurl={r['url']:r for r in receipts};ledger=[]
for r in queue:
    result=byurl.get(r['target_url']);old=prior.get(r['target_url'],{});status='PRIOR_B10_FETCH_REVIEW_SCOPE_PENDING' if old.get('file') else 'PRIOR_B10_DOWNLOAD_ERROR_REVIEW'
    if result:status='B11_ALL_OBSERVED_CSV_RECORDS_PARSED_SCOPE_PENDING' if result.get('parse_status')=='ALL_CSV_RECORDS_IN_OBSERVED_BODY_PARSED_SCOPE_UNKNOWN' else 'B11_FETCH_OR_PARSE_REVIEW'
    ledger.append(dict(**r,cumulative_status=status,new_receipt_json=json.dumps(result,ensure_ascii=False) if result else '',prior_receipt_json=json.dumps(old,ensure_ascii=False) if old else '',universe_completeness='UNKNOWN'))
write('registry_all_1897_download_progress.csv',ledger);write('registry_fetch_parse_gaps.csv',gaps)
write('registry_schema_fingerprints.csv',[dict(header_sha256=k,file_observations=n,header_json=next(r['header_json'] for r in receipts if r.get('header_sha256')==k),interpretation='SOURCE_FIELD_NAMES_ONLY_DICTIONARY_PENDING') for k,n in sorted(schemas.items())])
write('registry_source_code_observations.csv',[dict(field=k[0],source_code=k[1],unique_body_row_observations=n,code_meaning='UNKNOWN_PENDING_SOURCE_DICTIONARY') for k,n in sorted(valuecounts.items())])
for n in ['registry_all_1897_download_progress.csv','registry_fetch_parse_gaps.csv','registry_schema_fingerprints.csv','registry_source_code_observations.csv']:
    items=read(T/n)
    if not items:continue
    fields=list(items[0]);name=Path(n).stem;con.execute('CREATE TABLE "'+name+'" ('+','.join('"'+k+'" TEXT' for k in fields)+')');con.executemany('INSERT INTO "'+name+'" VALUES ('+','.join('?' for k in fields)+')',[[r[k] for k in fields] for r in items])
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for p,digest in baseline['protected'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest()
    if 'Inteligent' not in p:assert digest==current
    protected.append(dict(path=p,baseline_sha256=digest,current_sha256=current,batch_action='NO_WRITE'))
summary=dict(all_pending_urls_attempted=len(receipts),raw_gzip_roundtrip_receipts=sum(bool(r.get('file')) for r in receipts),parsed_files_reconciled=sum(r.get('parse_status')=='ALL_CSV_RECORDS_IN_OBSERVED_BODY_PARSED_SCOPE_UNKNOWN' for r in receipts),logical_csv_row_observations=sum(r.get('logical_csv_rows',0) for r in receipts),unique_body_logical_rows=sum(v['logical_rows'] for v in block_checks.values()),unique_parsed_body_hashes=len(block_checks),schema_variants=len(schemas),gaps=len(gaps),complete_1897_ledger=len(ledger),protected_files=protected,integrity='ok',global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in summary.items() if k!='protected_files'}))
