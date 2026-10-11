from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import json,csv,io,sys,tempfile,hashlib
sys.path.insert(0,str(Path(tempfile.gettempdir())/'科研壓縮驗收依賴_B64'));import zstandard
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/87_最新完整日檔品質核查_B64_20261011';assert not (工作/'值域分層收據.json').exists()
收=json.loads((工作/'取得收據.json').read_text(encoding='utf-8'));p=Path(收['本機原始檔']);h=hashlib.sha256()
with p.open('rb') as f:
    for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
assert h.hexdigest()==收['来源雜湊']
異=Counter();n=0
with p.open('rb') as f,zstandard.ZstdDecompressor().stream_reader(f) as z,io.TextIOWrapper(z,encoding='utf-8-sig',newline='') as text:
    r=csv.reader(text);head=next(r);s=head.index('status');d=head.index('draft');c=head.index('transceiver')
    for row in r:
        n+=1
        for index,field,lo,hi in [(s,'status',1,14),(d,'draft',1,24)]:
            v=row[index]
            if v and not lo<=float(v)<=hi:異[(field,v,row[c])]+=1
with (表/'字典值域外原值分層.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['原欄名','中文欄名','原字串值','原收發器類別','資料行','判定']);w.writeheader()
    w.writerows({'原欄名':field,'中文欄名':{'status':'航行狀態','draft':'吃水'}[field],'原字串值':v,'原收發器類別':c,'資料行':count,'判定':'字典對比差異；協議語義另核，不自動刪改'} for (field,v,c),count in sorted(異.items()))
(工作/'值域分層收據.json').write_text(json.dumps({'全檔再讀行數':n,'來源雜湊':h.hexdigest(),'來源重驗時間':datetime.now(timezone.utc).isoformat(),'原值分層組數':len(異),'航行狀態值域外行':sum(v for (field,_,_),v in 異.items() if field=='status'),'吃水值域外行':sum(v for (field,_,_),v in 異.items() if field=='draft')},ensure_ascii=False,indent=2),encoding='utf-8')
print('原值分層',dict(異))
