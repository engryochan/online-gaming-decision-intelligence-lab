from pathlib import Path
import json,csv
O=Path(__file__).resolve().parent;R=O.parents[2];T=R/'Reference/tables/59_pending_recheck_b35_20261009'
s=json.loads((O/'validation_receipt.json').read_text(encoding='utf-8'))
url='https://www.weathercompany.com/weather-data-apis/weather-data-apis-packages-pricing/'
claims=[('STANDARD_PRICE','Standard: USD500/month, annual plan, 1 million calls/month','OFFICIAL_PAGE_PRICE_NOT_NEGOTIATED_INVOICE'),('TRIAL','30 days; 50K calls/day; 100 calls/minute; enterprise eligibility conditions apply','OFFICIAL_PAGE_OFFER_NOT_ACCOUNT_TEST'),('ENTERPRISE','Custom annual plan; additional products selected through sales','OFFICIAL_PAGE_CUSTOM_PRICE_UNKNOWN'),('MAJOR_AIRLINES','Major airlines require custom Enterprise plan','OFFICIAL_PAGE_PLAN_RULE'),('COUNTRY_COVERAGE','249-country product-level availability and accuracy not tested','UNKNOWN_NOT_DERIVED_FROM_GLOBAL_MARKETING')]
with (T/'registry_weathercompany_claim_recheck.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['claim_id','current_assessment','evidence_scope','source_url','review_date','evidence_type']);w.writeheader()
    for k,v,scope in claims:w.writerow(dict(claim_id=k,current_assessment=v,evidence_scope=scope,source_url=url,review_date='2026-10-09',evidence_type='OFFICIAL_PAGE_BROWSER_READ_THIS_BATCH' if k!='COUNTRY_COVERAGE' else 'UNRESOLVED_EXTERNAL_TEST_REQUIRED'))
# Add the late-created evidence table without rewriting the completed weather tables.
import sqlite3
con=sqlite3.connect(T/'pending_recheck_b35.sqlite');rows=list(csv.DictReader((T/'registry_weathercompany_claim_recheck.csv').open(encoding='utf-8-sig')));keys=list(rows[0]);con.execute('CREATE TABLE registry_weathercompany_claim_recheck ('+','.join('"'+k+'" TEXT' for k in keys)+')');con.executemany('INSERT INTO registry_weathercompany_claim_recheck VALUES ('+','.join('?' for k in keys)+')',[[r[k] for k in keys] for r in rows]);con.commit();assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert con.execute('SELECT COUNT(*) FROM registry_weathercompany_claim_recheck').fetchone()[0]==5;con.close()
s['sqlite_counts']['registry_weathercompany_claim_recheck']=5;(O/'validation_receipt.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text='''---
title: "B35：最新版待辦再核對與34站氣象品質續作"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 最新基線與清單再核對

依使用者確認，Untitled.qmd無需恢復。以92358bd及已提交的Inteligent／weather.com最新版為基線，所有原有追蹤QMD及MD指紋保持不變。全量重新讀取93份名稱含pending／queue／gap／remaining／actionplan／work_progress的追蹤CSV，逐表核算行數、狀態與SHA256；另保留11版行動清單正文。清單涵蓋本地已辨識的待辦表，並非宣稱所有正文中的隱含任務已自動識別。歷史版各自保留，不能累加成唯一任務總數。

最新B25金融全表仍有4849項原始工作：2146項HTTP200待內容／範圍核定、2608項尚未嘗試、90項下載或非200覆核、5項截斷內容覆核。HTTP200不是實體驗證或完整收錄。B24的2828項未嘗試數已被B25取代，僅留作歷史。工商6項仍為PENDING_ENTITY_EXTRACT；378條分頁缺口保持待範圍覆核。B23工作簿衍生CSV及SQLite的發布保留未解除，不以B24候選值未匹配當作全面安全證明。

全球歷史政治實體、上市公司、券商、貨幣及科技完整性仍未驗收；不得因單批通過就結案。SDG業務分析仍凍結。93份表的外部來源沒有全部重新訪問，本輪新鮮度欄明确標記NOT_REVALIDATED_THIS_BATCH；未重新核官方來源的任務只更新本地狀態，尚未繼續採集。

## HTML與附件待辦

核查152個追蹤HTML的同名QMD，其中151個已有QMD；剩餘 `reports/2026-10-07/listed_universe_b04/raw/asx_directory.html` 是ASX下載原件，不是本項目報告成品。保留原始資料，沒有把下載頁偽稱作者源稿。同名QMD存在只證實路徑存在，本輪未重測151件渲染的逐字或位元組等價。B34指明的授權CSV未找到仍待獨立重建；已內嵌的附錄正文保留。

## 已核最新證據後接續的工作

重新下載 [NOAA GSOD官方說明](https://www.ncei.noaa.gov/data/global-summary-of-the-day/doc/readme.txt)，SHA256及完整位元組與B31來源一致，才將既有12欄單位／哨兵值規則套用B33的11163站日。新長表133956行，26966項來源缺值留空，解析／非有限數覆核0項。34站逐日位置及溫度極值窗口核查觸發0日；這僅表示未觸發本輪規則，不是資料真值或全球模型能力證明。

4676站日具有來源D／F／G降水報告窗口，其他記錄維持窗口未建立／不完整／缺值狀態；24小時窗口不保證本地午夜日。位置1公里是工程覆核參數，非NOAA認證標準。單位轉換保留原值及屬性，不提升量測精度。B33的1281個未觀測站日不補零、不覆寫原檔。

亦重新閱讀 [The Weather Company官方定價頁](https://www.weathercompany.com/weather-data-apis/weather-data-apis-packages-pricing/)，核對Standard公開價及年約額度、試用限制、Enterprise客製與大型航空公司方案規則。這支持公開報價，不是成交價、已開通API或249地區實測覆蓋；其餘所有權、客戶、模型、授權與產業主張未在本輪一律核實，不改寫原文。

## 可對賬交付

[93份清單再核對](tables/59_pending_recheck_b35_20261009/registry_all_queue_file_rechecks.csv)、[最新版待辦對照](tables/59_pending_recheck_b35_20261009/registry_current_unfinished_task_reconciliation.csv)、[行動清單歷史](tables/59_pending_recheck_b35_20261009/registry_actionplan_source_inventory.csv)、[HTML源檔核對](tables/59_pending_recheck_b35_20261009/registry_all_tracked_html_source_recheck.csv)、[新站變數長表](tables/59_pending_recheck_b35_20261009/registry_new_station_normalized_values.csv)、[逐日品質](tables/59_pending_recheck_b35_20261009/registry_new_station_daily_quality.csv)、[34站摘要](tables/59_pending_recheck_b35_20261009/registry_new_station_quality_summary.csv)、[供應商主張核對](tables/59_pending_recheck_b35_20261009/registry_weathercompany_claim_recheck.csv)、[SQLite](tables/59_pending_recheck_b35_20261009/pending_recheck_b35.sqlite)。

SQLite逐表行數、完整性、原始34檔來源雜湊、12欄乘積及所有既有QMD／MD指紋驗收通過。下一步先更新來源授權和模型評估的金標條件，再做持出年份／地區驗證；觀測資料不可當作歷史預報。金融與工商續作前仍須各自重新核對來源當期狀態。
'''
(R/'Reference/Pending_Recheck_B35_20261009.qmd').write_text(text,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:
    (R/n/'pending_recheck_b35_20261009.md').write_text('# '+n+'｜B35\n\n93份清單逐表再核對、11版行動清單保留；最新版金融未嘗試2608項而非舊2828項。來源外部新鮮度未核的項目不自動結案。NOAA官方說明重新下載相同後，完成34站11163日×12欄品質續作，缺值不填零，觀測不冒充預報。Untitled無需恢復，SDG業務分析凍結，安全保留不解除。\n\n[報告](../Reference/Pending_Recheck_B35_20261009.qmd)。\n',encoding='utf-8')
