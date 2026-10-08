# B04 交付定位

這是2026-10-08的固定交付快照，承接B03全部1,653個端點的主機集合，新增ANNA網站、名錄線索及完整來源檔的欄位化。QMD與HTML位於 `Reference/Global_Market_Directory_Expansion_B04_20261008.*`；資料表位於 `Reference/tables/29_global_market_directories_b04_20261008/`。

`final_acceptance.json` 記錄主機集合、來源行對賬、資料庫完整性、原行SHA256及報告／資料庫雜湊。`credential_scan.json` 是本輪掃描副本；其中ASX與B03資料庫候選屬於較早來源，B03候選已在B03驗收中判定為跨SQLite序列化邊界的假陽性。本輪未新增憑證候選，也另掃描37個壓縮檔內部成員。

腳本按 discover、parse_jse、collect_anna、extend_anna_sites、link_prior_isins、collect_observed_files、parse_psx、deliver、render、verify 的依賴順序執行。這些腳本記錄本次實際採集流程，不應直接重跑到已交付目錄。後續更新先檢查Git現況與本輪雜湊，使用新的批次／preview路徑，逐項比較後新增，保留使用者修改；不得為重跑刪除現有資料庫或刷新驗收基線。

來源觀測與內容完整性分開：網站回應200、關鍵字連結、ISIN校驗及相同ISIN，都不能證明公司／券商全球完整收錄。PSX名錄日期為2024年；JSE完整欄位及原文字編碼仍待核定。各種原始用途與時效標記均應保留。
