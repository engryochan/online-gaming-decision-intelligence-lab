# 四大 QMD × 對話全域聯集工程包（2026-10-12 優化版）

## 交付規則

- 上載的**四份正本原始位元組完整保留**，新增章節只追加，不會將報告內容誤寫回舊段落。
- 各文件包含共通的多領域集成附章，再附該文件專業定制章節。
- 不是原生平台逐字對話匯出；可見對話主題以 `conversation_topic_answer_ledger.csv` 登記（現為 C01–C40）。
- 部分外部事實只經限範圍來源核對；各年份、報價、法律、標準及技術版本不能默認長期有效。
- 所有列名對象不等於獨立法律實體、當期客戶、已驗證軍事合作或可免費商用圖資。
- 人物 QMD 包含 `lossless-html-snapshot` 恢復格式。

## 本輪優化重點（2026-10-12）

1. **conversation_topic_answer_ledger.csv**：擴充至 C40，完整覆蓋 Google 開源數據澄清、CesiumJS 首選、街景現實、OS 兼容、堂號規範、大秦賦算籌地圖架構。
2. **os_cross_platform_inventory.csv**：重寫為 21 項，新增 CesiumJS 瀏覽器／Electron 兼容性、街景適配、宣告式重現、國防相關性欄位。
3. **geospatial_licensing_matrix.csv**：明確區分 Google 專有圖資與 Street View vs CesiumJS／OSM／Mapillary／Sentinel 等開放或可商用選項。
4. **00_整合总览与审阅结论.md**：更新主要結論與完成項目數量，反映最新口徑。
5. 新增 **99_对话全域实体与组合标准附录.md**：彙整公司、組織、軟體、OS、工具、組合標準與口徑，方便直接引用。

## 對照附檔

- `conversation_topic_answer_ledger.csv`：主要問答議題與證據狀態（C01–C40）
- `cross_domain_entity_register.csv`：跨行業實體詞典與類型
- `entity_presence_original_four_files.csv`：這些名稱在四原文出現次數
- `os_cross_platform_inventory.csv`：作業系統與 Cesium 兼容性
- `integration_interface_contracts.csv`：GIS、宇航、人物、資料庫與安全接口
- `geospatial_licensing_matrix.csv`：API／圖資／影像商用授權審查
- `prompt_85_coverage_inherited.csv`：沿襲現存85種提示標籤與其執行狀態
- `acceptance_evidence_gates.csv`：19個驗收閘門
- `official_source_register.csv`：官方核驗入口
- `build_manifest.json`：位元組及SHA-256收據
- `99_对话全域实体与组合标准附录.md`：**本輪新增**全域實體與組合標準

## 文件特別注意

使用者既定安全限制仍然有效：不連接未授權企業原始數據或任何企業原始博彩數據。

本輪未下載外部 Google/OSM 街景照片、未推斷機密伺服器部署、未實際改動 WSL2/Kubuntu、未做付費API探測。
