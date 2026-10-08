# 天下百業全域資料工程 v2.0.0：七策審計及交付指引

日期：2026-10-08。**本輪完成離線可執行的資料攝取引擎和測試，並未完成官方真實資料全量入庫。**

## 核心實證
- 完整繼承 v1.9.0 的 249 個 ISO 3166-1 地區、85 個跨域類別、21,165 筆交叉矩陣。
- 新增 `v20_lei`、`v20_relationship`、`v20_classification`、`v20_source_file`、`v20_reject` 表。
- GLEIF LEI 採 ISO 17442 MOD97 校驗；無效國碼、名稱空白、同批重複均拒收。
- `strict` 模式存在任何拒收則回滾整批，`quarantine` 模式記錄拒收後只提交合格資料；SHA-256 重複來源阻斷。
- 合成測試：2 筆、1 筆被接受、1 筆被拒絕；示範資料並**未**保留於正式 SQLite。SQLite integrity_check=ok、外鍵違規 0。
- 執行環境對 api.gleif.org DNS 解析失敗；真實 GLEIF 法人新增 0 筆。ISIC Rev.5 細層與 CPC 3.0 亦未載入。

## redteam／紅隊
外部下載需先經防惡意檔案掃描、壓縮炸彈/超大欄位限制、來源網址核實與授權審核。現有匯入器僅針對已獲准的本機檔案，尚未具備完整生產級限流、簽章驗證與所有 GLEIF Golden Copy 格式相容性。

## critic／批判
ISO-249 並非獨立國際標準；本工程使用 ISO 3166-1。249 地區的目錄完整不代表 249 地區法人資料完整。LEI 涵蓋範圍也不等於所有公司、社團及古代組織。

## killcritic／證偽
若發生來源 SHA 重複匯入未被阻斷、外鍵違規非零、無效 LEI 進庫、合成資料混入正式庫、公開授權缺失，該批次 FAIL。本輪五項測試均通過，官方全量下載關卡仍 BLOCKED。

## blindspot／盲區
- 古代史的國別不可倒套現代 ISO，須另建歷史地理及模糊年代。
- 媒體、社交、支付、房地產、公共機構和小型非正式經濟不能只用 LEI 代表。
- GLEIF 關係類別主要反映特定定義下的會計合併關係，不等於完整實益擁有人網絡。
- 法律與授權不明的私有、保密、衛星或個人資料不得擅自獲取。

## blueprint／藍圖
全球空間主鍵 → 來源證據與授權 → ISIC 活動分類 × CPC 產品分類 → LEI/工商登記身份 → 版本化母子關係 → 雙時間圖譜 → 分級量化決策。資料量大時採用 Parquet 分區及增量去重；SQLite 僅作可攜原型。

## cheatsheet／操作速查
```
python global_ingest_engine_v2_0_0.py --db global_earth_temporal_lakehouse_v2_0_0.sqlite \
 --input /path/to/authorized_lei.jsonl --kind GLEIF_LEI \
 --source-url https://www.gleif.org/... --license-note OPEN_OFFICIAL \
 --rejects rejects.csv --reject-policy strict
```
分類 CSV 應含 `code,label_en,level,parent_code`。先以 `--kind ISIC --revision Rev.5` 或 `--kind CPC --revision 3.0` 輸入官方原始資料的**核驗後正規化副本**；這不是聲稱原始 UNSD CSV 可免轉換直接讀入。

## actionplan／行動計畫
1. 經合法途徑取得 GLEIF 官方 Golden Copy Level 1、Level 2、例外及增量檔，驗證原始檔 SHA-256、版本和授權；新增 CSV/JSON 官方格式適配器後再批次處理。
2. 從聯合國分類官網取得完整 ISIC Rev.5、CPC 3.0 結構並建立源檔到正規化欄位的映射與父子層級檢查。
3. 將 249 地區列為同時追蹤對象，區分官方登記簿可存取、需付款、需申請、保密、不適用、未知。
4. 每筆法人/活動/關係記錄加證據指紋、授權、有效時間、已知時間與置信度。
5. 將百業與文明史資料納入長期版本化湖倉，量化各國實際收錄率，不得用目錄筆數替代實體數。

## 官方來源
- ISIC Rev.5: https://unstats.un.org/unsd/classifications/Econ/isic
- CPC 3.0: https://unstats.un.org/unsd/classifications/Econ/CPC
- GLEIF Golden Copy: https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy
- GLEIF concatenated: https://www.gleif.org/en/lei-data/gleif-concatenated-file/download-the-concatenated-file
