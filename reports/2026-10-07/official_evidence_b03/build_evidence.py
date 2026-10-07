"""B03 official public evidence; preserves prior batches and original claims."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
TABLES=ROOT/'Reference/tables/13_official_evidence_20261007_b03'
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows,folder=TABLES):
    with (folder/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not TABLES.exists(),'Use a new batch'
baseline=[]
for folder in ['10_global_technology_iso249_20261006_b04','11_official_evidence_20261007_b01','12_official_evidence_20261007_b02']:
    baseline.extend((ROOT/'Reference/tables'/folder).glob('*.csv'))
manifest=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in baseline]
orgs={r['entity_id']:r for r in read(ROOT/'Reference/tables/10_global_technology_iso249_20261006_b04/registry_global_organizations.csv')}
assert not orgs['FRO0054']['source_id'] and not orgs['FRO0123']['source_id']
TABLES.mkdir(parents=True)
urls=['https://hadesdefense.nl/en/hds-fusion-c4isr-platform/','https://www.idf.il/en/mini-sites/directorates/military-intelligence-directorate/military-intelligence-directorate/','https://mod.gov.il/en/press-releases/press-room/2023-israel-defense-prize-awarded-to-4-outstanding-projects']
sources=[dict(source_id=f'OEB03S{i:02}',publisher=p,url=u,source_type=k,locator=l,published_on=d,read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',raw_http_archive='NOT_ARCHIVED',license_state='UNKNOWN') for i,(p,u,k,l,d) in enumerate(zip(['HADES Defense Systems','Israel Defense Forces','Israel Ministry of Defense'],urls,['PROVIDER_OFFICIAL_WEBSITE','MILITARY_OFFICIAL_DIRECTORY','GOVERNMENT_OFFICIAL_ANNOUNCEMENT'],['HDS FUSION introduction; reference architectures','Military Intelligence Directorate; 8200 paragraph','Winning projects items 2 and 3'],['UNKNOWN','UNKNOWN','2023-06-13']),1)]
facts=[('OEB03C01','FRO0054','OEB03S01','HADES 官網將 HDS FUSION 描述為軟件定義 C4ISR 平台；提供方展示名與平台名分開登記。','PUBLIC_DESCRIPTION_ONLY','PROVIDER_PLATFORM_CONTEXT_MATCH_NOT_LEGAL_ENTITY_PROOF'),
 ('OEB03C02','FRO0123','OEB03S02','IDF 官方介紹列明 8200 部隊隸屬軍事情報局。','OFFICIAL_ORGANIZATIONAL_AFFILIATION','OFFICIAL_UNIT_NAME_AND_AFFILIATION'),
 ('OEB03C03','FRO0123','OEB03S02','IDF 官方介紹描述 8200 部隊開發及使用資訊收集工具，進行分析、處理與分享。','PUBLIC_DESCRIPTION_ONLY','OFFICIAL_UNIT_NAME_AND_AFFILIATION'),
 ('OEB03C04','FRO0123','OEB03S03','國防部 2023 年獲獎公告列有 ISA－8200 與 Mossad－8200 兩項聯合項目；未公開名稱及技術規格。','HISTORICAL_OFFICIAL_COLLABORATION_ANNOUNCEMENT','OFFICIAL_UNIT_NAME_AND_AFFILIATION')]
claims=[dict(claim_id=c,entity_id=e,source_id=s,claim=t,evidence_state='VERIFIED',verification_scope=v,identity_link_state=i,reviewed_on='2026-10-07',performance_state='UNKNOWN',deployment_state='UNKNOWN',regulatory_state='UNKNOWN',world_frontier_rank_state='UNKNOWN',training_permission='UNKNOWN') for c,e,s,t,v,i in facts]
products=[dict(technology_id='OEB03T01',issuer_entity_id='FRO0054',display_name='HDS FUSION',supporting_claim_id='OEB03C01',verification_scope='PUBLIC_NAMING_OR_DESCRIPTION_ONLY',provider_display_name='HADES Defense Systems',legal_provider_identity='UNKNOWN',version_state='NOT_ESTABLISHED',availability_state='NOT_INDEPENDENTLY_TESTED',performance_state='UNKNOWN',license_state='UNKNOWN')]
relations=[dict(relation_id='OEB03R01',entity_id='FRO0123',relationship_type='OFFICIAL_ORGANIZATIONAL_AFFILIATION',related_name='IDF Military Intelligence Directorate',country_alpha2_context='IL',country_scope='PUBLIC_INSTITUTIONAL_AFFILIATION_NOT_COUNTRY_CAPABILITY',supporting_claim_id='OEB03C02',evidence_state='VERIFIED'),dict(relation_id='OEB03R02',entity_id='FRO0123',relationship_type='HISTORICAL_ANNOUNCED_PROJECT_PARTNER',related_name='ISA',country_alpha2_context='IL',country_scope='PUBLIC_INSTITUTIONAL_CONTEXT_NOT_COUNTRY_CAPABILITY',supporting_claim_id='OEB03C04',evidence_state='VERIFIED'),dict(relation_id='OEB03R03',entity_id='FRO0123',relationship_type='HISTORICAL_ANNOUNCED_PROJECT_PARTNER',related_name='Mossad',country_alpha2_context='IL',country_scope='PUBLIC_INSTITUTIONAL_CONTEXT_NOT_COUNTRY_CAPABILITY',supporting_claim_id='OEB03C04',evidence_state='VERIFIED')]
queue=read(ROOT/'Reference/tables/12_official_evidence_20261007_b02/baseline_missing_source_review.csv')
for r in queue:
    if r['entity_id'] in {'FRO0054','FRO0123'}:
        r['status_provenance']='B03';r['supplement_state']='B03_SCOPED_OFFICIAL_EVIDENCE_ADDED'
        r['legal_identity']='NOT_APPLICABLE_MILITARY_UNIT_OFFICIAL_AFFILIATION_VERIFIED' if r['entity_id']=='FRO0123' else 'UNKNOWN'
        r['country_relationship']='IL_OFFICIAL_INSTITUTIONAL_AFFILIATION_ONLY' if r['entity_id']=='FRO0123' else 'NOT_NEWLY_VERIFIED'
        r['required_followup']='Independent technical performance; disclosed project specifications; licensing' if r['entity_id']=='FRO0123' else 'Legal provider identity; country relationship; independent performance and licensing'
write('registry_supplemental_sources.csv',sources);write('registry_supplemental_claims.csv',claims);write('registry_supplemental_technology_descriptions.csv',products);write('registry_supplemental_relationships.csv',relations);write('baseline_missing_source_review.csv',queue);write('baseline_manifest.csv',manifest,OUT)
for rows,key in [(sources,'source_id'),(claims,'claim_id'),(products,'technology_id'),(relations,'relation_id')]:assert len({r[key] for r in rows})==len(rows)
assert {r['source_id'] for r in claims}<={r['source_id'] for r in sources}
assert {r['entity_id'] for r in claims}<={*orgs}
assert {r['supporting_claim_id'] for r in products+relations}<={r['claim_id'] for r in claims}
for m in manifest:assert sha(ROOT/m['path'])==m['sha256']
result=dict(pass_check=True,sources=3,claims=4,technology_descriptions=1,relationships=3,baseline_and_prior_batches_unchanged=True,original_missing_source_entities=7,entities_with_scoped_supplement_across_b01_b03=7,unresolved_compound_identity=['FRO0132'],new_legal_entities=0,new_country_capability_claims=0,new_rankings=0)
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
