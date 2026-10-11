from pathlib import Path
import csv,json,subprocess,re,hashlib,urllib.parse
根=Path(__file__).resolve().parents[3];工作=Path(__file__).resolve().parent
表=根/'Reference/tables/80_中文報告入口與引用核查_B57_20261011'
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd';雜湊=lambda b:hashlib.sha256(b).hexdigest()
assert not (工作/'基線.json').exists(),'禁止刷新基線'
表.mkdir();原文=(根/主).read_bytes()
路徑=[p for p in subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0') if p]
基={'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'原有文件':{p:雜湊((根/p).read_bytes()) for p in 路徑 if Path(p).suffix in ('.md','.qmd') and (根/p).is_file()},'主報告':主,'原文位元組':len(原文),'原文雜湊':雜湊(原文)}
(工作/'基線.json').write_text(json.dumps(基,ensure_ascii=False,indent=2),encoding='utf-8')
def 讀表(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def 寫表(名,資料):
    with (表/名).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(資料[0]));w.writeheader();w.writerows(資料)
對照=[('Access_Resolution_B52_20261011','星盾頁面與地理資訊授權核對_B52_20261011','星盾頁面與地理資訊授權核對'),('AIS_Semantics_B53_20261011','自動識別系統年代化欄位核對_B53_20261011','自動識別系統年代化欄位核對'),('AIS_Quality_B54_20261011','歷史自動識別系統樣本品質核對_B54_20261011','歷史自動識別系統樣本品質核對')]
詞={'SpaceX':'太空探索技術公司','Starshield':'星盾','Esri':'環境系統研究所公司','ArcGIS':'阿克地理資訊系統（平臺譯稱）','Living Atlas':'全球即時地圖集（產品譯稱）','Grok':'格羅克（產品譯稱）','xAI':'艾克斯人工智能公司（譯稱）','Meteomatics':'米特奧氣象資料公司（譯稱）','AIS':'自動識別系統','NOAA':'美國國家海洋暨大氣總署','FAQ':'常見問題','HTTP':'超文本傳輸協議','API':'應用程式介面','Token Required':'需要身份憑證','Range':'範圍請求','Content-Range':'回應位元組範圍','bytes':'位元組','ZIP':'壓縮封裝格式','CSV':'逗號分隔數據表','QMD':'可渲染源文件','HTML':'網頁標記格式','PDF':'可攜式文件格式','SQLite':'嵌入式數據庫','SHA256':'安全雜湊演算法256位元','CRC':'循環冗餘校驗','MMSI':'海上移動通信業務識別碼','IMO':'國際海事組織（欄位為其船舶識別編號）','UTC':'協調世界時','LAT':'緯度','LON':'經度','SOG':'對地航速','COG':'對地航向','Heading':'真航向','Draft':'吃水','AVIS':'權威船舶識別服務','AVID':'自動識別系統船舶識別資料庫','schema':'資料結構','declared type':'來源宣告型別','size':'來源宣告大小','domain':'有效值域','null':'空值','Level C':'丙類歷史資料分享分類','Total':'合計','GB':'十億位元組','InPort':'海洋暨大氣總署元資料入口','Transit Counts':'通行次數彙總','SDG':'永續發展目標','Untitled':'未命名文件（依使用者要求不恢復）','Master Agreement':'主協議','public item':'公開項目','credits':'服務點數','hosted':'託管','item':'項目','Feature Service':'地理要素服務','sentinel':'缺值或保留標記','true':'真／是','false':'假／否'}
鍵={'sample_complete_rows':'樣本完整資料行','compressed_prefix_bytes':'壓縮前綴位元組','decompressed_prefix_bytes':'解壓前綴位元組','discarded_incomplete_tail_bytes':'排除的不完整尾端位元組','deflate_stream_complete':'壓縮流是否完整','zip_crc_verified':'完整壓縮封裝校驗是否通過','full_files_verified':'完整檔案驗證數','checks':'檢查項數','use_reviews':'用途核對項數','global_complete':'全球是否完成','automatic_repairs':'自動修正數','dictionary_pages':'字典頁數','dictionary_updated':'字典更新日期','versioned_field_rows':'年代化欄位行數','field_mappings':'欄位映射數','previous_2019_header_exact_match':'2019年原表頭是否完全匹配','faq_pages':'常見問題頁數','summary_pages':'摘要頁數','annual_summary_rows':'年度摘要行數','quality_and_use_rules':'品質與用途規則數','source_receipts':'來源收據數','http_errors':'超文本傳輸協議錯誤數','public_layer_api_error':'公開圖層介面錯誤碼','full_data_rows_validated':'全量已驗證資料行數','automatic_corrections_applied':'已套用自動修正數','sqlite_counts':'嵌入式數據庫各表行數','starshield_visible_page_observed':'是否觀測星盾可見頁面','esri_faq_pages':'環境系統研究所公司常見問題頁數','esri_faq_source_date':'環境系統研究所公司常見問題來源日期','noaa_2019_objects':'海洋暨大氣總署2019年檔案物件數','partial_csv_columns':'部分數據表欄數','fetch_errors':'取得錯誤數','token_restrictions_retained':'保留的身份憑證限制數','full_ais_files_downloaded':'已完整下載自動識別系統檔案數'}
鍵.update({'preserved_preserved_registry_commercial_products': '保留的商業產品登記表', 'preserved_preserved_registry_preserved_498_asf_work': '保留的498項阿拉斯加衛星設施工作表', 'preserved_preserved_registry_product_workqueue': '保留的產品工作佇列表', 'preserved_registry_esri_catalog': '保留的環境系統研究所公司項目目錄', 'preserved_registry_esri_item_terms': '保留的環境系統研究所公司逐項條款', 'preserved_registry_esri_service_schema': '保留的環境系統研究所公司服務結構', 'registry_esri_obligations': '環境系統研究所公司使用義務登記表', 'registry_gap_resolution': '取用缺口核解登記表', 'registry_noaa_2019_csv_header': '海洋暨大氣總署2019年數據表表頭登記', 'registry_noaa_2019_daily_objects': '海洋暨大氣總署2019年逐日檔案登記', 'registry_source_receipts': '來源收據登記表', 'preserved_registry_gap_resolution': '保留的取用缺口核解登記表', 'preserved_registry_noaa_2019_csv_header': '保留的海洋暨大氣總署2019年數據表表頭', 'preserved_registry_noaa_2019_daily_objects': '保留的海洋暨大氣總署2019年逐日檔案', 'registry_official_annual_summary': '官方年度摘要登記表', 'registry_public_layer_access': '公開圖層取用登記表', 'registry_quality_and_use_rules': '品質及用途規則登記表', 'registry_schema_migration_comparison': '結構遷移對照登記表', 'registry_versioned_field_dictionary': '年代化欄位字典登記表'})
術語=[{'原名或原鍵':k,'中文對照':v,'範圍':'報告呈現層中譯；來源名稱與機器鍵不覆寫'} for k,v in {**詞,**鍵}.items()]
寫表('報告外語與統計鍵中文對照.csv',術語)
映射=[];連結=[]
for 舊,新,中文 in 對照:
    p=根/'Reference'/(舊+'.qmd');b=p.read_bytes();s=b.decode('utf-8');新路=根/'Reference'/(新+'.qmd')
    附='\n\n## 中文檔名與外語雙顯對照\n\n本中文檔名版本保留來源報告全文位元組作為前綴，另附中文說明；沒有刪減來源資訊或修改歷史數據。原檔名：'+舊+'（'+中文+'）；中文檔名：'+新+'。三個版本的來源、年代與驗收限制仍按原文保留。\n\n| 原名或原鍵 | 中文對照 |\n|---|---|\n'+''.join('| '+r['原名或原鍵']+' | '+r['中文對照']+' |\n' for r in 術語)+'\n\n原文中的機器鍵、原網址及產品標識保留，上表提供中文解釋。產品譯稱不冒充已核官方中文商標；原統計代碼中的批次與日期屬標識。完整檔案品質、根因、用途授權與全球覆蓋仍按接續清單核實。\n'
    新路.write_bytes(b+附.encode('utf-8'))
    映射.append({'原檔路徑':p.relative_to(根).as_posix(),'中文源文件':新路.relative_to(根).as_posix(),'中文成品':新路.with_suffix('.html').relative_to(根).as_posix(),'中文名稱':中文,'原文字節數':len(b),'原文雜湊':雜湊(b),'中文附錄雜湊':雜湊(附.encode('utf-8')),'遷移模式':'保留原名兼新增中文全文版本，舊引用不改寫'})
    for target in re.findall(r'\]\(([^)]+)\)',s):
        if urllib.parse.urlparse(target).scheme or target.startswith('#'):continue
        path=urllib.parse.unquote(target.split('#')[0]);resolved=(新路.parent/path).resolve();assert resolved.is_relative_to(根.resolve()),'引用超出項目'
        連結.append({'中文源文件':新路.relative_to(根).as_posix(),'原相對連結':target,'解析路徑':resolved.relative_to(根).as_posix(),'是否存在':resolved.is_file(),'引用來源':'保留原文中相對連結'})
assert 連結 and all(r['是否存在'] for r in 連結),'本批中文版本有缺失引用'
寫表('中文檔名與原文保留映射.csv',映射);寫表('相對連結實測.csv',連結)
歷史舊={r['提交雜湊']:r for r in 讀表(根/'Reference/tables/79_歷史提交全量中譯_B56_20261011/全部歷史提交完整中文對照.csv')}
歷史=[]
for line in subprocess.check_output(['git','log','--all','--format=%H%x09%aI%x09%s'],cwd=根).decode().splitlines():
    h,date,s=line.split('\t',2)
    if h in 歷史舊:
        r=歷史舊[h];assert (date,s)==(r['提交時間'],r['原提交訊息']);中=r['完整中文對照']
    elif s=='Update Inteligent_egaming_platform_ref_v000.000.001.qmd':中='更新智能電子博彩平臺參考源文件，版本000.000.001'
    else:assert not re.search('[A-Za-z]',s),'新提交需補中譯';中=s
    歷史.append({'提交雜湊':h,'提交時間':date,'原提交訊息':s,'完整中文對照':中,'是否改寫歷史':'否'})
寫表('現行全部歷史提交中文對照.csv',歷史)
統計={'中文全文源文件':len(映射),'中文網頁預期數':len(映射),'原文前綴完整保留':True,'相對連結已核數':len(連結),'缺失連結':0,'外語及統計鍵對照':len(術語),'基線歷史提交':len(歷史),'較前輪新增提交':len(歷史)-len(歷史舊),'全項目檔名遷移完成':False,'全球核實完成':False}
(工作/'核查結果.json').write_text(json.dumps(統計,ensure_ascii=False,indent=2),encoding='utf-8')
報告='''---
title: "中文報告入口與引用核查：第五十七批"
date: 2026-10-11
lang: zh-TW
format:
  html:
    toc: true
    embed-resources: true
---

## 保留最新使用者修改

本輪先核Git（分散式版本控制）現況，發現前輪後三次智能電子博彩平臺參考文件提交，合計新增1106行、刪除12行。依現行內容建立新批次基線，未覆寫這些修改。歷史提交中譯索引同步納入新提交，保留原文與雜湊。

## 中文全文版本及雙顯

''' + ''.join('- '+['星盾頁面與地理資訊授權核對','自動識別系統年代化欄位核對','歷史自動識別系統樣本品質核對'][i]+'：[中文源文件]('+新+'.qmd)、[中文網頁]('+新+'.html)。\n' for i,(_,新,_) in enumerate(對照))+'''

每份中文源文件均完整保留原報告位元組前綴，再附外語專名、欄位與統計鍵的中譯；沒有抽掉來源資訊，也沒有將來源宣告換成實測。保留原名兼增中文全文版本，舊引用保持有效，中文版本使用原相對資料表路徑。這完成本批三份報告的中文入口，並非全部舊檔名遷移完成。

## 驗收範圍

'''+''.join('- '+k+'：'+('是' if v is True else '否' if v is False else str(v))+'。\n' for k,v in 統計.items())+'''

[中文檔名與原文保留映射](tables/80_中文報告入口與引用核查_B57_20261011/中文檔名與原文保留映射.csv)、[相對連結實測](tables/80_中文報告入口與引用核查_B57_20261011/相對連結實測.csv)、[外語及統計鍵對照](tables/80_中文報告入口與引用核查_B57_20261011/報告外語與統計鍵中文對照.csv)、[最新歷史提交中文對照](tables/80_中文報告入口與引用核查_B57_20261011/現行全部歷史提交中文對照.csv)。

## 尚需施工

其餘報告與數據表的中文名稱、程式依賴及引用需按組逐項遷移。完整歷史資料的壓縮校驗、缺值根因、全量品質、逐用途許可與全球地域覆蓋尚未核完。主宇航比較報告與生態登記報告並存，既有數據與待辦不刪減；中譯及入口驗收不能代替科學與權利核實。
'''
(根/'Reference/中文報告入口與引用核查_B57_20261011.qmd').write_text(報告,encoding='utf-8')
附加='\n\n<!-- 中文報告入口與引用核查_B57_20261011_開始 -->\n## 2026-10-11 中文報告入口與引用核查：第五十七批\n\n新增[中文全文報告與引用核查](中文報告入口與引用核查_B57_20261011.qmd)，第五十二至五十四批三份報告新增中文檔名全文版本與外語對照，原文前綴及相對資料表引用完整保留。前輪後使用者三次提交保留，現行歷史提交中譯同步補齊。\n<!-- 中文報告入口與引用核查_B57_20261011_結束 -->\n'
(根/主).write_bytes(原文+附加.encode('utf-8'));(工作/'附加收據.json').write_text(json.dumps({'附加雜湊':雜湊(附加.encode('utf-8'))},ensure_ascii=False),encoding='utf-8')
for 目錄,名 in [('redteam','對抗審核'),('critic','批判核對'),('killcritic','批判再審'),('blindspot','盲點核查'),('blueprint','施工藍圖'),('cheatsheet','速查要點'),('actionplan','行動清單')]:
    (根/目錄/'中文報告入口與引用核查_B57_20261011.md').write_text('# '+名+'｜第五十七批\n\n三份中文全文版本保留原文前綴，原相對資料表逐項核存在；舊名與使用者新提交不覆寫。中譯及引用存在不等於全量資料品質或用途許可通過。接續其他報告依賴與來源核查。\n\n[中文報告](../Reference/中文報告入口與引用核查_B57_20261011.qmd)。\n',encoding='utf-8')
print(json.dumps(統計,ensure_ascii=False))
