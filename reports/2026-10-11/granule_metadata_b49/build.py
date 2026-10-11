from pathlib import Path
import csv,json,hashlib,subprocess,urllib.request,urllib.parse,datetime,sqlite3
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent; R=O.parents[2]; T=R/'Reference/tables/72_granule_metadata_b49_20261011'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
assert not (O/'baseline.json').exists(),'Never refresh baseline'
T.mkdir();(O/'raw').mkdir()
paths=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
protected={p:sha(R/p) for p in paths if p and Path(p).suffix in ('.md','.qmd') and (R/p).is_file()}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),starting_status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected),indent=2),encoding='utf-8')
prior=read(R/'Reference/tables/71_product_terms_b48_20261011/registry_all_166_product_terms_status.csv')
selected=[r for r in prior if r['evidence_batch']=='B48_PINNED_REVISION_FETCHED'];assert len(selected)==14
def fetch(r):
    year=2016 if r['short_name'].startswith('ALOS2') else 2009 if r['short_name'].startswith('ALOS') else 1998
    temporal=f'{year}-01-01T00:00:00Z,{year}-12-31T23:59:59Z'
    url='https://cmr.earthdata.nasa.gov/search/granules.umm_json?'+urllib.parse.urlencode(dict(collection_concept_id=r['concept_id'],page_size=1,temporal=temporal,sort_key='start_date'))
    rec=dict(concept_id=r['concept_id'],query_year=year,url=url,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',cmr_hits='',source_file='',sha256='',error='')
    items=[]
    try:
        with urllib.request.urlopen(url,timeout=30) as response:
            b=response.read(5000001);rec['http_status']=response.status;rec['cmr_hits']=response.headers.get('CMR-Hits','')
            assert response.headers.get('CMR-Timed-Out','false').lower()!='true'
        assert len(b)<=5000000
        p=O/'raw'/(r['concept_id']+'.json');p.write_bytes(b);rec.update(source_file=p.relative_to(R).as_posix(),sha256=sha(p))
        obj=json.loads(b);items=obj['items'];assert len(items)<=1
        assert int(rec['cmr_hits'])==obj['hits'] and int(rec['cmr_hits'])>=0
        assert bool(items)==(int(rec['cmr_hits'])>0)
        for item in items:
            assert item['meta']['collection-concept-id']==r['concept_id']
    except Exception as e:rec.update(error=type(e).__name__,http_status=getattr(e,'code',rec['http_status']));items=[]
    return rec,items
receipts=[];samples=[];states={}
with ThreadPoolExecutor(max_workers=2) as pool:
    for r,(rec,items) in zip(selected,pool.map(fetch,selected)):
        receipts.append(rec);states[r['concept_id']]='QUERY_FAILED' if rec['error'] else 'HISTORICAL_SAMPLE_METADATA_FETCHED' if items else 'NO_MATCH_IN_SELECTED_YEAR'
        for item in items:
            u=item['umm'];j=lambda key:json.dumps(u.get(key),ensure_ascii=False)
            samples.append(dict(collection_concept_id=r['concept_id'],short_name=r['short_name'],query_year=rec['query_year'],granule_concept_id=item['meta']['concept-id'],granule_revision=item['meta']['revision-id'],granule_ur=u.get('GranuleUR',''),temporal_extent_json=j('TemporalExtent'),spatial_extent_json=j('SpatialExtent'),data_granule_json=j('DataGranule'),related_urls_json=j('RelatedUrls'),platforms_json=j('Platforms'),additional_attributes_json=j('AdditionalAttributes'),full_item_json=json.dumps(item,ensure_ascii=False),source_file=rec['source_file'],source_sha256=rec['sha256'],imagery_downloaded=False,pixel_quality_verified=False,rights_approved=False))
for r in prior:r['b49_sample_state']=states.get(r['concept_id'],'NOT_SAMPLED_PRIOR_STATUS_RETAINED')
write('registry_all_166_product_status.csv',prior);write('registry_source_receipts.csv',receipts)
assert samples,'No usable samples; review receipts before delivery'
write('registry_historical_granule_samples.csv',samples)
work=read(R/'Reference/tables/71_product_terms_b48_20261011/registry_all_498_work_progress.csv')
for r in work:r['b49_metadata_sample_state']=states.get(r['concept_id'],'NOT_SAMPLED');r['task_closed']='False'
assert len(prior)==166 and len(work)==498;write('registry_all_498_work_progress.csv',work)
con=sqlite3.connect(T/'granule_metadata_b49.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);ks=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in ks)+')')
    con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in ks)+')',[[r[k] for k in ks] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close();assert all(sha(R/p)==h for p,h in protected.items())
stats=dict(queries=14,samples=len(samples),failures=sum(bool(r['error']) for r in receipts),empty_selected_year=sum(s=='NO_MATCH_IN_SELECTED_YEAR' for s in states.values()),collections_retained=166,work_items_retained=498,tasks_closed=0,imagery_downloaded=False,pixel_quality_verified=False,sqlite_counts=counts)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
report='''---
title: "B49：歷史衛星產品檔案元資料樣本"
date: 2026-10-11
format:
  html:
    toc: true
    embed-resources: true
---

## 影像與元資料的區別

此處影像指地球觀測產品。ASF集合包含雷達產品及ALOS AVNIR光學產品；雷達產品可能保存不同處理層級的觀測資料，不能一律當作一般照片。本批取得的是檔案目錄元資料，沒有下載影像像素，也沒有核實畫面、解析度、相位保留或實際測量品質。

## 有界歷史樣本

依[NASA CMR API](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html)，對B48的14個集合查詢每集合最多一筆：ALOS取2009年、ALOS2取2016年、ERS及JERS取1998年，依開始時間排序。不加地區條件，這是格式與結構樣本，不是指定地區的完整影像清單。查詢針對當次公開索引，並非固定B45集合revision下的歷史granule索引快照；各次請求也不是同時快照。查無選定年份不等於集合從未存在資料。

保存完整UMM item、granule修訂、時間、空間、DataGranule、相關URL、平台及附加屬性；缺欄位保持null，沒有從產品名稱猜格式或補零。DataGranule中的格式與容量僅為來源宣告，沒有實測下載大小。原始回應、查詢時間、篩選條件與SHA256均留存。相關下載URL僅登記，未訪問或接受下載條款。

## 交付與未結清範圍

'''+json.dumps(stats,ensure_ascii=False)+'''。

[樣本表](tables/72_granule_metadata_b49_20261011/registry_historical_granule_samples.csv)、[14項查詢收據](tables/72_granule_metadata_b49_20261011/registry_source_receipts.csv)、[166項完整狀態](tables/72_granule_metadata_b49_20261011/registry_all_166_product_status.csv)、[498項待辦](tables/72_granule_metadata_b49_20261011/registry_all_498_work_progress.csv)、[SQLite](tables/72_granule_metadata_b49_20261011/granule_metadata_b49.sqlite)。

B48產品特定權利限制全部保留，尤其JERS非開放旗標不因公開元資料可取得而解除。本批沒有結清任何工作，也不宣稱全球覆蓋、商業重分發許可或全球企業清單完成。下一步按實際用途選歷史地區、核當期條款與品質文檔，再評估適當產品及處理成本。全球金融、歷史政治實體與氣象待辦持續保留；SDG業務分析仍凍結，Untitled不恢復。
'''
(R/'Reference/Granule_Metadata_B49_20261011.qmd').write_text(report,encoding='utf-8')
notes={'redteam':'公開元資料不等於影像下載許可或可轉售。','critic':'每集合一筆指定年份樣本不是完整資料覆蓋。','killcritic':'完整UMM與原始回應留存，使產品格式查證可重做。','blindspot':'AVNIR為光學集合；不能把ASF全部稱為SAR。','blueprint':'歷史時間查詢→收據與原始UMM→樣本欄位→完整166及498清單。','cheatsheet':'14查詢；沒有像素下載；空結果與失敗分列。','actionplan':'依具體用途核當期條款、歷史地區及品質文件，再選產品。'}
for n,v in notes.items():(R/n/'granule_metadata_b49_20261011.md').write_text('# '+n+' | B49\n\n'+v+'\n\n[報告](../Reference/Granule_Metadata_B49_20261011.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
