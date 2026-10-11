from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from datetime import datetime, timezone, date, timedelta
from html.parser import HTMLParser
from urllib.parse import urljoin
import json, hashlib, csv, re
工作=Path(__file__).resolve().parent;根=工作.parents[2];原=工作/'原始來源';原.mkdir(exist_ok=True)
表=根/'Reference/tables/85_最新官方資料時效核查_B62_20261011';表.mkdir(parents=True,exist_ok=True)
assert not (工作/'來源收據.json').exists(),'不得覆寫既有來源證據'
來源=[('2025年逐日位置目錄','https://noaaocm.blob.core.windows.net/ais/csv2/csv2025/index.html'),('2026年逐日位置目錄探測','https://noaaocm.blob.core.windows.net/ais/csv2/csv2026/index.html'),('2026年航跡元資料','https://www.fisheries.noaa.gov/inport/item/80415'),('2025年位置元資料','https://www.fisheries.noaa.gov/inport/item/77594/full-list'),('航跡現行目錄','https://ocmgeodatastor1.blob.core.windows.net/marinecadastre/ais/aistrack/index-aistrack.html'),('航跡舊路徑目錄','https://ocmgeodatastor1.blob.core.windows.net/marinecadastre/aistrack/index-aistrack.html'),('通行密度目錄','https://ocmgeodatastor1.blob.core.windows.net/marinecadastre/ais/aistransit/index-aistransit.html'),('地理資訊服務目錄','https://coast.noaa.gov/arcgismc/rest/services/marinecadastre?f=pjson'),('關島區域目錄','https://ocmgeodatastor1.blob.core.windows.net/marinecadastre/data/ais/guam/index-guam.html')]
class 解析(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.text=[]
    def handle_starttag(self,t,a):
        if t=='a':
            h=dict(a).get('href')
            if h:self.links.append(h)
    def handle_data(self,d):self.text.append(d)
收=[];連=[]
for 名,url in 來源:
    try:
        with urlopen(Request(url,headers={'User-Agent':'Research-source-audit/1.0'}),timeout=45) as r:
            b=r.read(4*1024*1024+1);assert len(b)<=4*1024*1024;碼=r.status;終=r.url;標=dict(r.headers)
    except HTTPError as e:b=e.read(1024*1024);碼=e.code;終=e.url;標=dict(e.headers)
    except Exception as e:
        收.append({'名稱':名,'請求網址':url,'結果':'取得失敗','原因類別':type(e).__name__,'查證時間':datetime.now(timezone.utc).isoformat()});continue
    f=原/(名+'.response');f.write_bytes(b);p=解析();p.feed(b.decode('utf-8','replace'))
    收.append({'名稱':名,'請求網址':url,'最終網址':終,'狀態碼':碼,'位元組':len(b),'來源雜湊':hashlib.sha256(b).hexdigest(),'原始檔':f.relative_to(根).as_posix(),'查證時間':datetime.now(timezone.utc).isoformat(),'來源回應標頭':標,'取得層級':'目錄或元資料，未取得產品全量記錄'})
    if 碼==200:
        for h in p.links:
            if re.search(r'\.(?:zst|zip|parquet|gpkg|tif)(?:\?|$)',h,re.I):連.append({'來源名稱':名,'檔案連結':urljoin(終,h),'檔名觀測日期候選':','.join(re.findall(r'20\d{2}(?:[-_]\d{2}){0,2}',h)),'日期候選已核實語義':'否；需產品元資料交叉核對'})
    print(名+'：'+str(碼))
with (表/'產品目錄連結.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['來源名稱','檔案連結','檔名觀測日期候選','日期候選已核實語義']);w.writeheader();w.writerows(連)
日期=[re.search(r'ais-(2025-\d{2}-\d{2})\.csv\.zst',r['檔案連結'])[1] for r in 連 if r['來源名稱']=='2025年逐日位置目錄' and re.search(r'ais-(2025-\d{2}-\d{2})\.csv\.zst',r['檔案連結'])]
預期={(date(2025,1,1)+timedelta(days=i)).isoformat() for i in range(365)}
結果={'2025年逐日檔連結數':len(日期),'2025年唯一日期數':len(set(日期)),'2025年缺失日期':sorted(預期-set(日期)),'2025年範圍外日期':sorted(set(日期)-預期),'2025年重複日期連結':len(日期)-len(set(日期)),'產品目錄連結總數':len(連),'全量產品品質已核':False,'全球覆蓋已核':False}
(工作/'來源收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8');(工作/'核查結果.json').write_text(json.dumps(結果,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(結果,ensure_ascii=False))
