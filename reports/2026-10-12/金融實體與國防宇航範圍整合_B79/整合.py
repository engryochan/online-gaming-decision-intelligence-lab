from pathlib import Path
import csv,json,hashlib,re,collections
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/101_金融實體與國防宇航範圍整合_B79_20261012';T.mkdir(parents=True,exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rows for k in x)));d.writeheader();d.writerows(rows)
assert not (W/'結果.json').exists()
p=R/'Reference/tables/100_金融附屬下載全量續核_B78_20261012/試算表來源全量行.csv';raw=read(p);observations=[];checks=[]
for x in raw:
 if not x['網址'].endswith('/list.xlsx') or '企業一覧' not in x['工作表']:continue
 v=json.loads(x['欄值JSON'])
 if len(v)>6 and re.fullmatch(r'[0-9]{3}[0-9A-Z]',str(v[4])) and v[5]:
  date=re.search(r'(20[0-9]{2})年([0-9]+)月',x['工作表'])
  observations.append(dict(來源網址=x['網址'],工作表原文=x['工作表'],工作表中譯='資本成本及股價管理披露企業清單（歷史期別保留）',來源行=x['行'],觀察年月=date[1]+'-'+date[2].zfill(2) if date else 'UNKNOWN',證券代碼=str(v[4]),公司名稱原文=v[5],市場原文=v[3],市場中譯={'プライム':'主要市場','スタンダード':'標準市場'}.get(v[3],'待核'),行業原文=v[2],披露狀態原文=v[6],披露狀態中譯={'開示済':'已披露','検討中':'考慮中'}.get(v[6],'待核'),原始欄值JSON=x['欄值JSON'],法律實體識別碼='UNKNOWN（未知）',名冊完整性='披露企業子集，非日本全部上市公司'))
 elif int(x['行'])>9 and len(v)>6 and v[4] is not None:checks.append(dict(工作表=x['工作表'],行=x['行'],原始欄值JSON=x['欄值JSON'],處理='未符合企業代碼規則，保留待核'))
write('日本披露企業全部歷史觀察.csv',observations)
counts=collections.Counter(x['觀察年月'] for x in observations);write('日本披露企業各期對賬.csv',[dict(觀察年月=k,記錄數=n,唯一證券代碼=len({x['證券代碼'] for x in observations if x['觀察年月']==k})) for k,n in sorted(counts.items())])
# All organizations are carried forward as leads; listing/ownership cannot be inferred from display names.
base=R/'Reference/tables/07_global_technology_iso249_20261006';orgpath=base/'registry_global_organizations.csv';org=read(orgpath)
write('既有生態全部組織待核清單.csv',[dict(x,上市狀態='UNKNOWN（未知）',所有制='UNKNOWN（未知）',軍工國防宇航角色='逐項核查，不能從名稱推定',採購供應鏈關聯='UNKNOWN（未知）',法人完整性='UNKNOWN（未知）') for x in org])
countries=read(base/'registry_country_technology_coverage.csv');tasks=[]
for c in countries:
 for scope in ['證券行監管名冊、分支與牌照','交易所全部證券及上市公司法律實體','軍工國防宇航上市與非上市國企民企及科研政府單位']:
  tasks.append(dict(ISO代碼=c['iso_alpha2'],國家地區名稱原文=c['name_en'],施工範圍=scope,覆蓋狀態='UNKNOWN（未知）',驗收條件='官方總量及逐頁對賬、法人識別碼、日期及授權；缺口不得冒充完成'))
write('逐國金融與國防宇航接續範圍.csv',tasks)
write('日本代碼未分類行.csv',checks or [dict(工作表='無未分類代碼行',行='',原始欄值JSON='',處理='零')])
summary={'日本歷史企業觀察':len(observations),'觀察月份':len(counts),'跨期唯一證券代碼':len({x['證券代碼'] for x in observations}),'既有組織全部保留':len(org),'現行國家地區':len(countries),'逐國範圍工作':len(tasks),'全球完整性升級':0}
assert len(countries)==249 and len(tasks)==747
(W/'結果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');(W/'來源雜湊.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest(),str(orgpath.relative_to(R)):hashlib.sha256(orgpath.read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
text='---\ntitle: "金融實體與國防宇航範圍整合：第七十九批"\nlang: zh-Hant\nformat: html\n---\n\n.response／responses 是保存回應的檔案命名，不表示內容必為券商。券商可提供跨市場交易服務，上市公司則須以交易所、證券及法律實體關聯登記；不能以每家券商販售的產品當作獨立上市公司全集。\n\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n\n[日本披露企業歷史觀察](tables/101_金融實體與國防宇航範圍整合_B79_20261012/日本披露企業全部歷史觀察.csv)；[逐國接續範圍](tables/101_金融實體與國防宇航範圍整合_B79_20261012/逐國金融與國防宇航接續範圍.csv)；[全部既有組織](tables/101_金融實體與國防宇航範圍整合_B79_20261012/既有生態全部組織待核清單.csv)。\n\n日本來源是主要及標準市場的資本成本管理披露子集，歷史期別全部保留，不代表全部日本上市公司；同證券代碼跨期不合併掉歷史。國防宇航範圍包括上市、非上市、國企、民企、政府、研究機構、承包商、零組件、軟體、平台及上下游服務。既有組織全部帶入待核，不能將待核線索當作已核軍工企業。247以外歷史政治實體沿用既有歷史登記，不以現行249限制歷史範圍。\n\n下一步逐國核監管券商總量、交易所名冊及法律實體，國防宇航另核產品、供應鏈角色、採購關係、所有制與上市狀態。747項是新增範圍工作不是已補齊實體，也不取代B77金融4849項取得進度。原始來源、舊報告及使用者修改均不覆寫。\n'
text=text.replace('247以外','現行名單以外')
(R/'Reference/金融實體與國防宇航範圍整合_B79_20261012.qmd').write_text(text,encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
