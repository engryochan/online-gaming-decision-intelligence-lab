from pathlib import Path
from collections import Counter,defaultdict
from lxml import html
import csv,json,zipfile,hashlib,sqlite3,zlib,io
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;D=O/'raw';T=R/'Reference/tables/26_historical_polities_b01_20261007'
csv.field_size_limit(32*1024*1024)
def dump(name,rows):
 rows=list(rows); assert rows; p=T/name;assert not p.exists()
 with p.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 return rows
def j(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
manifest=json.loads((O/'source_manifest.json').read_text())
for m in manifest:assert hashlib.sha256((D/m['file']).read_bytes()).hexdigest()==m['sha256']
db=O/'historical_polities_v1.sqlite';assert not db.exists();c=sqlite3.connect(db)
c.executescript('CREATE TABLE historical_features(feature_id TEXT PRIMARY KEY,name TEXT,source_type TEXT,from_year INTEGER,to_year INTEGER,properties_json TEXT,raw_feature_zlib BLOB,raw_feature_sha256 TEXT); CREATE INDEX historical_years ON historical_features(from_year,to_year); CREATE INDEX historical_names ON historical_features(name); CREATE TABLE source_records(source TEXT,source_row INTEGER,fields_json TEXT,PRIMARY KEY(source,source_row)); CREATE TABLE current_country_checks(iso_alpha2 TEXT PRIMARY KEY,fields_json TEXT); CREATE TABLE financial_workstreams(task_id TEXT PRIMARY KEY,iso_alpha2 TEXT,stream TEXT,fields_json TEXT);')
z=zipfile.ZipFile(D/'cliopatria.geojson.zip');names=[n for n in z.namelist() if n.endswith('.geojson')];assert len(names)==1
data=json.loads(z.read(names[0]));features=data['features']; intervals=[];groups=defaultdict(list);types=Counter();mapdata=[]
def simplify(points,tol=.15):
 if len(points)<5:return [[round(v,4) for v in q[:2]] for q in points]
 keep={0,len(points)-1};stack=[(0,len(points)-1)]
 while stack:
  a,b=stack.pop();x,y=points[a][:2];dx=points[b][0]-x;dy=points[b][1]-y;den=dx*dx+dy*dy;best=-1;idx=None
  for k in range(a+1,b):
   u,v=points[k][0]-x,points[k][1]-y;t=max(0,min(1,(u*dx+v*dy)/den)) if den else 0;dist=(u-t*dx)**2+(v-t*dy)**2
   if dist>best:best,idx=dist,k
  if best>tol*tol and idx is not None:keep.add(idx);stack.extend([(a,idx),(idx,b)])
 out=[[round(v,4) for v in points[k][:2]] for k in sorted(keep)]
 return out if len(out)>=4 else [[round(v,4) for v in q[:2]] for q in points]
for i,f in enumerate(features,1):
 p=f['properties'];g=f['geometry'];fid=f'CLIO:{i:06d}';raw=j(f).encode();sha=hashlib.sha256(raw).hexdigest()
 assert isinstance(p['FromYear'],int) and isinstance(p['ToYear'],int) and p['FromYear']<=p['ToYear']
 assert g['type'] in ['Polygon','MultiPolygon'];types[p['Type']]+=1
 c.execute('INSERT INTO historical_features VALUES(?,?,?,?,?,?,?,?)',(fid,p['Name'],p['Type'],p['FromYear'],p['ToYear'],j(p),zlib.compress(raw),sha))
 row=dict(feature_id=fid,source_name=p['Name'],source_type=p['Type'],from_year_source=p['FromYear'],to_year_source=p['ToYear'],source_area_km2=p['Area'],geometry_type=g['type'],raw_feature_sha256=sha,evidence_status='SOURCE_RECORD_RECEIVED_SUBSTANTIVE_REVIEW_PENDING',border_status='SOURCE_RECONSTRUCTION_UNCERTAINTY_NOT_QUANTIFIED',source_properties_json=j(p))
 intervals.append(row);groups[(p['Name'],p['Type'])].append(row)
 polygons=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
 mapdata.append([fid,p['Name'],p['Type'],p['FromYear'],p['ToYear'],[[simplify(ring) for ring in poly] for poly in polygons]])
 if i%1000==0:print('Features',i,flush=True)
dump('registry_historical_polity_intervals.csv',intervals)
entities=[]
for (name,typ),rs in sorted(groups.items()):
 entities.append(dict(source_group_id='CLIO_GROUP:'+hashlib.sha256(j([name,typ]).encode()).hexdigest()[:20],source_name=name,source_type=typ,first_source_year=min(r['from_year_source'] for r in rs),last_source_year=max(r['to_year_source'] for r in rs),interval_records=len(rs),source_identity_rule='EXACT_NAME_AND_TYPE_GROUP_NOT_UNIQUE_LEGAL_OR_HISTORICAL_STATE',lifespan_status='MIN_MAX_SOURCE_COVERAGE_NOT_CONTINUOUS_EXISTENCE',iso_relationship='UNRESOLVED_NO_AUTOMATIC_NAME_MERGE',all_brokers='HISTORICAL_APPLICABILITY_AND_COMPLETENESS_UNKNOWN',all_listed_companies='HISTORICAL_APPLICABILITY_AND_COMPLETENESS_UNKNOWN',all_currencies='UNKNOWN'))
dump('registry_historical_entity_source_groups.csv',entities)
cow={}
for p in sorted(D.glob('*Datasets.zip')):
 z=zipfile.ZipFile(p);ns=[n for n in z.namelist() if n.endswith('.csv') and not n.startswith('__MACOSX')];assert len(ns)==1
 b=z.read(ns[0]);rs=list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'))));name=Path(ns[0]).stem;cow[name]=rs
 (T/('cow_'+name+'.csv')).write_bytes(b)
 for i,r in enumerate(rs,1):c.execute('INSERT INTO source_records VALUES(?,?,?)',('COW:'+name,i,j(r)))
statekeys={r['ccode'] for r in cow['statelist2024']};assert all(r['ccode'] in statekeys for r in cow['system2024']+cow['majors2024'])
tree=html.fromstring((D/'un_m49_overview.html').read_bytes());table=tree.xpath('//table[@id="downloadTableEN"]');assert len(table)==1
trs=table[0].xpath('.//tr');headers=[' '.join(x.itertext()).strip() for x in trs[0].xpath('./th|./td')];un=[]
for tr in trs[1:]:
 vals=[' '.join(x.itertext()).strip() for x in tr.xpath('./td')];assert len(vals)==len(headers);un.append(dict(zip(headers,vals)))
assert len({r['ISO-alpha2 Code'] for r in un})==len(un);dump('registry_un_m49_live_source.csv',un)
motherpath=R/'Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv'
with motherpath.open(encoding='utf-8-sig') as f:mother=list(csv.DictReader(f))
md={r['iso_alpha2']:r for r in mother};ud={r['ISO-alpha2 Code']:r for r in un};checks=[]
for code in sorted(md.keys()|ud.keys()):
 r=dict(iso_alpha2=code,project_mother_present=code in md,live_UN_M49_present=code in ud,mother_name=md.get(code,{}).get('name_en',''),UN_name=ud.get(code,{}).get('Country or Area',''),status='BOTH_SOURCES_PRESENT_NAME_OR_LEGAL_STATUS_NOT_ADJUDICATED' if code in md and code in ud else 'SOURCE_SCOPE_DIFFERENCE_REQUIRES_REVIEW',mother_fields_json=j(md.get(code,{})),UN_fields_json=j(ud.get(code,{})))
 checks.append(r);c.execute('INSERT INTO current_country_checks VALUES(?,?)',(code,j(r)))
dump('registry_current_country_live_comparison.csv',checks)
financepath=R/'reports/2026-10-07/financial_universe_b07/financial_universe_v4.sqlite';fin=sqlite3.connect(financepath)
tasks=fin.execute('SELECT task_id,iso_alpha2,stream,fields_json FROM country_workstreams').fetchall();assert len(tasks)==747
c.executemany('INSERT INTO financial_workstreams VALUES(?,?,?,?)',tasks)
financialcounts={t:fin.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ['listing_records','esma_entities','currency_entries']};fin.close()
dependencies=[dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [motherpath,financepath]]
(O/'dependency_manifest.json').write_text(json.dumps(dependencies,indent=2)+'\n')
gaprows=[dict(scope='BEFORE_3400_BCE',status='UNKNOWN',reason='Requested tens-of-thousands-of-years scope needs archaeological regional evidence; cultures, settlements and polities cannot be mechanically equated.'),dict(scope='3400_BCE_TO_2024_CE',status='PARTIAL_SOURCE_COVERAGE',reason='Cliopatria and COW are selected definitions and reconstructions; unlisted entities and alternate borders remain possible.'),dict(scope='2025_TO_2026_10_07',status='CURRENT_CHANGES_PENDING',reason='Historical sources stop at 2024; present financial register and UN snapshot do not verify every polity or current border.'),dict(scope='CURRENT_FINANCIAL_UNIVERSE',status='OPEN_ALL_COUNTRIES',reason='747 inherited tasks preserved; historical state counts do not close broker/listing/currency gaps.')]
dump('registry_historical_scope_gaps.csv',gaprows)
c.commit();assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for fid,blob,sha in c.execute('SELECT feature_id,raw_feature_zlib,raw_feature_sha256 FROM historical_features'):
 raw=zlib.decompress(blob);assert hashlib.sha256(raw).hexdigest()==sha;assert json.loads(raw)==features[int(fid.split(':')[1])-1]
c.close()
summary=dict(features=len(features),source_named_entities=len({f['properties']['Name'] for f in features}),name_type_groups=len(entities),source_types=dict(types),from_year=min(f['properties']['FromYear'] for f in features),to_year=max(f['properties']['ToYear'] for f in features),cow_rows={k:len(v) for k,v in cow.items()},cow_state_codes=len(statekeys),project_mother_rows=len(mother),live_UN_M49_rows=len(un),union_codes=len(checks),mother_only=sorted(md.keys()-ud.keys()),UN_only=sorted(ud.keys()-md.keys()),financial_tasks_retained=len(tasks),financial_counts=financialcounts,all_feature_roundtrips=True,all_source_hashes_match=True,database_integrity='ok',global_historical_complete=False,all_financial_complete=False)
(O/'validation.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
(O/'map_payload.json').write_text(j(mapdata),encoding='utf-8')
print(json.dumps(summary),flush=True)
