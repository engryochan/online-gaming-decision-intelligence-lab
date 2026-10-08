# 全球 ISO 3166-1 × 百業 × 法人實體 · v1.5.0 全球同步覆蓋審計

發行日 2026-10-08。**本版實現全球每一地區佔位與可審核資料管線，不代表已獲世界全部公司名錄。**

## Blueprint／藍圖
- ISO 3166-1: 249 個國家／地區；沿用 v1.4.0 的 Alpha2、Alpha3、名稱，不擅自裁決主權。
- 8 組獨立資料來源通道在每個地區均建佔位，共 1992 筆（全部為 NOT_INGESTED，嚴禁把佔位當資料）。
- 全球識別以 GLEIF LEI 為跨境鏈接；法人註冊號是法域本地身份；活動以 ISIC Rev.5 作分類映射；時間與證據可追溯。
- 官方國別登記機關（需逐個法域確證） > GLEIF／OpenCorporates 輔助 > 網站／報告線索；多源不代表來源獨立。
- 既有氣象 v1.1 與百業 v1.4 保留，不覆寫；原 25 業僅為 legacy 分類，不能說成正式 ISIC Rev.5 全表。

## redteam／紅隊
1. 偽造的官方登記站和惡意 CSV 公式：官方域名確證、檔案 SHA-256、來源白名單，CSV 單元格清洗。
2. 資料主權和使用權：分開查閱許可、批量下載許可、再發佈許可、跨境傳輸許可。
3. 偽多國覆蓋：全球 API 能查某座標不等於當地企業名錄可取得。
4. 跨國同名誤合併：必須先核 national ID + jurisdiction，LEI 作跨境參照；疑義採人工複核。
5. 所有權穿透誤判：GLEIF Level 2 為會計合併關係，非全量股權、實控人或受益所有人。

## critic／批判
- 249 地區僅 ISO 3166-1 的地理全集，不代表 249 個可完全公開下載的企業登記庫。
- ISIC 是行業分類，不是全球公司身份表；GLEIF 不收錄全球所有實體。
- 全球所有商家、家庭、政府組織和非法人組織不能被一張商業公司表完全表示。

## killcritic／反駁與證偽協議
- 用各法域官方企業存量／活躍公司總數（同統計口徑和時點）作分母；無分母則 coverage_ratio = UNDEFINED。
- 抽樣比對官方注冊紀錄，報 precision／recall、重複率、錯配率、時效差；不允許以命中自家樣本當全局召回。
- 給每條關係保留原始紀錄、日期、來源與具體關係類型；抽樣支持手動核對。

## blindspot／盲區
- 未申領 LEI 的小企業；個體戶；非註冊商業活動；公司分支機構；非營利組織；合作社；公共機構；信託；歷史清算公司。
- 地區與法域並非一一對應；同一國別內多個聯邦、省級、市級登記機構。
- 國家統計分類採用 ISIC Rev.4、NACE、NAICS 或地方分類時，須用版本化對照，不能硬把碼改成 Rev.5。

## cheatsheet／速查
`UNKNOWN` 沒有證據；`NOT_INGESTED` 沒有匯入；`UNVERIFIED_CANDIDATE` 機構候選；`VERIFIED` 已證實；`UNDEFINED` 缺分母；`0` 僅可用於明確計數零。

## actionplan／全球同步而非三國試點
1. 從 249 個地區同時建立官方登記機關及數據權限來源清單。
2. 從 UN 官方 CSV 匯入 ISIC Rev.5 完整 hierarchy，先逐字節 SHA-256 審核。
3. 抓取公開授權的 GLEIF Golden Copy L1 與 L2，批次以 DuckDB/Parquet 入庫，報告逐國實際非零記錄。
4. 橫向擴充全法域官方登記、OpenCorporates／本地資料供應者，按來源條款辨識重複。
5. 統一跨國法人時態圖譜，避免商標、法人、母集團混淆。
6. 對 249 地區逐國公佈證據缺口、母數及源可靠性，不能宣稱 100% 法人覆蓋。
7. 週期化更新／失效回查；若有法域權限問題，保留缺口而不偷採。

## Gate 結果
- G01: **PASS** — 249 rows; alpha2 distinct
- G02: **PASS** — 249 * 8 = 1992 slots; all listed
- G03: **BLOCKED** — No claim every registry URL has been independently verified
- G04: **BLOCKED** — UN CSV URL found, binary fetch failed
- G05: **BLOCKED** — No real LEI records downloaded or ingested
- G06: **BLOCKED** — No real RR records downloaded or ingested
- G07: **PENDING** — Jurisdiction and source licensing review required
- G08: **PENDING** — No truthful entity count until records ingested
- G09: **SCHEMA_READY** — Schemas include valid_from/to and identifier keys
- G10: **PASS** — Prior v1.1 assets remain separate and not overwritten

## 主要官方來源
- ISO: https://www.iso.org/iso-3166-country-codes.html
- UN M49: https://unstats.un.org/unsd/methodology/m49/
- UNSD ISIC Rev.5: https://unstats.un.org/unsd/classifications/Econ/isic
- GLEIF Golden Copy: https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy

**封存聲明**：未連接任何公司生產系統、博彩站點、StarRocks、Superset、DolphinScheduler；所有資料由本地既有附件衍生和官方公開頁面手工登錄來源資訊。
