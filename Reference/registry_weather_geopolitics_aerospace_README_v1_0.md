# 全球249國家／地區氣象、地緣與宇航註冊表｜v1.0.0

**基準日期**：2026-10-08。**範圍**：ISO 3166-1 技術註冊表共249行；不是249個主權國家。

## 建置成果

- `registry_weather_geopolitics_aerospace_iso3166_v1_0.csv`：**249**個國家／地區，每列保留原始13欄並擴展26欄。
- `registry_weather_geopolitics_aerospace_providers_v1_0.csv`：**31**筆去重的供應商／官方來源產品，標明定價模式、來源及未知限制。
- Excel活頁簿提供`ISO_249`、`Providers`、`Readme`。

## 注意：不能錯當已實證的欄位

本次未在249個法域逐個請求 API、驗證雷達與警報或翻閱每個國家的氣象主管機關。任何`*_country_status`是**候選／全球服務宣稱**，非逐國可用性的已驗證結果；`service_verification=NOT_TESTED`。本次也不連接公司生產線／博彩系統。

`NULL/空值=未查得`；`UNKNOWN=尚未證實`；`NOT_TESTED=未做現地或API試驗`。不以國別相關性代替價格／授權證據。

## 校驗與來源

- ISO正式國家代碼：https://www.iso.org/iso-3166-country-codes.html
- ISO國家／地區對照：https://unece.org/trade/cefact/unlocode-code-list-country-and-territory
- WMO會員（193=187國家+6地區）：https://contacts.wmo.int/members/
- 官方 NMHS 會員檔：https://community.wmo.int/en/members/profiles
- Weather Company API費率：https://www.weathercompany.com/weather-data-apis/weather-data-apis-packages-pricing/
- Open-Meteo API費率：https://open-meteo.com/en/pricing

## 後續驗收規格

1. 使用官方 ISO/UN 資料逐列映射 UN M49，針對歷史名稱更新記錄來源版本。
2. 使用WMO國別檔解析 NMHS 官方名稱及網站，分別審核國家、屬地及非會員。
3. 針對每個供應商、每個 ISO 對象收集授權、支付幣種、服務條款、生效日期和本地法規。
4. 以合法授權測試的獨立抽樣坐標驗證API、模型覆蓋、觀測密度及本地警報。
5. 最終以預報誤差（CRPS/MAE/RMSE）、警報 POD/FAR、延遲、SLA、成本和授權做多目標採購評估。

## 版本原則

新增欄位不覆蓋原始國家代碼表；證據升級必附鏈結與日期，並保留更正紀錄。
