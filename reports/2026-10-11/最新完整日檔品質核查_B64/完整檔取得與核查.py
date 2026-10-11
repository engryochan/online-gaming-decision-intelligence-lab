from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone
from collections import Counter
import json,csv,io,sys,tempfile,hashlib,subprocess,math,re
sys.path.insert(0,str(Path(tempfile.gettempdir())/'科研壓縮驗收依賴_B64'));import zstandard
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/87_最新完整日檔品質核查_B64_20261011';表.mkdir(parents=True,exist_ok=True)
H=lambda b:hashlib.sha256(b).hexdigest();主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd'
assert not (工作/'基線.json').exists(),'不得刷新基線'
原=(根/主).read_bytes();paths=subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0')
(工作/'基線.json').write_text(json.dumps({'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'主報告':主,'原文位元組':len(原),'原文雜湊':H(原),'原有文件':{p:H((根/p).read_bytes()) for p in paths if p.endswith(('.md','.qmd')) and (根/p).is_file()}},ensure_ascii=False,indent=2),encoding='utf-8')
url='https://noaaocm.blob.core.windows.net/ais/csv2/csv2026/ais-2026-06-30.csv.zst'
目錄=(根/'reports/2026-10-11/最新官方資料時效核查_B62/原始來源/2026年逐日位置目錄探測.response').read_bytes();assert b'ais-2026-06-30.csv.zst' in 目錄
p=Path(tempfile.mkdtemp(prefix='科研2026完整檔_'))/'2026年6月30日自動識別系統.csv.zst';h=hashlib.sha256();總=0
with urlopen(Request(url,headers={'User-Agent':'Historical-public-data-quality-audit/1.0'}),timeout=90) as r:
    宣=int(r.headers.get('Content-Length','0'));assert 0<宣<450*1024*1024
    with p.open('xb') as f:
        while True:
            b=r.read(4*1024*1024)
            if not b:break
            總+=len(b);assert 總<=450*1024*1024;f.write(b);h.update(b)
    assert 總==宣;碼=r.status
收={'官方網址':url,'取得時間':datetime.now(timezone.utc).isoformat(),'觀測日期候選':'2026-06-30','本機原始檔':str(p),'宣告位元組':宣,'實得位元組':總,'来源雜湊':h.hexdigest(),'完整下載':True,'狀態碼':碼,'原始資料推送':False,'解碼套件':'zstandard（Z標準壓縮格式解碼套件）0.25.0','目錄證據雜湊':H(目錄)}
(工作/'取得收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8');print('完整下載位元組',總,flush=True)
with (根/'Reference/tables/76_ais_semantics_b53_20261011/registry_versioned_field_dictionary.csv').open(encoding='utf-8-sig',newline='') as f:字典=[r for r in csv.DictReader(f) if r['schema_period']=='2025-PRESENT']
assert len(字典)==17
預期=[r['column_name'] for r in sorted(字典,key=lambda r:int(r['ordinal']))]
數域={'longitude':(-179.99999,179.99999),'latitude':(-89.99999,89.99999),'sog':(0,99.9),'cog':(0,359.9),'heading':(0,359),'vessel_type':(1,1024),'status':(1,14),'length':(1,509),'width':(1,61),'draft':(1,24),'cargo':(1,1024)}
統={n:Counter() for n in 預期};最小={};最大={};日期=Counter();小時=Counter();類=Counter();列數=0;異=Counter()
with p.open('rb') as f,zstandard.ZstdDecompressor().stream_reader(f) as zr,io.TextIOWrapper(zr,encoding='utf-8-sig',newline='') as text:
    reader=csv.reader(text);欄頭=next(reader);assert 欄頭==預期,('欄位版本不符',欄頭)
    for row in reader:
        列數+=1;assert 列數<25000000
        if len(row)!=len(欄頭):異['欄位數不符']+=1;continue
        r=dict(zip(欄頭,row))
        try:d=datetime.fromisoformat(r['base_date_time']);日期[d.date().isoformat()]+=1;小時[d.hour]+=1
        except ValueError:異['時間不可解析']+=1
        if not re.fullmatch(r'\d{9}',r['mmsi']):異['識別碼非九位數字']+=1
        類[r['transceiver']]+=1
        for n,v in r.items():
            s=統[n];s['資料行']+=1
            if v=='':s['空字串']+=1;continue
            s['非空']+=1
            if n in 數域:
                try:x=float(v)
                except ValueError:s['不可解析數值']+=1;continue
                if not math.isfinite(x):s['非有限數值']+=1;continue
                lo,hi=數域[n];s['字典值域外']+=not lo<=x<=hi
                最小[n]=min(最小.get(n,x),x);最大[n]=max(最大.get(n,x),x)
                if n in ['heading','vessel_type','status','length','width','cargo'] and x!=int(x):s['整數欄出現非整數']+=1
        if 列數%2000000==0:print('已核資料行',列數,flush=True)
# 第二遍檢查每個壓縮框架真正到達結尾，避免串流讀至末尾被誤當壓縮完整性通過。
框架=0;解壓位元組=0;dec=zstandard.ZstdDecompressor().decompressobj();完成=False
with p.open('rb') as f:
    while True:
        b=f.read(1024*1024)
        if not b:break
        if 完成:dec=zstandard.ZstdDecompressor().decompressobj();完成=False
        while b:
            out=dec.decompress(b);解壓位元組+=len(out);assert 解壓位元組<3*1024*1024*1024
            if dec.eof:
                框架+=1;b=dec.unused_data;完成=True
                if b:dec=zstandard.ZstdDecompressor().decompressobj();完成=False
            else:b=b''
assert 完成 and 框架>0,'壓縮框架未完整到達結尾'
def 寫(n,rows):
    with (表/n).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
中=['海上移動通信業務識別碼','基準日期時間','經度','緯度','對地速度','對地航向','真航向','船名','國際海事組織船號','呼號','船型','航行狀態','長度','寬度','吃水','貨物類型','收發器類別']
寫('全量逐欄品質.csv',[{'原欄名':n,'中文欄名':中[i],'資料行':統[n]['資料行'],'空字串':統[n]['空字串'],'非空':統[n]['非空'],'不可解析數值':統[n]['不可解析數值'],'非有限數值':統[n]['非有限數值'],'字典值域外':統[n]['字典值域外'],'整數欄出現非整數':統[n]['整數欄出現非整數'],'最小原數值':最小.get(n,''),'最大原數值':最大.get(n,''),'值域外判定':'僅與2025起字典對比；不是錯誤根因已核'} for i,n in enumerate(預期)])
寫('完整檔日期分布.csv',[{'日期':k,'資料行':v} for k,v in sorted(日期.items())]);寫('完整檔小時分布.csv',[{'小時':k,'資料行':v} for k,v in sorted(小時.items())]);寫('收發器類別分布.csv',[{'原類別':k,'資料行':v} for k,v in sorted(類.items())])
寫('完整檔基本核查.csv',[{'核查項':n,'不符資料行':異[n],'分母':列數} for n in ['欄位數不符','時間不可解析','識別碼非九位數字']]+[{'核查項':'日期不屬2026年6月30日','不符資料行':sum(v for k,v in 日期.items() if k!='2026-06-30'),'分母':列數}])
結果={'完整資料行':列數,'實得壓縮位元組':總,'完整解壓位元組':解壓位元組,'完整壓縮框架數':框架,'框架完整到尾':True,'欄位數':len(欄頭),'2025起欄位字典相符':True,'觀測日期分布':dict(日期),'來源雜湊':收['来源雜湊'],'精確重複已核':False,'異常根因已核':False,'全年品質已核':False,'全球覆蓋已核':False}
(工作/'核查結果.json').write_text(json.dumps(結果,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(結果,ensure_ascii=False),flush=True)
