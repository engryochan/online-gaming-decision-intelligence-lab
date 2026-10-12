from pathlib import Path
import csv,json,hashlib,urllib.request,subprocess
from concurrent.futures import ThreadPoolExecutor
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/103_軍工國防宇航官方欄位增補_B81_20261012';T.mkdir(parents=True,exist_ok=True)
def write(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rows for k in x)));d.writeheader();d.writerows(rows)
assert not (W/'結果.json').exists()
sources=[('S1','洛克希德馬丁2025年監管申報','https://www.sec.gov/Archives/edgar/data/936468/000162828026004195/lmt-20251231.htm'),('S2','薩博2025年年報發布','https://www.saab.com/newsroom/press-releases/2026/saab-publishes-its-2025-annual-report'),('S3','以色列航太工業2025年永續報告','https://www.iai.co.il/wp-content/uploads/2026/04/IAI_Sustainability_Report_2025_English_31_3_26.pdf'),('S4','以色列航太工業公司介紹','https://www.iai.co.il/about/'),('S5','韓華航太2025年永續報告','https://www.hanwhaaerospace.com/assets/content/esg/sustainBusiness/download/en/HanwhaAerospace_SustainabilityReport_2025_ENG.pdf'),('S6','韓華航太股權資訊','https://www.hanwhaaerospace.com/eng/ir/stock-info.do'),('S7','安杜里爾收購藍色力量科技公告','https://www.anduril.com/news/anduril-acquires-blue-force-technologies')]
def fetch(x):
 sid,name,u=x;a=dict(來源ID=sid,中文來源=name,網址=u,核查日='2026-10-12',網頁核查範圍='官方頁面或報告欄位人工核讀，非法人登記機關查冊')
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ResearchEvidence/1.0'}),timeout=20) as f:b=f.read(20000001);a.update(HTTP狀態=f.status,位元組=len(b),截斷=len(b)>20000000,SHA256=hashlib.sha256(b).hexdigest())
  p=W/'原始回應'/ (sid+'.response');p.parent.mkdir(exist_ok=True);p.write_bytes(b);a['原始檔']=p.relative_to(R).as_posix()
 except Exception as e:a['本機取得錯誤']=type(e).__name__;a['說明']='官方內容經網頁工具核讀；本機原始下載缺口保留'
 return a
with ThreadPoolExecutor(max_workers=4) as pool:receipts=list(pool.map(fetch,sources))
write('官方來源收據.csv',receipts)
org=[('FRO0026','洛克希德馬丁','Lockheed Martin Corporation','US','S1','航空、飛彈與射控、旋翼與任務系統、太空四個業務部門','NYSE（紐約證券交易所）LMT，2025年申報支持','UNKNOWN（未知）','2025-12-31'),('FRO0036','薩博','Saab AB','SE','S2','航空、武器、指揮控制、感測器、水下系統的設計製造維護','UNKNOWN（未知）','UNKNOWN（未知）','發布2026-03-03'),('FRO0041','以色列航太工業','Israel Aerospace Industries Ltd.','IL','S3|S4','國防、宇航及商業航空','來源稱私人公司；股票非上市／債券上市須另核','以色列國家全資所有，報告期末支持','2025-12-31'),('FRO0050','韓華航太','Hanwha Aerospace','KR','S5|S6','太空、航空、陸上及海洋綜合業務','UNKNOWN（未知）','股東構成有韓華及其他投資者；不直接推定國有／民營控制','股東表2025-12-31'),('FRO0024','安杜里爾工業','Anduril Industries','US','S7','國防科技及自主航空開發收購關係','UNKNOWN（未知）','UNKNOWN（未知）','收購公告2023年，當前整合狀態另核'),('B81:ELTA','艾爾塔系統','ELTA Systems Ltd.','IL','S3','同時為以色列航太工業的部門及子公司','UNKNOWN（未知）','子公司關係已描述，直接股權比例另核','2025-12-31')]
rows=[dict(原登記ID=i,中文名稱=cn,名稱原文=en,國家線索=c,國別性質='來源地域線索，非法律註冊地查冊',來源ID=s,產業鏈角色=role,上市狀態=listed,所有制證據=owner,證據有效期=asof,證據等級='VERIFIED（僅限官方明示欄位）',法人登記號='UNKNOWN（未知）',供應商全量='UNKNOWN（未知）') for i,cn,en,c,s,role,listed,owner,asof in org]
write('組織逐欄官方證據.csv',rows)
relations=[dict(主體='Israel Aerospace Industries Ltd.（以色列航太工業）',客體='ELTA Systems Ltd.（艾爾塔系統）',關係='子公司兼部門',來源ID='S3',有效期='2025-12-31',限制='不推定全部子公司或股權比例'),dict(主體='Anduril Industries（安杜里爾工業）',客體='Blue Force Technologies（藍色力量科技）',關係='官方收購公告',來源ID='S7',有效期='2023年公告',限制='公告事件不等於目前法人狀態或整合完成')]
write('產業鏈組織關係.csv',relations)
for a in receipts:
 if a.get('原始檔'):assert hashlib.sha256((R/a['原始檔']).read_bytes()).hexdigest()==a['SHA256']
summary={'組織欄位增補':len(rows),'既有登記關聯':5,'子公司增補':1,'官方來源':len(receipts),'本機成功取得':sum(a.get('HTTP狀態')==200 for a in receipts),'組織關係':len(relations),'法人登記機關完整核定':0,'全球完整性升級':0}
(W/'結果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
text='---\ntitle: "軍工國防宇航官方欄位增補：第八十一批"\nlang: zh-Hant\nformat: html\n---\n\n本輪增補實際官方欄位證據，舊299組織與既有登記不覆寫；5個既有組織關聯與1個子公司補充。VERIFIED只適用明示欄位，不把整個法人、全球供應商或上市所有制一律標為已核。\n\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n\n[逐欄組織證據](tables/103_軍工國防宇航官方欄位增補_B81_20261012/組織逐欄官方證據.csv)；[來源收據](tables/103_軍工國防宇航官方欄位增補_B81_20261012/官方來源收據.csv)。\n\n'
for sid,name,u in sources:text+=f'- [{name}]({u})。\n'
text+='\n以色列航太工業的報告支持國家全資身份；私人公司法律形式不等於民營，也不等於無上市債券。收購公告只記歷史事件，不直接推定目前控制及整合狀態。韓華股東頁不直接代替上市交易所與控制人查冊。各組織仍需登記號、股權及上市種類分別驗證，國企、民企與非上市皆不排除。\n\n後續核其餘既有組織的法人與產品證據、逐國官方採購及監管名冊，再展開完整子公司與上下游，全球金融進度仍沿用B80。\n'
(R/'Reference/軍工國防宇航官方欄位增補_B81_20261012.qmd').write_text(text,encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
