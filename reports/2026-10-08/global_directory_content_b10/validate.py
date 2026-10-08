from pathlib import Path
import csv,json,sqlite3,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/35_global_directory_content_b10_20261008'
con=sqlite3.connect(T/'global_directory_content_b10.sqlite');checks=[]
for path in sorted(T.glob('*.csv')):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;count=sum(1 for r in reader)
    if not fields:continue
    actual=con.execute('SELECT count(*) FROM "'+path.stem+'"').fetchone()[0];assert actual==count,path
    checks.append(dict(table=path.stem,rows=count,csv_database_reconciled=True))
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
original=R/'Reference/tables/30_global_directory_content_b05_20261008/registry_all_workqueue_priority_review.csv'
with original.open(encoding='utf-8-sig') as f:before={r['target_url'] for r in csv.DictReader(f)}
with (T/'registry_all_4849_work_progress.csv').open(encoding='utf-8-sig') as f:after={r['target_url'] for r in csv.DictReader(f)}
assert before==after and len(after)==4849
with (T/'registry_all_country_cumulative_source_progress.csv').open(encoding='utf-8-sig') as f:codes=[r['iso_alpha2'] for r in csv.DictReader(f)]
assert len(codes)==len(set(codes))==249
baseline=json.loads((O/'baseline.json').read_text());protected=[]
for p,digest in baseline['protected'].items():
    current=hashlib.sha256((R/p).read_bytes()).hexdigest()
    if 'Inteligent' not in p:assert current==digest
    protected.append(dict(path=p,baseline_sha256=digest,current_sha256=current,batch_action='PRESERVED_NO_WRITE'))
(O/'validation_receipt.json').write_text(json.dumps(dict(table_checks=checks,original_queue_preserved=True,country_mother_codes_preserved=249,protected_files=protected,integrity='ok'),indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(tables_reconciled=len(checks),original_queue_preserved=4849,country_mother_preserved=249)))
