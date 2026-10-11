from pathlib import Path
import csv,json,zipfile,io,hashlib,tempfile,collections,subprocess,datetime
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/82_完整單日重複率核查_B59_20261011'
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd';雜湊=lambda b:hashlib.sha256(b).hexdigest()
表.mkdir(exist_ok=True);原文=(根/主).read_bytes();路徑=[p for p in subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0') if p]
基={'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'原有文件':{p:雜湊((根/p).read_bytes()) for p in 路徑 if Path(p).suffix in ('.md','.qmd') and (根/p).is_file()},'主報告':主,'原文位元組':len(原文),'原文雜湊':雜湊(原文)}
if (工作/'基線.json').exists():
    assert json.loads((工作/'基線.json').read_text(encoding='utf-8'))==基,'重試時基線已變更，禁止刷新'
    assert not (工作/'核查結果.json').exists(),'本批已完成，禁止重跑'
else:
    (工作/'基線.json').write_text(json.dumps(基,ensure_ascii=False,indent=2),encoding='utf-8')
收=json.loads((根/'reports/2026-10-11/歷史完整檔品質核查_B58/完整檔取得收據.json').read_text(encoding='utf-8'));檔=Path(收['本機原始資料']);h=hashlib.sha256()
with 檔.open('rb') as f:
    for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
assert h.hexdigest()==收['來源雜湊'] and 檔.stat().st_size==收['取得位元組']
暫存=Path(tempfile.mkdtemp(prefix='科研精確重複核查_'));路=[暫存/('資料分區'+str(i)+'.jsonl') for i in range(256)];文件=[p.open('wb') for p in 路];行數=0;欄錯=0
try:
    with zipfile.ZipFile(檔) as z:
        infos=z.infolist();assert len(infos)==1
        with z.open(infos[0]) as raw,io.TextIOWrapper(raw,encoding='utf-8-sig',newline='') as f:
            reader=csv.reader(f);header=next(reader);assert len(header)==17
            for row in reader:
                行數+=1;欄錯+=len(row)!=17
                # JSON向量保留17欄原字串與順序，僅正規化CSV的引號封裝。
                b=json.dumps(row,ensure_ascii=False,separators=(',',':')).encode('utf-8')
                文件[hashlib.sha256(b).digest()[0]].write(b+b'\n')
                if 行數%1000000==0:print('精確重複分區進度：'+str(行數)+'行',flush=True)
finally:
    for f in 文件:f.close()
assert 行數==收['完整資料行']==7516408 and 欄錯==0
分區=[];頻數=collections.Counter();唯一=0;重複組=0;多餘=0;涉及=0;最多=0;峰值=0
for i,p in enumerate(路):
    # 以完整字串向量作字典鍵，不用雜湊相等代替資料相等。
    with p.open('rb') as f:c=collections.Counter(line[:-1] for line in f)
    n=sum(c.values());u=len(c);d=sum(v>1 for v in c.values());e=n-u;v=sum(v for v in c.values() if v>1);m=max(c.values(),default=0)
    唯一+=u;重複組+=d;多餘+=e;涉及+=v;最多=max(最多,m);峰值=max(峰值,u);頻數.update(c.values())
    分區.append({'分區編號':i,'資料行':n,'唯一字串向量':u,'重複組':d,'多餘重複行':e,'涉及重複的行':v,'最高出現次數':m,'本機分區檔':str(p),'分區位元組':p.stat().st_size})
    if (i+1)%32==0:print('精確分區對賬：'+str(i+1)+'／256',flush=True)
assert sum(r['資料行'] for r in 分區)==行數 and 唯一+多餘==行數
assert sum(k*v for k,v in 頻數.items())==行數 and sum(頻數.values())==唯一
def 寫表(名,rows):
    with (表/名).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
寫表('完整單日重複分區對賬.csv',分區)
寫表('完整單日出現次數分布.csv',[{'單一字串向量出現次數':k,'字串向量組數':v,'對應資料行':k*v} for k,v in sorted(頻數.items())])
統計={'完整資料行':行數,'唯一字串向量':唯一,'重複組':重複組,'多餘重複行':多餘,'涉及重複的行':涉及,'多餘重複行比例':多餘/行數,'涉及重複的行比例':涉及/行數,'最高出現次數':最多,'分區數':256,'峰值分區唯一向量':峰值,'來源雜湊':收['來源雜湊'],'原始資料是否改寫':False,'原始或分區資料是否推送':False,'完整壓縮校驗再次通過':True,'跨日重複已核':False,'全球完成':False,'定義':'17欄原字串及順序完全相同；CSV引號封裝正規化，不轉型或截斷；不把識別碼及時間相同當整行重複'}
(工作/'核查結果.json').write_text(json.dumps(統計,ensure_ascii=False,indent=2),encoding='utf-8')
(工作/'本機來源收據.json').write_text(json.dumps({'完整原始檔':str(檔),'本機分區目錄':str(暫存),'來源雜湊':收['來源雜湊'],'原來源收據':'reports/2026-10-11/歷史完整檔品質核查_B58/完整檔取得收據.json','資料是否推送':False},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(統計,ensure_ascii=False),flush=True)
