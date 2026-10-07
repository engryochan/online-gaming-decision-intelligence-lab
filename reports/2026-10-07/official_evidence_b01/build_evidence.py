"""Supplementary scoped evidence; preserves the B04 registry and existing UNKNOWN claims."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
TABLES=ROOT/'Reference/tables/11_official_evidence_20261007_b01'
BASE=ROOT/'Reference/tables/10_global_technology_iso249_20261006_b04'
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(folder,name,rows):
    with (folder/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists() and not TABLES.exists(),'Use a new evidence batch'
TABLES.mkdir(parents=True)
baseline=[BASE/'registry_global_organizations.csv',BASE/'registry_global_claims.csv',BASE/'registry_global_sources.csv']
manifest=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in baseline]
orgs={r['entity_id']:r for r in read(baseline[0])};claims={r['entity_id']:r for r in read(baseline[1])}
assert orgs['FRO0021']['display_name']=='Earthian AI' and orgs['FRO0022']['display_name']=='NERAI'
assert not orgs['FRO0021']['source_id'] and not orgs['FRO0022']['source_id']
sources=[dict(source_id='OEB01S01',publisher='Earthian AI',url='https://www.earthianai.com/',source_type='PROVIDER_OFFICIAL_WEBSITE',read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',locator='Models; FAQ',raw_http_archive='NOT_ARCHIVED',license_state='UNKNOWN'),
 dict(source_id='OEB01S02',publisher='NERAI',url='https://neraicorp.com/',source_type='PROVIDER_OFFICIAL_WEBSITE',read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',locator='What is NERAI; Platform',raw_http_archive='NOT_ARCHIVED',license_state='UNKNOWN'),
 dict(source_id='OEB01S03',publisher='NERAI',url='https://neraicorp.com/ai-agents.html',source_type='PROVIDER_OFFICIAL_WEBSITE',read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',locator='Introduction; Six read-only tools',raw_http_archive='NOT_ARCHIVED',license_state='UNKNOWN')]
facts=[('OEB01C01','FRO0021','OEB01S01','Earthian AI 官網將自身描述為金融風險推理平台，列有地緣與技術風險模型。'),
 ('OEB01C02','FRO0021','OEB01S01','官網 Models 列有 Geopolitics Axiom-0 與 Technology Tenet-0 名稱；同頁其他位置列有不同版本名，未將它們合併為單一當前版本。'),
 ('OEB01C03','FRO0022','OEB01S02','NERAI 官網介紹地緣風險平台，描述事件資料、國別指數、預測與問答功能。'),
 ('OEB01C04','FRO0022','OEB01S03','NERAI 的 AI Agents 頁介紹 hosted MCP server 與六個唯讀工具；本批未取得密鑰或實際呼叫。')]
newclaims=[dict(claim_id=cid,entity_id=eid,source_id=sid,claim=claim,evidence_state='VERIFIED',verification_scope='PUBLIC_DESCRIPTION_ONLY',identity_link_state='DISPLAY_NAME_AND_DOMAIN_CONTEXT_MATCH_NOT_LEGAL_ENTITY_PROOF',reviewed_on='2026-10-07',performance_state='UNKNOWN',deployment_state='UNKNOWN',regulatory_state='UNKNOWN',world_frontier_rank_state='UNKNOWN',legal_domicile_state='UNKNOWN',training_permission='UNKNOWN') for cid,eid,sid,claim in facts]
tech=[('OEB01T01','FRO0021','Geopolitics Axiom-0','OEB01C02'),('OEB01T02','FRO0021','Technology Tenet-0','OEB01C02'),('OEB01T03','FRO0022','NERAI geopolitical risk platform','OEB01C03'),('OEB01T04','FRO0022','NERAI hosted MCP server','OEB01C04')]
products=[dict(technology_id=tid,issuer_entity_id=eid,display_name=name,supporting_claim_id=cid,verification_scope='PUBLIC_NAMING_OR_DESCRIPTION_ONLY',version_state='NOT_RECONCILED_OR_NOT_ESTABLISHED',availability_state='NOT_INDEPENDENTLY_TESTED',performance_state='UNKNOWN',license_state='UNKNOWN') for tid,eid,name,cid in tech]
queue=[]
for r in orgs.values():
    if r['source_id']:continue
    found=r['entity_id'] in {'FRO0021','FRO0022'}
    queue.append(dict(entity_id=r['entity_id'],display_name=r['display_name'],baseline_source_id=r['source_id'],baseline_claim_state=claims[r['entity_id']]['evidence_state'],supplement_state='SCOPED_PUBLIC_DESCRIPTION_ADDED' if found else 'NOT_REVIEWED_THIS_BATCH',legal_identity='UNKNOWN',country_relationship='NOT_NEWLY_VERIFIED',required_followup='official legal registration; country relationship; independent performance and licensing evidence'))
assert len(queue)==7
write(TABLES,'registry_supplemental_sources.csv',sources);write(TABLES,'registry_supplemental_claims.csv',newclaims);write(TABLES,'registry_supplemental_technology_descriptions.csv',products);write(TABLES,'baseline_missing_source_review.csv',queue)
attempts=[dict(url='https://een.ec.europa.eu/partnering-opportunities/belgian-ai-supported-geopolitical-risk-intelligence-provider-seeks',result='403_FORBIDDEN_ON_OPEN',use='SEARCH_LEAD_ONLY_NOT_COUNTRY_OR_LEGAL_VERIFICATION')]
write(OUT,'access_attempts.csv',attempts);write(OUT,'baseline_manifest.csv',manifest)
assert {r['source_id'] for r in newclaims}<={r['source_id'] for r in sources}
assert {r['supporting_claim_id'] for r in products}<={r['claim_id'] for r in newclaims}
assert all(r['entity_id'] in orgs for r in newclaims)
for m in manifest:assert sha(ROOT/m['path'])==m['sha256']
result=dict(pass_check=True,supplemental_sources=3,supplemental_claims=4,technology_descriptions=4,baseline_missing_source_entities=7,entities_with_supplement=2,other_entities_unreviewed=5,baseline_unchanged=True,baseline_claims_not_overwritten=True,verified_scope='PUBLIC_DESCRIPTION_ONLY',new_country_relations=0,new_legal_entities=0,new_rankings=0)
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
