# QMD 檢查、修復、渲染與事實查證（2026-10-15）

最新營運與監管續核：累計101項（94項限定支持、2項矛盾、5項證據不足），本批11項見 `operations_20261016_receipt.json`。修正 Bet Behind Pro 的 bot 玩家／真人荷官分類，SOFTSWISS 成果明示公司自報；75.94%與所述 Smartico RL／bandit 部署及收購即技術驗證的推論均缺乏已讀證據，不再作已驗證基線。MGA 章程與 AI Act 分類依窄義官方文字判讀，沒有把自願章程當成法律豁免。下列90項及86項是歷史進度。可用 `validate_current_delivery.py` 核對現行源稿、輸出、壓縮清單與台帳；它只寫回執，不改正文或還原文件。

最新裁決：累計90項，其中87項在限定範圍獲支持、1項與所讀來源矛盾、2項證據不足。百家樂 AI 自動化報告另加有來源的首發品類、B2B推出與排他名單裁決；保留原 HTML 全部位元組，以快照＋Markdown增補模式顯示。詳見 `ai_dealer_20261016_receipt.json`。以下86項為前一批進度，不代表本輪最終數量。

2026-10-16 續核：台帳累計86項（85項在限定範圍獲支持、1項證據不足），本次新增16項，見 `hardware_review_20261016_receipt.json`。Gazebo 官方子文件已能支持模擬器用途；Orekit 官方頁仍遇存取挑戰。具名產品僅核對官方用途與類型，未將臨床研究宣傳當作監管許可或療效證明。`rendered_passages_20261016_manifest.json` 與相應壓縮 JSONL 另擴充358份閱讀版（含 HTML 快照）的段落／表格列待查清單；不以段落數冒充事實數，不宣稱完整原子主張抽取。最新查證日期與驗收在索引及 `current_acceptance.json` 顯示。

閱讀版清單包含歷史副本的重複內容，全部標為 `UNREVIEWED_PASSAGE`；不能以台帳數除以段落數計算查證完成率。清單記錄每份 HTML 與源稿雜湊及 XPath，現行數量與壓縮資料雜湊見 manifest。連結統計亦已釐清：`repaired_local_links` 是包含重渲染重做的累計操作數，索引改顯示 `unique_navigation_repair_mappings`（按文件、原引用、新引用去重）；790處未解析引用與15處歷史資源缺口仍保留。

初次清單有兩份抽取為零，現已補足：百家樂報告的正文是 `<pre>` 中的 Markdown，已以明示類型納入；SIX 快照的 `<main>` 位於未閉合的外層導覽之下，已優先保留正文。沒有更改原快照的 DOM 或位元組。此修正擴大待查文字覆蓋，不代表這些文字已核實。

最新續輪：外部事實台帳已增至70項（69項在限定範圍獲支持、1項證據不足），新增22項軟件／規範用途核對，見 `software_review_receipt.json`。STAC 與 BCI2000 新取得可讀官方正文，僅在有日期的增補中記錄，不回寫歷史 UNKNOWN。Orekit 與 Gazebo 仍待查。另修正40處指向指定「归档」目錄中完全同名歷史版本的閱讀版連結，未解析引用由830降至790，逐項依據見 `delivery_link_repairs.json` 的 `archive_resolutions`；未修改原快照、未以新版本替代舊版。下文48項及830處為上一輪狀態；現行數量以 `summary.json` 及 `current_acceptance.json` 為準。

從 [index.html](index.html) 開始閱讀。原有 357 份加工作期間新增 1 份，共 358 份 QMD 已生成 HTML；外部事實逐條查證仍未完成。並行新增文件另記於 `late_inputs.json`，不刷新原始基線、不改寫其內容。

目前有 290 份 Quarto HTML、63 份保留位元組的 HTML 快照、5 份「HTML 快照＋Markdown 增補」輸出。全部停用計算執行；未宣稱 R／Python 範例通過執行驗證、PDF 已生成、全部遠端依賴可離線使用或已完成逐頁視覺驗收。

## 源文件修改與保留

11 份既有 QMD 有針對性修改，詳見 `source_changes.json`；首輪為9份，續輪追加全球科技登記與百家樂 AI 自動化報告的有界增補：

- 地緣戰略主報告及百家樂《冊一》加入有來源、有限定範圍的事實裁決。
- B86 修正 ETF 與所有基金的分類差異，保留原始數量，補充逐行重算的旗標重疊數。
- 兩份大型稿僅調整 YAML，使用靜態 Markdown 引擎並關閉程式碼摺疊、工具及語法高亮，避免長路徑與記憶體問題；正文位元組保留。
- 兩份原有快照增補稿修正渲染模式，讓既有 Markdown 增補不再被快照抽取器遺漏。
- 兩份 Swagger UI 快照保留原始 HTML，另從同批保存的 JSON 產生 143／225 個 HTTP 方法與路徑組合的離線索引；不宣稱已重新呼叫接口。

`Reference/Aerospace_Ecosystem_Report.qmd` 沒有改動，`Interlligence` 檔名沒有改名。原有 HTML、資產、歷史 CSV／JSON 及生成器基線沒有覆寫；沒有從 HEAD 恢復刪除文件。修改前的源文件位元組另存於 `original_bytes/`，以 SHA256 命名。

