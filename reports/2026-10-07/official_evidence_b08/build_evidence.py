"""TMS device-specific regulatory decisions; no family-wide or national inference."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
TABLES=ROOT/'Reference/tables/18_official_evidence_20261007_b08'
csv.field_size_limit(16*1024*1024)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows,folder=TABLES):
    with (folder/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not TABLES.exists(),'Use another batch'
baseline=[]
for folder in ['10_global_technology_iso249_20261006_b04','11_official_evidence_20261007_b01','12_official_evidence_20261007_b02','13_official_evidence_20261007_b03','14_official_evidence_20261007_b04','15_official_evidence_20261007_b05','16_official_evidence_20261007_b06','17_official_evidence_20261007_b07']:
    baseline.extend((ROOT/'Reference/tables'/folder).glob('*.csv'))
manifest=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in baseline]
TABLES.mkdir(parents=True)
pages=[('OEB08S01','https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?id=K183303','FDA_DATABASE','Decision Date; Device Name'),('OEB08S02','https://www.accessdata.fda.gov/cdrh_docs/pdf18/K183303.pdf','FDA_LETTER_INDICATIONS_AND_APPLICANT_SUMMARY','PDF pp.1,3,5'),('OEB08S03','https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K200957','FDA_DATABASE','Decision Date; Device Name'),('OEB08S04','https://www.accessdata.fda.gov/cdrh_docs/pdf20/K200957.pdf','FDA_LETTER_INDICATIONS_AND_APPLICANT_SUMMARY','Device Description; Indications for Use; PDF p.6')]
sources=[dict(source_id=s,publisher='FDA (PDF includes applicant-supplied summary)',url=u,source_type=k,locator=l,read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',raw_http_archive='NOT_ARCHIVED',training_permission='UNKNOWN') for s,u,k,l in pages]
facts=[('OEB08C01','OEB08S01','FDA K183303 記錄 Brainsway Deep TMS System，申請人 Brainsway, Ltd.，2019-03-08 作出實質等同決定。','REGULATOR_DEVICE_SPECIFIC_DECISION'),('OEB08C02','OEB08S02','K183303 適用範圍為成人強迫症的輔助治療。','REGULATOR_DEVICE_SPECIFIC_INDICATIONS'),('OEB08C03','OEB08S03','FDA K200957 記錄同展示名器件，2020-08-21 作出實質等同決定；與 OCD 決定分開登記。','REGULATOR_DEVICE_SPECIFIC_DECISION'),('OEB08C04','OEB08S04','K200957 適用範圍為成人短期戒菸的輔助。','REGULATOR_DEVICE_SPECIFIC_INDICATIONS'),('OEB08C05','OEB08S02','申請人摘要描述 Deep TMS 為鄰近頭皮線圈提供的非侵入式磁刺激。','REGULATOR_HOSTED_APPLICANT_DEVICE_DESCRIPTION')]
claims=[dict(claim_id=c,entity_id='GTO0044',source_id=s,claim=t,evidence_state='VERIFIED',verification_scope=v,reviewed_on='2026-10-07',identity_link_state='REGULATORY_APPLICANT_DISPLAY_NAME_NOT_COMPANY_REGISTRATION',performance_state='NOT_INDEPENDENTLY_TESTED_THIS_BATCH',deployment_state='UNKNOWN',regulatory_state='SEE_DEVICE_SPECIFIC_DECISION_NOT_COMPANY_WIDE',world_frontier_rank_state='UNKNOWN',training_permission='UNKNOWN') for c,s,t,v in facts]
decisions=[dict(decision_id=f'OEB08D{i:02}',entity_id='GTO0044',applicant_name='Brainsway, Ltd.',device_display_name='Brainsway Deep TMS System',jurisdiction='US_FDA_DEVICE_REGULATION_NOT_LEGAL_DOMICILE',submission_id=k,pathway='510K',decision='SUBSTANTIALLY_EQUIVALENT',decision_date=d,indication=ind,population='ADULTS',scope='SUBMISSION_AND_LABEL_SPECIFIC',decision_claim_id=c,indication_claim_id=ic,evidence_state='VERIFIED',regulatory_history_complete='NO',current_all_product_labels='NOT_ESTABLISHED') for i,(k,d,ind,c,ic) in enumerate([('K183303','2019-03-08','ADJUNCT_FOR_TREATMENT_OF_OCD','OEB08C01','OEB08C02'),('K200957','2020-08-21','AID_IN_SHORT_TERM_SMOKING_CESSATION','OEB08C03','OEB08C04')],1)]
profiles=[dict(neuro_supplement_id=f'OEB08N{i:02}',entity_id='GTO0044',product_name='Brainsway Deep TMS System',submission_id=r['submission_id'],invasiveness='NONINVASIVE',modality='TMS',direction='STIMULATE',direction_scope='MAGNETIC_NEUROMODULATION_NOT_SEMANTIC_WRITING',brain_signal_reading='NOT_ESTABLISHED_BY_REVIEWED_DOCUMENTS',remote_neural_access='UNKNOWN_NOT_DEMONSTRATED',information_bandwidth='UNKNOWN_NOT_MEANINGFUL_AS_READOUT_SPEC',human_trial_state='NOT_REVIEWED_THIS_BATCH',clinical_phase='NOT_INFERRED_FROM_CLEARANCE',regulatory_decision_id=r['decision_id'],supporting_claim_ids=r['decision_claim_id']+';'+r['indication_claim_id']+';OEB08C05',country_capability_level='UNKNOWN') for i,r in enumerate(decisions,1)]
for name,rows in [('registry_supplemental_sources.csv',sources),('registry_supplemental_claims.csv',claims),('registry_regulatory_decisions.csv',decisions),('registry_neurotechnology_supplement.csv',profiles)]:write(name,rows)
write('baseline_manifest.csv',manifest,OUT)
assert {r['source_id'] for r in claims}<={r['source_id'] for r in sources}
ids={r['claim_id'] for r in claims}
assert all(set(r['supporting_claim_ids'].split(';'))<=ids for r in profiles)
assert len({r['submission_id'] for r in decisions})==2
for r in manifest:assert sha(ROOT/r['path'])==r['sha256']
result=dict(pass_check=True,sources=4,claims=5,regulatory_decisions=2,device_indication_profiles=2,source_files_unchanged=True,no_company_wide_clearance_inference=True,no_reading_or_semantic_writing_inference=True,no_complete_regulatory_history_claim=True,new_country_capability_levels=0)
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
