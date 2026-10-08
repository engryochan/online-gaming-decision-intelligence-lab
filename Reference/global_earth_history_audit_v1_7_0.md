# 全球地球全域百業與文明史產業鏈 v1.7.0 — 七策與驗收

**地理範圍**：地球 ISO 3166-1 全 249 國家／地區；不以現代政治疆界回填古代版圖。**時間範圍**：史前人類經濟活動至 2026，區間僅為全球比較研究分期，各文明不必同步。

**核心進展**：原有 v1.6.0 25 領域全部保留，擴增跨領域候選；新增 ISIC Rev.5 的 22 個官方 section（中譯僅供參考），而 87 division／258 group／463 class 尚待完整正式來源檔匯入。CPC Version 3.0 是產品／服務分類，不能用 ISIC 企業活動碼代替。

**真實入庫**：249 國別、分析領域、全域矩陣、ISIC 22 門、研究性歷史期、概念產業鏈已入 SQLite；企業法人=0、歷史個體實體=0。未匯入 GLEIF 或各國工商底檔；全域矩陣只是缺口管理，全部 NOT_VERIFIED。

## redteam／紅隊
偽造官方來源；不同語言譯名碰撞；現代主權錯投古史；歷史倖存偏差；未授權商業資料擷取；個資／國安機密誤流入資料湖；平台－品牌－法人重複計數；ISIC 與 CPC 混碼。

## critic／批判
「國別 × 領域」是覆蓋要求表，不是觀測資料表；古代並無統一公司登記制度；一種古代職業也不能直接映射現代 ISIC 四位碼。

## killcritic／反證程序
抽取任意 ISO2 必須有全部領域；前 25 個舊領域代碼必須保留；無任何法人證據不得落入 legal_entity；古代史料引用需在年代、地理、文字／考古證據三欄獨立審核；官方 ISIC 完整 830 類(22+87+258+463) 必須版本化匯入後才稱「正式四級完成」。

## blindspot／盲區
口述史、非正規經濟、無文字社會、奴役勞動、女性與家內生產、宗教與寺院經濟、原住民商貿、跨境海洋網絡、失傳產業、歷史文獻損毀、公司資料權限與地理數位落差。

## blueprint／藍圖
國別與歷史地理各自作維表 → ISIC(活動)／CPC(商品服務)雙分類 → 商業與非營利組織身份 → 事件／股權／交易關係 → 歷史資料多證據併存 → 雙時態與授權治理 → 氣象／社交／支付／房地產／宇航等橫向價值鏈圖譜。

## cheatsheet／速查
`CATALOGUED` 僅為範圍列出；`NOT_VERIFIED` 未實測；`NOT_INGESTED` 未取得內容；`UNDEFINED` 缺可靠分母；`NOT_APPLICABLE` 確實不適用；`0` 僅允許實測零。

## actionplan／行動
1. 全球並行逐一核實官方法人註冊來源／許可，不選三國樣本冒充全球。2. 官方匯入 ISIC 四級結構及 CPC v3 完整清單。3. GLEIF 與合法開放國別法人資料分批增量入庫。4. 搭建史前／古典／中世／近現代跨地區史料索引，依考古／文字／統計可信度分級。5. 做抽樣官方回查、資料漂移、全球可觀測覆蓋率與授權稽核。

## 來源
- https://unstats.un.org/unsd/classifications/Family/Detail/2095
- https://unstats.un.org/unsd/classifications/Family/Detail/2100
- https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy
- https://www.unesco.org/en/silk-roads/about-silk-roads
- https://whc.unesco.org/en/list/1141/

## 限制
所有分析分類為工程選定候選，不能冒充 ISIC 各細類。歷史年代大致區間不等於全球同步歷史紀年。未授權、不公開或依法保密資料不得假設可存取。
