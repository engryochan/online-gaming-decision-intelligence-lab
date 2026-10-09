from pathlib import Path
import csv,json,hashlib,collections,re,datetime,urllib.request,sqlite3
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/55_weather_observation_b30_20261009'
assert not (O/'validation_receipt.json').exists(),'Preserve completed batch'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    if not rs:return
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
cr=json.loads((O/'country_receipt.json').read_text());data=(O/'raw/country-list.txt').read_bytes();assert hashlib.sha256(data).hexdigest()==cr['sha256']
codes=[]
for n,line in enumerate(data.decode('utf-8-sig').splitlines(),1):
    if re.match(r'^[A-Z]{2}\s+',line):codes.append(dict(source_line=n,fips_code=line[:2],source_country_name=line[2:].strip(),iso_mapping='UNRESOLVED_NOT_STRING_EQUALITY'))
write('registry_noaa_country_dictionary.csv',codes);bycode=collections.defaultdict(list)
for r in codes:bycode[r['fips_code']].append(r['source_country_name'])
history=read(R/'Reference/tables/54_weather_station_b29_20261009/registry_station_history.csv');joined=[]
for r in history:joined.append(dict(source_row=r['source_row'],usaf=r['USAF'],wban=r['WBAN'],source_fips_code=r['CTRY'],dictionary_names_json=json.dumps(bycode.get(r['CTRY'],[])),dictionary_status='EMPTY_SOURCE_CODE' if not r['CTRY'] else ('MATCHED_SOURCE_DICTIONARY' if r['CTRY'] in bycode else 'UNRESOLVED_SOURCE_CODE'),iso_mapping='NOT_VERIFIED'))
write('registry_all_station_country_dictionary_join.csv',joined)
selected=[]
for code in ['US','UK','AS','SF','BR','JA']:
    candidates=[r for r in history if r['CTRY']==code and r['begin_iso']<='2024-01-01' and r['end_iso']>='2024-12-31' and json.loads(r['quality_flags_json'])==[] and r['ICAO']]
    candidates.sort(key=lambda r:(r['USAF'],r['WBAN']))
    if candidates:
        r=candidates[0];selected.append(dict(station_id=r['USAF']+r['WBAN'],source_country_code=code,source_country_names_json=json.dumps(bycode[code]),source_history_row=r['source_row'],station_name=r['STATION NAME'],selection='FIRST_SORTED_VALID_COORDINATE_ICAO_STATION_WITH_2024_HISTORY_INTERVAL',year=2024,url='https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2024/'+r['USAF']+r['WBAN']+'.csv'))
write('registry_observation_test_stations.csv',selected)
def fetch(r):
    out=dict(**r,http_status='',file='',sha256='',error='',bytes=0);rows=[]
    try:
        with urllib.request.urlopen(urllib.request.Request(r['url'],headers={'User-Agent':'ResearchWeather/1.0'}),timeout=20) as response:data=response.read(2000001);out['http_status']=response.status
        assert len(data)<=2000000
        p=O/'raw'/(r['station_id']+'_2024.csv');p.write_bytes(data);out.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
        import io
        for n,a in enumerate(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))),1):
            date=a.get('DATE','');flags=[]
            try:
                d=datetime.date.fromisoformat(date)
                if d.year!=2024:flags.append('OUTSIDE_SELECTED_YEAR')
            except ValueError:flags.append('DATE_PARSE_PENDING')
            if a.get('STATION')!=r['station_id']:flags.append('STATION_ID_MISMATCH')
            rows.append(dict(source_url=r['url'],source_row=n,expected_station_id=r['station_id'],station_id=a.get('STATION',''),date=date,raw_fields_json=json.dumps(a,ensure_ascii=False),quality_flags_json=json.dumps(flags),units_and_missing_value_conversion='NOT_APPLIED_RETAIN_ORIGINAL'))
    except Exception as e:out['error']=type(e).__name__
    return out,rows
receipts=[];observations=[]
with ThreadPoolExecutor(max_workers=6) as pool:
    for r,rs in pool.map(fetch,selected):receipts.append(r);observations.extend(rs)
write('observation_fetch_manifest.csv',receipts);write('registry_daily_observation_rows.csv',observations)
checks=[]
for r in selected:
    rs=[a for a in observations if a['expected_station_id']==r['station_id']];dates=[a['date'] for a in rs]
    checks.append(dict(station_id=r['station_id'],source_country_code=r['source_country_code'],observations=len(rs),distinct_dates=len(set(dates)),duplicate_dates=len(dates)-len(set(dates)),calendar_days_in_2024=366,unobserved_calendar_dates=366-len({d for d in dates if d.startswith('2024-')}),rows_with_quality_flags=sum(bool(json.loads(a['quality_flags_json'])) for a in rs),climate_representativeness='NOT_ESTABLISHED',missing_weather_values='RAW_SENTINELS_PRESERVED_NOT_ZERO_FILLED'))
