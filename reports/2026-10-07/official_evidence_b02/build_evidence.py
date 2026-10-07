"""Append-only official evidence B02; never rewrite the historical registry."""
from pathlib import Path
import csv, json, hashlib
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
TABLES=ROOT/'Reference/tables/12_official_evidence_20261007_b02'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows,folder=TABLES):
    with (folder/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not TABLES.exists(), 'Use a new batch, do not replace delivered evidence'
TABLES.mkdir(parents=True)
baseline=list((ROOT/'Reference/tables/10_global_technology_iso249_20261006_b04').glob('*.csv'))+list((ROOT/'Reference/tables/11_official_evidence_20261007_b01').glob('*.csv'))
manifest=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in baseline]
sources=[]
for sid,publisher,url,locator,date,kind in [
 ('OEB02S01','農業部智慧農業科技服務體系專區','https://www.intelligentagri.com.tw/smartagrilist/Producer/producer_more?id=4b908a0271ff4de18ad9cac05cad8c21','機構名稱、公司介紹、農業經驗','UNKNOWN','GOVERNMENT_SERVICE_DIRECTORY'),
 ('OEB02S02','Tron Future Tech','https://www.tronfuture.com/','Products; Space Tech; 中文公開聲明','UNKNOWN','PROVIDER_OFFICIAL_WEBSITE'),
 ('OEB02S03','Systems Planning & Analysis','https://spa.com/news/spa-announces-organizational-realignment-to-optimize-growth-in-key-markets/','2024 organizational realignment; Sea, Land, Air Division','2024-02-14','PROVIDER_OFFICIAL_ANNOUNCEMENT')]:
    sources.append(dict(source_id=sid,publisher=publisher,url=url,locator=locator,published_on=date,read_on='2026-10-07',source_type=kind,access_state='WEB_TOOL_TEXT_READ',raw_http_archive='NOT_ARCHIVED',license_state='UNKNOWN'))
facts=[('OEB02C01','FRO0195','OEB02S01','農業部服務名錄列出經緯航太科技股份有限公司，介紹無人飛行系統及農業影像分析服務。','DIRECTORY_NAME_CONTEXT_MATCH_NOT_LEGAL_REGISTRATION_PROOF'),
 ('OEB02C02','FRO0196','OEB02S02','創未來官網產品目錄列有雷達、感測器、太空通訊與 SAR 產品名稱。','DISPLAY_NAME_AND_DOMAIN_CONTEXT_MATCH_NOT_LEGAL_ENTITY_PROOF'),
 ('OEB02C03','FRO0132','OEB02S03','SPA 2024-02-14 公告以 Systems Planning & Analysis 展開縮寫，列有 GCAM、Cyber Assassin 及 ARCHER 技術方案。','PARTIAL_PROVIDER_PRODUCT_DISAMBIGUATION_COMPOUND_LABEL_UNRESOLVED')]
claims=[dict(claim_id=c,entity_id=e,source_id=s,claim=t,evidence_state='VERIFIED',verification_scope='PUBLIC_DESCRIPTION_ONLY',identity_link_state=i,reviewed_on='2026-10-07',performance_state='UNKNOWN',deployment_state='UNKNOWN',regulatory_state='UNKNOWN',world_frontier_rank_state='UNKNOWN',legal_domicile_state='UNKNOWN',training_permission='UNKNOWN') for c,e,s,t,i in facts]
names=[('FRO0195','無人機農業影像分析整合服務','OEB02C01')]+[('FRO0196',n,'OEB02C02') for n in ['T.Radar ER','T.Radar Pro','T.Sensor','T.Jammer','T.Cam','T.Meta','T.SpaceHub Mini','T.SpaceHub Micro','T.SAR','T.SpaceRouter']]+[('FRO0132',n,'OEB02C03') for n in ['GCAM','Cyber Assassin','ARCHER']]
products=[dict(technology_id=f'OEB02T{i:02}',issuer_entity_id=e,display_name=n,supporting_claim_id=c,verification_scope='PUBLIC_NAMING_OR_DESCRIPTION_ONLY',provider_link_state='SPA_OFFICIAL_2024_ANNOUNCEMENT_COMPOUND_ENTITY_UNRESOLVED' if e=='FRO0132' else 'PUBLIC_PAGE_CONTEXT_ONLY',version_state='NOT_ESTABLISHED',availability_state='NOT_INDEPENDENTLY_TESTED',performance_state='UNKNOWN',license_state='UNKNOWN') for i,(e,n,c) in enumerate(names,1)]
queue=read(ROOT/'Reference/tables/11_official_evidence_20261007_b01/baseline_missing_source_review.csv')
for r in queue:
    r['status_provenance']='B01_REVIEW_RETAINED'
    if r['entity_id'] in {'FRO0195','FRO0196','FRO0132'}:
        r['supplement_state']='B02_SCOPED_PUBLIC_DESCRIPTION_ADDED';r['status_provenance']='B02'
        if r['entity_id']=='FRO0132':r['required_followup']='Resolve Simulation & Analysis Center label separately; SPA abbreviation and product association only established in 2024 announcement'
attempts=[dict(url=u,result=result,use='DISCOVERY_ONLY_NOT_VERIFIED_REGISTRATION_OR_PROVIDER_CONTENT') for u,result in [('https://www.geosat.com.tw/','502_BAD_GATEWAY'),('https://www.geosat.com.tw/TW/about-us-milestones.aspx','WEB_TOOL_INTERNAL_ERROR'),('https://findbiz.nat.gov.tw/fts/company/27285850','WEB_TOOL_INTERNAL_ERROR'),('https://findbiz.nat.gov.tw/fts/company/27285850?fhl=en','403_FORBIDDEN')]]
write('registry_supplemental_sources.csv',sources);write('registry_supplemental_claims.csv',claims);write('registry_supplemental_technology_descriptions.csv',products);write('baseline_missing_source_review.csv',queue)
write('baseline_manifest.csv',manifest,OUT);write('access_attempts.csv',attempts,OUT)
assert len(queue)==7 and len(products)==14
assert {r['source_id'] for r in claims}<={r['source_id'] for r in sources}
assert {r['supporting_claim_id'] for r in products}<={r['claim_id'] for r in claims}
assert len({r['technology_id'] for r in products})==len(products)
for m in manifest:assert sha(ROOT/m['path'])==m['sha256']
(OUT/'validation.json').write_text(json.dumps(dict(pass_check=True,sources=3,claims=3,technology_descriptions=14,baseline_unchanged=True,new_country_relations=0,new_legal_entities=0,new_rankings=0,remaining_entities_without_supplement=2,compound_identity_unresolved=['FRO0132']),indent=2)+'\n',encoding='utf-8')
