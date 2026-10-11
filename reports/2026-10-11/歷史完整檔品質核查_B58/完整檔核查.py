from pathlib import Path
import urllib.request,hashlib,json,csv,zipfile,io,tempfile,datetime,math,sqlite3,subprocess,time
工作=Path(__file__).resolve().parent;根=工作.parents[2]
表=根/'Reference/tables/81_歷史完整檔品質核查_B58_20261011'
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
雜湊=lambda b:hashlib.sha256(b).hexdigest()
assert not (工作/'基線.json').exists(),'禁止刷新基線'
表.mkdir();原文=(根/主).read_bytes()
路徑=[p for p in subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0') if p]
基={'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'原有文件':{p:雜湊((根/p).read_bytes()) for p in 路徑 if Path(p).suffix in ('.md','.qmd') and (根/p).is_file()},'主報告':主,'原文位元組':len(原文),'原文雜湊':雜湊(原文)}
(工作/'基線.json').write_text(json.dumps(基,ensure_ascii=False,indent=2),encoding='utf-8')
暫存=Path(tempfile.mkdtemp(prefix='科研歷史完整檔_'));檔=暫存/'2019年1月1日自動識別系統.zip'
url='https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2019/AIS_2019_01_01.zip'
收={'來源中文名稱':'海洋暨大氣總署2019年1月1日歷史自動識別系統完整檔','官方網址':url,'開始時間':datetime.datetime.now(datetime.timezone.utc).isoformat(),'本機原始資料':str(檔),'原始資料是否推送':False,'預期位元組':289597662,'取得位元組':0,'回應狀態':'','回應範圍':'','來源雜湊':'','完整下載':False,'完整壓縮校驗':False,'錯誤':''}
def 保存收據():
    (工作/'完整檔取得收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8')
保存收據();計數=0;h=hashlib.sha256()
try:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PublicResearchRegistry/1.0','Accept-Encoding':'identity','Cache-Control':'no-cache'}),timeout=45) as r,檔.open('wb') as f:
        收['回應狀態']=r.status;收['回應範圍']=r.headers.get('Content-Range','');保存收據()
        assert r.status==200 or (r.status==206 and 收['回應範圍']=='bytes 0-289597661/289597662'),'伺服器沒有回傳完整檔範圍'
        while True:
            b=r.read(1024*1024)
            if not b:break
            計數+=len(b);assert 計數<=350*1024*1024,'超出本批下載上限';f.write(b);h.update(b)
            if 計數%(32*1024*1024)==0:print('完整檔下載進度：'+str(計數)+'位元組',flush=True)
    收['取得位元組']=計數;收['來源雜湊']=h.hexdigest();assert 計數==收['預期位元組'],'全檔長度與前轮來源宣告不一致'
    with 檔.open('rb') as f:assert 雜湊(f.read(65536))=='8ffc7f5fb2ba829c4d6c7d5aee2ad06a707bf80462e2aea1387f1e52048bd159','與封存前綴不一致'
    收['完整下載']=True;保存收據()
except Exception as e:
    收['取得位元組']=計數;收['錯誤']=type(e).__name__+'：'+str(e);保存收據();raise
列=['MMSI','BaseDateTime','LAT','LON','SOG','COG','Heading','VesselName','IMO','CallSign','VesselType','Status','Length','Width','Draft','Cargo','TransceiverClass']
空={k:0 for k in 列};解析={k:0 for k in ['LAT','LON','SOG','COG','Heading','Length','Width','Draft']};標={'對地航速102.3':0,'對地航向360':0,'真航向511':0};異={'欄位數不符':0,'日期格式不符':0,'日期不屬檔名日期':0,'識別碼非九位數字':0,'吃水負值':0,'緯度超界':0,'經度超界':0};行數=0;來源資料位元組=0
with zipfile.ZipFile(檔) as z:
    成員=z.infolist();assert len(成員)==1 and 成員[0].filename.endswith('.csv'),'封裝成員與預期不符';info=成員[0];assert info.file_size<2*1024**3,'解壓長度超出本批上限'
    收['成員數']=len(成員);收['成員原名']=info.filename;收['成員中文名']='2019年1月1日自動識別系統數據表';收['成員宣告位元組']=info.file_size;收['成員宣告循環冗餘校驗']=format(info.CRC,'08x');保存收據()
    with z.open(info) as raw,io.TextIOWrapper(raw,encoding='utf-8-sig',newline='') as f:
        reader=csv.reader(f);header=next(reader);assert header==列,'2019年表頭不符'
        for row in reader:
            行數+=1
            if len(row)!=len(列):異['欄位數不符']+=1;continue
            r=dict(zip(列,row))
            for k in 列:空[k]+=r[k]==''
            vals={}
            for k in 解析:
                if r[k]=='':continue
                try:v=float(r[k]);assert math.isfinite(v);vals[k]=v
                except (ValueError,AssertionError):解析[k]+=1
            異['緯度超界']+= 'LAT' in vals and not -90<=vals['LAT']<=90
            異['經度超界']+= 'LON' in vals and not -180<=vals['LON']<=180
            異['吃水負值']+= 'Draft' in vals and vals['Draft']<0
            標['對地航速102.3']+=vals.get('SOG')==102.3;標['對地航向360']+=vals.get('COG')==360;標['真航向511']+=vals.get('Heading')==511
            異['識別碼非九位數字']+=not(len(r['MMSI'])==9 and r['MMSI'].isdigit())
            try:d=datetime.datetime.fromisoformat(r['BaseDateTime']);異['日期不屬檔名日期']+=d.date()!=datetime.date(2019,1,1)
            except ValueError:異['日期格式不符']+=1
            if 行數%1000000==0:print('完整檔串流核查進度：'+str(行數)+'行',flush=True)
    # ZipExtFile讀至末尾會核CRC；上方完整CSV迭代不可提前停止。
    收['完整壓縮校驗']=True;收['完整資料行']=行數;保存收據()
def 寫表(名,rows):
    with (表/名).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
詞={'MMSI':'海上移動通信業務識別碼','BaseDateTime':'基準日期時間','LAT':'緯度','LON':'經度','SOG':'對地航速','COG':'對地航向','Heading':'真航向','VesselName':'船舶名稱','IMO':'國際海事組織船舶編號','CallSign':'呼號','VesselType':'船舶型別','Status':'狀態','Length':'長度','Width':'寬度','Draft':'吃水','Cargo':'原始船型或貨物類別欄','TransceiverClass':'收發機類別'}
結果=[{'核查項':'空字串','原欄名':k,'中文欄名':詞[k],'觀測數':v,'分母':行數,'範圍':'單日完整檔，不代表全年或全球'} for k,v in 空.items()]
結果 += [{'核查項':'非空值不能解析為有限數值','原欄名':k,'中文欄名':詞[k],'觀測數':v,'分母':行數-空[k],'範圍':'單日完整檔，空值另計，不重複當解析錯誤'} for k,v in 解析.items()]
結果 += [{'核查項':k,'原欄名':'不適用','中文欄名':k,'觀測數':v,'分母':行數,'範圍':'單日完整檔，不推斷根因或修正原值'} for k,v in {**標,**異}.items()]
寫表('完整單日品質核查.csv',結果)
寫表('完整檔來源收據.csv',[收])
統計={'完整歷史檔':1,'完整資料行':行數,'完整下載位元組':計數,'完整壓縮校驗通過':True,'品質檢查項':len(結果),'全量重複率已驗證':False,'全年完成':False,'全球完成':False,'用途許可已新增':False,'原始資料已推送':False}
(工作/'核查結果.json').write_text(json.dumps(統計,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(統計,ensure_ascii=False),flush=True)
