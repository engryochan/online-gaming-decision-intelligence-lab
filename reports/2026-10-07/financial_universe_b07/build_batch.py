from pathlib import Path
import csv,json,hashlib,sqlite3,collections,unicodedata
csv.field_size_limit(32*1024*1024)
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/25_iso249_financial_universe_b07_20261007';T.mkdir(exist_ok=True)
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def dump(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def load(n):return json.loads((O/'raw'/n).read_text(encoding='utf-8'))
def key(s):return ''.join(c for c in unicodedata.normalize('NFKD',s).upper() if c.isalnum() and not unicodedata.combining(c))
mother=read(R/'Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv');assert len(mother)==249 and len({x['iso_alpha2'] for x in mother})==249
names={key(x['name_en']):x['iso_alpha2'] for x in mother};parents=load('esma_mif_parents_complete.json');joined=load('esma_mif_join_complete.json');pmap={x['id']:x for x in parents}
assert len(parents)==7162 and len(joined)==82530 and len({x['id'] for x in joined})==len(joined)
assert pmap=={x['id']:x for x in joined if x['type_s']=='parent'} and {x['_root_'] for x in joined}<=set(pmap)
assert all(key(x['ae_homeMemberState']) in names for x in parents)
entities=[dict(record_id=x['id'],source_entity_name=x['ae_entityName'],source_home_state=x['ae_homeMemberState'],home_iso_alpha2=names[key(x['ae_homeMemberState'])],host_state=x.get('ae_hostMemberState',''),office_type=x['ae_officeType'],source_status=x['ae_status'],source_LEI=x.get('ae_lei',''),source_head_office_LEI=x.get('ae_headOfficeLei',''),competent_authority=x.get('ae_competentAuthority',''),as_of_source_last_update=x.get('ae_lastUpdate',''),raw_fields_json=json.dumps(x,ensure_ascii=False)) for x in parents]
activities=[dict(record_id=x['id'],parent_record_id=x['_root_'],record_type=x['entity_type'],home_iso_alpha2=names[key(pmap[x['_root_']]['ae_homeMemberState'])],service_name=x.get('ac_serviceName',x.get('ah_serviceName','')),source_status=x.get('ac_status',x.get('ah_status','')),raw_fields_json=json.dumps(x,ensure_ascii=False)) for x in joined if x['type_s']=='child']
dump('registry_esma_investment_firm_entities.csv',entities);dump('registry_esma_activities_and_history.csv',activities)
authorities=collections.defaultdict(list)
for x in entities:authorities[(x['home_iso_alpha2'],x['competent_authority'])].append(x['record_id'])
dump('registry_competent_authority_source_names.csv',[dict(home_iso_alpha2=k[0],source_authority_name=k[1],source_entity_records=len(v),source_ids_json=json.dumps(v),identity_state='SOURCE_NAME_NOT_GLOBAL_AUTHORITY_ID') for k,v in sorted(authorities.items())])
groups=collections.Counter((x['home_iso_alpha2'],x['source_status'],x['office_type']) for x in entities)
dump('esma_country_status_office_analysis.csv',[dict(home_iso_alpha2=k[0],source_status=k[1],office_type=k[2],source_records=v,unique_broker_count='UNKNOWN') for k,v in sorted(groups.items())])
base=R/'reports/2026-10-07/financial_universe_b06/financial_universe_v3.sqlite';db=O/'financial_universe_v4.sqlite';assert not db.exists();old=sqlite3.connect(base);con=sqlite3.connect(db);old.backup(con)
oldcoverage={x[0]:json.loads(x[1]) for x in old.execute('SELECT iso_alpha2,fields_json FROM country_coverage')};mic=[json.loads(x[0]) for x in old.execute('SELECT fields_json FROM mic_registry')]
rawmic={x['MIC']:json.loads(x['raw_fields_json']) for x in mic};currency=read(R/'Reference/tables/21_currency_broker_b03_20261007/registry_iso4217_all_entries.csv');coverage=[];tasks=[]
for m in sorted(mother,key=lambda x:x['iso_alpha2']):
 code=m['iso_alpha2'];c=dict(oldcoverage[code]);markets=[x for x in mic if x['country_iso_raw']==code];ep=[x for x in entities if x['home_iso_alpha2']==code];curr=[x for x in currency if x['state']=='CURRENT' and x['iso_alpha2']==code]
 sites=sorted({rawmic[x['MIC']]['WEBSITE'] for x in markets if rawmic[x['MIC']]['WEBSITE']});codes=sorted({x['alphabetic_code'] for x in curr if x['alphabetic_code']});auth=sorted({x['competent_authority'] for x in ep if x['competent_authority']})
 inventory={'ESMA_ENTITY_RECORDS':len(ep)} if ep else {}
 if code=='JP':inventory.update(FSA_FINANCIAL_INSTRUMENT_FIRMS=1951,JPX_PARTICIPANTS=158)
 if code=='TW':inventory.update(TWSE_BROKER_MATCHED_SOURCE_CODES=64)
 if code=='NZ':inventory.update(NZX_PARTICIPANTS=26)
 c.update(esma_home_state_records=len(ep),esma_active_records=sum(x['source_status']=='Active' for x in ep),esma_head_office_records=sum(x['office_type']=='Head office' for x in ep),esma_branch_records=sum(x['office_type']=='Branch' for x in ep),MIC_source_websites_json=json.dumps(sites,ensure_ascii=False),competent_authority_source_names_json=json.dumps(auth,ensure_ascii=False),currency_source_entries=len(curr),current_currency_codes_json=json.dumps(codes),securities_firm_source_inventory_json=json.dumps(inventory),mother_relationship_note=m.get('relationship_note',''),mother_row_json=json.dumps(m,ensure_ascii=False),all_brokers_complete='UNKNOWN',all_listed_companies_complete='UNKNOWN',all_locally_used_currencies='UNKNOWN')
 if ep:c['broker_coverage']='ESMA_MIF_ALL_SOURCE_ENTITIES_AND_ACTIVITIES_INGESTED_REGULATORY_SCOPE_REVIEW_PENDING'
 coverage.append(c);con.execute('UPDATE country_coverage SET fields_json=? WHERE iso_alpha2=?',(json.dumps(c,ensure_ascii=False),code))
 for stream in ['LISTED_COMPANIES','SECURITIES_FIRMS','CURRENCIES']:
  count=c.get('listing_source_records',0) if stream=='LISTED_COMPANIES' else (sum(inventory.values()) if stream=='SECURITIES_FIRMS' else len(curr))
  state='SOURCE_RECORDS_PRESENT_COMPLETENESS_NOT_CERTIFIED' if count else 'NO_GLOBAL_FEED_RECORDS_ADDITIONAL_PRIMARY_RESEARCH_REQUIRED'
  if stream=='SECURITIES_FIRMS' and code in ['JP','TW','NZ']:state='OTHER_BATCH_SOURCE_PRESENT_COMPLETENESS_NOT_CERTIFIED'
  task=dict(task_id=code+':'+stream,iso_alpha2=code,name_en=m['name_en'],stream=stream,source_record_count=count,source_state=state,completion='OPEN',market_websites_json=json.dumps(sites,ensure_ascii=False),competent_authority_names_json=json.dumps(auth,ensure_ascii=False),currency_codes_json=json.dumps(codes),gap='FULL_MARKET_AND_REGULATOR_ENUMERATION_LEGAL_IDENTITIES_OFFICIAL_TOTALS_ASOF_AND_CROSS_BORDER_RELATIONS' if stream!='CURRENCIES' else 'LEGAL_TENDER_ACTUAL_USAGE_LOCAL_SUPPLEMENTARY_DIGITAL_AND_HISTORICAL_SCOPE',closure_evidence='OFFICIAL_COMPLETE_REGISTERS_RECONCILED_AND_REVIEWED' if stream!='CURRENCIES' else 'CENTRAL_BANK_AND_OFFICIAL_RULES_ALL_CURRENCY_RELATIONS_REVIEWED',no_source_does_not_mean_absence=True)
  tasks.append(task)
assert len(coverage)==249 and len(tasks)==747 and len({x['task_id'] for x in tasks})==747
dump('registry_iso249_financial_coverage.csv',coverage);dump('registry_iso249_three_stream_tasks.csv',tasks)
sources=[]
for name in ['esma_parent_pagination.json','esma_activity_pagination.json']:
 pagination=json.loads((O/name).read_text(encoding='utf-8'));assert pagination['complete']
 for page in pagination['pages']:
  p=O/'raw'/page['file'];body=json.loads(p.read_text(encoding='utf-8'));assert body['response']['numFound']==pagination['stable_numFound'];sources.append(dict(path=p.relative_to(R).as_posix(),url=page['url'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),records=page['rows'],numFound=page['numFound'],source_server_date=page['server_date'],start=page['start']))
dump('source_page_manifest.csv',sources)
con.execute('CREATE TABLE esma_entities(record_id TEXT PRIMARY KEY,home_iso_alpha2 TEXT,source_status TEXT,office_type TEXT,fields_json TEXT)');con.executemany('INSERT INTO esma_entities VALUES (?,?,?,?,?)',[(x['record_id'],x['home_iso_alpha2'],x['source_status'],x['office_type'],json.dumps(x,ensure_ascii=False)) for x in entities])
con.execute('CREATE TABLE esma_activities(record_id TEXT PRIMARY KEY,parent_record_id TEXT,record_type TEXT,fields_json TEXT)');con.executemany('INSERT INTO esma_activities VALUES (?,?,?,?)',[(x['record_id'],x['parent_record_id'],x['record_type'],json.dumps(x,ensure_ascii=False)) for x in activities])
con.execute('CREATE INDEX esma_activities_parent ON esma_activities(parent_record_id)');con.execute('CREATE INDEX esma_entities_home ON esma_entities(home_iso_alpha2)');con.execute('CREATE TABLE country_workstreams(task_id TEXT PRIMARY KEY,iso_alpha2 TEXT,stream TEXT,fields_json TEXT)');con.executemany('INSERT INTO country_workstreams VALUES (?,?,?,?)',[(x['task_id'],x['iso_alpha2'],x['stream'],json.dumps(x,ensure_ascii=False)) for x in tasks])
manifest=[]
for p in sorted(T.glob('*.csv')):
 data=read(p);con.executemany('INSERT INTO raw_records VALUES (?,?,?,?)',[('FINANCIAL_B07',p.stem,i,json.dumps(x,ensure_ascii=False)) for i,x in enumerate(data,1)])
 assert [json.loads(x[0]) for x in con.execute('SELECT fields_json FROM raw_records WHERE namespace=? AND source_table=? ORDER BY source_row',('FINANCIAL_B07',p.stem))]==data
 manifest.append(dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=len(data)))
