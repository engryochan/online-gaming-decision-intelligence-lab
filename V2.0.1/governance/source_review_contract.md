# 外部資料精華採用合同

2026-10-08。外部文件只讀核查；本輪不複製下載檔、不匯入其中的法人、關係、联系人或統計觀測明細。採用內容限於經覆核的方法、資料模型、用途及更正主張。逐檔核查結果見 [下載資料審閱報告](../../Reference/Downloads_Essence_Review_20261008.qmd)。

## 來源證據與處理範圍

每份外部來源登記文件雜湊、格式、取得證據、版本、核查粒度及剩餘缺口。文件存在、成功解碼、CRC 通過、欄位可解析、內容語義確認、跨來源核對分別記錄；不能合併成單一 VERIFIED。SHA256 用於版本身份與重放，不能單獨證明官方來源或軟體可信。首 N 行屬順序樣本，不得推算全球分布或全檔缺失率。

同名或同長度檔案不自動合併；CRC32 可作初篩，完整內容雜湊才能作精確內容去重。正文中提及但本資料夾不存在的來源，標記 NOT_AVAILABLE_FOR_THIS_REVIEW，不能繼承另一份審计的已驗證狀態。文本模型回答只能成為待證主張，不能因模型數量增加而升級證據。

## 各類資料的業務粒度

| 資料 | 應保存的語義 | 禁止推論 | 業務價值及限制 |
|---|---|---|---|
| ISIC | 分類體系、版次、層級、代碼、父節點、說明及包含／排除條件 | 分類節點數就是企業數；有 LEI 就能自動分配產業 | 跨地區產業比較；企業活動映射仍須獨立證據 |
| GLEIF LEI | 法人識別、法定／總部地址、法人及登記狀態分職 | 登記狀態等於公司存續；LEI 覆蓋全部公司 | 身份消歧及對手方核查；以地方工商登記補充覆蓋 |
| RR | 關係型別、方向、有效期、登記與驗證狀態 | 一切關係等於股權、控制或最終實益擁有人 | 集團會計合併關係與曝險分析；按官方型別解碼 |
| REPEX | 未報告父關係的例外類別、原因及日期 | 沒有父关系就是沒有母公司；例外就是資料錯誤 | 關係缺口解釋；與 RR 互補而非用空值冒充完整 |
| SDG 觀測 | 指標、系列、地理、時期、單位、分組維度、來源及發布版次 | World／區域等於 ISO 國家；不同單位直接相加；NA 一律轉零 | 宏觀風險與政策比較；適用性、可比性及修訂需核查 |
| SDG 採集／聯絡表 | 保管機關、採集日程、來源責任鏈 | 聯絡表就是統計值；聯絡人就是公司名錄 | 來源治理與時效核查；本輪不再發布联系人明細 |
| 宇航／AI 平臺文本 | 產品、廠商、公開功能、部署層、證據日期 | 採購合同证明內部技術棧；廣告性能證明獨立實測 | 分層技術選型；任務適配、性能與合規逐案核定 |

[GLEIF 官方字典](https://www.gleif.org/en/lei-data/access-and-use-lei-data/gleif-data-dictionary)與[關係資料](https://www.gleif.org/en/lei-data/gleif-concatenated-file/download-the-concatenated-file)支撐身份、會計合併關係與例外分職。[UN SDG 採集資訊](https://unstats.un.org/sdgs/dataContacts/)與觀測資料庫用途分開。[ISIC 官方資料](https://unstats.un.org/unsd/classifications/Econ/isic)須保留版本與說明，不能只按產業名稱模糊配對。

## 處理效率與可重放

大檔採分塊雜湊與串流 CSV，不用 read_bytes／全檔 JSON 載入。解壓前檢查檔案數、總展開大小與格式；解碼、結構校验及統計分開，避免為一份檔案重複建立巨大資料副本。可解析記錄須對賬 read = accepted + rejected；拒收保存原因與來源列定位，不吞掉失敗。

真正入庫時以批次交易、版本化斷言與資料血統保存歷史；資料模型包含 source、dataset_release、entity_identifier、typed_relationship、classification_assignment、observation 及 coverage。有效時間與記錄時間分開；未知分母保持 NULL，已讀文件或網址不能當作全球覆蓋分母。增量／撤销亦須驗證，不能將快照直接累加。

## 允許採用與驗收

GLEIF 資料的 CC0 條款須以[官方資料使用條款](https://www.gleif.org/en/meta/lei-data-terms-of-use)及具體資料範圍核定；UN 各資料集分別核對條款。資料使用、再發布及模型訓練許可分職。本輪明確授權僅採用精華，即使資料可商業使用，也不能據此自行匯入下載文件。

可操作狀態至少包含 LOCAL_FILE_FOUND、FORMAT_CHECKED、FULL_STREAM_CHECKED、SEMANTICS_REVIEWED、ORIGIN_AUTHENTICATED 及 RECORDS_IMPORTED。各項為独立事實；不得把全文讀取或雜湊完成改寫成全部主張真實、全部欄位語義已核定、全世界資料已收齊。
