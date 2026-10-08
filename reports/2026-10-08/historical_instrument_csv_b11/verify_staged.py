from pathlib import Path
import subprocess,json,hashlib,csv,gzip
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/36_historical_instrument_csv_b11_20261008'
paths=[p.decode('utf-8') for p in subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=R).split(b'\0') if p]
prefixes=['Reference/Global_Historical_Instrument_CSV_B11_20261008.','Reference/tables/36_historical_instrument_csv_b11_20261008/','reports/2026-10-08/historical_instrument_csv_b11/']
assert all(p=='.gitignore' or any(p.startswith(prefix) for prefix in prefixes) for p in paths)
db='Reference/tables/36_historical_instrument_csv_b11_20261008/historical_instrument_csv_b11.sqlite'
assert hashlib.sha256(subprocess.check_output(['git','show',':'+db],cwd=R)).digest()==hashlib.sha256((R/db).read_bytes()).digest()
receipts=list(csv.DictReader((T/'registry_file_fetch_manifest.csv').open(encoding='utf-8-sig')));compressed=[r for r in receipts if r.get('file') and r.get('publication')!='LOCAL_ONLY_CREDENTIAL_CANDIDATE'];objects=[]
for r in compressed:
    objects.append(':'+r['file'])
# One cat-file session verifies every staged compressed source without per-file Git launches.
process=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for r,oid in zip(compressed,objects):
    process.stdin.write((oid+'\n').encode());process.stdin.flush();header=process.stdout.readline().decode().strip().split();assert len(header)==3 and header[1]=='blob',header;size=int(header[2]);data=process.stdout.read(size);assert process.stdout.read(1)==b'\n'
    assert hashlib.sha256(data).hexdigest()==r['gzip_sha256'];assert hashlib.sha256(gzip.decompress(data)).hexdigest()==r['content_sha256']
process.stdin.close();assert process.wait()==0
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for p,digest in baseline['protected'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest()
    if 'Inteligent' not in p:assert current==digest
    assert p not in paths;protected.append(dict(path=p,baseline_sha256=digest,current_sha256=current,batch_action='PRESERVED_NOT_STAGED'))
(O/'staged_acceptance.json').write_text(json.dumps(dict(staged_files=len(paths),staged_gzip_sources_verified=len(compressed),database_bytes_verified=True,protected_files=protected),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(staged_files=len(paths),staged_gzip_sources_verified=len(compressed),user_changes_not_staged=True)))
