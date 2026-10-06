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

重建：以Python執行 reports/2026-10-06/frontier_ecosystem/build_registry.py。生成報告、CSV、參考檔校訂索引與本地驗收回執；不聯網、不更新歷史HTML。驗收回執只是本地結構結果，不是獨立事實審核。
