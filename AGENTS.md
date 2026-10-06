# 文件保留與更新定位

- 開始更新前先檢查 `git status`、近期提交及目標文件的現行內容。使用者已提交的調整也必須保留，不能以工作區乾淨推斷可以覆寫。
- `Reference/Aerospace_Ecosystem_Report.qmd` 是保留原文的宇航數據栈比較報告；本輪生態登記生成器不得覆寫它。
- `Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd` 是世界前沿地緣戰略、軍工、宇航與AI生態登記報告。保留既有 `Interlligence` 檔名拼寫，未經使用者要求不要改名。
- 上述两份报告并存；校訂與新增登記寫入後者，歷史引用仍可指向前者。修改前依標題、用途與實際內容確認目標，禁止全項目機械替換檔名。
- `reports/2026-10-06/frontier_ecosystem/build_registry.py` 預設輸出至 `preview/`。先比較提案與現行文件，保留使用者修改；不要為通過 `--apply` 而自動刷新 `delivery_baseline.json` 或取消雜湊檢查。
- `validate_delivery.py` 只檢查交付文件及寫驗收回執，不恢復使用者刪除的文件、不改正文或換行。
- 渲染前記錄現行變更；若渲染器刪除資產，先確認本輪基線與依賴再處理，不能自動從HEAD恢復任意刪除項目。
- 全項目現況掃描可使用 `reports/2026-10-06/workspace_change_audit/scan_workspace.py`。快照記錄路徑、SHA256與Git狀態；`.git`內部與符號連結不掃描。它是版本基線，並非所有文件內容的實質核實。
