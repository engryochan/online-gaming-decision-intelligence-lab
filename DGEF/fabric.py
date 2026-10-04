"""大秦实体织网：stdlib SQLite implementation; no network or source mutation."""
from pathlib import Path
import argparse, csv, hashlib, json, re, secrets, sqlite3, time, uuid
from datetime import datetime, timezone
from table_layout import table_category

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
VERSION='1.0.1'
WORLD=('HISTORY','REAL-TWIN','SIM','FICTION')
COSMIC=('EARTH_SURFACE','EARTH_SUBSURFACE','EARTH_OCEAN','EARTH_ATMOSPHERE','EARTH_ORBIT','CISLUNAR','LUNAR_SURFACE','SOLAR_SYSTEM','GALACTIC','EXTRAGALACTIC','VIRTUAL_LOCAL')
STATES=('VERIFIED','OBSERVED','INFERRED','CLAIMED','UNKNOWN','REDACTED','RESTRICTED_NOT_INGESTED')
def choices(xs): return '('+','.join("'"+x+"'" for x in xs)+')'
TIME="valid_from TEXT NOT NULL, valid_to TEXT, transaction_time TEXT NOT NULL, CHECK(valid_to IS NULL OR valid_to > valid_from)"
PROV="source_id TEXT NOT NULL REFERENCES registry_source(source_id), evidence_state TEXT NOT NULL CHECK(evidence_state IN "+choices(STATES)+'), '+TIME
ENTITY="entity_id TEXT NOT NULL REFERENCES registry_entity(entity_id)"
SPECS={}
def table(name,definition,zh,grain): SPECS[name]=(definition,zh,grain)
table('registry_schema_version','version TEXT PRIMARY KEY, installed_at TEXT NOT NULL, description TEXT NOT NULL','度制版本','一次schema发布')
table('cosmic_domain','domain_code TEXT PRIMARY KEY, name_zh TEXT NOT NULL','宇域','一种空间域')
table('registry_entity_type','type_code TEXT PRIMARY KEY, name_zh TEXT NOT NULL','名籍类型','一种实体类型')
table('registry_license_policy',"policy_id TEXT PRIMARY KEY, license TEXT NOT NULL, redistribution_allowed INTEGER CHECK(redistribution_allowed IN (0,1)), ml_training_allowed INTEGER CHECK(ml_training_allowed IN (0,1)), commercial_use_allowed INTEGER CHECK(commercial_use_allowed IN (0,1)), retention_rule TEXT NOT NULL, assessed_at TEXT NOT NULL",'用数许可','一个有时间的许可评估；NULL=未知')
table('registry_source',"source_id TEXT PRIMARY KEY, publisher TEXT NOT NULL, source_type TEXT NOT NULL, canonical_uri TEXT NOT NULL UNIQUE, access_class TEXT NOT NULL CHECK(access_class IN ('PUBLIC','RESTRICTED')), publication_date TEXT, retrieved_at TEXT NOT NULL, content_hash TEXT, policy_id TEXT NOT NULL REFERENCES registry_license_policy(policy_id), verification_scope TEXT NOT NULL",'证据出处','一个来源文档或可核验入口')
table('registry_dataset',"dataset_id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES registry_source(source_id), dataset_version TEXT NOT NULL, file_sha256 TEXT NOT NULL, row_count INTEGER NOT NULL CHECK(row_count>=0), imported_at TEXT NOT NULL, UNIQUE(source_id,dataset_version,file_sha256)",'资料版本','一个数据集快照')
table('registry_entity',"entity_id TEXT PRIMARY KEY CHECK(entity_id GLOB 'DUECG-EID::*'), entity_type TEXT NOT NULL REFERENCES registry_entity_type(type_code), canonical_name TEXT NOT NULL, world_domain TEXT NOT NULL CHECK(world_domain IN "+choices(WORLD)+"), status TEXT NOT NULL, "+TIME,'实体正名','一个不因改名迁址换号的实体')
table('registry_entity_alias',"alias_id TEXT PRIMARY KEY, "+ENTITY+", alias TEXT NOT NULL, language_tag TEXT NOT NULL, alias_kind TEXT NOT NULL, "+PROV+", UNIQUE(entity_id,alias,language_tag,valid_from)",'异名同籍','实体的一个有时间别名')
table('bridge_entity_external_id',"bridge_id TEXT PRIMARY KEY, "+ENTITY+", id_system TEXT NOT NULL, external_id TEXT NOT NULL, external_version TEXT NOT NULL, match_method TEXT NOT NULL, match_score REAL CHECK(match_score BETWEEN 0 AND 1), review_status TEXT NOT NULL CHECK(review_status IN ('ACCEPTED','PENDING','REJECTED')), "+PROV+", UNIQUE(id_system,external_id,external_version,valid_from)",'外号桥接','外部命名空间+版本+有效起点的映射')
table('registry_external_id',"external_key TEXT PRIMARY KEY, id_system TEXT NOT NULL, external_id TEXT NOT NULL, external_version TEXT NOT NULL, "+PROV+", UNIQUE(id_system,external_id,external_version,valid_from)",'外号目录','尚可不绑定实体的外部ID')
table('registry_entity_relation',"relation_id TEXT PRIMARY KEY, subject_entity_id TEXT NOT NULL REFERENCES registry_entity(entity_id), predicate TEXT NOT NULL, object_entity_id TEXT NOT NULL REFERENCES registry_entity(entity_id), "+PROV,'实体关系','一条有来源与双时间的有向关系')
table('registry_entity_status_history',"history_id TEXT PRIMARY KEY, "+ENTITY+", status TEXT NOT NULL, "+PROV,'沿革','一次状态时期')
table('registry_claim',"claim_id TEXT PRIMARY KEY, subject_entity_id TEXT REFERENCES registry_entity(entity_id), predicate TEXT NOT NULL, value_json TEXT NOT NULL CHECK(json_valid(value_json)), confidence REAL CHECK(confidence BETWEEN 0 AND 1), claim_status TEXT NOT NULL CHECK(claim_status IN "+choices(STATES)+"), "+PROV,'主张账','一条可以被支持或反驳的主张')
table('registry_observation',"observation_id TEXT PRIMARY KEY, "+ENTITY+", metric_id TEXT NOT NULL, value REAL, unit TEXT NOT NULL, sample_n INTEGER CHECK(sample_n>=0), uncertainty REAL CHECK(uncertainty>=0), method_id TEXT NOT NULL, claim_id TEXT REFERENCES registry_claim(claim_id), "+PROV,'观测账','一个实体某指标的一次观测；NULL非零')
table('registry_evidence_link',"evidence_link_id TEXT PRIMARY KEY, claim_id TEXT NOT NULL REFERENCES registry_claim(claim_id), source_id TEXT NOT NULL REFERENCES registry_source(source_id), observation_id TEXT REFERENCES registry_observation(observation_id), direction TEXT NOT NULL CHECK(direction IN ('SUPPORTS','CONTRADICTS','CONTEXT')), locator TEXT NOT NULL, transaction_time TEXT NOT NULL",'互证账','主张与证据的一条对应')
table('registry_spatial_frame',"frame_id TEXT PRIMARY KEY, cosmic_domain TEXT NOT NULL REFERENCES cosmic_domain(domain_code), center_name TEXT NOT NULL, axis_definition TEXT NOT NULL, position_unit TEXT NOT NULL, velocity_unit TEXT, reference_uri TEXT NOT NULL",'时空度制','一个明确中心轴和单位的参考系')
table('registry_entity_location',"location_observation_id TEXT PRIMARY KEY, "+ENTITY+", cosmic_domain TEXT NOT NULL REFERENCES cosmic_domain(domain_code), spatial_frame TEXT NOT NULL REFERENCES registry_spatial_frame(frame_id), central_body TEXT NOT NULL, epoch TEXT NOT NULL, time_scale TEXT NOT NULL CHECK(time_scale IN ('UTC','TAI','TT','TDB','TCB','SIM_TIME')), geometry_ref TEXT, x REAL, y REAL, z REAL, vx REAL, vy REAL, vz REAL, position_unit TEXT NOT NULL, velocity_unit TEXT, uncertainty_ref TEXT, source_solution TEXT NOT NULL, disclosure_precision TEXT NOT NULL CHECK(disclosure_precision IN ('PUBLIC_GENERAL','PUBLIC_PRECISE','REDACTED')), "+PROV+", CHECK((x IS NULL AND y IS NULL AND z IS NULL) OR (x IS NOT NULL AND y IS NOT NULL AND z IS NOT NULL)), CHECK((vx IS NULL AND vy IS NULL AND vz IS NULL) OR (vx IS NOT NULL AND vy IS NOT NULL AND vz IS NOT NULL)), CHECK(evidence_state NOT IN ('UNKNOWN','REDACTED','RESTRICTED_NOT_INGESTED') OR (x IS NULL AND y IS NULL AND z IS NULL AND geometry_ref IS NULL AND vx IS NULL AND vy IS NULL AND vz IS NULL)), CHECK(disclosure_precision != 'REDACTED' OR (x IS NULL AND y IS NULL AND z IS NULL AND geometry_ref IS NULL AND vx IS NULL AND vy IS NULL AND vz IS NULL))",'位置观测','一次参考系+历元+时标+来源解的位置')
table('registry_country_area',"entity_id TEXT PRIMARY KEY REFERENCES registry_entity(entity_id), iso_alpha2 TEXT NOT NULL UNIQUE, iso_alpha3 TEXT NOT NULL UNIQUE, iso_numeric TEXT NOT NULL, un_m49_code TEXT, calling_code TEXT, baseline_json TEXT NOT NULL CHECK(json_valid(baseline_json)), "+PROV,'国家地区籍','原country/area快照的一行，不作政治裁定')
table('registry_admin_unit',"entity_id TEXT PRIMARY KEY REFERENCES registry_entity(entity_id), subdivision_code TEXT NOT NULL UNIQUE, country_entity_id TEXT NOT NULL REFERENCES registry_country_area(entity_id), name TEXT NOT NULL, unit_type TEXT NOT NULL, parent_entity_id TEXT REFERENCES registry_admin_unit(entity_id), baseline_json TEXT NOT NULL CHECK(json_valid(baseline_json)), "+PROV,'行政区籍','原ISO3166-2快照的一行')
DOMAIN={
'registry_settlement':('聚落','settlement_kind TEXT NOT NULL, country_entity_id TEXT REFERENCES registry_country_area(entity_id)'),
'registry_legal_entity':('法人','jurisdiction_entity_id TEXT REFERENCES registry_country_area(entity_id), legal_form TEXT, registration_status TEXT NOT NULL'),
'registry_public_body':('公署','jurisdiction_entity_id TEXT REFERENCES registry_country_area(entity_id), mandate TEXT NOT NULL'),
'registry_research_org':('学府研究组织','org_kind TEXT NOT NULL, research_scope TEXT NOT NULL'),
'registry_public_facility':('公开设施','facility_kind TEXT NOT NULL, public_acknowledgment_uri TEXT NOT NULL, operator_entity_id TEXT REFERENCES registry_entity(entity_id)'),
'registry_infrastructure':('基础设施','infrastructure_kind TEXT NOT NULL, operator_entity_id TEXT REFERENCES registry_entity(entity_id)'),
'registry_person_public_role':('公开任职','person_entity_id TEXT NOT NULL REFERENCES registry_entity(entity_id), organization_entity_id TEXT NOT NULL REFERENCES registry_entity(entity_id), role_title TEXT NOT NULL'),
'registry_space_org':('宇航组织','org_role TEXT NOT NULL'),
'registry_space_program':('宇航计划','lead_entity_id TEXT REFERENCES registry_entity(entity_id), program_status TEXT NOT NULL'),
'registry_space_mission':('宇航任务','program_entity_id TEXT REFERENCES registry_entity(entity_id), mission_status TEXT NOT NULL'),
'registry_space_asset':('宇航资产','asset_kind TEXT NOT NULL, mission_entity_id TEXT REFERENCES registry_entity(entity_id), operational_status TEXT NOT NULL'),
'registry_space_vehicle':('宇航运载器','vehicle_kind TEXT NOT NULL, operational_status TEXT NOT NULL'),
'registry_ground_facility_public':('公开地面设施','facility_entity_id TEXT NOT NULL REFERENCES registry_public_facility(entity_id), service_kind TEXT NOT NULL'),
'registry_space_research_output':('宇航研究成果','title TEXT NOT NULL, doi TEXT, organization_entity_id TEXT REFERENCES registry_entity(entity_id)'),
'registry_celestial_object':('天体','object_kind TEXT NOT NULL, catalog_solution TEXT NOT NULL'),
'registry_ephemeris_solution':('星历解','frame_id TEXT NOT NULL REFERENCES registry_spatial_frame(frame_id), epoch TEXT NOT NULL, time_scale TEXT NOT NULL, position_unit TEXT NOT NULL, velocity_unit TEXT NOT NULL, solution_version TEXT NOT NULL'),
'registry_astrobiology_evidence':('生命证据','evidence_kind TEXT NOT NULL, finding_status TEXT NOT NULL, claim_id TEXT NOT NULL REFERENCES registry_claim(claim_id)'),
'registry_virtual_world':('虚拟世界','engine_name TEXT NOT NULL, engine_version TEXT NOT NULL, local_frame TEXT NOT NULL'),
'registry_virtual_entity':('虚拟实体','virtual_world_entity_id TEXT NOT NULL REFERENCES registry_virtual_world(entity_id)'),
'registry_simulation_run':('模拟运行','virtual_world_entity_id TEXT REFERENCES registry_virtual_world(entity_id), model_version TEXT NOT NULL, random_seed TEXT NOT NULL, started_at TEXT NOT NULL, finished_at TEXT'),
'registry_synthetic_population':('合成人口','simulation_run_id TEXT NOT NULL REFERENCES registry_simulation_run(record_id), population_count INTEGER NOT NULL CHECK(population_count>=0), generation_method TEXT NOT NULL'),
}
for name,(zh,cols) in DOMAIN.items():
 table(name,'record_id TEXT PRIMARY KEY, '+ENTITY+', '+cols+', '+PROV+(', UNIQUE(entity_id)' if name in ('registry_public_facility','registry_virtual_world') else ''),zh,'一个有来源、双时间的领域记录')
