# 世界前沿生態登記 — 2026-10-06

196個研究候選；83條VERIFIED公開描述；113條UNKNOWN。不聲稱全球全量或世界排名。

| 文件 | 粒度／主鍵 |
|---|---|
| registry_frontier_organizations.csv | 機構／項目候選；entity_id |
| registry_frontier_claims.csv | 一條本輪描述；claim_id，entity_id外鍵 |
| registry_frontier_sources.csv | 來源指針與支持範圍；source_id |

VERIFIED只驗證claim文字；product_project_leads未被claim明確覆蓋時為UNKNOWN。法人、性能、部署、監管與市場排名沒有連帶驗證。country_candidate_iso_alpha2是編輯定位，非官方法人註冊地；服務覆蓋另建多對多presence。空國家碼不填造假代碼。

來源P0/P1只是類別，不代表獨立測效；UNKNOWN來源URL可只是待查入口。checked_on僅對本輪讀取或嘗試訪問的來源填寫，published_on未知留空。未保存HTTP原文。License UNKNOWN不能當再分發／模型訓練許可。

ISO外鍵對既有249條母表做結構驗證；本輪不重新核准ISO快照，也不建249行空白能力表。擴展presence與神經技術合同見報告。表均UTF-8 BOM CSV，所有ID在本批穩定；重建資料時勿重排DATA，新增應在末尾，避免ID變動。

更新目標：[地緣戰略、軍工、宇航與人工智能生態登記報告](../../Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd)。原Aerospace_Ecosystem_Report.qmd為保留的宇航數據栈比較報告，不能作為本批生成目標；保留使用者所定Interlligence檔名拼寫。

重建：以Python執行 reports/2026-10-06/frontier_ecosystem/build_registry.py，預設只在該腳本旁preview/生成提案，不修改現行報告、CSV或參考檔。只有明確加--apply且delivery_baseline.json包含所有輸出、現行SHA256完全匹配時才能覆寫本批管理文件；任何使用者編輯會拒絕覆寫，應先審閱差異而非刷新基線後強制套用。原宇航報告不在允許輸出清單。驗收腳本只讀取交付文件並輸出回執，不恢復刪除資產或修改正文。驗收回執只是本地結構結果，不是獨立事實審核。
