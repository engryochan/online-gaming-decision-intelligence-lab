from pathlib import Path
import csv,json,zipfile,io,hashlib,tempfile,collections,subprocess,datetime,math
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/83_時間粒度與異常分層核查_B60_20261011';主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd';雜湊=lambda b:hashlib.sha256(b).hexdigest()
assert not (工作/'基線.json').exists(),'禁止刷新基線'
表.mkdir();原文=(根/主).read_bytes();路徑=[p for p in subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0') if p]
基={'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'原有文件':{p:雜湊((根/p).read_bytes()) for p in 路徑 if Path(p).suffix in ('.md','.qmd') and (根/p).is_file()},'主報告':主,'原文位元組':len(原文),'原文雜湊':雜湊(原文)}
(工作/'基線.json').write_text(json.dumps(基,ensure_ascii=False,indent=2),encoding='utf-8')
收=json.loads((根/'reports/2026-10-11/歷史完整檔品質核查_B58/完整檔取得收據.json').read_text(encoding='utf-8'));檔=Path(收['本機原始資料']);h=hashlib.sha256()
with 檔.open('rb') as f:
    for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
assert h.hexdigest()==收['來源雜湊']
暫存=Path(tempfile.mkdtemp(prefix='科研時間鍵核查_'));路=[暫存/('時間鍵分區'+str(i)+'.jsonl') for i in range(256)];文件=[p.open('wb') for p in 路]
秒=collections.Counter();异常=collections.Counter();總行=0
try:
    with zipfile.ZipFile(檔) as z:
        assert len(z.infolist())==1
        with z.open(z.infolist()[0]) as raw,io.TextIOWrapper(raw,encoding='utf-8-sig',newline='') as f:
            reader=csv.reader(f);header=next(reader);assert len(header)==17 and header[:2]==['MMSI','BaseDateTime']
            for row in reader:
                assert len(row)==17;總行+=1
                向量=json.dumps(row,ensure_ascii=False,separators=(',',':')).encode('utf-8');鍵=json.dumps(row[:2],ensure_ascii=False,separators=(',',':')).encode('utf-8')
                文件[hashlib.sha256(鍵).digest()[0]].write(向量+b'\n')
                d=datetime.datetime.fromisoformat(row[1]);秒[(d.second,d.microsecond)]+=1
                if not(len(row[0])==9 and row[0].isdigit()):异常[('識別碼非九位數字','原字串長度'+str(len(row[0])),row[16] or '空字串')]+=1
                if row[14] and float(row[14])<0:异常[('吃水負值',row[14],row[16] or '空字串')]+=1
                if 總行%1000000==0:print('時間鍵與異常分區進度：'+str(總行)+'行',flush=True)
finally:
    for f in 文件:f.close()
assert 總行==7516408
分區=[];鍵頻=collections.Counter();欄衝=collections.Counter();範圍統計=collections.Counter();總鍵=0;多鍵=0;衝鍵=0;衝行=0;同向量多餘=0
for i,p in enumerate(路):
    groups={}
    with p.open('rb') as f:
        for line in f:
            向量=line[:-1];r=json.loads(向量);鍵=tuple(r[:2]);groups.setdefault(鍵,collections.Counter())[向量]+=1
    n=0;衝=0;涉及=0;多餘=0;多=0
    for 鍵,c in groups.items():
        次=sum(c.values());獨=len(c);n+=次;多+=次>1;鍵頻[(次,獨)]+=1;多餘+=次-獨
        有效=len(鍵[0])==9 and 鍵[0].isdigit();範='九位數字格式識別碼' if 有效 else '格式不符識別碼'
        範圍統計[(範,'時間鍵總數')]+=1;範圍統計[(範,'資料行')]+=次
        if 獨>1:
            衝+=1;涉及+=次;範圍統計[(範,'同鍵多向量組')]+=1;範圍統計[(範,'涉及行')]+=次
            vectors=[json.loads(v) for v in c]
            for j,k in enumerate(header):欄衝[k]+=len({r[j] for r in vectors})>1
    分區.append({'分區編號':i,'資料行':n,'時間鍵':len(groups),'同鍵多行組':多,'同鍵多向量組':衝,'多向量涉及行':涉及,'完全相同向量多餘行':多餘})
    總鍵+=len(groups);多鍵+=多;衝鍵+=衝;衝行+=涉及;同向量多餘+=多餘
    if (i+1)%32==0:print('時間鍵對賬：'+str(i+1)+'／256',flush=True)
assert sum(r['資料行'] for r in 分區)==總行 and 同向量多餘==515
assert sum(n*v for (n,u),v in 鍵頻.items())==總行 and sum(鍵頻.values())==總鍵
assert sum(秒.values())==總行
def 寫表(名,rs):
    with (表/名).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
寫表('時間鍵分區對賬.csv',分區)
寫表('同鍵資料行與向量分布.csv',[{'同鍵資料行':n,'同鍵唯一向量':u,'時間鍵組數':v} for (n,u),v in sorted(鍵頻.items())])
中=['海上移動通信業務識別碼','基準日期時間','緯度','經度','對地航速','對地航向','真航向','船名','國際海事組織船舶編號','呼號','船型','狀態','長度','寬度','吃水','原始船型或貨物類別','收發機類別']
寫表('同鍵不同欄位計數.csv',[{'原欄名':k,'中文欄名':中[j],'值不同的時間鍵組':欄衝[k],'分母同鍵多向量組':衝鍵} for j,k in enumerate(header)])
寫表('時間秒與微秒分布.csv',[{'秒':s,'微秒':u,'資料行':n} for (s,u),n in sorted(秒.items())])
寫表('異常原值或長度分層.csv',[{'異常項':k,'原吃水值或長度類別':v,'原收發機類別':c,'中文收發機說明':'甲類' if c=='A' else '乙類' if c=='B' else '空值或其他原碼','資料行':n,'根因狀態':'未取得原始輸入及處理歷程，不能據此判定根因'} for (k,v,c),n in sorted(异常.items())])
寫表('識別碼格式分層時間鍵統計.csv',[{'識別碼格式範圍':s,'統計項':k,'計數':n,'身份核定':'格式不是國籍、所有權或法人核定'} for (s,k),n in sorted(範圍統計.items())])
統計={'完整資料行':總行,'精確時間鍵':總鍵,'同鍵多行組':多鍵,'同鍵多向量組':衝鍵,'多向量涉及行':衝行,'完全相同向量多餘行':同向量多餘,'整分鐘時間行':秒[(0,0)],'非整分鐘時間行':總行-秒[(0,0)],'來源雜湊':收['來源雜湊'],'完整壓縮校驗再次通過':True,'同鍵多向量根因已核':False,'跨日重複已核':False,'全球完成':False,'定義':'按MMSI（海上移動通信業務識別碼）及BaseDateTime（基準日期時間）原字串精確分組；同鍵多向量不是已證實的錯誤或身份衝突'}
(工作/'核查結果.json').write_text(json.dumps(統計,ensure_ascii=False,indent=2),encoding='utf-8');(工作/'本機來源收據.json').write_text(json.dumps({'完整原始檔':str(檔),'本機時間鍵分區':str(暫存),'來源雜湊':收['來源雜湊'],'原始及分區是否推送':False},ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(統計,ensure_ascii=False),flush=True)
