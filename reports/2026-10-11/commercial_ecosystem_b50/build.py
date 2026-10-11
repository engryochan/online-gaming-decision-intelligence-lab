from pathlib import Path
import csv,json,hashlib,subprocess,urllib.request,urllib.parse,datetime,sqlite3,re
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/73_commercial_ecosystem_b50_20261011'
MAIN='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rs):
    assert rs
    with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
assert not (O/'baseline.json').exists(),'Never refresh baseline'
T.mkdir();(O/'raw').mkdir()
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
protected={p:sha((R/p).read_bytes()) for p in tracked if p and Path(p).suffix in ('.md','.qmd') and (R/p).is_file()}
original=(R/MAIN).read_bytes()
base=dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),starting_status=subprocess.check_output(['git','status','--porcelain'],cwd=R).decode(),protected=protected,authorized_append=dict(path=MAIN,prefix_bytes=len(original),prefix_sha256=sha(original)))
(O/'baseline.json').write_text(json.dumps(base,indent=2),encoding='utf-8')
# Official entry points; product labels are research candidates, not proof of deployment.
manifest=[
('SpaceX','Falcon 9 / Starship','LAUNCH','https://www.spacex.com/','SpaceX','發射服務、載具及任務文件','載荷集成與發射成本研究'),
('SpaceX','Rideshare','LAUNCH_INTEGRATION','https://rideshare.spacex.com/','Rideshare','軌道、載荷質量、公開詢價入口','商業衛星發射選型；報價不是已簽合同'),
('SpaceX','Starshield','GOVERNMENT_SPACE','https://www.spacex.com/starshield','Starshield','公開政府宇航產品說明','公開國防工業產品登記；合同與資料存取另核'),
('Starlink','Aviation','SATELLITE_CONNECTIVITY','https://www.starlink.com/business/aviation','aviation','航空通信服務與安裝文件入口','民航連線與韌性比較'),
('Starlink','Maritime','SATELLITE_CONNECTIVITY','https://www.starlink.com/business/maritime','maritime','海事通信服務入口','商船通信成本及可用性研究'),
('Starlink','Direct to Cell / Mobile','MOBILE_CONNECTIVITY','https://www.starlink.com/bs/business/direct-to-cell','cell','移動通信產品與營運商入口','逐國營運商、頻譜及可用服務需核'),
('Palantir','Foundry / AIP / Apollo / Gotham','DATA_AI_DEPLOYMENT','https://www.palantir.com/docs/foundry/architecture-center/platforms','Foundry','平台架構、Ontology、資料治理與部署文件','產業資料整合；不是全球情報資料開放庫'),
('Palantir','Foundry API','DATA_INTEGRATION','https://www.palantir.com/docs/foundry/api/general/overview','API','API文件；租戶資料與授權範圍另定','欄位血緣、整合成本及權限模型'),
('Palantir','Gotham','DEFENSE_ANALYTICS','https://www.palantir.com/platforms/gotham/','Gotham','公開產品入口','國防軟體產業分類；沒有取得客戶資料'),
('Palantir','Warp Speed','MANUFACTURING','https://www.palantir.com/offerings/warp-speed/','manufacturing','製造業方案入口','工業供應鏈流程候選，部署與ROI待核'),
('Esri','ArcGIS defense and intelligence','GIS_PLATFORM','https://www.esri.com/en-us/industries/defense-intelligence/overview','GIS','官方國防及情報GIS產業說明','公開產業鏈與GIS方法登記'),
('Esri','ArcGIS Living Atlas','GEOSPATIAL_CATALOG','https://www.esri.com/arcgis-blog/products/arcgis-living-atlas/mapping/living-atlas-subscriber-content-public-apps','subscriber','公眾、訂戶與premium圖層使用說明','逐圖層權利、credits及資料時效需核'),
('Esri','Feature Service Query','GIS_API','https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service-layer/','resultOffset','分頁、幾何及欄位查詢文件','全量對賬需處理分頁與服務上限'),
('Meteomatics','Weather API','WEATHER_DATA','https://www.meteomatics.com/en/api/getting-started/','NetCDF','历史、觀測、預報及WMS/WFS文件','災害韌性與航空天氣；API需授權'),
('Meteomatics','Models / Mix / EURO1k / US1k','WEATHER_MODEL','https://www.meteomatics.com/en/weather-api/','EURO1k','多模型及自有模型產品描述','模型、下采樣與原生解析度不能混為實測精度'),
('Meteomatics','ArcGIS and language connectors','WEATHER_INTEROPERABILITY','https://www.meteomatics.com/en/api/data-connectors/','ArcGIS','GIS及程式語言連接文件','工具兼容性與資料授權分開核'),
('Tesla','Megapack','ENERGY_STORAGE','https://www.tesla.com/megapack','Megapack','儲能產品入口','基礎設施能源韌性；不推論軍方部署'),
('x.ai / current site brand','Grok API','AI_SERVICE','https://docs.x.ai/overview','API','模型與API開發文件','AI摘要與資料流程候選；內容不等於事实證據'),
('x.ai / current site brand','Brand and legal footer','CORPORATE_IDENTITY','https://x.ai/','SpaceXAI','網站當期品牌及法律頁入口','品牌與法人、持股及併購生效日需分別核證'),
('Neuralink','Brain computer interface','NEUROTECHNOLOGY','https://neuralink.com/','Neuralink','公開腦機介面入口','人體試驗與監管另核；不推論遠程心靈相通'),
('The Boring Company','Prufrock / Loop / Tunnels','INFRASTRUCTURE','https://www.boringcompany.com/','Prufrock','掘進、交通與隧道產品說明','交通與公用設施產業研究；工程性能待獨立驗證'),
('Airbus','Space','AEROSPACE_INDUSTRY','https://www.airbus.com/en/products-services/space','space','宇航產品與服務入口','商業宇航及供應鏈候選'),
('Planet','Earth observation','COMMERCIAL_EO','https://www.planet.com/','Planet','商業地球觀測入口','與開放遙感做歷史品質與授權比較'),
('ICEYE','SAR and disaster solutions','COMMERCIAL_SAR','https://www.iceye.com/','SAR','雷達與災害服務入口','洪水與災害韌性候選，沒有取得SAR影像'),
('BlackSky','Earth observation analytics','COMMERCIAL_EO','https://www.blacksky.com/','BlackSky','商業觀測分析入口','供應商分類；沒有取得受限資料'),
('Rocket Lab','Launch and space systems','SPACE_COMPONENTS','https://www.rocketlabusa.com/','space','發射與宇航系統入口','載具、衛星與組件產業鏈候選'),
('Spire','Space based data services','SPACE_DATA','https://spire.com/','weather','太空資料服務入口','氣象資料與商業服務比較候選')]
(O/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
class Text(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style') and self.skip:self.skip-=1
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)
def fetch(pair):
    i,m=pair;org,product,role,url,key,fields,value=m
    receipt=dict(source_id=f'B50S{i:03}',url=url,final_url='',fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',response_sha256='',response_bytes='',visible_keyword_present=False,short_excerpt='',source_file='',sha256='',error='',evidence_scope='PAGE_RESPONSE_HASH_AND_BOUNDED_EXCERPT_ONLY')
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PublicResearchRegistry/1.0'}),timeout=25) as response:
            b=response.read(12000001);receipt.update(http_status=response.status,final_url=response.url)
        assert len(b)<=12000000
        parser=Text();parser.feed(b.decode('utf-8','replace'));txt=' '.join(' '.join(parser.parts).split());match=re.search(re.escape(key),txt,re.I)
        receipt.update(response_sha256=sha(b),response_bytes=len(b),visible_keyword_present=bool(match))
        if match:receipt['short_excerpt']=' '.join(txt[max(0,match.start()-30):match.start()+180].split()[:15])
    except Exception as e:receipt.update(error=type(e).__name__,http_status=getattr(e,'code',receipt['http_status']))
    return receipt
with ThreadPoolExecutor(max_workers=3) as pool:receipts=list(pool.map(fetch,enumerate(manifest,1)))
products=[];work=[]
for i,(m,rec) in enumerate(zip(manifest,receipts),1):
    org,product,role,url,key,fields,value=m;pid=f'B50P{i:03}'
    state='OFFICIAL_VISIBLE_TEXT_TOKEN_OBSERVED_NOT_CAPABILITY_VERIFIED' if rec['visible_keyword_present'] else 'HTTP_RESPONSE_WITHOUT_EXPECTED_VISIBLE_TEXT' if not rec['error'] else 'FETCH_FAILED_CONTENT_UNVERIFIED'
    products.append(dict(product_id=pid,organization_display=org,product_group=product,industry_role=role,source_id=rec['source_id'],official_url=url,evidence_state=state,candidate_data_fields=fields,business_value_hypothesis=value,legal_entity_verified=False,parent_ownership_verified=False,global_country_coverage='UNKNOWN_NOT_MEASURED',contracts_deployments='UNKNOWN_NOT_REVIEWED',performance='UNKNOWN_NOT_BENCHMARKED',data_rights='PRODUCT_AND_DATASET_TERMS_REVIEW_REQUIRED',private_data_ingested=False,revenue_verified=False))
    for task,acceptance in [('IDENTITY','官方法人文件與關係生效日期；不能只靠共同創辦人'),('RIGHTS','逐產品、圖層或模型之條款、商用及重分發範圍'),('DATA','授權歷史樣本之schema、時間空間、品質與分頁對賬'),('VALUE','指定用途持出測試、總成本與客戶驗收')]:
        work.append(dict(task_id=pid+'_'+task,product_id=pid,task_type=task,status='OPEN',acceptance=acceptance,task_closed=False))
write('registry_commercial_products.csv',products)
# A bounded public Esri catalog query, not the entire Living Atlas.
url='https://www.arcgis.com/sharing/rest/search?'+urllib.parse.urlencode(dict(f='json',q='owner:esri AND type:"Feature Service"',num=20,start=1,sortField='modified',sortOrder='desc'))
rec=dict(source_id='B50S028',url=url,final_url='',fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',response_sha256='',response_bytes='',visible_keyword_present=False,short_excerpt='',source_file='',sha256='',error='',evidence_scope='NEW_FETCH')
catalog=[];summary={}
try:
    with urllib.request.urlopen(url,timeout=30) as response:b=response.read(5000001);rec.update(http_status=response.status,final_url=response.url)
    assert len(b)<=5000000
    obj=json.loads(b);assert 'error' not in obj and len(obj['results'])<=20
    p=O/'raw'/'esri_catalog.json';p.write_bytes(b);rec.update(source_file=p.relative_to(R).as_posix(),sha256=sha(b),response_sha256=sha(b),response_bytes=len(b))
    summary={k:obj.get(k) for k in ['total','start','num','nextStart']}
    for item in obj['results']:
        assert item['owner'].lower()=='esri' and item['type']=='Feature Service'
        catalog.append(dict(item_id=item['id'],owner=item['owner'],title=item['title'],item_type=item['type'],modified_epoch_ms=item.get('modified'),access=item.get('access'),service_url=item.get('url'),extent_json=json.dumps(item.get('extent')),full_search_item_json=json.dumps(item,ensure_ascii=False),license_review='SEARCH_METADATA_ONLY_ITEM_LICENSE_AND_SERVICE_SCHEMA_PENDING',feature_records_downloaded=False,source_file=rec['source_file'],source_sha256=rec['sha256']))
except Exception as e:rec.update(error=type(e).__name__,http_status=getattr(e,'code',rec['http_status']))
receipts.append(rec);write('registry_source_receipts.csv',receipts);write('registry_product_workqueue.csv',work)
if catalog:write('registry_esri_catalog_sample.csv',catalog)
prior=read(R/'Reference/tables/72_granule_metadata_b49_20261011/registry_all_498_work_progress.csv');assert len(prior)==498
write('registry_preserved_498_asf_work.csv',prior)
defs=[('product_id','批次產品群穩定鍵，非全球法人主鍵'),('organization_display','展示名稱，不等於核定法人或同一控股集團'),('evidence_state','只反映入口取用與字詞觀察，不認證性能、部署或國別覆蓋'),('candidate_data_fields','後續可核欄位類型，不代表本批已下載'),('business_value_hypothesis','研究假設；須另驗成本、誤差及客戶價值'),('modified_epoch_ms','目錄item修改時點，非影像拍攝或資料更新時間'),('access','item可見性，非可商業再散布授權'),('extent_json','目錄宣告範圍，非逐國測量覆蓋率'),('response_sha256','取用當次回應指紋；网页全文未納入交付，不是官方簽章'),('full_search_item_json','完整該頁item；並非完整service schema或feature records')]
write('registry_business_definitions.csv',[dict(field=k,definition=v) for k,v in defs])
con=sqlite3.connect(T/'commercial_ecosystem_b50.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);ks=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in ks)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in ks)+')',[[r[k] for k in ks] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close()
assert all(sha((R/p).read_bytes())==h for p,h in protected.items())
stats=dict(product_groups=len(products),official_entry_queries=len(receipts),fetch_errors=sum(bool(r['error']) for r in receipts),visible_keyword_observed=sum(bool(r['visible_keyword_present']) for r in receipts),esri_items=len(catalog),esri_query=summary,new_open_tasks=len(work),prior_asf_work_retained=498,sqlite_counts=counts,global_complete=False,private_or_paid_data_downloaded=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
report='''---
title: "B50：商業宇航、GIS、資料平台與氣象生態增補"
date: 2026-10-11
lang: zh-TW
format:
  html:
    toc: true
    embed-resources: true
---

## 分層登記與證據

以公開宇航與國防工業產業研究、地理資料及災害韌性為用途。產品、資料集、法人、部署與性能分別核實。展示名稱與共同創辦人不能證明同一法人、控股或資料授權。網站HTTP成功甚至關鍵字出現只證明當次入口文字；不把它升格為能力VERIFIED。網站需JavaScript或取用受阻時保留具體狀態。每頁只保留15詞以內核查片段、時間與全文回應指紋，網頁全文未納入發布；ArcGIS公開目錄JSON另保留原始位元。

## 指定供應商與產業鏈

|層次|本輪登記|資料與用途邊界|
|---|---|---|
|發射、集成與宇航系統|SpaceX、Rideshare、Starshield、Rocket Lab、Airbus|產品入口與供應鏈角色；發射詢價不等於合同，政府方案不等於公開影像庫|
|衛星通信|Starlink航空、海事、Direct to Cell／Mobile|通信服務不是地球觀測影像供應；各國頻譜、營運商與服務資格逐項核|
|資料整合、AI及部署|Palantir Foundry、AIP、Apollo、Gotham、Warp Speed|[官方架構文件](https://www.palantir.com/docs/foundry/architecture-center/platforms)區分治理、Ontology、AI與部署；客戶租戶資料不因此開放|
|GIS平台與資料目錄|Esri ArcGIS、Living Atlas、Feature Service|[Query文件](https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service-layer/)供查詢設計；圖層權利、分頁與服務上限另核|
|氣象資料、模型及互通|Meteomatics Weather API、Mix／EURO1k／US1k、連接器|[入門文件](https://www.meteomatics.com/en/api/getting-started/)說明歷史、觀測、預報及WMS/WFS，API需登入；此輪未取得付費氣象樣本|
|商業地球觀測|Planet、ICEYE、BlackSky|入口與產品候選；樣本品質、授權、歷史區域與價格另核|
|太空資料服務|Spire|資料產品與角色候選；時空覆蓋及用途需授權實測|
|能源、AI、基建、神經技術延伸|Tesla Megapack、x.ai／Grok、Boring Company、Neuralink|分開法人、品牌、產品與實測；不自動歸為軍工或同一集團；Neuralink不證明遠程心靈相通|

x.ai本次[官方首頁](https://x.ai/)與[API文件](https://docs.x.ai/overview)顯示SpaceXSI／SpaceXAI相關品牌文字。僅登記網站當期文字；法人關係、持股、併購時間仍未完成法律文件核實，不能用舊稱或品牌自行補成控股結論。自稱世界最快、最高解析度或高回報等仍屬供應商主張。

## 實際目錄資料與缺口

ArcGIS此次只查owner:esri、type:Feature Service、按修改時間倒序第一頁最多20項；不是全部Esri資料，也不能宣稱全部Living Atlas。保存item ID、owner、標題、時間、URL、extent及完整該頁item。total、nextStart記錄於回執，未翻頁部分仍未收錄；未取feature內容、單item詳細條款或service schema。目錄修改時間不等於觀測時間。依[Esri訂戶內容說明](https://www.esri.com/arcgis-blog/products/arcgis-living-atlas/mapping/living-atlas-subscriber-content-public-apps)，使用可能涉及帳戶與credits；逐圖層權利不得從公開可见性推論。

'''+json.dumps(stats,ensure_ascii=False)+'''。

[產品群登記](tables/73_commercial_ecosystem_b50_20261011/registry_commercial_products.csv)、[來源收據](tables/73_commercial_ecosystem_b50_20261011/registry_source_receipts.csv)、[新待辦](tables/73_commercial_ecosystem_b50_20261011/registry_product_workqueue.csv)、[欄位業務定義](tables/73_commercial_ecosystem_b50_20261011/registry_business_definitions.csv)、[SQLite](tables/73_commercial_ecosystem_b50_20261011/commercial_ecosystem_b50.sqlite)。ArcGIS樣本表存在時位於同目錄registry_esri_catalog_sample.csv。

## 下一步驗收

先逐item取得ArcGIS詳細元資料與terms，再查服務schema、分頁限制及歷史小樣本；Meteomatics先核模型、參數、單位、保留值與用途條款，再做授權歷史持出比較。SpaceX／Starlink以官方技術與逐國監管文件核服務範圍；Palantir以公開架構與公司披露核產品、合法實體及商業部署，沒有存取私人租戶。任何供應鏈買賣、母子公司、訂戶或收入都需實體及時態證據。

本批保留此前全部498項ASF工作，沒有結清全球企業、券商、上市公司、貨幣、歷史政治實體及神經科技缺口。ISO母表、舊196項、原宇航報告與使用者版本均保留；SDG分析保持凍結，Untitled不恢復。
'''
(R/'Reference/Commercial_Ecosystem_B50_20261011.qmd').write_text(report,encoding='utf-8')
append='\n\n<!-- COMMERCIAL_ECOSYSTEM_B50_20261011_BEGIN -->\n## 2026-10-11 商業宇航、GIS、資料平台與氣象增補 B50\n\n新增[產品與來源報告](Commercial_Ecosystem_B50_20261011.qmd)及[數據表](tables/73_commercial_ecosystem_b50_20261011/registry_commercial_products.csv)，涵蓋SpaceX／Starlink、Palantir、Esri ArcGIS、Meteomatics及其他商業宇航與相關產品群。登記入口、產業鏈角色、業務定義、取用缺口與授權待辦；本批公開ArcGIS目錄只取有界第一頁，不宣稱全球全量。原正文位元保留，產品文字與HTTP成功不等於性能、合同、法人歸屬或全球覆蓋已核實。\n<!-- COMMERCIAL_ECOSYSTEM_B50_20261011_END -->\n'
(R/MAIN).write_bytes(original+append.encode('utf-8'));base_append=sha(append.encode('utf-8'))
(O/'append_receipt.json').write_text(json.dumps(dict(path=MAIN,prefix_bytes=len(original),prefix_sha256=sha(original),append_sha256=base_append),indent=2),encoding='utf-8')
notes={'redteam':'品牌、共同創辦人、官網成功與公開目錄不證明控股、部署或資料再分發權。','critic':'第一頁Esri樣本與27產品群不是全球公司或圖層全量。','killcritic':'產品角色、來源、時態、業務定義與授權待辦可讓後續核查逐項對賬。','blindspot':'通信、影像、分析平台、模型及能源設備是不同資料與產業層次。','blueprint':'實體與產品→來源證據→逐item授權→schema與历史樣本→品質與總成本。','cheatsheet':'目錄可見≠資料已入庫≠可商業轉售；品牌≠法人；修改時間≠觀測時間。','actionplan':'ArcGIS逐item條款與schema優先；Meteomatics模型參數定義；宇航與軟體公開實體及部署文件。'}
for n,v in notes.items():(R/n/'commercial_ecosystem_b50_20261011.md').write_text('# '+n+' | B50\n\n'+v+'\n\n[報告](../Reference/Commercial_Ecosystem_B50_20261011.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
