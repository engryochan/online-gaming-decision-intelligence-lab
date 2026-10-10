#!/usr/bin/env python3
"""民用地理風險報告：**純合成示例**，不可做土地判權、軍事決策或真實天災預報。"""
import argparse,csv,json,hashlib,datetime
from pathlib import Path

MOCK=[
 {"site_id":"DEMO_A","site_area_ha":"125","flood_fraction":"0.12","rain_p95_mm":"85","weather_age_hours":"3","source":"SYNTHETIC"},
 {"site_id":"DEMO_B","site_area_ha":"80","flood_fraction":"0.42","rain_p95_mm":"120","weather_age_hours":"48","source":"SYNTHETIC"},
]
def assess(row):
    if row['source']!='SYNTHETIC': raise ValueError('Demo only: real-world data must enter validated licensed ingestion pipeline')
    area=float(row['site_area_ha']); f=float(row['flood_fraction']); rain=float(row['rain_p95_mm']); age=float(row['weather_age_hours'])
    if not (area>0 and 0<=f<=1 and 0<=rain<=5000 and 0<=age<100000): raise ValueError('invalid range')
    # 教學用組合指標，非經驗校準機率或預測
    score=round(100*(.65*f+.35*min(rain/200,1)),1)
    return {**row,'illustrative_score':score,'freshness':'STALE' if age>24 else 'FRESH','publishable_as_real':'NO'}
def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    results=[assess(x) for x in MOCK]
    p=out/'synthetic_results.json';p.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    metadata={'asof':datetime.date(2026,10,9).isoformat(),'status':'SYNTHETIC_ONLY', 'sha256':sha, 'units':{'site_area_ha':'ha','rain_p95_mm':'mm'}, 'decision':'NOT_FOR_LIVE_USE'}
    (out/'provenance.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return results

def tests():
    r=assess(MOCK[0]);assert r['freshness']=='FRESH' and r['publishable_as_real']=='NO'
    r=assess(MOCK[1]);assert r['freshness']=='STALE'
    for bad in [dict(MOCK[0],flood_fraction='1.1'),dict(MOCK[0],site_area_ha='0'),dict(MOCK[0],source='UNKNOWN')]:
       try:assess(bad)
       except (ValueError,AssertionError):pass
       else:raise AssertionError('bad input accepted')
    print('SELF_TEST_PASS: 5 checks (synthetic), no API access')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');p.add_argument('--output',default='geo_demo_output');a=p.parse_args()
 if a.self_test: tests()
 else: print(json.dumps(run(a.output),ensure_ascii=False,indent=2))
