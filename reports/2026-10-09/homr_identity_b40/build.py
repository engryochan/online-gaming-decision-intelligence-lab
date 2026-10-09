from pathlib import Path
import csv,json,hashlib,subprocess,datetime,urllib.request,urllib.parse,sqlite3,collections,math
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/64_homr_identity_b40_20261009'
assert not (O/'validation_receipt.json').exists();T.mkdir(exist_ok=True);(O/'raw').mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if p and Path(p).suffix in ['.qmd','.md']}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=read(R/'Reference/tables/63_station_mapping_b39_20261009/registry_40_station_candidate_summary.csv');candidates=read(R/'Reference/tables/63_station_mapping_b39_20261009/registry_all_exact_icao_candidates.csv')
selected=[next(r for r in candidates if r['gsod_station_id']==s['gsod_station_id'] and r['ghcn_station_id']==s['ghcn_station_id']) for s in summary if s['ghcn_station_id']];assert len(selected)==17
def fetch(r):
    u='https://www.ncei.noaa.gov/access/homr/services/station/search?'+urllib.parse.urlencode(dict(qid='ICAO:'+r['legacy_icao'],date='all',phrData='false',definitions='false'))
    out=dict(gsod_station_id=r['gsod_station_id'],candidate_ghcn_station_id=r['ghcn_station_id'],queried_icao=r['legacy_icao'],url=u,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',file='',sha256='',error='',station_records=0);stations=[]
    try:
        with urllib.request.urlopen(u,timeout=25) as response:data=response.read(5000001);out['http_status']=response.status
        assert len(data)<=5000000
        d=json.loads(data);assert 'stationCollection' in d;stations=d['stationCollection'].get('stations',[]);assert isinstance(stations,list)
        p=O/'raw'/(r['gsod_station_id']+'.json');p.write_bytes(data);out.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),station_records=len(stations))
    except Exception as e:out['error']=type(e).__name__;out['http_status']=getattr(e,'code',out['http_status'])
    return out,stations
receipts=[];stationrows=[];idrows=[];decisions=[]
def covers(a):
    d=a.get('date',{});b=d.get('beginDate','');e=d.get('endDate','')
    return bool(b) and b[:10]<='2024-01-01' and (e=='Present' or bool(e) and e[:10]>='2024-12-31')
def distance(a,b,c,d):
    a,b,c,d=map(math.radians,[a,b,c,d]);v=math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 6371.0088*2*math.asin(min(1,math.sqrt(max(0,v))))
old={r['USAF']+r['WBAN']:r for r in read(R/'Reference/tables/54_weather_station_b29_20261009/registry_station_history.csv')}
with ThreadPoolExecutor(max_workers=2) as pool:
    for r,(receipt,stations) in zip(selected,pool.map(fetch,selected)):
        receipts.append(receipt);matches=[]
        for n,s in enumerate(stations,1):
            sid=str(s.get('ncdcStnId',''));ids=s.get('identifiers',[])
            stationrows.append(dict(query_gsod_station_id=r['gsod_station_id'],source_station_row=n,ncdc_station_id=sid,source_url=receipt['url'],raw_station_json=json.dumps(s,ensure_ascii=False)))
            for i,a in enumerate(ids,1):idrows.append(dict(query_gsod_station_id=r['gsod_station_id'],ncdc_station_id=sid,identifier_row=i,id_type=a.get('idType',''),identifier=a.get('id',''),begin_date=a.get('date',{}).get('beginDate',''),end_date=a.get('date',{}).get('endDate',''),covers_full_2024=covers(a)))
            ghcn=[a for a in ids if a.get('idType')=='GHCNH' and a.get('id')==r['ghcn_station_id'] and covers(a)]
            icao=[a for a in ids if a.get('idType')=='ICAO' and a.get('id')==r['legacy_icao'] and covers(a)]
            pairs=s.get('location',{}).get('latLonPairs',[]);deltas=[]
            for p in pairs:
                if covers(p):
                    try:deltas.append(distance(float(old[r['gsod_station_id']]['LAT']),float(old[r['gsod_station_id']]['LON']),float(p['latitude_dec']),float(p['longitude_dec'])))
                    except (ValueError,KeyError):pass
            if ghcn and icao:matches.append(dict(ncdc_station_id=sid,location_differences_km=deltas,platforms=s.get('platforms',[])))
        location_ok=len(matches)==1 and bool(matches[0]['location_differences_km']) and max(matches[0]['location_differences_km'])<=1
        state='HOMR_CONCURRENT_GHCNH_ICAO_ASSOCIATION_2024_LOCATION_CORROBORATED' if location_ok else 'HOMR_ASSOCIATION_PRESENT_LOCATION_OR_MULTIPLE_RECORD_REVIEW' if matches else 'NO_FULL_2024_ASSOCIATION_FOUND_OR_FETCH_FAILED'
        decisions.append(dict(gsod_station_id=r['gsod_station_id'],candidate_ghcn_station_id=r['ghcn_station_id'],icao=r['legacy_icao'],source_station_records=len(stations),matching_records=len(matches),matches_json=json.dumps(matches),association_state=state,historical_physical_continuity='NOT_ESTABLISHED',source_url=receipt['url'],weather_values_approved=False))