table('staging_service_catalogue',"catalogue_id TEXT PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, verification_status TEXT NOT NULL CHECK(verification_status IN ('V','P','U')), verification_url TEXT, verified_scope TEXT NOT NULL, raw_json TEXT NOT NULL CHECK(json_valid(raw_json)), dataset_id TEXT NOT NULL REFERENCES registry_dataset(dataset_id), candidate_entity_id TEXT REFERENCES registry_entity(entity_id), resolution_status TEXT NOT NULL CHECK(resolution_status IN ('PENDING','ACCEPTED','REJECTED')), transaction_time TEXT NOT NULL",'候选供应商','目录一行；合并品牌不得自动入法人籍')
table('registry_ingest_record',"ingest_id TEXT PRIMARY KEY, entity_id TEXT REFERENCES registry_entity(entity_id), dataset_id TEXT NOT NULL REFERENCES registry_dataset(dataset_id), external_key TEXT NOT NULL, record_payload TEXT NOT NULL CHECK(json_valid(record_payload)), transform_version TEXT NOT NULL, transaction_time TEXT NOT NULL, UNIQUE(dataset_id,external_key)",'异源原行账','原始响应内一条记录，保留取值与空缺并追溯转换版')
table('registry_coverage',"coverage_id TEXT PRIMARY KEY, country_entity_id TEXT NOT NULL REFERENCES registry_country_area(entity_id), layer TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('BASELINE','TO_RESOLVE','VERIFIED')), numerator INTEGER CHECK(numerator>=0), denominator INTEGER CHECK(denominator>=0), source_id TEXT NOT NULL REFERENCES registry_source(source_id), gap_reason TEXT NOT NULL, transaction_time TEXT NOT NULL, UNIQUE(country_entity_id,layer)",'覆盖缺口','国家地区×对象层；未知分母NULL')
table('registry_adapter_contract',"adapter_id TEXT PRIMARY KEY, id_system TEXT NOT NULL, canonical_uri TEXT NOT NULL, target_table TEXT NOT NULL, version_required INTEGER NOT NULL CHECK(version_required IN (0,1)), status TEXT NOT NULL CHECK(status IN ('LOCAL_IMPORTED','INTERFACE_ONLY','BLOCKED')), license_review TEXT NOT NULL, notes TEXT NOT NULL",'异源接榫','一个外部库接入合同；不冒充已下载')
ALIASES={'space_organization':'registry_space_org','space_program':'registry_space_program','space_mission':'registry_space_mission','space_vehicle':'registry_space_vehicle','space_object':'registry_space_asset','space_facility_public':'registry_ground_facility_public','space_research_output':'registry_space_research_output','registry_relation':'registry_entity_relation'}

