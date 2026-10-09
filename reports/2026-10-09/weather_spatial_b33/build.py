from pathlib import Path
import csv,json,hashlib,subprocess,datetime,urllib.request,io,sqlite3,collections
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/58_weather_spatial_b33_20261009'
assert not (O/'validation_receipt.json').exists(),'Completed batch must be preserved'
T.mkdir(exist_ok=True);(O/'raw').mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
protected=[R/'Reference/Aerospace_Ecosystem_Report.qmd',R/'Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd',R/'Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd',R/'Untitled.qmd']+list(R.glob('Reference/geo_defense_space_handoff_v2_3_0*'))+list(R.glob('Reference/weather.com*.md'))
baseline={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.exists()}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),status=subprocess.check_output(['git','status','--porcelain']).decode(),protected=baseline),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
preview=read(R/'Reference/tables/57_weather_quality_b32_20261009/registry_next_spatial_sample_preview.csv');assert len(preview)==34
def fetch(r):
    url='https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2024/'+r['station_id']+'.csv'
    receipt=dict(station_id=r['station_id'],latitude_band=r['latitude_band'],longitude_band=r['longitude_band'],source_country_code=r['source_country_code'],source_url=url,fetched_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',file='',sha256='',bytes=0,error='',rows=0);rows=[]
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ResearchWeather/1.0'}),timeout=25) as response:
            data=response.read(2000001);receipt['http_status']=response.status
        assert len(data)<=2000000,'Response exceeds limit'
        p=O/'raw'/(r['station_id']+'_2024.csv');p.write_bytes(data);receipt.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
        reader=csv.DictReader(io.StringIO(data.decode('utf-8-sig')));assert {'STATION','DATE','TEMP','PRCP'}<=set(reader.fieldnames or []),'Unexpected schema'
        for n,a in enumerate(reader,1):
            flags=[]
            try:
                if datetime.date.fromisoformat(a['DATE']).year!=2024:flags.append('OUTSIDE_YEAR')
            except ValueError:flags.append('DATE_PARSE_REVIEW')
            if a['STATION']!=r['station_id']:flags.append('STATION_ID_MISMATCH')
            rows.append(dict(source_url=url,source_row=n,expected_station_id=r['station_id'],station_id=a['STATION'],date=a['DATE'],raw_fields_json=json.dumps(a,ensure_ascii=False),quality_flags_json=json.dumps(flags),conversion='RAW_SENTINELS_AND_ATTRIBUTES_PRESERVED'))
        receipt['rows']=len(rows)
    except Exception as e:
        receipt['error']=type(e).__name__;receipt['http_status']=getattr(e,'code',receipt['http_status']);rows=[];receipt['rows']=0
    return receipt,rows
receipts=[];days=[]
with ThreadPoolExecutor(max_workers=4) as pool:
    for receipt,rows in pool.map(fetch,preview):receipts.append(receipt);days.extend(rows)
write('registry_fetch_manifest.csv',receipts)
if days:write('registry_daily_observation_rows.csv',days)
checks=[];missing=[];calendar={datetime.date(2024,1,1)+datetime.timedelta(days=i) for i in range(366)}
for r in receipts:
    rs=[a for a in days if a['expected_station_id']==r['station_id']];valid=[]
    for a in rs:
        try:
            d=datetime.date.fromisoformat(a['date'])
            if d.year==2024:valid.append(d)
        except ValueError:pass
    dates=set(valid);absent=sorted(calendar-dates)
    status='FETCH_OR_PARSE_FAILED_UNKNOWN_OBSERVATION_AVAILABILITY' if r['error'] else 'ACQUIRED_SOURCE_DAILY_ROWS'
    checks.append(dict(station_id=r['station_id'],latitude_band=r['latitude_band'],longitude_band=r['longitude_band'],source_country_code=r['source_country_code'],status=status,source_rows=len(rs),distinct_valid_dates=len(dates),duplicate_valid_dates=len(valid)-len(dates),calendar_days=366,dates_not_observed_in_this_batch=len(absent),flagged_rows=sum(bool(json.loads(a['quality_flags_json'])) for a in rs),climate_representativeness='NOT_ESTABLISHED',iso_mapping='NOT_VERIFIED'))
    for d in absent:missing.append(dict(station_id=r['station_id'],date=d.isoformat(),status='BATCH_NOT_OBSERVED_AFTER_FETCH_FAILURE' if r['error'] else 'DATE_ABSENT_FROM_ACQUIRED_SOURCE_FILE',weather_value='UNKNOWN_NOT_ZERO'))
write('registry_station_availability.csv',checks)
if missing:write('registry_unobserved_calendar_dates.csv',missing)
con=sqlite3.connect(T/'weather_spatial_b33.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);q=lambda s:'"'+s.replace('"','""')+'"'
    con.execute('CREATE TABLE '+q(p.stem)+' ('+','.join(q(k)+' TEXT' for k in keys)+')');con.executemany('INSERT INTO '+q(p.stem)+' VALUES ('+','.join('?' for k in keys)+')',[[a[k] for k in keys] for a in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close()
assert sum(r['rows'] for r in receipts)==len(days)
assert sum(r['distinct_valid_dates']+r['dates_not_observed_in_this_batch'] for r in checks)==34*366
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in baseline.items())
for r in receipts:
    if r['file']:assert hashlib.sha256((R/r['file']).read_bytes()).hexdigest()==r['sha256']
stats=dict(attempted_stations=34,successful_files=sum(not bool(r['error']) for r in receipts),errors=sum(bool(r['error']) for r in receipts),source_rows=len(days),unobserved_station_dates=len(missing),flagged_rows=sum(bool(json.loads(r['quality_flags_json'])) for r in days),sqlite_counts=counts,protected_files_unchanged=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
notes={'redteam':'逐檔限制2MB、核對schema、站號與日期；失敗不填零，保留下載時間與來源雜湊。','critic':'34站是經緯網格中的確定性樣本，不能宣稱逐國覆蓋或氣候代表性。','killcritic':'34份收據與34×366站日對賬；原始欄位保留，CSV和SQLite逐表計數及完整性核查。','blindspot':'極區與海洋分布、站點運作時段、來源回補、搬遷、非等面積網格會影響比較；GSOD不是逐時資料。','blueprint':'B32預覽→B33逐站實取與缺日台帳→單位/窗口/位置覆核→持出評估；不以站史代替實際觀測。','cheatsheet':'取得檔案≠全年完整；缺日≠零天氣；FIPS≠ISO；觀測≠預報；規則分層≠隨機樣本。','actionplan':'已實取全部34個預覽站並記錄可得性。下一輪對新站套用B31單位及B32窗口位置規則，保留金融與法人待辦。'}
for n,s in notes.items():(R/n/'weather_spatial_b33_20261009.md').write_text('# '+n+'｜B33\n\n'+s+'\n\n[報告](../Reference/Weather_Spatial_B33_20261009.qmd)。\n',encoding='utf-8')
report='''---
title: "B33：全球經緯分層34站公開觀測實取與缺日台帳"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 實際取得

'''+f"接續B32全部34個預覽站，取得 {stats['successful_files']} 份2024公開日摘要檔、{len(days):,} 條來源行；下載或解析失敗 {stats['errors']} 項。逐站全年366日對賬，本批未觀測站日 {len(missing):,} 項，站號／日期旗標 {stats['flagged_rows']} 行。"+'''

## 來源與可用性

逐站網址直接指向 [NOAA NCEI GSOD年度公開目錄](https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2024/)。[官方摘要說明](https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt)的單位、哨兵值及報告窗口仍需對新站逐項套用；本批保留完整來源欄位，不填零、不推算缺日，也不產生預報能力或災害風險分數。下載SHA256只證實本地位元組身份，不是氣象真值證明。

選站是B32的30°×60°非等面積網格內按站號排序，具有ICAO及涵蓋2024的站史期間；不是隨機樣本，亦非249國逐國覆蓋。來源國碼是FIPS，不直接對接ISO。失敗表示本次未取得；空缺日期表示本檔沒有該日，不推論其他NOAA產品或其他機構沒有觀測。B30六站與所有歷史批次保留。

## 交付與後續

[逐檔收據](tables/58_weather_spatial_b33_20261009/registry_fetch_manifest.csv)、[完整日摘要行](tables/58_weather_spatial_b33_20261009/registry_daily_observation_rows.csv)、[逐站可得性](tables/58_weather_spatial_b33_20261009/registry_station_availability.csv)、[缺日台帳](tables/58_weather_spatial_b33_20261009/registry_unobserved_calendar_dates.csv)、[SQLite](tables/58_weather_spatial_b33_20261009/weather_spatial_b33.sqlite)。驗收含原件雜湊、全年日期對賬、CSV／SQL計數、資料庫完整性與保留文件指紋。

下一步將B31單位／缺值及B32窗口／位置覆核套用新站，才建立可比較指標。您新增的weather.com競爭盤點原文保留，其價格、客戶與市場數字本輪尚未外部逐項核實。SDG業務分析仍凍結；金融2608項、工商六項及其他歷史缺口未結案；全球完整度與商業收益未證实。
'''
(R/'Reference/Weather_Spatial_B33_20261009.qmd').write_text(report,encoding='utf-8');print(json.dumps(stats))
