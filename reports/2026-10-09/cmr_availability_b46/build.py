from pathlib import Path
import csv,json,hashlib,subprocess,datetime,urllib.request,urllib.parse,sqlite3,collections
from concurrent.futures import ThreadPoolExecutor

O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/70_cmr_availability_b46_20261009'
B45=R/'reports/2026-10-09/cmr_asf_b45';BT=R/'Reference/tables/69_cmr_asf_b45_20261009'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
assert not (O/'baseline.json').exists(),'Never refresh an existing baseline'
T.mkdir();(O/'raw').mkdir()
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
protected={p:sha(R/p) for p in tracked if p and Path(p).suffix in ('.md','.qmd') and (R/p).is_file()}
# A separate review of intact B45 delivery does not replace its failed original baseline.
b45_files={p.relative_to(R).as_posix():sha(p) for root in [B45,BT] for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
for p in [R/'Reference/CMR_ASF_B45_20261009.qmd',R/'Reference/CMR_ASF_B45_20261009.html']+[R/n/'cmr_asf_b45_20261009.md' for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']]:
    b45_files[p.relative_to(R).as_posix()]=sha(p)
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
    starting_status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected,b45_delivery_review=b45_files),indent=2)+'\n',encoding='utf-8')
records=read(BT/'registry_all_asf_collections.csv');assert len(records)==166
for receipt in read(BT/'registry_source_receipts.csv'):assert sha(R/receipt['source_file'])==receipt['sha256']
def fetch(job):
    key,url=job
    r=dict(request_key=key,url=url,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',final_url='',
        source_file='',sha256='',headers_json='',cmr_hits='',error='')
    data=None
    try:
        with urllib.request.urlopen(url,timeout=20) as response:
            b=response.read(5000001);r.update(http_status=response.status,final_url=response.url)
            h=dict(response.headers);r.update(headers_json=json.dumps(h),cmr_hits=h.get('CMR-Hits',h.get('cmr-hits','')))
        assert len(b)<=5000000,'Response cap'
        p=O/'raw'/(key+'.response');p.write_bytes(b);r.update(source_file=p.relative_to(R).as_posix(),sha256=sha(p));data=b
    except Exception as e:r.update(error=type(e).__name__,http_status=getattr(e,'code',r['http_status']))
    return r,data
jobs=[(r['concept_id'],'https://cmr.earthdata.nasa.gov/search/granules.json?'+urllib.parse.urlencode(dict(collection_concept_id=r['concept_id'],page_size=0))) for r in records]
receipts=[];counts=[]
with ThreadPoolExecutor(max_workers=3) as pool:
    for r,(receipt,b) in zip(records,pool.map(fetch,jobs)):
        receipts.append(receipt);state='FETCH_ERROR_RETAIN_UNKNOWN';count='';returned='';error=receipt['error']
        if not error:
            try:
                d=json.loads(b);returned=len(d['feed']['entry']);count=int(receipt['cmr_hits']);assert count>=0 and returned==0
                state='PUBLIC_CMR_GRANULE_METADATA_COUNT_OBSERVED' if count else 'ZERO_PUBLIC_MATCHING_METADATA_NOT_PROOF_NO_IMAGERY'
            except (ValueError,KeyError,TypeError,AssertionError) as e:
                state='RESPONSE_SCHEMA_REVIEW';error=type(e).__name__;count=''
        counts.append(dict(concept_id=r['concept_id'],collection_revision=r['revision_id'],metadata_granule_count=count,
            result_state=state,returned_entries=returned,probe_scope='PUBLIC_NO_AREA_OR_TIME_FILTER_PAGE_SIZE_ZERO',
            file_download_verified=False,spatial_country_coverage_verified=False,all_history_complete=False,
            source_file=receipt['source_file'],source_sha256=receipt['sha256'],error=error))
license_urls=sorted({json.loads(r['use_constraints_json']).get('LicenseURL',{}).get('Linkage','') for r in records}-{''})
license_receipts={}
with ThreadPoolExecutor(max_workers=2) as pool:
    for url,(receipt,b) in zip(license_urls,pool.map(fetch,[('license_'+str(i),u) for i,u in enumerate(license_urls,1)])):
        receipts.append(receipt);license_receipts[url]=receipt
rights=[]
for r in records:
    u=json.loads(r['use_constraints_json']);a=json.loads(r['access_constraints_json']);url=u.get('LicenseURL',{}).get('Linkage','');q=license_receipts.get(url,{})
    flag=u.get('FreeAndOpenData','ABSENT');text=u.get('LicenseText','')
    if flag is False:state='SOURCE_EXPLICIT_NOT_FREE_AND_OPEN_REQUIRES_TERMS_REVIEW'
    elif text:state='INLINE_LICENSE_TEXT_REQUIRES_PRODUCT_SPECIFIC_REVIEW'
    elif url:state='LICENSE_REFERENCE_FETCHED_NEEDS_SEMANTIC_REVIEW' if q.get('source_file') else 'LICENSE_REFERENCE_FETCH_FAILED_RETAIN_UNKNOWN'
    else:state='NO_LICENSE_URL_OR_TEXT_NOT_PROOF_NO_RIGHTS'
    rights.append(dict(concept_id=r['concept_id'],revision_id=r['revision_id'],free_and_open_source_flag=str(flag),
        license_url=url,license_text=text,eula_identifiers_json=json.dumps(u.get('EULAIdentifiers',[])),
        all_use_constraints_json=r['use_constraints_json'],all_access_constraints_json=r['access_constraints_json'],
        rights_review_state=state,commercial_use_approved=False,license_source_file=q.get('source_file',''),
        license_source_sha256=q.get('sha256',''),license_http_status=q.get('http_status',''),
        catalog_source_file=r['source_file'],catalog_source_sha256=r['source_sha256']))