def schema():
 sql=['PRAGMA foreign_keys=ON;']
 for name,(definition,_,_) in SPECS.items(): sql.append(f'CREATE TABLE IF NOT EXISTS {name} ({definition}) STRICT;')
 for name in SPECS:
  # Named indexes are stable schema artifacts, not arbitrary query interpolation.
  definition=SPECS[name][0]
  for col in ('entity_id','subject_entity_id','object_entity_id','source_id','country_entity_id','claim_id'):
   if re.search(r'\b'+col+r' TEXT',definition):sql.append(f'CREATE INDEX IF NOT EXISTS ix_{name}_{col} ON {name}({col});')
 for alias,target in ALIASES.items():sql.append(f'CREATE VIEW IF NOT EXISTS {alias} AS SELECT * FROM {target};')
 sql += ["CREATE VIEW IF NOT EXISTS v_country_admin AS SELECT c.iso_alpha2,c.iso_alpha3,c.entity_id AS country_entity_id,a.entity_id AS admin_entity_id,a.subdivision_code,a.name,a.parent_entity_id,a.evidence_state FROM registry_country_area c LEFT JOIN registry_admin_unit a ON a.country_entity_id=c.entity_id;",
 "CREATE VIEW IF NOT EXISTS v_model_features_approved AS SELECT o.observation_id,o.entity_id,o.metric_id,o.value,o.unit,o.valid_from,o.valid_to,o.transaction_time,o.source_id,o.uncertainty FROM registry_observation o JOIN registry_entity e USING(entity_id) JOIN registry_source s ON s.source_id=o.source_id JOIN registry_license_policy p ON p.policy_id=s.policy_id WHERE e.world_domain='REAL-TWIN' AND o.evidence_state IN ('VERIFIED','OBSERVED') AND o.value IS NOT NULL AND o.method_id!='UNKNOWN' AND p.ml_training_allowed=1 AND s.access_class='PUBLIC';"]
 # Validate both insert and update: a gate only on INSERT is not a gate.
 for action in ('INSERT','UPDATE'):
  sql.append(f"CREATE TRIGGER IF NOT EXISTS eid_format_{action.lower()} BEFORE {action} ON registry_entity BEGIN SELECT CASE WHEN length(NEW.entity_id)!=47 OR substr(NEW.entity_id,1,11)!='DUECG-EID::' OR substr(NEW.entity_id,26,1)!='7' OR substr(NEW.entity_id,31,1) NOT IN ('8','9','a','b') OR length(replace(substr(NEW.entity_id,12),'-',''))!=32 OR replace(substr(NEW.entity_id,12),'-','') GLOB '*[^0-9a-f]*' THEN RAISE(ABORT,'invalid UUIDv7 entity ID') END; END;")
  sql.append(f"CREATE TRIGGER IF NOT EXISTS location_frame_{action.lower()} BEFORE {action} ON registry_entity_location BEGIN SELECT CASE WHEN NOT EXISTS(SELECT 1 FROM registry_spatial_frame f WHERE f.frame_id=NEW.spatial_frame AND f.cosmic_domain=NEW.cosmic_domain AND f.center_name=NEW.central_body AND f.position_unit=NEW.position_unit AND f.velocity_unit IS NEW.velocity_unit) THEN RAISE(ABORT,'frame/domain/center/unit mismatch') END; SELECT CASE WHEN EXISTS(SELECT 1 FROM registry_entity e WHERE e.entity_id=NEW.entity_id AND ((e.world_domain IN ('SIM','FICTION') AND NEW.cosmic_domain!='VIRTUAL_LOCAL') OR (e.world_domain='REAL-TWIN' AND NEW.cosmic_domain='VIRTUAL_LOCAL'))) THEN RAISE(ABORT,'world/cosmic domain mismatch') END; END;")
 return '\n'.join(sql)+'\n'

