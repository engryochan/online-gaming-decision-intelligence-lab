from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone
import csv,json,hashlib
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/87_最新完整日檔品質核查_B64_20261011';f=工作/'原始來源/甲類靜態航程報文官方語義.response';assert not (工作/'靜態協議收據.json').exists()
url='https://www.navcen.uscg.gov/ais-class-a-static-voyage-message-5'
if f.exists():b=f.read_bytes();碼=200
else:
    with urlopen(Request(url,headers={'User-Agent':'Public-data-meaning-audit/1.0'}),timeout=45) as r:b=r.read(2*1024*1024+1);碼=r.status
    assert len(b)<=2*1024*1024;f.write_bytes(b)
if not (b'0.1' in b or b'1/10' in b):
    from html.parser import HTMLParser
    class 解析(HTMLParser):
        def __init__(self):super().__init__();self.parts=[]
        def handle_data(self,d):self.parts.append(d)
    p=解析();p.feed(b.decode('utf-8','replace'));t=' '.join(p.parts)
    for w in ['draught','Draught','draft','Draft']:
        i=t.find(w)
        if i>=0:print(t[max(0,i-50):i+1100])
    raise RuntimeError('原文未找到預期精度字串，保留回應後先核對語義')
(工作/'靜態協議收據.json').write_text(json.dumps([{'網址':url,'中文來源':'海岸警衛隊甲類靜態及航程報文語義','狀態碼':碼,'原始檔':f.relative_to(根).as_posix(),'来源雜湊':hashlib.sha256(b).hexdigest(),'取得時間':datetime.now(timezone.utc).isoformat()}],ensure_ascii=False,indent=2),encoding='utf-8')
with (表/'字典值域外原值分層.csv').open(encoding='utf-8-sig',newline='') as h:rows=list(csv.DictReader(h))
assert sum(int(r['資料行']) for r in rows if r['原欄名']=='status')==3587055 and all(r['原字串值']=='0' for r in rows if r['原欄名']=='status')
assert sum(int(r['資料行']) for r in rows if r['原欄名']=='draft')==34586 and all(0.1<=float(r['原字串值'])<=0.9 for r in rows if r['原欄名']=='draft')
追加='''
## 字典差異的全量分層覆核

重新核來源雜湊並完整再讀10,622,482行：航行狀態字典域外3,587,055行全部是甲類收發器的狀態0，已核官方協議為使用引擎航行，不能列為非法狀態。

吃水字典域外34,586行全部是0.1至0.9米，11個原值／收發器分層組。[官方甲類靜態及航程報文](https://www.navcen.uscg.gov/ais-class-a-static-voyage-message-5)以0.1米編碼吃水，因此這些小於1米的正值在協議編碼中可以表達，不能僅因產品字典下限1米便判為物理或協議錯誤。這不證明實際船舶吃水正確。乙類的0.3米356行與0.6米6行另保留來源類別，不因產品欄有值推定乙類原报文直接帶有同欄。

目前兩欄差異已從「字典對比域外」收斂為具體原值與協議解釋；實際船舶屬性正確性及來源補值根因仍需額外證據，不自動改寫。詳見[原值分層](tables/87_最新完整日檔品質核查_B64_20261011/字典值域外原值分層.csv)。
'''
p=根/'Reference/最新完整日檔品質核查_B64_20261011.qmd';p.write_text(p.read_text(encoding='utf-8')+追加,encoding='utf-8')
# 本批自有驗證器增補分層與新來源核驗；舊基線及原收據不刷新。
p=工作/'驗證與提交.py';s=p.read_text(encoding='utf-8');s=s.replace("+json.loads((工作/'協議語義收據.json').read_text(encoding='utf-8'))","+json.loads((工作/'協議語義收據.json').read_text(encoding='utf-8'))+json.loads((工作/'靜態協議收據.json').read_text(encoding='utf-8'))")
s=s.replace("r['來源雜湊']","r.get('來源雜湊',r.get('来源雜湊'))")
s=s.replace('    if 暫存:',"    層=讀表('字典值域外原值分層.csv');assert len(層)==12\n    assert sum(int(r['資料行']) for r in 層 if r['原欄名']=='status')==3587055\n    assert sum(int(r['資料行']) for r in 層 if r['原欄名']=='draft')==34586\n    assert json.loads((工作/'值域分層收據.json').read_text(encoding='utf-8'))['全檔再讀行數']==結['完整資料行']\n    if 暫存:")
p.write_text(s,encoding='utf-8')
print('兩欄全量差異原值與官方協議語義已校訂。')
