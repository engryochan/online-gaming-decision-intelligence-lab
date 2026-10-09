from pathlib import Path
import csv,json,hashlib,subprocess,sqlite3,urllib.request,datetime
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/61_source_terms_b37_20261009'
assert not (O/'validation_receipt.json').exists()
T.mkdir(exist_ok=True);(O/'raw').mkdir(exist_ok=True)
def write(n,rows):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files','-z']).decode('utf-8').split('\0') if p and Path(p).suffix in ['.qmd','.md']}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
gsod='https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00516/html';ssod='https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C01690/html'
receipts=[]
for name,url in [('gsod_metadata',gsod),('ssodv2_metadata',ssod)]:
    receipt=dict(url=url,http_status='',file='',sha256='',error='',fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        with urllib.request.urlopen(url,timeout=20) as response:data=response.read(2000001);receipt['http_status']=response.status
        assert len(data)<2000000
        p=O/'raw'/(name+'.html');p.write_bytes(data);receipt.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:receipt['error']=type(e).__name__
    receipts.append(receipt)
write('registry_official_metadata_receipts.csv',receipts)
rows=[]
def add(i,asset,layer,url,commercial,raw,derived,conditions,scope):
    rows.append(dict(audit_id=i,asset=asset,rights_layer=layer,source_url=url,review_date='2026-10-09',commercial_use= commercial,redistribute_raw=raw,redistribute_derived=derived,conditions=conditions,evidence_scope=scope,review_state='OFFICIAL_PAGE_READ_SCOPE_LIMITED',used_in_project='YES' if asset=='NOAA_GSOD' else 'CANDIDATE_OR_REFERENCE_NOT_INGESTED',blanket_clearance=False))
add('B37-01','NOAA_GSOD','DATASET_METADATA',gsod,'NOT_EXPLICITLY_ADJUDICATED_IN_METADATA','NOT_EXPLICITLY_ADJUDICATED_IN_METADATA','NOT_EXPLICITLY_ADJUDICATED_IN_METADATA','Cite dataset, subset and access date; no accuracy/completeness warranty','Specific GSOD dataset metadata; NWS page is not blanket NCEI license')
add('B37-02','NOAA_NWS_PAGES','GOVERNMENT_CONTENT','https://www.weather.gov/disclaimer','LAWFUL_PURPOSE_UNLESS_EXCEPTION','PERMITTED_UNLESS_EXCEPTION','PERMITTED_UNLESS_EXCEPTION','Identify NWS source; no endorsement, copyright claim on NWS content or modified-official representation','NWS page policy only; third-party material separately licensed')
add('B37-03','OPEN_METEO','FREE_API_SERVICE','https://open-meteo.com/en/terms','NOT_PERMITTED_ON_FREE_SERVICE','SEPARATE_DATA_LICENSE','SEPARATE_DATA_LICENSE','Noncommercial only; current per-day/hour/minute limits; paid plan needed for commercial service use','API service contract distinct from data copyright')
add('B37-04','OPEN_METEO','API_DATA','https://open-meteo.com/en/licence','CC_BY_4_0_SUBJECT_TO_SERVICE_ACCESS_TERMS','CC_BY_4_0','CC_BY_4_0','Credit, license link, changes indicated; no endorsement','Provider data license statement; upstream dataset terms require product-specific review')
add('B37-05','OPEN_METEO','SOFTWARE','https://open-meteo.com/en/licence','AGPL_V3_OR_LATER_COMPLIANCE_REQUIRED','SOURCE_LICENSE_APPLIES','SOURCE_LICENSE_APPLIES','Review exact software license and deployment before code reuse','Data license does not license software or trademarks')
add('B37-06','COPERNICUS_SENTINEL','DATA','https://dataspace.copernicus.eu/terms-and-conditions','FREE_FULL_OPEN_SUBJECT_TO_LEGAL_NOTICE','CHECK_SENTINEL_LEGAL_NOTICE','CHECK_SENTINEL_LEGAL_NOTICE','Portal points to separate Sentinel data legal notice; detailed adjudication pending','Sentinel data distinct from website content')
add('B37-07','COPERNICUS_PORTAL_OTHER_CONTENT','WEBSITE_CONTENT','https://dataspace.copernicus.eu/terms-and-conditions','NONCOMMERCIAL_PERMISSION_ONLY','NO_GENERAL_RESALE_REDISTRIBUTION_GRANT','NO_GENERAL_DERIVATIVE_GRANT','Credit and content ownership restrictions','Does not describe Sentinel dataset license; no portal raw copy published')
add('B37-08','NOAA_SSODV2','DATASET_METADATA',ssod,'NOT_EXPLICITLY_ADJUDICATED_IN_METADATA','NOT_EXPLICITLY_ADJUDICATED_IN_METADATA','NOT_EXPLICITLY_ADJUDICATED_IN_METADATA','Cite version/subset/access; metadata DOI placeholder not valid DOI; fitness responsibility','SSODv2 metadata, not all NOAA datasets')
write('registry_license_scope_audit_b37.csv',rows)
versions=[dict(dataset='GSOD',identifier='gov.noaa.ncdc:C00516',source_url=gsod,upstream='ISD_ISH',role='LEGACY_REPRODUCTION_BATCHES_PRESERVED',publication='UNKNOWN_IN_METADATA',citation_issue='No DOI fabricated',ingestion='B30_B33_STATION_SAMPLES'),dict(dataset='SSODv2',identifier='gov.noaa.ncdc:C01690',source_url=ssod,upstream='GHCNh',role='SUCCESSOR_PRIMARY_RESEARCH_CANDIDATE_PENDING_SCHEMA_VALIDATION',publication='2026-03-25',citation_issue='Metadata https://doi.org/DOI is unresolved placeholder',ingestion='METADATA_ONLY_NO_OBSERVATIONS')]
write('registry_weather_dataset_version_transition.csv',versions)
tasks=[dict(task_id='B37-M'+str(i),task=v,status='PENDING',acceptance=a) for i,(v,a) in enumerate([('Read SSODv2 format-specific documentation','Versioned units, sentinels, attributes, timing and station identifiers'),('Map 40 existing GSOD sample station identifiers to SSODv2','No presumed identity from matching strings'),('Acquire matched-year authorized small sample','Per-file receipts and raw row/schema counts'),('Compare old/new station-date overlap and values','Preserve both versions; report differences, not silently overwrite'),('Resolve dataset-specific rights and citation DOI','No blanket government-site or placeholder DOI clearance'),('Review 125 legacy MXSPD conflicts','Keep numeric analysis withheld until format-specific authoritative evidence')],1)]
write('registry_migration_and_rights_workqueue.csv',tasks)
con=sqlite3.connect(T/'source_terms_b37.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=list(csv.DictReader(p.open(encoding='utf-8-sig')));keys=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
(O/'validation_receipt.json').write_text(json.dumps(dict(license_scope_rows=8,dataset_versions=2,pending_migration_tasks=6,sqlite_counts=counts,old_qmd_md_preserved=True,missing_34_row_license_csv_not_claimed_recovered=True,new_ssod_observation_files=0,global_complete=False),indent=2)+'\n',encoding='utf-8')
report='''---
title: "B37：來源授權分層及GSOD／SSODv2版本更新"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 版本更新影響

[NOAA SSODv2官方元資料](https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C01690/html)確認SSODv2繼承GSOD，來源改為GHCNh；發布日期2026-03-25。官方將舊GSOD定位為重現舊研究的版本，而非主要新研究資料集。本項目B30至B36既有GSOD原件、規則及報告均保留，尚未取得SSODv2觀測，不能宣稱已遷移。新研究先核新版格式與站號映射，不再以舊版可下載當作最新版本證明。元資料引用中的DOI仍是佔位符，本輪未填造DOI。

## 授權分層核查

本輪另建8條資料／服務／軟體／網站內容核查，不宣稱找回正文所述的34條授權CSV。已讀官方頁面與尚待核的產品使用範圍分欄；UNKNOWN不等於准許或禁止。

[Open-Meteo條款](https://open-meteo.com/en/terms)將免費API服務限於非商業用途；[資料／程式授權頁](https://open-meteo.com/en/licence)分別列CC BY 4.0與AGPLv3或後續版。資料再用、API存取及軟體部署是三層規則，不以一層替代全部。[Copernicus入口條款](https://dataspace.copernicus.eu/terms-and-conditions)把Sentinel資料導向獨立法律告知，網站其他內容另有限制。本輪沒有發布第三方條款網頁原件，採來源链接和有限摘要。

[GSOD產品元資料](https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00516/html)要求引用產品、子集及存取日期並說明品質責任；沒有把其他NOAA部門頁面政策當作NCEI產品完整商業清權。[NWS政策](https://www.weather.gov/disclaimer)只按其明示範圍登记，第三方材料另核。

## 交付與待辦

[8條範圍核查](tables/61_source_terms_b37_20261009/registry_license_scope_audit_b37.csv)、[2個版本關係](tables/61_source_terms_b37_20261009/registry_weather_dataset_version_transition.csv)、[6項遷移／授權工作](tables/61_source_terms_b37_20261009/registry_migration_and_rights_workqueue.csv)、[官方元資料下載收據](tables/61_source_terms_b37_20261009/registry_official_metadata_receipts.csv)、[SQLite](tables/61_source_terms_b37_20261009/source_terms_b37.sqlite)。這是條款及版本證據台帳，並非法律意見或已授權付費服務。

125筆MXSPD衝突數值分析繼續扣留；金融2608項、工商6項、分頁378項及其他全球清單仍開放。下一步讀取SSODv2正式格式說明並建立小樣本新舊對照，再決定模型輸入；不將觀測冒充預報。SDG業務分析凍結，Untitled不恢復。
'''
(R/'Reference/Source_Terms_B37_20261009.qmd').write_text(report,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:(R/n/'source_terms_b37_20261009.md').write_text('# '+n+'｜B37\n\n來源8條分層核查；SSODv2是新研究版本候選，GSOD舊批次完整保留。資料授權、API服務、軟體及网站內容分欄；未核定範圍維持UNKNOWN，未找回34條原授權CSV。6項遷移待辦、125筆風速衝突仍未結案。\n\n[報告](../Reference/Source_Terms_B37_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(dict(metadata_saved=sum(bool(r['file']) for r in receipts),rights_rows=8,pending_tasks=6)))
