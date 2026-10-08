from pathlib import Path
import csv,json,sqlite3,hashlib,collections,subprocess
from urllib.parse import urlparse
O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/29_global_market_directories_b04_20261008'
def read(name):return list(csv.DictReader((T/name).open(encoding='utf-8-sig')))
def write(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
checks=read('registry_all_host_directory_discovery.csv')+read('registry_anna_new_host_checks.csv')
links=read('registry_observed_directory_links.csv')+read('registry_anna_observed_directory_links.csv')
assert len({r['host'] for r in checks})==len(checks)==1502
expected=list(csv.DictReader((R/'Reference/tables/28_global_market_sources_b03_20261008/registry_global_source_endpoints.csv').open(encoding='utf-8-sig')))
assert {urlparse(r['url']).hostname for r in expected}<={r['host'] for r in checks}
work=collections.defaultdict(list)
for row in links:work[row['target_url']].append(row)
tasks=[]
for url,rows in sorted(work.items()):
    tasks.append(dict(target_url=url,discovery_hosts='|'.join(sorted({r['host'] for r in rows})),source_observation_count=len(rows),
        source_observations_json=json.dumps(rows,ensure_ascii=False),business_value='DIRECTORY_EXPORT_DISCOVERY_AND_UNIVERSE_BOUNDARY',
        action='REVIEW_ROLE_THEN_FETCH_ALL_PAGES_AND_SOURCE_TOTAL;CLASSIFY_COMPANY_SECURITY_MEMBER_LICENSEE_OR_FORM',
        completeness='UNKNOWN',status='OBSERVED_LINK_REQUIRES_CONTENT_VALIDATION'))
write('registry_all_directory_collection_workqueue.csv',tasks)
known={r['host'] for r in checks};next_hosts=collections.defaultdict(list)
for row in links:
    host=urlparse(row['target_url']).hostname
    if host and host not in known:next_hosts[host].append(row)
write('registry_new_linked_host_review.csv',[dict(host=h,link_observations=len(rows),source_links_json=json.dumps(rows,ensure_ascii=False),
    decision='REVIEW_RELEVANCE_EXTERNAL_HOST_NOT_AUTOMATICALLY_FINANCIAL_SOURCE') for h,rows in sorted(next_hosts.items())])
for row in read('prior_ISIN_input_manifest.csv'):
    assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256']
assert not subprocess.check_output(['git','diff','--name-only'],cwd=R).strip()
db=O/'global_directory_registry_b04.sqlite'
assert not db.exists()
with sqlite3.connect(db) as con:
    for path in sorted(T.glob('*.csv')):
        rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))
        if not rows:continue
        fields=list(rows[0]);table=path.stem
        con.execute('CREATE TABLE "'+table+'" ('+','.join('"'+f.replace('"','""')+'" TEXT' for f in fields)+')')
        con.executemany('INSERT INTO "'+table+'" VALUES ('+','.join('?' for f in fields)+')',[[r[f] for f in fields] for r in rows])
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
summary=dict(source_endpoints_covered=len(expected),host_checks=len(checks),original_hosts=1434,new_ANNA_hosts=68,
    observed_directory_links=len(links),unique_directory_targets=len(tasks),next_host_review=len(next_hosts),
    HTTP200_hosts=sum(r.get('http_status')=='200' for r in checks),
    ANNA_source_rows=259,ANNA_source_website_rows=125,ANNA_country_mother_rows=249,ANNA_exact_prefix_country_matches=247,
    JSE_source_records=14782,JSE_unique_ISINs=14743,JSE_name_groups=401,PSX_online_broker_snapshot_rows=77,
    direct_files_downloaded=4,CSV_XLSX_physical_rows=3592,PSX_archive_workbook_rows=78,
    source_files_retained=True,existing_tracked_content_changes=[],global_full_coverage=False)
