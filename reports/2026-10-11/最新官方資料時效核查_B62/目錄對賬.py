from pathlib import Path
import re,json,csv
from datetime import date,timedelta
工作=Path(__file__).resolve().parent;根=工作.parents[2];p=工作/'原始來源';表=根/'Reference/tables/85_最新官方資料時效核查_B62_20261011'
統=[]
for 年,名 in [(2025,'2025年逐日位置目錄'),(2026,'2026年逐日位置目錄探測')]:
    b=(p/(名+'.response')).read_text(encoding='utf-8');d=re.findall(r'href="ais-('+str(年)+r'-\d{2}-\d{2})\.csv\.zst"',b);assert d
    始=date.fromisoformat(min(d));終=date.fromisoformat(max(d));expected={(始+timedelta(days=i)).isoformat() for i in range((終-始).days+1)}
    統.append({'觀測年份':年,'日檔連結數':len(d),'唯一日期':len(set(d)),'最早檔名日期':min(d),'最晚檔名日期':max(d),'已列區間缺失日期':','.join(sorted(expected-set(d))),'重複日期':len(d)-len(set(d)),'目錄文件更新時間':','.join(sorted(set(re.findall(r'class="date">(2026-[\d :\-]+)<',b)))),'查證日期':'2026-10-11','核實層級':'目錄日期對賬；未核全量內容'})
with (表/'位置目錄日期對賬.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(統[0]));w.writeheader();w.writerows(統)
服=json.loads((p/'地理資訊服務目錄.response').read_text(encoding='utf-8'));assert not 服.get('error')
with (表/'公開地理資訊服務.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['原服務名','原服務類型','核查範圍']);w.writeheader();w.writerows({'原服務名':s['name'],'原服務類型':s['type'],'核查範圍':'公開目錄；非逐圖層授權或性能驗證'} for s in 服.get('services',[]))
(工作/'時效對賬.json').write_text(json.dumps({'年度目錄':統,'公開服務數':len(服.get('services',[])),'來源未下載全量產品':True},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(統,ensure_ascii=False));print('公開服務數',len(服.get('services',[])))
print((p/'航跡現行目錄.response').read_text(encoding='utf-8')[:2500])
