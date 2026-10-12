from pathlib import Path
import csv,json,importlib.util
from lxml import html
W=Path(__file__).resolve().parent;R=W.parents[2];T=R/'Reference/tables/107_全球交易所與美國證券全量續核_B85_20261012'
tree=html.fromstring((W/'世界交易所聯合會.response').read_bytes());rows=[]
for i,e in enumerate(tree.xpath('//a[@href]'),1):
 name=' '.join(e.text_content().split())
 rows.append(dict(來源='世界交易所聯合會',來源網址='https://www.world-exchanges.org/membership-events',頁內序號=i,名稱原值=name,名稱中譯='待逐項中譯',連結原值=e.get('href'),類型核定='全部頁面連結，含導覽；待分類，不作股市數量'))
with (T/'官方頁面全部連結待分類.csv').open('w',encoding='utf-8-sig',newline='') as f:
 d=csv.DictWriter(f,fieldnames=list(rows[0]));d.writeheader();d.writerows(rows)
p=W/'結果.json';x=json.loads(p.read_text(encoding='utf-8'));x['官方頁內連結待分類']=len(rows);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
(W/'頁面結構校正收據.json').write_text(json.dumps({'舊解析連結':0,'全頁連結':len(rows),'原因':'頁面未使用main或article容器，改為保留全部a元素，導覽與機構仍待分類','原始來源未改動':True},ensure_ascii=False,indent=2),encoding='utf-8')
q=R/'Reference/全球交易所與美國證券全量續核_B85_20261012.qmd'
with q.open('a',encoding='utf-8') as f:f.write(f'\n頁面結構校正後保留世界交易所聯合會全部{len(rows)}個連結，包含導覽，尚未核定為機構數量。美國證監會頁面下載失敗，現行名稱依官方網頁閱讀核查，未冒充已取得本機原文。\n')
spec=importlib.util.spec_from_file_location('核查',R/'reports/2026-10-11/未啟動服務替代來源核查_B65/驗證與提交.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.工作=W;m.範圍=[W.relative_to(R).as_posix(),T.relative_to(R).as_posix(),q.relative_to(R).as_posix()];m.密碼掃描();print('全部連結保留：',len(rows))
