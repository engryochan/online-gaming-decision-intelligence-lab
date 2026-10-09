# weather.com 氣象服務生態與全球頂尖競爭對手盤點

Oct 9, 2026 · @黄联富

weather.com 由 The Weather Company LLC 營運，2024 年 2 月自 IBM 轉手私募基金 Francisco Partners 成為獨立公司；其數據以航空、媒體、廣告、政府與國防為主要企業市場，自助式 Weather Data API 標準版月費 500 美元、企業版議價。對照 ISO 3166-1 的 249 個國家／地區，商業氣象供應商普遍宣稱全球網格覆蓋，但真正逐國落地的地面觀測與預警解析度差距極大；地緣戰略、宇航與軍工層的氣象產品則幾乎全為付費或政府採購，僅各國官方氣象機構與歐盟 Copernicus 一線為免費開放。

## 一、weather.com 的主體現況

weather.com 不是一家獨立公司的名字，而是 The Weather Company LLC 旗下三個消費端品牌之一（另兩個為 Weather Underground、Storm Radar）。釐清主體，才能判斷誰是真正的對手。

| 項目 | 現況 |
| --- | --- |
| 法人主體 | The Weather Company LLC（美國，亞特蘭大） |
| 所有權 | 私募基金 Francisco Partners；2023 年 8 月簽約自 IBM 收購，2024 年 2 月完成交割（IBM 2016 年原以逾 20 億美元購入） |
| 不含在內 | The Weather Channel 有線電視頻道（另一主體 Allen Media Group） |
| IBM 殘留關係 | IBM 保留 Environmental Intelligence Suite，續用 TWC 數據 |
| 消費端規模 | 月活約 3.6 億至 4.15 億人 |
| 企業客戶 | 逾 2,000 家；航空、媒體、廣告、政府與國防 |
| 核心引擎 | GRAF 全球高解析模式 + Forecast on Demand（FOD），日產約 250 億筆預報、覆蓋 22 億個位置點 |
| 觀測網 | 全球逾 40 萬個氣象站（含美國約 40 萬個人氣象站 PWS 網絡） |
| 模式集成 | 日吸收 PB 級資料、驅動逾 100 個預報模式，AI／ML 加「human over the loop」 |
| 第三方評比 | ForecastWatch 連續八年評為全球最準（由 TWC 自行委託，非獨立採購） |

**產品線分層**：Weather Data APIs（自助與企業）、Aviation（Pilotbrief、Maverick Dispatch／Ground Ops／WXAlert、Fusion、Weather Forecast Services，日支援約 25,000 架次）、Media（Max 系列廣電圖形平臺、ReelSphere）、Advertising（Weather Targeting 天氣觸發廣告）、Government & Defense。

> 判讀：TWC 的護城河不在模式本身（模式多為公開 NWP 加工），而在 **消費端流量 × 廣電 Max 平臺裝機 × 航空簽派軟體黏著度 × 廣告變現**。要與之競爭，單靠 API 準度不夠。

## 二、誰在簽購 weather.com／TWC 的氣象數據

TWC 不公開完整客戶名冊，下表只列可查證或由官方自述確認者；標「已停用」者為重要的歷史轉折，說明這條供應鏈並不穩固。

| 類別 | 對象 | 狀態 | 說明 |
| --- | --- | --- | --- |
| 操作系統／手機 | Samsung Galaxy（Android、Tizen）原生天氣小工具 | 長期合作 | 2017 年起 TWC 成為 Samsung 指定天氣數據供應方 |
| 操作系統／手機 | Apple iOS 內建「天氣」App | **已停用** | 2014 年由 Yahoo 改用 The Weather Channel 數據；2020 年 Apple 收購 Dark Sky，2022 年起改用自家 WeatherKit |
| 搜尋／地圖 | Google Weather、Google Maps 天氣層 | 非 TWC | Google 改用自家 WeatherNext／GraphCast，歷史上地圖層曾用 OpenWeather |
| 航空 | British Airways、Breeze Airways 等 | 官方具名 | 使用 Aviation API 與 Pilotbrief／Maverick 系列，逾 180 支航空 API |
| 航空 | 全球多家大型航空公司 | 必須走企業合約 | TWC 定價頁明示「major airlines must enroll in a custom Enterprise plan」 |
| 體育 | NASCAR | 官方案例 | 賽事排程與安全決策統一使用 TWC |
| 廣電 | 全球大量電視臺 | 裝機型 | Max Cloud／Max Studio／Max Storm 等廣電圖形系統 |
| 雲與算力 | AWS（含 SageMaker MLOps）、NVIDIA | 供應方而非客戶 | TWC 生成式 AI 與模式訓練基礎設施 |
| 軟體巨頭 | IBM | 續用方 | Environmental Intelligence Suite 續採 TWC 數據 |
| 其他垂直 | 農業巨頭、智慧家居系統、道路救援 | 官方泛稱 | TWC 自述「major global airlines, agricultural giants, sports leagues, and smart home systems」 |

