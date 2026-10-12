from pathlib import Path
from collections import defaultdict,Counter
import csv,json
工作=Path(__file__).resolve().parent;根=工作.parents[2]
表=根/'Reference/tables/94_全項目進度審計_B72_20261012'
with (根/'Reference/tables/93_全球貨幣與市場代碼全量續核_B71_20261012/未關聯貨幣來源記錄.csv').open(encoding='utf-8-sig',newline='') as f:原=list(csv.DictReader(f))
組=defaultdict(list)
for r in 原:組[r['來源實體名稱原值']].append(r)
中={'ARAB MONETARY FUND':'阿拉伯貨幣基金','BOLIVIA':'玻利維亞','BURMA':'緬甸（歷史英文名稱）','CZECHOSLOVAKIA':'捷克斯洛伐克','EUROPEAN MONETARY CO-OPERATION FUND (EMCF)':'歐洲貨幣合作基金','EUROPEAN UNION':'歐洲聯盟','GERMAN DEMOCRATIC REPUBLIC':'德意志民主共和國','INTERNATIONAL MONETARY FUND (IMF)':'國際貨幣基金組織','LAO':'寮國','MEMBER COUNTRIES OF THE AFRICAN DEVELOPMENT BANK GROUP':'非洲開發銀行集團成員國','NETHERLANDS ANTILLES':'荷屬安的列斯','SAINT MARTIN':'聖馬丁（具體屬地關聯待核）','SERBIA AND MONTENEGRO':'塞爾維亞與蒙特內哥羅','SISTEMA UNITARIO DE COMPENSACION REGIONAL DE PAGOS "SUCRE"':'蘇克雷區域支付補償體系','SOUTHERN RHODESIA':'南羅德西亞','SWAZILAND':'史瓦濟蘭（歷史英文名稱）','TURKEY':'土耳其','UNION OF SOVIET SOCIALIST REPUBLICS':'蘇維埃社會主義共和國聯盟','VENEZUELA':'委內瑞拉','YEMEN, DEMOCRATIC':'民主葉門','YUGOSLAVIA':'南斯拉夫','ZAIRE':'薩伊（歷史英文名稱）','ZZ01_Bond Markets Unit European_EURCO':'歐洲債券市場計價單位EURCO','ZZ01_Gold-Franc':'金法郎','ZZ02_Bond Markets Unit European_EMU-6':'歐洲債券市場計價單位EMU-6','ZZ02_RINET Funds Code':'RINET（原識別名）基金代碼','ZZ03_Bond Markets Unit European_EUA-9':'歐洲債券市場計價單位EUA-9','ZZ04_Bond Markets Unit European_EUA-17':'歐洲債券市場計價單位EUA-17','ZZ05_UIC-Franc':'國際鐵路聯盟計價法郎','ZZ06_Testing_Code':'測試代碼','ZZ07_No_Currency':'無貨幣','ZZ08_Gold':'黃金','ZZ09_Palladium':'鈀','ZZ10_Platinum':'鉑','ZZ11_Silver':'白銀'}
行=[]
for name,rs in sorted(組.items()):
    clean=name.strip();assert clean in 中
    if clean.startswith('ZZ'):kind='ZZ前綴專用實體名稱；不是缺失國家數'
    elif any(s in clean for s in ['FUND','BANK GROUP','SISTEMA','EUROPEAN UNION']):kind='跨國機構或計价體系候選；角色仍待核'
    elif all(r['狀態中譯']=='歷史' for r in rs):kind='只見於本次歷史來源表；政治類型另核'
    else:kind='名稱與國別關聯待核'
    行.append({'來源實體名稱原值':name,'中文編輯參考':中[clean],'中譯證據':'編輯中譯；不是法定名稱或官方國別對照認證','来源行數':len(rs),'現行來源行':sum(r['狀態中譯']=='現行' for r in rs),'歷史來源行':sum(r['狀態中譯']=='歷史' for r in rs),'分流類別':kind,'記錄識別碼JSON':json.dumps([r['記錄識別碼'] for r in rs],ensure_ascii=False),'代碼與撤回日期JSON':json.dumps([{'字母代碼':r['字母代碼'],'撤回日期原值':r['撤回日期原值']} for r in rs],ensure_ascii=False),'國別關聯已提升':False,'接續驗收條件':'須以適用版本的官方證據確認實體類型及國別／歷史實體關聯；不強行塞入現行母表'})
assert sum(r['来源行數'] for r in 行)==len(原)==42 and len(行)==35
with (表/'未關聯貨幣來源全量分流.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(行[0]));w.writeheader();w.writerows(行)
(工作/'分流驗收.json').write_text(json.dumps({'原始來源行':len(原),'來源名稱數':len(行),'全量保留與對賬':True,'已增加中文編輯參考':35,'分流類別分布':dict(Counter(r['分流類別'] for r in 行)),'國別關聯已提升':False},ensure_ascii=False,indent=2),encoding='utf-8')
print('42條來源記錄、35個名稱已全量分流，不提升未知國別證據。')
