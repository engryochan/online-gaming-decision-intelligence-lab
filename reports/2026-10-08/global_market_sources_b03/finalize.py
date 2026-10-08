from pathlib import Path
import csv,json,sqlite3,hashlib,zipfile,io
from urllib.parse import urlparse

O=Path(__file__).parent;R=O.parents[2];T=R/'Reference/tables/28_global_market_sources_b03_20261008'
def read(name):return list(csv.DictReader((T/name).open(encoding='utf-8-sig')))
def write(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (T/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def host(url):return (urlparse(url).hostname or '').lower().removeprefix('www.')
wfe=read('registry_wfe_directory_entries.csv');valid_wfe={r['url'] for r in wfe if r['url']}
sources=read('registry_global_source_endpoints.csv');removed=[]
sources2=[]
for r in sources:
    if r['discovery_kinds']=='WFE_DIRECTORY_SITE' and r['url'] not in valid_wfe:
        removed.append(dict(url=r['url'],reason='FOOTER_LINK_OUTSIDE_BOUNDED_MEMBERSHIP_SECTION'));continue
    sources2.append(r)
sources={r['url']:r for r in sources2}
regulators=read('registry_iosco_members_source_entries.csv')
for r in regulators:
    for url in json.loads(r['websites_json']):
        if url not in sources:
            sources[url]=dict(url=url,discovery_kinds='IOSCO_MEMBER_WEBSITE',provenance_json=json.dumps([dict(category=r['category'],page=r['page'],source_row=r['source_row'],source_url=r['source_url'])]),evidence='DISCOVERED_NOT_FULL_DIRECTORY_VERIFIED')
        elif 'IOSCO_MEMBER_WEBSITE' not in sources[url]['discovery_kinds']:
            sources[url]['discovery_kinds']+='|IOSCO_MEMBER_WEBSITE'
write('registry_global_source_endpoints.csv',sorted(sources.values(),key=lambda r:r['url']))
write('source_boundary_exclusions.csv',removed)
checks=read('registry_endpoint_live_checks.csv')+read('registry_regulator_endpoint_checks.csv')
by_url={r['url']:r for r in checks if r['url'] in sources}
assert set(sources)<=set(by_url), 'Unprobed endpoint retained in final registry'
write('registry_all_endpoint_checks.csv',[by_url[u] for u in sorted(sources)])
relations=read('registry_all_MIC_source_relations.csv');country_sites={}
for r in relations:
    if r['url']:country_sites.setdefault(host(r['url']),set()).add(r['country_iso'])
tasks=[]
for url,r in sorted(sources.items()):
    tasks.append(dict(url=url,discovery_kinds=r['discovery_kinds'],country_candidates='|'.join(sorted(country_sites.get(host(url),set()))),
                      required_work='FULL_LISTED_ISSUER_AND_SECURITY_DIRECTORY;FULL_MEMBER_OR_LICENSEE_DIRECTORY;SOURCE_TOTAL_AND_PAGINATION_RECONCILIATION;ISIN_LEI_MIC_LINKING',
                      applicability='REVIEW_MARKET_TYPE_AND_REGULATORY_ROLE_NOT_EVERY_SITE_IS_EQUITY_EXCHANGE',
                      http_status=by_url[url].get('http_status',''),completeness='UNKNOWN',
                      business_value='AUTHORITATIVE_UNIVERSE_BOUNDARY_AND_ENTITY_IDENTIFICATION',
                      access_action='LICENSE_OR_PUBLIC_EXPORT_SCOPE_REVIEW' if 'LICENSED_VENDOR' in r['discovery_kinds'] else 'PUBLIC_DIRECTORY_DISCOVERY_AND_FULL_EXPORT'))
write('registry_source_collection_workqueue.csv',tasks)
country=read('registry_all_country_source_coverage.csv')
assert len(country)==249 and len({r['iso_alpha2'] for r in country})==249
assert len(relations)==2883 and len({r['MIC'] for r in relations})==2883
pages=read('iosco_category_fetch_manifest.csv')
assert all(r['http_status']=='200' and r['truncated']=='False' for r in pages)
assert sum(int(r['entries']) for r in pages)==len(regulators)
members=read('registry_additional_source_records.csv')
archive=zipfile.ZipFile(io.BytesIO((O/'raw/JSE_ISIN_FULL.response').read_bytes()))
assert sum(len(archive.read(n).splitlines()) for n in archive.namelist() if not n.endswith('/'))==len(members)==14782
db=O/'global_source_registry_b03.sqlite'
if db.exists():raise FileExistsError(str(db))
with sqlite3.connect(db) as con:
    for path in sorted(T.glob('*.csv')):
        rows=list(csv.DictReader(path.open(encoding='utf-8-sig')))
        if not rows:continue
        fields=list(rows[0]);table=path.stem
        con.execute('CREATE TABLE "'+table+'" ('+','.join('"'+f.replace('"','""')+'" TEXT' for f in fields)+')')
        con.executemany('INSERT INTO "'+table+'" VALUES ('+','.join('?' for _ in fields)+')',[[r[f] for f in fields] for r in rows])
    assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
summary=dict(date='2026-10-08',MIC_rows=len(relations),MIC_countries=len({r['country_iso'] for r in relations}),
    country_mother_rows=len(country),source_endpoints=len(sources),checked_endpoints=len(by_url),
    endpoint_HTTP_200=sum(r.get('http_status')=='200' for r in by_url.values()),WFE_entries=len(wfe),
    IOSCO_entries=len(regulators),IOSCO_pages=len(pages),JSE_source_lines=len(members),
    preservation_scope='ADDITIVE_NEW_OUTPUTS_OLD_SOURCE_FILES_NOT_WRITTEN',global_company_completeness='UNKNOWN',all_websites_enumerated=False,
    interrupted_pending_responses=sum(r.get('status')=='INTERRUPTED_PENDING_RESPONSE' for r in by_url.values()))
(O/'final_acceptance.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
qmd=R/'Reference/Global_Market_Source_Coverage_B03_20261008.qmd'
assert not qmd.exists()
body=f'''---
title: "全球金融來源擴展與 Euronext 採集範圍審核 B03"
date: 2026-10-08
lang: zh-Hant
format:
  html:
    toc: true
    embed-resources: true
execute:
  enabled: false
---

## 為何上一輪集中於 Euronext

既有採集並非僅 Euronext。已核對第19至25批來源清單：Nasdaq Trader、JPX、HKEX、ASX、TMX、NZX、TWSE、TPEX、ESMA、日本 FSA、ISO 與 SIX 均有來源記錄。B02 的 `fetch.py` 同時嘗試 Euronext、巴西 CVM 與 Seshat；CVM 與 Seshat 回應403，Euronext 名冊可下載，因此該批新增金融記錄集中於 Euronext。這是該批可成功交付的來源範圍，不能推論全球只有此一交易所，也不能證明其他市場已完整覆蓋。過去交付摘要未充分呈現跨批來源與缺口，本輪改為逐站登記及全球對賬。

相關歷史清單見 [既有採集來源審核](tables/28_global_market_sources_b03_20261008/prior_collection_source_audit.csv)。B02來源紀錄保留於 `reports/2026-10-07/global_expansion_b02/source_manifest.json`，舊報告、舊資料庫與原始宇航比較報告均未覆寫。

## 本轮實測與保存

|項目|本輪記錄數|可證明的範圍|
|---|---:|---|
|ISO10383 MIC|{len(relations)}|官方公開版本全部行，含各類市場與失效狀態|
|現行國家／地區母表|{len(country)}|逐項保留來源覆蓋與缺口|
|全球來源端點|{len(sources)}|全部已嘗試HTTP連線，並非全部名冊下載完畢|
|HTTP200端點|{summary['endpoint_HTTP_200']}|僅連線結果，不代表頁面內容有效或名冊完整|
|WFE頁面來源項|{len(wfe)}|有界會員區塊的命名項，保留缺少網站的項目|
|IOSCO三類會員來源項|{len(regulators)}|追蹤所有發現頁碼，共{len(pages)}頁，原始條目完整保存|
|南非JSE完整ISIN檔|{len(members)}行|完整壓縮檔及逐行來源資料，尚未核定欄位／唯一公司數|

ISO官方檔本輪下載成功，SHA256與2026-10-07保存版本一致；沒有把舊檔當成新版本。MIC涵蓋交易所、交易平台及報價申報設施，並非上市公司或證券行名單。[ISO官方名錄](https://www.iso20022.org/market-identifier-codes)。WFE為交叉檢查來源，不把其會員當成全球全部市場。[WFE官方名錄](https://www.world-exchanges.org/membership-events)。IOSCO會員包含監管及其他類別組織，不能把246項全稱為國家監管局。[IOSCO官方會員頁](https://www.iosco.org/about/?subsection=membership)。

## 資料表與業務定義

- [全部MIC與網站關係](tables/28_global_market_sources_b03_20261008/registry_all_MIC_source_relations.csv)：保留市場識別、國別、類型、狀態和原始網站；沒有網站的項目仍保留。
- [全球端點登記](tables/28_global_market_sources_b03_20261008/registry_global_source_endpoints.csv)：ISO、WFE、IOSCO、既有直接採集及補充商業來源的聯集；逐項保留發現依據。
- [全部連線結果](tables/28_global_market_sources_b03_20261008/registry_all_endpoint_checks.csv)：原URL、最終URL、狀態碼、時間、觀測內容雜湊與截斷資訊；網路錯誤不混稱網站封鎖。
- [249項逐國覆蓋](tables/28_global_market_sources_b03_20261008/registry_all_country_source_coverage.csv)：無MIC來源的國家列缺口，不能推論沒有市場、券商或貨幣。
- [逐站採集工作](tables/28_global_market_sources_b03_20261008/registry_source_collection_workqueue.csv)：完整公司／證券、會員／牌照、分頁／總數核對及識別碼串接；依市場類型再核定適用性。
- [IOSCO原始會員條目](tables/28_global_market_sources_b03_20261008/registry_iosco_members_source_entries.csv)：保留分類、頁码、行号、全文與原HTML片段；國家／組織標準化仍待審閱。
- [JSE來源全部行](tables/28_global_market_sources_b03_20261008/registry_additional_source_records.csv)：完整固定寬度文字行；原始位元組在壓縮檔中保留，不將ISIN總行數稱為公司總數。

Bloomberg、LSEG、FactSet、S&P Global、MSCI、ICE及Moody’s Orbis等商業資料來源列入補充候選端點，以評估資料授權、歷史深度、識別碼與交叉核對價值；沒有聲稱取得付費資料或證明它們涵蓋全球所有公司。官方名錄用於市場及監管边界；商業資料用於補充及交叉核對，兩者均保留來源與授權範圍。

## 未完成項與驗收

美國SEC ticker／exchange檔本輪實測403，失敗回應及雜湊已保存，沒有以零筆代替完整資料。JSE檔來自[官方下載頁](https://clientportal.jse.co.za/downloadable-files?RequestNode=%2FISIN%2FEquities)，還需取得欄位字典及確認證券種類、存續狀態、境外發行人、基金與歷史項目。

目前完成的是本輪已界定官方來源名錄與端點的擴展、逐站連線核查及新增完整檔的保存；仍未收齊全世界每家上市公司、證券行、每種貨幣或所有相關網站。HTTP200不能作為VERIFIED完整性判定；逐國三類完整性均維持UNKNOWN。歷史政治實體及史前組織保留既有登記與缺口，不以現行249項替代。

統一來源庫：`reports/2026-10-08/global_market_sources_b03/global_source_registry_b03.sqlite`。驗收：`reports/2026-10-08/global_market_sources_b03/final_acceptance.json`。全部MIC唯一碼、249母表唯一碼、IOSCO來源頁行數、JSE壓縮檔行數與SQLite完整性均已核對。連線回應最多觀測2MB，截斷回應的雜湊只代表觀測片段，並不聲稱保存完整網站。
'''
qmd.write_text(body,encoding='utf-8')
print(json.dumps(summary),flush=True)