**三個值得注意的事實**

1. Apple 的退出（2022）與 Google 的自建（WeatherNext）說明：**平臺級客戶正在從「買數據」轉為「自建模式」**，這是 TWC 最大的結構性風險。
2. Samsung 仍是 TWC 最大的裝機型渠道，但 Samsung Galaxy Watch Studio 另採用 OpenWeather，顯示同一集團內多源並行。
3. 政府與國防（Government & Defense）是 TWC 近年主推的新增長線，與 NOAA／美太空軍的商業數據採購趨勢同向。

## 三、TWC 自身的收費結構（基準線）

| 方案 | 額度 | 價格 | 內容 |
| --- | --- | --- | --- |
| Free trial | 30 天、每日 5 萬次、每分鐘 100 次 | 免費（限企業客戶，須審核） | 實況、15 天逐日／逐時／日內預報、生活指數、預警、天氣影像 |
| Standard | 每月 100 萬次呼叫，年約 | **500 美元／月** | 同上全套標準資料 |
| Enterprise | 議價 | 議價 | 加購：機率預報、閃電落雷、熱帶氣旋、清洗後歷史資料、History on Demand、季節與次季節預報、強對流、再生能源、地面運輸、媒體方案、客製洞察、專屬客戶經理 |

規模感：TWC 自稱每月處理約 6 兆次 API 呼叫。按 Standard 的單價換算，100 萬次／500 美元 ≈ 每千次 0.5 美元，屬企業級定價區間的中高段——OpenWeather、Open-Meteo 等同量級低一至兩個數量級，差價買的是準度評比、歷史清洗度與航空／廣電的垂直軟體。

## 四、全球頂尖商業氣象競爭對手

「覆蓋國數」一欄的判讀規則：*全球網格* 指以 ECMWF／GFS 等全球模式插值，理論上涵蓋 ISO 3166-1 全部 249 個國家與地區（含南極、無人島嶼）；*逐國落地* 指另有地面觀測、雷達或官方預警對接。只有極少數供應商兩者兼具。

### 4.1 第一梯隊：全棧型（數據 + 垂直軟體 + 消費端）

| 供應商 | 母體／國別 | 強項 | 覆蓋 | 收費 |
| --- | --- | --- | --- | --- |
| The Weather Company | Francisco Partners（美） | 準度評比、航空 Pilotbrief／Maverick、廣電 Max、天氣廣告 | 全球網格 + 美國 PWS 40 萬站 | 付費；500 美元／月起 |
| AccuWeather | 私人控股（美） | 分鐘級降水 MinuteCast、SkyGuard 預警服務、授權廣泛 | 全球網格 + 逾百國在地化 | 付費；入門約 12 美元／月，企業議價 |
| DTN | TBG AG（美／挪威資本） | 併購 MeteoGroup，農業、能源、航運、航空營運情報 | 全球；歐洲在地化最強 | 付費，企業議價（無自助） |
| Vaisala / Xweather | Vaisala Oyj（芬蘭） | 自有全球閃電偵測網（GLD360）、道路氣象、硬體+數據一體 | 全球；閃電為真正全球實測 | 付費，企業級 |
| StormGeo | Alfa Laval（挪威） | 航運氣象導航、離岸能源、風電 | 全球海域 | 付費，企業議價 |
| Weathernews Inc. | 上市（日本，TSE 4825） | 全球最大民間氣象公司之一；航運 OSR、鐵道、零售 | 全球；日本最密 | 付費 |
| Baron Weather | 私人（美） | 廣電雷達圖形、關鍵天氣基礎設施、政府雷達系統出口 | 全球 + 國家級雷達整合 | 付費 |
| Earth Networks | 私人（美） | 全球閃電網 ENTLN、早期預警系統出口至新興市場政府 | 全球閃電 | 付費 |

