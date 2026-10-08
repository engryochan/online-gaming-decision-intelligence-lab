from pathlib import Path
from collections import Counter
import csv,json,hashlib,sqlite3
R=Path(__file__).resolve().parents[3];O=Path(__file__).parent;T=R/'Reference/tables/27_global_expansion_b02_20261007';s=json.loads((O/'validation.json').read_text());m=json.loads((O/'source_manifest.json').read_text());csv.field_size_limit(32*1024*1024)
gaps=[dict(source_file=x['file'],source_url=x['url'],HTTP_status=x['http_status'],status='NO_DATA_INGESTED_ACCESS_DENIED',gap='Public source attempt blocked; source absence does not imply no organizations or polities') for x in m if x['http_status']!=200]
with (T/'registry_source_access_gaps.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=list(gaps[0]));w.writeheader();w.writerows(gaps)
contracts=[dict(dataset='euronext_securities',row_grain='One source security listing row, not one legal issuer',business_value='Enumerate trading instruments and locate source market evidence',completion_rule='Full download count reconciled; national and legal-issuer coverage remains unresolved'),dict(dataset='euronext_members',row_grain='One exchange member record with source details and permission tables',business_value='Locate trading and clearing intermediaries for regulatory identity review',completion_rule='15 pages reconcile 292 rows; all national licensed brokers still UNKNOWN'),dict(dataset='historical_relationships',row_grain='One semicolon-separated Components or MemberOf token per source interval',business_value='Recover source-defined composite and membership relationships in time',completion_rule='Exact names and overlapping intervals locate candidates; substantive historical authority remains pending'),dict(dataset='historical_interval_gaps',row_grain='One unobserved interval inside one source-name sequence',business_value='Identify where continuous lifespan assumptions would invent evidence',completion_rule='Gaps are not evidence of absence; require independent regional historical sources'),dict(dataset='historical_currency_dates',row_grain='One historical ISO4217 source record with original withdrawal date',business_value='Separate code withdrawal chronology from actual circulation history',completion_rule='No inferred start date or automatic historical-polity identity; non-ISO and earlier currencies remain open'),dict(dataset='country_coverage',row_grain='One existing current mother-table country or area',business_value='Keep universal current coverage obligations while historical universe expands',completion_rule='249 current rows and 747 tasks retained; neither limits historical entity count')]
with (T/'dataset_business_definitions.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=list(contracts[0]));w.writeheader();w.writerows(contracts)
with (T/'registry_euronext_trading_members.csv').open(encoding='utf-8-sig') as f:members=list(csv.DictReader(f))
types=Counter('; '.join(json.loads(r['source_detail_fields_json']).get('Type',[])) for r in members)
body=f'''---
title: "全球全集增補 B02：Euronext 全量金融名冊、歷史政治關係及貨幣日期"
date: 2026-10-07
format:
  html:
    toc: true
---

## 本輪實際交付

研究範圍持續包括全部現行國家／地區及有證據的歷史政治實體，不以249作歷史總數上限。新增Euronext股票來源{s['euronext_security_records']:,}列及全量會員{s['member_records']}列；統一快照v5保留v4全部金融原始列、上市來源列、MIC、ESMA公司與活動，並收進歷史v1的全部{s['historical_features_retained']:,}份完整未簡化疆域feature及COW原始列。舊資料庫均保留。

累計上市工具／公司目錄來源{s['total_listing_records']:,}列、原始資料表列{s['total_raw_records']:,}列；不是唯一公司或唯一券商總數。來源中可能包含同一公司多種證券、多市場交易、外國股票、已失效登記與不同時段，仍須依法律身份和有效日期消歧。

## Euronext 全部股票與市場範圍

下載入口由[官方全部股票頁](https://live.euronext.com/en/products/equities/list)的實際drupalSettings.jsongateway_download取得，完整CSV有3,834條證券列及3條標題／日期／數據時點附註。證券列數與目錄回應iTotalRecords及iTotalDisplayRecords均為3,834，附註全部另存，没有當成公司。下載標示2026年10月7日，數據截至最後活躍交易日結束；不當作全部價格均為即時值。

2,793個不同ISIN仍不是法律公司數；ISIN亦未逐項向發碼機構核實。32種來源市場標籤包括跨市场組合，以及Global Equity Market、EuroTLX與Trading After Hours；不能把全部當成當地公司的首次上市。

市場標籤與既有MIC來源的對照是明示候選，尚待逐項核實。下表計算一條來源列涉及的候選交易市場所在地；多地交易會重複計數，不是發行人國籍或每國所有公司。

| 候選市场所在地 | 來源列關聯數 |
|---|---:|
'''
for code,count in sorted(s['candidate_market_country_counts'].items()):body+=f'| {code} | {count:,} |\n'
body+='''
官方普通目錄回應僅提供20條畫面預覽；本輪未拿它冒充全量資料。另按官方腳本嘗試POST全目錄時回應總數為null、資料為空，已保留原始回應；因此驗收依據是完整CSV與目錄總數一致，尚未完成兩套全量來源逐ID比對。保留所有CSV欄位及原檔，沒有用預覽資料取代全表。

## 全部交易所會員

[官方會員頁](https://live.euronext.com/en/resources/members-list)實際嵌入公開會員表。15頁對賬292條，名稱字串亦為292個；每頁Displaying總數均一致，所有主列、詳細欄位及權限子表原HTML完整保留。會員名稱唯一不等於法律身份已核實。

'''
body+='| 來源會員類型字串 | 記錄數 |\n|---|---:|\n'
for typ,n in sorted(types.items()):body+='| '+typ.replace('|','／')+f' | {n} |\n'
body+='''
地址文字沒有自動當作公司註冊國，會員記錄也沒有直接當作各國所有持牌證券行；交易／清算角色、不同市場權限與監管身份分别保留。未加入會員頁指向的獨立Athens名冊，因此不宣稱集團所有場所均已涵蓋。

## 歷史政治關係、年代與勢力圖邊界

從13,797份原始feature的Components及MemberOf欄位抽出9,345個分號分隔關係項，保留原字串。所有項目都能找到同名且年代相交的来源feature候選；候選定位不等於從屬、控制或聯盟关系已獨立核實，也不推定軍力強弱。RELATION層與POLITY層保留來源類型。

同名來源序列沒有相交的時段，但有427段內部未觀測區間；其中的政體是否持續存在需查其他來源，不能以最早／最晚年填滿，也不能以空窗推定滅亡。保留[上一批年代疆域圖](Historical_Polities_Timeline_Map_B01_20261007.html)，本輪不重繪未知政治勢力邊界。

Cliopatria來源覆蓋公元前3400年至2024年；年代更早至數萬年前、2025年至今，以及未納入來源的實體仍待逐區考古與歷史證據增補。此次Seshat在線政體目錄下載實測403，沒有把搜尋摘要當成已接收864條來源。考古文化、聚落、城邦、帝國與現代國家不能機械等同；所有存在過的國家總數仍UNKNOWN。

## 全部貨幣與現行國家工作的延續

保留既有449條現行／歷史ISO4217來源，展開其中169條歷史貨幣原始撤銷日期及日期精度。日期文字不合單一YYYY-MM形式者標為待核實；未知起始日期、歷史政體身份及實際流通範圍均維持UNKNOWN。ISO代碼撤銷不等於貨幣開始／停止在所有地方使用，也不包含所有古代貨幣及交換媒介。

全部249條現行母表記錄及747項上市公司／證券行／貨幣工作保留，新增市場候選證據後仍為OPEN。上批聯合國M49實測248列、項目母表249列的差異原資料保留；不能將M49範圍差異當成刪除TW或已量得ISO官方現行全集的證據。

巴西[CVM公司目錄](https://dados.cvm.gov.br/dataset/cia_aberta-cad)及下載CSV／字典均實測403，沒有接收公司列。所有國家的全部公司、券商和所有貨幣未因本批接收而宣稱收齊；沒有來源不表示不存在。

## 資料、業務定義與驗收

'''
for p in sorted(T.glob('*.csv')):body+=f'- [{p.name}](tables/{T.name}/{p.name})\n'
body+='\n- [統一快照v5](../reports/2026-10-07/global_expansion_b02/global_universe_v5.sqlite)\n- [來源指紋](../reports/2026-10-07/global_expansion_b02/source_manifest.json)與[數量／保留驗收](../reports/2026-10-07/global_expansion_b02/validation.json)\n\n來源列、原始幾何及舊金融資料逐列保留驗收通過，SQLite完整性通過；這不等於各個歷史或法律主張皆已VERIFIED。各資料表的記錄粒度、用途及完成條件分別寫入業務定義表，沒有以表行數充當業務價值或全球完整度。\n'
p=R/'Reference/Global_Universe_Expansion_B02_20261007.qmd';assert not p.exists();p.write_text(body,encoding='utf-8')
q={'listing_sources':'SELECT namespace,COUNT(*) FROM listing_records GROUP BY namespace','members':'SELECT COUNT(*) FROM euronext_trading_members','historical_features':'SELECT source_type,COUNT(*) FROM historical_feature_snapshots GROUP BY source_type','historical_relationships':'SELECT COUNT(*) FROM historical_source_relationships','historical_gaps':'SELECT COUNT(*) FROM historical_interval_gaps','currency_chronology':'SELECT COUNT(*) FROM historical_currency_withdrawal_dates','country_tasks':'SELECT stream,COUNT(*) FROM country_workstreams GROUP BY stream'}
c=sqlite3.connect(O/'global_universe_v5.sqlite');results={k:c.execute(v).fetchall() for k,v in q.items()};c.close();assert results['members']==[(292,)] and results['historical_relationships']==[(9345,)] and all(x[1]==249 for x in results['country_tasks']);(O/'query_acceptance.json').write_text(json.dumps(results,indent=2)+'\n');(O/'queries.sql').write_text('\n'.join('-- '+k+'\n'+v+';' for k,v in q.items())+'\n')
template=R/'reports/2026-10-07/historical_polities_b01/append_index.py';x=template.read_text(encoding='utf-8');a=x.index('addition=');b=x.index('\nsaved=',a);addition='\n\n<!-- GLOBAL_EXPANSION_B02_20261007 -->\n\n## 全球金融與歷史關係增補 B02\n\n[本輪全量名冊與時序檢查](Global_Universe_Expansion_B02_20261007.qmd)接收Euronext 3,834條股票工具與292條會員記錄，逐頁對賬；保留全部歷史feature，展開9,345個來源政治關係、427段未觀測時段及169條歷史貨幣日期。v5保留舊金融與歷史資料，現行747項工作及史前缺口仍OPEN。\n';x=x[:a]+'addition='+repr(addition)+x[b:];x=x.replace("marker='HISTORICAL_POLITIES_B01_20261007'","marker='GLOBAL_EXPANSION_B02_20261007'");(O/'append_index.py').write_text(x,encoding='utf-8')
manifest=[dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(T.glob('*.csv'))]
with (T/'integration_input_manifest.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=['path','sha256']);w.writeheader();w.writerows(manifest)
print('Report, source gaps, business definitions, queries and append helper created')
