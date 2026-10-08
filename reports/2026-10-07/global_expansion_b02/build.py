from pathlib import Path
from collections import Counter,defaultdict
from lxml import html
import csv,json,sqlite3,hashlib,re,zlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;D=O/'raw';T=R/'Reference/tables/27_global_expansion_b02_20261007';T.mkdir(parents=True,exist_ok=True);csv.field_size_limit(32*1024*1024)
def j(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def dump(name,rows,fields=None):
 rows=list(rows);p=T/name;assert not p.exists()
 with p.open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
 return rows
def text(e):return ' '.join(' '.join(e.itertext()).split())
for m in json.loads((O/'source_manifest.json').read_text()):assert hashlib.sha256((D/m['file']).read_bytes()).hexdigest()==m['sha256']
prior=R/'reports/2026-10-07/financial_universe_b07/financial_universe_v4.sqlite';hist=R/'reports/2026-10-07/historical_polities_b01/historical_polities_v1.sqlite';db=O/'global_universe_v5.sqlite';assert not db.exists();c=sqlite3.connect(db);old=sqlite3.connect(prior);old.backup(c);old.close();c.execute('ATTACH DATABASE ? AS prior',(str(prior),));c.execute('ATTACH DATABASE ? AS hist',(str(hist),))
c.executescript('CREATE TABLE historical_feature_snapshots AS SELECT * FROM hist.historical_features; CREATE UNIQUE INDEX hist_feature_id ON historical_feature_snapshots(feature_id); CREATE INDEX hist_feature_years ON historical_feature_snapshots(from_year,to_year); CREATE TABLE historical_cow_records AS SELECT * FROM hist.source_records; CREATE TABLE country_workstreams_prior_b07 AS SELECT * FROM country_workstreams;')
with (D/'euronext_full_download.response').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f,delimiter=';'))
metadata=[r for r in rows if r.get('ISIN') is None];data=[r for r in rows if r.get('ISIN') is not None];overview=json.loads((D/'euronext_directory.response').read_text());assert len(data)==overview['iTotalRecords']==overview['iTotalDisplayRecords'] and len(metadata)==3
assert all(None not in r for r in data)
dump('registry_euronext_download_all_rows.csv',[dict(source_row=i,row_class='SOURCE_METADATA' if r.get('ISIN') is None else 'SECURITY_RECORD',raw_fields_json=j(r)) for i,r in enumerate(rows,1)])
mic={r[0]:dict(country=r[1],raw=json.loads(r[2])) for r in c.execute('SELECT MIC,country_iso_raw,fields_json FROM mic_registry')}
base={'Amsterdam':'XAMS','Brussels':'XBRU','Dublin':'XMSM','Lisbon':'XLIS','Milan':'MTAA','Paris':'XPAR'}
aliases={'Oslo Børs':['XOSL'],'EuroTLX':['ETLX'],'Euronext Global Equity Market':['BGEM'],'Trading After Hours':['MTAH'],'Euronext Growth Milan':['EXGM'],'Euronext Expand Oslo':['XOAS'],'Euronext Growth Oslo':['MERK'],'Euronext Paris - Multi-currency Trading':['XPAR'],'Euronext Access Paris':['XMLI'],'Euronext Access Brussels':['MLXB'],'Euronext Access Lisbon':['ENXL'],'Euronext Growth Paris':['ALXP'],'Euronext Growth Brussels':['ALXB'],'Euronext Growth Dublin':['XESM'],'Euronext Growth Lisbon':['ALXL']}
marketmap=[];country_counts=Counter();securities=[];edges=[]
for label in sorted({r['Market'] for r in data}):
 if label in aliases:codes=aliases[label]
 elif label.startswith('Euronext Growth '):codes=[{'Paris':'ALXP','Brussels':'ALXB','Dublin':'XESM','Lisbon':'ALXL','Milan':'EXGM','Oslo':'MERK'}[s.strip()] for s in label[len('Euronext Growth '):].split(',')]
 else:assert label.startswith('Euronext '),label;codes=[base[s.strip()] for s in label[len('Euronext '):].split(',')]
 assert all(x in mic for x in codes),codes
 marketmap.append(dict(source_market_label=label,candidate_MICs_json=j(codes),candidate_market_countries_json=j(sorted({mic[x]['country'] for x in codes})),identity_state='CURATED_LABEL_TO_MIC_CANDIDATE_REVIEW_PENDING',MIC_source_rows_json=j([mic[x]['raw'] for x in codes])))
