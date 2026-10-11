from pathlib import Path
import csv,json,hashlib,subprocess,urllib.request,datetime,sqlite3,collections
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/71_product_terms_b48_20261011'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
assert not (O/'baseline.json').exists(),'Never refresh a baseline'
T.mkdir();(O/'raw').mkdir()
paths=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
protected={p:sha(R/p) for p in paths if p and Path(p).suffix in ('.md','.qmd') and (R/p).is_file()}
(O/'baseline.json').write_text(json.dumps(dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),starting_status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected),indent=2)+'\n',encoding='utf-8')
prior=read(R/'Reference/tables/70_cmr_availability_b46_20261009/registry_all_166_rights_evidence.csv')
original={r['concept_id']:r for r in read(R/'Reference/tables/69_cmr_asf_b45_20261009/registry_all_asf_collections.csv')}
selected=[r for r in prior if r['license_text'] or r['free_and_open_source_flag']=='False'];assert len(selected)==14
def fetch(r):
    cid=r['concept_id'];rev=r['revision_id'];url=f'https://cmr.earthdata.nasa.gov/search/concepts/{cid}/{rev}.umm_json'
    receipt=dict(concept_id=cid,revision_id=rev,url=url,fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_file='',sha256='',http_status='',error='')
    obj=None
    try:
        with urllib.request.urlopen(url,timeout=20) as response:b=response.read(5000001);receipt['http_status']=response.status
        assert len(b)<=5000000
        obj=json.loads(b);assert obj['ShortName']==original[cid]['short_name']
        p=O/'raw'/(cid+'.json');p.write_bytes(b);receipt.update(source_file=p.relative_to(R).as_posix(),sha256=sha(p))
    except Exception as e:receipt.update(error=type(e).__name__,http_status=getattr(e,'code',receipt['http_status']));obj=None
    return receipt,obj
receipts=[];results={}
with ThreadPoolExecutor(max_workers=2) as pool:
    for r,(receipt,obj) in zip(selected,pool.map(fetch,selected)):
        receipts.append(receipt);results[r['concept_id']]=(receipt,obj)
