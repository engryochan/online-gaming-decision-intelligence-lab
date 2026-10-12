from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone
from collections import Counter,defaultdict
import csv,io,json,hashlib,xml.etree.ElementTree as ET,subprocess
工作=Path(__file__).resolve().parent;根=工作.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
原=工作/'原始來源';原.mkdir(exist_ok=True)
表=根/'Reference/tables/93_全球貨幣與市場代碼全量續核_B71_20261012';表.mkdir(parents=True,exist_ok=True)
assert not (工作/'基線.json').exists(),'不得刷新基線'
paths=subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0')
(工作/'基線.json').write_text(json.dumps({'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'既有正文':{p:H((根/p).read_bytes()) for p in paths if p.endswith(('.md','.qmd')) and (根/p).is_file()}},ensure_ascii=False,indent=2),encoding='utf-8')
收=[]
def 取(名,url):
    with urlopen(Request(url,headers={'User-Agent':'Global-public-registry-audit/1.0'}),timeout=60) as r:
        b=r.read(15*1024*1024+1);assert len(b)<=15*1024*1024
        p=原/名;p.write_bytes(b)
        收.append({'中文來源':名,'網址':url,'觀測UTC':datetime.now(timezone.utc).isoformat(),'狀態碼':r.status,'回應標頭':dict(r.headers),'原始檔':p.relative_to(根).as_posix(),'來源雜湊':H(b),'實得位元組':len(b)})
    return b
def 讀(p):
    with (根/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def 寫(n,rows):
    assert rows
    with (表/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
母=讀('Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv');assert len({r['iso_alpha2'] for r in 母})==len(母)
舊幣=讀('Reference/tables/21_currency_broker_b03_20261007/registry_iso4217_all_entries.csv')
舊市=讀('Reference/tables/24_financial_universe_b06_20261007/registry_iso10383_mic.csv')
別=defaultdict(set)
for r in 舊幣:
    if r['iso_alpha2']:別[r['source_entity_name']].add(r['iso_alpha2'])
for r in 母:
    別[r['name_en'].upper()].add(r['iso_alpha2'])
    if r['official_name_en']:別[r['official_name_en'].upper()].add(r['iso_alpha2'])
領=json.loads(取('中文區域名稱參考.json','https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-localenames-full/main/zh-Hant/territories.json'))['main']['zh-Hant']['localeDisplayNames']['territories']
幣譯=json.loads(取('中文貨幣名稱參考.json','https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-numbers-full/main/zh-Hant/currencies.json'))['main']['zh-Hant']['numbers']['currencies']
幣=[];版={}
for state,tag,name in [('CURRENT','CcyNtry','現行貨幣與基金.xml'),('HISTORICAL','HstrcCcyNtry','歷史貨幣與基金.xml')]:
    url='https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/'+('list-one.xml' if state=='CURRENT' else 'list-three.xml')
    x=ET.fromstring(取(name,url));版[state]=dict(x.attrib)
    entries=x.findall('.//'+tag);assert entries
    for i,e in enumerate(entries,1):
        entity=e.findtext('CtryNm','');code=e.findtext('Ccy','');a=別.get(entity,set());iso=next(iter(a)) if len(a)==1 else ''
        幣.append({'記錄識別碼':state+':'+str(i),'狀態中譯':'現行' if state=='CURRENT' else '歷史','來源實體名稱原值':entity,'國家地區ISO代碼':iso,'國家地區中譯參考':領.get(iso,'待核實'),'關聯證據':'沿用既有名稱對照，未提升為官方代碼關聯' if iso else '待核實；保留來源實體','貨幣名稱原值':e.findtext('CcyNm',''),'貨幣中譯參考':幣譯.get(code,{}).get('displayName','待核實'),'字母代碼':code,'數字代碼':e.findtext('CcyNbr',''),'最小單位原值':e.findtext('CcyMnrUnts',''),'撤回日期原值':e.findtext('WthdrwlDt',''),'基金屬性原值':json.dumps(e.find('CcyNm').attrib if e.find('CcyNm') is not None else {},ensure_ascii=False),'來源XML':ET.tostring(e,encoding='unicode')})
    assert len([r for r in 幣 if r['狀態中譯']==('現行' if state=='CURRENT' else '歷史')])==len(entries)
取('市場代碼官方發布頁.html','https://www.iso20022.org/market-identifier-codes')
mic=取('完整市場識別碼.csv','https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv')
reader=csv.DictReader(io.StringIO(mic.decode('utf-8-sig')));市=[]
for i,r in enumerate(reader,1):
    code=r['MIC'];country=r['ISO COUNTRY CODE (ISO 3166)']
    市.append({'来源序號':i,'市場識別碼':code,'營運市場識別碼':r['OPERATING MIC'],'營運或分段原值':r['OPRT/SGMT'],'市場名稱原值':r['MARKET NAME-INSTITUTION DESCRIPTION'],'市場名稱中譯狀態':'待逐項校訂；原名稱保留','法定實體名稱原值':r['LEGAL ENTITY NAME'],'法定實體中譯狀態':'待逐項校訂；不得猜譯','國家地區ISO代碼':country,'國家地區中譯參考':領.get(country,'待核實'),'狀態原值':r['STATUS'],'分類原值':r['MARKET CATEGORY CODE'],'網站原值':r['WEBSITE'],'來源所有欄位JSON':json.dumps(r,ensure_ascii=False,sort_keys=True)})
assert 市 and len({r['市場識別碼'] for r in 市})==len(市)
寫('全量現行與歷史貨幣.csv',幣);寫('全量市場識別碼.csv',市)
覆=[]
for m in 母:
    c=m['iso_alpha2'];cc=[r for r in 幣 if r['國家地區ISO代碼']==c];mm=[r for r in 市 if r['國家地區ISO代碼']==c]
    覆.append({'國家地區ISO代碼':c,'國家地區中譯參考':領.get(c,'待核實'),'名稱原值':m['name_en'],'現行貨幣來源行':sum(r['狀態中譯']=='現行' for r in cc),'歷史貨幣來源行':sum(r['狀態中譯']=='歷史' for r in cc),'市場代碼來源行':len(mm),'上市公司全量狀態':'UNKNOWN（未完成）','券商全量狀態':'UNKNOWN（未完成）','所有貨幣全量狀態':'UNKNOWN（ISO登記表已接收；地方及更早歷史貨幣未竣工）','證據邊界':'無來源行不等於沒有貨幣或市場；市場代碼不等於公司或券商'})
寫('逐國家地區覆蓋與缺口.csv',覆)
舊碼={r['MIC']:r for r in 舊市};新碼={r['市場識別碼']:r for r in 市}
差=[{'市場識別碼':c,'變更類型':'新增代碼' if c not in 舊碼 else '本次未見舊代碼','舊狀態':舊碼.get(c,{}).get('status',''),'新狀態':新碼.get(c,{}).get('狀態原值','')} for c in sorted(set(舊碼)^set(新碼))]
for c in sorted(set(舊碼)&set(新碼)):
    if 舊碼[c]['status']!=新碼[c]['狀態原值']:差.append({'市場識別碼':c,'變更類型':'狀態改變','舊狀態':舊碼[c]['status'],'新狀態':新碼[c]['狀態原值']})
if 差:寫('市場代碼跨批次差異.csv',差)
結={'核查UTC':datetime.now(timezone.utc).isoformat(),'國家地區母表行數':len(母),'現行貨幣來源行':sum(r['狀態中譯']=='現行' for r in 幣),'歷史貨幣來源行':sum(r['狀態中譯']=='歷史' for r in 幣),'貨幣來源實體未關聯行':sum(not r['國家地區ISO代碼'] for r in 幣),'現行唯一非空字母代碼':len({r['字母代碼'] for r in 幣 if r['狀態中譯']=='現行' and r['字母代碼']}),'貨幣源版本':版,'市场代碼來源行':len(市),'市場國家地區代碼數':len({r['國家地區ISO代碼'] for r in 市}),'市場狀態分布':dict(Counter(r['狀態原值'] for r in 市)),'市場跨批次差異項':len(差),'官方及中譯參考回應數':len(收),'全球上市公司已齊':False,'全球券商已齊':False,'所有歷史貨幣已齊':False}
(工作/'來源收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8')
(工作/'核查結果.json').write_text(json.dumps(結,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(結,ensure_ascii=False),flush=True)
