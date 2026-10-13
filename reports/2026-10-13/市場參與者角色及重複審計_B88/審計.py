from pathlib import Path
import csv,json,hashlib,collections,importlib.util
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/110_市場參與者角色及重複審計_B88_20261013';T.mkdir(parents=True,exist_ok=True)
assert not (W/'結果.json').exists()
p=R/'Reference/tables/109_全對話清單接續_B87_20261013/市場參與者全部原始記錄.csv';b=p.read_bytes();old=list(csv.DictReader(p.open(encoding='utf-8-sig')));groups=collections.defaultdict(list);rows=[]
roles={'A':'代理報價','C':'電子通訊交易網絡','E':'交易所','M':'造市商','N':'其他參與者','O':'訂單輸入機構','P':'納斯達克參與者','Q':'僅查詢機構','S':'專業交易商'}
for x in old:
 raw=json.loads(x['全部原欄位JSON']);y=dict(x);y['角色中譯']=roles.get(raw.get('MP Type',''),'官方定義待核');y['來源會員旗標JSON']=json.dumps({k:v for k,v in raw.items() if 'Member' in k or 'Participant' in k},ensure_ascii=False);y['證據界限']='只核來源角色及旗標，不核法人持牌狀態';rows.append(y);groups[raw['MPID']].append((x,raw))
duplicates=[]
for code,g in groups.items():
 if len(g)<2:continue
 names=sorted(set(r.get('Name','') for x,r in g));types=sorted(set(r.get('MP Type','') for x,r in g));distinct=len(set(json.dumps(r,sort_keys=True) for x,r in g))
 duplicates.append(dict(參與者代碼=code,原記錄數=len(g),不同完整記錄數=distinct,不同名稱數=len(names),名稱原值JSON=json.dumps(names,ensure_ascii=False),角色原值JSON=json.dumps(types),原行號JSON=json.dumps([x['來源行'] for x,r in g]),處置='全部保留；不可按代碼自動選最後一行或合併法人'))
def write(n,data):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in data for k in x)) or ['無資料']);d.writeheader();d.writerows(data)
write('全部角色與會員旗標觀察.csv',rows);write('重複參與者碼逐組審計.csv',duplicates)
counts=collections.Counter(x['類型原值'] for x in old);write('角色數量對賬.csv',[dict(角色原值=k,角色中譯=roles.get(k,'待核'),來源行數=v,券商法人數='UNKNOWN（未知）') for k,v in sorted(counts.items())])
assert len(rows)==len(old)==4219 and sum(counts.values())==4219
assert sum(int(x['原記錄數'])-1 for x in duplicates)==len(rows)-len(groups)
assert all(all(y[k]==x[k] for k in x) for x,y in zip(old,rows))
result={'全部記錄保留':len(rows),'非空唯一參與者碼':len([k for k in groups if k]),'重複碼組':len(duplicates),'重複碼額外觀察行':sum(x['原記錄數']-1 for x in duplicates),'多名稱碼組':sum(x['不同名稱數']>1 for x in duplicates),'角色來源行對賬':dict(counts),'全球券商法人數':'UNKNOWN（未知）'}
(W/'結果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');(W/'保留驗收.json').write_text(json.dumps({'來源路徑':p.relative_to(R).as_posix(),'來源SHA256':hashlib.sha256(b).hexdigest(),'所有原欄位逐行保留':True,'原檔未改動':p.read_bytes()==b},ensure_ascii=False,indent=2),encoding='utf-8')
q=R/'Reference/市場參與者角色及重複審計_B88_20261013.qmd';text='---\ntitle: "市場參與者角色與重複審計：第八十八批"\nlang: zh-Hant\nformat: html\n---\n\n保留工作區冊二的使用者改動。本輪對B87全部記錄作角色中譯、會員旗標展開及重複碼審計，沒有刪除原記錄或將代碼當法人。\n\n```json\n'+json.dumps(result,ensure_ascii=False,indent=2)+'\n```\n\n[全部原欄位與角色](tables/110_市場參與者角色及重複審計_B88_20261013/全部角色與會員旗標觀察.csv)、[重複碼逐組審計](tables/110_市場參與者角色及重複審計_B88_20261013/重複參與者碼逐組審計.csv)、[角色對賬](tables/110_市場參與者角色及重複審計_B88_20261013/角色數量對賬.csv)。\n\n[納斯達克官方字段定義（Nasdaq Symbol Directory Definitions）](https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs)區分九類市場參與者，並指出代碼可涉及分支所在地。來源會員旗標只表示該名冊觀察，不替代監管登記與持牌狀態的實質核定。重複碼含不同名稱時須另核歷史名稱、分支、碼重用及來源更新，不自動推定任何一種原因。全球逐國清單仍沿用B87，整體未竣工。\n';q.write_text(text,encoding='utf-8')
spec=importlib.util.spec_from_file_location('核查',R/'reports/2026-10-11/未啟動服務替代來源核查_B65/驗證與提交.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.工作=W;m.範圍=[W.relative_to(R).as_posix(),T.relative_to(R).as_posix(),q.relative_to(R).as_posix()];m.密碼掃描();print(json.dumps(result,ensure_ascii=False))
