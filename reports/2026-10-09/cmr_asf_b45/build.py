from pathlib import Path
import csv,json,hashlib,subprocess,datetime,urllib.request,urllib.parse,sqlite3,collections

O=Path(__file__).resolve().parent; R=O.parents[2]; T=R/'Reference/tables/69_cmr_asf_b45_20261009'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
assert not (O/'baseline.json').exists(),'Do not refresh a baseline'
T.mkdir();(O/'raw').mkdir()
names=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
protected={p:sha(R/p) for p in names if p and Path(p).suffix in ('.qmd','.md') and (R/p).is_file()}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
    starting_status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected),indent=2)+'\n',encoding='utf-8')
receipts=[]
def fetch(url,name):
    with urllib.request.urlopen(url,timeout=30) as response:
        b=response.read(10000001);headers=dict(response.headers);status=response.status
    assert len(b)<=10000000,'Response cap; never publish truncated evidence'
    p=O/'raw'/name;p.write_bytes(b)
    receipts.append(dict(source_file=p.relative_to(R).as_posix(),sha256=sha(p),url=url,
        fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status=status,
        cmr_hits=headers.get('CMR-Hits',headers.get('cmr-hits','')),headers_json=json.dumps(headers),error=''))
    return b,headers
fetch('https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html','cmr_api.html')
records=[];links=[];pages=[];reported=None;seen=set()
for page in range(1,101):
    url='https://cmr.earthdata.nasa.gov/search/collections.umm_json?'+urllib.parse.urlencode(dict(provider='ASF',page_size=50,page_num=page))
    b,headers=fetch(url,'collections_page_'+str(page)+'.json');d=json.loads(b)
    items=d['items'];hits=int(headers.get('CMR-Hits',headers.get('cmr-hits',d.get('hits',-1))))
    assert hits>=0 and isinstance(items,list)
    if reported is None:reported=hits
    assert hits==reported,'Catalog count changed during pagination'
    if 'hits' in d:assert int(d['hits'])==reported
    pages.append(dict(page_number=page,items=len(items),server_hits=hits,source_file=receipts[-1]['source_file'],source_sha256=receipts[-1]['sha256']))
    for ordinal,item in enumerate(items,1):
        meta=item['meta'];umm=item['umm'];cid=meta['concept-id']
        assert cid not in seen,'Duplicate collection across pages';seen.add(cid)
        assert meta['provider-id']=='ASF'
        records.append(dict(concept_id=cid,revision_id=meta.get('revision-id',''),provider_id=meta['provider-id'],
            native_id=meta.get('native-id',''),short_name=umm.get('ShortName',''),version=umm.get('Version',''),
            entry_title=umm.get('EntryTitle',''),doi_json=json.dumps(umm.get('DOI',{})),
            temporal_extents_json=json.dumps(umm.get('TemporalExtents',[])),spatial_extent_json=json.dumps(umm.get('SpatialExtent',{})),
            platforms_json=json.dumps(umm.get('Platforms',[])),processing_level_json=json.dumps(umm.get('ProcessingLevel',{})),
            use_constraints_json=json.dumps(umm.get('UseConstraints',{})),access_constraints_json=json.dumps(umm.get('AccessConstraints',{})),
            distributions_json=json.dumps(umm.get('DistributionInformation',{})),raw_item_json=json.dumps(item,ensure_ascii=False),
            source_page=page,source_row=ordinal,source_file=receipts[-1]['source_file'],source_sha256=receipts[-1]['sha256'],
            registry_state='CATALOG_METADATA_INGESTED',imagery_downloaded=False,country_coverage_verified=False,
            commercial_rights='NOT_ADJUDICATED_PER_COLLECTION'))
        for i,link in enumerate(umm.get('RelatedUrls',[]),1):
            links.append(dict(concept_id=cid,revision_id=meta.get('revision-id',''),source_link_row=i,
                url=link.get('URL',''),url_content_type=link.get('URLContentType',''),type=link.get('Type',''),subtype=link.get('Subtype',''),
                raw_link_json=json.dumps(link,ensure_ascii=False),link_fetch_state='CATALOG_REFERENCE_NOT_FETCHED',source_file=receipts[-1]['source_file']))
    # Request an explicit empty terminal page, including when the final nonempty page is short.
    if not items:
        assert len(records)==reported;break
else:raise AssertionError('Pagination cap reached; catalog incomplete')
assert records and len(seen)==reported
write('registry_all_asf_collections.csv',records);write('registry_all_related_url_references.csv',links)
write('registry_pagination_reconciliation.csv',pages);write('registry_source_receipts.csv',receipts)
definitions=[
 ('concept_id','CMR collection identity','Stable collection key; not a satellite, company or downloaded image'),
 ('revision_id','Source metadata revision','Supports change tracking; latest public revision only, not all historical revisions'),
 ('provider_id','CMR metadata provider','ASF filter scope; not ISO nationality or ultimate spacecraft owner'),
 ('short_name_and_version','Collection release identifiers','Keep release variants separate; do not collapse by display title'),
 ('temporal_extents','Declared dataset time coverage','Catalog claim; not proof of uninterrupted observations or file availability'),
 ('spatial_extent','Declared geometry','Source geometry retained; not verified coverage of every ISO territory'),
 ('platforms','Declared platform and instrument descriptions','Preserve source arrays; not current operational capability proof'),
 ('constraints','Per collection access/use metadata','Evidence for later review; no inherited blanket CC0 from NOAA SSOD'),
 ('related_urls','Source typed references','Documentation/access/service references; URLs not fetched or availability-tested'),
 ('raw_item_json','Complete original item including meta and UMM','Preserves all fields not projected into typed columns'),
 ('CMR-Hits','Search result count','Reconcile provider-filtered latest accessible metadata; not all Earth science holdings'),
 ('business_value','Non-operational disaster resilience data discovery','Candidate selection and provenance; no forecast accuracy or revenue demonstrated')]
