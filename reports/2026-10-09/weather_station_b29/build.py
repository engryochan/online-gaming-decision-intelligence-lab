from pathlib import Path
import csv,json,hashlib,datetime,collections,sqlite3
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/54_weather_station_b29_20261009'
assert not (O/'validation_receipt.json').exists(),'Preserve completed batch'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
receipt=json.loads((O/'source_receipt.json').read_text());p=R/receipt['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['sha256']
rows=read(p);assert list(rows[0])==['USAF','WBAN','STATION NAME','CTRY','STATE','ICAO','LAT','LON','ELEV(M)','BEGIN','END']
counts=collections.Counter((r['USAF'],r['WBAN']) for r in rows)
parsed=[];quality=collections.Counter();countries=collections.Counter()
for n,r in enumerate(rows,1):
    reasons=[];lat=lon=None
    try:
        lat=float(r['LAT']);lon=float(r['LON'])
        if not (-90<=lat<=90 and -180<=lon<=180):reasons.append('COORDINATES_OUT_OF_RANGE')
        if lat==0 and lon==0:reasons.append('ZERO_ZERO_LOCATION_REVIEW_NOT_AUTOMATIC_NULL')
    except ValueError:reasons.append('COORDINATES_MISSING_OR_UNPARSEABLE')
    begin=end=''
    try:
        begin=datetime.datetime.strptime(r['BEGIN'],'%Y%m%d').date().isoformat();end=datetime.datetime.strptime(r['END'],'%Y%m%d').date().isoformat()
        if begin>end:reasons.append('DATE_ORDER_REVIEW')
        if end>'2026-10-09':reasons.append('END_AFTER_OBSERVED_DATE_REVIEW')
    except ValueError:reasons.append('DATE_PARSE_REVIEW')
    if counts[(r['USAF'],r['WBAN'])]>1:reasons.append('REPEATED_ID_PAIR_PRESERVE_ALL_VERSIONS')
    if not r['CTRY']:reasons.append('EMPTY_SOURCE_COUNTRY_CODE')
    quality.update(reasons);countries[r['CTRY']]+=1
    parsed.append(dict(source_row=n,**r,begin_iso=begin,end_iso=end,quality_flags_json=json.dumps(reasons),identity_scope='SOURCE_STATION_HISTORY_ROW_NOT_UNIQUE_PHYSICAL_STATION',country_mapping_status='SOURCE_CODE_PRESERVED_ISO_MAPPING_NOT_VERIFIED',continuous_observations_verified='UNKNOWN',current_station_active='UNKNOWN'))
write('registry_station_history.csv',parsed)
write('registry_station_quality_summary.csv',[dict(flag=k,rows=v,meaning='REVIEW_SIGNAL_NOT_AUTOMATIC_REJECTION') for k,v in quality.items()])
write('registry_source_country_counts.csv',[dict(source_country_code=k,history_rows=v,iso_alpha2='',iso_mapping='NOT_VERIFIED_DO_NOT_JOIN_BY_STRING_EQUALITY') for k,v in sorted(countries.items())])
years=[]
for year in [1900,1950,2000,2020,2026]:
    day=f'{year}-01-01';years.append(dict(date=day,history_intervals_containing_date=sum(r['begin_iso']<=day<=r['end_iso'] for r in parsed if r['begin_iso'] and r['end_iso']),continuous_reporting='UNKNOWN',coverage_denominator='UNKNOWN'))
write('registry_history_interval_checks.csv',years)
con=sqlite3.connect(T/'weather_station_b29.sqlite');cs={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);q=lambda s:'"'+s.replace('"','""')+'"';con.execute('CREATE TABLE '+q(p.stem)+' ('+','.join(q(k)+' TEXT' for k in keys)+')');con.executemany('INSERT INTO '+q(p.stem)+' VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);cs[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in cs.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert len(parsed)==len(rows)
for p,h in json.loads((O/'baseline.json').read_text())['protected'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
a=dict(source_rows=len(rows),parsed_rows=len(parsed),rejected_or_dropped=0,distinct_id_pairs=len(counts),distinct_nonempty_source_country_codes=sum(bool(c) for c in countries),quality_signals=dict(quality),sqlite_counts=cs,imagery_or_weather_observation_rows_downloaded=0,iso_country_mapping_verified=False,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8')
notes={'redteam':'全量來源行保留；坐標範圍、零零坐標、日期及重複ID均以review信號記錄，不偷偷丟棄。','critic':'氣象站歷史名錄不是氣象觀測，更不是災害風險或全球API覆蓋實測。','killcritic':'read=parsed+rejected，rejected=0；CSV/SQLite、雜湊及保護文件對賬。品質旗標不自動宣稱資料錯誤。','blindspot':'來源CTRY不能按字串直接當ISO；歷史跨度不保證每天報告；零零坐標可能需原站證據；船舶與移動站可能不同粒度。','blueprint':'公開站史原件→逐行時態/坐標核查→國碼映射→授權氣象觀測→官方金標→持出地區回測。當前只完成站史核查。','cheatsheet':'站史≠天氣值；日期區間≠連續報告；CTRY≠已驗證ISO；ID對≠唯一地理站；採集≠商業收入。','actionplan':'遵循最新交接優先序，取得NOAA一個完整公開schema資料集。下一步核對來源國碼及代表站觀測，金融/法人/歷史待辦保留；SDG分析不恢復。'}
for n,s in notes.items():(R/n/'weather_station_b29_20261009.md').write_text('# '+n+'｜B29\n\n'+s+'\n\n[報告](../Reference/Weather_Station_History_B29_20261009.qmd)。\n',encoding='utf-8')
report='''---
title: "B29：NOAA全球氣象站歷史名錄全量核查"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 定位與實測

依最新提交交接書，優先氣象／災害韌性公開資料，不恢復SDG分析。取得一個明確schema的公開站史資料集，沒有採集軍事目標、即時軍事動態或受限系統。

'''+f"完整讀取 {len(rows)} 條站史來源行，保留全部11個原始欄位、前導零和來源行號；解析 {len(parsed)} 條，拒收或丟棄0條。實測 {len(counts)} 個不同USAF/WBAN對、{a['distinct_nonempty_source_country_codes']} 個非空來源國碼。這些是站史記錄與來源代碼，不是已核實唯一實體站、ISO地區覆蓋或活躍站數。"+'''

## 品質與時間

品質信號分職保留，見逐行旗標與彙總。空坐標不填0；零零坐標不自動改為空；重複ID對不機械合併。BEGIN/END解碼為日期，區間檢查不能當成連續氣象觀測。來源CTRY未核定ISO映射，不以同字母自動連結249母表；母表與歷史政治實體原資料均保留。

## 官方來源与範圍

[NOAA ISD官方說明](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database)說明全球地面觀測及時間／空間覆蓋差異；[站史CSV](https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv)本輪全部取得。站史名錄不是溫度、降水或衛星影像；本輪未下載氣象觀測，也未建立預報精度或災害模型。原始SHA256證明保存版本，不是內容真實性的独立認證。實際產品及衍生使用仍按來源條款逐項核定。

## 交付與下一步

[全站史核查](tables/54_weather_station_b29_20261009/registry_station_history.csv)、[品質摘要](tables/54_weather_station_b29_20261009/registry_station_quality_summary.csv)、[來源國碼](tables/54_weather_station_b29_20261009/registry_source_country_counts.csv)、[年代區間檢查](tables/54_weather_station_b29_20261009/registry_history_interval_checks.csv)、[SQLite](tables/54_weather_station_b29_20261009/weather_station_b29.sqlite)。全量來源行數、CSV/SQL、完整性及保護文件雜湊核對通過，七向文件已更新。下一步先核對國碼與站史欄位定义，再取得代表站歷史觀測，對照官方金標，不能用名錄行數替代模型效果。

原金融清單2608項未嘗試、六個工商查詢、歷史封存與分頁缺口均未結案。全球完整收錄及商業收益仍UNKNOWN。交接書和兩份主報告未覆寫。
'''
(R/'Reference/Weather_Station_History_B29_20261009.qmd').write_text(report,encoding='utf-8');print(json.dumps(a))
