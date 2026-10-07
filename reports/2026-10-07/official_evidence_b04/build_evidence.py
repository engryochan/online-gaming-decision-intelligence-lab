"""SPA current catalogue supplement, distinct from historical global batch B04."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
TABLES=ROOT/'Reference/tables/14_official_evidence_20261007_b04'
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows,folder=TABLES):
    with (folder/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not TABLES.exists(),'Create another batch instead of overwriting'
baseline=[]
for folder in ['10_global_technology_iso249_20261006_b04','11_official_evidence_20261007_b01','12_official_evidence_20261007_b02','13_official_evidence_20261007_b03']:
    baseline.extend((ROOT/'Reference/tables'/folder).glob('*.csv'))
baseline.append(ROOT/'reports/2026-10-07/evidence_integration/global_registry_evidence_query.sqlite')
manifest=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in baseline]
TABLES.mkdir(parents=True)
pages=[('OEB04S01','https://spa.com/our-approach/technology/','UNKNOWN','Inside Our Tech'),('OEB04S02','https://spa.com/news/spa-advances-analytics-capabilities-for-critical-national-security-missions/','2026-09-02','Advanced Analytics Lab'),('OEB04S03','https://spa.com/news/spa-australia-showcases-modeling-and-simulation-capabilities/','2024-09-16','Demonstrations using GCAM, ARCHER and AnyLogic')]
sources=[dict(source_id=s,publisher='Systems Planning & Analysis',url=u,published_on=d,locator=l,source_type='PROVIDER_OFFICIAL_WEBSITE_OR_ANNOUNCEMENT',read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',raw_http_archive='NOT_ARCHIVED',license_state='UNKNOWN') for s,u,d,l in pages]
facts=[('OEB04C01','OEB04S01','SPA 現行技術頁列出八項工具／服務名稱及用途。','PUBLIC_DESCRIPTION_ONLY'),('OEB04C02','OEB04S02','SPA 2026-09-02 公告介紹 Advanced Analytics Lab 及其分析工作環境。','PUBLIC_DESCRIPTION_ONLY'),('OEB04C03','OEB04S03','SPA 2024-09-16 公告稱澳洲團隊展示使用 GCAM、ARCHER 與 AnyLogic；使用不等同產品所有權。','HISTORICAL_PROVIDER_DEMONSTRATION_ANNOUNCEMENT')]
claims=[dict(claim_id=c,entity_id='FRO0132',source_id=s,claim=t,evidence_state='VERIFIED',verification_scope=v,provider_display_name='Systems Planning & Analysis',identity_link_state='SPA_PROVIDER_IDENTIFIED_COMPOUND_LEGACY_LABEL_UNRESOLVED',reviewed_on='2026-10-07',performance_state='UNKNOWN',deployment_state='UNKNOWN',regulatory_state='UNKNOWN',world_frontier_rank_state='UNKNOWN',training_permission='UNKNOWN') for c,s,t,v in facts]
items=[('GCAM','模擬分析工具'),('COMSTAT','排程分析軟件'),('ArcherEye','模型與任務效度評估'),('AthenaSight','協作規劃環境'),('VeracityCast','資源預測分析流程'),('SPA Red Six Mission Assurance Program','評估服務'),('SwarmInsight','評估工具集'),('NSS','海事模擬工具')]
tech=[dict(technology_id=f'OEB04T{i:02}',issuer_entity_id='FRO0132',provider_display_name='Systems Planning & Analysis',display_name=n,public_category=k,supporting_claim_id='OEB04C01',verification_scope='PUBLIC_NAMING_OR_DESCRIPTION_ONLY',legacy_entity_link_state='COMPOUND_LABEL_UNRESOLVED',version_state='NOT_ESTABLISHED',availability_state='NOT_INDEPENDENTLY_TESTED',performance_state='UNKNOWN',license_state='UNKNOWN') for i,(n,k) in enumerate(items,1)]
relations=[dict(relation_id='OEB04R01',entity_id='FRO0132',provider_display_name='Systems Planning & Analysis',related_name='Advanced Analytics Lab',relationship_type='PROVIDER_DESCRIBED_INTERNAL_LAB',supporting_claim_id='OEB04C02',evidence_state='VERIFIED',verification_scope='PUBLIC_DESCRIPTION_ONLY',legal_identity_state='NOT_SEPARATE_LEGAL_ENTITY_ESTABLISHED'),dict(relation_id='OEB04R02',entity_id='FRO0132',provider_display_name='SPA Australia',related_name='AnyLogic',relationship_type='HISTORICAL_DEMONSTRATION_USE_NOT_OWNERSHIP',supporting_claim_id='OEB04C03',evidence_state='VERIFIED',verification_scope='HISTORICAL_PROVIDER_DEMONSTRATION_ANNOUNCEMENT',legal_identity_state='NOT_ESTABLISHED')]
decision=[dict(legacy_entity_id='FRO0132',legacy_label='Simulation & Analysis Center / SPA',supported_provider_display_name='Systems Planning & Analysis',provider_evidence='OEB02C03;OEB04C01;OEB04C02;OEB04C03',simulation_center_alias_state='UNKNOWN',archer_archereye_version_equivalence='UNKNOWN',cyber_assassin_current_availability='UNKNOWN',decision='KEEP_LEGACY_LABEL;NO_LEGAL_MERGE;NO_VERSION_MERGE',reason='No reviewed primary source establishes the compound label as a formal alias; absence in reviewed pages is not proof of nonexistence')]
write('registry_supplemental_sources.csv',sources);write('registry_supplemental_claims.csv',claims);write('registry_supplemental_technology_descriptions.csv',tech);write('registry_supplemental_relationships.csv',relations);write('identity_adjudication.csv',decision);write('baseline_manifest.csv',manifest,OUT)
for rows,key in [(sources,'source_id'),(claims,'claim_id'),(tech,'technology_id'),(relations,'relation_id')]:assert len({r[key] for r in rows})==len(rows)
assert {r['source_id'] for r in claims}<={r['source_id'] for r in sources}
assert {r['supporting_claim_id'] for r in tech+relations}<={r['claim_id'] for r in claims}
assert 'AnyLogic' not in {r['display_name'] for r in tech}
for r in manifest:assert sha(ROOT/r['path'])==r['sha256']
result=dict(pass_check=True,sources=3,claims=3,technology_descriptions=8,relationships=2,identity_decisions=1,prior_batches_and_query_snapshot_unchanged=True,compound_identity_unresolved=True,no_anylogic_ownership_claim=True,no_archer_version_merge=True,new_legal_entities=0,new_country_capability_claims=0,new_rankings=0)
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
