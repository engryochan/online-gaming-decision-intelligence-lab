from pathlib import Path
import csv,json,hashlib,sqlite3,collections,re
csv.field_size_limit(16*1024*1024)
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/24_financial_universe_b06_20261007';T.mkdir(exist_ok=True)
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def dump(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def load(n):return json.loads((O/'raw'/n).read_text(encoding='utf-8-sig'))
sources=[];micraw=read(O/'raw/ISO10383_MIC.csv');assert len({x['MIC'] for x in micraw})==len(micraw)
assert {x['OPERATING MIC'] for x in micraw}<={x['MIC'] for x in micraw}
mic=[dict(MIC=x['MIC'],operating_MIC=x['OPERATING MIC'],operating_or_segment=x['OPRT/SGMT'],market_name=x['MARKET NAME-INSTITUTION DESCRIPTION'],legal_entity_name=x['LEGAL ENTITY NAME'],LEI=x['LEI'],market_category=x['MARKET CATEGORY CODE'],country_iso_raw=x['ISO COUNTRY CODE (ISO 3166)'],status=x['STATUS'],raw_fields_json=json.dumps(x,ensure_ascii=False)) for x in micraw]
dump('registry_iso10383_mic.csv',mic)
queue=[dict(MIC=x['MIC'],country_iso_raw=x['country_iso_raw'],market_name=x['market_name'],market_category=x['market_category'],investigation_state='LISTING_SCOPE_AND_OFFICIAL_DIRECTORY_TO_VERIFY',all_issuers_complete='UNKNOWN') for x in mic if x['operating_or_segment']=='OPRT' and x['status']=='ACTIVE']
dump('registry_operating_market_research_queue.csv',queue)
sources.append(dict(source='ISO10383_MIC',url='https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv',sha256=hashlib.sha256((O/'raw/ISO10383_MIC.csv').read_bytes()).hexdigest(),rows=len(mic),as_of='PUBLICATION_2026-09-14_IMPLEMENTATION_2026-09-28',scope='ALL_PUBLISHED_MIC_ROWS_NOT_ALL_STOCK_EXCHANGES'))
companies=[];raw_company_sets=[]
for feed,fname,url,kind in [('TWSE_LISTED','twse_listed.json','https://openapi.twse.com.tw/v1/opendata/t187ap03_L','LISTED'),('TPEX_OTC','tpex_otc.json','https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O','OTC'),('TPEX_EMERGING','tpex_emerging.json','https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_R','EMERGING_SEPARATE_CATEGORY')]:
 data=load(fname);assert isinstance(data,list) and len(data)>100
 for i,x in enumerate(data,1):
  code=x['公司代號'] if feed=='TWSE_LISTED' else x['SecuritiesCompanyCode'];name=x['公司名稱'] if feed=='TWSE_LISTED' else x['CompanyName'];uid=x['營利事業統一編號'] if feed=='TWSE_LISTED' else x['UnifiedBusinessNo.'];foreign=x['外國企業註冊地國'] if feed=='TWSE_LISTED' else x['Registration'];date=x['出表日期'] if feed=='TWSE_LISTED' else x['Date']
  companies.append(dict(record_id=f'{feed}:{i}',feed=feed,company_code=code,source_company_name=name,source_business_number=uid,source_foreign_registration_country=foreign,market_iso_alpha2='TW',legal_domicile_iso_alpha2='UNKNOWN',listing_category=kind,source_date_raw=date,raw_fields_json=json.dumps(x,ensure_ascii=False)))
 assert [json.loads(x['raw_fields_json']) for x in companies if x['feed']==feed]==data
 raw_company_sets.append((feed,len(data)));sources.append(dict(source=feed,url=url,sha256=hashlib.sha256((O/'raw'/fname).read_bytes()).hexdigest(),rows=len(data),as_of='SOURCE_ROW_DATE_PRESERVED',scope='ALL_API_RESPONSE_COMPANY_ROWS'))
dump('registry_tw_company_profiles.csv',companies)
hq=load('twse_broker_hq.json');profiles=load('twse_broker_profiles.json');assert len({x['Code'] for x in hq})==len(hq) and len({x['證券代號'] for x in profiles})==len(profiles);assert {x['Code'] for x in hq}=={x['證券代號'] for x in profiles}
hqmap={x['Code']:x for x in hq};brokers=[dict(broker_code=x['證券代號'],source_short_name=x['券商(證券IB)簡稱'],source_business_number=x['營利事業統一編號'],source_business_type=x['業務種類'],source_issue_state=x['發行狀況'],source_date_raw=x['出表日期'],market_iso_alpha2='TW',legal_domicile='UNKNOWN',hq_raw_fields_json=json.dumps(hqmap[x['證券代號']],ensure_ascii=False),profile_raw_fields_json=json.dumps(x,ensure_ascii=False)) for x in profiles]
assert [json.loads(x['profile_raw_fields_json']) for x in brokers]==profiles
assert {x['broker_code']:json.loads(x['hq_raw_fields_json']) for x in brokers}==hqmap
dump('registry_tw_broker_source_profiles.csv',brokers)
for source,fname,url in [('TWSE_BROKER_HQ','twse_broker_hq.json','https://openapi.twse.com.tw/v1/brokerService/brokerList'),('TWSE_BROKER_PROFILE','twse_broker_profiles.json','https://openapi.twse.com.tw/v1/opendata/t187ap18')]:sources.append(dict(source=source,url=url,sha256=hashlib.sha256((O/'raw'/fname).read_bytes()).hexdigest(),rows=len(load(fname)),as_of='PROFILE_DATE_1151007_HQ_DATE_NOT_PROVIDED',scope='ALL_RESPONSE_ROWS_NOT_REGULATOR_ALL_LICENSES_CERTIFIED'))
dump('source_manifest.csv',sources)
edges=[]
for b in brokers:
 uid=b['source_business_number'].strip()
 if re.fullmatch('[0-9]{8}',uid) and uid!='00000000':
  for c in companies:
   if c['source_business_number'].strip()==uid:
    edges.append(dict(broker_code=b['broker_code'],company_record_id=c['record_id'],company_code=c['company_code'],source_business_number=uid,method='EXACT_SHARED_OFFICIAL_BUSINESS_NUMBER',state='SOURCE_IDENTIFIER_MATCH_LEGAL_REGISTRATION_REVIEW_PENDING'))
if edges:dump('broker_company_identifier_links.csv',edges)
base=R/'reports/2026-10-07/listed_universe_b05/financial_universe_v2.sqlite';db=O/'financial_universe_v3.sqlite';assert not db.exists();old=sqlite3.connect(base);con=sqlite3.connect(db);old.backup(con)
new=[('B06:'+x['record_id'],'FINANCIAL_B06_TW','TW',x['company_code'],x['source_company_name'],json.dumps(x,ensure_ascii=False),'SOURCE_BUSINESS_NUMBER_REGISTRATION_REVIEW_PENDING') for x in companies];con.executemany('INSERT INTO listing_records VALUES (?,?,?,?,?,?,?)',new)
con.execute('CREATE TABLE mic_registry(MIC TEXT PRIMARY KEY,operating_MIC TEXT,country_iso_raw TEXT,status TEXT,fields_json TEXT)');con.executemany('INSERT INTO mic_registry VALUES (?,?,?,?,?)',[(x['MIC'],x['operating_MIC'],x['country_iso_raw'],x['status'],json.dumps(x,ensure_ascii=False)) for x in mic])
coverage=[json.loads(x[0]) for x in old.execute('SELECT fields_json FROM country_coverage ORDER BY iso_alpha2')];market_counts=dict(con.execute('SELECT * FROM market_listing_counts'));known={x['iso_alpha2'] for x in coverage};miccountries={x['country_iso_raw'] for x in mic}
for x in coverage:
 code=x['iso_alpha2'];subset=[m for m in mic if m['country_iso_raw']==code];x['listing_source_records']=market_counts.get(code,0);x['listing_feed_state']='PARTIAL_SOURCE_INGESTION' if x['listing_source_records'] else 'NOT_YET_INGESTED';x['MIC_source_rows']=len(subset);x['MIC_active_rows']=sum(m['status']=='ACTIVE' for m in subset);x['all_stock_exchanges_enumerated']='UNKNOWN'
 if code=='TW':x['broker_coverage']='TWSE_HQ_AND_PROFILE_CODESETS_RECONCILED_REGULATORY_UNIVERSE_PENDING'
 con.execute('UPDATE country_coverage SET fields_json=? WHERE iso_alpha2=?',(json.dumps(x,ensure_ascii=False),code))
dump('registry_country_financial_coverage.csv',coverage)
manifest=[]
for p in sorted(T.glob('*.csv')):
 data=read(p);con.executemany('INSERT INTO raw_records VALUES (?,?,?,?)',[('FINANCIAL_B06',p.stem,i,json.dumps(x,ensure_ascii=False)) for i,x in enumerate(data,1)])
 assert [json.loads(x[0]) for x in con.execute('SELECT fields_json FROM raw_records WHERE namespace=? AND source_table=? ORDER BY source_row',('FINANCIAL_B06',p.stem))]==data
 manifest.append(dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=len(data)))
