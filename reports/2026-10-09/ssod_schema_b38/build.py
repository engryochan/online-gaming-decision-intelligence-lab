from pathlib import Path
import csv,json,hashlib,subprocess,datetime,urllib.request,sqlite3,collections
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/62_ssod_schema_b38_20261009'
assert not (O/'validation_receipt.json').exists()
T.mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if p and Path(p).suffix in ['.qmd','.md']}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
base='https://www.ncei.noaa.gov/oa/synoptic-summary-of-the-day/'
urls=[base+'?list-type=2&prefix=v2/doc/',base+'v2/doc/ssodv2_DOCUMENTATION.pdf',base+'v2/access/by-year/2023/ssod_USW00003812_2023.csv',base+'?list-type=2&prefix=v2/access/by-year/2023/csv/SSOD_USW00003812',base+'v2/access/by-year/2023/csv/SSOD_USW00003812_2023.csv']
receipts=[]
for i,u in enumerate(urls):
    r=dict(url=u,time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',file='',sha256='',error='')
    try:
        with urllib.request.urlopen(u,timeout=15) as response:b=response.read(2000001);r['http_status']=response.status
        assert len(b)<2000000
        name=['documentation_listing.xml','ssodv2_DOCUMENTATION.pdf','example_original.csv','sample_listing.xml','SSOD_USW00003812_2023.csv'][i];p=O/'raw'/name;p.write_bytes(b);r.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(b).hexdigest())
    except Exception as e:r['error']=type(e).__name__;r['http_status']=getattr(e,'code',r['http_status'])
    receipts.append(r)
write('registry_source_receipts.csv',receipts)
assert receipts[1]['file'] and receipts[4]['file']
sample=read(O/'raw/SSOD_USW00003812_2023.csv');keys=list(sample[0]);assert len(keys)==31
from pypdf import PdfReader
pdf=PdfReader(O/'raw/ssodv2_DOCUMENTATION.pdf');text='\n'.join(p.extract_text() for p in pdf.pages)
(O/'raw/ssodv2_DOCUMENTATION.txt').write_text(text,encoding='utf-8')
units={'mean_temperature':'C','mean_dew_point_temperature':'C','mean_sea_level_pressure':'hPa','mean_station_level_pressure':'hPa','mean_visibility':'km','mean_wind_speed':'m/s','max_wind_speed':'m/s','max_wind_gust':'m/s','max_temperature':'C','min_temperature':'UNIT_NOT_EXPLICIT_IN_ITS_ENTRY_REVIEW','total_precipitation':'mm','snow_depth':'mm'}
schema=[dict(column_number=i,field=k,unit=units.get(k,'IDENTIFIER_METADATA_OR_ATTRIBUTE'),document_field_present=k in text,missing_definition='NOT_EXPLICITLY_FOUND_IN_DOCUMENT',unit_scope='ENTRY_READ' if k in units and k!='min_temperature' else 'REVIEW_OR_NOT_MEASUREMENT',version='SSOD_2.0.0') for i,k in enumerate(keys,1)]
assert all(r['document_field_present'] for r in schema);write('registry_ssodv2_31_column_schema.csv',schema)
days=[];suspect=[]
for n,r in enumerate(sample,1):
    d=datetime.date.fromisoformat(r['DATE']);flags=[]
    if d.year!=2023 or [d.year,d.month,d.day]!=[int(r[x]) for x in ['Year','Month','Day']]:flags.append('DATE_COMPONENT_REVIEW')
    if r['STATION']!='USW00003812':flags.append('STATION_REVIEW')
    days.append(dict(source_url=urls[4],source_row=n,station_id=r['STATION'],date=r['DATE'],raw_fields_json=json.dumps(r),flags_json=json.dumps(flags),numeric_analysis='SCHEMA_TEST_ONLY_NOT_APPROVED_MODEL_INPUT'))
    for k in units:
        if r[k].strip()=='-9999.9':suspect.append(dict(station_id=r['STATION'],date=r['DATE'],field=k,raw_value=r[k],assessment='OBSERVED_SUSPECTED_MISSING_TOKEN_NO_EXPLICIT_DOCUMENT_DEFINITION',normalized_value='',action='WITHHOLD_NUMERIC_ANALYSIS'))