write('registry_business_field_definitions.csv',[dict(field=f,business_definition=d,value_and_limit=v) for f,d,v in definitions])
work=[dict(concept_id=r['concept_id'],revision_id=r['revision_id'],task_type=t,state='OPEN',
           evidence='CMR_COLLECTION_METADATA_ONLY',completion_required=need) for r in records for t,need in [
 ('PER_COLLECTION_RIGHTS','Read collection-specific official use/access terms and third-party limitations'),
 ('GRANULE_AVAILABILITY','Query and reconcile granule availability by defined area/time without assuming metadata extent proves coverage'),
 ('SCHEMA_QUALITY_VALIDATION','Inspect product format, missing/quality flags and held-out-area accuracy before numerical analysis')]]
write('registry_per_collection_workqueue.csv',work)
con=sqlite3.connect(T/'cmr_asf_b45.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')')
    con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close();assert all(sha(R/p)==h for p,h in protected.items())
stats=dict(provider='ASF',server_reported_hits=reported,collections=len(records),distinct_concept_ids=len(seen),
    related_url_references=len(links),pages_including_empty_terminal=len(pages),scoped_pagination_reconciled=True,
    atomic_source_snapshot=False,all_historical_revisions_ingested=False,imagery_downloaded=False,
    per_collection_open_tasks=len(work),sqlite_counts=counts,old_documents_preserved=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B45：NASA CMR／ASF全分頁集合目錄與逐產品工作清單"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 交接清單中的衛星地球觀測

按[官方CMR API](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html)的provider參數採集ASF公開集合中繼資料，使用每頁50項、原始JSON及回應標頭逐頁保存。以CMR-Hits核對累計及唯一concept_id，另取空終止頁。ASF是地球觀測來源供應單位，不是國家、上市公司或單一衛星。[ASF官方資料發現說明](https://asf.alaska.edu/asf/asf-services-data-discovery/)亦列出Earthdata Search等入口。

此交付涵蓋本輪ASF查詢所回傳的全部最新公開集合，不等於所有NASA／全球資料源、所有歷史版本或全部影像。分頁不是原子交易快照：保存各次請求時間、來源版本與筆數，不宣稱期間無中繼資料更新。

## 內容、價值與限制

完整meta與UMM記錄保留在raw_item_json及原始檔；投影集合識別碼、來源修訂、短名／版本、時間、空間、平台、DOI、約束與連結，不因表格欄位有限而丟棄其餘資訊。相關網址逐項保留原始型別，但本輪沒有逐一下載或測可用性。

用途是災害韌性與環境風險資料集選型及來源追溯。目錄時間／幾何不證明連續觀測或逐國實測覆蓋，資料集不是公司或物理衛星統計。各集合另列授權、granule可用性及產品格式品質三項待辦；不把SSODv2的CC0授權移植至ASF產品，不宣稱已下載影像或已驗證收益。

## 可追溯交付

'''+ '統計：`'+json.dumps(stats)+'`。\n\n'+'''
[全部集合](tables/69_cmr_asf_b45_20261009/registry_all_asf_collections.csv)、[相關網址](tables/69_cmr_asf_b45_20261009/registry_all_related_url_references.csv)、[分頁對賬](tables/69_cmr_asf_b45_20261009/registry_pagination_reconciliation.csv)、[來源收據](tables/69_cmr_asf_b45_20261009/registry_source_receipts.csv)、[業務欄位定義](tables/69_cmr_asf_b45_20261009/registry_business_field_definitions.csv)、[逐集合清單](tables/69_cmr_asf_b45_20261009/registry_per_collection_workqueue.csv)、[SQLite](tables/69_cmr_asf_b45_20261009/cmr_asf_b45.sqlite)。

先前15项測站佐證、25項未結、3,114個SSOD待核值、125筆GSOD風速衝突均保留；全球金融、工商、歷史政治實體等待辦不結案。下一步依集合特定授權與granule證據選定可驗收的地球觀測產品；SDG業務分析仍凍結，Untitled不恢復。既有並行修改不納入本輪提交。
'''
(R/'Reference/CMR_ASF_B45_20261009.qmd').write_text(report,encoding='utf-8')
notes={'redteam':'目錄覆蓋、當前任務運作與影像可下載不是同一事實；禁止推出即時軍事追蹤或目標資料。',
 'critic':'CMR-Hits與空終止頁僅證明本輪ASF查詢對賬，不能宣稱全球來源全收齊。',
 'killcritic':'完整UMM與revision保留，資料集選型可追溯；尚未下載影像不抹去目錄工程價值。',
 'blindspot':'collection、granule、衛星、法人及ISO國家不可混算；時空extent不證明連續資料。',
 'blueprint':'完整原始頁與來源標頭→集合與連結→業務字典→逐產品授權／granule／品質工作清單。',
 'cheatsheet':'ASF全分頁查詢對賬≠所有NASA；元資料入庫≠影像入庫≠品質驗證≠收入。',
 'actionplan':'核每集合授權，再核限定地區年代granule可用性與產品schema；其他全球未結項保留。'}
for n,v in notes.items():(R/n/'cmr_asf_b45_20261009.md').write_text('# '+n+' | B45\n\n'+v+'\n\n[報告](../Reference/CMR_ASF_B45_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