## 驗證回執

- `before.json`：渲染前的 QMD、HTML 與相關資源清單、雜湊及 Git 狀態；CSV 僅記錄路徑及大小，其他類型未全部納入。不是全項目全部文件內容的實質核實。
- `results.json`：逐文件實際渲染結果及源文件雜湊。
- `after_delta.json`：前述基線範圍內的源文件差異。
- `snapshot_acceptance.json`：64 份純快照輸出與源 HTML 區塊一致；4 份混合快照保留原 HTML，另顯示 Markdown 增補。
- `output_validation.json`：生成 HTML 的雜湊及樣式、腳本等資源檢查。
- `delivery_link_repairs.json`：只修改新生成 Quarto HTML 的導覽，不修改原 HTML 快照。QMD 引用導向生成的 HTML，既存資料附件連回同一工作區。歷史副本的部分缺失相對引用，在同名正式稿標題一致且目標確實存在時，使用正式稿的 Reference 目錄解析；不把當期文件冒充凍結的歷史附件。
- `b86_recomputed_counts.json`：兩份原始證券檔共 13,294 行；ETF=Y 5,773 行，Test Issue=Y 37 行，兩者均 Y 2 行，兩者均 N 7,486 行。已與原取得收據的 SHA256 比對。
- `b89_recomputed_counts.json`：4,849 項歷史進度、40 份回應的雜湊及原報告各項數量重新核對一致；不是即時網路重驗或完整名冊證明。

仍有三份歷史網頁快照的 15 個原站資源參照未保存；兩份 API 快照有可讀靜態索引，嫦娥五號頁面正文保留但原站版式不能保證。原文仍有未找到目標的本地引用，逐項列在引用台帳；未虛構缺失附件或把引用缺口當作事實驗收通過。

## 外部事實工作狀態

`verified_facts.json` 逐項記錄本輪讀到的一手來源、具體主張、裁決與適用邊界；某一主張獲支持，不連帶驗證整份文件、所有數值、部署案例、現時股權、認證或國家排名。

`fact_candidates.json` 與 `external_urls.json` 是初步啟發式清單：18,272 段候選文字及 5,067 個網址，並非完整原子主張清單，也不是已核實數量。純 HTML 快照、程式碼及超長行未完整抽成原子主張。其餘逐條外部核實仍待完成，`summary.json` 明確保留 `external_fact_check_complete: false`。

## 重現

使用可用 Python 執行 `audit_render.py`；本機 Quarto 為 1.10.19。腳本隔離源文件，使用停用計算及非自包含 HTML 模式，並將本機 `QUARTO_ESBUILD` 指向現有的 `C:/work/tools/bin/tools/x86_64/esbuild.exe`。失敗的大型稿可用 `retry_large.py` 以短路徑和靜態程式碼版式重試。

之後依序執行 `repair_delivery_links.py`、`check_outputs.py`、`build_index.py`。快照與增補使用 `audit_render.py` 的對應模式，不能把單獨抽取原 HTML 當作混合文件完整渲染。

`apply_addenda.py`、`add_static_api.py` 是本輪增補操作的保留腳本，日常渲染不需要重複套用。所有輸出都在本目錄；大型資料附件保留於原工作區，不能只搬走 `rendered/` 便宣稱交付包完整。

## 最新重新掃描與續核

以使用者最新提交 `d1f93f3` 為掃描基準，保留《冊二》及原 HTML 的已提交更新。全文件雜湊快照見 [rescan20261015b_summary.json](../../2026-10-06/workspace_change_audit/rescan20261015b_summary.json)：14,023 個一般文件、7,219,018,882 位元組，無讀取期間變動；一個 RStudio 工作階段鎖檔因權限無法讀取。掃描器依設計排除其自身回執，並排除 Git 內部與符號連結。這些雜湊不是所有文件內容的實質核實。

`rescan_diagnostics.json` 另列文件類型、358 份獨立 QMD、文字編碼及 JSON 格式候選；暫存鏡像只計入文件類型，不冒充額外源稿。三份 RStudio 日誌為逐行 JSON，逐行通過；無 YAML 的附錄為可渲染引用片段，見 `rescan_candidate_dispositions.json`。診斷不包含所有二進位格式的內部語義驗證。

《冊二》及全球科技登記已重新渲染，其餘沿用源稿雜湊一致的成功結果。最新狀態以 `current_acceptance.json` 為準；`final_acceptance.json` 保留首輪歷史回執。源稿與358份結果雜湊全部一致，歷史資源缺口仍15處、未解析本地引用仍830處。

外部事實台帳現為48項：本次新增14項，47項在限定範圍獲支持、1項證據不足。量子機構與四家科研／半導體機構僅核對公開描述；Layer 7-T 三項核對來自 FDA K242618 特定器材文件，不延伸至長期無線 BCI 系統獲准。Xanadu 主頁本次沒有可讀正文，保留待查。歷史登記 CSV、原196筆、使用者原 HTML 與原宇航報告均未因本次續核而改寫。全量外部事實核實仍未完成。
