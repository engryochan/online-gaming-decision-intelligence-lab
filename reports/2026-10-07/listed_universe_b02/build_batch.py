from pathlib import Path
import csv,json,hashlib,sqlite3,collections,datetime
import openpyxl
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/20_global_listed_universe_b02_20261007';T.mkdir(exist_ok=True)
def dump(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def norm(v):
 return v.isoformat() if isinstance(v,(datetime.datetime,datetime.date)) else v
allrows=[];cells=[];sources=[]
for feed,file,skip,country,url in [('JPX_TSE','data_j.xlsx',0,'JP','https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xlsx'),('HKEX','ListOfSecurities.xlsx',2,'HK','https://www.hkex.com.hk/eng/services/trading/securities/securitieslists/ListOfSecurities.xlsx')]:
 p=O/'raw'/file;w=openpyxl.load_workbook(p,read_only=True,data_only=True);s=w.active;s.reset_dimensions();values=[list(map(norm,row)) for row in s.values];headers=values[skip];data=[];blanks=0
 for number,row in enumerate(values,1):cells.append(dict(feed=feed,sheet=s.title,excel_row=number,cells_json=json.dumps(row,ensure_ascii=False)))
 for number,row in enumerate(values[skip+1:],skip+2):
  if not any(v is not None for v in row):blanks+=1;continue
  assert len(row)==len(headers)
  raw=dict(zip(headers,row));code=row[1] if feed=='JPX_TSE' else row[0];name=row[2] if feed=='JPX_TSE' else row[1];category=row[3] if feed=='JPX_TSE' else row[2]
  assert code is not None and name is not None
  data.append(dict(record_id=f'{feed}:{number}',feed=feed,excel_row=number,security_code=str(code),security_name=name,category=category,subcategory='' if feed=='JPX_TSE' else row[3],ISIN='' if feed=='JPX_TSE' else row[5],market_iso_alpha2=country,issuer_identity='UNRESOLVED',issuer_domicile='UNKNOWN',raw_fields_json=json.dumps(raw,ensure_ascii=False)))
 allrows.extend(data);sources.append(dict(feed=feed,url=url,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),data_rows=len(data),workbook_rows=len(values),blank_rows=blanks,as_of='2026-09-30' if feed=='JPX_TSE' else values[1][0],retrieved_on='2026-10-07',scope='SOURCE_ALL_ROWS_NOT_COUNTRY_ALL_EXCHANGES'))
dump('registry_listing_records.csv',allrows);dump('workbook_rows_lossless.csv',cells);dump('source_manifest.csv',sources)
c=collections.Counter((r['feed'],r['category'],r['subcategory']) for r in allrows)
dump('category_analysis.csv',[dict(feed=k[0],category=k[1],subcategory=k[2],security_rows=v,unique_company_count='UNKNOWN') for k,v in sorted(c.items())])
with (R/'Reference/tables/19_global_listed_company_universe_20261007/registry_country_market_coverage.csv').open(encoding='utf-8-sig') as f:mother=list(csv.DictReader(f))
for row in mother:
 if row['iso_alpha2'] in ['JP','HK']:
  row['market_feed_state']='PARTIAL_OFFICIAL_FEEDS_INGESTED';row['security_rows']=sum(1 for r in allrows if r['market_iso_alpha2']==row['iso_alpha2'])
dump('registry_country_market_coverage.csv',mother)
db=O/'listed_universe_b02.sqlite';assert not db.exists();con=sqlite3.connect(db)
for name,rows in [('listing_records',allrows),('workbook_rows',cells),('sources',sources),('country_coverage',mother)]:
 keys=list(rows[0]);con.execute('CREATE TABLE '+name+' ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for k in keys)+')',[[None if r[k] is None else str(r[k]) for k in keys] for r in rows])
assert [json.loads(x[0]) for x in con.execute('SELECT cells_json FROM workbook_rows')]==[json.loads(r['cells_json']) for r in cells]
con.commit();con.close()
result=dict(listing_records=len(allrows),workbook_rows=len(cells),sources=sources,countries=249,workbook_cells_roundtrip=True,company_count='UNKNOWN',global_complete=False)
(O/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
text='''---
title: "全球上市名錄 B02：東證與港交所完整來源接收"
lang: zh-Hant
format: html
---

## 定義與覆蓋

首批13,285是證券記錄，不是證券行、上市公司或全球總數。證券行屬金融服務機構；上市公司涵蓋全部產業，不按科技題材或知名度抽選。公司、證券、上市關係與市場所在地分表處理；跨市場和不同股類尚未取得身份證據前不合併、不報唯一公司數。

本批完整讀取兩份官方工作簿所有工作表列，收錄 **TOTAL 筆上市／證券記錄**。全項目來源記錄累計 **CUMULATIVE 筆**，未去重，亦非公司總數。

|來源|資料列|截至日期|范围|
|---|---:|---|---|
SOURCE_TABLE

[JPX官方頁](https://www.jpx.co.jp/markets/statistics-equities/misc/01.html)提供東證月末上市銘柄，不能當成日本全部交易所。[HKEX官方頁](https://www.hkex.com.hk/Services/Trading/Securities/Securities-Lists?sc_lang=en)提供完整證券清單；含股票、衍生權證、牛熊證、債券、ETP與REIT，產品數不能當成公司數。兩地上市的外國公司也不能自動歸為該市場本地公司。

## 全量資料與驗收

- [上市記錄全部列](tables/20_global_listed_universe_b02_20261007/registry_listing_records.csv)
- [工作簿逐列保留](tables/20_global_listed_universe_b02_20261007/workbook_rows_lossless.csv)：標題、日期、欄名、空白列也保留；原始 xlsx 另存來源批次。
- [官方分類分析](tables/20_global_listed_universe_b02_20261007/category_analysis.csv)
- [來源、日期與SHA256](tables/20_global_listed_universe_b02_20261007/source_manifest.csv)
- [249國家／地區覆蓋](tables/20_global_listed_universe_b02_20261007/registry_country_market_coverage.csv)

SQLite位於 `reports/2026-10-07/listed_universe_b02/listed_universe_b02.sqlite`。HKEX工作簿的宣告範圍僅到第8列；解析時重新掃描實際全部行，防止依宣告範圍而遺漏後續資料。完整欄位、空值與Excel列號保留，資料庫逐列還原驗證通過。來源列全收錄不等於來源自身及全國市場已無遺漏。

## 每家公司不遺漏的完成條件

249條目逐一確認交易所及監管機構；對每個交易所接收官方全量股票及公司名錄，核對來源總数與報表日期，解析發行人官方身份及公司全名，建立一家公司多項上市的關係。再按註冊地、總部及市場所在地分別歸國。基金、權證及其他證券保留在產品表，不混入上市公司總數；歷史退市另按有效日期保存。

目前US、JP、HK有官方来源批次；其餘246條目尚未接收，三個已接收市場也未宣稱全國全部公司完成。公司唯一身份、完整交易所枚舉及全球總數仍UNKNOWN。這些缺口必須逐項閉合後，才可宣稱每國每家公司已收齊。
'''
text=text.replace('TOTAL',f'{len(allrows):,}').replace('CUMULATIVE',f'{13285+len(allrows):,}').replace('SOURCE_TABLE','\n'.join(f"|{r['feed']}|{r['data_rows']:,}|{r['as_of']}|完整來源全部列|" for r in sources))
(R/'Reference/Global_Listed_Company_Universe_B02_20261007.qmd').write_text(text,encoding='utf-8');print(json.dumps(result,ensure_ascii=True))