rules={
 'RTC':[
 ('NAMED_PRODUCT_SCOPE','Applies to ALOS PALSAR RTC products, not automatically to original raw data'),
 ('USE_PERMISSION','Named RTC use is described as unrestricted, subject to other explicit agreement clauses'),
 ('COPYRIGHT_RETENTION','Do not remove, obscure or alter existing copyright notices'),
 ('NASA_JAXA_METI_NOTICE','Carry the specified NASA notice including JAXA/METI material and acquisition year'),
 ('VAP_DISTINCTION','Value-added product requires irreversible high-level processing under this definition'),
 ('NO_WARRANTY','Source disclaims product correctness and fitness'),
 ('MODIFICATION','Agreement reserves future modification; pinned revision is historical evidence')],
 'JAXA':[
 ('ORIGINAL_RIGHTS','Original data intellectual property rights remain with JAXA'),
 ('VAP_DISTINCTION','High-level irreversible processing defines a value-added product'),
 ('VAP_CREDIT','Publication or redistribution of generated VAP requires source-provider credit'),
 ('RESULTS_COPYRIGHT','Published direct or indirect results require JAXA notice and acquisition year'),
 ('NO_WARRANTY','Quality and timely provision are not guaranteed'),
 ('RAW_REEXPORT_UNKNOWN','This excerpt does not explicitly resolve every commercial raw-data re-export use')],
 'ERS':[
 ('OWNERSHIP','ESA ownership remains acknowledged'),
 ('MARK_REPRODUCTIONS','Reproductions require clearly visible data credit or image copyright'),
 ('DATA_IMAGE_NOTICE','Different source templates apply to data and images; include acquisition/access dates where specified'),
 ('NO_WARRANTY','Suitability and consequential uses are not guaranteed'),
 ('ACCESS_ACCEPTANCE','Agreement discusses access upon acceptance; this metadata fetch does not accept a download EULA')]
}
profiles=[];obligations=[]
def norm(t):return ' '.join(t.split())
for r in prior:
    cid=r['concept_id'];text=r['license_text'];family='NO_INLINE_TERMS_REVIEWED'
    if text.startswith('ALOS PALSAR RTC Product License'):family='RTC'
    elif text.strip().startswith('ALOS/PALSAR/AVNIR-2'):family='JAXA'
    elif text.startswith('ESA ERS-1 and ERS-2'):family='ERS'
    elif text:raise AssertionError('Unreviewed inline family')
    evidence='B46_CARRIED_NOT_REFETCHED';receipt={};text_match='NOT_REFETCHED';flag_match='NOT_REFETCHED'
    if cid in results:
        receipt,obj=results[cid]
        evidence='B48_PINNED_REVISION_FETCHED' if obj else 'B48_FETCH_FAILED_PRIOR_EVIDENCE_RETAINED'
        if obj:
            u=obj.get('UseConstraints',{});text_match=norm(u.get('LicenseText',''))==norm(text)
            flag_match=str(u.get('FreeAndOpenData','ABSENT'))==r['free_and_open_source_flag']
            assert text_match and flag_match,'Pinned revision discrepancy requires review before classifying'
    state='INLINE_OBLIGATIONS_PARSED_SCOPE_REVIEW_OPEN' if family in rules else r['rights_review_state']
    if r['free_and_open_source_flag']=='False':state='EXPLICIT_NONOPEN_FLAG_HELD_FOR_PRODUCT_SPECIFIC_TERMS'
    profiles.append(dict(concept_id=cid,revision_id=r['revision_id'],short_name=original[cid]['short_name'],
        prior_rights_state=r['rights_review_state'],current_rights_state=state,inline_terms_family=family,
        source_free_and_open_flag=r['free_and_open_source_flag'],evidence_batch=evidence,
        pinned_revision_terms_match=text_match,pinned_revision_open_flag_match=flag_match,
        original_license_text=text,original_use_constraints_json=r['all_use_constraints_json'],
        new_source_file=receipt.get('source_file',''),new_source_sha256=receipt.get('sha256',''),
        prior_source_file=r['catalog_source_file'],prior_source_sha256=r['catalog_source_sha256'],
        commercial_raw_redistribution_approved=False,imagery_downloaded=False,eula_accepted=False))
    for code,meaning in rules.get(family,[]):
        obligations.append(dict(concept_id=cid,revision_id=r['revision_id'],family=family,obligation_code=code,
            business_definition=meaning,assessment='MANUAL_SOURCE_TEXT_SCOPE_REVIEW_NOT_BLANKET_LEGAL_CLEARANCE',
            inline_text_sha256=hashlib.sha256(text.encode('utf-8')).hexdigest(),
            original_text_file=r['catalog_source_file'],original_file_sha256=r['catalog_source_sha256'],
            refreshed_pinned_source_file=receipt.get('source_file','')))
assert len(profiles)==166
write('registry_all_166_product_terms_status.csv',profiles)
write('registry_inline_product_obligations.csv',obligations);write('registry_source_receipts.csv',receipts)
work=read(R/'Reference/tables/70_cmr_availability_b46_20261009/registry_all_498_work_progress.csv')
pm={r['concept_id']:r for r in profiles}
for r in work:
    r['b48_terms_progress']=pm[r['concept_id']]['current_rights_state'] if r['task_type']=='PER_COLLECTION_RIGHTS' else 'B46_PROGRESS_RETAINED_NO_NEW_AVAILABILITY_OR_VALUE_ANALYSIS'
    r['task_closed']='False'
assert len(work)==498;write('registry_all_498_work_progress.csv',work)
con=sqlite3.connect(T/'product_terms_b48.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);keys=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in keys)+')')
    con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close();assert all(sha(R/p)==h for p,h in protected.items())
