from pathlib import Path
import csv,json,hashlib,subprocess,math,collections,sqlite3
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/57_weather_quality_b32_20261009';T.mkdir(exist_ok=True)
assert not (O/'validation_receipt.json').exists(),'Preserve completed review'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
ps=[R/'Reference/Aerospace_Ecosystem_Report.qmd',R/'Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd',R/'Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd',R/'Untitled.qmd']+list(R.glob('Reference/geo_defense_space_handoff_v2_3_0*'))
baseline={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in ps if p.exists()}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),status=subprocess.check_output(['git','status','--porcelain']).decode(),protected=baseline),indent=2)+'\n',encoding='utf-8')
history=read(R/'Reference/tables/54_weather_station_b29_20261009/registry_station_history.csv');history_byid={r['USAF']+r['WBAN']:r for r in history}
days=read(R/'Reference/tables/55_weather_observation_b30_20261009/registry_daily_observation_rows.csv')
long=read(R/'Reference/tables/56_weather_units_b31_20261009/registry_normalized_weather_values.csv')
values={(r['station_id'],r['date'],r['field']):r for r in long}
def distance(a,b,c,d):
    a,b,c,d=map(math.radians,[a,b,c,d]);v=math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 6371.0088*2*math.asin(min(1,math.sqrt(max(0,v))))
assert abs(distance(0,0,0,0))<1e-9 and 111<distance(0,0,0,1)<112
checks=[];stations=collections.defaultdict(list)
for r in days:
    station=r['station_id'];date=r['date'];raw=json.loads(r['raw_fields_json']);h=history_byid[station];flags=[];delta=''
    try:
        delta=distance(float(h['LAT']),float(h['LON']),float(raw['LATITUDE']),float(raw['LONGITUDE']))
        if delta>1:flags.append('LOCATION_DISTANCE_ABOVE_REVIEW_PARAMETER_1KM')
    except ValueError:flags.append('LOCATION_PARSE_REVIEW')
    def n(field):
        v=values[(station,date,field)]['normalized_value'];return float(v) if v else None
    mean,minimum,maximum=n('TEMP'),n('MIN'),n('MAX')
    if minimum is not None and maximum is not None and minimum>maximum:flags.append('MIN_ABOVE_MAX_WINDOW_OR_DATA_REVIEW')
    if mean is not None and minimum is not None and maximum is not None and not minimum<=mean<=maximum:flags.append('MEAN_OUTSIDE_EXTREMES_WINDOW_REVIEW')
    count=raw.get('TEMP_ATTRIBUTES','').strip()
    enough=count.isdigit() and int(count)>=4
    precip=values[(station,date,'PRCP')];attr=precip['attribute_raw'].strip();present=bool(precip['normalized_value'])
    row=dict(source_url=r['source_url'],source_row=r['source_row'],station_id=station,date=date,location_difference_km=round(delta,6) if delta!='' else '',history_station_name=h['STATION NAME'],observation_station_name=raw.get('NAME',''),name_exact_equal=h['STATION NAME']==raw.get('NAME',''),temp_source_observation_count=count,temp_analysis_status='NUMERIC_WITH_AT_LEAST_4_SOURCE_OBSERVATIONS' if mean is not None and enough else 'MISSING_OR_INSUFFICIENT_COUNT',prcp_attribute=attr,precipitation_window_status='REPORTED_24H_OR_SUMMED_24H_WINDOW_NOT_LOCAL_CALENDAR_GUARANTEE' if present and attr in ['D','F','G'] else 'INCOMPLETE_MISSING_OR_WINDOW_NOT_ESTABLISHED',flags_json=json.dumps(flags),automatic_rejection=False,local_calendar_comparability='NOT_ESTABLISHED')
    checks.append(row);stations[station].append(row)
write('registry_daily_window_location_review.csv',checks)
summary=[]
for station,rs in sorted(stations.items()):
    summary.append(dict(station_id=station,source_days=len(rs),maximum_location_difference_km=max(float(r['location_difference_km']) for r in rs if r['location_difference_km']!=''),numeric_temp_count_sufficient=sum(r['temp_analysis_status'].startswith('NUMERIC') for r in rs),precip_reported_24h_windows=sum(r['precipitation_window_status'].startswith('REPORTED') for r in rs),days_with_review_flags=sum(bool(json.loads(r['flags_json'])) for r in rs),calendar_year_days=366,unobserved_days=366-len({r['date'] for r in rs}),prediction_skill='NOT_TESTED'))
