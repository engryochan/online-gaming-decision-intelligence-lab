from pathlib import Path
import csv,json,hashlib,subprocess,urllib.request,urllib.parse,datetime,sqlite3,re
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/74_platform_details_b51_20261011'
MAIN='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
assert not (O/'baseline.json').exists(),'Never refresh baseline'
T.mkdir();(O/'raw').mkdir()
paths=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0');original=(R/MAIN).read_bytes()
protected={p:sha((R/p).read_bytes()) for p in paths if p and Path(p).suffix in ('.md','.qmd') and (R/p).is_file()}
base=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),starting_status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected,authorized_append=dict(path=MAIN,prefix_bytes=len(original),prefix_sha256=sha(original)))
(O/'baseline.json').write_text(json.dumps(base,indent=2),encoding='utf-8')
class Text(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style') and self.skip:self.skip-=1
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)
def fetch(spec):
    sid,url,kind,key=spec
    rec=dict(source_id=sid,url=url,final_url='',fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',source_file='',sha256='',response_sha256='',response_bytes='',error='',api_error_code='',visible_keyword_present=False,short_excerpt='',evidence_scope='NEW_FETCH' if kind=='JSON' else 'RESPONSE_HASH_BOUNDED_EXCERPT')
    obj=None
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PublicResearchRegistry/1.0'}),timeout=25) as response:b=response.read(12000001);rec.update(http_status=response.status,final_url=response.url)
        assert len(b)<=12000000
        rec.update(response_sha256=sha(b),response_bytes=len(b))
        if kind=='JSON':
            obj=json.loads(b);p=O/'raw'/(sid+'.json');p.write_bytes(b);rec.update(source_file=p.relative_to(R).as_posix(),sha256=sha(b))
            if 'error' in obj:rec['api_error_code']=obj['error'].get('code','UNKNOWN')
        else:
            parser=Text();parser.feed(b.decode('utf-8','replace'));txt=' '.join(' '.join(parser.parts).split());m=re.search(re.escape(key),txt,re.I);rec['visible_keyword_present']=bool(m)
            if m:rec['short_excerpt']=' '.join(txt[max(0,m.start()-25):m.start()+180].split()[:15])
    except Exception as e:rec.update(error=type(e).__name__,http_status=getattr(e,'code',rec['http_status']))
    return rec,obj
receipts=[];catalog=[];pages=[];start=1;seen=set();totals=set()
while True:
    url='https://www.arcgis.com/sharing/rest/search?'+urllib.parse.urlencode(dict(f='json',q='owner:esri AND type:"Feature Service"',num=20,start=start,sortField='modified',sortOrder='desc'))
    rec,obj=fetch((f'B51PAGE{start:03}',url,'JSON',''));receipts.append(rec)
    assert obj and not rec['api_error_code'] and not rec['error'],'Catalog page failed; do not claim reconciliation'
    totals.add(obj['total']);assert len(totals)==1,'Live index changed totals; review before continuation'
    pages.append(dict(start=start,total=obj['total'],returned=len(obj['results']),next_start=obj['nextStart'],source_file=rec['source_file'],source_sha256=rec['sha256']))
    for item in obj['results']:
        assert item['id'] not in seen and item['owner'].lower()=='esri' and item['type']=='Feature Service';seen.add(item['id'])
        catalog.append(dict(item_id=item['id'],title=item['title'],owner=item['owner'],item_type=item['type'],full_item_json=json.dumps(item,ensure_ascii=False),source_file=rec['source_file'],source_sha256=rec['sha256']))
    if obj['nextStart']==-1:break
    assert obj['nextStart']>start;start=obj['nextStart'];assert start<1000
assert len(catalog)==next(iter(totals))
old=read(R/'Reference/tables/73_commercial_ecosystem_b50_20261011/registry_esri_catalog_sample.csv')
comparison=[dict(item_id=r['item_id'],present_in_b51=r['item_id'] in seen,prior_source_sha256=r['source_sha256']) for r in old]
write('registry_esri_catalog.csv',catalog);write('registry_page_reconciliation.csv',pages);write('registry_b50_identity_comparison.csv',comparison)
specs=[('B51ITEM'+r['item_id'],'https://www.arcgis.com/sharing/rest/content/items/'+r['item_id']+'?f=json','JSON','') for r in catalog]
details=[];items={}
with ThreadPoolExecutor(max_workers=3) as pool:
    for r,(rec,obj) in zip(catalog,pool.map(fetch,specs)):
        receipts.append(rec);ok=obj is not None and not rec['error'] and not rec['api_error_code']
        if ok:assert obj['id']==r['item_id'];items[r['item_id']]=obj
        details.append(dict(item_id=r['item_id'],title=r['title'],fetch_state='ITEM_METADATA_FETCHED' if ok else 'FAILED_OR_API_ERROR',access=obj.get('access') if ok else None,license_info_json=json.dumps(obj.get('licenseInfo') if ok else None,ensure_ascii=False),access_information_json=json.dumps(obj.get('accessInformation') if ok else None,ensure_ascii=False),type_keywords_json=json.dumps(obj.get('typeKeywords') if ok else None),full_item_json=json.dumps(obj,ensure_ascii=False),source_file=rec['source_file'],source_sha256=rec['sha256'],rights_adjudication='TERMS_TEXT_RECORDED_NOT_BLANKET_COMMERCIAL_CLEARANCE'))
write('registry_esri_item_terms.csv',details)
service_specs=[]
for r in old:
    item=items.get(r['item_id'],{});url=item.get('url','');host=urllib.parse.urlparse(url).hostname or ''
    if url.startswith('https://') and (host.endswith('.arcgis.com') or host.endswith('.arcgisonline.com')) and '/FeatureServer' in url:
        service_specs.append(('B51SERVICE'+r['item_id'],url+'?f=json','JSON',''))
services=[]
with ThreadPoolExecutor(max_workers=3) as pool:
    for spec,(rec,obj) in zip(service_specs,pool.map(fetch,service_specs)):
        receipts.append(rec);ok=obj is not None and not rec['error'] and not rec['api_error_code']
        services.append(dict(item_id=spec[0].removeprefix('B51SERVICE'),url=spec[1],http_status=rec['http_status'],api_error_code=rec['api_error_code'],state='PUBLIC_SERVICE_METADATA_FETCHED' if ok else 'SERVICE_METADATA_UNAVAILABLE_NO_AUTH_RETRY',max_record_count=obj.get('maxRecordCount') if ok else None,capabilities=obj.get('capabilities') if ok else None,layers_json=json.dumps(obj.get('layers') if ok else None),full_service_json=json.dumps(obj,ensure_ascii=False),source_file=rec['source_file'],source_sha256=rec['sha256'],features_downloaded=False))
if services:write('registry_esri_service_schema.csv',services)
docs=[('B51STARSHIELD','https://new.spacex.com/starshield','HTML','Earth Observation'),('B51GROKMODELS','https://docs.x.ai/developers/models','HTML','grok-4.7'),('B51GROKSECURITY','https://docs.x.ai/developers/faq/security','HTML','API'),('B51METEORESERVED','https://www.meteomatics.com/en/api/response/reserved-values/','HTML','-999'),('B51METEOMODELS','https://www.meteomatics.com/en/api/request/optional-parameters/data-source/','HTML','mix'),('B51METEOWIND','https://www.meteomatics.com/en/api/available-parameters/weather-parameter/standard-weather-parameters-wind/','HTML','wind_speed'),('B51METEOREQUEST','https://www.meteomatics.com/en/api/request/','HTML','parameters')]
with ThreadPoolExecutor(max_workers=3) as pool:
    for rec,obj in pool.map(fetch,docs):receipts.append(rec)
write('registry_source_receipts.csv',receipts)
rm={r['source_id']:r for r in receipts}
definitions=[('Meteomatics','-999','數據不可取得，保留原值及缺值原因','B51METEORESERVED'),('Meteomatics','-888','參數特定保留值，需按該參數解讀','B51METEORESERVED'),('Meteomatics','-777','參數特定保留值，需按該參數解讀','B51METEORESERVED'),('Meteomatics','-666','情境不適用，不能補成零','B51METEORESERVED'),('Meteomatics','mix','多來源混合；不等於固定單一模式或原始站點觀測','B51METEOMODELS'),('Meteomatics','model','指定資料來源；保留初始化、有效時間及模式版本','B51METEOMODELS'),('Meteomatics','parameter:unit','參數及單位編碼需原樣保存，不把不同高度和區間混用','B51METEOREQUEST'),('Meteomatics','wind_speed_<level>:<unit>','風速的高度及單位需依官方參數文件選擇','B51METEOWIND'),('Grok / xAI','grok-4.7','當期官網列示模型；版本與價格需按查證時間保存，非實測性能','B51GROKMODELS'),('Grok / xAI','Web Search / X Search','即時資訊需啟用相應工具；模型記憶不是最新資料來源','B51GROKMODELS'),('Grok / xAI','model alias','別名可能更新；可重現研究應記錄實際版本與回應資訊','B51GROKMODELS'),('Grok / xAI','API governance','API治理文件與消費者Grok政策分开核；本批沒有接受條款或建立帳戶','B51GROKSECURITY'),('Starshield / 星盾','Earth Observation','官方索引產品主張：觀測酬載與處理數據交付；沒有公共影像API證據','B51STARSHIELD'),('Starshield / 星盾','Communications','官方索引政府通信產品主張，不能等同Starlink消費者套餐','B51STARSHIELD'),('Starshield / 星盾','Hosted Payloads','官方索引衛星平台／搭載酬載產品主張；不推論已取得任何客戶數據','B51STARSHIELD')]
defs=[]
for org,key,meaning,sid in definitions:
    rec=rm[sid];defs.append(dict(organization=org,field_or_product=key,business_definition=meaning,source_id=sid,url=rec['url'],evidence_state='OFFICIAL_DOCUMENT_MANUAL_REVIEW_NOT_API_BENCHMARK' if rec['visible_keyword_present'] else 'DOCUMENT_REVIEW_WITH_LOCAL_FETCH_GAP_NO_CAPABILITY_VERIFICATION',local_visible_keyword_present=rec['visible_keyword_present'],source_response_sha256=rec['response_sha256']))
write('registry_product_definitions.csv',defs)
for name in ['registry_commercial_products.csv','registry_product_workqueue.csv','registry_preserved_498_asf_work.csv']:
    rows=read(R/'Reference/tables/73_commercial_ecosystem_b50_20261011'/name);write('preserved_'+name,rows)
con=sqlite3.connect(T/'platform_details_b51.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);ks=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in ks)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in ks)+')',[[r[k] for k in ks] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close();assert all(sha((R/p).read_bytes())==h for p,h in protected.items())
stats=dict(esri_query_total=len(catalog),catalog_pages=len(pages),item_terms_success=sum(r['fetch_state']=='ITEM_METADATA_FETCHED' for r in details),item_terms_failures=sum(r['fetch_state']!='ITEM_METADATA_FETCHED' for r in details),service_queries=len(services),service_metadata_success=sum(r['state']=='PUBLIC_SERVICE_METADATA_FETCHED' for r in services),source_receipts=len(receipts),document_fetch_gaps=[r['source_id'] for r in receipts if r['evidence_scope']!='NEW_FETCH' and not r['visible_keyword_present']],http_failures=sum(bool(r['error']) for r in receipts),api_errors=sum(bool(r['api_error_code']) for r in receipts),definitions=len(defs),previous_20_ids_preserved=all(r['present_in_b51'] for r in comparison),sqlite_counts=counts,features_downloaded=False,paid_or_private_api_called=False,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
report='''---
title: "B51：星盾、Grok／xAI及ArcGIS、Meteomatics資料定義"
date: 2026-10-11
lang: zh-TW
format:
  html:
    toc: true
    embed-resources: true
---

## 星盾與Grok／xAI增補

使用者已確認「星頓」所指為星盾Starshield；不新增錯誤同名法人。[SpaceX官方Starshield入口](https://new.spacex.com/starshield)的搜尋索引列示地球觀測、通信與搭載酬載產品主張。實際頁面取用若失敗或不可讀，收據與定義表清楚標記缺口，不能升格為已核實部署、性能、公共API或全球覆蓋。以公開政府宇航產品與工業供應鏈研究為用途，未取得政府或機密資料。

[Grok官方模型文件](https://docs.x.ai/developers/models)列示當期模型與不同文字、影像、語音產品，並說明即時資料需要搜尋工具，別名可能更動。新增模型時態、搜尋工具及版本重現要求；不把生成文字當作地緣事实證據。xAI、SpaceXSI品牌、Grok產品與法律實體繼續分欄；本批沒有核定持股或併購結論。[API治理文件](https://docs.x.ai/developers/faq/security)保留官方入口與取用證據，不外推至消費者產品條款。本批未呼叫付費API或建立帳戶。

## ArcGIS逐item條款及服務結構

重新執行B50的owner:esri AND type:Feature Service有界查詢，依nextStart翻至-1並對賬total及唯一item ID；不是全部Esri或全球GIS清單。全部該查詢item嘗試詳細元資料，保留licenseInfo、accessInformation、typeKeywords及完整JSON，缺少條款保持null，不補作無限制授權。B50最初20個item另嘗試公開服務根結構，記錄maxRecordCount、capabilities、layers與API錯誤；HTTP 200帶token錯誤不算取得schema。未取feature內容，不重試身份驗證。服務根layers名錄不是逐layer fields、幾何或完整資料驗收。

每頁請求不是原子快照；total稳定与ID對賬只證明這次查詢觀測的完整性，不能證明全部資料永久不變。B50第一頁歷史證據保留，前20項身份比較另表登記。

## Meteomatics語意校對

依[保留值文件](https://www.meteomatics.com/en/api/response/reserved-values/)，-999表示不可取得、-666表示情境不適用，-888及-777須按參數定義解釋；全部保留原值及原因，不能補零或當作真實氣象數值。[模型來源文件](https://www.meteomatics.com/en/api/request/optional-parameters/data-source/)區分mix混合與指定來源。[風參數](https://www.meteomatics.com/en/api/available-parameters/weather-parameter/standard-weather-parameters-wind/)及[請求文件](https://www.meteomatics.com/en/api/request/)要求保留高度、單位與區間，避免把不同物理量合併。這是官方文件語意登記，尚未取得付費時序樣本、驗證誤差或核完商業再分發條款。

## 本輪實測與交付

'''+json.dumps(stats,ensure_ascii=False)+'''。

[完整有界ArcGIS目錄](tables/74_platform_details_b51_20261011/registry_esri_catalog.csv)、[逐item條款](tables/74_platform_details_b51_20261011/registry_esri_item_terms.csv)、[服務結構](tables/74_platform_details_b51_20261011/registry_esri_service_schema.csv)、[產品與參數定義](tables/74_platform_details_b51_20261011/registry_product_definitions.csv)、[來源收據](tables/74_platform_details_b51_20261011/registry_source_receipts.csv)、[SQLite](tables/74_platform_details_b51_20261011/platform_details_b51.sqlite)。

前輪27產品群、108待辦與498項ASF工作完整保留，沒有用本批部分元資料結清全球企業、歷史、金融或神經技術缺口。下一步按逐item具體權利條款決定歷史小樣本，再取公開layer fields、空間參考、時間欄位及缺值規則。影像品質、全球覆蓋、使用授權與部署性能依然待核。原宇航報告及使用者版本保留；SDG分析凍結，Untitled不恢復。
'''
(R/'Reference/Platform_Details_B51_20261011.qmd').write_text(report,encoding='utf-8')
append='\n\n<!-- PLATFORM_DETAILS_B51_20261011_BEGIN -->\n## 2026-10-11 星盾、Grok／xAI與平台資料定義 B51\n\n「星頓」經使用者澄清為星盾Starshield。新增[星盾與Grok／xAI、ArcGIS及Meteomatics核查報告](Platform_Details_B51_20261011.qmd)及[產品定義表](tables/74_platform_details_b51_20261011/registry_product_definitions.csv)，包含有界ArcGIS目錄分頁對賬、逐item條款與服務結構、Meteomatics保留值與參數語意、Grok版本與搜尋資訊要求。原文位元保留；未取得付費、私人或機密資料，未核准跨產品商用再分發。\n<!-- PLATFORM_DETAILS_B51_20261011_END -->\n'
(R/MAIN).write_bytes(original+append.encode('utf-8'))
(O/'append_receipt.json').write_text(json.dumps(dict(path=MAIN,prefix_bytes=len(original),prefix_sha256=sha(original),append_sha256=sha(append.encode('utf-8'))),indent=2),encoding='utf-8')
notes={'redteam':'HTTP成功帶API錯誤不能算schema取用；授權不可從public可見性推論。','critic':'有界Esri查詢全頁對賬不是全球GIS全量；服務根不等於layer完整欄位。','killcritic':'逐item條款、來源指紋、API錯誤與保留值語意，使後續核查具體可驗。','blindspot':'星盾與星鏈分列；Grok別名更動、模型時間與氣象缺值必須追溯。','blueprint':'目錄分頁→item條款→公開服務根→語意定義→授權歷史layer樣本。','cheatsheet':'-999不可取得；-666不適用；-888/-777參數特定；不可補零。','actionplan':'按具體條款選歷史layer，核fields、空間參考、時間與缺值，再做成本品質持出測試。'}
for n,v in notes.items():(R/n/'platform_details_b51_20261011.md').write_text('# '+n+' | B51\n\n'+v+'\n\n[報告](../Reference/Platform_Details_B51_20261011.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
