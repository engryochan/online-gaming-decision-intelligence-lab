from pathlib import Path
import csv,json,hashlib,collections
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/98_證券雙櫃台與日期對賬_B76_20261012';T.mkdir(parents=True,exist_ok=True)
B=R/'Reference/tables/97_試算表實際行範圍全量修復_B75_20261012'
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rows for k in x)));d.writeheader();d.writerows(rows)
assert not (W/'結果.json').exists()
paths=[B/'實際全量試算表來源行.csv',B/'港交所逐證券分類觀察.csv'];base={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
raw=read(paths[0]);securities=read(paths[1]);by={x['證券代碼'].zfill(5):x for x in securities};out=[]
for x in raw:
 if 'Dual_Counter' not in x['網址']:continue
 v=json.loads(x['欄值JSON'])
 if len(v)<7 or not isinstance(v[0],int):continue
 h=str(v[0]).zfill(5);m=str(v[1]).zfill(5);a=by.get(h);b=by.get(m)
 out.append(dict(來源網址=x['網址'],來源行=x['行'],港幣代碼=h,人民幣代碼=m,公司名稱原文=v[2],中文簡稱=v[3],人民幣櫃台增設日期原文=v[4],指定生效日期原文=v[5],港幣記錄存在=bool(a),人民幣記錄存在=bool(b),港幣ISIN=a['ISIN'] if a else '',人民幣ISIN=b['ISIN'] if b else '',ISIN一致=bool(a and b and a['ISIN'] and a['ISIN']==b['ISIN']),交易貨幣吻合=bool(a and b and a['交易貨幣']=='HKD' and b['交易貨幣']=='RMB'),法律實體ID='UNKNOWN（未知）'))
write('雙櫃台逐項交叉核對.csv',out)
catmap={'Callable Bull/Bear Contracts':'牛熊證','Debt Securities':'債務證券','Derivative Warrants':'衍生權證','Equity':'股權','Equity Warrants (GEM)':'股權認股權證（創業板）','Equity Warrants (Main Board)':'股權認股權證（主板）','Exchange Traded Products':'交易所買賣產品','Real Estate Investment Trusts':'房地產投資信託'}
submap={'None':'未提供','Depositary Receipts':'存託憑證','Equity Securities (GEM)':'股權證券（創業板）','Equity Securities (Main Board)':'股權證券（主板）','Investment Companies':'投資公司','Trading Only Securities':'僅供交易證券','Exchange Traded Funds':'交易所買賣基金','Leveraged and Inverse':'槓桿及反向產品'}
c=collections.Counter((x['類別原文'],x['子類別原文']) for x in securities)
write('證券類別中外雙顯.csv',[dict(類別原文=a,類別中譯=catmap.get(a,'待核中譯'),子類別原文=b,子類別中譯=submap.get(b,'待核中譯'),記錄數=n,中譯性質='編輯中譯，非法律實體核定') for (a,b),n in sorted(c.items())])
isins=collections.defaultdict(list)
for x in securities:
 if x['ISIN'] and x['ISIN']!='None':isins[x['ISIN']].append(x['證券代碼'])
write('重複ISIN代碼組.csv',[dict(ISIN=k,證券代碼JSON=json.dumps(v),記錄數=len(v),解釋='同識別碼不等於同公司，須核櫃台與工具') for k,v in isins.items() if len(v)>1])
dates=[dict(來源網址=x['網址'],來源行=x['行'],日期聲明原文=x['欄值JSON'],性質='來源更新聲明，不推定法律生效時刻') for x in raw if ('ListOfSecurities.xlsx' in x['網址'] and 'Updated as at' in x['欄值JSON']) or ('Dual_Counter' in x['網址'] and x['行']=='3')]
write('來源日期聲明.csv',dates)
assert sum(c.values())==17205 and len(out)==23
for p in paths:assert hashlib.sha256(p.read_bytes()).hexdigest()==base[p.relative_to(R).as_posix()]
summary={'證券記錄':len(securities),'雙櫃台來源配對':len(out),'兩端存在':sum(x['港幣記錄存在'] and x['人民幣記錄存在'] for x in out),'兩端ISIN一致':sum(x['ISIN一致'] for x in out),'兩端貨幣吻合':sum(x['交易貨幣吻合'] for x in out),'重複ISIN組':sum(len(v)>1 for v in isins.values()),'類別子類別組':len(c),'法律實體完整性升級':0}
(W/'結果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');(W/'來源雜湊.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf-8')
text='---\ntitle: "證券雙櫃台與日期對賬：第七十六批"\nlang: zh-Hant\nformat: html\n---\n\n本輪只核已保存來源的跨表一致性，未宣稱重新取得最新全市場資料。港交所證券清單更新聲明為12/10/2026；雙櫃台表更新日期為31-08-2026，宣告下一交易日生效，各配對增設與指定日期保留原值。不同日期的表不能直接認定同日完整性。\n\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n\n[雙櫃台逐項對賬](tables/98_證券雙櫃台與日期對賬_B76_20261012/雙櫃台逐項交叉核對.csv)；[類別中外雙顯](tables/98_證券雙櫃台與日期對賬_B76_20261012/證券類別中外雙顯.csv)。\n\n證券代碼、ISIN與公司法律實體分開登記。ISIN一致只能支持跨櫃台工具關聯，不能直接證明集團或法人唯一身份；中文簡稱沿用雙櫃台來源，不以簡稱替代法律名称。全球公司／券商完整性不升級，原資料及歷史批次不覆寫。下一步核對不一致配對、逐法人識別碼與來源有效日期，並續查B73未嘗試清單。\n'
(R/'Reference/證券雙櫃台與日期對賬_B76_20261012.qmd').write_text(text,encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
