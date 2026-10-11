from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from datetime import datetime,timezone
import json,csv,hashlib,subprocess
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/86_公開服務逐圖層核查_B63_20261011';表.mkdir(parents=True,exist_ok=True)
原=工作/'原始來源';原.mkdir(exist_ok=True);H=lambda b:hashlib.sha256(b).hexdigest()
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd';b=(根/主).read_bytes();paths=subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0')
if (工作/'基線.json').exists():
    基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));assert H(b)==基['原文雜湊']
    assert all((根/p).is_file() and H((根/p).read_bytes())==h for p,h in 基['原有文件'].items()),'原有文件變更，停止續作'
else:(工作/'基線.json').write_text(json.dumps({'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'主報告':主,'原文位元組':len(b),'原文雜湊':H(b),'原有文件':{p:H((根/p).read_bytes()) for p in paths if p.endswith(('.md','.qmd')) and (根/p).is_file()}},ensure_ascii=False,indent=2),encoding='utf-8')
assert not (工作/'來源收據.json').exists(),'已完成取得，不得重做'
if any(原.glob('*.response')) and not (工作/'首次中斷證據.json').exists():
    (工作/'首次中斷證據.json').write_text(json.dumps({'中斷原因':'部分圖層fields為空值；修正空值處理後續作，原回應保留','原始回應':[{'原始檔':f.relative_to(根).as_posix(),'來源雜湊':H(f.read_bytes())} for f in 原.glob('*.response')]},ensure_ascii=False,indent=2),encoding='utf-8')
收=[];服務=[];圖=[];欄=[]
def 取得(名,url):
    try:
        with urlopen(Request(url,headers={'User-Agent':'Public-metadata-quality-audit/1.0'}),timeout=30) as r:內容=r.read(4*1024*1024+1);碼=r.status;終=r.url
        assert len(內容)<=4*1024*1024,'元資料超過本輪上限'
    except HTTPError as e:內容=e.read(1024*1024);碼=e.code;終=e.url
    except Exception as e:
        收.append({'中文名稱':名,'網址':url,'取得時間':datetime.now(timezone.utc).isoformat(),'結果':'失敗','錯誤類別':type(e).__name__});return {}
    f=原/(名+'.response');序=1
    while f.exists():f=原/(名+'_續作'+str(序)+'.response');序+=1
    f.write_bytes(內容)
    try:j=json.loads(內容)
    except ValueError:j={}
    收.append({'中文名稱':名,'網址':url,'最終網址':終,'狀態碼':碼,'取得時間':datetime.now(timezone.utc).isoformat(),'原始檔':f.relative_to(根).as_posix(),'來源雜湊':H(內容),'位元組':len(內容),'服務錯誤':j.get('error'),'核查層級':'公開元資料；未讀取要素或影像'})
    return j if 碼==200 and not j.get('error') else {}
with (根/'Reference/tables/85_最新官方資料時效核查_B62_20261011/公開地理資訊服務.csv').open(encoding='utf-8-sig',newline='') as f:清=list(csv.DictReader(f))
中譯={'AISVesselTransitCounts':'船舶通行次數','AlaskaSignificantWaveHeight':'阿拉斯加有效波高','AtlanticSignificantWaveHeight':'大西洋有效波高','CoastalWetlands':'沿岸濕地','gulf_of_maine_2021':'緬因灣2021年','HawaiiSignificantWaveHeight':'夏威夷有效波高','IOOSRegions':'綜合海洋觀測系統區域','PacificSignificantWaveHeight':'太平洋有效波高','Seagrasses':'海草','TropicalCycloneStormSegments':'熱帶氣旋風暴分段','TropicalCycloneWindExposure':'熱帶氣旋風暴暴露','USStateSubmergedLands':'美國州級水下土地'}
for i,r in enumerate(清):
    原名=r['原服務名'].split('/')[-1];中文=next((v+原名[len(k):] for k,v in 中譯.items() if 原名.startswith(k)),原名)
    url='https://coast.noaa.gov/arcgismc/rest/services/'+r['原服務名']+'/'+r['原服務類型'];j=取得(f'{i+1:02d}_{中文}_服務',url+'?f=pjson')
    列=j.get('layers',[])+j.get('tables',[]);assert len(列)<=200
    服務.append({'中文服務名':中文,'原服務名':r['原服務名'],'元資料可讀':bool(j),'服務說明原文':j.get('description',''),'服務版权原文':j.get('copyrightText',''),'能力原文':j.get('capabilities',''),'格式原文':j.get('supportedImageFormatTypes',''),'空間參考原值':json.dumps(j.get('spatialReference',{}),ensure_ascii=False),'完整範圍原值':json.dumps(j.get('fullExtent',{}),ensure_ascii=False),'列出圖層及表數':len(列),'用途授權結論':'未核定；版权文字及可讀性不是用途授權'})
    for x in 列:
        id=x['id'];d=取得(f'{i+1:02d}_{中文}_圖層_{id}',url+'/'+str(id)+'?f=pjson')
        圖.append({'中文服務名':中文,'原圖層名':x.get('name',''),'圖層識別碼':id,'元資料可讀':bool(d),'類型原值':d.get('type',''),'父圖層原值':json.dumps(d.get('parentLayer')),'子圖層原值':json.dumps(d.get('subLayers')),'幾何原值':d.get('geometryType',''),'欄位數':len(d.get('fields') or []),'栅格類型原值':d.get('dataType',''),'查詢能力原值':d.get('capabilities',''),'圖層版权原文':d.get('copyrightText',''),'圖層說明原文':d.get('description',''),'圖層範圍原值':json.dumps(d.get('extent',{}),ensure_ascii=False),'最小比例尺':d.get('minScale'),'最大比例尺':d.get('maxScale'),'元資料網址':url+'/'+str(id)+'?f=pjson','全量品質狀態':'未核；只讀元資料','逐用途授權狀態':'未核；未推定可商用'})
        for field in (d.get('fields') or []):欄.append({'中文服務名':中文,'圖層識別碼':id,'原欄名':field.get('name'),'原欄別名':field.get('alias'),'型態原值':field.get('type'),'長度':field.get('length'),'可空原值':field.get('nullable'),'域定義原值':json.dumps(field.get('domain'),ensure_ascii=False)})
    print(中文+'：'+str(len(列))+'項')
取得('海洋地籍來源授權文件','https://raw.githubusercontent.com/ocm-marinecadastre/ais-vessel-traffic/main/LICENSE.md')
取得('海洋地籍免责声明','https://marinecadastre.gov/about/disclaimer.html')
for 名,rows in [('服務用途與範圍.csv',服務),('逐圖層結構與授權狀態.csv',圖),('逐欄結構與域.csv',欄)]:
    with (表/名).open('w',encoding='utf-8-sig',newline='') as f:
        if rows:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
結果={'服務數':len(服務),'可讀服務數':sum(r['元資料可讀'] for r in 服務),'圖層及表數':len(圖),'可讀圖層及表數':sum(r['元資料可讀'] for r in 圖),'欄位登記數':len(欄),'來源回應數':len(收),'全量品質通過':False,'逐用途授權通過':False,'全球覆蓋通過':False,'未查詢逐要素資料':True}
(工作/'來源收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8');(工作/'核查結果.json').write_text(json.dumps(結果,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(結果,ensure_ascii=False))
