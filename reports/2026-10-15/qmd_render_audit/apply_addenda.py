"""Insert bounded factual review notes without rewriting existing document bytes."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
patches=[('Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd',
          '<!-- INTEGRATION_20261007_BEGIN -->', '''<!-- FACT_CHECK_20261015_BEGIN -->
## 2026-10-15 外部事實續核（有界增補） {#sec-fact-check-20261015}

本節只裁決下表的具體主張。歷史問答、來源附錄、全部機構登記及原有 VERIFIED 標籤尚未由本輪逐條重驗；不得把本節理解為全報告事實驗收。原宇航數據栈比較報告及歷史批次原文保留。

| 核對項 | 本輪裁決與適用邊界 | 一手來源 |
|---|---|---|
| NASA cFS | 確認為飛行軟體架構框架。公開 GitHub demo bundle 明示並非可直接飛行的發行版，任務方仍須負責按任務要求驗證；框架存在不等於本項目已取得任務認證。 | [NASA cFS README](https://github.com/nasa/cFS) |
| Open MCT | 確認為網頁式任務運作資料視覺化框架；不據此推論與 cFS 已整合或具有飛行控制認證。 | [NASA Open MCT](https://nasa.github.io/openmct/) |
| Apollo 連線設定 | 官方文件的 No connection expected 模式不發出 Plans；Relayed from another Hub 以 bundles 匯入回報狀態。不能把唯讀轉送說成由該 Hub 發出部署計畫。 | [Apollo connection settings](https://www.palantir.com/docs/apollo/managing-environments/environment-connection-settings) |
| Open-Meteo API | 免費 API 限非商業使用；customer API 包含商業使用授權。API 服務方案與底層資料授權仍須分別核對。 | [官方定價與 FAQ](https://open-meteo.com/en/pricing) |
| Athea 成立公告 | 2021-05-27 公告的合資雙方為 Thales 與 Atos；這項歷史公告不能證明現時股權，也不能改寫成 Helsing 與 Saab 合資。 | [Thales 原公告](https://www.thalesgroup.com/fr/group/journaliste/press-release/thales-et-atos-creent-le-champion-europeen-du-big-data-et) |
| Saab 與 Helsing | 2023-09-14 公告支持戰略合作及 7,500 萬歐元取得 5% 股份的當期交易條件；不當作現時持股比例。 | [Saab 原公告](https://www.saab.com/newsroom/press-releases/2023/saab-signs-strategic-cooperation-agreement-and-makes-investment-in-helsing) |
| Synopsys 與 Ansys | 2025-07-17 官方公告支持完成收購；不據此判定後續所有產品、法人及剝離交易。 | [Synopsys 完成收購公告](https://investor.synopsys.com/news/news-details/2025/Synopsys-Completes-Acquisition-of-Ansys/default.aspx) |
| MAGE 開發方 | NGA 的專案說明支持由 NGA 與 BIT Systems 合作開發；不與 Esri ArcGIS 合併為同一產品。 | [NGA MAGE About](https://ngageoint.github.io/MAGE/about/) |

本輪細項證據與未核清單位於 `../reports/2026-10-15/qmd_render_audit/`。文件渲染與外部事實驗收分開記錄。
<!-- FACT_CHECK_20261015_END -->

'''),
('Reference/春秋戰國諸子百家之頂級在線百家樂平臺_冊一.qmd',
 '<!-- FRONTIER_REVIEW_20261006_START -->', '''<!-- FACT_CHECK_20261015_BEGIN -->
# 2026-10-15 提問一事實續核 {#sec-question-one-fact-check-20261015}

以下只更新提問一中明確列出的主張，後文原模型回答保留供追溯；其他提問與數值尚未逐條完成外部重驗。

| 提問一主張 | 本輪裁決 | 一手來源 |
|---|---|---|
| Playtech 於 2017 年 10 月收購 BetBuddy，且當時已完成 IMS 整合 | 收購公告日期為 2017-10-27；公告對 IMS 整合使用將來式，不能單靠該公告把整合完成日定在收購當日。現行產品頁可支持 BetBuddy 的 AI 行為監測與預測風險用途，不能反推早期部署日期。 | [收購公告](https://www.playtech.com/es/playtech-acquires-betbuddy/)、[現行 Playtech Protect](https://www.playtech.com/sustainable-success/playtech-protect/) |
| 2018 年 1 月完成 Featurespace 與 IMS 整合 | 官方 2018-01-30 公告明確支持已完成機器學習反詐工具整合；這是供應商的產品整合披露，並非真人百家樂桌台已採用強化學習的證據。 | [Playtech 整合公告](https://www.playtech.com/playtech-integrates-featurespaces-real-time-gameplay-fraud-detection-into-ims/) |
| Entain ARC 以近 30 個行為標記運作 | 本輪讀到的 2021 年官方說明支持擴充行為指標、模型開發與預定推出安排，沒有給出「近 30 個」的精確數目；該數目維持證據不足，不能把計畫語句當作完成部署。 | [Entain ARC 官方說明](https://www.entaingroup.com/news-insights/latest-news/2021/entain-pioneers-preventative-approach-to-player-protection/) |
| AI 風險監測可直接證明 RL 營運自動化 | 上述資料僅支持各自公開披露的風險分析、保護與反詐用途，沒有證明指定百家樂營運商已部署 RL、牌局預測、動態抽水或獲利保證。 | 適用邊界：依上列原公告逐項判斷 |

完整待核候選與本輪證據台帳見 `../reports/2026-10-15/qmd_render_audit/`；候選抽取數量不是已核實事實數量。
<!-- FACT_CHECK_20261015_END -->

''')]
records=json.loads((OUT/'source_changes.json').read_text(encoding='utf-8')) if (OUT/'source_changes.json').exists() else []
for rel,marker,note in patches:
    p=ROOT/rel;old=p.read_bytes()
    if b'<!-- FACT_CHECK_20261015_BEGIN -->' in old: continue
    token=marker.encode();assert old.count(token)==1,rel
    nl=b'\r\n' if b'\r\n' in old[:2000] else b'\n'
    inserted=note.replace('\n','\r\n').encode() if nl==b'\r\n' else note.encode()
    new=old.replace(token,inserted+token,1)
    h=hashlib.sha256(old).hexdigest();(OUT/'original_bytes').mkdir(exist_ok=True)
    (OUT/'original_bytes'/(h+'.bin')).write_bytes(old)
    p.write_bytes(new)
    assert new.replace(inserted,b'',1)==old
    records.append(dict(path=rel,before_sha256=h,after_sha256=hashlib.sha256(new).hexdigest(),
                        change='bounded insertion only; all pre-existing bytes preserved'))
(OUT/'source_changes.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=True))
