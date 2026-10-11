from pathlib import Path
import csv,json,hashlib,subprocess,urllib.request,urllib.parse,datetime,sqlite3,re,struct,zlib
from html.parser import HTMLParser
from pypdf import PdfReader
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/75_access_resolution_b52_20261011'
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
receipts=[]
def fetch(sid,url,limit,range_header=None):
    rec=dict(source_id=sid,url=url,final_url='',fetched_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),http_status='',content_range='',declared_content_length='',source_file='',sha256='',saved_bytes='',partial_response=bool(range_header),error='',evidence_scope='NEW_FETCH')
    b=b''
    try:
        headers={'User-Agent':'PublicResearchRegistry/1.0'}
        if range_header:headers['Range']=range_header
        with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as response:
            b=response.read(limit+1);rec.update(http_status=response.status,final_url=response.url,content_range=response.headers.get('Content-Range',''),declared_content_length=response.headers.get('Content-Length',''))
        if range_header:b=b[:limit]
        else:assert len(b)<=limit
        p=O/'raw'/(sid+('.part' if range_header else '.pdf' if b.startswith(b'%PDF') else '.response'));p.write_bytes(b);rec.update(source_file=p.relative_to(R).as_posix(),sha256=sha(b),saved_bytes=len(b))
    except Exception as e:rec.update(error=type(e).__name__,http_status=getattr(e,'code',rec['http_status']));b=b''
    receipts.append(rec);return rec,b
# Browser-observed official page: retained as a human-readable observation, not an HTTP response.
observation=dict(url='https://www.spacex.com/starshield',method='CODEx_IN_APP_BROWSER_ACCESSIBILITY_OBSERVATION',observed_date='2026-10-11',title='SpaceX - Starshield',headings=['EARTH OBSERVATION','COMMUNICATIONS','HOSTED PAYLOADS'],scope='Official page rendered successfully after initial header-only state; product descriptions observed, performance and deployment not independently verified')
p=O/'raw/starshield_browser_observation.json';p.write_text(json.dumps(observation,indent=2),encoding='utf-8')
receipts.append(dict(source_id='B52STARSHIELD',url=observation['url'],final_url=observation['url'],fetched_utc='2026-10-11_BROWSER_OBSERVATION',http_status='NOT_CAPTURED_BROWSER',content_range='',declared_content_length='',source_file=p.relative_to(R).as_posix(),sha256=sha(p.read_bytes()),saved_bytes=p.stat().st_size,partial_response=False,error='',evidence_scope='NEW_FETCH'))
pdfrec,b=fetch('B52ESRIFAQ','https://goto.arcgis.com/termsofuse/viewsummary',2000000)
pdf_pages=0;pdf_date=''
if b:
    pdf=PdfReader(R/pdfrec['source_file']);pdf_pages=len(pdf.pages);assert pdf_pages==1
    text=pdf.pages[0].extract_text();assert all(s in text for s in ['April 21, 2025','commercial use','self-host','attribution']);pdf_date='2025-04-21'
    (O/'pdf_review_receipt.json').write_text(json.dumps(dict(source_file=pdfrec['source_file'],pages=pdf_pages,source_date=pdf_date,full_page_text_inspected=True)),encoding='utf-8')
masterrec,_=fetch('B52ESRIMASTER','https://www.esri.com/en-us/legal/terms/master-agreement',4000000)
indexrec,b=fetch('B52NOAA2019','https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2019/',4000000)
class Links(HTMLParser):
    def __init__(self):super().__init__();self.hrefs=[]
    def handle_starttag(self,t,a):
        if t=='a':self.hrefs.extend(v for k,v in a if k=='href')
catalog=[];columns=[]
if b:
    parser=Links();parser.feed(b.decode('utf-8','replace'));seen=set()
    for href in parser.hrefs:
        url=urllib.parse.urljoin(indexrec['url'],href);name=urllib.parse.urlparse(url).path.rsplit('/',1)[-1]
        if re.fullmatch(r'AIS_2019_\d{2}_\d{2}\.zip',name):
            assert url.startswith(indexrec['url']) and name not in seen;seen.add(name)
            day=datetime.date.fromisoformat(name[4:-4].replace('_','-'))
            catalog.append(dict(filename=name,date=day.isoformat(),url=url,format='ZIP_WITH_CSV_AS_DECLARED_BY_INDEX',source_file=indexrec['source_file'],source_sha256=indexrec['sha256'],full_object_downloaded=False))
    assert len(catalog)==365 and len({r['date'] for r in catalog})==365
    write('registry_noaa_2019_daily_objects.csv',catalog)
    target=next(r for r in catalog if r['date']=='2019-01-01')
    rec,prefix=fetch('B52NOAAZIPHEADER',target['url'],65536,'bytes=0-65535')
    if prefix:
        assert rec['http_status']==206 and rec['content_range'].startswith('bytes 0-65535/'),'Unexpected Range response; do not parse as complete object'
        assert prefix[:4]==b'PK\x03\x04';fields=struct.unpack('<IHHHHHIIIHH',prefix[:30]);method=fields[3];namelen=fields[-2];extra=fields[-1]
        member=prefix[30:30+namelen].decode('utf-8');assert member.lower().endswith('.csv') and method==8
        dec=zlib.decompressobj(-15);head=dec.decompress(prefix[30+namelen+extra:],8192);header=head.split(b'\n',1)[0].decode('utf-8-sig').strip('\r')
        names=next(csv.reader([header]));assert 'MMSI' in names and 'LAT' in names and 'LON' in names
        columns=[dict(ordinal=i,column_name=n,member_name=member,source_file=rec['source_file'],source_sha256=rec['sha256'],evidence='HEADER_FROM_PARTIAL_ZIP_NOT_FULL_FILE_OR_ROW_VALIDATION',business_definition='SOURCE_COLUMN_NAME_ONLY_SEMANTIC_DICTIONARY_REVIEW_PENDING') for i,n in enumerate(names,1)]
        write('registry_noaa_2019_csv_header.csv',columns)
