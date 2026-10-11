from pathlib import Path
from urllib.request import urlopen,Request
from html.parser import HTMLParser
from datetime import datetime,timezone
import json,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];原=工作/'原始來源'
assert not (工作/'免責正文收據.json').exists()
j=json.loads((原/'免責頁官方項目內容.response').read_text(encoding='utf-8'))
def 找(v):
    if isinstance(v,dict):
        if v.get('slug')=='disclaimer' and v.get('id'):return v
        for x in v.values():
            r=找(x)
            if r:return r
    if isinstance(v,list):
        for x in v:
            r=找(x)
            if r:return r
r=找(j);assert r and r['title']=='Disclaimer - Marine Cadastre';收=[];文字=[]
for 名,尾 in [('免責頁正文項目元資料','?f=pjson'),('免責頁正文結構','/data?f=pjson')]:
    url='https://www.arcgis.com/sharing/rest/content/items/'+r['id']+尾
    with urlopen(Request(url,headers={'User-Agent':'Public-terms-audit/1.0'}),timeout=30) as f:b=f.read(4*1024*1024+1);碼=f.status
    assert len(b)<=4*1024*1024;檔=原/(名+'.response');assert not 檔.exists();檔.write_bytes(b);d=json.loads(b);assert not d.get('error')
    收.append({'中文名稱':名,'網址':url,'狀態碼':碼,'原始檔':檔.relative_to(根).as_posix(),'來源雜湊':hashlib.sha256(b).hexdigest(),'取得時間':datetime.now(timezone.utc).isoformat(),'識別碼來源':'官方網站項目內容的pages列表，slug為disclaimer'})
    def 遍(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in ['text','html','markdown'] and isinstance(x,str) and x.strip():文字.append(x)
                else:遍(x)
        elif isinstance(v,list):
            for x in v:遍(x)
    if 尾.startswith('/data'):遍(d)
class 解析(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,d):self.parts.append(d)
p=解析();p.feed('\n'.join(文字));正文='\n'.join(p.parts)
(工作/'免責頁正文摘取.txt').write_text(正文,encoding='utf-8');(工作/'免責正文收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8');print(正文[:6500])
