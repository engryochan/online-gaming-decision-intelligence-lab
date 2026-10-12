# 四大 QMD × 對話全域聯集工程包（2026-10-12）

## 交付規則

- 上載的**四份正本原始位元組完整保留**，新增章節只追加，不會將報告內容誤寫回舊段落。
- 各文件包含共通的多領域集成附章，再附該文件專業定制章節。
- 不是原生平台逐字對話匯出；可見對話主題以 `conversation_topic_answer_ledger.csv` 登記。
- 部分外部事實只經限範圍來源核對；各年份、報價、法律、標準及技術版本不能默認長期有效。
- 所有列名對象不等於獨立法律實體、當期客戶、已驗證軍事合作或可免費商用圖資。
- 人物 QMD 包含 `lossless-html-snapshot` 恢復格式：本次追加 Markdown 正文以保存其原始 HTML，專用恢復腳本是否顯示追加章節需再確認。

## 對照附檔

- `conversation_topic_answer_ledger.csv`：主要問答議題與證據狀態
- `cross_domain_entity_register.csv`：跨行業實體詞典與類型
- `entity_presence_original_four_files.csv`：這些名稱在四原文出現次數，不是通用 NER 全抽取
- `os_cross_platform_inventory.csv`：作業系統與主要用途
- `integration_interface_contracts.csv`：GIS、宇航、人物、資料庫與安全接口
- `geospatial_licensing_matrix.csv`：API／圖資／影像商用授權審查
- `prompt_85_coverage_inherited.csv`：沿襲現存85種提示標籤與其執行狀態
- `acceptance_evidence_gates.csv`：19個驗收閘門；源原文前綴的驗證已通過，系統實機驗收未執行
- `official_source_register.csv`：官方核驗入口（不表示所有章節全自動認證）
- `build_manifest.json`：位元組及SHA-256收據

## 文件特別注意

使用者既定安全限制仍然有效：不連接 Superset、StarRocks、DolphinScheduler、博彩網站或任何企業原始博彩數據。

本輪未下載外部 Google/OSM 街景照片、未推斷機密伺服器部署、未實際改動 WSL2/Kubuntu、未做付費API探測。
