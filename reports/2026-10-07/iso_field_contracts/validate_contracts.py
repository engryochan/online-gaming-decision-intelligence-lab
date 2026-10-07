"""Independent preservation checks and SQL grouping of source subdivisions."""
from pathlib import Path
import csv,json,hashlib,sqlite3
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
for m in read(OUT/'source_manifest.csv'):assert hashlib.sha256((ROOT/m['path']).read_bytes()).hexdigest()==m['sha256']
a=read(ROOT/'reports/2026-10-07/reference_field_contracts/field_semantics_v4.csv');b=read(OUT/'field_semantics_v5.csv');assert len(a)==len(b)==1989
changes=0
for old,new in zip(a,b):
    if old==new:continue
    assert old['definition_status']=='UNRESOLVED' and old['role']=='REFERENCE_DATA'
    assert new['definition_status']=='PROPOSED_BASELINE_CONTEXT_REVIEW'
    assert {k for k in old if old[k]!=new[k]}=={'definition','definition_status','definition_locator'}
    changes+=1
assert changes==41
remaining=[r for r in b if r['definition_status']=='UNRESOLVED'];assert len(remaining)==334
assert remaining==read(OUT/'remaining_unresolved.csv')
admin=read(ROOT/'Reference/tables/02_admin_units/registry_admin_units_iso3166_2_20261004.csv')
country=read(ROOT/'Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv')
with sqlite3.connect(':memory:') as db:
    db.executescript('CREATE TABLE admin(code TEXT PRIMARY KEY,country TEXT,parent TEXT); CREATE TABLE country(code TEXT PRIMARY KEY,n INTEGER);')
    db.executemany('insert into admin values(?,?,?)',[(r['subdivision_code'],r['country_iso_alpha2'],r['parent_code']) for r in admin])
    db.executemany('insert into country values(?,?)',[(r['iso_alpha2'],int(r['iso3166_2_subdivision_count'])) for r in country])
    assert not db.execute("select a.code from admin a left join admin p on a.parent=p.code where a.parent<>'' and p.code is null").fetchall()
    assert not db.execute('select c.code from country c left join admin a on a.country=c.code group by c.code,c.n having count(a.code)<>c.n').fetchall()
result=dict(pass_check=True,definitions_added=changes,unchanged_semantic_records=1948,unresolved=334,sql_subdivision_counts='PASS',source_files_unchanged=5,owner_approval='PENDING',current_country_or_political_facts='NOT_REVERIFIED')
(OUT/'independent_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