write('registry_station_window_quality_summary.csv',summary)
# Global source metadata strata, not ISO or verified observational coverage.
strata=collections.Counter();candidates=collections.defaultdict(list)
for r in history:
    try:
        lat=float(r['LAT']);lon=float(r['LON'])
        if not (-90<=lat<=90 and -180<=lon<=180) or (lat==0 and lon==0):continue
    except ValueError:continue
    key=(min(5,int((lat+90)//30)),min(5,int((lon+180)//60)));strata[key]+=1
    if r['begin_iso'] and r['begin_iso']<='2024-01-01' and r['end_iso']>='2024-12-31' and r['ICAO']:candidates[key].append(r)
coverage=[];preview=[];selected_ids=set(stations)
for a in range(6):
    for b in range(6):
        key=(a,b);coverage.append(dict(lat_min=-90+30*a,lat_max=-60+30*a,lon_min=-180+60*b,lon_max=-120+60*b,source_history_rows=strata[key],candidate_history_rows=len(candidates[key]),actual_observation_coverage='UNKNOWN'))
        rs=sorted(candidates[key],key=lambda r:(r['USAF'],r['WBAN']))
        r=next((r for r in rs if r['USAF']+r['WBAN'] not in selected_ids),None)
        if r:preview.append(dict(station_id=r['USAF']+r['WBAN'],history_row=r['source_row'],latitude_band=a,longitude_band=b,source_country_code=r['CTRY'],station_name=r['STATION NAME'],action='PREVIEW_ONLY_NOT_FETCHED',sampling='FIRST_VALID_ID_IN_30_BY_60_DEGREE_CELL_NOT_EQUAL_AREA_OR_RANDOM'))
write('registry_global_metadata_spatial_strata.csv',coverage);write('registry_next_spatial_sample_preview.csv',preview)
con=sqlite3.connect(T/'weather_quality_b32.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);q=lambda s:'"'+s.replace('"','""')+'"';con.execute('CREATE TABLE '+q(p.stem)+' ('+','.join(q(k)+' TEXT' for k in keys)+')');con.executemany('INSERT INTO '+q(p.stem)+' VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert len(checks)==2125 and len(summary)==6 and len(coverage)==36
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in baseline.items())
stats=dict(source_days=len(days),reviewed_days=len(checks),flagged_days=sum(bool(json.loads(r['flags_json'])) for r in checks),spatial_cells=36,preview_stations=len(preview),new_observation_files=0,sqlite_counts=counts,protected_files_unchanged=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
notes={'redteam':'坐標差異與極值關係旗標只觸發覆核，不自動拒收；同站不同年份搬遷/名稱别名可能合理。','critic':'至少4個平均觀測不證明全天均勻取樣；24h降水窗口不證明本地午夜日；不輸出全球能力分數。','killcritic':'2125站日完整對賬；球面距離零點/一度測試、36網格、6站摘要與SQL完整性核查。','blindspot':'站史和觀測非同時版本；座標四捨五入、站點搬遷與海拔差異可能影响；規則網格不是等面積樣本。','blueprint':'站史與觀測版本→位置/窗口核查→可分析旗標→分層選站預覽→實際取得→持出回測。','cheatsheet':'品質訊號≠錯誤；預覽≠取得；有歷史站≠有觀測；足夠次數≠均勻時間；24h窗口≠本地日。','actionplan':'已完成六站2125日的窗口位置覆核、全球36格 metadata 分層與下一輪選站預覽。下一步實取預覽站并按來源可得性記錄拒收/缺口。'}
for n,s in notes.items():(R/n/'weather_quality_b32_20261009.md').write_text('# '+n+'｜B32\n\n'+s+'\n\n[報告](../Reference/Weather_Quality_B32_20261009.qmd)。\n',encoding='utf-8')
report='''---
title: "B32：站史／觀測位置與時間窗口核查"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 實測範圍

'''+f"完整核查六站 {len(checks)} 個站日，{stats['flagged_days']} 日有覆核旗標；沒有刪除或自動拒收。另以全部站史有效坐標建立36個30度緯度×60度經度網格，展開 {len(preview)} 個下一輪站點預覽，未新增下載觀測。"+'''

## 品質窗口與參數

位置使用球面距離，半徑6371.0088km，1km是工程覆核參數而非NOAA品質標準。精度、站点搬遷或不同時點的原件可能導致差異；不同名稱不直接視為不同站。TEMP數值與源觀測次數≥4分開記錄，不能推定全天均匀報告；降水D/F/G屬24h或合計24h報告窗口，不保證本地午夜日完整，其他旗標維持待核。平均值與極值不一致可能涉及窗口，不直接判錯。

[官方GSOD格式文件](https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt)的原件已在B31保存，本輪只讀沿用。規則網格不是等面積／隨機抽樣；metadata站史數不代表可用觀測、ISO地區或全球氣候覆蓋。未產生氣候指標、災害評分或預報技能。

## 對賬交付

[逐日核查](tables/57_weather_quality_b32_20261009/registry_daily_window_location_review.csv)、[六站摘要](tables/57_weather_quality_b32_20261009/registry_station_window_quality_summary.csv)、[全球metadata分層](tables/57_weather_quality_b32_20261009/registry_global_metadata_spatial_strata.csv)、[下一輪預覽](tables/57_weather_quality_b32_20261009/registry_next_spatial_sample_preview.csv)、[SQLite](tables/57_weather_quality_b32_20261009/weather_quality_b32.sqlite)。行數及SQLite完整性、保護文件雜湊通過。使用者正在修改的Inteligent文件與Untitled.qmd均保留，排除本輪提交。金融2608項、法人六項、歷史與分頁待辦保留；SDG業務分析維持凍結，全球完整性UNKNOWN。
'''
(R/'Reference/Weather_Quality_B32_20261009.qmd').write_text(report,encoding='utf-8');print(json.dumps(stats))
