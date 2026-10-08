# 全球249國家／地區氣象、地緣、宇航服務名冊 v1.1.0｜審計報告

基準日：2026-10-08

## 完成

- 249 個 ISO3166-1 國家／地區條目；原始主鍵 100% 保留。
- 31 家服務供應商：承襲 v1.0.0 報價表；**本版未逐家重新覆核價格**。
- 75 個 ISO 對象填入氣象機關名稱候選；68 條使用 WMO 世界天氣資訊服務參與機關名錄名稱，7 條名稱為正規化暫列、待官方逐項比對；皆不代表氣象機關網址已驗證。
- 生成 249 × 31 = **7,719 條** country-provider 核驗矩陣；均記為 `NOT_VERIFIED`，絕不冒充開通實證。
- 來源證據表與版本變更日誌。

## 方法邊界

- ISO 249 不是 249 主權國家；WMO 193 會員不等於 193 個 ISO 行項。
- WWIS 收錄的氣象機關名稱可供建檔，但不證明雷達、CAP、商業 API 或國別服務。
- WMO Alerting Authorities 及 SWIC 為索引／警報平台；未驗證特定地區是否持續提供警報。
- 未從 WMO 官網抓取 CSV 檔、未對服務商執行 API 測試：工具環境無法直接取得外站批量檔案，因此明確保留未知。
- 沒有連接 Superset、StarRocks、DolphinScheduler、博彩網站及生產資料。

## 校驗

- ISO-2 非空唯一：PASS。
- 249×31 欄位矩陣：PASS。
- 每筆國別服務狀態不得默認 VERIFIED：PASS。
- 新增列來源標識與承襲原版：PASS。

## 後續必要工作

1. WMO Members 官方 CSV 抓取後以 ISO2 join 校驗 193 會員，並取得 NMS 官網。
2. 逐國官網核實 CAP／雷達及衛星供應範圍。
3. 供應商依產品×法域核實 licence、價格、SLA。
4. 只有合法具授權的測試資料才執行精度或覆蓋測試，測試證據回填個別矩陣列。

## 引證來源

- https://contacts.wmo.int/members/
- https://worldweather.wmo.int/en/members.html
- https://severeweather.wmo.int/
- https://alertingauthority.wmo.int/
