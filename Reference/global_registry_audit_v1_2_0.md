# 全球百業法律實體註冊工程 v1.2.0｜審計與邊界

截至 2026-10-08。

## 實際驗收

- countries: 249
- unique_iso2: 249
- sector_count: 25
- coverage_cells: 6225
- expected_cells: 6225
- agency_candidates: 51
- wb_directory_candidates: 37
- entity_records: 0
- weather_provider_count: 31
- all_slots_not_enumerated: True

## 核心限制

1. 國別繼承 v1.1.0 的 249 筆 ISO 編碼；不是逐筆重新核對 ISO 付費授權主數據。
2. 百業分類是分析候選，不得冒稱聯合國 ISIC Rev.5 正式編碼；待取得正式版本表後映射。
3. 工商機關資料為「來源指引」，不代表本版已下載所有法律實體。某些世界銀行來源實為統計機關，而非可逐家檢索的工商局。
4. 全球法律實體、子公司、集團最終控制、各國所有行業皆不存在已證實完整的公共單一資料庫；此版法人名冊僅交付空表規格，並不虛構公司。
5. 保留舊版 31 供應商與 7,719 天氣矩陣於既有交付，不重寫其未驗證狀態。
6. 所有第三方資料再分發需審核授權與個資法；本版未接觸任何公司生產系統。

## 資料模型

`country_area (ISO 3166-1) → country_sector_coverage (候選行業) → legal_entity (register_id/LEI) → entity_activity (ISIC) → relationship (parent/subsidiary) → evidence → revision`

關鍵驗收公式：只有 `verified_unique_entity_count / independently_reconciled_registered_entity_total` 的分子與分母皆可核，才可公示覆蓋率。

## 官方來源

- ISO 3166 country and area codes: https://www.iso.org/iso-3166-country-codes.html
- ISIC Revision 5: https://unstats.un.org/unsd/classifications/Econ/isic
- World Bank Entrepreneurship Database sources: https://www.worldbank.org/en/programs/entrepreneurship/sources
- GLEIF Global LEI Index: https://www.gleif.org/en/lei-data/global-lei-index/
- GLEIF Golden Copy and Delta Files: https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy
- WMO members: https://wmo.int/about-us/wmo-members
- OpenCorporates: https://opencorporates.com/