def uuid7():
 n=(int(time.time()*1000)<<80)|(7<<76)|(secrets.randbits(12)<<64)|(2<<62)|secrets.randbits(62)
 return str(uuid.UUID(int=n))
def now():return datetime.now(timezone.utc).isoformat(timespec='microseconds')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_csv(p):
 with p.open(encoding='utf-8-sig',newline='') as stream:return list(csv.DictReader(stream))
def insert(c,table_name,**row):
 cols=','.join(row);c.execute(f"INSERT OR IGNORE INTO {table_name} ({cols}) VALUES ({','.join('?' for _ in row)})",tuple(row.values()))
def source(c,sid,publisher,uri,digest=None,scope='LOCAL_BASELINE_NOT_LIVE_VALIDATED',kind='LOCAL_DATASET'):
 insert(c,'registry_source',source_id=sid,publisher=publisher,source_type=kind,canonical_uri=uri,access_class='PUBLIC',retrieved_at=now(),content_hash=digest,policy_id='UNKNOWN',verification_scope=scope)
def entity(c,key,name,etype):
 # Persist identity mapping before reuse; never regenerate accepted IDs on re-import.
 r=c.execute('SELECT entity_id FROM bridge_entity_external_id WHERE id_system=? AND external_id=? AND external_version=?',('LOCAL_BASELINE',key,'2026-10-04')).fetchone()
 if r:return r[0]
 eid='DUECG-EID::'+uuid7()
 insert(c,'registry_entity',entity_id=eid,entity_type=etype,canonical_name=name,world_domain='REAL-TWIN',status='BASELINE',valid_from='2026-10-04',transaction_time=now())
 insert(c,'bridge_entity_external_id',bridge_id=uuid7(),entity_id=eid,id_system='LOCAL_BASELINE',external_id=key,external_version='2026-10-04',match_method='EXACT_BASELINE_KEY',review_status='ACCEPTED',source_id='SOURCE_COUNTRY' if etype=='COUNTRY_AREA' else 'SOURCE_ADMIN',evidence_state='CLAIMED',valid_from='2026-10-04',transaction_time=now())
 return eid

