# ISO 249 全球科技登記：本輪交付與重建

本輪完成249個ISO國家／地區的廣泛發現檢索，並對選定機構、產品與工具核實具體公開描述。它不是每地每領域完整普查，也不提供世界頂尖或N0～N7排名。952筆搜索線索全部UNKNOWN；299笔機構候選包含原196筆及新增103筆，不能把政府政策支援單位誤當技術世界領先者。

`country_search_log.json`保存實際查詢、結果、日期與限流重試歷史；`curated_seed.json`是經人工讀取一手網頁後的短主張與來源。`additional_source_access_receipts.json`只保留第二組官方頁面的工具訪問元資料。未保存完整原始HTTP頁面，因此來源仍可能日後變動。來源支持公開描述，不代表獨立測試或當下實際部署。

生成器 `build_global_registry.py` 預設只寫此目錄的 `preview/`。核對 `preview_validation.json`與實際預覽後，初次交付可用 `--apply`；它檢查 `global_start_files.csv`中的主報告、參考底稿及AGENTS基線，拒絕覆蓋其他新文件或經人修改的輸出。初次apply在主報告與底稿尾端追加有界區塊，保留原有位元組。完成後不應再次apply；後續更新先比較現行內容並產生新批次，不刷新基線繞過使用者變更。

來源資料：`Reference/tables/01_country_area/registry_country_area_iso3166_20261004_enhanced.csv`與保留的`06_frontier_ecosystem_20261006`批次。輸出是新附錄 `Reference/Global_Technology_ISO249_Registry.qmd`及`Reference/tables/07_global_technology_iso249_20261006/`的9份CSV與JSON資料字典。舊批次七筆UNKNOWN没有來源外鍵，整合表保留原空值，不虛構網址。

驗收 `validate_global_registry.py --preview`檢查預覽；無參數檢查交付、外鍵、計數、來源限定、原196筆內容、原宇航報告與資產雜湊、使用者主報告HTML及兩份來源QMD原始位元組。它只產生驗收回執，不修正文。渲染僅針對新附錄HTML；本輪已由使用者修改的主報告HTML保留。

後續優先：每地當地語言與領域專項檢索、搜尋結果國別相關性、明確實體消歧、原始論文／基準／專利／監管／試驗證據、逐字段核實。Georgia首次檢索混入美國Georgia州頁面，全部仍為UNKNOWN，不計為喬治亞國家機構。空數值為UNKNOWN，不能轉為0；fNIRS並非思想解碼，遠程治療協議下發並非無設備讀腦。
