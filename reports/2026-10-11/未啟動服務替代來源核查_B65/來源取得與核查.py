from pathlib import Path
from urllib.request import urlopen,Request
from urllib.error import HTTPError
from datetime import datetime,timezone
import json,csv,hashlib,re,subprocess
from 栅格標籤解析 import 解析
工作=Path(__file__).resolve().parent;根=工作.parents[2];原=工作/'原始來源';原.mkdir(exist_ok=True);表=根/'Reference/tables/88_未啟動服務替代來源核查_B65_20261011';表.mkdir(parents=True,exist_ok=True)
H=lambda b:hashlib.sha256(b).hexdigest();assert not (工作/'基線.json').exists()
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd';b=(根/主).read_bytes();paths=subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0')
(工作/'基線.json').write_text(json.dumps({'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'主報告':主,'原文位元組':len(b),'原文雜湊':H(b),'原有文件':{p:H((根/p).read_bytes()) for p in paths if p.endswith(('.md','.qmd')) and (根/p).is_file()}},ensure_ascii=False,indent=2),encoding='utf-8')
收=[];產品=[]
for 年,id in [(2020,64828),(2021,67463),(2022,69555)]:
    meta='https://www.fisheries.noaa.gov/inport/item/'+str(id)
    with urlopen(Request(meta,headers={'User-Agent':'Official-product-alternative-audit/1.0'}),timeout=30) as r:b=r.read(2*1024*1024+1);碼=r.status
    assert len(b)<=2*1024*1024;f=原/(str(年)+'年通行次數元資料.response');f.write_bytes(b);html=b.decode('utf-8')
    url='https://ocmgeodatastor1.blob.core.windows.net/marinecadastre/ais/aistransit/ais-transit-count-'+str(年)+'.tif';assert url in html
    收.append({'中文來源':str(年)+'年官方產品元資料','網址':meta,'狀態碼':碼,'原始檔':f.relative_to(根).as_posix(),'來源雜湊':H(b),'取得時間':datetime.now(timezone.utc).isoformat(),'取得層級':'元資料'})
    with urlopen(Request(url,method='HEAD'),timeout=30) as r:長=int(r.headers['Content-Length']);etag=r.headers.get('ETag');modified=r.headers.get('Last-Modified');headstatus=r.status
    請求=0;累積=0;cache={}
    def 讀(offset,size):
        global 請求,累積
        assert 0<=offset and 0<size<=65536 and offset+size<=長
        for (lo,hi),v in cache.items():
            if lo<=offset and offset+size<=hi:return v[offset-lo:offset-lo+size]
        assert 請求<100 and 累積+size<=2*1024*1024
        with urlopen(Request(url,headers={'Range':f'bytes={offset}-{offset+size-1}','If-Match':etag}),timeout=30) as r:
            b=r.read(size+1);cr=r.headers.get('Content-Range','');assert r.status==206 and cr==f'bytes {offset}-{offset+size-1}/{長}' and len(b)==size and r.headers.get('ETag')==etag
        請求+=1;累積+=len(b);f=原/(str(年)+'年栅格範圍_'+str(offset)+'_'+str(size)+'.bin');assert not f.exists();f.write_bytes(b);cache[(offset,offset+size)]=b
        收.append({'中文來源':str(年)+'年栅格元資料範圍','網址':url,'狀態碼':206,'原始檔':f.relative_to(根).as_posix(),'來源雜湊':H(b),'取得時間':datetime.now(timezone.utc).isoformat(),'請求起點':offset,'實得位元組':len(b),'完整來源位元組':長,'範圍回應原文':cr,'來源版本標籤':etag,'取得層級':'指定範圍元資料；不是完整產品'})
        return b
    try:tags=解析(讀);錯=''
    except Exception as e:tags={};錯=type(e).__name__+':'+str(e)
    產品.append({'觀測年份':年,'元資料識別碼':id,'元資料網址':meta,'原服務中譯':'船舶通行次數'+str(年),'官方替代網址':url,'頭請求狀態':headstatus,'完整檔宣告位元組':長,'來源修改時間原值':modified,'來源版本標籤':etag,'限定範圍取得位元組':累積,'限定範圍請求數':請求,'栅格標籤解析通過':bool(tags),'第一影像目錄標籤JSON':json.dumps(tags,ensure_ascii=False),'解析缺口':錯,'元資料觀測期間':f'{年}-01-01至{年}-12-31','產品特定用途中譯':'海岸及海洋規劃；不推定所有用途','来源精度狀態中譯':'來源標明精度未測試；精度設計敘述不等於獨立實測','地域中譯':'美國本土、夏威夷、美屬維爾京群島及波多黎各，依來源完整性文字；非全球','同年替代來源已核':True,'逐像元完整品質已核':False,'原服務已恢復':False})
    print(str(年)+'年：替代檔存在，元資料範圍'+str(累積)+'位元組；解析'+str(bool(tags)),flush=True)
with (表/'官方替代來源與栅格結構.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(產品[0]));w.writeheader();w.writerows(產品)
(工作/'來源收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8');(工作/'核查結果.json').write_text(json.dumps({'原服務數':3,'同年官方替代來源數':len(產品),'標籤解析通過數':sum(r['栅格標籤解析通過'] for r in 產品),'原始來源回應數':len(收),'範圍實得總位元組':sum(r['限定範圍取得位元組'] for r in 產品),'完整產品已取得':False,'原服務恢復已核':False,'逐像元品質已核':False,'全球覆蓋已核':False},ensure_ascii=False,indent=2),encoding='utf-8')
