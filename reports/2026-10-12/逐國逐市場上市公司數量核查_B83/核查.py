from pathlib import Path
import csv,json,hashlib,urllib.request,collections
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/105_逐國逐市場上市公司數量核查_B83_20261012';T.mkdir(parents=True,exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rows for k in x)));d.writeheader();d.writerows(rows)
assert not (W/'結果.json').exists()
receipts=[];data={}
for name,url in [('世界銀行經濟體','https://api.worldbank.org/v2/country?format=json&per_page=1000'),('上市本地公司最近非空值','https://api.worldbank.org/v2/country/all/indicator/CM.MKT.LDOM.NO?format=json&per_page=20000&mrnev=1')]:
 try:
  with urllib.request.urlopen(url,timeout=30) as f:b=f.read();status=f.status
  p=W/(name+'.json');p.write_bytes(b);data[name]=json.loads(b);receipts.append(dict(名稱=name,網址=url,HTTP狀態=status,位元組=len(b),SHA256=hashlib.sha256(b).hexdigest(),原始檔=p.relative_to(R).as_posix()))
 except Exception as e:receipts.append(dict(名稱=name,網址=url,錯誤=type(e).__name__))
write('官方統計取得收據.csv',receipts)
cpath=R/'Reference/tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv';mpath=R/'Reference/tables/93_全球貨幣與市場代碼全量續核_B71_20261012/全量市場識別碼.csv';countries=read(cpath);markets=read(mpath);iso={x['iso_alpha3']:x for x in countries};codes={x['iso_alpha2'] for x in countries}
wb=data.get('上市本地公司最近非空值',[{},[]]);meta=wb[0];records=wb[1] if len(wb)>1 and isinstance(wb[1],list) else []
assert not records or meta['pages']==1 and len(records)==meta['total']
economies={x['id']:x for x in data.get('世界銀行經濟體',[{},[]])[1]};values={};extras=[];aggregates=[]
for x in records:
 code=x['countryiso3code'];row=dict(經濟體代碼=code,名稱原文=x['country']['value'],數值=x['value'] if x['value'] is not None else 'UNKNOWN（未知）',統計年份=x['date'],指標='CM.MKT.LDOM.NO（上市本地公司數）',口徑='年末本地上市公司，含僅在該市場上市的外國公司例外；非逐交易所總公司數')
 if economies.get(code,{}).get('region',{}).get('id')=='NA':aggregates.append(row);continue
 if code in iso:values[code]=row
 else:extras.append(dict(row,ISO母表關聯='未以本資料代碼直接匹配，須逐項核；不推定獨立國家'))
write('非ISO直接匹配統計經濟體.csv',extras or [dict(經濟體代碼='無',名稱原文='',數值='',統計年份='',說明='零筆')]);write('統計聚合體另存.csv',aggregates)
by=collections.defaultdict(list)
for x in markets:by[x['國家地區ISO代碼']].append(x)
rows=[]
for c in countries:
 v=values.get(c['iso_alpha3']);m=by[c['iso_alpha2']]
 rows.append(dict(ISO二字碼=c['iso_alpha2'],ISO三字碼=c['iso_alpha3'],名稱原文=c['name_en'],市場識別碼數=len(m),營運市場識別碼數=sum(x['營運或分段原值']=='OPRT' for x in m),本地上市公司官方統計=v['數值'] if v else 'UNKNOWN（未知）',統計年份=v['統計年份'] if v else '',統計來源='世界銀行WDI（世界發展指標）' if v else '本輪未取得非空值',各股市完整性='UNKNOWN（未知）',逐家公司完整性='UNKNOWN（未知）',說明='MIC數不是股市數；無統計或無MIC不等於無公司或無股市'))
write('全部249國家地區上市公司統計與缺口.csv',rows)
write('全部市場逐項上市公司數待核.csv',[dict(x,市場業務類型='須核股市／債券／衍生品／場外／報告服務，原分類保留',上市本地公司數='UNKNOWN（未知）',上市外國公司數='UNKNOWN（未知）',上市總公司數='UNKNOWN（未知）',公司名冊完整性='UNKNOWN（未知）',日期口徑='來源MIC快照，上市公司數另需交易所有效日期') for x in markets])
write('市場非ISO直接匹配項.csv',[dict(x,說明='市場源代碼未在母表，須別名或額外市場審查') for x in markets if x['國家地區ISO代碼'] not in codes] or [dict(說明='無未匹配項')])
assert len(rows)==249 and len(markets)==2883 and any(x['ISO二字碼']=='TW' for x in rows)
summary={'現行國家地區母表':249,'完整保留市場識別記錄':len(markets),'有非空本地上市公司統計國家地區':sum(x['本地上市公司官方統計']!='UNKNOWN（未知）' for x in rows),'非ISO直接匹配經濟體':len(extras),'逐股市上市公司數已核':0,'臺灣母表TW存在':True,'全球上市公司總数':'UNKNOWN（異期統計不加總；跨市場法人未去重）'}
(W/'結果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');(W/'來源雜湊.json').write_text(json.dumps({p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [cpath,mpath]},ensure_ascii=False,indent=2),encoding='utf-8')
text='---\ntitle: "逐國逐市場上市公司數量核查：第八十三批"\nlang: zh-Hant\nformat: html\n---\n\n標準為ISO 3166-1，臺灣已有TW母表及市場來源項，並非沒有ISO代碼。現行國家／地區全部保留，非直接匹配統計經濟體另表，不混入聚合區域。\n\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n\n[逐國上市公司統計](tables/105_逐國逐市場上市公司數量核查_B83_20261012/全部249國家地區上市公司統計與缺口.csv)；[全部市場逐項對賬](tables/105_逐國逐市場上市公司數量核查_B83_20261012/全部市場逐項上市公司數待核.csv)。\n\n[世界銀行指標定義](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/CM.MKT.LDOM.NO)；[WFE上市公司口徑](https://focus.world-exchanges.org/statistics/articles/number-listed-companies)。本地上市公司統計不包含全部外國上市公司；最近非空值的年份可能不同。缺值不是零，不能混年加總全球公司數。\n\nMIC包括營運市場、分段及非股市服務，2883不是股市數，本輪保留全部而不誤刪候選。仍須逐市場核公司名冊、有效日期、本地／外國公司與法人去重；未認定全天下每個股市已被發現或各市場數已補齊。非ISO直接匹配經濟體與歷史政治實體要另核市場存在，不以ISO母表排除。\n'
(R/'Reference/逐國逐市場上市公司數量核查_B83_20261012.qmd').write_text(text,encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
