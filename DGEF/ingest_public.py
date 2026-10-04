"""Validate downloaded evidence, append typed records, preserve existing identities."""
import csv,hashlib,json,re,sqlite3
from pathlib import Path
import fabric as f
HERE=f.HERE;INBOX=HERE/'inbox';OUT=f.ROOT/'reports/2026-10-04/dgef';OUT.mkdir(exist_ok=True)
TRANSFORM='public-snapshot-1.0'
def stable(*xs):return hashlib.sha256('\x1f'.join(str(x) for x in xs).encode('utf-8')).hexdigest()
def rows(table):return dict(C.execute(f'SELECT entity_id,canonical_name FROM {table}'))
def prov(sid,date):return dict(source_id=sid,evidence_state='VERIFIED',valid_from=date,transaction_time=f.now())
def identity(system,key,name,kind,sid,date,version):
 existing={r[0] for r in C.execute('SELECT entity_id FROM bridge_entity_external_id WHERE id_system=? AND external_id=?',(system,key))}
 if len(existing)>1:raise ValueError('Conflicting accepted identity:'+system+key)
 eid=next(iter(existing)) if existing else 'DUECG-EID::'+f.uuid7()
 f.insert(C,'registry_entity',entity_id=eid,entity_type=kind,canonical_name=name,world_domain='REAL-TWIN',status='SOURCE_CONFIRMED',valid_from=date,transaction_time=f.now())
 f.insert(C,'bridge_entity_external_id',bridge_id=stable(system,key,version),entity_id=eid,id_system=system,external_id=key,external_version=version,match_method='EXACT_EXTERNAL_IDENTIFIER_NOT_NAME_MATCH',review_status='ACCEPTED',**prov(sid,date))
 return eid
def claim(eid,predicate,value,sid,date,key=None):
 cid='WEBCLAIM_'+stable(eid,predicate,key or sid)
 f.insert(C,'registry_claim',claim_id=cid,subject_entity_id=eid,predicate=predicate,value_json=json.dumps(value,ensure_ascii=False),claim_status='VERIFIED',**prov(sid,date))
 f.insert(C,'registry_evidence_link',evidence_link_id='WEBEVIDENCE_'+stable(cid,sid),claim_id=cid,source_id=sid,direction='SUPPORTS',locator=predicate,transaction_time=f.now())
 return cid
def raw_record(did,key,r,eid):
 f.insert(C,'registry_ingest_record',ingest_id=stable(did,key),entity_id=eid,dataset_id=did,external_key=key,record_payload=json.dumps(r,ensure_ascii=False),transform_version=TRANSFORM,transaction_time=f.now())
def alias(eid,name,lang,kind,sid,date):
 f.insert(C,'registry_entity_alias',alias_id=stable(eid,name,lang,date),entity_id=eid,alias=name,language_tag=lang or 'und',alias_kind=kind,**prov(sid,date))
def domain(table,eid,sid,date,**fields):
 f.insert(C,table,record_id=stable(table,eid,sid),entity_id=eid,**fields,**prov(sid,date))

