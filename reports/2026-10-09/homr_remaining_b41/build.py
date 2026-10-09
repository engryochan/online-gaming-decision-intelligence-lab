from pathlib import Path
import csv,json,hashlib,subprocess,datetime,urllib.request,urllib.parse,sqlite3,collections,math
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/65_homr_remaining_b41_20261009'
assert not (O/'validation_receipt.json').exists();T.mkdir(exist_ok=True);(O/'raw').mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if p and Path(p).suffix in ['.qmd','.md']}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prior=read(R/'Reference/tables/64_homr_identity_b40_20261009/registry_40_station_identity_adjudication.csv');old={r['USAF']+r['WBAN']:r for r in read(R/'Reference/tables/54_weather_station_b29_20261009/registry_station_history.csv')}
official={r['GHCN_ID']:r for r in read(R/'Reference/tables/63_station_mapping_b39_20261009/registry_full_ghcnh_station_list.csv')}
pending=[r for r in prior if r['association_state']!='HOMR_CONCURRENT_GHCNH_ICAO_ASSOCIATION_2024_LOCATION_CORROBORATED'];assert len(pending)==26
def interval(a):
    d=a.get('date',{});b=d.get('beginDate','');e=d.get('endDate','')
    try:begin=datetime.date.fromisoformat(b[:10])
    except (ValueError,TypeError):return 'BEGIN_UNKNOWN_OR_UNPARSEABLE'
    if e=='Present':end=datetime.date.max
    else:
        try:end=datetime.date.fromisoformat(e[:10])
        except (ValueError,TypeError):return 'END_UNKNOWN_OR_UNPARSEABLE'
    if begin>end:return 'INTERVAL_REVERSED_REVIEW'
    return 'COVERS_FULL_2024' if begin<=datetime.date(2024,1,1) and end>=datetime.date(2024,12,31) else 'DOES_NOT_COVER_FULL_2024'
assert interval({'date':{'beginDate':'Unknown','endDate':'Present'}})=='BEGIN_UNKNOWN_OR_UNPARSEABLE'
assert interval({'date':{'beginDate':'2023-01-01','endDate':'Present'}})=='COVERS_FULL_2024'
def distance(a,b,c,d):
    a,b,c,d=map(math.radians,[a,b,c,d]);v=math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
    return 6371.0088*2*math.asin(min(1,math.sqrt(max(0,v))))
def fetch(r):
    station=r['gsod_station_id'];icao=old[station]['ICAO'];u='https://www.ncei.noaa.gov/access/homr/services/station/search?'+urllib.parse.urlencode(dict(qid='ICAO:'+icao,date='all',phrData='false',definitions='false'))
    out=dict(gsod_station_id=station,queried_icao=icao,url=u,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',file='',sha256='',error='',station_records=0);stations=[]
    try:
        assert icao.strip(),'Empty qualified identifier'
        with urllib.request.urlopen(u,timeout=25) as response:data=response.read(5000001);out['http_status']=response.status
        assert len(data)<=5000000
        d=json.loads(data);assert 'stationCollection' in d;stations=d['stationCollection'].get('stations',[]);assert isinstance(stations,list)
        p=O/'raw'/(station+'.json');p.write_bytes(data);out.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),station_records=len(stations))
    except Exception as e:out['error']=type(e).__name__;out['http_status']=getattr(e,'code',out['http_status'])
    return out,stations
receipts=[];records=[];identifiers=[];associations=[];decisions=[]
with ThreadPoolExecutor(max_workers=2) as pool:
    for r,(receipt,stations) in zip(pending,pool.map(fetch,pending)):
        receipts.append(receipt);station=r['gsod_station_id'];h=old[station];icao=h['ICAO'];links=[]
        for n,s in enumerate(stations,1):
            sid=str(s.get('ncdcStnId',''));ids=s.get('identifiers',[]);records.append(dict(query_gsod_station_id=station,source_station_row=n,ncdc_station_id=sid,raw_station_json=json.dumps(s,ensure_ascii=False),source_url=receipt['url']))
            for i,a in enumerate(ids,1):identifiers.append(dict(query_gsod_station_id=station,ncdc_station_id=sid,source_identifier_row=i,id_type=a.get('idType',''),identifier=a.get('id',''),begin_date=a.get('date',{}).get('beginDate',''),end_date=a.get('date',{}).get('endDate',''),interval_status=interval(a)))
            icaos=[a for a in ids if a.get('idType')=='ICAO' and a.get('id')==icao]
            for g in [a for a in ids if a.get('idType')=='GHCNH']:
                gid=g.get('id','');period_ok=interval(g)=='COVERS_FULL_2024' and any(interval(a)=='COVERS_FULL_2024' for a in icaos)
                deltas=[]
                for p in s.get('location',{}).get('latLonPairs',[]):
                    if interval(p)=='COVERS_FULL_2024':
                        try:deltas.append(distance(float(h['LAT']),float(h['LON']),float(p['latitude_dec']),float(p['longitude_dec'])))
                        except (ValueError,KeyError):pass
                link=dict(gsod_station_id=station,ncdc_station_id=sid,icao=icao,ghcnh_identifier=gid,ghcnh_interval_status=interval(g),icao_interval_statuses_json=json.dumps([interval(a) for a in icaos]),both_identifiers_cover_2024=period_ok,in_official_ghcnh_station_list=gid in official,active_coordinate_differences_km_json=json.dumps(deltas),location_within_1km=bool(deltas) and max(deltas)<=1,platforms_json=json.dumps(s.get('platforms',[])),source_url=receipt['url'])
                links.append(link);associations.append(link)
        accepted=[a for a in links if a['both_identifiers_cover_2024'] and a['in_official_ghcnh_station_list'] and a['location_within_1km']]
        if receipt['error']:state='FETCH_FAILED_RETAIN_UNKNOWN'
        elif len(accepted)==1:state='NEW_HOMR_2024_ASSOCIATION_LOCATION_CORROBORATED'
        elif len(accepted)>1:state='MULTIPLE_CORROBORATED_ASSOCIATIONS_REVIEW'
        elif not stations:state='EMPTY_QUERY_RESULT_NOT_PROOF_STATION_ABSENT'
        elif not links:state='NO_GHCNH_ID_IN_RETURNED_STATION_HISTORY'
        elif not any(a['both_identifiers_cover_2024'] for a in links):state='IDENTIFIER_ASSOCIATION_PRESENT_TIME_UNKNOWN_OR_OUTSIDE_2024'
        else:state='TIMED_ASSOCIATION_LOCATION_OR_STATION_LIST_REVIEW'
        decisions.append(dict(gsod_station_id=station,previous_state=r['association_state'],current_state=state,ghcnh_identifier=accepted[0]['ghcnh_identifier'] if len(accepted)==1 else '',source_station_records=len(stations),ghcnh_associations=len(links),corroborated_associations=len(accepted),physical_continuity='NOT_ESTABLISHED',weather_values_approved=False,evidence_batch='B41_NEW_QUERY'))
