"""Institutional speech study announcement plus Crossmark correction relation."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
TABLES=ROOT/'Reference/tables/17_official_evidence_20261007_b07'
csv.field_size_limit(16*1024*1024)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows,folder=TABLES):
    with (folder/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not TABLES.exists(),'Use a new batch'
baseline=[]
for folder in ['10_global_technology_iso249_20261006_b04','11_official_evidence_20261007_b01','12_official_evidence_20261007_b02','13_official_evidence_20261007_b03','14_official_evidence_20261007_b04','15_official_evidence_20261007_b05','16_official_evidence_20261007_b06']:
    baseline.extend((ROOT/'Reference/tables'/folder).glob('*.csv'))
manifest=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in baseline]
orgs={r['entity_id']:r for r in read(ROOT/'Reference/tables/10_global_technology_iso249_20261006_b04/registry_global_organizations.csv')}
assert all('UC Davis Neuroprosthetics Lab'!=r['display_name'] for r in orgs.values())
TABLES.mkdir(parents=True)
sources=[dict(source_id='OEB07S01',publisher='UC Davis Health',url='https://health.ucdavis.edu/news/headlines/new-brain-computer-interface-allows-man-with-als-to-speak-again/2024/08',source_type='RESEARCH_INSTITUTION_OFFICIAL_ANNOUNCEMENT',published_on='2024-08-14',locator='Lab affiliation; BrainGate enrollment; Faster training, better results',read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',raw_http_archive='NOT_ARCHIVED',training_permission='UNKNOWN'),dict(source_id='OEB07S02',publisher='Crossmark / Crossref publisher-supplied metadata',url='https://crossmark.crossref.org/dialog/?doi=10.1038%2Fs41586-023-06443-4',source_type='PUBLICATION_UPDATE_METADATA',published_on='UNKNOWN_METADATA_CURRENT_READ',locator='Correction dated 2024-07-04; Change Details',read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',raw_http_archive='NOT_ARCHIVED',training_permission='UNKNOWN')]
entities=[dict(entity_id='OEB07E01',display_name='UC Davis Neuroprosthetics Lab',entity_type='UNIVERSITY_RESEARCH_UNIT',primary_domain='NEUROTECH',evidence_state='VERIFIED',verification_scope='INSTITUTION_OFFICIAL_UNIT_DESCRIPTION',legal_entity_state='NOT_SEPARATE_LEGAL_ENTITY_ESTABLISHED',country_context='US_INSTITUTION_CONTEXT_NOT_CAPABILITY',source_id='OEB07S01',world_frontier_rank_state='UNKNOWN')]
facts=[('OEB07C01','OEB07E01','OEB07S01','UC Davis Health 公告明列 Neuroprosthetics Lab 及其語音 BCI 研究。','INSTITUTION_OFFICIAL_UNIT_DESCRIPTION'),('OEB07C02','OEB07E01','OEB07S01','機構公告報告單一 ALS 參與者、四組微電極陣列及分階段詞彙準確率；正文尚未讀取。','INSTITUTION_REPORTED_STUDY_RESULTS_NOT_PAPER_VERIFICATION'),('OEB07C03','OEB07E01','OEB07S01','機構公告稱該參與者入組 BrainGate 試驗；未推定全部 BrainGate 成績。','INSTITUTION_REPORTED_TRIAL_ASSOCIATION'),('OEB07C04','GBO0036','OEB07S02','Crossmark 列 Metzger 2023 論文的2024-07-04更正與 DOI；更正全文未成功讀取。','PUBLICATION_CORRECTION_RELATION_ONLY')]
claims=[dict(claim_id=c,entity_id=e,source_id=s,claim=t,evidence_state='VERIFIED',verification_scope=v,reviewed_on='2026-10-07',performance_state='INSTITUTION_REPORTED_ONLY' if c=='OEB07C02' else 'UNKNOWN',regulatory_state='UNKNOWN',independent_replication_state='NOT_ESTABLISHED',world_frontier_rank_state='UNKNOWN',training_permission='UNKNOWN') for c,e,s,t,v in facts]
studies=[dict(study_id='OEB07P01',entity_id='OEB07E01',display_name='Card 2024 speech neuroprosthesis institutional report',doi_linked_by_institution='10.1056/NEJMoa2314132',article_full_text_state='NOT_SUCCESSFULLY_READ',participant_count=1,implant_type='INTRACORTICAL_MICROELECTRODES_INSTITUTION_DESCRIPTION',clinical_phase='UNKNOWN',nct_id='UNKNOWN_NOT_ESTABLISHED_THIS_BATCH',country_capability='UNKNOWN',source_id='OEB07S01')]
values=[('WORD_ACCURACY',99.6,'percent','FIRST_SESSION_50_WORD_VOCABULARY'),('WORD_ACCURACY',90.2,'percent','SECOND_SESSION_125000_WORD_VOCABULARY_ADDITIONAL_1_4_HOURS_TRAINING_DATA'),('WORD_ACCURACY',97.5,'percent','AFTER_CONTINUED_DATA_COLLECTION_NOT_FIRST_DAY'),('DATA_COLLECTION_SESSIONS',84,'sessions','REPORTED_STUDY_COLLECTION'),('OBSERVATION_SPAN',32,'weeks','REPORTED_STUDY_COLLECTION')]
metrics=[dict(metric_id=f'OEB07M{i:02}',study_id='OEB07P01',entity_id='OEB07E01',metric_name=n,value=v,unit=u,statistic='ANNOUNCEMENT_REPORTED',participant_count=1,conditions=k,supporting_claim_id='OEB07C02',evidence_state='VERIFIED',verification_scope='INSTITUTION_REPORTED_ONLY_NOT_PAPER_OR_REPLICATION',information_rate_bits_per_second='UNKNOWN_NOT_DERIVED') for i,(n,v,u,k) in enumerate(values,1)]
relations=[dict(relation_id='OEB07R01',entity_id='OEB07E01',related_entity_id='GTO0040',related_name='BrainGate',relationship_type='INSTITUTION_REPORTED_TRIAL_ASSOCIATION',supporting_claim_id='OEB07C03',evidence_state='VERIFIED',scope='REPORTED_PARTICIPANT_ENROLLMENT_NOT_ORGANIZATION_OWNERSHIP')]
corrections=[dict(correction_id='OEB07U01',entity_id='GBO0036',technology_id='GBT0008',original_doi='10.1038/s41586-023-06443-4',correction_doi='10.1038/s41586-024-07735-z',correction_date='2024-07-04',supporting_claim_id='OEB07C04',relation_state='VERIFIED_CROSSMARK_METADATA',correction_full_text='NOT_SUCCESSFULLY_READ',effect_on_existing_metrics='UNKNOWN_NO_AUTOMATIC_REWRITE',reviewed_on='2026-10-07')]
attempts=[dict(url=u,result=r,use='DISCOVERY_ONLY_NOT_FULL_TEXT_VERIFICATION') for u,r in [('https://www.nature.com/articles/s41586-023-06377-x','IDENTITY_PROVIDER_REDIRECT_UNAVAILABLE'),('https://www.nature.com/articles/s41586-023-06443-4','IDENTITY_PROVIDER_REDIRECT_UNAVAILABLE'),('https://www.nature.com/articles/s41586-024-07735-z','IDENTITY_PROVIDER_REDIRECT_UNAVAILABLE'),('https://www.nejm.org/doi/10.1056/NEJMoa2314132','403_FORBIDDEN'),('https://www.nejm.org/doi/full/10.1056/NEJMoa2314132','403_FORBIDDEN'),('https://pmc.ncbi.nlm.nih.gov/articles/PMC11328962/','BROWSER_CHECK_PAGE'),('https://pubmed.ncbi.nlm.nih.gov/39141853/','NO_ARTICLE_CONTENT_RETURNED'),('https://pubmed.ncbi.nlm.nih.gov/38965438/','NO_ARTICLE_CONTENT_RETURNED')]]
for name,rows in [('registry_supplemental_sources.csv',sources),('registry_supplemental_entities.csv',entities),('registry_supplemental_claims.csv',claims),('registry_neuro_study_descriptions.csv',studies),('registry_study_metrics.csv',metrics),('registry_supplemental_relationships.csv',relations),('registry_publication_corrections.csv',corrections)]:write(name,rows)
write('baseline_manifest.csv',manifest,OUT);write('access_attempts.csv',attempts,OUT)
assert {r['entity_id'] for r in claims}<=(set(orgs)|{'OEB07E01'})
assert relations[0]['related_entity_id'] in orgs
assert {r['source_id'] for r in claims}<={r['source_id'] for r in sources}
assert {r['supporting_claim_id'] for r in metrics+relations+corrections}<={r['claim_id'] for r in claims}
for r in manifest:assert sha(ROOT/r['path'])==r['sha256']
result=dict(pass_check=True,sources=2,claims=4,research_units=1,study_descriptions=1,metrics=5,trial_relationships=1,correction_relationships=1,baseline_unchanged=True,no_2023_metrics_duplicated=True,paper_and_correction_full_text_not_verified=True,new_legal_entities=0,new_country_capability_claims=0)
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
