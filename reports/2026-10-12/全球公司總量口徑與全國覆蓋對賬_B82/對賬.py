from pathlib import Path
import csv,json,hashlib,collections
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/104_全球公司總量口徑與全國覆蓋對賬_B82_20261012';T.mkdir(parents=True,exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rows for k in x)));d.writeheader();d.writerows(rows)
assert not (W/'結果.json').exists()
paths=sorted((R/'Reference/tables').glob('*/registry_structured_directory_records.csv'));allrows=[];base={};groups=collections.defaultdict(list)
for p in paths:
 base[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 for n,x in enumerate(read(p),1):
  row=dict(來源表=p.relative_to(R).as_posix(),來源表記錄=n,来源網址=x.get('source_url',''),名稱原文=x.get('name',''),證券符號原文=x.get('symbol',''),角色原文=x.get('role',''),角色中譯='來源名冊觀察，尚未核定公司／券商',原始記錄JSON=json.dumps(x,ensure_ascii=False),法人識別碼='UNKNOWN（未知）',國別法律關聯='UNKNOWN（未知）')
  allrows.append(row);groups[(x.get('source_url',''),x.get('name',''),x.get('symbol',''),x.get('role',''))].append(row)
write('全部歷史名冊記錄來源索引.csv',allrows)
write('來源名稱符號候選去重組.csv',[dict(来源網址=k[0],名稱原文=k[1],證券符號原文=k[2],角色原文=k[3],觀察數=len(v),原記錄位置JSON=json.dumps([dict(來源表=x['來源表'],來源表記錄=x['來源表記錄']) for x in v],ensure_ascii=False),去重性質='來源名稱符號相同的候選組，非法律實體去重') for k,v in groups.items()])
p=R/'Reference/tables/50_global_directory_content_b25_20261008/registry_all_country_cumulative_source_progress.csv';countries=read(p);base[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
write('全部249國家地區公司總量缺口.csv',[dict(x,全體公司範圍='上市與非上市、國企民企、軍工國防宇航及其他產業',公司總量='UNKNOWN（未知）',唯一法人數='UNKNOWN（未知）',名冊完整性='UNKNOWN（未知）',驗收口徑='固定有效日期；各國公司登記與證券監管、交易所名冊逐項對賬；登記號或LEI法律實體去重',資料時點說明='逐國來源关联沿用B25快照，非2026-10-12全部重新查冊') for x in countries])
definitions=[('公司','法律實體識別碼及本地登記號','基金、信託、個體戶與政府機構分型，不自動算公司'),('券商','監管牌照＋法人＋有效期','同法人多牌照、分支及品牌不直接重複計數'),('上市公司','發行人法律實體＋上市有效期','多地上市、雙櫃台、不同股類不直接增加公司数'),('證券','ISIN或市場代碼＋證券代碼＋日期','基金、債券、權證與牛熊證不當上市公司'),('軍工國防宇航','法人＋產品／採購／供應鏈角色＋日期','上市／非上市、國企／民企全部納入，機密或未公開範圍標缺口')]
write('公司及證券計數業務口徑.csv',[dict(對象=a,識別方式=b,邊界與價值=c) for a,b,c in definitions])
assert len(countries)==249 and len({x['iso_alpha2'] for x in countries})==249
assert sum(len(v) for v in groups.values())==len(allrows)
for p,h in base.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
summary={'歷史結構化來源表':len(paths),'全部來源記錄':len(allrows),'來源名稱符號候選組':len(groups),'現行國家地區母表':len(countries),'公司總量已核國家地區':0,'全球全部公司總數':'UNKNOWN（未知，不能以來源記錄相加）','全球完整性升級':0}
(W/'結果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');(W/'來源雜湊.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf-8')
text='---\ntitle: "全球公司總量口徑與全國覆蓋對賬：第八十二批"\nlang: zh-Hant\nformat: html\n---\n\n使用者要求擴展為ISO 3166-1全部國家／地區的所有公司，不限上市、券商或軍工國防宇航。ISO是國家地區代碼標準，不是全球公司名冊。現行母表249項全部保留，歷史政治實體另沿用既有登記。\n\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n\n[全部原名冊來源索引](tables/104_全球公司總量口徑與全國覆蓋對賬_B82_20261012/全部歷史名冊記錄來源索引.csv)；[全部249項逐國缺口](tables/104_全球公司總量口徑與全國覆蓋對賬_B82_20261012/全部249國家地區公司總量缺口.csv)；[計數定義](tables/104_全球公司總量口徑與全國覆蓋對賬_B82_20261012/公司及證券計數業務口徑.csv)。\n\n來源名稱符號候選組只減少相同來源觀察，不是法律實體唯一公司數。基金、證券、品牌、分支、集團與子公司需分型；本輪沒有把它們相加作全球公司數。日本13期企業披露與香港證券資料仍在B79及B75中保留，此索引只整合17份既有結構化名冊表，不宣稱全項目每種資料已合併。\n\n[ISO國家代碼說明](https://www.iso.org/iso-3166-country-codes.html)；[GLEIF全球LEI索引](https://www.gleif.org/lei-data/global-lei-index)。LEI資料池只能作取得LEI的實體參考，不取代各國全公司登記。官方登記機關清單頁本輪網頁取得逾時，保留缺口，未假造逐國官方名冊。\n\n全球全部公司總數目前不能核定。完成條件是固定時點及公司範圍、逐國取得完整登記、交易所與牌照對賬、處理撤銷與歷史實體、以登記號跨來源去重，然後加總逐國互斥的註冊地法人。軍工國防宇航跨國業務足跡另表，不以足跡重复計數公司。接續需补非上市公司官方登記名冊，金融未嘗試仍沿用B80的2248項。\n'
(R/'Reference/全球公司總量口徑與全國覆蓋對賬_B82_20261012.qmd').write_text(text,encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