stats=dict(collections_retained=166,pinned_revision_queries=14,fetch_errors=sum(bool(r['error']) for r in receipts),
    inline_families=dict(collections.Counter(r['inline_terms_family'] for r in profiles)),obligation_rows=len(obligations),
    explicit_nonopen_held=2,prior_other_collections_not_refetched=152,all_498_work_retained=True,tasks_closed=0,
    raw_redistribution_approved=False,imagery_downloaded=False,eula_accepted=False,sqlite_counts=counts,
    old_documents_preserved=True,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B48：產品特定條款義務與166集合最新狀態"
date: 2026-10-11
format:
  html:
    toc: true
    embed-resources: true
---

## 來源時態與範圍

針對12項有內嵌條款及2項明示非開放集合，依[CMR指定修訂端點](https://cmr.earthdata.nasa.gov/search/site/docs/search/api.html)重取B45所登記revision的完整UMM，核對ShortName、條款與開放標記；原始JSON、時間及SHA256保留。這是固定修訂版本覆核，不是宣稱最新法律條款或同時重新掃描全部166集合。其餘152項清楚標為沿用B46未重新下載。

## 三類產品條款分列

ALOS RTC的條款描述允許具名RTC產品使用，同时要求保留版權與NASA／JAXA／METI通知，不能把這段具名產品許可套用到所有原始數據。JAXA ALOS內嵌條款保留原數據權利，區分不可逆高階處理的增值產品及發布署名；本文不把未明定用途自行補成自由原始資料轉售。ESA ERS條款保留ESA所有權，要求重製時明顯標示數據信用／影像版權。三類文本均有免責條件，義務明細逐集合記錄；讀取元資料沒有接受下載EULA。

2項JERS集合的FreeAndOpenData=false原值保持，沒有因其公開目錄筆數非零而解除限制。缺少內嵌文本也不是無權利或無條款的證明。對各類商用、原始／增值重分發仍保留具體用途待核，不發出跨集合授權清關結論。

## 完整清單與交付

'''+ '統計：`'+json.dumps(stats)+'`。\n\n'+'''
[全部166項狀態](tables/71_product_terms_b48_20261011/registry_all_166_product_terms_status.csv)、[逐產品義務](tables/71_product_terms_b48_20261011/registry_inline_product_obligations.csv)、[14項來源收據](tables/71_product_terms_b48_20261011/registry_source_receipts.csv)、[全部498項進度](tables/71_product_terms_b48_20261011/registry_all_498_work_progress.csv)、[SQLite](tables/71_product_terms_b48_20261011/product_terms_b48.sqlite)。原始文本在狀態表與來源記錄保留，不覆寫B45／B46表或用户報告。

下一步為具體產品／用途核完整當期條款，再在指定地區及歷史時段查granule與品質。本輪沒有下載影像、核准原始資料商業轉售或結清498項工作；氣象身份／缺值與全球金融、工商、歷史政治實體清單繼續保留。SDG業務分析凍結，Untitled不恢復。
'''
(R/'Reference/Product_Terms_B48_20261011.qmd').write_text(report,encoding='utf-8')
notes={'redteam':'開放旗標與具名產品授權不外推至原始資料自由轉售。','critic':'固定修訂14項不是全部166項當期授權重新審查。',
 'killcritic':'保留原文及逐產品義務，使公開目錄從旗標升級為可審查的用途證據。','blindspot':'RTC、原始ALOS、ERS與JERS不可套一項政策；變更條款与免責仍存在。',
 'blueprint':'修訂元資料→原條款與旗標核對→逐產品義務→166項状态及498項待辦。','cheatsheet':'14項重取；152項沿用；2項非開放保留；沒有影像下載或EULA接受。',
 'actionplan':'具體用途核當期條款，再取限定歷史時空granule與品質，其他全球工作保留。'}
for n,v in notes.items():(R/n/'product_terms_b48_20261011.md').write_text('# '+n+' | B48\n\n'+v+'\n\n[報告](../Reference/Product_Terms_B48_20261011.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