(O/'final_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
qmd=R/'Reference/Global_Market_Directory_Expansion_B04_20261008.qmd';assert not qmd.exists()
qmd.write_text(f'''---
title: "全球市場名錄搜尋、ANNA來源補齊與證券識別整合 B04"
date: 2026-10-08
lang: zh-Hant
format:
  html:
    toc: true
    embed-resources: true
execute:
  enabled: false
---

## 本輪範圍與成果

承接B03的全部1,653個來源端點，本輪按主機展開，不僅挑選Euronext或少數大型交易所。所有1,434個既有主機均已嘗試官方首頁名錄搜尋；ANNA新增68個主機也全部納入，共 **1,502個主機**。每個來源端點與主機的關係保留在資料表，不因同一主機合併查詢而刪除端點。

共保留 **{len(links):,}條候選連結觀測、{len(tasks):,}個不同目標URL**，涵蓋上市、發行人、證券、會員、參與者、券商、牌照、名錄、下載等文字及URL線索。共有{summary['HTTP200_hosts']}個主機回應HTTP200，這不是完整名冊數；連結也可能是申請表、報價申報、技術文檔或其他服務，必須再核對內容。已將{len(next_hosts)}個新增外部主機列為相關性審閱項，不自動認定全部屬於金融來源。

本輪僅新增文件，既有報告、CSV、HTML、原始宇航報告及資料庫未覆寫。前一輪已收錄Nasdaq、JPX、HKEX、ASX、TMX、NZX、ESMA等官方來源，本轮並非以Euronext替代它們。所謂頂尖、高端來源，採取官方權責、識別標準、完整名冊、可追溯性及授權價值等可審查條件，不杜撰全球網站排名。

## 全球ANNA來源與國家缺口

已從[ANNA官方名錄](https://anna-web.org/anna-members/)保存全部 **259條來源列**，包含機構、轄區、ISIN前綴、會員狀態、網站與替代編號機構，另保留125條有網站的來源列。逐項核對249項現行母表，有247項存在相同前綴，兩項没有相同前綴：LU及BQ。

ISIN前綴與政治國家、發行人住所及上市地不是同一概念。Luxembourg的轄區文字可另行對照XS來源；BQ與舊AN或替代機構的責任關係仍待正式證據確認，沒有自動改寫國別。EZ、XT、EU、XK及Global等特殊或不同範圍項目仍保留，不能為湊249而刪除。

來源頁面宣告120家完整會員，但來源表實際有119條Member、5條Partner、2條currently suspended、132條Other及1條Association，已保留不一致與日期／狀態待審問題，沒有悄悄改數。這些是編號服務來源，不是每家證券行或每家上市公司名錄。

## JSE完整来源的欄位化與跨來源對照

前一輪下載的JSE完整ISIN壓縮檔全部14,782行均保留。本轮形成ISIN、發行人名稱、證券描述、完整原始行及未解析尾部的可分析表；14,782行校驗碼皆通過，有14,743個不同ISIN、401個名稱群組及39個重複ISIN群組。重複來源行仍保留，名稱群組不能稱為401家上市公司。

[官方舊欄位說明](https://www.jse.co.za/sites/default/files/media/documents/2020-11/ISIN%20Equities%20Record%20Structure.pdf)的前3欄合計178字節，可與來源切分對照；完整舊格式合計286字節，而實際每行277字節，PDF本輪下載回應403，故完整欄位定義尚未核定。尾部99字節不猜測、不刪除。文字採可逆Latin-1位元組映射，原始編碼仍待核定。校驗碼按[ANNA識別規則](https://anna-web.org/identifiers/)檢查，只證明格式一致，不證明存續上市狀態。

已對照既有3份具ISIN欄位的來源表、25,918行，形成14條精確ISIN關係觀測，涉及9條JSE來源行。保留原表行號及完整來源行；ISIN相同仅作證券識別匹配，不據此合併公司或宣告雙重上市。

## 全部直接資料檔候選的採集

本輪在觀測範圍內發現4個直接CSV／Excel／ZIP候選，全部下載並保存雜湊：Bloomberg APA公開CSV、Euronext FX成交量Excel、ICEX會員GST申請格式及PSX網上券商ZIP。前三檔全部15、3,571、6行均保留，共3,592行，不把交易資料或空白申請表誤算為公司／券商。

PSX壓縮檔內的Excel全部78行保留，另形成 **77條網上券商來源記錄**，包含會員代碼、名稱、來源狀態、地址、電話、電郵及網站。來源文件名日期為2024-08-13，不能當成2026年完整有效牌照名冊；當前授權狀態與巴基斯坦全部券商覆蓋仍為UNKNOWN。原始工作簿公式及欄位在來源行JSON與壓縮檔內保留。

## 交付與下一步工作定位

- [全部主機搜尋](tables/29_global_market_directories_b04_20261008/registry_all_host_directory_discovery.csv)及[ANNA新增主機核查](tables/29_global_market_directories_b04_20261008/registry_anna_new_host_checks.csv)：成功、HTTP錯誤與網路例外分開保留。
- [全部候選名錄工作](tables/29_global_market_directories_b04_20261008/registry_all_directory_collection_workqueue.csv)：逐URL保存所有觀測來源、業務價值及內容／分頁／總數驗證工作。
- [ANNA全部來源列](tables/29_global_market_directories_b04_20261008/registry_anna_prefix_numbering_agency_source.csv)、[逐國覆蓋](tables/29_global_market_directories_b04_20261008/registry_all_country_anna_coverage.csv)及[語義差異審閱](tables/29_global_market_directories_b04_20261008/registry_anna_semantic_review.csv)。
- [JSE逐行欄位化](tables/29_global_market_directories_b04_20261008/registry_jse_isin_structured_partial.csv)、[重複ISIN審閱](tables/29_global_market_directories_b04_20261008/registry_jse_duplicate_ISIN_review.csv)及[既有來源對照](tables/29_global_market_directories_b04_20261008/registry_jse_prior_ISIN_matches.csv)。
- [PSX券商來源快照](tables/29_global_market_directories_b04_20261008/registry_psx_online_broker_snapshot.csv)及[完整工作簿行](tables/29_global_market_directories_b04_20261008/registry_psx_online_broker_all_workbook_rows.csv)。

統一增補庫為 `reports/2026-10-08/global_market_directories_b04/global_directory_registry_b04.sqlite`。本輪完成主機集合覆蓋、來源行對賬、舊來源雜湊核查及SQLite完整性驗收。

搜尋僅觀測每站首頁最多131,073字節；JavaScript產生、深層頁面、會員登入、付費授權、其他語言或沒有關鍵字的來源仍可能遺漏。候選連結不等於已取得完整名冊，頂尖商業資料也未聲稱已購得。下一步依全部URL工作表核對名錄內容、完整分頁及公告總數，同時持續擴展官方／編號／監管來源。全球每家上市公司、證券行、每種貨幣與所有相關網站仍未全部核實；現行與歷史政治實體的既有缺口均保留，禁止以本輪成功樣本宣告全球完成。
''',encoding='utf-8')
print(json.dumps(summary),flush=True)