write('registry_source_receipts.csv',receipts)
terms=[('SUBSCRIPTION','Esri自有item摘要以ArcGIS訂閱及Esri軟體條件描述使用範圍'),('ATTRIBUTION','保留Esri及資料提供者署名'),('OFFLINE_BASEMAP','離線底圖限指定Esri Content Packages與軟體範圍'),('NO_SELF_HOST','摘要列出下載、重分發或自架Esri hosted content限制'),('COMMERCIAL_LIVING_ATLAS','商業Living Atlas用途需與Esri討論適用許可；不能當成一律自由商用'),('AGREEMENT_PRIORITY','摘要不是完整Master Agreement、E300、訂單或逐item特約條款的替代')]
write('registry_esri_obligations.csv',[dict(code=k,meaning=v,scope='ESRI_OWNED_CONTENT_FAQ_NOT_ALL_ARCGIS_HOSTED_THIRD_PARTY_DATA',source_file=pdfrec['source_file'],source_sha256=pdfrec['sha256'],source_date=pdf_date,review='MANUAL_DOCUMENT_SUMMARY_NOT_BLANKET_LEGAL_CLEARANCE') for k,v in terms])
statuses=[dict(gap='STARSHIELD_VISIBLE_PRODUCT_DESCRIPTION',state='PUBLIC_PAGE_RENDERED_OBSERVED',remaining='性能、部署、合同及公共影像API仍未核實'),dict(gap='ESRI_20_TOKEN_REQUIRED_SERVICES',state='ACCESS_LIMIT_RETAINED',remaining='20項499維持；沒有帳戶授權，不取得原服務內容'),dict(gap='ESRI_OWNED_TERMS',state='FAQ_REVIEWED' if pdf_pages else 'FETCH_REVIEW_GAP',remaining='逐item及完整協議的特定用途裁定未完成'),dict(gap='HISTORICAL_AIS_ALTERNATIVE',state='PUBLIC_ORIGINAL_CATALOG_AND_PARTIAL_HEADER' if columns else 'CATALOG_ONLY',remaining='NOAA原始點位CSV與Esri加工Feature Service非同一產品，不等價替換；未下載全量')]
write('registry_gap_resolution.csv',statuses)
for name in ['registry_esri_catalog.csv','registry_esri_item_terms.csv','registry_esri_service_schema.csv','preserved_registry_commercial_products.csv','preserved_registry_product_workqueue.csv','preserved_registry_preserved_498_asf_work.csv']:
    write('preserved_'+name,read(R/'Reference/tables/74_platform_details_b51_20261011'/name))
con=sqlite3.connect(T/'access_resolution_b52.sqlite');counts={}
for p in T.glob('*.csv'):
    rs=read(p);ks=list(rs[0]);con.execute('CREATE TABLE "'+p.stem+'" ('+','.join('"'+k+'" TEXT' for k in ks)+')');con.executemany('INSERT INTO "'+p.stem+'" VALUES ('+','.join('?' for k in ks)+')',[[r[k] for k in ks] for r in rs]);counts[p.stem]=len(rs)