### 4.2 第二梯隊：API 原生與開發者市場

| 供應商 | 國別 | 免費層 | 付費起點 | 備註 |
| --- | --- | --- | --- | --- |
| Tomorrow.io | 美 | 有（每日 500 次／每月方案限制） | 企業議價 | 自有衛星星座（雷達 + 微波探空）；客戶含 Delta、JetBlue、Uber、Ford；美國防部 STRATFI 合約 |
| Meteomatics | 瑞士 | 僅 14 天試用 | 全議價 | 1,800+ 參數、EURO1k／US1k 1 公里模式、Meteodrone 探空無人機；科研與能源最強 |
| OpenWeather | 英 | 每月 100 萬次 | 約 40 美元／月；One Call 超量 0.0015 美元／次 | 逾 200 萬客戶；Google Ads 天氣投放、Samsung Galaxy Watch Studio |
| Visual Crossing | 美 | 每日 1,000 筆 | 35 美元／月，或約 0.0001 美元／筆 | 50 年以上歷史檔案最深 |
| Weatherbit | 美 | 每日 50–500 次 | 約 45 美元／月 | 農業與能源 API |
| WeatherAPI.com | 美 | 每月 100 萬次 | 低價階梯 | 預報天期較短 |
| Weatherstack (apilayer) | 奧地利／英 | 每月 1,000 次 | 階梯訂閱 | 歷史 2008 年起、海事 API |
| Open-Meteo | 德（開源） | 每日 1 萬次、**免金鑰** | 商用訂閱選購 | 直供 ECMWF／ICON／GFS 開放資料；非商業用途完全免費 |
| Pirate Weather | 加（開源） | 有 | 自願贊助 | Dark Sky API 相容替代品 |
| Ambee | 印度 | 有 | 訂閱 | 空氣品質、花粉、火災等環境層 |
| Meteoblue | 瑞士 | 有限 | 訂閱 | 高解析降尺度、歷史模擬 |
| Foreca | 芬蘭 | 無 | 企業議價 | 北歐與亞洲廣電、OEM 授權 |
| Jua.ai | 瑞士 | 無 | 企業議價 | EPT-2 自研基礎模型，能源交易專用，宣稱風／溫優於 ECMWF HRES |
| Climavision | 美 | 無 | 企業議價 | 自建私人 X 波段雷達網補 NEXRAD 空隙 |
| Brightband | 美 | 部分開放 | 議價 | 以 NVIDIA Earth-2 Medium Range 每日運行全球預報 |

### 4.3 中國與亞太陣營

| 供應商 | 主體 | 定位 | 收費 |
| --- | --- | --- | --- |
| 中國氣象局／風雲衛星 | 國家級 | FY-2／FY-3／FY-4 系列，向「一帶一路」國家免費提供衛星數據服務 | 公共數據免費 |
| 和風天氣 QWeather | 北京彩雲（ColorfulClouds 系） | 開發者 API 市場領導者，5×5 公里全球網格、分鐘級雷達、99.99% SLA | 免費開發版 + 付費訂閱 |
| 彩云天气 Caiyun | 彩雲科技 | 分鐘級降水起家，v2.6 API；需審核 | 免費額度 + 付費 |
| 心知天气 Seniverse | 心知科技 | 企業 API、車載與 IoT | 付費為主 |
| 墨迹天气 MoJi | 上市 | 消費端流量最大，廣告變現模式與 TWC 同構 | 消費免費、廣告變現 |
| 華風愛科 Huafeng-AccuWeather | 中國氣象局 × AccuWeather 合資 | 「中國天氣」App 與官方數據商業化 | 付費授權 |
| 高德／騰訊天氣 API | 阿里／騰訊 | 地圖生態內嵌 | 免費額度 + 付費 |
| Weathernews（日）、Skymet（印）、Kweather（韓） | 民間 | 各自本土最密觀測網 | 付費 |

