from pathlib import Path
import csv,json,hashlib,subprocess,math,collections,sqlite3,urllib.request,datetime,io
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/63_station_mapping_b39_20261009'
assert not (O/'validation_receipt.json').exists();T.mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if p and Path(p).suffix in ['.qmd','.md']}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipts=[]
def fetch(url,name,limit=5000000):
    r=dict(url=url,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',file='',sha256='',error='');data=None
    try:
        with urllib.request.urlopen(url,timeout=20) as response:data=response.read(limit+1);r['http_status']=response.status
        assert len(data)<=limit
        p=O/'raw'/name;p.write_bytes(data);r.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:r['error']=type(e).__name__;r['http_status']=getattr(e,'code',r['http_status']);data=None
    receipts.append(r);return data
base='https://www.ncei.noaa.gov/oa/global-historical-climatology-network/'
fetch(base+'?list-type=2&prefix=hourly/doc/','official_doc_listing.xml')
assert fetch(base+'hourly/doc/ghcnh-station-list.csv','ghcnh-station-list.csv')
assert fetch(base+'hourly/doc/ghcnh_DOCUMENTATION.pdf','ghcnh_DOCUMENTATION.pdf')
source=read(O/'raw/ghcnh-station-list.csv');full=[dict(source_row=i,**r) for i,r in enumerate(source,1)];write('registry_full_ghcnh_station_list.csv',full)
old={r['USAF']+r['WBAN']:r for r in read(R/'Reference/tables/54_weather_station_b29_20261009/registry_station_history.csv')}
ids=[r['gsod_station_id'] for r in read(R/'Reference/tables/62_ssod_schema_b38_20261009/registry_legacy_40_station_mapping_workqueue.csv')]
byicao=collections.defaultdict(list)
for r in full:
    if r['ICAO'].strip():byicao[r['ICAO'].strip()].append(r)
def distance(a,b,c,d):
    a,b,c,d=map(math.radians,[a,b,c,d]);v=math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 6371.0088*2*math.asin(min(1,math.sqrt(max(0,v))))
assert distance(0,0,0,0)==0 and 111<distance(0,0,0,1)<112
candidates=[];summary=[]
for station in ids:
    h=old[station];rs=byicao.get(h['ICAO'].strip(),[]);near=[]
    for r in rs:
        try:delta=distance(float(h['LAT']),float(h['LON']),float(r['LATITUDE']),float(r['LONGITUDE']))
        except ValueError:delta=None
        candidate=dict(gsod_station_id=station,legacy_icao=h['ICAO'],ghcn_station_id=r['GHCN_ID'],ghcnh_source_row=r['source_row'],ghcnh_icao=r['ICAO'],legacy_name=h['STATION NAME'],ghcnh_name=r['NAME'],location_difference_km=round(delta,6) if delta is not None else '',elevation_difference_m=round(float(r['ELEVATION'])-float(h['ELEV(M)']),3) if r['ELEVATION'] and h['ELEV(M)'] else '',source_iso_code=r['ISO_CODE'],evidence='EXACT_NONEMPTY_ICAO_AND_LOCATION_DIAGNOSTIC',historic_identity='HOMR_HISTORY_PENDING_NOT_PHYSICAL_CONTINUITY_PROOF')
        candidates.append(candidate)
        if delta is not None and delta<=1:near.append(candidate)
    summary.append(dict(gsod_station_id=station,icao_candidates=len(rs),candidates_within_engineering_1km=len(near),ghcn_station_id=near[0]['ghcn_station_id'] if len(near)==1 else '',state='UNIQUE_NEAR_ICAO_CANDIDATE_HISTORY_PENDING' if len(near)==1 else 'AMBIGUOUS_OR_NO_NEAR_CANDIDATE',identity_verified=False))
write('registry_40_station_candidate_summary.csv',summary);write('registry_all_exact_icao_candidates.csv',candidates)
# Candidate pipeline tests only; not an accepted crosswalk or numeric climate comparison.
selected=[];countries=set()
for r in candidates:
    s=next(s for s in summary if s['gsod_station_id']==r['gsod_station_id'])
    if s['ghcn_station_id']==r['ghcn_station_id'] and r['source_iso_code'] not in countries:
        selected.append(r);countries.add(r['source_iso_code'])
    if len(selected)==3:break
old_days=read(R/'Reference/tables/55_weather_observation_b30_20261009/registry_daily_observation_rows.csv')+read(R/'Reference/tables/58_weather_spatial_b33_20261009/registry_daily_observation_rows.csv');new=[];comparison=[]
for r in selected:
    ghcn=r['ghcn_station_id'];url='https://www.ncei.noaa.gov/oa/synoptic-summary-of-the-day/v2/access/by-year/2024/csv/SSOD_'+ghcn+'_2024.csv'
    data=fetch(url,'SSOD_'+ghcn+'_2024.csv');rs=[]
    if data:
        rs=list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
        assert len(rs[0])==31
        for i,a in enumerate(rs,1):
            flags=[]
            if a['STATION']!=ghcn:flags.append('STATION_MISMATCH')
            if datetime.date.fromisoformat(a['DATE']).year!=2024:flags.append('YEAR_MISMATCH')
            new.append(dict(candidate_gsod_station_id=r['gsod_station_id'],ghcn_station_id=ghcn,date=a['DATE'],source_row=i,source_url=url,raw_fields_json=json.dumps(a),flags_json=json.dumps(flags),identity_status='PROVISIONAL_CANDIDATE_NOT_ACCEPTED_HISTORICAL_CROSSWALK',numeric_comparison='NOT_PERFORMED_PENDING_IDENTITY_AND_MISSING_RULES'))
    olddates={a['date'] for a in old_days if a['station_id']==r['gsod_station_id']};newdates={a['DATE'] for a in rs}
    comparison.append(dict(gsod_station_id=r['gsod_station_id'],candidate_ghcn_station_id=ghcn,gsod_dates=len(olddates),ssod_dates=len(newdates),common_dates=len(olddates&newdates),gsod_only_dates=len(olddates-newdates),ssod_only_dates=len(newdates-olddates),state='CANDIDATE_DATE_COVERAGE_ONLY_NOT_IDENTITY_OR_VALUE_VALIDATION'))
write('registry_candidate_year_date_comparison.csv',comparison)
if new:write('registry_candidate_ssod_2024_daily_rows.csv',new)
write('registry_source_receipts.csv',receipts)
con=sqlite3.connect(T/'station_mapping_b39.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert len(summary)==40 and all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
stats=dict(official_station_rows=len(full),legacy_station_rows=40,exact_icao_candidate_rows=len(candidates),unique_near_candidates=sum(bool(r['ghcn_station_id']) for r in summary),accepted_historical_crosswalks=0,sample_attempts=len(selected),sample_rows=len(new),sample_flagged_rows=sum(bool(json.loads(r['flags_json'])) for r in new),candidate_date_comparison=comparison,sqlite_counts=counts,protected_files_unchanged=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B39：官方GHCNh全站表與40站映射候選覆核"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 完整來源與候選規則

'''+f"保存官方GHCNh站表全部{len(full):,}行及所有原始欄位，來源行號可追溯；重新下載官方版本1.1.0說明。40個既有GSOD站依非空ICAO精確對照，取得{len(candidates)}條候選，其中{stats['unique_near_candidates']}站只有一個1公里內候選。1公里是工程診斷參數，不是NOAA認證門檻。"+'''

官方文件說明GHCN識別碼含來源國碼與網絡碼，國碼前綴不直接等於ISO；站表ISO_CODE另欄保留，不機械從站號取ISO。US W網絡與WBAN、I網絡與ICAO的編碼規則也不能替代所有站點的歷史連續性證據。ICAO與坐標對照只支持候選，不證明搬遷、合併或重編前後完全同一物理站。

## 同年候選管線測試

'''+f"從唯一近距離候選按來源ISO_CODE分散選3站，嘗試取得2024 SSOD原檔，保存{len(new):,}行。只比較來源日期集合，不比較氣象量或推導模型誤差；尚無已接受的歷史crosswalk。"+'''

此採樣不是全球或三國氣候代表性測試；31欄schema與站號／年份檢查只是管線驗收。新版疑似缺值及125筆舊風速衝突維持扣留。HOMR歷史識別碼、搬遷及當期時段仍待正式核對。

## 可追溯交付

[全站表](tables/63_station_mapping_b39_20261009/registry_full_ghcnh_station_list.csv)、[40站摘要](tables/63_station_mapping_b39_20261009/registry_40_station_candidate_summary.csv)、[全部ICAO候選](tables/63_station_mapping_b39_20261009/registry_all_exact_icao_candidates.csv)、[同年日期對照](tables/63_station_mapping_b39_20261009/registry_candidate_year_date_comparison.csv)、[原欄位日摘要](tables/63_station_mapping_b39_20261009/registry_candidate_ssod_2024_daily_rows.csv)、[來源收據](tables/63_station_mapping_b39_20261009/registry_source_receipts.csv)、[SQLite](tables/63_station_mapping_b39_20261009/station_mapping_b39.sqlite)。

[官方站表](https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/doc/ghcnh-station-list.csv)與[站表格式](https://www.ncei.noaa.gov/oa/global-historical-climatology-network/hourly/doc/ghcnh_DOCUMENTATION.pdf)分別保存指紋；完整站表不等於全部站點均有2024觀測。下一步核HOMR歷史識別碼與候選冲突，再決定接受哪些crosswalk。其他全球、金融、授權與歷史未完成清單保留，SDG业务分析凍結，Untitled不恢復；舊報告及資料不覆寫。
'''
(R/'Reference/Station_Mapping_B39_20261009.qmd').write_text(report,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:(R/n/'station_mapping_b39_20261009.md').write_text('# '+n+'｜B39\n\n完整官方GHCNh站表保存，40站用非空ICAO精確對照與位置診斷建立候選；候選≠已核歷史站點身分。三個來源地區候選2024管線測試只對日期集合，氣象量及模型指標不比較；HOMR、缺值與舊125筆風速冲突仍待核。\n\n[報告](../Reference/Station_Mapping_B39_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