mm={r['source_market_label']:r for r in marketmap};dump('registry_market_label_MIC_candidates.csv',marketmap)
for i,r in enumerate(data,1):
 countries=json.loads(mm[r['Market']]['candidate_market_countries_json']);rec=dict(record_id=f'EURONEXT:{i}',source_name=r['Name'],ISIN=r['ISIN'],symbol=r['Symbol'],source_market=r['Market'],candidate_market_countries_json=j(countries),candidate_MICs_json=mm[r['Market']]['candidate_MICs_json'],issuer_country='UNKNOWN',issuer_identity='UNRESOLVED',raw_fields_json=j(r));securities.append(rec)
 c.execute('INSERT INTO listing_records VALUES(?,?,?,?,?,?,?)',(f'B08:EURONEXT:{i}','FINANCIAL_B08',countries[0] if len(countries)==1 else 'UNKNOWN',r['ISIN']+'|'+r['Symbol'],r['Name'],j(rec),'UNRESOLVED'))
 for code in countries:country_counts[code]+=1;edges.append(dict(record_id=rec['record_id'],iso_alpha2=code,relation='CANDIDATE_TRADING_MARKET_LOCATION_NOT_ISSUER_DOMICILE',evidence_state='REVIEW_PENDING'))
dump('registry_euronext_securities.csv',securities);dump('registry_euronext_country_candidates.csv',edges)
pagination=json.loads((O/'member_pagination.json').read_text());pages=[D/'members_iframe.html']+[D/x['file'] for x in pagination['other_pages']];members=[];pagecounts=[]
for page,p in enumerate(pages):
 t=html.fromstring(p.read_bytes());total=re.search(r'Displaying\s+(\d+)\s*-\s*(\d+)\s+of\s+(\d+)',' '.join(t.itertext()));assert total and int(total[3])==pagination['expected_total'];rs=t.xpath('//table')[0].xpath('./tbody/tr');n=0
 for k,r in enumerate(rs):
  cells=r.xpath('./td');
  if len(cells)!=9:continue
  assert k+2<len(rs) and len(rs[k+1].xpath('./td'))==len(rs[k+2].xpath('./td'))==1
  detail={}
  for box in rs[k+1].xpath('.//div[contains(@class,"col-3")]'):
   ps=box.xpath('./p');
   if ps:detail[text(ps[0])]=[text(x) for x in ps[1:]]
  perms=[]
  for tb in rs[k+2].xpath('.//table'):perms.append(dict(headers=[text(x) for x in tb.xpath('./thead/tr/th')],values=[[text(x) for x in tr.xpath('./td')] for tr in tb.xpath('./tbody/tr')],raw_html=html.tostring(tb,encoding='unicode')))
  member=dict(record_id=f'EURONEXT_MEMBER:{len(members)+1}',source_page=page,source_name=text(cells[0]),source_detail_fields_json=j(detail),overview_cells_json=j([dict(text=text(x),html=html.tostring(x,encoding='unicode')) for x in cells]),source_permissions_json=j(perms),raw_three_rows_html='\n'.join(html.tostring(x,encoding='unicode') for x in rs[k:k+3]),legal_identity='UNRESOLVED',source_country='UNKNOWN_NO_AUTOMATIC_ADDRESS_INFERENCE');members.append(member);n+=1
 assert n==int(total[2])-int(total[1])+1;pagecounts.append(dict(page=page,source_records=n,source_total=int(total[3]),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert len(members)==pagination['expected_total'];dump('registry_euronext_trading_members.csv',members);dump('registry_member_page_reconciliation.csv',pagecounts)
features=[dict(feature_id=fid,properties=json.loads(props)) for fid,props in c.execute('SELECT feature_id,properties_json FROM historical_feature_snapshots')];byname=defaultdict(list);relations=[]
for x in features:
 p=x['properties'];byname[p['Name']].append(x)
 for field in ['Components','MemberOf']:
  if not p.get(field):continue
  for token in p[field].split(';'):
   if token.strip():relations.append(dict(feature_id=x['feature_id'],source_name=p['Name'],source_type=p['Type'],from_year=p['FromYear'],to_year=p['ToYear'],relation_field=field,target_name_literal=token.strip(),target_resolution='PENDING',source_property_value=p[field]))
for r in relations:
 candidates=[x['feature_id'] for x in byname.get(r['target_name_literal'],[]) if x['properties']['FromYear']<=r['to_year'] and x['properties']['ToYear']>=r['from_year']];r['target_candidate_ids_json']=j(candidates);r['target_resolution']='EXACT_SOURCE_NAME_AND_TIME_CANDIDATES_NOT_ADJUDICATED' if candidates else 'NO_OVERLAPPING_EXACT_NAME_SOURCE_RECORD'
dump('registry_historical_source_relationships.csv',relations)
overlaps=[];gaps=[]
for name,rs in byname.items():
 rs=sorted(rs,key=lambda x:(x['properties']['FromYear'],x['properties']['ToYear']));end=None;prev=None
 for x in rs:
  p=x['properties']
  if end is not None:
   if p['FromYear']<=end:overlaps.append(dict(source_name=name,previous_feature_id=prev['feature_id'],feature_id=x['feature_id'],overlap_from=p['FromYear'],overlap_to=min(end,p['ToYear']),status='OVERLAPPING_SOURCE_INTERVALS_REVIEW_PENDING'))
   elif p['FromYear']>end+1:gaps.append(dict(source_name=name,after_feature_id=prev['feature_id'],before_feature_id=x['feature_id'],unobserved_from=end+1,unobserved_to=p['FromYear']-1,status='SOURCE_GAP_NOT_PROOF_OF_POLITY_ABSENCE'))
  if end is None or p['ToYear']>end:end=p['ToYear'];prev=x
dump('registry_historical_interval_overlaps.csv',overlaps,['source_name','previous_feature_id','feature_id','overlap_from','overlap_to','status']);dump('registry_historical_interval_gaps.csv',gaps,['source_name','after_feature_id','before_feature_id','unobserved_from','unobserved_to','status'])
currency_path=R/'Reference/tables/21_currency_broker_b03_20261007/registry_iso4217_all_entries.csv'
with currency_path.open(encoding='utf-8-sig') as f:currencies=list(csv.DictReader(f))
currency_dates=[]
for r in currencies:
 if r['state']!='HISTORICAL':continue
 raw=r['withdrawal_date'];currency_dates.append(dict(record_id=r['record_id'],source_entity_name=r['source_entity_name'],currency_name=r['currency_name'],alphabetic_code=r['alphabetic_code'],withdrawal_date_source=raw,date_precision='MONTH' if re.fullmatch(r'\d{4}-\d{2}',raw) else 'SOURCE_TEXT_REQUIRES_REVIEW',start_date='UNKNOWN',historical_polity_identity='UNRESOLVED',usage_scope='ISO4217_WITHDRAWAL_NOT_ALL_HISTORICAL_CURRENCY_USAGE',raw_fields_json=j(r)))
dump('registry_historical_currency_withdrawal_dates.csv',currency_dates)
coverage=[]
for code,fields in c.execute('SELECT iso_alpha2,fields_json FROM country_coverage').fetchall():
 r=json.loads(fields);r['euronext_candidate_market_records']=country_counts[code];r['euronext_label_mapping_state']='REVIEW_PENDING_NOT_COUNTRY_COMPLETE';coverage.append(dict(iso_alpha2=code,fields_json=j(r)));c.execute('UPDATE country_coverage SET fields_json=? WHERE iso_alpha2=?',(j(r),code))
 task=c.execute('SELECT fields_json FROM country_workstreams WHERE task_id=?',(code+':LISTED_COMPANIES',)).fetchone();p=json.loads(task[0]);p['euronext_candidate_market_records']=country_counts[code];p['completion']='OPEN';c.execute('UPDATE country_workstreams SET fields_json=? WHERE task_id=?',(j(p),code+':LISTED_COMPANIES'))
dump('registry_all_current_country_coverage.csv',coverage)
for table in ['historical_source_relationships','historical_interval_gaps','historical_interval_overlaps','historical_currency_withdrawal_dates','euronext_trading_members']:
 c.execute('CREATE TABLE '+table+'(source_row INTEGER PRIMARY KEY,fields_json TEXT)')
 p=T/('registry_'+table+'.csv')
 with p.open(encoding='utf-8-sig') as f:
  for i,row in enumerate(csv.DictReader(f),1):c.execute('INSERT INTO '+table+' VALUES(?,?)',(i,j(row)))
for p in sorted(T.glob('*.csv')):
 with p.open(encoding='utf-8-sig') as f:
  for i,row in enumerate(csv.DictReader(f),1):c.execute('INSERT INTO raw_records VALUES(?,?,?,?)',('GLOBAL_EXPANSION_B02',p.stem,i,j(row)))
for table in ['raw_records','listing_records','mic_registry','esma_entities','esma_activities']:
 cols=[r[1] for r in c.execute('PRAGMA main.table_info('+table+')')];select=','.join('"'+x+'"' for x in cols);assert c.execute('SELECT COUNT(*) FROM (SELECT '+select+' FROM prior.'+table+' EXCEPT SELECT '+select+' FROM main.'+table+')').fetchone()[0]==0
assert c.execute('SELECT COUNT(*) FROM (SELECT * FROM hist.historical_features EXCEPT SELECT * FROM historical_feature_snapshots)').fetchone()[0]==0
c.commit();assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
summary=dict(euronext_security_records=len(data),euronext_metadata_rows=len(metadata),directory_total=overview['iTotalRecords'],all_download_records_count_reconciled=True,euronext_ISIN_count=len({r['ISIN'] for r in data}),source_market_labels=len(marketmap),candidate_market_country_counts=dict(country_counts),member_records=len(members),member_pages=len(pages),member_name_count=len({r['source_name'] for r in members}),all_member_pages_reconciled=True,historical_features_retained=len(features),historical_relation_tokens=len(relations),relations_without_overlapping_exact_name=sum(r['target_resolution'].startswith('NO_') for r in relations),overlapping_intervals=len(overlaps),unobserved_intervals=len(gaps),historical_currency_records=len(currency_dates),current_country_rows=len(coverage),financial_tasks=c.execute('SELECT COUNT(*) FROM country_workstreams').fetchone()[0],total_listing_records=c.execute('SELECT COUNT(*) FROM listing_records').fetchone()[0],total_raw_records=c.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0],all_prior_financial_rows_retained=True,all_prior_historical_features_retained=True,global_complete=False,database_integrity='ok',full_POST_query_not_received=json.loads((D/'equities_full_post.json').read_text()).get('iTotalRecords') is None)
(O/'validation.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8');c.close()
deps=[prior,hist,currency_path];(O/'dependency_manifest.json').write_text(json.dumps([dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in deps],indent=2)+'\n',encoding='utf-8');print(json.dumps(summary))