def run():
 global C
 manifest=json.loads((INBOX/'manifest.json').read_text(encoding='utf-8'))
 # Snapshot existing database before additive schema/data changes.
 C=sqlite3.connect(HERE/'artifacts/dgef.sqlite');C.execute('PRAGMA foreign_keys=ON')
 before=rows('registry_entity');before_ids=set(before);old_counts={n:C.execute(f'SELECT count(*) FROM {n}').fetchone()[0] for n in f.SPECS if C.execute('SELECT 1 FROM sqlite_master WHERE name=?',(n,)).fetchone()}
 backup=OUT/'before_public_ingestion.sqlite'
 if not backup.exists():
  with sqlite3.connect(backup) as b:C.backup(b)
 C.executescript(f.schema());warnings=[];ror_records={};stats={}
 country={r[0]:r[1] for r in C.execute('SELECT iso_alpha2,entity_id FROM registry_country_area')}
 with C:
  f.insert(C,'registry_schema_version',version=f.VERSION,installed_at=f.now(),description='Additive registry_ingest_record; public snapshots, no baseline replacement')
  f.insert(C,'registry_license_policy',policy_id='ROR_CC0',license='CC0-1.0',redistribution_allowed=1,commercial_use_allowed=1,retention_rule='KEEP_VERSION_AND_ATTRIBUTION',assessed_at=f.now())
  for m in manifest:
   if m['status']!='FETCHED':warnings.append(dict(key=m['key'],reason=m.get('error','FETCH_FAILED')));continue
   b=(INBOX/m['file']).read_bytes()
   if hashlib.sha256(b).hexdigest()!=m['sha256']:raise ValueError('Raw response fingerprint mismatch:'+m['key'])
   sid='PUBLIC_'+stable(m['url'])[:24];date=m['retrieved_at'][:10];version=m['sha256'];did='SNAPSHOT_'+stable(sid,version)
   f.insert(C,'registry_source',source_id=sid,publisher=m['kind'],source_type='OFFICIAL_DATA' if m['kind']!='OFFICIAL_WEB' else 'OFFICIAL_WEBSITE',canonical_uri=m['url'],access_class='PUBLIC',retrieved_at=m['retrieved_at'],content_hash=version,policy_id='ROR_CC0' if m['kind']=='ROR' else 'UNKNOWN',verification_scope='Downloaded response; exact supported fields only. No independent performance or completeness certification.')
   data=json.loads(b) if m['kind']!='OFFICIAL_WEB' else {'page_uri':m['url'],'content_sha256':version}
   records=data.get('items',[]) if m['kind']=='ROR' else data.get('data',[]) if m['kind']=='LEI' else data if m['kind']=='EXOPLANET' else [data]
   f.insert(C,'registry_dataset',dataset_id=did,source_id=sid,dataset_version=version,file_sha256=version,row_count=len(records),imported_at=m['retrieved_at'])
   stats[m['key']]=len(records)
   if m['kind']=='ROR':
    for r in records:
     name=next(n['value'] for n in r['names'] if 'ror_display' in n['types']);key=r['id'];eid=identity('ROR',key,name,'RESEARCH_ORG',sid,date,version)
     raw_record(did,key,r,eid);ror_records[key]=(eid,r,sid,date)
     domain('registry_research_org',eid,sid,date,org_kind=';'.join(r['types']),research_scope='SOURCE_ORGANIZATION_REGISTRY; SPECIFIC_CAPABILITIES_NOT_ASSESSED')
     claim(eid,'ROR_ORGANIZATION_METADATA',{'types':r['types'],'status':r['status'],'last_modified':r['admin']['last_modified'],'established':r.get('established')},sid,date)
     f.insert(C,'registry_entity_status_history',history_id=stable(eid,sid,'status'),entity_id=eid,status='ROR:'+r['status'],**prov(sid,date))
     for n in r['names']:alias(eid,n['value'],n['lang'],';'.join(n['types']),sid,date)
     loc=r.get('locations',[]);cc=loc[0]['geonames_details']['country_code'] if loc else None
     if 'government' in r['types']:domain('registry_public_body',eid,sid,date,jurisdiction_entity_id=country.get(cc),mandate='ROR_GOVERNMENT_TYPE; STATUTORY_MANDATE_NOT_ASSESSED')
     if 'facility' in r['types']:
      # ROR coordinates refer to a GeoNames locality, not verified facility coordinates.
      if not C.execute('SELECT 1 FROM registry_public_facility WHERE entity_id=?',(eid,)).fetchone():domain('registry_public_facility',eid,sid,date,facility_kind='ROR_RESEARCH_FACILITY',public_acknowledgment_uri=key)
     for ext in r.get('external_ids',[]):
      for val in ext['all']:
       f.insert(C,'registry_external_id',external_key=stable(ext['type'],val,version),id_system=ext['type'],external_id=val,external_version=version,**prov(sid,date))
     if r.get('locations'):warnings.append(dict(key=key,reason='CITY_CENTROID_NOT_FACILITY_POSITION; epoch/frame precision unverified, not promoted to canonical location'))
   elif m['kind']=='LEI':
    for r in records:
     a=r['attributes'];e=a['entity'];key=a['lei'];name=e['legalName']['name']
     if e.get('category')=='SOLE_PROPRIETOR':warnings.append(dict(key=key,reason='PERSONAL_SOLE_PROPRIETOR_OUTSIDE_ORGANIZATION_SCOPE'));continue
     eid=identity('LEI',key,name,'LEGAL_ENTITY',sid,date,version);raw_record(did,key,r,eid)
     domain('registry_legal_entity',eid,sid,date,jurisdiction_entity_id=country.get(e['jurisdiction']),legal_form=e['legalForm'].get('id'),registration_status=a['registration']['status'])
     claim(eid,'GLEIF_LEGAL_REGISTRATION',{'entity_status':e['status'],'lei_status':a['registration']['status'],'registeredAt':e['registeredAt'],'registeredAs':e['registeredAs'],'jurisdiction':e['jurisdiction']},sid,date)
     f.insert(C,'registry_entity_status_history',history_id=stable(eid,sid,'status'),entity_id=eid,status='GLEIF_ENTITY:'+e['status']+';LEI:'+a['registration']['status'],**prov(sid,date))
     alias(eid,name,e['legalName']['language'],'LEGAL_NAME',sid,date)
     for n in e['otherNames']:alias(eid,n['name'],n['language'],n['type'],sid,date)
     # URLs for parent reporting exceptions are not parent relationships.
   elif m['kind']=='EXOPLANET':
    for r in records:
     key=r['pl_name'];eid=identity('NASA_EXOPLANET',key,key,'CELESTIAL_OBJECT',sid,date,version);raw_record(did,key,r,eid)
     domain('registry_celestial_object',eid,sid,date,object_kind='CONFIRMED_EXOPLANET',catalog_solution='pscomppars:'+version)
     claim(eid,'EXOPLANET_DISCOVERY_METADATA',r,sid,date)
   elif m['kind']=='SBDB':
    if data['signature']['version']!='1.3':raise ValueError('Unexpected SBDB schema version')
    obj=data['object'];key=obj['spkid'];eid=identity('JPL_SBDB_SPKID',key,obj['fullname'],'CELESTIAL_OBJECT',sid,date,version);raw_record(did,key,data,eid)
    domain('registry_celestial_object',eid,sid,date,object_kind=obj['kind'],catalog_solution='SBDB orbit:'+obj['orbit_id'])
    claim(eid,'SBDB_OBJECT_AND_ORBIT',{'object':obj,'orbit':data.get('orbit')},sid,date)
    for p in data.get('phys_par',[]):
     try:value=float(p['value'])
     except (ValueError,TypeError):continue
     try:unc=float(p['sigma']) if p.get('sigma') else None
     except ValueError:unc=None
     cid=claim(eid,'SBDB_PHYSICAL_PARAMETER_'+p['name'],p,sid,date)
     ref=p.get('ref') or ''
     if re.search(r'\b(?:Science|Nature|Icarus|Astron|Astrophys)',ref) and re.search(r'\b(?:19|20)\d{2}\b',ref):
      output_eid=identity('JPL_SBDB_BIBLIOGRAPHIC_REFERENCE',ref,'Reference: '+ref,'RESEARCH_OUTPUT',sid,date,version)
      domain('registry_space_research_output',output_eid,sid,date,title='Bibliographic reference (not verified paper title): '+ref)
      claim(output_eid,'BIBLIOGRAPHIC_REFERENCE_LISTED_BY_SBDB',{'reference':ref,'metric':p['name'],'object':obj['fullname']},sid,date)
     f.insert(C,'registry_observation',observation_id=stable(eid,p['name'],sid),entity_id=eid,metric_id='SBDB:'+p['name'],value=value,unit=p['units'] or 'SOURCE_UNSPECIFIED',uncertainty=unc,method_id='CATALOG_PARAMETER_RETRIEVAL; '+str(p.get('ref')),claim_id=cid,**prov(sid,date))
   elif m['kind']=='HORIZONS':
    result=data['result'];target=re.search(r'Target body name:\s+(.+?)\s+\((\d+)\)',result)
    if not target or 'Center body name: Sun (10)' not in result or 'TDB' not in result:raise ValueError('Unexpected Horizons frame/target metadata')
    name,key=target.groups();eid=identity('HORIZONS_TARGET',key,name,'CELESTIAL_OBJECT',sid,date,version);raw_record(did,key,data,eid)
    frame='HORIZONS_ECLIPJ2000_SUN_AU'
    f.insert(C,'registry_spatial_frame',frame_id=frame,cosmic_domain='SOLAR_SYSTEM',center_name='Sun',axis_definition='J2000 ecliptic reference plane, ICRF orientation, as requested and confirmed in response',position_unit='AU',velocity_unit='AU/day',reference_uri='https://ssd-api.jpl.nasa.gov/doc/horizons.html')
    domain('registry_celestial_object',eid,sid,date,object_kind='NATURAL_SATELLITE' if key=='301' else 'PLANET',catalog_solution='Horizons:'+version)
    content=result.split('$$SOE')[1].split('$$EOE')[0]
    for line in content.strip().splitlines():
     cells=next(csv.reader([line]));jd=cells[0].strip();vals=[float(x) for x in cells[2:8]]
     if len(vals)!=6:raise ValueError('Vector row shape mismatch')
     f.insert(C,'registry_entity_location',location_observation_id=stable(eid,jd,sid),entity_id=eid,cosmic_domain='SOLAR_SYSTEM',spatial_frame=frame,central_body='Sun',epoch='JD:'+jd,time_scale='TDB',x=vals[0],y=vals[1],z=vals[2],vx=vals[3],vy=vals[4],vz=vals[5],position_unit='AU',velocity_unit='AU/day',source_solution='Horizons:'+version,disclosure_precision='PUBLIC_PRECISE',**prov(sid,date))
     f.insert(C,'registry_ephemeris_solution',record_id=stable(eid,jd,sid),entity_id=eid,frame_id=frame,epoch='JD:'+jd,time_scale='TDB',position_unit='AU',velocity_unit='AU/day',solution_version=version,**prov(sid,date))
   elif m['kind']=='OFFICIAL_WEB':
    raw_record(did,m['key'],data,None)
  # Only resolve relationships whose endpoints were independently returned by ROR.
  for key,(eid,r,sid,date) in ror_records.items():
   for rel in r.get('relationships',[]):
    if rel['id'] not in ror_records:continue
    other=ror_records[rel['id']][0]
    f.insert(C,'registry_entity_relation',relation_id=stable(eid,rel['type'],other,sid),subject_entity_id=eid,predicate='ROR:'+rel['type'],object_entity_id=other,**prov(sid,date))
  curated_web(manifest,ror_records)
  for system,target,url in [('ROR','registry_research_org','https://api.ror.org/v2/organizations'),('LEI','registry_legal_entity','https://api.gleif.org/api/v1/lei-records'),('JPL_SBDB','registry_celestial_object','https://ssd-api.jpl.nasa.gov/sbdb.api'),('JPL_HORIZONS','registry_ephemeris_solution','https://ssd.jpl.nasa.gov/api/horizons.api'),('NASA_EXOPLANET','registry_celestial_object','https://exoplanetarchive.ipac.caltech.edu/TAP/sync'),('OFFICIAL_SPACE_WEB','registry_space_mission','https://www.cnsa.gov.cn/')]:
   f.insert(C,'registry_adapter_contract',adapter_id='PUBLIC_SNAPSHOT:'+system,id_system=system,canonical_uri=url,target_table=target,version_required=1,status='LOCAL_IMPORTED',license_review='ROR_CC0' if system=='ROR' else 'KEEP_UNKNOWN_FOR_TRAINING',notes='Versioned downloaded responses imported; query sample only. Earlier interface-only contract retained as baseline history.')
 assert before=={k:v for k,v in rows('registry_entity').items() if k in before_ids},'Existing identity/name regression'
 assert C.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert not C.execute('PRAGMA foreign_key_check').fetchall()
 after={n:C.execute(f'SELECT count(*) FROM {n}').fetchone()[0] for n in f.SPECS};assert all(after[k]>=v for k,v in old_counts.items())
 report=dict(fetched=sum(m['status']=='FETCHED' for m in manifest),failed=sum(m['status']!='FETCHED' for m in manifest),source_response_records=stats,counts_before=old_counts,counts_after=after,new_entity_count=len(rows('registry_entity'))-len(before),old_identity_and_names_preserved=True,integrity='ok',foreign_key_errors=[],warnings=warnings,scope='query-based sample, not global full download; no frontier ranking assigned')
 (OUT/'public_ingestion_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');C.close();f.build(HERE/'artifacts');print(json.dumps({k:report[k] for k in ('fetched','failed','new_entity_count','integrity')},ensure_ascii=True))

