# 天下百業全域資料目錄 v1.6.0 — 七策治理與工程驗收

日期：2026-10-08。基線：v1.5.0；不修改舊檔。

## 核心判準
ISO 3166-1 的 249 個國家／地區是地理目錄，不是已蒐集全世界所有實體的證明。非公開資料可登錄存在性、權利人、許可流程、可公開元資料，但不代表有權存取內容。尚未知曉的資料不可能證明零遺漏。

## 七策
### redteam／紅隊
假法人、鏡像官網、編造來源、資料投毒、跨國重名、機密外洩、衛星圖像授權混淆、地緣統計偏差與故意製造數據缺口；每個威脅設來源簽章、哈希、雙人複核、回滾與查詢稽核。
### critic／批判
249×25 只是領域責任網格，不等於 6225 組真實資料已取得；全球 API 提供服務不等於對每個地區的細節充分；LEI 不是全世界企業全集。
### killcritic／證偽
反例優先：抽選沒有 LEI、沒有公開登記、已註銷、跨境分公司與非營利組織進行召回測試；缺官方分母時不填覆蓋率。
### blindspot／盲區
海洋、南極、國際水域、軌道與天體並非單一 ISO 領土模型；增設非地理對象命名空間，不杜撰主權。音訊、影像、科學實驗與動態事件須自帶時效。
### blueprint／藍圖
全域 ISO/UN M49 → 產業 ISIC → 來源目錄 → 授權閘門 → 法人主資料 → 時態關係圖 → 多模態資料／空間圖層 → 指標／模型 → 獨立稽核。優先 Parquet/Iceberg + DuckDB/Polars + GeoParquet + STAC + RDF/JSON-LD；規模需求證實後再引入分散式運算。
### cheatsheet／速查
PRESENT_IN_INDEX ≠ SOURCE_VERIFIED ≠ ACCESS_AUTHORIZED ≠ INGESTED ≠ QUALITY_VALIDATED ≠ GLOBAL_COVERAGE_PROVEN。UNKNOWN≠0；無法合法取得時只保存依法可以公開的元資料。
### actionplan／行令
1. 審核 ISIC Rev.5 官方 CSV 來源與校驗碼；2. GLEIF 官方 Golden Copy 與增量檔的授權下載；3. 各法域登記來源盤點；4. 建立 entity resolution 的弱標籤與人工復核；5. 每個行業的全球多來源對照；6. 以證據類別公布覆蓋率；7. 滾動回測與資料漂移驗收。

## 已達與未達
PASS: ISO 主鍵 249 唯一；領域索引 249×25=6225；通道索引 249×6=1494；舊版 249×8=1992 證據矩陣未修改。
BLOCKED: 未獲正式 ISIC 四位碼完整下載；GLEIF Level 1/2 尚未真正入庫；沒有任何證據可證明全世界網站／私有／機密衛星資料已一件不漏取得。

## 外部正式來源
- ISO https://www.iso.org/iso-3166-country-codes.html
- UN M49 https://unstats.un.org/unsd/methodology/m49/
- UN ISIC https://unstats.un.org/unsd/classifications/Econ/isic
- GLEIF https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy
- OECD https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0463