> 這一層的戰略意涵：中國的氣象 API 已把 **MCP／AI Agent 介面** 當成標配（和風天氣已提供 19 項天氣 MCP 工具、支援 Claude Desktop 與 Cursor），在「給 AI 用的氣象數據」這條新賽道上，進度不落後於歐美。

## 五、國家級官方機構：真正的全球基礎層

商業供應商幾乎全部站在這一層之上。它們才是對 249 國 ISO 覆蓋的實際擁有者，而且多數免費。

| 機構 | 轄區 | 關鍵資產 | 收費 |
| --- | --- | --- | --- |
| ECMWF | 歐洲 35 國共同體 | IFS（HRES／ENS）+ AIFS；全球公認中期預報標竿 | **開放資料免費**（2022 年起全量開放）；即時高解析仍有成員國商業條款 |
| NOAA / NWS（美） | 全球 + 美國 | GFS、HRRR、GOES 衛星、api.weather.gov | **完全免費、無限制** |
| EUMETSAT | 歐洲 30 成員國 | Meteosat、MTG、Metop | 多數免費註冊取用 |
| Copernicus（C3S／CAMS／CDS） | 歐盟 | ERA5 再分析、空氣品質、氣候投影 | 免費 |
| Met Office（英） | 全球 | 全球模式、DataPoint／DataHub | 混合：部分開放，商業產品付費 |
| DWD（德） | 全球 | ICON 模式、Open Data Server | **免費開放** |
| Météo-France | 全球 | ARPEGE／AROME | 2024 年起主要公共資料免費開放 |
| 中國氣象局 CMA | 全球 | 風雲衛星、CMA-GFS；向多國免費提供衛星服務 | 公共免費，商業授權另計 |
| JMA（日） | 亞太 | 向日葵 Himawari-8／9、全球模式 | 區域內多為免費 |
| KMA（韓）、IMD（印）、BoM（澳）、ECCC（加）、Roshydromet（俄）、INMET（巴） | 各國 | 本國觀測與預警權威 | 多數免費或象徵性收費 |
| WMO | 193 會員國 | GTS 全球電信系統、Global Basic Observing Network | 會員國間交換，非商業 |

**覆蓋現實**：WMO 有 193 個會員國，ISO 3166-1 有 249 個條目。差額的 56 個條目是屬地、海外領地與無人地區（南極 AQ、布威島 BV、赫德島 HM 等）。沒有任何商業供應商對這 56 個條目有逐國落地服務；它們的「全球覆蓋」在這些格點上，等同於全球模式的插值結果。

## 六、AI 氣象大模型：最前沿的那一層

這是 2024–2026 年整個產業的斷層線。它把預報成本降了三到四個數量級，直接威脅「賣預報數據」這門生意。

| 模型 | 出處 | 狀態（2026） | 權重／取用 |
| --- | --- | --- | --- |
| AIFS Single / AIFS ENS | ECMWF | 2025 年 2 月轉全面業務化，2026 年 5 月升級；首個官方機構業務化 AI 模式 | **開放授權權重**，Hugging Face 可下載；輸出隨開放資料免費 |
| WeatherNext 2 | Google DeepMind | 2025 年發布，已開源 | 開源權重；Google Weather API 商用付費 |
| GenCast | Google DeepMind | 機率式 AI 集合預報 | 研究開放 |
| GraphCast | Google DeepMind | 奠基之作；ECMWF 2026 年停止日常並行運行（已被 AIFS 超越） | 開源 |
| Aurora / Aurora 1.5 | Microsoft Research | 2026 年 7 月擴充為地球系統基礎模型；整合 Azure | 開放權重於 Hugging Face |
| Pangu-Weather 盤古氣象 | 華為雲 | Nature 2023；較傳統集合快約 10,000 倍；無降水輸出為其限制 | 公開；華為雲商用 |
| FengWu 風烏 | 上海人工智能實驗室 | 持續迭代 | 開放 |
| FuXi 伏羲 | 復旦大學 | 次季節延伸 | 開放 |
| Earth-2（Atlas／StormScope／HealDA／CorrDiff／FourCastNet） | NVIDIA | 2026 年 1 月發布「全球首個全開放 AI 氣象軟體棧」：15 天中期、公里級臨近預報、GPU 全球資料同化 | **商用與非商用皆可授權**；需 NVIDIA GPU |
| AIGFS | NOAA | 美方官方 AI 全球模式，側重氣旋路徑 | 免費 |
| EPT-2 | Jua.ai | 宣稱在風、溫、SSRD 上全程優於 ECMWF HRES、Aurora、GraphCast | 商用付費 |

