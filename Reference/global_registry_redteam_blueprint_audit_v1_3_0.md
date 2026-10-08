# 全球 ISO 3166-1 百業法律實體註冊工程 — v1.3.0 審計與七策

核驗時點：2026-10-08。版本為非退化增量；原 v1.1 氣象矩陣與 v1.2 主體檔保持不動。

## 實測結果

- ISO 3166-1 歷史主表：249 筆；Alpha-2 唯一 249。
- 項目自訂 25 類分析分組：全部保留，**不等同 ISIC Rev.5 官方完整分類**。
- 聯合國 ISIC Rev.5 已正式提供四層分類 CSV/XLSX；本輪直連下載失敗，故官方各層級匯入數量為 0（BLOCKED），不虛構數碼。
- 世界銀行工商登記資料來源候選繼承，但沒有批次提取每家法人。真正法人實體載入 **0 筆**，公司全域覆蓋率 **不可計算**。
- 資料字典新增：跨國法人、工商登記、母子公司、有效期、活動分類、來源及授權欄位；不可將主辦／銷售地與註冊地混淆。

## redteam／紅隊

敵對情境：假冒工商登記頁、同名公司合併、跨國法人空殼、註銷實體未更新、法人號碼格式碰撞、商用資料禁轉售、股權資料時間差。門檻：官方來源優先、雙來源衝突排隊、不可無來源自動覆寫。

## critic／批判

249 地區 × 行業組合並不是世界公司名冊；不同法域欠缺公開母數、部分登記僅付費可查；LEI 以參與 LEI 制度的實體為主，不是全球所有營業主體。

## killcritic／證偽與反駁

若批評“永遠不能百分百”，建立可量測的來源分母才可證偽：在公開完整註冊簿的法域，對照公開登記母數及抽樣漏失；在不可知法域，報告 UNKNOWN，禁止宣稱 100%。

## blindspot／盲區

跨境實際營運、無法人協會、非法實體、非營利組織、合作社、基金、信託、政府部門、國企、已撤銷公司、地方名稱變體、受制裁及保密主體。對公民個人敏感資料採最小化收集，不做未授權爬取。

## blueprint／藍圖

Country (ISO2) → OfficialRegister (jurisdiction+register) → LegalEntity (register_number composite key) → EntityActivity (ISIC Rev.5 code + valid time) → OwnershipRelation (from/to entity + valid time) → GroupResolver (time-bounded consolidation). 每一層具 source_id、observed_at、record_hash、evidence_tier、licence、confidence，衝突保留多版本。

## cheatsheet／速查表

`NULL` 未知；`NOT_INGESTED` 未取得；`NOT_APPLICABLE` 不適用；`VERIFIED` 有一手記錄；`REJECTED` 有正式反證。LEI ≠ 全國註冊號；品牌 ≠ 法律實體；全球營運 ≠ 在每個國家註冊。

## actionplan／行令

P0：從聯合國官方鏈接匯入完整 ISIC Rev.5 CSV 並驗證四層層級與 SHA-256。P1：以世界銀行及國家工商註冊來源建立國別權威機關目錄。P2：檢查授權／頻率／限額／身份認證。P3：先選公開註冊接口的 3-5 個法域取得真實資料，依法人複合鍵去重。P4：接入 GLEIF 開放資料作交叉識別，不把 LEI 當全集。P5：執行來源/時效/一致性/涵蓋率閘門。P6：逐國擴展，以缺口與高風險錯誤優先。

## 官方來源

- https://unstats.un.org/unsd/classifications/Econ/isic
- https://www.gleif.org/en/lei-data/access-and-use-lei-data
- https://www.gleif.org/en/lei-data/gleif-api/
- https://www.worldbank.org/en/programs/entrepreneurship/sources