assert len(counts)==len(rights)==166 and len({r['concept_id'] for r in counts})==166
write('registry_all_166_granule_count_probes.csv',counts);write('registry_all_166_rights_evidence.csv',rights)
write('registry_source_receipts.csv',receipts)
work=[];prior=read(BT/'registry_per_collection_workqueue.csv');assert len(prior)==498
cm={r['concept_id']:r for r in counts};rm={r['concept_id']:r for r in rights}
for r in prior:
    t=r['task_type'];c=cm[r['concept_id']]
    progress='RIGHTS_METADATA_PARSED_NOT_LEGAL_CLEARANCE' if t=='PER_COLLECTION_RIGHTS' else (
        c['result_state']+'_AREA_TIME_AND_DOWNLOAD_PENDING' if t=='GRANULE_AVAILABILITY' else 'PRODUCT_SCHEMA_AND_VALUES_NOT_INSPECTED')
    work.append(dict(**r,b46_progress=progress,task_closed=False))
write('registry_all_498_work_progress.csv',work)
con=sqlite3.connect(T/'cmr_availability_b46.sqlite');sqlcounts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')')
    con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);sqlcounts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in sqlcounts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close()
assert all(sha(R/p)==h for p,h in protected.items())
assert all(sha(R/p)==h for p,h in b45_files.items())
stats=dict(collections=166,granule_probe_states=dict(collections.Counter(r['result_state'] for r in counts)),
    unique_license_urls=len(license_urls),license_fetch_successes=sum(bool(q['source_file']) for q in license_receipts.values()),
    source_requests=len(receipts),rights_states=dict(collections.Counter(r['rights_review_state'] for r in rights)),
    all_498_tasks_retained=True,tasks_closed=0,imagery_downloaded=False,commercial_use_approved=False,
    old_documents_preserved=True,b45_delivery_preserved=True,b45_original_baseline_refreshed=False,sqlite_counts=sqlcounts,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B46：全部166集合的公開影像目錄計數與逐集合授權證據"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 全集合查詢與業務意義

對B45全部166個ASF集合逐一執行官方CMR公開granule目錄計數，使用page_size=0不下載影像或granule清單。保存回應原始字節、HTTP標頭、CMR-Hits與時間。零筆、HTTP錯誤、schema不符分開，失敗保留未知而不填0。集合修訂為B45時點，granule計數為各次請求時點，不假稱同時或原子快照。

目錄筆數有助於資料選型與後續採樣預算，但不是實際成功下載數、獨立觀測數、影像品質或逐國覆蓋。未加時空篩選，因此不能回答指定設施／年代是否有影像。不同集合可能含版本或加工變體，不能加總作全球獨立影像總數。

## 166項授權欄位與來源

完整解析全部集合的UseConstraints、AccessConstraints、內嵌LicenseText、LicenseURL及EULAIdentifiers。91項來源標示FreeAndOpenData=true、2項false、73項未填該標記，保留原值；true不自动等於CC0或商用清關。所有唯一非空授權網址都嘗試下載，重定向及失敗如實記錄。

授權文本保留供逐產品核閱，本輪未作完整法律語意清關，沒有任何集合被自動准許商用。68項缺少LicenseURL亦不能被說成完全沒有授權資訊，因其他欄位可能存在條款。SSODv2的CC0不擴及本批產品。

## 清單進度与版本保留

'''+ '統計：`'+json.dumps(stats)+'`。\n\n'+'''
[全部166項目錄查詢](tables/70_cmr_availability_b46_20261009/registry_all_166_granule_count_probes.csv)、[全部166項授權證據](tables/70_cmr_availability_b46_20261009/registry_all_166_rights_evidence.csv)、[來源收據](tables/70_cmr_availability_b46_20261009/registry_source_receipts.csv)、[全部498項進度](tables/70_cmr_availability_b46_20261009/registry_all_498_work_progress.csv)、[SQLite](tables/70_cmr_availability_b46_20261009/cmr_availability_b46.sqlite)。查詢方式依[官方CMR文件](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html)。

B45原有文件、基線和publication_hold回執完整保留，本輪另記其交付雜湊以獨立覆核，沒有把舊失敗改寫為通過。開始時已有的Inteligent工作區修改不納入交付，提交前若再變動仍須中止。498項工作全部保留，不因目錄计數成功就結案。

下一步逐產品核正式條款，再對限定地區年代核granule清單與品質；測站25項未結、SSOD缺值、GSOD125筆風速衝突以及全球金融、工商、歷史政治實體待辦仍保持開放。SDG業務分析凍結，Untitled不恢復。
'''
(R/'Reference/CMR_Availability_B46_20261009.qmd').write_text(report,encoding='utf-8')
notes={'redteam':'CMR計數不證明可下載、逐國覆蓋或軍事能力；true開放標記不等於所有第三方權利放行。',
 'critic':'166項全部實測但未指定時空範圍；失敗與0分開，不宣稱完成全域影像驗收。',
 'killcritic':'逐集合請求及完整授權欄位有可重現價值，不應混為只列宣傳名單。',
 'blindspot':'版本加工可能重複；68項無URL不等於無條款；查詢與集合修訂不同時點。',
 'blueprint':'CMR集合→逐集合計數收據→授權來源與原文本→完整498項進度；保留B45原中止歷史。',
 'cheatsheet':'166集合全測；影像未下載、商用未核准、498項不自動結案。',
 'actionplan':'先核產品特定條款，再限定地區年代查granule與品質；其他全球清單保留。'}
for n,v in notes.items():(R/n/'cmr_availability_b46_20261009.md').write_text('# '+n+' | B46\n\n'+v+'\n\n[報告](../Reference/CMR_Availability_B46_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
