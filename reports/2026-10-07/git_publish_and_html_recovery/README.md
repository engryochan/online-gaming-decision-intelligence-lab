# HTML 來源補齊與精確輸出

日期：2026-10-08。

`recovery_manifest.json` 列出每份原 HTML、SHA256、QMD、Git 歷史查詢結果及可能的既有 Markdown。QMD 保存現行 HTML 的完整原始位元組，包含腳本、樣式、BOM、換行與所有文字；這是來源快照重建，並不聲稱還原作者原始 Markdown。既有 HTML、既有 QMD 與原有資產均未覆寫。

在專案根目錄執行：

```powershell
python reports/2026-10-07/git_publish_and_html_recovery/recover_html.py --render
```

輸出位於本資料夾的 `preview/`，保留原相對路徑。`byte_exact_acceptance.json` 逐項記錄與現行原檔的位元組比較及 SHA256。腳本直接讀取 QMD 的完整 HTML 區塊，修改區塊會實際改變輸出，不會被隱藏副本蓋回。編輯後與原檔不一致會使驗收失敗，應審閱差異，不要偽造通過。

一般 `quarto render` 會產生 Quarto 文件外框，不能作為逐位元相同的輸出方式。精確輸出須使用上述附帶渲染器。原 HTML 相鄰資產仍由原位置提供；預覽輸出主要用於內容與位元組驗收，並非獨立打包網站。

下載快照、存檔及模板也另外保留為 QMD，不能視為已核實的研究報告。含憑證候選欄位的 ASX 快照沒有建立衍生 QMD；原檔已存在於較早遠端歷史，本輪不修改、不新增副本，也未重寫歷史。

大型 SQLite 使用 Git LFS，資料庫內容完整保留。研究目錄被舊規則忽略的 CSV 另行檢查後納入；環境、密碼檔、快取及 IDE 執行狀態不納入。

首次推送被 GitHub 秘密掃描阻擋：`raw/euronext_script_63.js` 含 Mapbox Secret Access Token。該腳本完整保留在本機，加入忽略清單，從本輪尚未發布的提交中排除；不繞過 GitHub 保護。掃描結果只能反映所用規則，不代表形式化證明所有格式的憑證都不存在。