for r in prior:
    if r not in pending:decisions.append(dict(gsod_station_id=r['gsod_station_id'],previous_state=r['association_state'],current_state='CARRIED_B40_2024_ASSOCIATION_LOCATION_CORROBORATED',ghcnh_identifier=r['candidate_ghcn_station_id'],source_station_records=r['source_station_records'],ghcnh_associations=r['matching_records'],corroborated_associations=1,physical_continuity='NOT_ESTABLISHED',weather_values_approved=False,evidence_batch='B40_CARRIED_NOT_REFETCHED'))
decisions.sort(key=lambda r:r['gsod_station_id']);assert len(decisions)==40
write('registry_homr_fetch_receipts.csv',receipts);write('registry_complete_station_records.csv',records);write('registry_all_identifier_periods.csv',identifiers)
if associations:write('registry_ghcnh_icao_dated_associations.csv',associations)
write('registry_latest_40_station_adjudication.csv',decisions)
con=sqlite3.connect(T/'homr_remaining_b41.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
stats=dict(queries=26,query_errors=sum(bool(r['error']) for r in receipts),source_station_records=len(records),identifier_periods=len(identifiers),ghcnh_associations=len(associations),all_40_stations_retained=True,states=dict(collections.Counter(r['current_state'] for r in decisions)),sqlite_counts=counts,old_documents_preserved=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B41：餘26站HOMR再核對與最新40站判定"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 完整未結站史覆核

'''+f"B40未取得全年共時佐證的26站全部依ICAO重新查詢官方HOMR；{stats['query_errors']}項查詢失敗，保存{len(records)}筆完整站史、{len(identifiers)}個識別碼時段、{len(associations)}項GHCNH／ICAO關聯。最新全部40站狀態 `{json.dumps(stats['states'])}`。原14站佐證直接保留並標明B40未重新下載，不假稱本輪全部重新查詢。"+'''

## 未結原因與判定規則

明確區分來源起訖日期Unknown、日期不涵蓋2024、沒有GHCNH識別碼、空回傳、多候選與位置差異；Unknown日期不自行補成最早日期。三個B40未結項本輪亦重新取得，而非只重述舊摘要。GHCND／GHCNMLT與GHCNH識別碼分開，不用相同字串替代資料集命名空間。

只有同一NCDC記錄內ICAO與GHCNH都具有全年2024時段、GHCNH在官方站表、有效時段坐標在1公里工程覆核參數內，且唯一關聯，才增加共時關聯佐證。仍不證明物理站跨年代連續，不開放疑似缺值數值分析；高空／地面平台原欄位保留，不因同ICAO合併。

## 可追溯交付與下一步

[26項來源收據](tables/65_homr_remaining_b41_20261009/registry_homr_fetch_receipts.csv)、[完整站史](tables/65_homr_remaining_b41_20261009/registry_complete_station_records.csv)、[所有識別碼時段](tables/65_homr_remaining_b41_20261009/registry_all_identifier_periods.csv)、[GHCNH／ICAO關聯](tables/65_homr_remaining_b41_20261009/registry_ghcnh_icao_dated_associations.csv)、[最新40站判定](tables/65_homr_remaining_b41_20261009/registry_latest_40_station_adjudication.csv)、[SQLite](tables/65_homr_remaining_b41_20261009/homr_remaining_b41.sqlite)。[官方API規則](https://www.ncei.noaa.gov/access/homr/api)本輪重新閱讀，完整來源JSON及SHA256保留。

下一步針對時段Unknown與位置／站表不一致的站查正式站史字段，並核新版缺值規則後再作新舊量測比較。125筆舊風速衝突、新版疑似缺值、金融、工商、分頁與其他全球待辦保持開放。SDG業務分析凍結，Untitled不恢復，所有舊報告和已提交修改保留。
'''
(R/'Reference/HOMR_Remaining_B41_20261009.qmd').write_text(report,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:(R/n/'homr_remaining_b41_20261009.md').write_text('# '+n+'｜B41\n\n剩餘26站全部重新查HOMR，原14站佐證標明保留來源批次。Unknown日期不填補，跨資料集同字串不冒充命名空間映射；空回傳不證明站不存在。最新40站判定、完整平台及時段均保留，量測與缺值仍未放行。\n\n[報告](../Reference/HOMR_Remaining_B41_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
