from pathlib import Path
from collections import Counter
import json,csv,hashlib,io,xml.etree.ElementTree as ET
工作=Path(__file__).resolve().parent;根=工作.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));附=json.loads((工作/'附加收據.json').read_text(encoding='utf-8'))
for p,h in 基['既有正文'].items():
    b=(根/p).read_bytes()
    if p==附['主報告']:
        n=附['原文位元組'];assert H(b[:n])==h==附['原文雜湊'] and H(b[n:])==附['附加雜湊']
    else:assert H(b)==h,'既有正文變更：'+p
收=json.loads((工作/'來源收據.json').read_text(encoding='utf-8'));結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'));assert len(收)==6
for r in 收:
    b=(根/r['原始檔']).read_bytes();assert H(b)==r['來源雜湊'] and len(b)==r['實得位元組'] and r['狀態碼']==200
表=根/'Reference/tables/93_全球貨幣與市場代碼全量續核_B71_20261012'
def 讀(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
幣=讀(表/'全量現行與歷史貨幣.csv');市=讀(表/'全量市場識別碼.csv');覆=讀(表/'逐國家地區覆蓋與缺口.csv');未=讀(表/'未關聯貨幣來源記錄.csv')
母=讀(根/'Reference/tables/01_country_area/registry_country_area_iso3166_m49_e164_20261004.csv');codes={r['iso_alpha2'] for r in 母}
assert len(覆)==len(母)==結['國家地區母表行數'] and {r['國家地區ISO代碼'] for r in 覆}==codes
for name,tag,state in [('現行貨幣與基金.xml','CcyNtry','現行'),('歷史貨幣與基金.xml','HstrcCcyNtry','歷史')]:
    e=ET.parse(工作/'原始來源'/name).findall('.//'+tag);rows=[r for r in 幣 if r['狀態中譯']==state]
    assert len(e)==len(rows)
    for x,r in zip(e,rows):
        y=ET.fromstring(r['來源XML']);assert ET.tostring(x).strip()==ET.tostring(y).strip()
        assert r['字母代碼']==x.findtext('Ccy','') and r['來源實體名稱原值']==x.findtext('CtryNm','')
src=讀(工作/'原始來源/完整市場識別碼.csv');assert len(src)==len(市)==結['市场代碼來源行']
assert all(a==json.loads(b['來源所有欄位JSON']) for a,b in zip(src,市))
assert len({r['市場識別碼'] for r in 市})==len(市)
assert len(未)==結['貨幣來源實體未關聯行']==sum(not r['國家地區ISO代碼'] for r in 幣)
assert {r['國家地區ISO代碼'] for r in 幣 if r['國家地區ISO代碼']}<=codes
for c in 覆:
    iso=c['國家地區ISO代碼']
    assert int(c['現行貨幣來源行'])==sum(r['國家地區ISO代碼']==iso and r['狀態中譯']=='現行' for r in 幣)
    assert int(c['歷史貨幣來源行'])==sum(r['國家地區ISO代碼']==iso and r['狀態中譯']=='歷史' for r in 幣)
    assert int(c['市場代碼來源行'])==sum(r['國家地區ISO代碼']==iso for r in 市)
assert not 結['全球上市公司已齊'] and not 結['全球券商已齊'] and not 結['所有歷史貨幣已齊']
html=根/'Reference/全球貨幣與市場代碼全量續核_B71_20261012.html';assert html.stat().st_size>1000
(工作/'交付驗收.json').write_text(json.dumps({'既有正文保留數':len(基['既有正文']),'主報告原文保留':True,'來源回應雜湊核對數':6,'母表全部行納入':True,'貨幣原始元素逐項對賬':True,'市場所有欄位逐項對賬':True,'未關聯行保留':True,'成品雜湊':H(html.read_bytes()),'市場來源未落母表行數':sum(r['國家地區ISO代碼'] not in codes for r in 市)},ensure_ascii=False,indent=2),encoding='utf-8')
print('全球來源逐項對賬、母表覆蓋及原文保留驗收通過。')
