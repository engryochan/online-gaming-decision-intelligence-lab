from pathlib import Path
import csv, json, hashlib, urllib.request, datetime, subprocess
工作=Path(__file__).resolve().parent
根=工作.parents[2]
原=工作/'原始回應'; 原.mkdir(exist_ok=True)
表=根/'Reference/tables/89_服務現況重測_B67_20261012';表.mkdir(parents=True,exist_ok=True)
def 讀表(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
舊=讀表(根/'Reference/tables/86_公開服務逐圖層核查_B63_20261011/未啟動服務證據.csv')
產品=讀表(根/'Reference/tables/88_未啟動服務替代來源核查_B65_20261011/官方替代來源與栅格結構.csv')
收=[];行=[]
for s,p in zip(舊,產品):
    年=p['觀測年份']
    for 類,url,method in [('原服務',s['網址'],'GET'),('替代栅格',p['官方替代網址'],'HEAD')]:
        req=urllib.request.Request(url,method=method,headers={'User-Agent':'Research-source-audit/1.0'})
        with urllib.request.urlopen(req,timeout=60) as resp:
            b=resp.read() if method=='GET' else b''
            記={'觀測UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'年份':年,'類型':類,'網址':url,'方法':method,'狀態碼':resp.status,'回應標頭':dict(resp.headers),'正文位元組':len(b)}
        if method=='GET':
            data=json.loads(b);err=data.get('error');ok=not err and ('layers' in data or 'currentVersion' in data)
            f=原/(年+'_原服務.json');f.write_bytes(b)
            記.update({'原始檔':f.relative_to(根).as_posix(),'來源雜湊':hashlib.sha256(b).hexdigest()})
            行.append({'年份':年,'類型':類,'HTTP狀態':記['狀態碼'],'可用':ok,'服務錯誤':json.dumps(err,ensure_ascii=False),'宣告位元組':'','與前批大小一致':'','與前批版本一致':''})
        else:
            h={k.lower():v for k,v in 記['回應標頭'].items()};size=int(h['content-length']);tag=h.get('etag','').strip('"')
            行.append({'年份':年,'類型':類,'HTTP狀態':記['狀態碼'],'可用':記['狀態碼']==200,'服務錯誤':'','宣告位元組':size,'與前批大小一致':size==int(p['完整檔宣告位元組']),'與前批版本一致':tag==p['來源版本標籤']})
        收.append(記)
assert len(收)==len(行)==6
(工作/'來源收據.json').write_text(json.dumps(收,ensure_ascii=False,indent=2),encoding='utf-8')
with (表/'服務與替代檔案現況.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(行[0]));w.writeheader();w.writerows(行)
結果={'觀測日期':'2026-10-12','原服務實測數':3,'原服務可用數':sum(r['可用'] for r in 行 if r['類型']=='原服務'),'替代檔頭請求數':3,'替代檔版本及大小一致數':sum(r['與前批大小一致'] and r['與前批版本一致'] for r in 行 if r['類型']=='替代栅格'),'完整產品品質已核':False}
(工作/'核查結果.json').write_text(json.dumps(結果,ensure_ascii=False,indent=2),encoding='utf-8')
報='''---
title: "第六十七批：服務現況與官方替代檔案重測"
lang: zh-TW
format: html
---

本輪另存 2026 年 10 月 12 日實測，不覆寫第六十三至六十六批證據。

## 本輪實測結果

'''+ '\n'.join('- '+k+'：'+str(v) for k,v in 結果.items())+'''

原服務判定同時檢查 HTTP（超文本傳輸協定）狀態與 JSON（結構化資料格式）正文內的服務錯誤，不把 HTTP 200 當成服務可用。替代檔案使用 HEAD（只取得回應標頭）核對完整檔案宣告大小與 ETag（來源版本標籤）；版本標籤不等於完整檔案雜湊。

## 保存證據與限制

六次請求的網址、UTC（協調世界時）觀測時間及回應標頭見 `reports/2026-10-12/服務現況重測_B67/來源收據.json`。三份服務原始正文另存並記錄 SHA256（安全雜湊算法）；表格見 `tables/89_服務現況重測_B67_20261012/服務與替代檔案現況.csv`。

檔案可取得與版本未變只支持本次連線現況，不能證明逐像元品質、所有用途授權或全球覆蓋。尚未取得三份完整栅格；仍保留此前投影、無資料值與地域限制。
'''
(根/'Reference/服務現況重測_B67_20261012.qmd').write_text(報,encoding='utf-8')
print(json.dumps(結果,ensure_ascii=False))