def build(output):
 output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
 (HERE/'schema.sql').write_text(schema(),encoding='utf-8')
 c=sqlite3.connect(output/'dgef.sqlite');c.execute('PRAGMA foreign_keys=ON');c.executescript(schema())
 installed={r[0] for r in c.execute('SELECT version FROM registry_schema_version')}
 if installed-{'1.0.0',VERSION}:raise RuntimeError('Unknown schema version: migration required')
 inputs={'country':ROOT/'Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv','admin':ROOT/'Reference/tables/02_admin_units/registry_admin_units_iso3166_2_20261004.csv','catalogue':ROOT/'reports/2026-10-04/tables/01_services/strategy_services_registry.csv'}
 initial={k:sha(p) for k,p in inputs.items()}
 with c:
  insert(c,'registry_schema_version',version=VERSION,installed_at=now(),description='G0-G3 local baseline; model gate only, no trained NN')
  insert(c,'registry_license_policy',policy_id='UNKNOWN',license='UNKNOWN',retention_rule='REVIEW_BEFORE_EXPORT_OR_TRAINING',assessed_at=now())
  for d in COSMIC:insert(c,'cosmic_domain',domain_code=d,name_zh=d)
  for t in ('COUNTRY_AREA','ADMIN_UNIT','LEGAL_ENTITY','PUBLIC_BODY','RESEARCH_ORG','FACILITY','SPACE_ORG','PROGRAM','MISSION','ASSET','CELESTIAL_OBJECT','PERSON','VIRTUAL_WORLD','VIRTUAL_ENTITY','RESEARCH_OUTPUT','UNRESOLVED'):
   insert(c,'registry_entity_type',type_code=t,name_zh=t)
  datasets={}
  for key,p in inputs.items():
   sid='SOURCE_'+key.upper();source(c,sid,'Project baseline',p.as_uri(),initial[key])
   rows=read_csv(p)
   did=key+':'+initial[key];datasets[key]=did
   # Changed snapshots cannot silently overwrite accepted baseline attributes.
   if c.execute('SELECT 1 FROM registry_dataset WHERE source_id=? AND file_sha256!=?',(sid,initial[key])).fetchone():raise RuntimeError('Input baseline changed: explicit migration required')
   insert(c,'registry_dataset',dataset_id=did,source_id=sid,dataset_version='2026-10-04',file_sha256=initial[key],row_count=len(rows),imported_at=now())
  countries=read_csv(inputs['country']);admins=read_csv(inputs['admin'])
  if len(countries)!=249 or len(admins)!=5046:raise ValueError('Unexpected baseline size')
  country_ids={}
  for r in countries:
   eid=entity(c,'COUNTRY:'+r['iso_alpha2'],r['name_en'],'COUNTRY_AREA');country_ids[r['iso_alpha2']]=eid
   insert(c,'registry_country_area',entity_id=eid,iso_alpha2=r['iso_alpha2'],iso_alpha3=r['iso_alpha3'],iso_numeric=r['iso_numeric'],un_m49_code=r['un_m49_code'] or None,calling_code=r['e164_country_calling_code'] or None,baseline_json=json.dumps(r,ensure_ascii=False),source_id='SOURCE_COUNTRY',evidence_state='CLAIMED',valid_from=r['as_of'],transaction_time=now())
   for system,value in [('ISO_ALPHA2',r['iso_alpha2']),('ISO_ALPHA3',r['iso_alpha3']),('M49',r['un_m49_code'])]:
    if value:insert(c,'bridge_entity_external_id',bridge_id=uuid7(),entity_id=eid,id_system=system,external_id=value,external_version=r['as_of'],match_method='BASELINE_CROSSWALK',review_status='ACCEPTED',source_id='SOURCE_COUNTRY',evidence_state='CLAIMED',valid_from=r['as_of'],transaction_time=now())
   insert(c,'registry_entity_alias',alias_id=uuid7(),entity_id=eid,alias=r['name_en'],language_tag='en',alias_kind='BASELINE_NAME',source_id='SOURCE_COUNTRY',evidence_state='CLAIMED',valid_from=r['as_of'],transaction_time=now())
   for layer in ('ADMIN','LEGAL_ENTITY','PUBLIC_BODY','RESEARCH_ORG','PUBLIC_FACILITY','SPACE_ORG','SPACE_ASSET'):
    insert(c,'registry_coverage',coverage_id=uuid7(),country_entity_id=eid,layer=layer,status='BASELINE' if layer=='ADMIN' else 'TO_RESOLVE',numerator=int(r['iso3166_2_subdivision_count']) if layer=='ADMIN' else None,denominator=None,source_id='SOURCE_COUNTRY',gap_reason='LIVE_VALIDATION_REQUIRED' if layer=='ADMIN' else 'NO_EXHAUSTIVE_VERIFIABLE_DENOMINATOR',transaction_time=now())
  admin_ids={r['subdivision_code']:entity(c,'ADMIN:'+r['subdivision_code'],r['name'],'ADMIN_UNIT') for r in admins}
  for r in admins:
   insert(c,'registry_admin_unit',entity_id=admin_ids[r['subdivision_code']],subdivision_code=r['subdivision_code'],country_entity_id=country_ids[r['country_iso_alpha2']],name=r['name'],unit_type=r['type'],parent_entity_id=None,baseline_json=json.dumps(r,ensure_ascii=False),source_id='SOURCE_ADMIN',evidence_state='CLAIMED',valid_from=r['as_of'],transaction_time=now())
   insert(c,'bridge_entity_external_id',bridge_id=uuid7(),entity_id=admin_ids[r['subdivision_code']],id_system='ISO3166_2',external_id=r['subdivision_code'],external_version=r['as_of'],match_method='BASELINE_EXACT_KEY',review_status='ACCEPTED',source_id='SOURCE_ADMIN',evidence_state='CLAIMED',valid_from=r['as_of'],transaction_time=now())
  for r in admins:
   if r['parent_code']:
    parent=r['parent_code']; parent=parent if parent in admin_ids else r['country_iso_alpha2']+'-'+parent
    if parent not in admin_ids:raise ValueError('Unresolved administrative parent:'+parent)
    c.execute('UPDATE registry_admin_unit SET parent_entity_id=? WHERE entity_id=?',(admin_ids[parent],admin_ids[r['subdivision_code']]))
  for r in read_csv(inputs['catalogue']):
   insert(c,'staging_service_catalogue',catalogue_id=r['id'],name=r['name'],category=r['category'],verification_status=r['status'],verification_url=r['verification_url'] or None,verified_scope=r['verified_scope'],raw_json=json.dumps(r,ensure_ascii=False),dataset_id=datasets['catalogue'],resolution_status='PENDING',transaction_time=now())
  for r in json.loads((HERE/'verification_sources.json').read_text(encoding='utf-8')):
   sid='OFFICIAL_'+r['id'];source(c,sid,r['publisher'],r['uri'],scope=r['scope'],kind='OFFICIAL_DOCUMENT')
   claim='CLAIM_'+r['id'];insert(c,'registry_claim',claim_id=claim,predicate=r['predicate'],value_json=json.dumps(r['value'],ensure_ascii=False),claim_status=r['status'],source_id=sid,evidence_state=r['status'],valid_from=r['valid_from'],transaction_time=now())
   insert(c,'registry_evidence_link',evidence_link_id='EVIDENCE_'+r['id'],claim_id=claim,source_id=sid,direction='SUPPORTS' if r['status']=='VERIFIED' else 'CONTEXT',locator=r['scope'],transaction_time=now())
  for system,url,target in [('ISO','https://www.iso.org/iso-3166-country-codes.html','registry_country_area'),('M49','https://unstats.un.org/unsd/methodology/m49/','registry_country_area'),('SALB','https://salb.un.org/en/data','registry_admin_unit'),('GERS','https://docs.overturemaps.org/gers/stability/','bridge_entity_external_id'),('LEI','https://www.gleif.org/en/lei-data','registry_legal_entity'),('ROR','https://ror.org/','registry_research_org'),('OpenAlex','https://help.openalex.org/data/institutions/','registry_research_org'),('IAF','https://www.iafastro.org/','registry_space_org'),('JPL','https://ssd.jpl.nasa.gov/horizons/manual.html','registry_ephemeris_solution'),('NAIF','https://naif.jpl.nasa.gov/','registry_spatial_frame'),('SIMBAD','https://simbad.cds.unistra.fr/simbad/','registry_celestial_object'),('Gaia','https://gea.esac.esa.int/archive/','registry_celestial_object'),('MPC','https://minorplanetcenter.net/','registry_celestial_object'),('NASA_EXOPLANET','https://exoplanetarchive.ipac.caltech.edu/','registry_celestial_object'),('IAU','https://planetarynames.wr.usgs.gov/','registry_celestial_object')]:
   insert(c,'registry_adapter_contract',adapter_id=system,id_system=system,canonical_uri=url,target_table=target,version_required=1,status='LOCAL_IMPORTED' if system in ('ISO','M49') else 'INTERFACE_ONLY',license_review='UNKNOWN_REQUIRES_REVIEW',notes='No completeness claim; local ISO/M49 are unverified baseline crosswalks')
 assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert not c.execute('PRAGMA foreign_key_check').fetchall()
 assert initial=={k:sha(p) for k,p in inputs.items()},'Source mutation during build'
 export=c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
 csvdir=output/'tables';csvdir.mkdir(exist_ok=True)
 dictionary=[];counts={}
 for (name,) in export:
  cur=c.execute(f'SELECT * FROM {name} ORDER BY 1');rows=cur.fetchall();cols=[x[0] for x in cur.description];counts[name]=len(rows)
  category_dir=csvdir/table_category(name);category_dir.mkdir(parents=True,exist_ok=True)
  with (category_dir/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.writer(f);w.writerow(cols);w.writerows(['' if v is None else v for v in row] for row in rows)
  for col in c.execute(f'PRAGMA table_info({name})'):
   dictionary.append(dict(table=name,table_name_zh=SPECS[name][1],grain=SPECS[name][2],column=col[1],sql_type=col[2],not_null=col[3],primary_key=col[5],null_semantics='UNKNOWN_OR_NOT_APPLICABLE; NEVER_IMPUTE_ZERO',business_definition=field_definition(col[1]),example_use=SPECS[name][2]))
 with (HERE/'contracts/data_dictionary.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=dictionary[0].keys());w.writeheader();w.writerows(dictionary)
 plans=[list(r) for r in c.execute('EXPLAIN QUERY PLAN SELECT * FROM registry_admin_unit WHERE country_entity_id=?',(country_ids['CN'],))]
 report=dict(schema_version=VERSION,sqlite_version=sqlite3.sqlite_version,table_count=len(SPECS),view_count=c.execute("SELECT count(*) FROM sqlite_master WHERE type='view'").fetchone()[0],row_counts=counts,input_sha256=initial,integrity='ok',foreign_key_errors=[],query_plan_country_admin=plans,training_approved_rows=c.execute('SELECT count(*) FROM v_model_features_approved').fetchone()[0],null_csv_encoding='empty field is SQL NULL; never convert to numeric zero',external_ingestion='PUBLIC_RESPONSE_SNAPSHOTS_IMPORTED' if counts['registry_ingest_record'] else 'ONLY_LOCAL_BASELINES; OTHER_ADAPTERS_INTERFACE_ONLY')
 (output/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');c.close();return report

def field_definition(col):
 definitions={'entity_id':'永久实体根号，发号时间不代表成立时间','source_id':'可追溯证据入口外键','valid_from':'业务有效起点；快照导入不代表成立时间','valid_to':'业务有效终点，半开区间；NULL表示尚未给定终点','transaction_time':'本系统记录时间UTC，与业务有效时间分离','evidence_state':'证据状态；导入旧表不得自动升级为已查证','world_domain':'HISTORY/REAL-TWIN/SIM/FICTION，保留现行四域','cosmic_domain':'空间物理域，与世界域正交','baseline_json':'原CSV一整行逐字段保留，不自动视为真实事实','denominator':'可验证总量；未知为NULL，不能宣称覆盖100%','match_score':'实体匹配分数，仅用于人工复核，不自动合并','external_version':'外部命名空间发布版或快照日期','epoch':'位置或星历的历元，必须结合时标','value':'观测数值，未知为NULL；零必须是实际零','candidate_entity_id':'未经审核的目录行不自动进入实体正籍'}
 return definitions.get(col,col.replace('_',' ')+'；定义受所属表粒度与SQL约束限定')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(HERE/'artifacts'));args=parser.parse_args()
 print(json.dumps(build(args.output),ensure_ascii=True,indent=2))
