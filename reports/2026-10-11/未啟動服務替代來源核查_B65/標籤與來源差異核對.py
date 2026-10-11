from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone
import json,csv,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/88_未啟動服務替代來源核查_B65_20261011';原=工作/'原始來源'
assert not (工作/'標準來源收據.json').exists()
收=[]
for 名,url in [('開放地理空間聯盟地理標籤影像標準','https://docs.ogc.org/is/19-008r4/19-008r4.html'),('美國國會圖書館標籤影像標籤索引','https://www.loc.gov/preservation/digital/formats/content/tiff_tags.shtml')]:
    with urlopen(Request(url,headers={'User-Agent':'Raster-metadata-validation/1.0'}),timeout=30) as r:b=r.read(4*1024*1024+1);碼=r.status
    assert len(b)<=4*1024*1024;f=原/(名+'.response');assert not f.exists();f.write_bytes(b)
    收.append({'中文來源':名,'網址':url,'狀態碼':碼,'原始檔':f.relative_to(根).as_posix(),'來源雜湊':hashlib.sha256(b).hexdigest(),'取得時間':datetime.now(timezone.utc).isoformat()})
(工作/'標準來源收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8')
with (表/'官方替代來源與栅格結構.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
結果=[]
for r in rows:
    年=r['觀測年份'];t=json.loads(r['第一影像目錄標籤JSON']);g=t['地理鍵目錄原值'];assert len(g)==4+4*g[3];keys={g[i]:g[i+1:i+4] for i in range(4,len(g),4)}
    assert keys[1024]==[0,1,1] and keys[1025]==[0,1,1] and keys[2048]==[0,1,4326] and keys[3072]==[0,1,32767] and keys[3076]==[0,1,9001]
    html=(原/(年+'年通行次數元資料.response')).read_text(encoding='utf-8');assert '4269' in html and 'NAD83' in html
    結果.append({'觀測年份':年,'像元列數':t['像元列數'],'像元行數':t['像元行數'],'宣告像元總數':t['像元列數']*t['像元行數'],'像元比例原值':json.dumps(t['像元比例原值']),'像元比例單位中譯':'投影坐標單位米；不代表各緯度地面等面積','栅格單元型態中譯':'像元代表面積','樣本中譯':'32位元無符號整數，單樣本','無資料值原文':t['無資料值原文'],'無資料值判定中譯':'0為無資料標籤；不能直接推定零交通或沒有接收','產品地理參考中譯':'世界大地坐標系1984及球面網頁墨卡托投影文字，投影鍵為使用者自訂','原投影地理鍵':32767,'原地理基準鍵':4326,'目錄元資料參考中譯':'北美大地基準1983，原代碼4269','差異狀態':'已核來源與產品標籤不同；轉換與比較前須分清產品版本','像元全量已讀':'否；僅第一影像目錄','全球覆蓋推定':'禁止由矩形尺寸或檔案存在外推'})
with (表/'投影無資料值與來源差異.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(結果[0]));w.writeheader();w.writerows(結果)
print('三產品投影與無資料值原標籤已核；未讀取像元。')