write('registry_observation_join_checks.csv',checks)
con=sqlite3.connect(T/'weather_observation_b30.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);q=lambda s:'"'+s.replace('"','""')+'"';con.execute('CREATE TABLE '+q(p.stem)+' ('+','.join(q(k)+' TEXT' for k in keys)+')');con.executemany('INSERT INTO '+q(p.stem)+' VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert len(joined)==29661
for p,h in json.loads((O/'baseline.json').read_text())['protected'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
stats=dict(dictionary_rows=len(codes),distinct_fips_codes=len(bycode),station_rows_joined=len(joined),dictionary_join_status=dict(collections.Counter(r['dictionary_status'] for r in joined)),selected_test_stations=len(selected),files_saved=sum(bool(r['file']) for r in receipts),fetch_errors=sum(bool(r['error']) for r in receipts),observations=len(observations),station_date_checks=checks,sqlite_counts=counts,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
notes={'redteam':'FIPS不能直接連ISO；缺天和缺天氣值不填零；原件与原欄位保存。','critic':'六站是確定性管線測試，不是隨機全球樣本；不能推全球誤差、災害风险或收益。','killcritic':'全部29661站史對照來源字典；站號、日期、重複日、366天差額及SQL行數逐項對賬。','blindspot':'FIPS歷史地區、海洋站和重複碼保持多值；GSOD日摘要不等於原始每小時觀測，缺文件不代表該站無任何資料。','blueprint':'站史→FIPS來源字典→年度觀測→原欄位與品質旗標→單位及哨兵值核定→持出驗證。未核定前不輸出氣候指標。','cheatsheet':'來源碼匹配≠ISO已核；有日期≠所有變數齊全；無記錄≠零降水；六站≠全球；站史期間≠連續報告。','actionplan':'已建立全球站史字典對照與六站2024管線測試。續核GSOD單位、缺值及日摘要定義，再取得擴展分層樣本；SDG保持凍結，金融/法人待辦保留。'}
for n,s in notes.items():(R/n/'weather_observation_b30_20261009.md').write_text('# '+n+'｜B30\n\n'+s+'\n\n[報告](../Reference/Weather_Observation_B30_20261009.qmd)。\n',encoding='utf-8')
report='''---
title: "B30：全球站史FIPS字典對照與2024觀測管線測試"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 實測範圍

'''+f"完整保存官方字典 {len(codes)} 行、{len(bycode)} 個不同FIPS代碼；全量對照B29的 {len(joined)} 條站史，狀態 `{json.dumps(stats['dictionary_join_status'])}`。六個來源地區各取一個符合條件的站，取得 {stats['files_saved']} 份2024觀測檔、{len(observations)} 條日摘要行；{stats['fetch_errors']} 個下載失敗保留收據。"+'''

## 官方證據與邊界

[NOAA站史欄位說明](https://www.ncei.noaa.gov/pub/data/noaa/isd-history.txt)確認CTRY為FIPS；[官方國码字典](https://www.ncei.noaa.gov/pub/data/noaa/country-list.txt)含歷史與非主權地區，重複碼保留來源行。這不是ISO對照表。全站史列出有碼未解與空碼，不自動推定國家。

觀測檔逐URL、SHA256保存。六站依有效坐標、ICAO、涵蓋2024的站史區間，按站號排序取首站；並非代表氣候的隨機或分層樣本。原始日摘要欄位完整保存，尚未核定單位、哨兵值和摘要定義，未把缺值轉零、未生成温度／降水指標。站號和日期檢查不驗證氣象量本身。

## 可對賬交付

[官方字典](tables/55_weather_observation_b30_20261009/registry_noaa_country_dictionary.csv)、[全站史字典對照](tables/55_weather_observation_b30_20261009/registry_all_station_country_dictionary_join.csv)、[站點選取](tables/55_weather_observation_b30_20261009/registry_observation_test_stations.csv)、[逐檔收據](tables/55_weather_observation_b30_20261009/observation_fetch_manifest.csv)、[日摘要行](tables/55_weather_observation_b30_20261009/registry_daily_observation_rows.csv)、[站號／日期檢查](tables/55_weather_observation_b30_20261009/registry_observation_join_checks.csv)、[SQLite](tables/55_weather_observation_b30_20261009/weather_observation_b30.sqlite)。讀取行數與SQL對賬通過；舊站史、交接與主報告保留。金融2608項、工商六項、歷史與分頁缺口沒有結案。SDG業務分析不恢復，全球覆蓋與商業收益仍UNKNOWN。
'''
(R/'Reference/Weather_Observation_B30_20261009.qmd').write_text(report,encoding='utf-8');print(json.dumps(stats))
