# 全球分類與法人官方下載障礙實測審計 v2.2.0
日期：2026-10-08；範圍：僅診斷官方公開網站及當前工具環境；未觸及私人網絡或公司服務。

## 已驗證
1. 受限 Python 運行容器內，`socket.getaddrinfo` 對 `unstats.un.org`、`www.gleif.org`、`api.gleif.org`、`www.google.com` 全部回報 `[Errno -3] Temporary failure in name resolution`。`requests.get` 對 UN 與 GLEIF 均因 NameResolutionError 失敗，未建立 HTTPS 連線。
2. 獨立網頁查證通道成功讀取聯合國 ISIC 網頁，頁面列有 Rev.5 的 CSV 結構與 XLSX 說明檔。
3. 同一網頁通道點開 ISIC 官方 CSV 時回報 `400 Unsupported content-type: application/octet-stream`，點開 XLSX 時回報 `400 Unsupported content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`。此訊息是讀取通道對附件格式的限制，**不足以表示來源伺服器拒絕公眾下載**。
4. 可透過網頁查證通道瀏覽 GLEIF Golden Copy 介紹頁，官方記載 Level 1/Level 2 及每日更新／增量機制；GLEIF API 在該網頁通道讀取失敗，未能證實 API 的實際 HTTP 狀態。
5. v2.1.0 SQLite 來源表保持完整，`PRAGMA quick_check` 回報 `ok`；本次沒有往正式資料表寫入模擬法人。

## 因果邊界
- 可以確認：當前 Python 容器存在一般性 DNS 解析失敗；網頁工具無法擷取某些二進位文件。
- 不能確認：UN 有意封鎖下載、地緣政治審查、個人電腦故障、公司 IT 限制或安全機關干預。
- 網頁工具可以閱讀 HTML 但無法擷取 CSV/XLSX，與容器 DNS 失敗是兩條不同故障路徑。

## 官方地址
- 聯合國分類目錄：https://unstats.un.org/unsd/classifications/Econ/isic
- ISIC Rev.5 CSV：https://unstats.un.org/unsd/classifications/Econ/Download/In%20Text/ISIC_Rev_5_english_structure.csv
- ISIC Rev.5 XLSX：https://unstats.un.org/unsd/classifications/Econ/Download/ISIC5_Exp_Notes_19_Aug_2026.xlsx
- GLEIF Golden Copy：https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy

## redteam／critic／killcritic／blindspot
- redteam：禁止更改本機安全控制、停用防護或使用來路不明下載鏡像；保留來源域名與 SHA-256。
- critic：DNS 失敗並非 HTTP 403；工具不支援檔案類型亦非網站禁止訪問。
- killcritic：在獲准使用的獨立 Windows 或其他網絡環境執行隨附只讀診斷，記錄 DNS、HEAD HTTP、Content-Type；必要時用瀏覽器正常手動下載後校驗來源。
- blindspot：代理設定、DNS 過濾、TLS 交握、HTTP 302、CDN、HEAD 方法被禁止、工具下載政策等，均須獨立甄別。

## blueprint／cheatsheet／actionplan
- blueprint：來源發現 → DNS → TCP/TLS → HTTP/重定向 → 檔案讀取 → 雜湊 → 格式驗證 → 正式入庫 → 追溯。
- cheatsheet：DNS_ERROR≠HTTP_403；UNSUPPORTED_MIME≠ACCESS_DENIED；INDEXED≠DOWNLOADED；DOWNLOADED≠VERIFIED。
- actionplan：第一步僅在您有權管理的本機執行 `global_dns_download_diagnostic_v2_2_0.ps1`；第二步通過官方網站正常下載分類文件並核對 SHA-256；第三步使用 v2.1.0 匯入器沙盒驗收；第四步才將正式來源受控寫入資料庫。全球 249 個 ISO 3166-1 地區全部保留，分級標註來源和缺口。
