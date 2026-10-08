from pathlib import Path
import csv,json,hashlib,zipfile,io,sys,collections
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/42_global_directory_followup_b17_20261008'
sys.path.insert(0,str(O.parent/'global_directory_content_b05'));import intake
intake.O=O;intake.T=T
rows=[];receipts=[];texts=[]
for r in csv.DictReader((T/'direct_file_fetch_manifest.csv').open(encoding='utf-8-sig')):
    if not r.get('file') or not r['url'].split('?')[0].lower().endswith('.zip') or r.get('truncated')=='True':continue
    p=R/r['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        for info in z.infolist():
            if info.is_dir():continue
            data=z.read(info);digest=hashlib.sha256(data).hexdigest()
            try:text=data.decode('utf-8-sig');encoding='UTF8'
            except UnicodeDecodeError:text=data.decode('latin1');encoding='LATIN1_REVERSIBLE_ENCODING_UNCONFIRMED'
            if info.filename.lower().endswith('.csv'):
                try:sep=csv.Sniffer().sniff(text[:8192],delimiters=',;\t|').delimiter
                except csv.Error:sep=';' if text[:8192].count(';')>text[:8192].count(',') else ','
                n=0
                for n,cells in enumerate(csv.reader(io.StringIO(text,newline=''),delimiter=sep),1):
                    rows.append(dict(url=r['url'],member=info.filename,member_sha256=digest,row=n,encoding=encoding,delimiter=sep,cells_json=json.dumps(cells,ensure_ascii=False),role='REGULATORY_SOURCE_ROW_INCLUDING_HEADER_NOT_ENTITY_COUNT'))
                receipts.append(dict(url=r['url'],member=info.filename,bytes=len(data),sha256=digest,encoding=encoding,delimiter=sep,logical_rows=n,status='FULL_MEMBER_CSV_PARSED'))
            elif info.filename.lower().endswith(('.txt','.md','.json','.xml','.html','.htm')):
                texts.append(dict(url=r['url'],member=info.filename,sha256=digest,encoding=encoding,text=text,role='SOURCE_DICTIONARY_OR_TEXT_SEMANTICS_PENDING'))
intake.write('registry_archive_csv_rows.csv',rows);intake.write('registry_archive_csv_parse_receipts.csv',receipts);intake.write('registry_archive_text_members.csv',texts)
counts=collections.Counter((r['url'],r['member']) for r in rows)
assert all(counts[(r['url'],r['member'])]==r['logical_rows'] for r in receipts)
(O/'archive_acceptance.json').write_text(json.dumps(dict(csv_members=len(receipts),logical_csv_rows=len(rows),text_members=len(texts),row_counts_verified=True,includes_headers_and_empty_rows=True),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(csv_members=len(receipts),logical_csv_rows=len(rows),text_members=len(texts))))
