# 天下百業全域工程 v1.9.0 — 七策審計與實際入庫關卡

2026-10-08。基線自 v1.8.0 SQLite 複製，無刪除歷史資料。

## 實測結果

- ISO 3166-1：249 筆，跨領域：21165 筆。
- GLEIF 真實法人：0 筆；正式資料下載受 DNS 阻斷，因此未偽造入庫。
- 以獨立 fixture 測試 JSON:API 匯入：讀 2、收 1、拒 1，且已清除測試資料。
- SQLite integrity_check=ok；foreign_key_check=0。

## redteam／紅隊

假資料冒充官方；同名法人誤合併；錯誤國別碼；惡意 JSON；重複 LEI；未確認授權；來源遭替換；失效註冊與跨時點所有權混淆。暫以驗證、雜湊及拒收資料隔離，尚須增加格式大小上限、簽章確認及批次回滾演練。

## critic／批判

全球 249 個地理代碼不代表全球企業入庫。公開 GLEIF 記錄僅是持有 LEI 的實體子集合，不是全球所有企業名冊。

## killcritic／證偽

每批必須報告：官方來源網址／授權／擷取日期／SHA-256／讀取／接受／拒收／重複／國別匹配與外鍵。只有來源位元組可核對，才可提高證據等級。

## blindspot／盲區

需要 Level 2 母子關係與申報例外、歷史政權、古代商號、非營利組織、非正式經濟、沒有 LEI 的企業，以及逐國登記制度差異。測試匯入器目前僅支援 GLEIF API JSON:API 單檔及 records 陣列，不支援 Golden Copy 壓縮全檔格式。

## blueprint／藍圖

ISO 3166-1／UN M49 → 各國登記資料 → GLEIF Identity → ISIC Rev.5／CPC → 雙時間實體圖譜 → 證據與授權 → 全球覆蓋率；地球以外空間另設坐標域，避免錯用國別碼。

## cheatsheet／速查

NOT_DISCOVERED ≠ ACCESS_DENIED ≠ NOT_INGESTED ≠ VERIFIED_ZERO；註冊號 ≠ LEI；子公司 ≠ 品牌；研究目錄 ≠ 史實；API 測試通過 ≠ 全球入庫完成。

## actionplan／行令

1. 從 [GLEIF 官方 API](https://www.gleif.org/en/lei-data/gleif-api/) 合法下載 JSON 資料檔。
2. 使用 `python global_lei_ingest_v1_9_0.py --input data.json --db global_earth_temporal_lakehouse_v1_9_0.sqlite --source-url <official-url> --collected-at <ISO-8601> --rejects rejected.csv`。
3. 核對批次讀取、接受、拒收、實體數及資料源版本，勿將測試 fixture 匯入正式庫。
4. 正式分類由 UN 原件匯入，缺正式原件時不可升級 PASS。
5. 在 249 個國別中同步查證來源完整度，不以三國樣本推論全球全域。

## 外部資料

- https://unstats.un.org/unsd/classifications/Econ/isic
- https://www.gleif.org/en/lei-data/gleif-api/
- https://www.gleif.org/en/lei-data/access-and-use-lei-data/supporting-documents