for table in ['raw_records','listing_records','mic_registry']:
 original=old.execute('SELECT * FROM '+table+' ORDER BY 1,2,3').fetchall();query='SELECT * FROM '+table+(" WHERE namespace!='FINANCIAL_B07'" if table=='raw_records' else '')+' ORDER BY 1,2,3';assert original==con.execute(query).fetchall()
assert con.execute('SELECT COUNT(*) FROM esma_activities a LEFT JOIN esma_entities e ON a.parent_record_id=e.record_id WHERE e.record_id IS NULL').fetchone()[0]==0
assert con.execute('SELECT COUNT(*) FROM currency_entries').fetchone()[0]==449 and con.execute('SELECT COUNT(*) FROM fsa_firms').fetchone()[0]==1951
assert {x['id']:x for x in parents}=={x['record_id']:json.loads(x['raw_fields_json']) for x in entities}
assert {x['id']:x for x in joined if x['type_s']=='child'}=={x['record_id']:json.loads(x['raw_fields_json']) for x in activities}
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';result=dict(all_249_countries_present=True,workstream_tasks=len(tasks),esma_entities=len(entities),esma_home_countries=len({x['home_iso_alpha2'] for x in entities}),esma_active_home_countries=len({x['home_iso_alpha2'] for x in entities if x['source_status']=='Active'}),esma_entity_status_counts=dict(collections.Counter(x['source_status'] for x in entities)),esma_office_type_counts=dict(collections.Counter(x['office_type'] for x in entities)),current_activity_records=sum(x['record_type']=='aeActivity' for x in activities),activity_history_records=sum(x['record_type']=='aeActivityHistory' for x in activities),authority_source_groups=len(authorities),all_page_numFound_and_unique_ids_reconciled=True,parent_entity_documents_match_join_query=True,all_activity_parents_present=True,all_source_json_fields_roundtrip=True,all_prior_raw_listing_mic_records_exactly_retained=True,total_listing_source_records=con.execute('SELECT COUNT(*) FROM listing_records').fetchone()[0],total_raw_records=con.execute('SELECT COUNT(*) FROM raw_records').fetchone()[0],new_tables=len(manifest),global_complete=False)
con.close();old.close();dump('integration_input_manifest.csv',manifest);(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');(O/'prior_snapshot_manifest.json').write_text(json.dumps(dict(path=base.relative_to(R).as_posix(),sha256=hashlib.sha256(base.read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
