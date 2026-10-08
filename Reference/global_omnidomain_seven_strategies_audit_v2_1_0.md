# 天下百業全球全域資料工程 v2.1.0 — 七策審計

核驗日：2026-10-08。地球空間與古今文明研究繼承 v2.0.0。

## 實際驗收
- 國別249、研究領域85、國別×領域21165。SQLite 完整性通過、外鍵零違規。
- v2.1.0 法人、母子關係、正式 ISIC/CPC 細類新增均為 **0**；此數字不得宣稱全世界公司數量。
- 本輪直接下載官方資料遭 DNS 阻斷；**沒有真實官方紀錄入庫**。
- 新增離線 CSV/ZIP CSV 匯入器，可讀取含已知 GLEIF 平坦欄位的文件；官方 Golden Copy 實際格式尚未驗證，不保證不需欄位適配。
- 合成測試：嚴格模式回滾、隔離模式1接受1拒收、重複 SHA 阻斷、不完整欄位阻斷；測試只在臨時資料庫。

## redteam／紅隊
防範來源假冒、檔名替換、未授權文件、LEI 校驗碼錯誤、國別錯配、ZIP 多檔歧義。後續仍需 ZIP 解壓炸彈防護與數位簽章核驗。

## critic／批判
本引擎不是世界企業全集；資料來源存在不等於資料已獲取。對於只在地方登記的法人及古文明實體，GLEIF 覆蓋不足。

## killcritic／證偽
明確阻斷：無效 LEI、不支援來源欄位、同檔重複、同來源 SHA 重複、外鍵問題。無法驗證的官方結構不得標為已完成。

## blindspot／盲區
歷史國界不可套用當代 ISO；LEI 父關係大多反映會計合併而非所有實際控制；地區工商公開政策不一致；資料授權不同。

## blueprint／藍圖
全球249地區全域目錄 → ISIC/CPC 官方版本及跨版映射 → 法人身份與歷史實體 → 關係/時態斷言 → 來源授權/雜湊 → 可重放批次 → 覆蓋率治理。

## cheatsheet／速查
- `CATALOGUED` 已列目錄，不等於 `INGESTED`。
- `AUTHORIZED` 可使用，不等於 `PUBLIC`。
- `VERIFIED` 需要來源檔、結構、時間及交叉核對。
- `UNKNOWN` 不等於 `ZERO`。

## actionplan／行動
1. 在合法授權環境下載 GLEIF 官方 Golden Copy CSV/ZIP，記錄網址、取得日期、授權、SHA。
2. 實際樣本先與官方欄位逐項比對，修訂匯入映射；再跑全量與增量。
3. 匯入聯合國官方 ISIC Rev.5/CPC 3.0，核對分類層次與父子關係。
4. 以 ISO 249 個地區逐一登記當地工商來源、覆蓋分母及資料使用權；採全球並行排程，非僅三國。
5. 為史前至現代非當代國家的實體另建歷史地理坐標與證據鏈。

## 使用示例（官方原始檔已依法下載之後）
```bash
python global_official_ingest_v2_1_0.py --db global_earth_temporal_lakehouse_v2_1_0.sqlite --input /path/official_lei.csv --kind GLEIF_LEI --source-url https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy --license-note official-public-source --mode strict --rejects rejects.csv
```
注意：官方 CSV 欄位或結構可能與適配器不同，應先進行小批次驗收，切勿直接視為生產級支持。