con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
for k,v in counts.items():assert con.execute('SELECT COUNT(*) FROM "'+k+'"').fetchone()[0]==v
con.close();assert all(sha((R/p).read_bytes())==h for p,h in protected.items())
stats=dict(starshield_visible_page_observed=True,esri_faq_pages=pdf_pages,esri_faq_source_date=pdf_date,noaa_2019_objects=len(catalog),partial_csv_columns=len(columns),source_receipts=len(receipts),fetch_errors=sum(bool(r['error']) for r in receipts),token_restrictions_retained=20,full_ais_files_downloaded=0,sqlite_counts=counts,global_complete=False)
(O/'validation_receipt.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
report='''---
title: "B52：星盾頁面取用、Esri條款與歷史公開替代來源"
date: 2026-10-11
lang: zh-TW
format:
  html:
    toc: true
    embed-resources: true
---

## 星盾讀取缺口補核

透過瀏覽器載入[SpaceX原官方Starshield頁](https://www.spacex.com/starshield)，由初始僅頁首狀態轉為完整可見產品段落，核對地球觀測、通信與搭載酬載三類說明。保留瀏覽器觀察回執與來源網址，沒有把它冒充原始HTTP回應或官方簽章。B51替代域名522原證據保留；本次關閉的是公開頁面文字取用缺口，不是性能、部署、機密資料或公共影像API核實。

## Esri使用摘要與仍需授權的服務

取得[Esri官方一頁FAQ](https://goto.arcgis.com/termsofuse/viewsummary)，文件日期2025-04-21，完整閱讀後分列訂閱、署名、離線底圖、下載／重分發／自架與商業Living Atlas用途條件。摘要對Esri自有內容有使用限制，不能由public item或不消耗credits推論自由商業轉售。其適用範圍不擴成所有第三方ArcGIS hosted資料；仍要核對[完整Master Agreement及產品特定條款](https://www.esri.com/en-us/legal/terms/master-agreement)、訂單與逐item內容。沒有建立帳戶或接受條款。

B51的20項Token Required維持限制，原始20項499回應及全部68項item資料原樣保留，沒有將公開替代來源寫成原服務已取得。

## 回到歷史AIS原始公開來源

Esri有界清單包含US Vessel Traffic 2019產品。另核對[NOAA原始2019 AIS目錄](https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2019/)，登記365個逐日ZIP連結，逐日日期及唯一檔名對賬。頁面宣告全量約99.1G；本輪沒有下載全量。原始AIS點位CSV與Esri加工Feature Service在處理、幾何、欄位與授權層次不同，只登記為替代研究來源，不宣稱內容等價。

對2019-01-01公開ZIP僅作HTTP Range前65536 bytes取用，驗證206及Content-Range，解壓首個CSV的有界前綴取得表頭。保存原始部分位元與來源指紋，沒有完整ZIP中央目錄／CRC驗證、沒有全檔／記錄數核實，也沒有分析船舶軌跡。欄名不等於業務語意核實；下一步需官方字典及合法指定用途的歷史資料品質核對。

## 統計與交付

'''+json.dumps(stats,ensure_ascii=False)+'''。

[缺口狀態](tables/75_access_resolution_b52_20261011/registry_gap_resolution.csv)、[Esri義務](tables/75_access_resolution_b52_20261011/registry_esri_obligations.csv)、[365逐日目錄](tables/75_access_resolution_b52_20261011/registry_noaa_2019_daily_objects.csv)、[部分ZIP表頭](tables/75_access_resolution_b52_20261011/registry_noaa_2019_csv_header.csv)、[來源收據](tables/75_access_resolution_b52_20261011/registry_source_receipts.csv)、[SQLite](tables/75_access_resolution_b52_20261011/access_resolution_b52.sqlite)。

前輪68個ArcGIS item、20個服務錯誤、27個產品群、108項商業工作及498項ASF工作均保留。Grok／xAI與Meteomatics版本、參數及保留值成果保留；影像品質、具體用途授權、全球覆蓋及部署仍未全面核實。全球金融、歷史與神經科技待辦未結清；SDG分析保持凍結，Untitled不恢復。
'''
(R/'Reference/Access_Resolution_B52_20261011.qmd').write_text(report,encoding='utf-8')
append='\n\n<!-- ACCESS_RESOLUTION_B52_20261011_BEGIN -->\n## 2026-10-11 公開取用缺口補核 B52\n\n新增[星盾頁面、Esri條款與歷史公開替代来源報告](Access_Resolution_B52_20261011.qmd)：星盾原官方頁面成功渲染；Esri官方使用摘要分列義務；NOAA 2019 AIS逐日目錄及部分ZIP表頭保留。ArcGIS的20項Token限制仍在，替代資料不冒充原服務。原文保留，未取得付費、私人或機密資料。\n<!-- ACCESS_RESOLUTION_B52_20261011_END -->\n'
(R/MAIN).write_bytes(original+append.encode('utf-8'))
(O/'append_receipt.json').write_text(json.dumps(dict(path=MAIN,prefix_bytes=len(original),prefix_sha256=sha(original),append_sha256=sha(append.encode('utf-8'))),indent=2),encoding='utf-8')
notes={'redteam':'公開替代CSV不能冒充訂閱Feature Service；摘要不能外推至所有第三方圖層。','critic':'365連結及部分CSV表頭不是全量資料驗證或全球海事覆蓋。','killcritic':'成功渲染星盾並回溯原始公開資料，將讀取缺口轉成可核證據。','blindspot':'HTTP499是API身份限制，522是取用失敗；兩者與資料不存在不同。','blueprint':'可見頁面→條款義務→原始來源目錄→有界表頭→合法歷史品質驗證。','cheatsheet':'星盾產品描述已讀；20項Token限制仍在；NOAA部分ZIP未做全檔CRC驗證。','actionplan':'取得官方AIS字典，核原始與加工產品差別及歷史品質；訂閱服務待合法帳戶授權。'}
for n,v in notes.items():(R/n/'access_resolution_b52_20261011.md').write_text('# '+n+' | B52\n\n'+v+'\n\n[報告](../Reference/Access_Resolution_B52_20261011.qmd)。\n',encoding='utf-8')
print(json.dumps(stats))
