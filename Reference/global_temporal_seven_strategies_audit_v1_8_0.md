# 全球跨文明時態實體資料庫 v1.8.0｜七策驗收報告

**日期：**2026-10-08。**母本：**v1.7.0 SQLite 位元複製後作可回溯新增，不覆蓋原版。

## Blueprint／藍圖
六軸：地理（當代 ISO 與歷史政區分離）、實體、產業／產品分類、事件／關係、有效時間＋系統記錄時間、來源及授權。新增 9 類持續入庫治理結構（`spatial_reference`、`entity_identity`、`entity_alias`、`temporal_assertion`、`classification_node`、`source_snapshot`、`assertion_evidence`、`global_coverage_gate`、`ingestion_run`），以及一個全球門檻摘要視圖。現有 country/domain 等表未刪改。

## Redteam／紅隊
測試不存在國別外鍵 `ZZ` 無法寫入，倒置時間範圍無法寫入；資料證據獨立於聲稱，避免無來源推論悄然晉級。另須日後測試 XML 實體擴展、壓縮炸彈、偽造 LEI、來源重放、跨語種同名、授權污染。

## Critic／批判
`spatial_reference` 249 筆為 ISO 代碼空間佔位，非已證實疆域邊界； `global_coverage_gate` 21,165 筆皆標示 `NOT_VERIFIED`，不是 21,165 個已證明可取得資料源。保存所有舊版矩陣，但將模型架構完整度與事實收錄率分開。

## Killcritic／證偽
以 `PRAGMA integrity_check`、`foreign_key_check`、阻斷無效國別／時序區間，以及既有資料表計數驗證結構。未經來源文件的正式分類或法人紀錄不得自動置 `VERIFIED`。

## Blindspot／盲區
ISO 3166-1 為當代地理編碼，不涵蓋古國疆域、史前流動社群、公海和跨境網絡；歷史年份的 `valid_from` 與 `valid_to` 應使用能表達 BCE、模糊世紀及年代區間的擴展日期型別，**目前 TEXT 日期 CHECK 只保證字串次序，不等於完整考古年代語意驗證**。現有 GLEIF Level 2 主要描述會計合併關係，並非全部實益擁有人。

## Cheatsheet／速查
- `COUNTRY CODED` ≠ `OFFICIAL SOURCE VERIFIED` ≠ `ENTITY LOADED`。
- `UNVERIFIED` ≠ `ZERO`。
- `valid_from/to`＝現實生效時間；`recorded_from/to`＝系統認知時間。
- `classification_node` 可容納 ISIC／CPC 正式分類，但當前尚無官方四位分類實際匯入。
- `source_snapshot` 必須存 SHA-256、取得時間、授權依據。

## Actionplan／行動
1. 取得並逐位元驗證 UNSD ISIC Rev.5 官方檔，才導入全部層級。
2. 分辨 CPC Version 3.0 草案與正式版本，再建立 ISIC→CPC 跨分類關係。
3. GLEIF Level 1/2 官方資料經授權政策檢查後，串流／分批進入 SQLite 或 Parquet 分區；絕不先塞進 Excel。
4. 249 國別並行登記合法官方登記機關、可下載端點及公開分母，缺口繼續保留。
5. 歷史條目以原始史籍／考古來源和時間不確定性為先，才進入跨文明產業圖譜。
6. 為資料池配置快照指紋、來源撤銷、記錄覆寫檢查、資料品質報告與可復現 SQL。

## 驗收結果
- COUNTRY_PK: PASS; measured=249; base inherited
- DOMAIN_COUNT: PASS; measured=85; base inherited
- COUNTRY_DOMAIN_COUNT: PASS; measured=21165; base inherited
- COVERAGE_INITIALIZATION: PASS; measured=21165; all NOT_VERIFIED
- FOREIGN_KEY_INTEGRITY: PASS; measured=0; no violations
- SQLITE_INTEGRITY: PASS; measured=ok; pragma
- INVALID_COUNTRY_REJECT: PASS; measured=1; red-team test
- INVERTED_INTERVAL_REJECT: PASS; measured=1; red-team test
- REAL_ENTITIES_IMPORTED: BLOCKED; measured=0; no actual legal entity data loaded
- ISIC_REV5_FULL_IMPORT: BLOCKED; measured=0; official source not imported
- CPC_COMPLETE_IMPORT: BLOCKED; measured=0; official structure not imported
- HISTORICAL_ENTITY_EVIDENCE: BLOCKED; measured=0; no verified historical entities

**保密界線：**不連 Superset、StarRocks、DolphinScheduler、博彩網站或任何公司資料；不嘗試繞過機密與個資訪問控制。
