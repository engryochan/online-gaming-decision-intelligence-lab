from pathlib import Path
import urllib.request,tempfile,datetime,json,csv,zipfile,io,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/84_相鄰日期完整檔核查_B61_20261011'
assert not (工作/'取得收據.json').exists(),'禁止覆寫前次取得證據'
表.mkdir();暫存=Path(tempfile.mkdtemp(prefix='科研相鄰歷史檔_'));檔=暫存/'2019年1月2日自動識別系統.zip'
url='https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2019/AIS_2019_01_02.zip'
收={'官方網址':url,'中文來源':'2019年1月2日歷史自動識別系統完整檔','取得時間':datetime.datetime.now(datetime.timezone.utc).isoformat(),'本機原始檔':str(檔),'回應狀態':'','宣告位元組':0,'實得位元組':0,'來源雜湊':'','完整下載':False,'壓縮校驗通過':False,'原始資料推送':False,'錯誤':''}
def 保存():(工作/'取得收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8')
保存();h=hashlib.sha256();n=0
try:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PublicResearchRegistry/1.0','Accept-Encoding':'identity'}),timeout=45) as r,檔.open('wb') as f:
        收['回應狀態']=r.status;assert r.status==200,'未取得完整回應';收['宣告位元組']=int(r.headers.get('Content-Length','0'));保存()
        assert 0<收['宣告位元組']<=400*1024**2,'無完整檔長度或超出上限'
        while True:
            b=r.read(1024**2)
            if not b:break
            n+=len(b);assert n<=400*1024**2;f.write(b);h.update(b)
            if n%(64*1024**2)==0:print('相鄰完整檔下載：'+str(n)+'位元組',flush=True)
    assert n==收['宣告位元組'];收.update(實得位元組=n,來源雜湊=h.hexdigest(),完整下載=True);保存()
except Exception as e:收.update(實得位元組=n,錯誤=type(e).__name__+'：'+str(e));保存();raise
行數=0;錯={'欄位數不符':0,'時間無法解析':0,'不屬2019年1月2日':0};最早=None;最晚=None;日期={}
with zipfile.ZipFile(檔) as z:
    infos=z.infolist();assert len(infos)==1;收['成員原名']=infos[0].filename;收['成員中譯']='2019年1月2日自動識別系統數據表';收['成員宣告位元組']=infos[0].file_size;收['成員宣告循環冗餘校驗']=format(infos[0].CRC,'08x');保存()
    assert infos[0].file_size<2*1024**3
    with z.open(infos[0]) as raw,io.TextIOWrapper(raw,encoding='utf-8-sig',newline='') as f:
        reader=csv.reader(f);header=next(reader);assert header==['MMSI','BaseDateTime','LAT','LON','SOG','COG','Heading','VesselName','IMO','CallSign','VesselType','Status','Length','Width','Draft','Cargo','TransceiverClass']
        for row in reader:
            行數+=1
            if len(row)!=17:錯['欄位數不符']+=1;continue
            try:d=datetime.datetime.fromisoformat(row[1])
            except ValueError:錯['時間無法解析']+=1;continue
            day=d.date().isoformat();日期[day]=日期.get(day,0)+1;錯['不屬2019年1月2日']+=day!='2019-01-02';最早=d if 最早 is None else min(最早,d);最晚=d if 最晚 is None else max(最晚,d)
            if 行數%2000000==0:print('相鄰完整檔日期核查：'+str(行數)+'行',flush=True)
收.update(壓縮校驗通過=True,完整資料行=行數,最早時間=最早.isoformat(),最晚時間=最晚.isoformat());保存()
def 寫表(名,rs):
    with (表/名).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
寫表('相鄰完整檔日期核查.csv',[{'核查項':k,'不符資料行':v,'分母':行數} for k,v in 錯.items()])
寫表('相鄰完整檔日期分布.csv',[{'日期':k,'資料行':v} for k,v in sorted(日期.items())])
with (根/'Reference/tables/81_歷史完整檔品質核查_B58_20261011/完整單日品質核查.csv').open(encoding='utf-8-sig') as f:前=list(csv.DictReader(f))
原檢={r['核查項']:int(r['觀測數']) for r in 前 if r['核查項'] in ['欄位數不符','日期格式不符','日期不屬檔名日期']};assert len(原檢)==3
可證=all(v==0 for v in 錯.values()) and all(v==0 for v in 原檢.values())
統計={'相鄰完整資料行':行數,'前日完整資料行':7516408,'兩日合計資料行':行數+7516408,'相鄰完整下載位元組':n,'相鄰壓縮校驗通過':True,'精確跨日重複可判定':可證,'精確原時間鍵跨日重複行':0 if 可證 else '未判定','日期不符行':錯['不屬2019年1月2日'],'來源雜湊':收['來源雜湊'],'判定依據':'兩檔全部有效日期分別為2019年1月1日及2日，原精確時間不可能相同；只適用含原時間欄的鍵及完整向量，不是日界連續性驗證','全球完成':False,'跨日運動連續性已核':False,'全年完成':False}
(工作/'核查結果.json').write_text(json.dumps(統計,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(統計,ensure_ascii=False),flush=True)
