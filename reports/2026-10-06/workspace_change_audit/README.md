# 文件定位與全項目變更掃描（2026-10-06）

已接納使用者將新生態登記報告分檔、保留舊宇航報告的調整。掃描開始時Git工作區乾淨；HEAD為`049988a`。近期`00888e8`與`049988a`已包含分檔及資產調整，不能把已提交的修改當成可覆寫內容。

| 文件 | 用途與更新規則 |
|---|---|
| [Aerospace_Ecosystem_Report.qmd](../../../Reference/Aerospace_Ecosystem_Report.qmd) | 保留原宇航數據栈比較原文；本輪未修改正文、HTML或資產 |
| [Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd](../../../Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd) | 世界前沿生態登記與後續校訂；沿用使用者檔名拼寫 |
| [Inteligent參考檔](../../../Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd) | 本輪只更新新增校訂索引的報告連結；歷史回答及舊報告引用保留 |
| Reference/Aerospace_Ecosystem_Report.md | 相對`4982fcc`的已提交變更中為刪除；未恢復。歷史提及由引用索引保留，不能機械替換成新報告 |

生成腳本已改成新報告目標，預設只產出`frontier_ecosystem/preview/`提案。顯式`--apply`須通過所有7項管理輸出的SHA256基線檢查；有現行修改即拒絕覆寫。不要為強行套用而刷新基線。驗收腳本已移除恢復刪除資產和修改換行的行為。跨回合定位規則另寫入根目錄[AGENTS.md](../../../AGENTS.md)。

掃描與檢查結果：

- [before_files.csv](before_files.csv)：修改路由前的全項目SHA256清單，374個常規文件（含剛新增的掃描器），約149.8MB。
- [current_files.csv](current_files.csv)、[current_summary.json](current_summary.json)：交付時的文件路徑、大小、時間、SHA256、Git狀態及相對初掃的變化。含未追蹤與被忽略的預覽文件；`.git`內部、符號連結及本掃描器生成的CSV／JSON／README回執除外，以避免自引用。
- [current_committed_changes.csv](current_committed_changes.csv)：`4982fcc`至初掃HEAD的13個淨變更路徑，包含上輪交付與使用者調整；不是本輪未提交變更清單。
- [current_document_references.csv](current_document_references.csv)：文字文件中兩份報告與舊`.md`名稱的引用位置，只存路徑、行號和目標名，不存正文。歷史提及不等於失效的活動連結。
- [safety_checks.json](safety_checks.json)：16個原宇航文件與資產SHA256未變、3份CSV未變、預設生成不改現行文件、提案與新報告一致、模擬過期基線在寫入前被拒絕。

兩份本輪更新的HTML已重新渲染。新長檔名報告直接渲染遇到Windows寫入錯誤，改從Reference目錄用短暫輸出名渲染成功，再同步回對應HTML；暫存輸出已移除。Quarto只有zh-TW翻譯回退警告。未重渲染或改寫保留的宇航報告。

此掃描核對文件版本、引用與更新路由，不等於逐文件逐主張的實質內容查證。後續更新前先重新掃描並比較現況，不以本次快照推斷未來文件未變。

重跑掃描：`python reports/2026-10-06/workspace_change_audit/scan_workspace.py --label current`。保留`before`快照；後續批次另用不同label。`check_update_safety.py`僅供本輪驗收，其建立的delivery_baseline不能作為繞過未來使用者修改的操作。