for table in ['raw_records','listing_records']:
 original=old.execute('SELECT * FROM '+table+' ORDER BY 1,2,3').fetchall();retained=con.execute('SELECT * FROM '+table+" WHERE namespace NOT LIKE 'FINANCIAL_B06%' ORDER BY 1,2,3").fetchall();assert original==retained
assert con.execute('SELECT COUNT(*) FROM currency_entries').fetchone()[0]==449 and con.execute('SELECT COUNT(*) FROM fsa_firms').fetchone()[0]==1951
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
result=dict(mic_rows=len(mic),mic_statuses=dict(collections.Counter(x['status'] for x in mic)),mic_mother_country_matches=len(miccountries & known),mic_nonmother_codes=sorted(miccountries-known),active_operating_research_rows=len(queue),mic_parent_references_valid=True,company_feeds=dict(raw_company_sets),company_rows=len(companies),broker_profile_rows=len(brokers),broker_code_sets_equal=True,broker_company_identifier_links=len(edges),prior_rows_exactly_retained=True,all_new_rows_roundtrip=True,total_listing_source_records=con.execute('SELECT COUNT(*) FROM listing_records').fetchone()[0],total_raw_records=con.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0],new_tables=len(manifest),global_complete=False)
con.close();old.close();dump('integration_input_manifest.csv',manifest);(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');(O/'prior_snapshot_manifest.json').write_text(json.dumps(dict(path=base.relative_to(R).as_posix(),sha256=hashlib.sha256(base.read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
