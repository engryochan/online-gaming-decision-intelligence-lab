from pathlib import Path
import csv,json,hashlib,subprocess,sys,re,threading,collections
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor,as_completed
工作=Path(__file__).resolve().parent;根=工作.parents[2]
表=根/'Reference/tables/99_全球金融未嘗試來源續查_B77_20261012'
來源=根/'Reference/tables/95_全球金融未嘗試來源續查_B73_20261012/全4849項接續進度.csv'
def 寫表(名,列):
    欄=list(dict.fromkeys(k for x in 列 for k in x)) or ['無觀察記錄']
    with (表/名).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=欄);w.writeheader();w.writerows(列)
def main():
    assert not (工作/'續查結果.json').exists(),'保留已完成批次'
    表.mkdir(parents=True,exist_ok=True)
    基={'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'來源SHA256':hashlib.sha256(來源.read_bytes()).hexdigest(),'使用者文件雜湊':{p.relative_to(根).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (根/'Reference').glob('春秋戰國*冊二.*')},'Git狀態':subprocess.check_output(['git','status','--short'],cwd=根).decode('utf-8')}
    (工作/'基線.json').write_text(json.dumps(基,ensure_ascii=False,indent=2),encoding='utf-8')
    全=list(csv.DictReader(來源.open(encoding='utf-8-sig')))
    未=[x for x in 全 if int(x['attempt_observations'] or 0)==0]
    訊號=re.compile(r'issuer|equit|securit|stock|compan|instrument|participant|register|licen|broker|member|listing|directory|empresas|emittent|notiert|titres|listed|dealing|admitted',re.I)
    候=[]
    for x in 未:
        u=urlparse(x['target_url']);s=訊號.findall(u.path+'?'+u.query)
        if x['priority'].startswith('P3') or not s or u.username or u.password:continue
        y=dict(x);y['selection_evidence']='未嘗試來源路徑訊號（非官方角色認證）：'+'|'.join(s);y['排序分']=len(s);候.append(y)
    主機=collections.defaultdict(list)
    for x in sorted(候,key=lambda x:(-x['排序分'],x['target_url'])):主機[urlparse(x['target_url']).hostname].append(x)
    選=[]
    for 深 in range(max(map(len,主機.values()),default=0)):
        for h in sorted(主機):
            if 深<len(主機[h]):選.append(主機[h][深])
        if len(選)>=120:break
    選=選[:120];寫表('本輪選定來源.csv',選)
    sys.path.insert(0,str(根/'reports/2026-10-08/global_directory_content_b05'));import intake
    intake.O=工作;intake.T=表;intake.D=工作/'原始回應';intake.D.mkdir(exist_ok=True)
    intake.locks={urlparse(x['target_url']).hostname:threading.Semaphore(1) for x in 選}
    結=[];列=[];下載=[];頁=[]
    with ThreadPoolExecutor(max_workers=8) as 池:
        for future in as_completed([池.submit(intake.get,x) for x in 選]):
            a,b,c,d=future.result();a['checked_on']='2026-10-12';a['核實範圍']='回應及靜態表格取得；實體角色、全量、授權仍待核實';結.append(a);列.extend(b);下載.extend(c);頁.extend(d)
            if len(結)%20==0:print('完成來源',len(結),flush=True)
    for 名,值 in [('來源取得收據.csv',結),('來源表格全量觀察.csv',列),('下載連結觀察.csv',下載),('分頁連結觀察.csv',頁)]:寫表(名,值)
    對={x['work_id']:x for x in 結};新=[]
    for x in 全:
        y=dict(x)
        if x['work_id'] in 對:
            a=對[x['work_id']];y['attempt_observations']=str(int(x['attempt_observations'] or 0)+1);y['last_http_status']=str(a.get('http_status',''));y['receipts_json']=json.dumps(json.loads(x['receipts_json'] or '[]')+[dict(a,batch='B77')],ensure_ascii=False);y['acquisition_status']='本輪取得回應，內容與範圍待核實' if a.get('http_status')==200 else '本輪未取得成功回應，保留缺口'
        新.append(y)
    寫表('全4849項接續進度.csv',新)
    摘={'原工作項':len(全),'原未嘗試':len(未),'本輪嘗試':len(結),'主機數':len({urlparse(x['url']).hostname for x in 結}),'HTTP200':sum(x.get('http_status')==200 for x in 結),'表格觀察行':len(列),'下載觀察':len(下載),'分頁觀察':len(頁),'剩餘未嘗試':sum(int(x['attempt_observations'] or 0)==0 for x in 新),'完整性升級':0,'全球竣工':False}
    assert len(全)==len(新)==4849 and len(結)==len(選) and len(對)==len(選)
    assert all(a['directory_completeness']==b['directory_completeness'] and a['completeness']==b['completeness'] for a,b in zip(全,新))
    assert hashlib.sha256(來源.read_bytes()).hexdigest()==基['來源SHA256']
    for a in 結:
        if a.get('file'):assert hashlib.sha256((根/a['file']).read_bytes()).hexdigest()==a['sha256']
    (工作/'續查結果.json').write_text(json.dumps(摘,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(摘,ensure_ascii=False),flush=True)
    文='---\ntitle: "全球金融未嘗試來源續查：第七十七批"\nlang: zh-Hant\nformat: html\n---\n\n本輪從既有4,849項工作母表挑選尚未嘗試且路徑包含金融名冊訊號的來源，以主機輪替取得回應。訊號不代表網站已獲官方認證；HTTP 200不代表名冊齊全。\n\n'
    文+='| 核查項 | 結果 |\n|---|---:|\n'+''.join(f'|{k}|{v}|\n' for k,v in 摘.items())
    文+='\n原批次與原資料均未覆寫。本輪完整保留取得的靜態表格觀察；觀察行不能直接當成公司或券商數量。截斷回應、動態內容、分頁、實體去重、逐用途授權和國家歸屬均須另核。所有完整性狀態保持未知。\n\n[全量接續進度](tables/99_全球金融未嘗試來源續查_B77_20261012/全4849項接續進度.csv)；[来源取得收據](tables/99_全球金融未嘗試來源續查_B77_20261012/來源取得收據.csv)。\n\n每次回應的網址、日期、位元組及雜湊見收據；程式與基線見 `reports/2026-10-12/全球金融未嘗試來源續查_B77/`。後續先核本輪下載及分頁，再按剩餘未嘗試清單續查，不將新聞與工具頁冒充名冊。\n'
    (根/'Reference/全球金融未嘗試來源續查_B77_20261012.qmd').write_text(文,encoding='utf-8')
if __name__=='__main__':main()
