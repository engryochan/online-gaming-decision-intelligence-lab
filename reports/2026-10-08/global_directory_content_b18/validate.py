from pathlib import Path
import csv,json,sqlite3,hashlib
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/43_global_directory_content_b18_20261008'
a=json.loads((O/'delivery_acceptance.json').read_text());con=sqlite3.connect(T/'global_directory_content_b18.sqlite')
for name,n in a['sqlite_counts'].items():
    assert con.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0]==n
    assert len(list(csv.DictReader((T/(name+'.csv')).open(encoding='utf-8-sig'))))==n
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
assert {r['target_url'] for r in read(T/'registry_all_4849_work_progress.csv')}=={r['target_url'] for r in read(R/'Reference/tables/30_global_directory_content_b05_20261008/registry_all_workqueue_priority_review.csv')}
assert {r['iso_alpha2'] for r in read(T/'registry_all_country_cumulative_source_progress.csv')}=={r['iso_alpha2'] for r in read(R/'Reference/tables/28_global_market_sources_b03_20261008/registry_all_country_source_coverage.csv')}
for p,h in json.loads((O/'baseline.json').read_text())['protected'].items():
    assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
(O/'validation_receipt.json').write_text(json.dumps({'sqlite_integrity':'ok','csv_sql_counts_verified':len(a['sqlite_counts']),'all_original_urls_preserved':4849,'country_codes_preserved':249,'protected_hashes_unchanged':True},indent=2)+'\n',encoding='utf-8')
print('Validation passed')