for s in summary:
    if not s['ghcn_station_id']:decisions.append(dict(gsod_station_id=s['gsod_station_id'],candidate_ghcn_station_id='',icao='',source_station_records='',matching_records='',matches_json='[]',association_state='B39_AMBIGUOUS_OR_NO_NEAR_CANDIDATE_RETAINED_NOT_QUERIED',historical_physical_continuity='NOT_ESTABLISHED',source_url='',weather_values_approved=False))
decisions.sort(key=lambda r:r['gsod_station_id']);assert len(decisions)==40
write('registry_homr_fetch_receipts.csv',receipts)
if stationrows:write('registry_homr_complete_station_records.csv',stationrows)
if idrows:write('registry_homr_identifier_periods.csv',idrows)
write('registry_40_station_identity_adjudication.csv',decisions)
byid={r['gsod_station_id']:r for r in decisions};comparisons=read(R/'Reference/tables/63_station_mapping_b39_20261009/registry_candidate_year_date_comparison.csv')
for r in comparisons:r['homr_association_state']=byid[r['gsod_station_id']]['association_state'];r['numeric_comparison']='NOT_PERFORMED_MISSING_RULES_AND_PLATFORM_SCOPE_PENDING'
write('registry_three_sample_date_comparison_with_identity.csv',comparisons)
con=sqlite3.connect(T/'homr_identity_b40.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
stats=dict(homr_queries=17,query_errors=sum(bool(r['error']) for r in receipts),source_station_records=len(stationrows),identifier_periods=len(idrows),all_legacy_stations_preserved=40,association_states=dict(collections.Counter(r['association_state'] for r in decisions)),sqlite_counts=counts,protected_documents_unchanged=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B40：HOMR全歷史識別碼與2024共時關聯核查"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 一手查詢與時段證據

依[HOMR官方API](https://www.ncei.noaa.gov/access/homr/api)對17個B39唯一近距離候選精確查ICAO，date=all保留全部歷史，phrData=false僅略過本輪不需要的元素歷史。搜尋匹配預設跨歷史，不能把回傳當作2024現行資料；本輪另逐項核識別碼與坐標有效時段涵蓋全年2024。GHCNH字段在實測JSON出現，完整原始回傳保留，不猜測API未列出的查詢類型。

'''+f"17項查詢中{stats['query_errors']}項錯誤，保存{len(stationrows)}筆完整站史及{len(idrows)}個識別碼時段；全部40站判定狀態 `{json.dumps(stats['association_states'])}`。"+'''

只有同一NCDC站史同時包含精確GHCNH與ICAO且各自涵蓋2024，再以有時段的坐標對照符合1公里工程參數，才標記共時識別碼關聯有佐證。這不是從最相近名稱猜映射，不證明所有年代的物理站連續或從未搬遷。

## 平台與品質邊界

例如ENJA查詢同時回傳高空站及地面站，不能僅按ICAO合併。完整平台、名稱、地理時段與識別碼保留供後續核查；缺少平台欄位不能推斷平台一致。23個無唯一近距離候選的舊站保留未查詢狀態，沒有被移除。

三個B39樣本的日期覆蓋對照附上本輪站史狀態；仍不比較氣象數值，新版疑似缺值與舊125筆風速衝突未解除。來源Present表示來源開放結束時段，不是永久有效保證。

## 可追溯交付與續作

[逐查收據](tables/64_homr_identity_b40_20261009/registry_homr_fetch_receipts.csv)、[完整站史](tables/64_homr_identity_b40_20261009/registry_homr_complete_station_records.csv)、[識別碼時段](tables/64_homr_identity_b40_20261009/registry_homr_identifier_periods.csv)、[40站判定](tables/64_homr_identity_b40_20261009/registry_40_station_identity_adjudication.csv)、[三樣本日期覆蓋及站史狀態](tables/64_homr_identity_b40_20261009/registry_three_sample_date_comparison_with_identity.csv)、[SQLite](tables/64_homr_identity_b40_20261009/homr_identity_b40.sqlite)。

下一步覆核無候選／多候選站的歷史識別碼、遷移與來源坐標，並取得格式專用缺值證據後才比較量測。金融、工商、分頁、全球與授權待辦不結案；SDG業務分析凍結，Untitled不恢復，所有既有報告與原件保留。
'''
(R/'Reference/HOMR_Identity_B40_20261009.qmd').write_text(report,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:(R/n/'homr_identity_b40_20261009.md').write_text('# '+n+'｜B40\n\n17個候選HOMR全歷史查詢，40站全部保留判定。共時GHCNH／ICAO與2024有效坐標證據和物理連續性分開；多平台不得單按ICAO合併，缺值扣留不解除。\n\n[報告](../Reference/HOMR_Identity_B40_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