def curated_web(manifest,ror_records):
 successful={m['key']:m for m in manifest if m['status']=='FETCHED'}
 def ror_exact(name):
  return next((eid for eid,r,s,d in ror_records.values() if any(n['value']==name for n in r['names'])),None)
 def context(key):
  m=successful[key];return 'PUBLIC_'+stable(m['url'])[:24],m['retrieved_at'][:10],m['sha256']
 if 'chang_e_5' in successful:
  sid,date,v=context('chang_e_5');cnsa=ror_exact('China National Space Administration')
  program=identity('OFFICIAL_NAMED_PROGRAM','CNSA:LUNAR_EXPLORATION','中国探月工程','PROGRAM',sid,date,v)
  mission=identity('OFFICIAL_NAMED_MISSION','CNSA:CHANG_E_5','嫦娥五号任务','MISSION',sid,date,v)
  probe=identity('OFFICIAL_NAMED_ASSET','CNSA:CHANG_E_5_PROBE','嫦娥五号探测器','ASSET',sid,date,v)
  vehicle=identity('OFFICIAL_NAMED_VEHICLE','CNSA:CZ5_Y5','长征五号遥五运载火箭','ASSET',sid,date,v)
  domain('registry_space_program',program,sid,date,lead_entity_id=cnsa,program_status='PUBLIC_PROGRAM_RECORD; CURRENT_STATUS_NOT_ASSESSED')
  domain('registry_space_mission',mission,sid,date,program_entity_id=program,mission_status='HISTORICAL_LAUNCH_CONFIRMED_2020_11_24')
  domain('registry_space_asset',probe,sid,date,asset_kind='LUNAR_PROBE',mission_entity_id=mission,operational_status='HISTORICAL_LAUNCH_RECORD; CURRENT_STATUS_NOT_ASSESSED')
  domain('registry_space_vehicle',vehicle,sid,date,vehicle_kind='LAUNCH_VEHICLE_FLIGHT',operational_status='HISTORICAL_LAUNCH_2020_11_24')
  claim(mission,'HISTORICAL_LAUNCH_DATE','2020-11-24',sid,date)
  if cnsa:domain('registry_space_org',cnsa,sid,date,org_role='PUBLIC_SPACE_AGENCY')
 if 'artemis' in successful:
  sid,date,v=context('artemis');nasa=ror_exact('National Aeronautics and Space Administration')
  program=identity('OFFICIAL_NAMED_PROGRAM','NASA:ARTEMIS','Artemis','PROGRAM',sid,date,v)
  mission=identity('OFFICIAL_NAMED_MISSION','NASA:ARTEMIS_I','Artemis I','MISSION',sid,date,v)
  asset=identity('OFFICIAL_NAMED_ASSET','NASA:ORION','Orion spacecraft','ASSET',sid,date,v)
  vehicle=identity('OFFICIAL_NAMED_VEHICLE','NASA:SLS','Space Launch System','ASSET',sid,date,v)
  domain('registry_space_program',program,sid,date,lead_entity_id=nasa,program_status='OFFICIAL_PROGRAM_PAGE')
  domain('registry_space_mission',mission,sid,date,program_entity_id=program,mission_status='HISTORICAL_UNCREWED_TEST_FLIGHT_2022_11')
  domain('registry_space_asset',asset,sid,date,asset_kind='CREW_SPACECRAFT',operational_status='OFFICIAL_PLATFORM_DESCRIPTION; VEHICLE_UNIT_NOT_IDENTIFIED')
  domain('registry_space_vehicle',vehicle,sid,date,vehicle_kind='LAUNCH_VEHICLE_FAMILY',operational_status='OFFICIAL_PLATFORM_DESCRIPTION')
  if nasa:domain('registry_space_org',nasa,sid,date,org_role='PUBLIC_SPACE_AGENCY')
 for key,name in [('kennedy','Kennedy Space Center'),('jpl','Jet Propulsion Laboratory')]:
  if key not in successful:continue
  sid,date,v=context(key);eid=ror_exact(name) or identity('NASA_PUBLIC_FACILITY',key,name,'FACILITY',sid,date,v)
  if not C.execute('SELECT 1 FROM registry_public_facility WHERE entity_id=?',(eid,)).fetchone():domain('registry_public_facility',eid,sid,date,facility_kind='PUBLIC_SPACE_RESEARCH_CENTER',public_acknowledgment_uri=successful[key]['url'])
  domain('registry_ground_facility_public',eid,sid,date,facility_entity_id=eid,service_kind='PUBLIC_NASA_CENTER; NO_OPERATIONAL_SITE_DETAILS')

if __name__=='__main__':run()
