"""Study-bound published observations, not independent replication or national ranking."""
from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
TABLES=ROOT/'Reference/tables/16_official_evidence_20261007_b06'
csv.field_size_limit(16*1024*1024)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows,folder=TABLES):
    with (folder/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not TABLES.exists(),'Use a new batch'
baseline=[]
for folder in ['10_global_technology_iso249_20261006_b04','11_official_evidence_20261007_b01','12_official_evidence_20261007_b02','13_official_evidence_20261007_b03','14_official_evidence_20261007_b04','15_official_evidence_20261007_b05']:
    baseline.extend((ROOT/'Reference/tables'/folder).glob('*.csv'))
manifest=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)) for p in baseline]
TABLES.mkdir(parents=True)
sources=[dict(source_id='OEB06S01',publisher='JAMA Neurology',url='https://jamanetwork.com/journals/jamaneurology/fullarticle/2799839',source_type='PEER_REVIEWED_ORIGINAL_STUDY',locator='Abstract; Results; Table 2; Computer Control; Funding',published_on='2023-01-09',read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',raw_http_archive='NOT_ARCHIVED',training_permission='UNKNOWN_NOT_GRANTED'),dict(source_id='OEB06S02',publisher='JAMA Neurology',url='https://jamanetwork.com/journals/jamaneurology/fullarticle/2802981',source_type='PUBLISHER_CORRECTION',locator='Error in Figure 3',published_on='2023-03-27',read_on='2026-10-07',access_state='WEB_TOOL_TEXT_READ',raw_http_archive='NOT_ARCHIVED',training_permission='UNKNOWN_NOT_GRANTED')]
facts=[('OEB06C01','OEB06S01','SWITCH 為單中心前瞻性首次人體研究；入組5人、植入及分析4人，追蹤12個月。'),('OEB06C02','OEB06S01','該樣本未觀察到嚴重不良事件；另報告8次輕度器件不良影響。'),('OEB06C03','OEB06S01','研究報告平均訊號頻寬233 Hz；此為電生理訊號頻率範圍，不是資訊 bits/s。'),('OEB06C04','OEB06S01','配合眼動游標的 BCI 點擊打字測試報告平均每分鐘16.6個正確字元；未當作 BCI 單獨輸入成績。'),('OEB06C05','OEB06S01','Synchron 出資並參與研究設計、資料分析及發表；此為已發表研究，非獨立重現。'),('OEB06C06','OEB06S02','期刊2023-03-27更正 Figure 3D 左圖的縱軸為0至30。')]
claims=[dict(claim_id=c,entity_id='GTO0034',source_id=s,claim=t,evidence_state='VERIFIED',verification_scope='PUBLISHER_CORRECTION' if c=='OEB06C06' else 'PUBLISHED_STUDY_REPORTED_OBSERVATION',study_id='OEB06P01',reviewed_on='2026-10-07',independent_replication_state='NOT_ESTABLISHED',performance_state='STUDY_BOUND_REPORTED_OBSERVATIONS_NOT_GENERAL_VALIDATION',regulatory_state='NOT_INFERRED_FROM_PUBLICATION',world_frontier_rank_state='UNKNOWN',training_permission='UNKNOWN_NOT_GRANTED') for c,s,t in facts]
paper=[dict(publication_id='OEB06P01',entity_id='GTO0034',study_name='SWITCH',doi='10.1001/jamaneurol.2022.4847',pmid='36622685',publication_type='PEER_REVIEWED_ORIGINAL_STUDY',nct_id_as_reported='NCT03834857',registry_current_status='UNKNOWN_NOT_READ',design='SINGLE_CENTER_PROSPECTIVE_FIRST_IN_HUMAN',country_context='AU_STUDY_SITE_NOT_NATIONAL_CAPABILITY',funding='SYNCHRON',sponsor_role='DESIGN_DATA_ANALYSIS_MANUSCRIPT_PUBLICATION_INVOLVEMENT',independent_replication='NOT_ESTABLISHED',correction_doi='10.1001/jamaneurol.2023.0594',correction_date='2023-03-27',source_id='OEB06S01',correction_source_id='OEB06S02',license_state='UNKNOWN_NOT_TRAINING_AUTHORIZATION')]
values=[('enrolled',5,'participants','UNKNOWN','ENROLLED_COHORT','OEB06C01'),('implanted_analyzed',4,'participants','UNKNOWN','IMPLANTED_ANALYSIS_COHORT','OEB06C01'),('followup',12,'months','UNKNOWN','FOUR_IMPLANTED_PARTICIPANTS','OEB06C01'),('serious_adverse_events',0,'events','UNKNOWN','FOUR_PARTICIPANTS_12_MONTH_STUDY_NOT_ZERO_RISK','OEB06C02'),('mild_adverse_device_effects',8,'events','UNKNOWN','FOUR_PARTICIPANTS_12_MONTH_STUDY','OEB06C02'),('signal_bandwidth_mean',233,'Hz',16,'SIGNAL_FREQUENCY_BANDWIDTH_NOT_INFORMATION_RATE','OEB06C03'),('correct_characters_per_minute_mean',16.6,'correct_characters/minute',5.6,'BCI_CLICK_PLUS_EYE_TRACKING_CURSOR','OEB06C04')]
metrics=[dict(metric_id=f'OEB06M{i:02}',publication_id='OEB06P01',entity_id='GTO0034',metric_name=n,value=v,unit=u,standard_deviation=sd,context=k,statistic='MEAN' if n.endswith('_mean') else 'COUNT_OR_DURATION',supporting_claim_id=c,evidence_state='VERIFIED',verification_scope='PUBLISHED_STUDY_REPORTED_OBSERVATION',information_rate_bits_per_second='UNKNOWN_NOT_DERIVED') for i,(n,v,u,sd,k,c) in enumerate(values,1)]
attempts=[dict(url=u,result=k,use='DISCOVERY_LEAD_NOT_VERIFIED_PAPER_CONTENT') for u,k in [('https://pmc.ncbi.nlm.nih.gov/articles/PMC9857731/','BROWSER_CHECK_PAGE'),('https://www.medrxiv.org/content/10.1101/2025.09.19.25335897v1.full','403_FORBIDDEN'),('https://pubmed.ncbi.nlm.nih.gov/41040697/','WEB_TOOL_INTERNAL_ERROR'),('https://www.hunterschone.com/_files/ugd/93dcee_f576ba00acfb4b349752a88d452518bc.pdf','WEB_TOOL_INTERNAL_ERROR')]]
write('registry_supplemental_sources.csv',sources);write('registry_supplemental_claims.csv',claims);write('registry_neuro_publications.csv',paper);write('registry_study_metrics.csv',metrics);write('baseline_manifest.csv',manifest,OUT);write('access_attempts.csv',attempts,OUT)
assert len({r['metric_id'] for r in metrics})==7
assert {r['supporting_claim_id'] for r in metrics}<={r['claim_id'] for r in claims}
assert {r['source_id'] for r in claims}<={r['source_id'] for r in sources}
assert all(r['information_rate_bits_per_second']=='UNKNOWN_NOT_DERIVED' for r in metrics)
for r in manifest:assert sha(ROOT/r['path'])==r['sha256']
result=dict(pass_check=True,sources=2,claims=6,publications=1,metrics=7,corrections=1,source_files_unchanged=True,no_bandwidth_to_information_rate_conversion=True,no_eye_tracking_result_as_bci_only=True,no_country_capability_or_regulatory_claims=True,other_paper_not_verified=True)
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
