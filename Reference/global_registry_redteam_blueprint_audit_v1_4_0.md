# 全球百業企業與組織登記工程 v1.4.0 | 2026-10-08

## 判決與身份

以 `global_country_registry_v1_3_0.csv` 為 249 筆 ISO Alpha-2 歷史主鍵基線。保留原 25 類研究用行業、31 項氣象與地緣供應商。不得聲稱 ISO 3166-1 內有 249 個主權國家、不得聲稱 25 類等於正式 ISIC Rev.5、不得聲稱本輪已收錄 GLEIF 任何真實法人。

## 本輪已實證

- ISO Alpha-2：249 條與 249 唯一鍵，原始檔 SHA-256 見驗收輸出。
- 聯合國 ISIC Rev.5 官網提供結構 CSV，但執行環境直接下載失敗；完整正式 ISIC 分類入庫 **BLOCKED**。
- GLEIF 截至 2026-10-07 的官方 **發佈清單**：L1 3,454,757 記錄，L2 672,711 關係，例外報告 6,235,987；本輪原始檔均 **NOT_INGESTED**，不能視為本地實證數。
- 離線 LEI JSON:API 適配器支持已授權的本地文件；此處的 SAMPLE ENTITY 純屬測試資料，不進入正式註冊表。

## redteam／紅隊

來源偽造／網站冒牌、API 鍵暴露、營利再分發超授權、登記號碰撞、同名跨國誤合併、母子公司實際控制與會計合併關係混淆、日期穿越、惡意篡改 ISIC 四位碼、超大檔案耗盡 Excel 記憶體、惡意 CSV 公式注入。對策：白名單來源、SHA-256、欄位審核、獨立異常表、時間切片、許可審核、只讀原件、公式字元防護、分批載入。

## critic／批判

ISO 3166-1 為地理身份不是公司全集；ISIC 是**經濟活動**分類，不是工商機構唯一性證明；GLEIF 主要覆蓋持有 LEI 的實體，存在選擇偏差；OpenCorporates 自述 2 億+ 公司，仍無法當成全球全部工商實體。全球法人覆蓋率不能以「下載筆數／人口」代替。集團、商標、實體分支與公法人分別建模。

## killcritic／可證偽裁定

C1 有可靠官方當年逐國登記存量分母且與抽樣工商簿冊一致，才允許聲稱該國企業覆蓋率；C2 當同名異 LEI 的重複率過高時取消自動合併；C3 上下游實體關係須有關係型別及有效日期；C4 明確保留未知、未收集與否定證據的區分。

## blindspot／盲區

分公司、合作社、慈善機構、政企、國有企業、註銷公司、域外登記、離岸主體、地方登記、異體字／多語名、未登記經濟活動、政府／軍工資料不公開、LEI Level2 的報告例外。另需把 WMO 等事業機關與 ISO 地區映射獨立管理。

## blueprint／七層結構

1. `country_area`: ISO 3166-1 + UN M49，含代碼版本。
2. `source_authority`: 官方註冊機關、商業資料供應商、授權、資料批次、校驗值。
3. `entity_identity`: (jurisdiction, registration_no, legal_form, validity) 作候選主鍵；LEI、統一編號為交叉識別。
4. `entity_activity`: 多 ISIC／NACE／NAICS／當地分類、活動開始終止日。
5. `group_relationship`: shareholder / direct_parent / ultimate_parent / branch / joint_venture，區分控制與披露。
6. `source_assertion`: value、source_id、observed_at、effective_from/to、confidence、disputed。
7. `coverage_and_audit`: country、agency、sector、as_of、numerator、denominator、license、verification_state。

**記錄層**採 append-only；避免一次性將原始數百萬筆塞入 Excel：原始放 Parquet／DuckDB、彙總以 Excel／CSV，API 更新須按許可和增量校驗。

## cheatsheet／速查

- `UNKNOWN` 未取得｜`NOT_INGESTED` 未匯入｜`NOT_APPLICABLE` 不適用｜`0` 實測為零。
- `P0` 法規與官網登記紀錄；`P1` 官方公司年報；`P2` 可信彙編；`P3` 未證。
- `coverage = independently_verified_unique_entities / audited_official_active_registry_count`，缺分母時為 `UNDEFINED`。
- Source URL ≠ successful download；LEI ≠ 每家公司必有；ISIC assignment ≠ 法律註冊主鍵。
- 官網發佈數 ≠ 本地入庫數；測試資料不得冒充真實法人。

## actionplan／驗收行令

- **P0** 輸入正式 ISIC CSV 的已校驗原始 bytes；執行 importer，人工批准 schema 與 Errata；未取得前維持 BLOCKED。
- **P1** 從 GLEIF 公開接口依法下載 L1 + L2 檔至隔離離線區；優先以分批 JSON:API 檢查前 100 條 schema；大檔另建 CDF XML streamer。
- **P2** 擇優以馬來西亞 SSM、英國 Companies House、歐盟 BRIS 等官方來源建立司法管轄區樣本，先有可靠分母再發佈覆蓋率。
- **P3** 全局重複、名稱變更、時間有效性、跨國集團關係與語言測試。
- **P4** 在完全離線測試環境完成資料授權、效能、可追溯與 R/Python 讀取驗收後再規劃 ETL。

## 來源鏈與限制

- UN ISIC: https://unstats.un.org/unsd/classifications/Econ/isic
- GLEIF L1/L2: https://www.gleif.org/en/lei-data/gleif-concatenated-file/download-the-concatenated-file
- GLEIF JSON:API: https://api.gleif.org/api/v1/lei-records
- OpenCorporates: https://api.opencorporates.com/ — 2026-09-09 版本之許可條款須查證。

未連接任何禁用公司生產平台。此版是可執行**離線匯入和阻斷驗證骨架**，未假裝完成全球企業實體數據拉取。
