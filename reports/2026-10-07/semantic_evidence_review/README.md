# 業務語義與證據審校續批

起始 HEAD 為 20439fb，起始基線保持不變：`../../2026-10-06/workspace_change_audit/semantics_20261007_start_files.csv`。本批沒有重跑舊整合生成器、刷新 delivery_baseline 或重寫 DGEF。

`build_semantic_catalog.py` 讀取上一批盤點的168份表檔與現行DGEF字典／結構，給出明確標狀態的業務定義提案。CSV解析上限16MiB修復139101字元JSON儲存格的漏欄問題，真實欄位記錄1989。既有SQLite存在即拒絕覆寫本批。

`apply_review.py` 依起始主文件雜湊保護套用，保存修改前全文，加入五項裁決，對宇航原文三處錯誤定點更正，非目標文字可逆驗證。原說法保持在歷史來源／快照，不機械改写所有模型答覆。

來源在本輪改副檔名的事件另見concurrent_source_renames.json。兩份現實策略來源內容位元組相同；地緣来源補總標題、甲題標題與四份空模板，該增量已補入兩份主報告。原TXT保持刪除，新MD保持使用者內容；未把空模板當作新增技術證據。edit_manifest包含两階段連續版本雜湊，claim_locations定位至第一階段前的快照行號，不冒充當期行號。

`validate_review.py` 只讀驗證字段、來源雜湊、空值、SQLite完整性、原資料未變及源更名狀態，只寫驗證結果。未做所有外部主張普查，業務定義未獲負責人簽核。先前回執仍只對應先前版本，不能延用為當期PASS。

此次原研究報告HTML保持原狀；僅新續批閱讀頁與本輪受影響的整合入口／架構HTML重新渲染，後兩者的舊HTML亦保存於originals。Quarto不執行來源程式。
