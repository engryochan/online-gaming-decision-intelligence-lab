from pathlib import Path
import csv,json,hashlib,urllib.request,datetime,subprocess,sqlite3
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/60_weather_sentinel_b36_20261009'
assert not (O/'validation_receipt.json').exists()
T.mkdir(exist_ok=True);(O/'raw').mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
protected={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if p and Path(p).suffix in ['.qmd','.md']}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),protected=protected),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
urls=['https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt','https://www.ncei.noaa.gov/pub/data/gsod/readme.txt','https://www.ncei.noaa.gov/pub/data/gsod/GSOD_DESC.txt','https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/GSOD_DESC.txt','https://www7.ncdc.noaa.gov/CDO/GSOD_DESC.txt']
def fetch(pair):
    i,url=pair;r=dict(url=url,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',file='',sha256='',error='',mxspd_context='',supports_999_9=False)
    try:
        with urllib.request.urlopen(url,timeout=18) as response:data=response.read(1000001);r['http_status']=response.status
        assert len(data)<=1000000
        text=data.decode('utf-8',errors='replace');lines=text.splitlines();context=[]
        for n,line in enumerate(lines):
            if 'MXSPD' in line:context.extend(lines[max(0,n-1):min(len(lines),n+7)])
        assert context,'No MXSPD documentation: reject unrelated response'
        p=O/'raw'/('documentation_'+str(i)+'.txt');p.write_bytes(data);r.update(file=p.relative_to(R).as_posix(),sha256=hashlib.sha256(data).hexdigest(),mxspd_context='\n'.join(context))
        # Only the detailed MXSPD entry, not adjacent GUST, can establish its sentinel.
        import re
        entries=re.findall(r'MXSPD[^\n]*Maximum sustained[\s\S]*?(?=\n\s*GUST|\Z)',text,re.I)
        r['supports_999_9']=any(re.search(r'Missing\s*=\s*999\.9',e,re.I) for e in entries)
    except Exception as e:r['error']=type(e).__name__;r['http_status']=getattr(e,'code',r['http_status'])
    return r
with ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(fetch,enumerate(urls)))
write('registry_official_documentation_attempts.csv',receipts)
prior=read(R/'Reference/tables/59_pending_recheck_b35_20261009/registry_mxspd_sentinel_conflicts.csv');assert len(prior)==125
daily=read(R/'Reference/tables/58_weather_spatial_b33_20261009/registry_daily_observation_rows.csv');byday={(r['station_id'],r['date']):json.loads(r['raw_fields_json']) for r in daily}
decisions=[]
support=[r['url'] for r in receipts if r['supports_999_9']]
for r in prior:
    raw=byday[(r['station_id'],r['date'])];assert raw['MXSPD'].strip()=='999.9'
    decisions.append(dict(station_id=r['station_id'],date=r['date'],source_url=r['source_url'],source_row=r['source_row'],raw_mxspd=raw['MXSPD'],raw_mean_wind=raw.get('WDSP',''),mean_wind_count=raw.get('WDSP_ATTRIBUTES',''),raw_gust=raw.get('GUST',''),decision='OFFICIAL_ALTERNATE_DOC_MISSING_999_9_WITH_CURRENT_DOC_CONFLICT' if support else 'CONFLICT_UNRESOLVED_NUMERIC_ANALYSIS_WITHHELD',normalized_value='',supporting_urls_json=json.dumps(support),source_document_conflict='PRESERVED_NOT_SILENTLY_RESOLVED',physical_impossibility_not_used_as_proof=True))
write('registry_mxspd_adjudication.csv',decisions)
summary=[]
for station in sorted({r['station_id'] for r in decisions}):
    rs=[r for r in decisions if r['station_id']==station];summary.append(dict(station_id=station,conflict_days=len(rs),earliest=min(r['date'] for r in rs),latest=max(r['date'] for r in rs),same_day_mean_wind_missing=sum(r['raw_mean_wind'].strip()=='999.9' for r in rs),same_day_gust_missing=sum(r['raw_gust'].strip()=='999.9' for r in rs),correlated_missingness='DIAGNOSTIC_NOT_AUTHORITATIVE_SENTINEL_PROOF'))
write('registry_conflict_station_summary.csv',summary)
con=sqlite3.connect(T/'weather_sentinel_b36.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for n,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+n+'"').fetchone()[0]==v
con.close();assert sum(r['conflict_days'] for r in summary)==125
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
stats=dict(official_urls_attempted=len(receipts),documentation_saved=sum(bool(r['file']) for r in receipts),supporting_official_999_9_docs=len(support),conflict_rows_reconciled=125,stations=len(summary),decision_counts=dict(__import__('collections').Counter(r['decision'] for r in decisions)),sqlite_counts=counts,prior_documents_preserved=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B36：MXSPD風速缺值衝突的一手來源覆核"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 已接續的未結項

'''+f"重新嘗試{len(receipts)}個NOAA官方說明網址，保存{stats['documentation_saved']}份具MXSPD段落的文件；其中{len(support)}份詳細段落明確支持999.9缺值。B35全部125筆衝突逐站逐日與原始JSON對賬，涉及{len(summary)}站，未遺漏、未填零。"+'''

## 判定邊界

[現行GSOD說明](https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt)與備選官方說明分別記錄URL、時間、HTTP狀態、SHA256及原段落。404或受阻不代表相關資料不存在；其他機構或社群解析器的慣例不能冒充NOAA當期schema。

本輪判定保留來源文件衝突，125筆標準化值均留空、暫停數值分析。即使另有官方文件支持999.9，也不消除現行說明999的版本差異。平均風／陣風同日缺值的伴隨情況只作診斷，不能獨立證明缺值定義。不以物理不合理值直接篡改原文，不把999值規則全局套用其他欄位。

## 交付與下一步

[官方文件嘗試](tables/60_weather_sentinel_b36_20261009/registry_official_documentation_attempts.csv)、[125筆逐項判定](tables/60_weather_sentinel_b36_20261009/registry_mxspd_adjudication.csv)、[逐站診斷](tables/60_weather_sentinel_b36_20261009/registry_conflict_station_summary.csv)、[SQLite](tables/60_weather_sentinel_b36_20261009/weather_sentinel_b36.sqlite)。原B31/B35規則與文件均保留；本批為有界覆核增補。

下一步只對具有版本化明確缺值規則的欄位建立模型輸入條件；風速衝突在來源正式釐清或取得格式專用一手定義之前保持扣留。金融2608项、工商6项、分頁378项及授權CSV等清單仍未結案，SDG业务分析仍凍結，Untitled不恢復。這次覆核不是全球觀測完整性或預報能力驗收。
'''
(R/'Reference/Weather_Sentinel_B36_20261009.qmd').write_text(report,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:(R/n/'weather_sentinel_b36_20261009.md').write_text('# '+n+'｜B36\n\n125筆MXSPD衝突逐項核對，重新訪問5個官方說明候選。官方文件、受阻收據与逐站伴隨缺值診斷分開保存；不以社群慣例或物理推斷替代格式專用官方定義。衝突值數值分析保持扣留，所有舊文件保留。\n\n[報告](../Reference/Weather_Sentinel_B36_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
