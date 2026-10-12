from pathlib import Path
import sys,subprocess,csv,json,hashlib,urllib.request
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/106_全行業逐市場名冊續核_B84_20261012';T.mkdir(parents=True,exist_ok=True)
def write(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rows for k in x)) or ['無取得記錄']);d.writeheader();d.writerows(rows)
assert not (W/'結果.json').exists()
sources=[('TWSE','臺灣上市公司基本資料','https://openapi.twse.com.tw/v1/opendata/t187ap03_L'),('TPEX','臺灣上櫃公司基本資料','https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O'),('JPX','東京上市公司官方數量','https://www.jpx.co.jp/english/listing/co/'),('HKEX','香港上市公司官方數量','https://www.hkex.com.hk/News/Market-Communications/2026/260930news?sc_lang=en')]
receipts=[];records=[];counts=[]
for sid,name,u in sources:
 a=dict(來源ID=sid,中文名稱=name,網址=u,取得日期='2026-10-12')
 try:
  child="import urllib.request,sys; f=urllib.request.urlopen(urllib.request.Request(sys.argv[1],headers={'User-Agent':'ResearchListing/1.0'}),timeout=10); sys.stdout.buffer.write(f.read())"
  b=subprocess.run([sys.executable,'-c',child,u],capture_output=True,check=True,timeout=25).stdout;a['HTTP狀態']=200
  p=W/(sid+'.response');p.write_bytes(b);a.update(位元組=len(b),SHA256=hashlib.sha256(b).hexdigest(),原始檔=p.relative_to(R).as_posix())
  if sid in ['TWSE','TPEX']:
   data=json.loads(b);assert isinstance(data,list)
   for n,x in enumerate(data,1):records.append(dict(來源ID=sid,來源網址=u,來源行=n,公司代號=x.get('公司代號',x.get('SecuritiesCompanyCode','')),公司名稱=x.get('公司名稱',x.get('CompanyName','')),行業原值=x.get('產業別',x.get('SecuritiesIndustryCode','')),有效日期原值=x.get('出表日期',x.get('Date','')),原始欄位JSON=json.dumps(x,ensure_ascii=False),法人登記完整性='UNKNOWN（未知）'))
   codes=[str(x.get('公司代號',x.get('SecuritiesCompanyCode',''))) for x in data];a['名冊記錄數']=len(data);a['唯一非空代號數']=len(set(c for c in codes if c));a['重複代號數']=len(codes)-len(set(codes))
   counts.append(dict(市場MIC='XTAI' if sid=='TWSE' else 'ROCO',市場中文=name,數量=len(data),數量性質='本輪官方基本資料陣列記錄數，非已完成總量對賬',有效日期='來源每列出表日期另存',來源ID=sid,來源網址=u,名冊完整性='尚須官方統計總量與上市生效狀態對賬'))
 except Exception as e:a['錯誤類型']=type(e).__name__
 receipts.append(a)
counts += [dict(市場MIC='XTKS',市場中文='東京證券交易所全部四板',數量=3883,數量性質='官方上市公司總量',有效日期='2026-10-09',來源ID='JPX',來源網址=sources[2][2],名冊完整性='逐公司完整名冊待核'),dict(市場MIC='XTKS',市場中文='東京證券交易所全部四板',數量=3890,數量性質='官方上市公司月末總量',有效日期='2026-09-30',來源ID='JPX',來源網址=sources[2][2],名冊完整性='逐公司完整名冊待核'),dict(市場MIC='XHKG',市場中文='香港主板與創業板',數量=2772,數量性質='官方上市公司月末總量',有效日期='2026-09-30',來源ID='HKEX',來源網址=sources[3][2],名冊完整性='逐法人名冊與證券清單對賬待核')]
write('官方取得收據.csv',receipts);write('上市櫃公司全部行業名冊觀察.csv',records);write('逐市場官方數量與名冊對賬.csv',counts)
p=R/'Reference/tables/105_逐國逐市場上市公司數量核查_B83_20261012/全部市場逐項上市公司數待核.csv';old=list(csv.DictReader(p.open(encoding='utf-8-sig')));new=[]
for x in old:
 y=dict(x);matches=[c for c in counts if c['市場MIC']==x['市場識別碼']];y['本輪數量來源JSON']=json.dumps(matches,ensure_ascii=False);y['行業範圍']='全部行業，不按軍工或其他產業篩選';new.append(y)
assert len(new)==len(old)==2883
write('全球全部市場數量接續表.csv',new)
summary={'保留全部市場':2883,'本輪取得來源':len(receipts),'成功回應':sum(x.get('HTTP狀態')==200 for x in receipts),'臺灣上市櫃公司來源行':len(records),'逐市場數量觀察':len(counts),'全球全部股市完整性':'UNKNOWN（未知）'}
(W/'結果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');(W/'原市場表雜湊.json').write_text(json.dumps({'路徑':p.relative_to(R).as_posix(),'SHA256':hashlib.sha256(p.read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
text='---\ntitle: "全行業逐市場名冊續核：第八十四批"\nlang: zh-Hant\nformat: html\n---\n\n全部行業納入，沒有軍工或其他行業篩選。全球249項母表、非直接ISO匹配統計經濟體與2883項市場識別候選沿用B83，不因本輪選核市場而刪除其他缺口。臺灣TW已在母表，缺統計不表示沒有ISO代碼。\n\n'+json.dumps(summary,ensure_ascii=False,indent=2)+'\n\n[全球全部市場接續表](tables/106_全行業逐市場名冊續核_B84_20261012/全球全部市場數量接續表.csv)；[逐市場數量](tables/106_全行業逐市場名冊續核_B84_20261012/逐市場官方數量與名冊對賬.csv)；[上市櫃公司逐行名冊](tables/106_全行業逐市場名冊續核_B84_20261012/上市櫃公司全部行業名冊觀察.csv)。\n\n東京2026-10-09官方總量3883家，2026-09-30為3890家，均含四板及5家外國公司；香港2026-09-30主板2466、創業板306，合計2772家。已核官方統計總量，不等於公司法人名冊已完整對賬。臺灣接口陣列全列保留，記錄數與官方總公司数仍須同日對賬，不能直接升級為完整。\n\n'
for sid,name,u in sources:text+=f'- [{name}]({u})。\n'
text+='\n期貨、債券、基金、報告服務與股市分開；同公司多市場上市仍須法人去重。不同時點不得加總作全球唯一公司數。所有未竣工的逐市場名冊、逐國額外市場發現與授權缺口保留，未宣稱天下股市已無遺漏。\n'
(R/'Reference/全行業逐市場名冊續核_B84_20261012.qmd').write_text(text,encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