write('registry_ssodv2_sample_daily_rows.csv',days);write('registry_ssodv2_suspect_missing_values.csv',suspect)
legacy={r['station_id'] for r in read(R/'Reference/tables/55_weather_observation_b30_20261009/registry_daily_observation_rows.csv')}|{r['station_id'] for r in read(R/'Reference/tables/58_weather_spatial_b33_20261009/registry_daily_observation_rows.csv')};assert len(legacy)==40
write('registry_legacy_40_station_mapping_workqueue.csv',[dict(gsod_station_id=k,ghcn_station_id='',mapping_status='PENDING_OFFICIAL_CROSSWALK_OR_MULTIFIELD_IDENTITY_EVIDENCE',sample_match='NOT_ESTABLISHED') for k in sorted(legacy)])
issues=[dict(issue='DOCUMENT_EXAMPLE_URL',evidence='Original lowercase sample path HTTP404; listed /csv/SSOD_ path retrieved',state='ACCESS_PATH_CORRECTED_BY_OBJECT_LISTING'),dict(issue='SENTINEL',evidence='Observed -9999.9 in sample; PDF missing-value definition not explicit',state='OPEN_NUMERIC_HOLD'),dict(issue='DEFINITION_TEXT',evidence='Several pressure/visibility/wind entries reuse dew-point wording; min-temperature entry lacks explicit unit',state='OPEN_SOURCE_TEXT_REVIEW'),dict(issue='PRECIPITATION_ATTRIBUTE',evidence='New numeric n represents count of hourly totals; letter flags also supported',state='SCHEMA_RULE_REQUIRED_NOT_REUSE_GSOD_ONLY_LETTERS'),dict(issue='STATION_ID',evidence='GHCN identifier replaces legacy USAF/WBAN concatenation',state='40_MAPPINGS_PENDING'),dict(issue='MEAN_COUNT',evidence='Means require report in each six-hour period, not only total>=4',state='REVIEW_SAMPLING_WINDOW_RULE')]
write('registry_document_and_schema_issues.csv',issues)
con=sqlite3.connect(T/'ssod_schema_b38.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);cols=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in cols)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in cols)+')',[[r[k] for k in cols] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for name,n in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+name+'"').fetchone()[0]==n
con.close();assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
stats=dict(document_pages=len(pdf.pages),schema_columns=31,sample_days=len(days),distinct_dates=len({r['date'] for r in days}),suspect_values=len(suspect),flagged_days=sum(bool(json.loads(r['flags_json'])) for r in days),pending_station_mappings=40,sqlite_counts=counts,old_documents_preserved=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B38：SSODv2格式核對、示例採集與40站映射待辦"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 官方格式與實測

讀取SSOD 2.0.0官方PDF全部7頁，視覺核對第6頁降水標記表，確認新版使用GHCN站號、SI量測單位及UTC日；均值需四個6小時時段各有報告，不能只用總次數≥4替代。降水屬性新增小時報告數n，並保留字母標记。文件若干欄位說明有重複文字，最低溫欄位未明寫單位，均列待核。

官方PDF示例網址實測404；公開物件清單確認需csv子目錄及大寫SSOD_檔名。取得USW00003812（ASHEVILLE AP）2023完整來源檔，這是官方具名示例測試，非先前40站的新舊匹配，也非全球代表性樣本。

'''+f"樣本{len(days)}條日記錄、31欄全部與PDF欄位名對照；日期／站號旗標{stats['flagged_days']}行。出現{len(suspect)}個-9999.9值，文件未明示其缺值規則，本輪保留原值并暫停數值分析，不把觀察到的格式慣例當作正式定義。"+'''

## 可追溯交付

[來源收據](tables/62_ssod_schema_b38_20261009/registry_source_receipts.csv)、[31欄字典](tables/62_ssod_schema_b38_20261009/registry_ssodv2_31_column_schema.csv)、[完整樣本行](tables/62_ssod_schema_b38_20261009/registry_ssodv2_sample_daily_rows.csv)、[待核缺值](tables/62_ssod_schema_b38_20261009/registry_ssodv2_suspect_missing_values.csv)、[40站映射清單](tables/62_ssod_schema_b38_20261009/registry_legacy_40_station_mapping_workqueue.csv)、[格式問題](tables/62_ssod_schema_b38_20261009/registry_document_and_schema_issues.csv)、[SQLite](tables/62_ssod_schema_b38_20261009/ssod_schema_b38.sqlite)。

[官方PDF](../reports/2026-10-09/ssod_schema_b38/raw/ssodv2_DOCUMENTATION.pdf)及[實取CSV](../reports/2026-10-09/ssod_schema_b38/raw/SSOD_USW00003812_2023.csv)保留來源位元組；物件目錄是有限prefix查詢，不宣稱全目錄下載。31欄存在不是每個值正確的證明。

本輪完成格式閱讀和獨立示例管線，40站身分映射、同年新舊比較、明確缺值裁定及SSOD引用／授權仍未竣工。125筆舊GSOD風速衝突继续扣留，舊批次和使用者正文均保留。下一步核官方站號crosswalk，匹配後才取2024對照樣本；金融及其他待辦不結案，SDG業務分析仍凍結，Untitled不恢復。
'''
(R/'Reference/SSOD_Schema_B38_20261009.qmd').write_text(report,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:(R/n/'ssod_schema_b38_20261009.md').write_text('# '+n+'｜B38\n\nSSODv2官方7頁與31欄對照完成，修正示例下載路徑並取得獨立2023示例。GHCN站號、SI單位、四個6小時時段與數字降水標记皆需新規則；疑似缺值及源文問題保持待核，不推定40站匹配或全球完成。\n\n[報告](../Reference/SSOD_Schema_B38_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
