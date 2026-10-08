from pathlib import Path
import csv,json,hashlib,sqlite3
csv.field_size_limit(2147483647)
O=Path(__file__).resolve().parent;R=O.parents[2]
T=R/'Reference/tables/51_global_registry_semantic_b26_20261008'
B=R/'Reference/tables/50_global_directory_content_b25_20261008'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
original=read(B/'registry_structured_directory_records.csv')
corrected=read(T/'registry_projection_scope_corrections.csv')
assert len(original)==len(corrected)==575
for index,(old,new) in enumerate(zip(original,corrected),1):
    assert int(new['b25_projection_id'])==index
    assert (old['source_url'],old['table'],old['row'])==(new['source_url'],new['source_table'],new['source_row'])
events=read(T/'registry_nsx_status_events.csv')
assert sum(x['status']=='SUSPENDED' for x in events)==7
assert sum(x['status']=='DELISTED' for x in events)==408
con=sqlite3.connect(T/'global_registry_semantic_b26.sqlite')
for p in T.glob('*.csv'):
    assert len(read(p))==con.execute('SELECT COUNT(*) FROM "'+p.stem+'"').fetchone()[0]
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';con.close()
for p,h in json.loads((O/'baseline.json').read_text())['protected'].items():
    assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
print('575 lineage references, 7 suspended, 408 delisted, CSV/SQL and protected hashes passed')
