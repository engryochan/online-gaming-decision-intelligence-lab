from pathlib import Path
from collections import Counter, defaultdict
import csv, io, json, hashlib, struct, tempfile, sys, subprocess, datetime
工作=Path(__file__).resolve().parent;根=工作.parents[2]
H=lambda b:hashlib.sha256(b).hexdigest()

def 計數(rows,ki):
    groups=defaultdict(Counter)
    for row in rows:groups[tuple(row[i] for i in ki)][tuple(row)]+=1
    return {'資料行':sum(sum(c.values()) for c in groups.values()),'候選鍵數':len(groups),'完整欄值唯一數':sum(len(c) for c in groups.values()),'精確重複額外行':sum(sum(c.values())-len(c) for c in groups.values()),'精確重複組':sum(sum(n>1 for n in c.values()) for c in groups.values()),'候選鍵多行組':sum(sum(c.values())>1 for c in groups.values()),'同鍵不同完整欄值組':sum(len(c)>1 for c in groups.values()),'最大同鍵資料行':max((sum(c.values()) for c in groups.values()),default=0)}

def main():
    依賴=Path.home()/'AppData/Local/Temp/科研壓縮驗收依賴_B64'
    sys.path.insert(0,str(依賴));import zstandard
    舊=根/'reports/2026-10-11/最新完整日檔品質核查_B64'
    收=json.loads((舊/'取得收據.json').read_text(encoding='utf-8'));p=Path(收['本機原始檔'])
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    assert h.hexdigest()==收['来源雜湊'] and p.stat().st_size==收['實得位元組']
    paths=subprocess.check_output(['git','ls-files','-z'],cwd=根).decode().split('\0')
    if (工作/'基線.json').exists():
        基=json.loads((工作/'基線.json').read_text(encoding='utf-8'))
        assert all(H((根/q).read_bytes())==v for q,v in 基['既有正文'].items()),'既有正文有變更，停止'
    else:
        (工作/'基線.json').write_text(json.dumps({'提交':subprocess.check_output(['git','rev-parse','HEAD'],cwd=根).decode().strip(),'既有正文':{q:H((根/q).read_bytes()) for q in paths if q.endswith(('.md','.qmd')) and (根/q).is_file()}},ensure_ascii=False,indent=2),encoding='utf-8')
    tmp=Path(tempfile.mkdtemp(prefix='科研精確重複_B68_'));桶=[tmp/(str(i)+'.jsonl') for i in range(256)]
    fs=[q.open('wb') for q in 桶];n=0
    try:
        with p.open('rb') as f,zstandard.ZstdDecompressor().stream_reader(f) as zr,io.TextIOWrapper(zr,encoding='utf-8-sig',newline='') as t:
            reader=csv.reader(t);header=next(reader);assert len(header)==17
            ki=[header.index('mmsi'),header.index('base_date_time')]
            for row in reader:
                assert len(row)==17
                key=json.dumps([row[i] for i in ki],ensure_ascii=False,separators=(',',':')).encode()
                payload=json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()
                fs[hashlib.sha256(key).digest()[0]].write(payload+b'\n');n+=1
                if n%2000000==0:print('已分桶資料行',n,flush=True)
    finally:
        for f in fs:f.close()
    assert n==10622482
    rows=[]
    for i,q in enumerate(桶):
        with q.open('r',encoding='utf-8') as f:r=計數((json.loads(line) for line in f),ki)
        rows.append({'分桶編號':i,**r})
        if i%32==0:print('已核查分桶',i+1,flush=True)
    total={k:(max(r[k] for r in rows) if k=='最大同鍵資料行' else sum(r[k] for r in rows)) for k in rows[0] if k!='分桶編號'}
    assert total['資料行']==n==total['完整欄值唯一數']+total['精確重複額外行']
    表=根/'Reference/tables/90_最新日檔精確重複核查_B68_20261012';表.mkdir(parents=True,exist_ok=True)
    with (表/'分桶精確核查.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    結={'核查UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'觀測日期':'2026-06-30','來源SHA256':h.hexdigest(),'候選鍵':['mmsi（海上移動通信業務識別碼）','base_date_time（基準日期時間）'],'比對定義':'CSV解析後全部17欄字串逐項相等；不修剪、不改大小寫、不轉數值、不改時間精度','雜湊用途':'只分桶；鍵與全部欄值以原字串元組比較，不以雜湊相同判定重複','分桶數':256,'暫存桶總位元組':sum(q.stat().st_size for q in 桶),'原始記錄推送':False,'精確重複已核':True,'全年品質已核':False,'全球覆蓋已核':False,**total}
    (工作/'核查結果.json').write_text(json.dumps(結,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(結,ensure_ascii=False),flush=True)
    # 只清除本脚本剛建立、已完成計數的單層暫存桶；原始壓縮檔保留。
    for q in 桶:q.unlink()
    tmp.rmdir()

if __name__=='__main__':main()
