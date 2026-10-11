from pathlib import Path
import csv, json, hashlib, subprocess, urllib.request, datetime, re, struct, zlib

根=Path(__file__).resolve().parents[3]
工作=Path(__file__).resolve().parent
表=根/'Reference/tables/78_中文化與缺口核實_B55_20261011'
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
雜湊=lambda b:hashlib.sha256(b).hexdigest()
assert not (工作/'基線.json').exists(),'禁止刷新基線'
表.mkdir();(工作/'原始證據').mkdir()
舊文=(根/主).read_bytes()
路徑=[p for p in subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0') if p]
基線={'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'原有文件':{p:雜湊((根/p).read_bytes()) for p in 路徑 if Path(p).suffix in ('.md','.qmd') and (根/p).is_file()},'主報告':主,'原文位元組':len(舊文),'原文雜湊':雜湊(舊文)}
(工作/'基線.json').write_text(json.dumps(基線,ensure_ascii=False,indent=2),encoding='utf-8')
def 寫表(名,資料):
    with (表/名).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(資料[0]));w.writeheader();w.writerows(資料)
詞={'Reference':'參考資料','reports':'報告','tables':'數據表','registry':'登記','global':'全球','historical':'歷史','polities':'政治實體','technology':'科技','ecosystem':'生態體系','aerospace':'宇航','report':'報告','geostrategy':'地緣戰略','defense':'國防','industry':'產業','artificial':'人工','intelligence':'智能','interlligence':'智能（原名筆誤）','inteligent':'智能（原名筆誤）','interligent':'智能（原名筆誤）','ais':'自動識別系統','quality':'品質','semantics':'語意','access':'取用','resolution':'核解','source':'來源','sources':'來源','terms':'條款','rights':'權利','dictionary':'字典','field':'欄位','versioned':'版本化','schema':'結構','migration':'遷移','comparison':'比較','official':'官方','annual':'年度','summary':'摘要','prefix':'前綴','use':'用途','review':'覆核','receipt':'收據','receipts':'收據','validation':'驗收','baseline':'基線','build':'生成','finish':'完成','verify':'驗證','security':'密碼掃描','publish':'提交推送','test':'測試','preserved':'保留','gap':'缺口','public':'公開','layer':'圖層','csv':'逗號分隔數據表','html':'網頁','qmd':'可渲染源文件','md':'說明文件','json':'結構化記錄','sqlite':'嵌入式數據庫','py':'程式源文件','png':'無損圖片','pdf':'可攜式文件','git':'版本控制','commercial':'商業','platform':'平臺','details':'詳情','metadata':'元資料','granule':'資料粒度','product':'產品','products':'產品','collection':'集合','catalog':'目錄','content':'內容','data':'資料','daily':'逐日','objects':'物件','header':'表頭','noaa':'美國國家海洋暨大氣總署','esri':'環境系統研究所公司','item':'項目','service':'服務','services':'服務','workqueue':'工作佇列','work':'工作','directory':'名錄','directories':'名錄','market':'市場','followup':'接續','raw':'原始證據','actionplan':'行動清單','redteam':'對抗審核','critic':'批判核對','killcritic':'批判再審','blindspot':'盲點核查','blueprint':'施工藍圖','cheatsheet':'速查要點','audit':'稽核','scan':'掃描','workspace':'工作區','change':'變更','and':'與','web':'網頁','version':'版本','map':'地圖','timeline':'年代','universe':'總體範圍','expansion':'擴展','financial':'金融','currency':'貨幣','currencies':'貨幣','listed':'上市','companies':'公司','brokers':'證券行','government':'政府','research':'科研','neurotechnology':'神經科技','network':'網絡','egaming':'電子博彩','online':'線上','gaming':'博彩','decision':'決策','lab':'實驗室','frontier':'前沿','iso249':'國際標準化組織249項母表（非主權國家數）','iso':'國際標準化組織','iso3166':'國家與地區代碼標準','gitignore':'版本控制忽略規則','gitattributes':'版本控制檔案屬性','readme':'閱讀說明','agents':'協作規則','license':'許可','tests':'測試','staged':'暫存','acceptance':'驗收','credential':'憑證','append':'附加','delivery':'交付','intake':'接收'}
盤點=[]
for p in 路徑:
    token=re.findall(r'[A-Za-z][A-Za-z0-9]*',Path(p).name)
    未譯=sorted({t for t in token if t.lower() not in 詞 and not re.fullmatch(r'[BbVv]\d+',t)})
    顯示='／'.join(詞.get(t.lower(),t+'（待核中譯）') if not re.fullmatch(r'[BbVv]\d+',t) else t+'（批次或版本代碼）' for t in token)
    盤點.append({'原路徑':p,'中文顯示對照':顯示 or '中文名稱或無外語詞','待核外語詞':'；'.join(未譯),'名稱狀態':'待人工核譯及引用遷移' if 未譯 else '已有詞級中文對照，完整語意待覆核','是否已改名':'否','文件存在':(根/p).is_file()})
寫表('全項目檔名中譯盤點.csv',盤點)
提交=[]
確譯={'fab1620':'核實歷史自動識別系統有界樣本品質及中文用途審核','371212d':'保留各年代自動識別系統欄位結構及用途限制','4fbc32e':'補核星盾公開頁面取用及地理資訊權利','092ec1f':'覆核星盾、格羅克及逐項地理資訊與天氣語意','f5ab643':'登記商業宇航、地理資訊、天氣及人工智能生態來源'}
for line in subprocess.check_output(['git','log','--all','--format=%H%x09%aI%x09%s'],cwd=根).decode('utf-8').splitlines():
    h,date,title=line.split('\t',2);中=確譯.get(h[:7])
    if not re.search('[A-Za-z]',title):中=title
    提交.append({'提交雜湊':h,'提交時間':date,'原提交訊息':title,'中文對照':中 or '待逐條核譯，原提交保留','中譯狀態':'人工核譯' if 中 else '待核譯','是否改寫歷史':'否'})
寫表('全部可見提交中譯索引.csv',提交)
來源=[]
網址=[('甲類位置報告','https://www.navcen.uscg.gov/ais-class-a-reports'),('乙類位置報告','https://www.navcen.uscg.gov/ais-class-b-reports'),('甲類靜態與航程報告','https://www.navcen.uscg.gov/ais-class-a-static-voyage-message-5')]
for 名,url in 網址:
    r={'來源中文名稱':名,'官方網址':url,'取得時間':datetime.datetime.now(datetime.timezone.utc).isoformat(),'回應狀態':'','保存路徑':'','雜湊':'','錯誤':''}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PublicResearchRegistry/1.0'}),timeout=30) as response:
            b=response.read(2000001);assert len(b)<=2000000;r['回應狀態']=response.status
        p=工作/'原始證據'/(名+'.html');p.write_bytes(b);r.update(保存路徑=p.relative_to(根).as_posix(),雜湊=雜湊(b))
    except Exception as e:r['錯誤']=type(e).__name__;r['回應狀態']=getattr(e,'code','未取得')
    來源.append(r)
寫表('官方來源取得收據.csv',來源)
from html.parser import HTMLParser
class 文本(HTMLParser):
    def __init__(self):super().__init__();self.x=[]
    def handle_data(self,s):self.x.append(s)
證據=[]
for r in 來源[:2]:
    if not r['保存路徑']:continue
    parser=文本();parser.feed((根/r['保存路徑']).read_text(encoding='utf-8'));s=' '.join(' '.join(parser.x).split());assert '511' in s and 'heading' in s.lower()
    i=s.find('True heading');片段=s[i:i+180] if i>=0 else ''
    assert '511' in 片段 and 'not available' in 片段
    證據.append({'核查項':'真航向511缺值編碼','來源':r['來源中文名稱'],'英文欄名':'True heading','中文欄名':'真航向','原文短摘':片段[:105],'中文核對':'511表示不可用；有效真航向為0至359度','驗證範圍':'廣播協議明文；不是所有2019加工記錄逐項溯源','原始資料處理':'保留原值，不自動修正','證據狀態':'官方明文已核','來源路徑':r['保存路徑'],'來源雜湊':r['雜湊']})
assert len(證據)==2
寫表('真航向缺值官方核對.csv',證據)
原始=根/'reports/2026-10-11/access_resolution_b52/raw/B52NOAAZIPHEADER.part';b=原始.read_bytes();assert 雜湊(b)=='8ffc7f5fb2ba829c4d6c7d5aee2ad06a707bf80462e2aea1387f1e52048bd159'
f=struct.unpack('<IHHHHHIIIHH',b[:30]);assert f[3]==8;dec=zlib.decompressobj(-15);解=dec.decompress(b[30+f[-2]+f[-1]:],2000000);assert not dec.unconsumed_tail
行=list(csv.DictReader(解[:解.rfind(b'\n')+1].decode('utf-8-sig').splitlines()));assert len(行)==1683
異常=[('真航向缺值','Heading（真航向）',sum(r['Heading']=='511.0' or r['Heading']=='511' for r in 行),872),('吃水負值','Draft（吃水）',sum(float(r['Draft'])<0 for r in 行 if r['Draft']),2),('識別字串格式不符','MMSI（海上移動通信業務識別碼）',sum(not(len(r['MMSI'])==9 and r['MMSI'].isdigit()) for r in 行),3)]
assert all(n==expected for _,_,n,expected in 異常)
寫表('歷史樣本異常重現核查.csv',[{'核查項':名,'原欄名與中譯':欄,'重現計數':n,'前輪計數':預期,'分母':len(行),'核對結果':'一致','是否知道根本原因':'否；待來源處理記錄','原值處理':'保持原值','來源原始雜湊':雜湊(b)} for 名,欄,n,預期 in 異常])
缺口=[('全量品質','未完成','原始全檔完整性、全年缺值及重複率未驗證','完整歷史檔串流、壓縮完整性與分區對賬'),('真航向511協議語意','已核明文','甲乙類官方協議均明列缺值；加工歷程逐項溯源仍未完成','保留原值，逐來源版本核查'),('負吃水與異常識別碼根因','未完成','重現數量不等於根因已知','核來源處理規則及原始輸入'),('逐用途授權','未取得新增許可','官方條件審核不等於授權人批准','逐產品及用途取得適用條款或許可'),('全球覆蓋','未完成','區域地面接收樣本不能替代全球驗收','逐來源地域與時間覆蓋證據'),('全部檔名中譯遷移','未完成','已有全量盤點；人工譯名與引用遷移未完成','依引用關係分批新增中文入口與遷移'),('歷史提交全部中譯','未完成','保存全部可見歷史；只核譯部分近期訊息','逐條中譯索引，不改寫提交雜湊')]
寫表('未完成核實清單.csv',[dict(項目=n,狀態=s,證據或限制=e,下一步=a) for n,s,e,a in 缺口])
統計={'盤點已追蹤路徑':len(盤點),'待核外語詞路徑':sum(bool(r['待核外語詞']) for r in 盤點),'可見歷史提交':len(提交),'已核中文提交對照':sum(r['中譯狀態']=='人工核譯' for r in 提交),'官方協議核查':len(證據),'歷史样本完整行':len(行),'異常重現項':len(異常),'全球完成':False,'既有檔案改名':0}
(工作/'核查結果.json').write_text(json.dumps(統計,ensure_ascii=False,indent=2),encoding='utf-8')
報告='''---
title: "中文化與缺口核實：第五十五批"
date: 2026-10-11
lang: zh-TW
format:
  html:
    toc: true
    embed-resources: true
---

## 中文交付與歷史保留

本批新增檔名、數據表、核查結果與提交訊息採用中文。Git（分散式版本控制）的既有提交雜湊不改寫；以中譯索引保留原提交訊息與中文解釋。英文原檔路徑逐項盤點，但词級對照不是已完成的自然中文譯名，未知詞明列待核。尚未完成全部舊檔名的人工中譯及引用遷移，不冒稱全項目已中文化。副檔名與協議標識作為格式識別保留。

## 補核真航向缺值

美國海岸防衛隊航行中心的[甲類位置報告](https://www.navcen.uscg.gov/ais-class-a-reports)與[乙類位置報告](https://www.navcen.uscg.gov/ais-class-b-reports)，均明列True heading（真航向）的有效值為0至359度，511表示不可用。這補強了此前常見問題文件只談早期資料而留下的協議語意缺口。

這是對官方廣播協議的核實，不是對2019年全部加工記錄的溯源認證。解釋層可以識別缺值編碼，原始值仍保留；不得用511當作真實方向，也不自行覆寫原值。AIS（自動識別系統）的地域覆蓋和接收中斷仍須另核。

## 樣本异常重新核對

重新從既有65536位元組封存前綴有界解壓，核SHA256（安全雜湊演算法256位元）與完整換行，再現1683行樣本。真航向511共872行、負吃水2行、MMSI（海上移動通信業務識別碼）格式不符3行，與前輪一致。只保存彙總；異常原因尚不能由計數推定。

完整ZIP（壓縮封裝格式）的CRC（循環冗餘校驗）及全量資料品質依然未驗證。逐用途授權未獲新增許可；付費、私人與受限服務需適用授權才能核查其實際內容。不存在以補寫文字代替授權或全量實測的做法。

## 中文清單與驗收

'''+''.join('- '+k+'：'+str(v)+'。\n' for k,v in 統計.items())+'''

[全項目檔名中譯盤點](tables/78_中文化與缺口核實_B55_20261011/全項目檔名中譯盤點.csv)、[全部可見提交中譯索引](tables/78_中文化與缺口核實_B55_20261011/全部可見提交中譯索引.csv)、[真航向缺值官方核對](tables/78_中文化與缺口核實_B55_20261011/真航向缺值官方核對.csv)、[異常重現核查](tables/78_中文化與缺口核實_B55_20261011/歷史樣本異常重現核查.csv)、[未完成清單](tables/78_中文化與缺口核實_B55_20261011/未完成核實清單.csv)。

接續按引用關係核譯與遷移舊檔名，保留每項來源、年代、地域、用途及證據層次；原宇航比較報告、舊196筆及全球金融、歷史政治實體、神經科技清單均不覆寫。未完成項逐項續作，不以樣本或來源宣告充當全球完成。
'''
(根/'Reference/中文化與缺口核實_B55_20261011.qmd').write_text(報告,encoding='utf-8')
附加='\n\n<!-- 中文化與缺口核實_B55_20261011_開始 -->\n## 2026-10-11 中文化與缺口核實：第五十五批\n\n新增[中文檔名與提交索引及缺口核查](中文化與缺口核實_B55_20261011.qmd)。全項目已追蹤路徑及可見歷史提交逐項盤點；官方協議補核真航向511缺值，異常樣本重新重現。既有名稱引用保留，全部人工中譯與全量品質仍未完成。\n<!-- 中文化與缺口核實_B55_20261011_結束 -->\n'
(根/主).write_bytes(舊文+附加.encode('utf-8'));(工作/'附加收據.json').write_text(json.dumps({'附加雜湊':雜湊(附加.encode('utf-8'))},ensure_ascii=False),encoding='utf-8')
for 目錄,標題 in [('redteam','對抗審核'),('critic','批判核對'),('killcritic','批判再審'),('blindspot','盲點核查'),('blueprint','施工藍圖'),('cheatsheet','速查要點'),('actionplan','行動清單')]:
    (根/目錄/'中文化與缺口核實_B55_20261011.md').write_text('# '+標題+'｜第五十五批\n\n官方協議缺值明文已補核；異常根因、全量品質、用途許可及全球覆蓋不得冒稱完成。舊檔名盤點之後，逐項核中文譯名與引用關係，分批遷移，不改寫既有提交歷史。\n\n[中文報告](../Reference/中文化與缺口核實_B55_20261011.qmd)。\n',encoding='utf-8')
print(json.dumps(統計,ensure_ascii=False))
