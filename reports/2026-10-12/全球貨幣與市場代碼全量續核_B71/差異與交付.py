from pathlib import Path
from collections import Counter
import csv,json,hashlib,xml.etree.ElementTree as ET
工作=Path(__file__).resolve().parent;根=工作.parents[2];表=根/'Reference/tables/93_全球貨幣與市場代碼全量續核_B71_20261012';H=lambda b:hashlib.sha256(b).hexdigest()
基=json.loads((工作/'基線.json').read_text(encoding='utf-8'));assert all(H((根/p).read_bytes())==h for p,h in 基['既有正文'].items())
def 讀(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def 寫(n,rows,fields):
    with (表/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
幣=讀(表/'全量現行與歷史貨幣.csv');市=讀(表/'全量市場識別碼.csv');未=[r for r in 幣 if not r['國家地區ISO代碼']]
寫('未關聯貨幣來源記錄.csv',未,list(幣[0]))
舊市={r['MIC']:json.loads(r['raw_fields_json']) for r in 讀(根/'Reference/tables/24_financial_universe_b06_20261007/registry_iso10383_mic.csv')};差=[]
for r in 市:
    c=r['市場識別碼'];n=json.loads(r['來源所有欄位JSON']);o=舊市.get(c,{})
    keys=sorted(k for k in set(n)|set(o) if n.get(k)!=o.get(k))
    if keys:差.append({'市場識別碼':c,'差異欄位原名':' / '.join(keys),'舊所有欄位JSON':json.dumps(o,ensure_ascii=False),'新所有欄位JSON':json.dumps(n,ensure_ascii=False)})
寫('市場全部欄位跨批次差異.csv',差,['市場識別碼','差異欄位原名','舊所有欄位JSON','新所有欄位JSON'])
def 特徵(state,xml):
    x=ET.fromstring(xml)
    return (state,tuple((e.tag,e.text or '',tuple(sorted(e.attrib.items()))) for e in x))
舊幣=讀(根/'Reference/tables/21_currency_broker_b03_20261007/registry_iso4217_all_entries.csv')
a=Counter(特徵(r['state'],r['raw_xml']) for r in 舊幣);b=Counter(特徵('CURRENT' if r['狀態中譯']=='現行' else 'HISTORICAL',r['來源XML']) for r in 幣)
結=json.loads((工作/'核查結果.json').read_text(encoding='utf-8'));結.update({'市場全部欄位差異記錄數':len(差),'未關聯貨幣實體名稱數':len({r['來源實體名稱原值'] for r in 未}),'貨幣來源多重集合新增行':sum((b-a).values()),'貨幣來源多重集合未見舊行':sum((a-b).values()),'市場營運分段分布':dict(Counter(r['營運或分段原值'] for r in 市))})
(工作/'核查結果.json').write_text(json.dumps(結,ensure_ascii=False,indent=2),encoding='utf-8')
報='''---
title: "第七十一批：全球貨幣與市場識別碼全量續核"
lang: zh-TW
format: html
---

本輪核對最新提交及接續清單，轉回全球金融資料。另存官方完整下載，不覆寫舊資料庫、前批清單或使用者報告。國家／地區母表取現有完整表，實際讀取行數，不把249設定為歷史政治實體的總量上限。

## 完整來源接收與對賬

'''+f"- 現有國家／地區母表：{結['國家地區母表行數']} 行，全部納入本輪覆蓋表。\n- 現行貨幣與基金：{結['現行貨幣來源行']} 行；唯一非空字母代碼 {結['現行唯一非空字母代碼']} 個。\n- 歷史貨幣與基金：{結['歷史貨幣來源行']} 行。\n- 市場識別碼：{結['市场代碼來源行']:,} 行，涉及 {結['市場國家地區代碼數']} 個來源國家／地區代碼。\n- 未可靠關聯至母表的貨幣來源記錄：{結['貨幣來源實體未關聯行']} 行、{結['未關聯貨幣實體名稱數']} 個來源名稱，全部另表保留。\n\n"+'''[SIX（瑞士金融基礎設施集團）維護的ISO 4217貨幣表](https://www.six-group.com/en/products-services/financial-information/market-reference-data/data-standards.html)原始版本日期：現行表2026年9月17日、歷史表2026年1月1日。本次取得日期是2026年10月12日；取得日期不取代來源發布日期。

[ISO 10383市場識別碼官方發布頁](https://www.iso20022.org/market-identifier-codes)本次仍展示2026年9月14日發布、9月28日實施、10月12日下次發布的時程；不因今日是預定發布日，就宣稱10月份版本已取得。

'''+f"市場狀態原值分布：ACTIVE（來源標記有效）{結['市場狀態分布'].get('ACTIVE',0)}、EXPIRED（來源標記失效）{結['市場狀態分布'].get('EXPIRED',0)}、UPDATED（來源標記更新）{結['市場狀態分布'].get('UPDATED',0)}。這些狀態不是本輪實測營業或監管資格。\n\n市場全部來源欄位與既有第六批對照，差異 {結['市場全部欄位差異記錄數']} 條；貨幣來源多重集合與原第三批對照，新增 {結['貨幣來源多重集合新增行']} 行、未見舊行 {結['貨幣來源多重集合未見舊行']} 行。零差異只表示這次源表與指定基線一致，不是全球金融活動沒有變動。\n\n"+'''## 業務定義與完整性邊界

貨幣表的一行是「來源實體—貨幣／基金」關係，同一代碼可以出現多次；字母代碼包括基金、貴金屬、測試或無貨幣等用途，不能當作日常流通貨幣種類總數。ISO歷史表也不等於人類文明所有地方、古代及非ISO貨幣。

MIC（市場識別碼）識別交易場所、交易平台、分段或報告設施；營運代碼與分段代碼不等於不同公司，更不等於證券行或上市公司總数。保留有效、失效及更新狀態，不刪歷史行。來源未列市場的國家／地區不推定沒有金融市場。

貨幣名稱關聯沿用既有對照，不把編輯對照升级為ISO官方逐國關聯。未匹配行完整保留。中文區域與貨幣名称參考 [Unicode CLDR（通用區域資料庫）](https://github.com/unicode-org/cldr-json)，原名稱並存；市場與法定實體名稱中譯仍逐項待校，不編造中譯或取代法定原名。

## 尚未竣工與接續施工

逐國覆蓋表保留全部母表行及上市公司、券商、所有貨幣的待完成狀態；本輪沒有宣稱收齊每家公司。下一步優先逐項校核未關聯來源名稱、歷史政治實體與基金專用實體的區別，再按實際交易所及監管名冊補齊公司與持牌券商，對賬來源總量和分頁，不以市場識別碼代替名冊。

逐用途授權、全球各家公司的完整性及人類歷史所有貨幣仍待核實。完整原始回應、取得時間、標頭及SHA256（安全雜湊算法）保存在 `reports/2026-10-12/全球貨幣與市場代碼全量續核_B71/`；所有來源欄位及逐國覆蓋見 `tables/93_全球貨幣與市場代碼全量續核_B71_20261012/`。
'''
(根/'Reference/全球貨幣與市場代碼全量續核_B71_20261012.qmd').write_text(報,encoding='utf-8')
主='Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd';原=(根/主).read_bytes()
附=('\n\n## 第七十一批有界增補：全球金融標準母表續核\n\n全量接收280條現行貨幣與基金、169條歷史記錄、2,883條市場識別碼，全部249行現有國家／地區母表納入覆蓋表。42條貨幣來源記錄尚未可靠關聯，另表完整保留。市場代碼不等於上市公司或券商；歷史ISO貨幣表不等於所有歷史貨幣。來源版本與取得日期分列，未宣稱全球已竣工。詳見[第七十一批報告](全球貨幣與市場代碼全量續核_B71_20261012.qmd)。\n').encode('utf-8')
(根/主).write_bytes(原+附)
(工作/'附加收據.json').write_text(json.dumps({'主報告':主,'原文位元組':len(原),'原文雜湊':H(原),'附加雜湊':H(附)},ensure_ascii=False,indent=2),encoding='utf-8')
for d,t in {'redteam':'市場代碼、分段與法定實體不能混成券商或上市公司總數。','critic':'完整接收標準表不等於收齊全球名冊；全部249行覆蓋表保留待完成狀態。','killcritic':'全來源欄位、多重集合對照與原始雜湊提供可重現證據；不隱藏零差異或未匹配行。','blindspot':'42條未關聯來源記錄可能涉及歷史政治實體、基金專用名稱或名稱差異，須逐項核實。','blueprint':'來源實體、貨幣代碼、交易場所、法定公司及監管資格分表，透過有證據的關聯連接。','cheatsheet':'280條現行來源關係、169條歷史關係、2,883條MIC；不直接當作貨幣種類或公司數。','actionplan':'先核實35個未匹配來源名稱，再逐交易所／監管名冊全量對賬公司與券商；保留全部國家／地區工作。'}.items():
    (根/d/'全球貨幣與市場代碼全量續核_B71_20261012.md').write_text('# 第七十一批核查筆記\n\n'+t+'\n\n[報告](../Reference/全球貨幣與市場代碼全量續核_B71_20261012.qmd)。\n',encoding='utf-8')
print(json.dumps(結,ensure_ascii=False))