**對 TWC 的意涵**：TWC 的 GRAF 與 FOD 仍是物理模式 + AI 後處理的混合架構。當 ECMWF 的 AIFS 權重與 NVIDIA 的 Earth-2 棧都能免費取得、而能源商（TotalEnergies 已具名採用 Earth-2）與國家氣象局（以色列氣象局用 Earth-2 在 2.5 公里解析度省下 90% 算力）可自行運行時，**「準度」本身正在快速商品化**。剩下的差異化只有觀測資產（閃電網、私人雷達、自有衛星）與垂直軟體。

## 七、地緣政治與戰略情報層

這一層與氣象層的交會點是「風險情報平臺」：企業買的是一張把政治動盪、安全事件、極端天氣、供應鏈中斷疊在同一張地圖上的訂閱。TWC 的 Government & Defense 線正在往這裡靠。

| 供應商 | 國別 | 定位 | 收費 |
| --- | --- | --- | --- |
| RANE Network（含 Stratfor Worldview） | 美 | 地緣 + 網安 + 合規 + 安全四合一；已上 Bloomberg Terminal | 個人 Worldview 約 199–349 美元／年；企業方案業界估逾 5 萬美元／年 |
| Janes | 英 | 國防裝備、兵力編成、軍工開源情報權威 | 付費，企業議價 |
| Verisk Maplecroft | 英 | 量化國家風險指數（政治、ESG、人權、氣候），可直接接入投組 | 付費訂閱 |
| Control Risks | 英 | 顧問 + 情報混合 | 付費 |
| Dragonfly Intelligence | 英 | 地緣與安全情報訂閱 | 付費 |
| Sibylline | 英 | 戰略風險顧問 | 付費 |
| Crisis24（GardaWorld） | 加／美 | 旅外人員安全、即時事件告警 | 付費 |
| Seerist | 美 | AI + 分析師的威脅風險平臺 | 付費 |
| Oxford Analytica | 英 | 專家網絡式宏觀地緣分析 | 付費 |
| Eurasia Group | 美 | 政治風險顧問，年度 Top Risks | 報告部分免費、服務付費 |
| Economist Intelligence Unit | 英 | 國家風險與預測 | 付費 |
| Dataminr / Recorded Future / Factal / Samdesk | 美 | 即時事件偵測（含極端天氣觸發） | 付費 |
| ACLED / Liveuamap | 美／烏 | 衝突事件資料庫與地圖 | **學術與非商業免費**；商業授權付費 |
| Palantir Foundry / Gotham | 美 | 情報融合平臺（含氣象圖層） | 付費，政府級合約 |
| S&P Global、Verisk、Moody's RMS | 美 | 巨災模型、氣候實體風險定價 | 付費 |

> 唯一成規模的免費者是 ACLED（非商業用途）與各國政府開放的衝突／制裁資料。這一層沒有「免費增值」文化。

## 八、宇航與軍工氣象生態產業鏈

### 8.1 美國軍用氣象衛星架構轉換（DMSP 退役中）

