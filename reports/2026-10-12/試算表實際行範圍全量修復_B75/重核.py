from pathlib import Path
import io,csv,json,hashlib,zipfile,xml.etree.ElementTree as E,collections,subprocess
from openpyxl import load_workbook
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/97_試算表實際行範圍全量修復_B75_20261012';T.mkdir(parents=True,exist_ok=True)
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig')))
def write(n,rows):
 fields=list(dict.fromkeys(k for x in rows for k in x)) or ['無觀察']
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=fields);d.writeheader();d.writerows(rows)
assert not (W/'結果.json').exists()
B=R/'Reference/tables/96_金融下載與分頁分類續核_B74_20261012';old=read(B/'試算表來源全量行.csv');receipts=read(B/'下載與分頁收據.csv');rows=[];audits=[];baseline={}
for x in receipts:
 if not x.get('原始檔') or 'XLSX' not in x.get('解析',''):continue
 p=R/x['原始檔'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==x['SHA256'];baseline[x['原始檔']]=x['SHA256']
 book=load_workbook(io.BytesIO(b),read_only=True,data_only=False);z=zipfile.ZipFile(p)
 for index,s in enumerate(book,1):
  declared=s.calculate_dimension();s.reset_dimensions();before=[v for v in old if v['網址']==x['網址'] and v['工作表']==s.title];n=0
  for num,values in enumerate(s.iter_rows(values_only=True),1):
   if any(v is not None for v in values):rows.append(dict(網址=x['網址'],工作表=s.title,行=num,欄值JSON=json.dumps(values,ensure_ascii=False,default=str),語義='原始来源行，實體及完整性待核',來源SHA256=x['SHA256']));n+=1
  # worksheet XML names are inspected directly rather than assuming all declared dimensions are trustworthy.
  audits.append(dict(網址=x['網址'],工作表=s.title,宣告範圍=declared,舊非空行=len(before),重核非空行=n,新增行=n-len(before)))
 book.close()
 # Preserve independent XML row observations for every worksheet part.
 for name in z.namelist():
  if name.startswith('xl/worksheets/sheet') and name.endswith('.xml'):
   root=E.fromstring(z.read(name));ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};dim=root.find('s:dimension',ns);rs=root.findall('s:sheetData/s:row',ns)
   audits.append(dict(網址=x['網址'],XML成員=name,XML宣告範圍=dim.attrib.get('ref','') if dim is not None else '',XML行節點=len(rs),XML最大行=max([int(v.attrib.get('r',0)) for v in rs],default=0)))
oldxlsx=[x for x in old if x['網址'] in {a['網址'] for a in rows}]
lookup={(x['網址'],x['工作表'],str(x['行'])):x['欄值JSON'] for x in rows}
def norm(v):
 a=json.loads(v)
 while a and a[-1] is None:a.pop()
 return a
assert all(norm(lookup[(x['網址'],x['工作表'],x['行'])])==norm(x['欄值JSON']) for x in oldxlsx),'舊來源行不得遺漏或改寫'
write('實際全量試算表來源行.csv',rows);write('宣告範圍與實際行對賬.csv',audits)
securities=[x for x in rows if 'ListOfSecurities.xlsx' in x['網址']];data=[];cats=collections.Counter()
for x in securities:
 v=json.loads(x['欄值JSON'])
 if len(v)>5 and str(v[0]).isdigit():
  cats[(str(v[2]),str(v[3]))]+=1;data.append(dict(來源行=x['行'],證券代碼=str(v[0]),證券名稱原文=v[1],類別原文=v[2],子類別原文=v[3],ISIN=v[5],交易貨幣=v[16] if len(v)>16 else '',原始欄值JSON=x['欄值JSON'],公司關聯='UNKNOWN（未知）'))
write('港交所逐證券分類觀察.csv',data);write('港交所來源類別計數.csv',[dict(類別原文=k[0],子類別原文=k[1],來源記錄數=n) for k,n in sorted(cats.items())])
summary=dict(XLSX舊行=len(oldxlsx),XLSX重核行=len(rows),新增保留行=len(rows)-len(oldxlsx),舊行逐欄保留=True,港交所證券觀察=len(data),證券代碼重複=len(data)-len({x['證券代碼'] for x in data}),公司完整性升級=0)
(W/'結果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');(W/'來源雜湊.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
text='---\ntitle: "試算表實際行範圍全量修復：第七十五批"\nlang: zh-Hant\nformat: html\n---\n\n第七十四批只按XLSX宣告範圍串流解析。本輪發現宣告範圍可能小於實際資料，對所有已解析XLSX重設串流範圍並讀取實際全部非空行；逐檔保留原始位元組並檢查所有舊行逐欄一致。舊批次不覆寫，其「全量」僅為當時解析器輸出，應以本轮對賬補正。\n\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n\n[行範圍對賬](tables/97_試算表實際行範圍全量修復_B75_20261012/宣告範圍與實際行對賬.csv)；[逐證券分類](tables/97_試算表實際行範圍全量修復_B75_20261012/港交所逐證券分類觀察.csv)。\n\n類別及名稱保留來源原文：Equity（股權）、Debt Securities（債務證券）、Exchange Traded Products（交易所買賣產品）、Derivative Warrants（衍生權證）、Callable Bull/Bear Contracts（牛熊證）；其他標籤待逐一中譯。不能把證券數直接當上市公司數，ISIN、雙櫃台及法律實體關聯、授權仍待核。資料日期保留於來源標題行，不以取得日期冒充業務有效日期。\n'
(R/'Reference/試算表實際行範圍全量修復_B75_20261012.qmd').write_text(text,encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
