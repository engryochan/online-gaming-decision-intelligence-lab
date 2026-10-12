from pathlib import Path
import csv,json,io,hashlib,subprocess,sys,importlib.util
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/108_證券券商口徑與全球缺口審計_B86_20261012';T.mkdir(parents=True,exist_ok=True)
assert not (W/'結果.json').exists()
B=R/'reports/2026-10-12/全球交易所與美國證券全量續核_B85';summary=json.loads((B/'結果.json').read_text(encoding='utf-8'));audit=[];allrows=[]
for a in summary['來源取得']:
 if a['來源'] not in ['納斯達克上市','其他交易所上市']:continue
 b=(B/(a['來源']+'.response')).read_bytes();assert hashlib.sha256(b).hexdigest()==a['SHA256']
 lines=b.decode('utf-8-sig').splitlines();footer=[x for x in lines if x.startswith('File Creation Time:')];rows=list(csv.DictReader(io.StringIO('\n'.join(x for x in lines if not x.startswith('File Creation Time:'))),delimiter='|'));assert len(rows)==a['解析資料行'];allrows+=rows
 audit.append(dict(來源=a['來源'],原檔SHA256=a['SHA256'],資料記錄數=len(rows),基金旗標Y=sum(x.get('ETF')=='Y' for x in rows),測試旗標Y=sum(x.get('Test Issue')=='Y' for x in rows),非基金且非測試證券=sum(x.get('ETF')=='N' and x.get('Test Issue')=='N' for x in rows),檔尾=json.dumps(footer,ensure_ascii=False),券商數='不適用：本檔對象是證券',公司法人數='UNKNOWN（未知）'))
assert len(allrows)==13294
url='https://www.nasdaqtrader.com/dynamic/SymDir/mpidlist.txt';receipt={'來源':'納斯達克市場參與者名冊','網址':url,'取得日期':'2026-10-12'};participants=[]
try:
 code="import urllib.request,sys; r=urllib.request.urlopen(urllib.request.Request(sys.argv[1],headers={'User-Agent':'MarketRegistryResearch/1.0'}),timeout=10);sys.stdout.buffer.write(r.read())"
 b=subprocess.run([sys.executable,'-c',code,url],capture_output=True,check=True,timeout=25).stdout;(W/'市場參與者.response').write_bytes(b);lines=b.decode('utf-8-sig').splitlines();data=list(csv.DictReader(io.StringIO('\n'.join(x for x in lines if not x.startswith('File Creation Time:'))),delimiter='|'));assert data and 'MPID' in data[0]
 for i,x in enumerate(data,1):participants.append(dict(來源行=i,市場參與者代碼=x['MPID'],名稱原值=x.get('Name',''),名稱中譯='待逐項中譯',全部原始欄位JSON=json.dumps(x,ensure_ascii=False),券商法人核定='UNKNOWN（未知）：分支、類型與監管登記須另核',來源網址=url))
 receipt.update(狀態='取得及解析成功',記錄數=len(data),SHA256=hashlib.sha256(b).hexdigest(),位元組=len(b),檔尾=[x for x in lines if x.startswith('File Creation Time:')])
except Exception as e:receipt.update(狀態='取得失敗，保留缺口',錯誤類型=type(e).__name__)
def write(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rows for k in x)) or ['尚無取得資料']);d.writeheader();d.writerows(rows)
write('13294條證券原檔重核.csv',audit);write('市場參與者逐項待核.csv',participants);write('官方取得收據.csv',[receipt])
paths=['Reference/tables/107_全球交易所與美國證券全量續核_B85_20261012/全球全部市場數量接續表.csv','Reference/tables/102_全球金融未嘗試來源續查_B80_20261012/全4849項接續進度.csv']
gaps=[]
for s in paths:
 p=R/s
 if not p.exists():gaps.append(dict(來源路徑=s,狀態='路径待定位，不宣稱清單完成'));continue
 rows=list(csv.DictReader(p.open(encoding='utf-8-sig')));write(p.name,rows);gaps.append(dict(來源路徑=s,原檔SHA256=hashlib.sha256(p.read_bytes()).hexdigest(),保留記錄=len(rows),狀態='完整保留原表；來源取得不等於法人名冊完整'))
write('接續清單審計.csv',gaps)
result={'原檔重核證券記錄':len(allrows),'基金旗標Y':sum(x['基金旗標Y'] for x in audit),'測試旗標Y':sum(x['測試旗標Y'] for x in audit),'非基金且非測試證券':sum(x['非基金且非測試證券'] for x in audit),'新增市場參與者觀察':len(participants),'全球券商法人總數':'UNKNOWN（未知）','全球上市公司法人總數':'UNKNOWN（未知）'}
(W/'結果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
q=R/'Reference/證券券商口徑與全球缺口審計_B86_20261012.qmd';text='---\ntitle: "證券、券商口徑與全球缺口審計：第八十六批"\nlang: zh-Hant\nformat: html\n---\n\n13,294不是全球券商數，亦不是全球公司數，是B85兩份美國市場證券來源的資料行。已逐檔重算及核對SHA256，原始證據未改動。此前回答未直接列明兩份來源數量及旗標構成，容易造成誤解，本輪補齊可重現證據。\n\n'
text+='```json\n'+json.dumps(result,ensure_ascii=False,indent=2)+'\n```\n\n'
text+='[原檔重核及構成](tables/108_證券券商口徑與全球缺口審計_B86_20261012/13294條證券原檔重核.csv)；[市場參與者逐項待核](tables/108_證券券商口徑與全球缺口審計_B86_20261012/市場參與者逐項待核.csv)；[原接續清單審計](tables/108_證券券商口徑與全球缺口審計_B86_20261012/接續清單審計.csv)。\n\n'
text+='證券是可交易的金融工具；券商是經監管登記的業務法人；上市公司是發行人；交易所是市場營運者。非基金、非測試證券仍可能包括不同股類、優先股或存託憑證，不能直接作公司數。市場參與者碼也可能含分支、交易所或其他參與者，不等於券商法人總數。\n\n'
text+='[納斯達克字段定義（Nasdaq Symbol Directory Definitions）](https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs)區分證券檔與市場參與者檔。實際otherlisted來源出現F、M交易所碼，但本次閱讀官方定義僅列A、N、P、Z、V；F、M另列定義缺口，不自行猜測名稱。\n\n'
text+=f'[市場參與者官方檔]({url})。基金旗標與測試旗標可重疊，兩者不可簡單相減；使用逐行條件核算。全球逐國市場发现、券商監管名冊、逐發行人去重、同日公司總量與授權核實均未竣工，未將未知填零，未刪除其他國家缺口。\n';q.write_text(text,encoding='utf-8')
spec=importlib.util.spec_from_file_location('核查',R/'reports/2026-10-11/未啟動服務替代來源核查_B65/驗證與提交.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.工作=W;m.範圍=[W.relative_to(R).as_posix(),T.relative_to(R).as_posix(),q.relative_to(R).as_posix()];m.密碼掃描();print(json.dumps(result,ensure_ascii=False))