| 計畫 | 承包商 | 狀態 | 用途 |
| --- | --- | --- | --- |
| DMSP（1960 年代起） | Lockheed Martin、Northrop Grumman | 原定 2026 年 9 月終止服務；FY2026 國防授權法要求延役至 **至少 2028 年** | 全球軍用雲圖、微波成像 |
| WSF-M（後續微波） | BAE Systems Space & Mission Systems（原 Ball Aerospace） | SV-1 於 2024 年 4 月發射、2025 年驗收；SV-2 排程 2026–2028 | 海面風、熱帶氣旋強度、雪深、海冰、土壤濕度 + 帶電粒子「太空天氣」感測 |
| EWS（電光／紅外氣象系統） | General Atomics Electromagnetic Systems（主星）、Orion Space Solutions（立方衛星驗證）、Raytheon Intelligence & Space（早期 OTA 6,700 萬美元） | 首星 2026–2027、次星 2028 | 雲層成像與軍事任務規劃 |
| EWS-G（地球同步） | Boeing（原 GOES 平臺） | 印度洋區覆蓋至 2030 年後 | 經澳洲 Dongara 地面站回傳 |

### 8.2 NOAA 商業氣象數據採購（2026 年 9 月擴編至 14 家，7 類）

| 資料類別 | 獲選供應商 |
| --- | --- |
| GNSS 掩星（大氣廓線 + 電離層太空天氣） | Spire Global、PlanetiQ、Ethereal Space、Precursor SPC、Tomorrow.io |
| GNSS 反射（陸海表面） | Spire Global、Tomorrow.io、Muon Space |
| 微波探空（含超光譜溫濕廓線） | Spire Global、Tomorrow.io、BAE Systems Space & Mission Systems、Weather Stream |
| 多光譜成像（含微光與野火） | Ethereal Space、Tomorrow.io、Muon Space、Hydrosat、Tropical Weather Analytics |
| 熱層中性密度（軌道預測） | Spire Global、PlanetiQ、Ethereal Space、SpaceX |

### 8.3 其餘生態鏈角色

| 環節 | 代表企業 | 收費 |
| --- | --- | --- |
| 衛星平臺與感測器製造 | Lockheed Martin、Northrop Grumman、L3Harris（GOES 成像儀）、BAE、Airbus Defence and Space、Thales Alenia Space、General Atomics | 政府合約 |
| 商業遙測與 GEOINT | Maxar Intelligence、Planet Labs、BlackSky、ICEYE、Satellogic、Ursa Space、EarthDaily | 付費訂閱／任務 |
| 系統整合與地面段 | Leidos、Peraton、Jacobs、SAIC、Booz Allen | 政府合約 |
| 太空天氣專業 | NOAA SWPC（免費）、ESA Space Weather Service Network（免費）、Spire、Atmospheric & Space Technology Research Associates | 混合 |
| 海上與離岸作業 | StormGeo、DTN、Fugro、Metocean Solutions | 付費 |

> 結構判讀：軍工層的氣象採購正從 **自建專屬衛星** 轉向 **政府出題、商業星座供料**。Tomorrow.io 是唯一同時出現在「開發者 API」「NOAA 五類採購」「美國防部 STRATFI」三張名單上的公司——這是目前最接近「新一代 The Weather Company」的對手。

## 九、收費總覽、249 國覆蓋落差與來源

### 9.1 收費與否一覽

| 層級 | 免費 | 免費增值 | 純付費／政府合約 |
| --- | --- | --- | --- |
| 官方氣象 | NOAA/NWS、DWD、Copernicus、ECMWF 開放資料、CMA 公共數據、多數 NMHS | Met Office、Météo-France（部分） | 各國商業授權部門 |
| 開發者 API | Open-Meteo（非商業）、Pirate Weather | OpenWeather、WeatherAPI、Visual Crossing、Weatherbit、Tomorrow.io、和風天氣、彩云 | Meteomatics、Foreca、Jua、Climavision |
| 全棧商業 | 無 | AccuWeather（入門級） | **The Weather Company**、DTN、Xweather、StormGeo、Weathernews、Baron |
| AI 模型權重 | AIFS、Aurora、WeatherNext 2、GraphCast、Pangu、FengWu、FuXi、Earth-2 | — | Jua EPT-2、各家託管推論服務 |
| 地緣戰略情報 | ACLED（非商業） | — | 全部其餘 |
| 宇航／軍工氣象 | NOAA SWPC、ESA SWE（太空天氣） | — | 全部其餘（政府採購為主） |

