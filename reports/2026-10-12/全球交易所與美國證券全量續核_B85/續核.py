from pathlib import Path
import csv,json,hashlib,subprocess,sys,io,collections,importlib.util
from concurrent.futures import ThreadPoolExecutor
from lxml import html
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/107_全球交易所與美國證券全量續核_B85_20261012';T.mkdir(parents=True,exist_ok=True)
assert not (W/'結果.json').exists()
sources={'納斯達克上市':'https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt','其他交易所上市':'https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt','世界交易所聯合會':'https://www.world-exchanges.org/membership-events','美國證監會':'https://www.sec.gov/about/divisions-offices/division-trading-markets/national-securities-exchanges'}
def fetch(item):
 n,u=item;a={'來源':n,'網址':u,'取得日期':'2026-10-12'}
 try:
  code="import urllib.request,sys; r=urllib.request.urlopen(urllib.request.Request(sys.argv[1],headers={'User-Agent':'GlobalMarketResearch/1.0'}),timeout=10);sys.stdout.buffer.write(r.read())"
  b=subprocess.run([sys.executable,'-c',code,u],capture_output=True,check=True,timeout=25).stdout
  (W/(n+'.response')).write_bytes(b);a.update(狀態='已取得',位元組=len(b),SHA256=hashlib.sha256(b).hexdigest())
 except Exception as e:a.update(狀態='取得失敗，保留缺口',錯誤類型=type(e).__name__)
 return a
receipts=list(ThreadPoolExecutor(4).map(fetch,sources.items()));rows=[];totals=[];leads=[]
for a in receipts:
 n=a['來源'];p=W/(n+'.response')
 if not p.exists():continue
 if n in ['納斯達克上市','其他交易所上市']:
  lines=p.read_text(encoding='utf-8-sig').splitlines();footer=[s for s in lines if s.startswith('File Creation Time:')];data=list(csv.DictReader(io.StringIO('\n'.join(s for s in lines if not s.startswith('File Creation Time:'))),delimiter='|'))
  assert data and 'Security Name' in data[0]
  for i,x in enumerate(data,1):
   rows.append(dict(來源=n,來源網址=a['網址'],來源行=i,證券代碼=x.get('Symbol',x.get('ACT Symbol','')),證券名稱原值=x['Security Name'],證券名稱中譯='待逐項中譯；原值完整保留',交易所來源碼=x.get('Exchange','NASDAQ'),基金旗標=x.get('ETF',''),測試旗標=x.get('Test Issue',''),原始全部欄位JSON=json.dumps(x,ensure_ascii=False),公司法人識別='UNKNOWN（未知）',来源檔尾=json.dumps(footer,ensure_ascii=False)))
  a['解析資料行']=len(data)
 else:
  tree=html.fromstring(p.read_bytes())
  for i,e in enumerate(tree.xpath('//main//a[@href] | //article//a[@href]'),1):
   name=' '.join(e.text_content().split())
   if name:leads.append(dict(來源=n,來源網址=a['網址'],頁內序號=i,名稱原值=name,名稱中譯='待逐項中譯',連結原值=e.get('href'),類型核定='待判別交易所、清算機構、集團或導覽；不得計作股市'))
for (s,m),group in __import__('itertools').groupby(sorted(rows,key=lambda x:(x['來源'],x['交易所來源碼'])),key=lambda x:(x['來源'],x['交易所來源碼'])):
 g=list(group);totals.append(dict(來源=s,交易所來源碼=m,證券記錄數=len(g),基金旗標Y=sum(x['基金旗標']=='Y' for x in g),測試旗標Y=sum(x['測試旗標']=='Y' for x in g),上市公司數='UNKNOWN（未知）：須法人識別及多股類去重'))
def write(name,data):
 with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in data for k in x)) or ['尚無取得資料']);d.writeheader();d.writerows(data)
write('全行業逐證券名冊.csv',rows);write('逐市場證券與公司數量口徑.csv',totals);write('官方頁面全部連結待分類.csv',leads);write('官方來源取得收據.csv',receipts)
p=R/'Reference/tables/106_全行業逐市場名冊續核_B84_20261012/全球全部市場數量接續表.csv';b=p.read_bytes();markets=list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'))));assert len(markets)==2883
write('全球全部市場數量接續表.csv',markets)
summary={'全球市場候選保留':len(markets),'新增全行業證券記錄':len(rows),'逐市場證券分組':len(totals),'官方頁內連結待分類':len(leads),'全球完整上市公司數':'UNKNOWN（未知）','來源取得':receipts}
(W/'結果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');(W/'基線.json').write_text(json.dumps({'原市場路徑':p.relative_to(R).as_posix(),'SHA256':hashlib.sha256(b).hexdigest(),'Git提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()},ensure_ascii=False,indent=2),encoding='utf-8')
text='---\ntitle: "全球交易所與美國證券全量續核：第八十五批"\nlang: zh-Hant\nformat: html\n---\n\n'
text+=f'沿用全部249項國家／地區母表、非ISO直接匹配統計實體及2883項市場候選，不刪除任何原有缺口。本輪新增{len(rows)}條全行業證券記錄；不按國防、宇航或行業篩選。\n\n'
text+='[逐項證券名冊](tables/107_全球交易所與美國證券全量續核_B85_20261012/全行業逐證券名冊.csv)、[逐市場數量](tables/107_全球交易所與美國證券全量續核_B85_20261012/逐市場證券與公司數量口徑.csv)、[全球全部市場接續表](tables/107_全球交易所與美國證券全量續核_B85_20261012/全球全部市場數量接續表.csv)、[官方頁面連結](tables/107_全球交易所與美國證券全量續核_B85_20261012/官方頁面全部連結待分類.csv)。\n\n'
text+='證券數不等於公司數；基金、測試項、多種股份及外國發行人均保留原旗標，法人總數未核定。檔尾生成時間另存，不计作證券。世界交易所聯合會會員包含清算機構與集團，頁面連結是待分類來源線索，並非全球股市完整清單。原始英文名稱雙顯中譯狀態，未翻譯項不假稱已校訂。\n\n道瓊斯工業平均指數是指數。美國證監會現行頁面列NYSE Texas（紐約證券交易所德州市場，原NYSE Chicago／芝加哥證券交易所）與Nasdaq Texas（納斯達克德州市場，原Nasdaq BX／波士頓市場）；期貨與選擇權場所有獨立用途，不能用上市公司數概括。\n\n'
for n,u in sources.items():text+=f'- [{n}官方來源]({u})。\n'
text+='\n[道瓊斯指數官方說明](https://www.spglobal.com/spdji/en/indices/equity/dow-jones-industrial-average/)。逐國尚未發現的額外市場、非ISO實體、官方同日公司總數、法人去重、逐用途授權及全部名冊仍待逐項核實；本輪不宣稱全球無遺漏。\n'
q=R/'Reference/全球交易所與美國證券全量續核_B85_20261012.qmd';q.write_text(text,encoding='utf-8')
assert hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('核查',R/'reports/2026-10-11/未啟動服務替代來源核查_B65/驗證與提交.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.工作=W;m.範圍=[W.relative_to(R).as_posix(),T.relative_to(R).as_posix(),q.relative_to(R).as_posix()];m.密碼掃描()
print(json.dumps({k:v for k,v in summary.items() if k!='來源取得'},ensure_ascii=False))
