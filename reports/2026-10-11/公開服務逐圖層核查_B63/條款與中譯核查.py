from pathlib import Path
import json,csv,re,hashlib
from urllib.request import Request,urlopen
from datetime import datetime,timezone
工作=Path(__file__).resolve().parent;根=工作.parents[2];原=工作/'原始來源';表=根/'Reference/tables/86_公開服務逐圖層核查_B63_20261011'
assert not (工作/'條款取得收據.json').exists()
網站=(原/'海洋地籍免责声明.response').read_text(encoding='utf-8');id=re.search(r'https://www.arcgis.com/sharing/rest/content/items/([0-9a-f]{32})/resources/',網站)[1]
收=[]
for 名,尾 in [('免責頁官方項目元資料','?f=pjson'),('免責頁官方項目內容','/data?f=pjson')]:
    url='https://www.arcgis.com/sharing/rest/content/items/'+id+尾
    with urlopen(Request(url,headers={'User-Agent':'Public-source-license-audit/1.0'}),timeout=30) as r:b=r.read(4*1024*1024+1);碼=r.status
    assert len(b)<=4*1024*1024;f=原/(名+'.response');assert not f.exists();f.write_bytes(b)
    j=json.loads(b);收.append({'中文名稱':名,'網址':url,'狀態碼':碼,'來源雜湊':hashlib.sha256(b).hexdigest(),'原始檔':f.relative_to(根).as_posix(),'取得時間':datetime.now(timezone.utc).isoformat(),'錯誤':j.get('error'),'識別碼來源':'免責頁官方回應中的社群圖片項目路徑；需元資料標題覆核'})
    print(名, j.get('title'),str(j)[:250])
(工作/'條款取得收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8')
替=[('AIS Vessel Transit Counts','自動識別系統船舶通行次數'),('Significant Wave Height','有效波高'),('Wave Climate','波浪氣候'),('Wave Height','波高'),('Gulf of Maine','緬因灣'),('North Atlantic','北大西洋'),('Eastern Pacific','東太平洋'),('Western Pacific','西太平洋'),('Atlantic','大西洋'),('Pacific','太平洋'),('Alaska','阿拉斯加'),('Hawaii','夏威夷'),('Coastal Wetlands','沿岸濕地'),('Benthic Habitat','底栖棲息地'),('No Data Mask','無資料遮罩'),('Geoform','地貌'),('Hillshade','地形陰影'),('Area','區域'),('IOOS','綜合海洋觀測系統'),('Region Boundary Names','區域邊界名稱'),('Region Boundaries','區域邊界'),('Region Boundary Name','區域邊界名稱'),('Region Names','區域名稱'),('Region Name','區域名稱'),('Regions','區域'),('Seagrasses','海草'),('Storm Segments','風暴分段'),('Tropical Cyclone AOI','熱帶氣旋關注區域'),('34-knot Occurrence','34節風速發生次數'),('US State Submerged Lands','美國州級水下土地'),('sqkm','平方公里')]
def 讀(n):
    with (表/n).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def 寫(n,rows):
    with (表/n).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
圖=讀('逐圖層結構與授權狀態.csv');雙=[]
for r in 圖:
    中文=r['原圖層名']
    for a,b in 替:中文=中文.replace(a,b)
    assert not re.search('[A-Za-z]',中文),中文
    雙.append({'原圖層名':r['原圖層名'],'中文圖層名':中文,'中文服務名':r['中文服務名'],'圖層識別碼':r['圖層識別碼']})
寫('圖層名稱中外雙顯.csv',雙)
映=dict(zip('OBJECTID pointId waveDirection waveAbsolutePeriod significantWaveHeight wavePeakPeriod maximumEnergyDirection spatial hexagonIdentifier Shape aquaticSetting NWIClass NWIWaterRegime salinityRegime biotic substrate geometry geoform_category_one FeatureID ZOrder AnnotationClassID Element SymbolID Status TextString FontName FontStyle FontSize Underline VerticalAlignment HorizontalAlignment XOffset YOffset Angle FontLeading WordSpacing CharacterWidth CharacterSpacing FlipAngle Override SHAPE shortName region associationName nation stateUSPS bioticClass bioticSubclass bioticGroup bioticCommunity CMECS cover sourceRecord sourceDate acres stormName stormSegmentYear stormSegmentMonth stormSegmentDay stormSegmentHour stormSegmentCategory stormSegmentMaxWind stormSerialNumber stormSegmentCount federalGeoregulation citation codification authority contact website'.split(),'物件識別碼 點識別碼 波向 波浪絕對週期 有效波高 波峰週期 最大能量方向 空間幾何 六邊形識別碼 幾何形狀 水域環境 國家濕地清單分類 國家濕地清單水文制度 鹽度制度 生物 底質 幾何 地貌第一分類 要素識別碼 疊放次序 註記分類識別碼 元素 符號識別碼 狀態 文字字串 字型名稱 字型樣式 字型大小 底線 垂直對齊 水平對齊 水平偏移 垂直偏移 角度 字型行距 單字間距 字元寬度 字元間距 翻轉角度 覆寫 幾何形狀 簡稱 區域 協會名稱 國別 美國郵政州代碼 生物類 生物亞類 生物群 生物群落 海岸海洋生態分類標準 覆蓋 來源記錄 來源日期 英畝 風暴名稱 風暴分段年份 風暴分段月份 風暴分段日期 風暴分段小時 風暴分段類別 風暴分段最大風速 風暴序號 風暴分段數 聯邦地理規範 引用 編纂 授權機構 聯繫 網站'.split()))
for i in range(1,8):映['species'+str(i)]='物種'+str(i)
for 原前,中前 in [('occurrence','發生次數'),('returnInterval','重現間隔')]:
    for n in [34,50,64]:映[原前+str(n)+'kt']=str(n)+'節風速'+中前
for n in ['spatial','Shape','SHAPE']:
    映[n+'.STArea()']='幾何面積函數';映[n+'.STLength()']='幾何長度函數'
欄=讀('逐欄結構與域.csv');names=sorted({r['原欄名'] for r in 欄});assert all(n in 映 for n in names),[n for n in names if n not in 映]
寫('欄名中外雙顯.csv',[{'原欄名':n,'中文欄名':映[n],'翻譯層級':'欄名語義中譯；不替代來源單位或域定義'} for n in names])
print('全部圖層中譯',len(雙),'唯一欄名中譯',len(names))