### 9.2 對 249 國清單的落差判讀

專案中的 `registry_country_area_iso3166_m49_e164_20261004.csv` 列出 249 個 ISO 3166-1 條目。按這份清單核對氣象服務覆蓋，可切成四級：

1. **逐國落地（約 100–130 個）** — 有本國 NMHS、雷達或官方預警對接。商業供應商的預警（watches/warnings）API 真正可用的範圍大致在此。
2. **全球模式插值（其餘全部）** — 所有宣稱「全球覆蓋」的供應商在此層等價，差異只在降尺度方法。
3. **屬地與海外領地（約 40–50 個）** — 由宗主國機構代管（如 Météo-France 覆蓋 GP／MQ／RE／YT／NC／PF；NOAA 覆蓋 PR／VI／GU／AS／MP）。供應商的「國家」欄位常與 ISO 條目對不上，需以 `associated_or_administering_state_iso3` 欄位做映射。
4. **無常住人口／極地（AQ、BV、HM、TF、UM、GS 等）** — 僅有模式格點與衛星，無任何商業落地服務。`inhabited_status` 欄位可直接用來把這批排除在覆蓋率分母外。

> 建議的量化作法：以該 CSV 的 `iso_alpha2` 為主鍵，為每家供應商建一張 249 列的覆蓋矩陣，欄位分 `grid_only / observations / radar / official_alerts / localized_app`，再用 `inhabited_status` 與 `constitutional_relationship_type` 做加權，才能得出可比的「真實覆蓋率」，而不是各家行銷頁上的「全球」二字。

### 9.3 已核實的主要來源

- [The Weather Company — Weather Data API 方案與定價](https://www.weathercompany.com/weather-data-apis/weather-data-apis-packages-pricing/)
- [The Weather Company — 關於我們與準度說明](https://www.weathercompany.com/proven-accuracy/)
- [Francisco Partners 完成收購 The Weather Company](https://www.franciscopartners.com/media/francisco-partners-completes-acquisition-of-the-weather-company)
- [TechCrunch：IBM 出售 The Weather Company 資產](https://techcrunch.com/2023/08/22/ibm-sells-the-weather-company-assets-to-francisco-partners)
- [The Weather Company × Samsung 策略聯盟（PRNewswire）](https://www.prnewswire.com/news-releases/the-weather-company-expands-strategic-alliance-with-samsung-to-bring-worlds-most-accurate-weather-data-to-samsung-devices-300431130.html)
- [Wikipedia：Apple 天氣 App 的數據來源變遷](<https://en.wikipedia.org/wiki/Weather_(Apple)>)
- [ECMWF：告別外部 AI 模式（AIFS 現況）](https://www.ecmwf.int/en/about/media-centre/aifs-blog/2026/farewell-external-ai-models)
- [SiliconANGLE：NVIDIA 發布 Earth-2 開放 AI 氣象模式](https://siliconangle.com/2026/01/26/nvidia-launches-earth-2-open-ai-weather-forecast-models-tools/)
- [Via Satellite：NOAA 擴編 14 家商業氣象數據供應商](https://www.satellitetoday.com/imagery-and-sensing/2026/09/11/noaa-names-14-commercial-providers-for-weather-data-contract/)
- [Air & Space Forces：太空軍延役 DMSP 至 2028 年](https://www.airandspaceforces.com/space-force-legacy-weather-sats-2028-replacements/)
- [Air & Space Forces：WSF-M 計畫檔案](https://www.airandspaceforces.com/weapons/wsf-m/)
- [Air & Space Forces：EWS-G 計畫檔案](https://www.airandspaceforces.com/weapons/ews-g/)
- [RANE Worldview 訂閱方案](https://www.ranenetwork.com/worldview-subscribe)
- [Xweather（Vaisala）：2026 年生產級氣象 API 評比](https://www.xweather.com/blog/top-weather-apis-for-production-2026)

**未核實項**：TWC 企業方案實際成交價、各家供應商逐國落地數的官方確認值，以及中國與俄羅斯軍工氣象鏈的內部採購結構，均無公開可引來源，本文未作數字推斷。
