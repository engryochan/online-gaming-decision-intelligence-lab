from pathlib import Path
import csv,json,hashlib,io,importlib.util,subprocess
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/109_全對話清單接續_B87_20261013';T.mkdir(parents=True,exist_ok=True)
assert not (W/'結果.json').exists()
def read(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def write(n,rows):
 with (T/n).open('w',encoding='utf-8-sig',newline='') as f:
  d=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in rows for k in x)) or ['無資料']);d.writeheader();d.writerows(rows)
p=W/'市場參與者.response';b=p.read_bytes();lines=b.decode('utf-8-sig').splitlines();footer=[x for x in lines if x.startswith('File Creation Time:')];data=list(csv.DictReader(io.StringIO('\n'.join(x for x in lines if not x.startswith('File Creation Time:'))),delimiter='|'));assert data and 'MPID' in data[0]
rows=[dict(來源行=i,市場參與者代碼=x['MPID'],名稱原值=x.get('Name',''),名稱中譯='待逐項中譯',類型原值=x.get('MP Type',''),全部原欄位JSON=json.dumps(x,ensure_ascii=False),法人唯一識別='UNKNOWN（未知）',來源網址='https://www.nasdaqtrader.com/dynamic/SymDir/mpidlist.txt') for i,x in enumerate(data,1)]
write('市場參與者全部原始記錄.csv',rows)
receipts=[]
sources=[('領域既有清單','Reference/tables/94_全項目進度審計_B72_20261012/領域進度與優先施工清單.csv'),('金融全部來源工作','Reference/tables/102_全球金融未嘗試來源續查_B80_20261012/全4849項接續進度.csv'),('金融及國防宇航逐國範圍','Reference/tables/101_金融實體與國防宇航範圍整合_B79_20261012/逐國金融與國防宇航接續範圍.csv'),('全球全部市場','Reference/tables/107_全球交易所與美國證券全量續核_B85_20261012/全球全部市場數量接續表.csv'),('服務授權逐圖層','Reference/tables/86_公開服務逐圖層核查_B63_20261011/逐圖層結構與授權狀態.csv'),('未完成核實舊清單','Reference/tables/78_中文化與缺口核實_B55_20261011/未完成核實清單.csv')]
for n,s in sources:
 p=R/s;old=read(p);write(n+'.csv',old);receipts.append(dict(清單=n,原來源=s,SHA256=hashlib.sha256(p.read_bytes()).hexdigest(),保留原記錄數=len(old),完整性='保留清單，不等於實質核實完成'))
write('清單保留與来源索引.csv',receipts)
scopes=[('全行業上市公司','逐國逐市場名冊、同日總量、法人識別、多地上市去重'),('證券行與交易所','監管持牌法人、分支、市場參與者、交易所、清算機構分開核定'),('國家地區及非ISO實體','ISO現行及歷史、非ISO政治與統計實體均保留；不能固定249為全部歷史總量'),('貨幣','現行、歷史、地方貨幣及基金金屬代碼分流'),('歷史政治實體','年代、疆界、勢力範圍、史前證據與爭議來源'),('科技與神經技術','公司大學政府軍方公開項目、技術、方向、遠程、帶寬、人體試驗、監管、N0至N7證據'),('國防宇航與人工智能','上市及未上市、國企民企、供應鏈、SpaceX星盾、xAI、Grok、Palantir、ArcGIS、Meteomatics等來源及中譯'),('地理氣象海事影像','全量品質、地域覆蓋、逐產品用途授權及付費私人資料取得缺口'),('文件整合與版本','原始報告保留、最新版本差異、拼寫歷史、下载目錄取精髓不直接收錄、使用者改動保護'),('HTML與QMD','逐成品來源回溯及重渲比對、禁止恢復Untitled.qmd'),('中文交付與安全Git','中文檔名及提交、原外語雙顯中譯、密碼隔離及限定範圍提交推送'),('七類審閱','redteam、critic、killcritic、blindspot、blueprint、cheatsheet、actionplan接續審閱')]
write('全對話範圍與未竣工驗收要求.csv',[dict(範圍=n,驗收要求=d,完成狀態='未竣工，逐項證據驗收',來源='本對話使用者指令，非外部資料事實') for n,d in scopes])
result={'新增市場參與者來源行':len(rows),'非空MPID唯一數':len(set(x['MPID'] for x in data if x['MPID'])),'全球券商法人數':'UNKNOWN（未知）','原接續清單數':len(receipts),'全對話施工範圍':len(scopes),'原始檔SHA256':hashlib.sha256(b).hexdigest(),'檔尾':footer,'實際取得日期':'2026-10-13'}
(W/'結果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
q=R/'Reference/全對話清單接續_B87_20261013.qmd';text='---\ntitle: "全對話清單接續與市场參與者續核：第八十七批"\nlang: zh-Hant\nformat: html\n---\n\n已保留最近使用者兩筆研究文件整合提交及B86未提交審計；未覆寫原宇航報告。將對話範圍彙整為12類驗收要求，並完整承接六份原清單，不將網站下載成功或數量增加當作全球竣工。此範圍表是對話索引，並非宣稱所有歷史文件內容均已審閲。\n\n'
text+='```json\n'+json.dumps(result,ensure_ascii=False,indent=2)+'\n```\n\n'
text+='[逐項市場參與者](tables/109_全對話清單接續_B87_20261013/市場參與者全部原始記錄.csv)、[全對話驗收要求](tables/109_全對話清單接續_B87_20261013/全對話範圍與未竣工驗收要求.csv)、[原清單保留索引](tables/109_全對話清單接續_B87_20261013/清單保留與来源索引.csv)。\n\n市場參與者碼（MPID）可代表不同交易參與者或分支，不是全球券商法人名冊。完整保留所有類型及會員旗標，不按券商名稱猜測或刪除其他角色；法人去重、監管狀態與全球券商總量仍待核。\n\n[官方名冊](https://www.nasdaqtrader.com/dynamic/SymDir/mpidlist.txt)與[字段定義](https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs)。\n';q.write_text(text,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:
 (R/n/'全對話清單接續_B87_20261013.md').write_text('# 全對話清單接續\n\n'+{'redteam':'防止把證券行數、參與者碼及下載成功誤報為全球法人總數。','critic':'本輪取得美國參與者名冊，不能取代其他國家的監管證據。','killcritic':'尚未取得法人識別，不以名稱相似自動合併或刪除。','blindspot':'史前政治實體、非ISO市場、付費資料與逐用途授權仍列缺口。','blueprint':'以清單來源雜湊、原行JSON、角色、時間、法人識別及驗收狀態建立可追溯關係。','cheatsheet':'證券≠券商≠上市公司≠交易所；未知不填零。','actionplan':'先逐項分類新參與者並核監管身份，接續全球金融未嘗試來源；各領域依驗收要求續作。'}[n]+'\n',encoding='utf-8')
spec=importlib.util.spec_from_file_location('核查',R/'reports/2026-10-11/未啟動服務替代來源核查_B65/驗證與提交.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.工作=W;m.範圍=[W.relative_to(R).as_posix(),T.relative_to(R).as_posix(),q.relative_to(R).as_posix()]+[n+'/全對話清單接續_B87_20261013.md' for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']];m.密碼掃描();print(json.dumps(result,ensure_ascii=False))
