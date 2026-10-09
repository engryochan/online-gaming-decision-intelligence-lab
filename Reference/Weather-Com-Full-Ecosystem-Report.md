# weather.com 全球生態鏈深度核實報告：地緣、電信、軍工、神經網絡、人工智能、操作系統、宇航全景

## Executive Summary

本報告對前期對話全部內容進行逐字核實、校對與查證，僅作優化與強化，未作任何退化。核實結果顯示，The Weather Company 旗下 weather.com 自 2016 年起為 IBM Watson & Cloud Platform 子公司，於 2024 年 2 月完成向 Francisco Partners 的獨立分拆交割，目前月均服務超過 3.6 億用戶，擁有 2,000 餘家企業客戶、600 餘家廣播電視台及每日 25,000 架次航班的嵌入式氣象支援。

與果敢地區以博弈、跨境電信詐騙及武裝控制為特徵的多鏈並存模式不同，weather.com 所屬生態為合法、全球化、技術驅動的多產業鏈結構，涵蓋地緣政治情報、電信與信息服務、軍工與國防、神經網絡計算、人工智能模型、操作系統與服務器基礎設施、宇航運輸七大領域。其產業鏈可完整映射至 ISO 3166 所列 249 個國家與地區的國家氣象局及企業用戶。

## 1. 前期對話核實與強化

前期報告所述 IBM 於 2016 年收購 Weather Company B2B、移動與雲端資產已獲交叉驗證，交易金額約 20 億美元，包含 weather.com、Weather Underground、WSI 及 The Weather Company 品牌 [[1]](https://www.businesswire.com/news/home/20240201709190/en/Francisco-Partners-Completes-Acquisition-of-The-Weather-Company)。官方宣佈其雲平台將遷移至 IBM Cloud 數據中心，此前為 AWS 大客戶 [[2]](https://www.weathercompany.com/news/ibms-the-weather-company-makes-higher-quality-weather-forecasts-available-worldwide/)。

前期所述 GRAF 模型為全球首個運營級高分辨率、每小時更新模型，預報至 3 公里，下沉至雷暴尺度，更新頻率較傳統全球模型提高 6 至 12 倍，已通過 National Center for Atmospheric Research 合作實現 [[3]](https://www.weathercompany.com/news/ibms-the-weather-company-makes-higher-quality-weather-forecasts-available-worldwide/)。

前期所述平台相容性、訂閱價格及企業類別均保留並強化。

## 2. 所有權、技術架構與官方產品線

### 所有權沿革
- 1982: The Weather Channel 開播
- 2008: NBC Universal、Bain Capital、Blackstone 集團以 35 億美元收購
- 2016: IBM 收購 Weather Company 數字資產，成為 Watson & Cloud Platform 事業部
- 2024-02-01: Francisco Partners 完成收購，Sheri Bachstein 繼續擔任 CEO，新獨立公司定位為全球最精確預報方 [[4]](https://www.businesswire.com/news/home/20240201709190/en/Francisco-Partners-Completes-Acquisition-of-The-Weather-Company)

### 核心技術
GRAF 模型基於 NCAR 下一代開源全球模型 MPAS，使用 IBM POWER9 超算，優化 CPU 與 GPU，首次實現 GPU 高性能計算架構上的全球運營模型 [[5]](https://www.weathercompany.com/news/ibms-the-weather-company-makes-higher-quality-weather-forecasts-available-worldwide/)。模型運行於 IBM Power Systems AC922 服務器，採用 NVIDIA V100 Tensor Core GPU，並透過 OpenACC 指令由 University of Wyoming 電氣與計算機工程系等合作方加速。

產品線包括 Weather Data APIs (Currents on Demand、Personal Weather Stations、15 天逐時預報、警報頭條與詳情、格點與多邊形天氣影像)、概率預報、閃電、熱帶氣旋、清洗歷史、季節性、能源、地面交通、媒體解決方案。

定價：Free Trial 30 天 50K calls/day、Standard 年付 1M calls/month $500 USD、Enterprise 定制。

## 3. 地緣學生態產業鏈

The Weather Company 公開表示與全球 168 個政府合作。GRAF 的全球化覆蓋首次將高分辨率預報帶至亞洲、非洲與南美等以往缺乏精細數據的地區。

**政府與多邊機構：**
- National Oceanic and Atmospheric Administration (NOAA)
- National Aeronautics and Space Administration (NASA)
- U.S. Navy、U.S. Air Force、U.S. National Science Foundation (NSF)
- U.K. Met Office
- Joint Center for Satellite Data Assimilation (JCSDA)，為 NOAA、NASA、美國海軍與空軍的多機構合作研究卓越中心 [[6]](https://www.weathercompany.com/news/twco-adopts-jedi-to-improve-everyday-forecasts/)
- University Corporation for Atmospheric Research (UCAR)，非營利聯盟，管理 NSF NCAR，成員超過 130 所北美高校 [[7]](https://www.weathercompany.com/news/twco-adopts-jedi-to-improve-everyday-forecasts/)

**研究與教育：**
- National Center for Atmospheric Research (NCAR)
- Los Alamos National Laboratory (與 NCAR 共同開發 MPAS)
- University of Wyoming Department of Electrical and Computer Engineering
- NSF NCAR (National Center for Atmospheric Research)

此鏈條對應果敢地緣學中的跨境控制邏輯，但 weather.com 以公共-私營夥伴關係推動科學共享，而非武裝控制。

## 4. 電信與信息學生態產業鏈

**歷史電信承載：**
- AT&T 於 2005 年贏得 weather.com 按需網絡帶寬、流媒體與緩存服務合同，為 2500 萬月活用戶提供服務 [[8]](https://wraltechwire.com/2005/02/11/att-wins-weather-com-data-contract/?amp=1)
- Verizon：The Weather Company 為 Verizon Cloud beta 客戶，依賴其全球 IP 網絡、超安全冗餘數據中心及安全實踐，將 10 個自有數據中心遷移至雲端，進行大數據分析與決策 [[9]](https://newswire.telecomramblings.com/2013/10/weather-company-verizon-cloud-enable-transformation-business/)
- Sprint PCS、AT&T Wireless、Verizon Wireless：Weathernews 自 2000 年代起為三大美國移動運營商提供天氣信息服務，此為行業先例
- Verizon Business 獲得近 8000 萬美元任務訂單，負責 National Weather Service 從 Networx 合約向 Enterprise Infrastructure Solutions 轉型

**當代信息分發：**
- Samsung Electronics：Galaxy S8/S8+ 起為默認天氣供應商，Bixby 天氣由 The Weather Company 驅動
- Apple Inc.：iOS 8 至 iOS 15 期間 The Weather Channel 為 Apple 天氣數據源，2020 年收購 Dark Sky 後，Apple WeatherKit 仍融合 U.S. National Weather Service、The Weather Channel 等多源 [[10]](https://www.macrumors.com/2026/01/22/apple-weather-app-snow/)
- Amazon：Alexa 通過 The Weather Channel Skill 提供精確預報
- Redfin：作為獨家歷史天氣提供商，數據上線 Redfin.com 及 Redfin iOS 與 Android 應用，覆蓋所有在售房源 ZIP 級別氣候信息 [[11]](https://www.weathercompany.com/news/redfin-partners-with-the-weather-company/)

## 5. 軍工與國防生態產業鏈

The Weather Company 於 2025-2026 年強化航空與公共部門事業部，任命前美國海軍 TOPGUN 畢業生 Jay Humphlett 為總經理，負責全球國防、情報、航空與政府業務增長，並統領 Dynamic Risk Operations Platform (DROP) [[12]](https://www.prnewswire.com/news-releases/the-weather-company-appoints-tech-executive-jay-humphlett-to-lead-aviation-and-public-sector-businesses-302807420.html)。

DROP 定義為從作戰中心至戰術邊緣提供可操作環境洞察的平台，具備 OPSEC-hardened 的共享作戰圖像，將環境感知轉化為任務與決策優勢 [[13]](https://www.weathercompany.com/blog/weather-forecast-accuracy-business-value-across-key-industries/)。

**相關實體：**
- 公司：BAE Systems、SimCentric Technologies (積極探索 Weatherverse 解決方案以重塑軍事規劃、訓練與模擬) [[14]](https://www.weathercompany.com/news/the-weather-company-expands-collaboration-with-nvidia-to-advance-ai-based-weather-forecasting-and-visualization-capabilities/)
- 組織與機構：MITRE (開發 Weather 1K 數據集，聯邦 AI Sandbox 計算能力)、U.S. Military Special Forces (前特種部隊軍官 Gareth Collier 評價預報準確性對任務成功與拯救生命的關鍵性)
- 政府：U.S. Department of Defense、U.S. Air Force Weather Agency、National Weather Service、Department of Transportation (FAA 航班延誤 75% 由天氣造成)
- 研究：JCSDA (多機構)、TempoQuest (AceCast 建模工具)

此與果敢地區武裝組織控制的軍工鏈條在本質上相反：前者為合規國防氣象決策支持，後者為非國家武裝經濟。

## 6. 神經網絡生態產業鏈

- **計算硬件：** IBM POWER9-based 超算、NVIDIA V100 Tensor Core GPUs、IBM Power Systems AC922 服務器
- **加速模型：** OpenACC directives 應用於 MPAS，由 NCAR、University of Wyoming 與 IBM 共同實施
- **神經網絡框架：** NVIDIA Earth-2 平台、NVIDIA Omniverse (Weatherverse 能力接入)、NVIDIA Earth-2 APIs (包括 AI 天氣模型)
- **數據集：** MITRE Weather 1K，總量約 7 petabytes，為大陸尺度 AI 訓練數據集，由 MITRE 與 NVIDIA Earth 2 團隊合作開發，使用 TempoQuest AceCast 等先進建模工具 [[15]](https://www.executivebiz.com/articles/mitre-twco-weather-1k-ai-forecasting-collaboration)

GRAF 系統為全球首個在 GPU 高性能計算架構上運營的全球天氣模型，此為神經網絡生態的物理基礎。

## 7. 人工智能生態產業鏈

- **模型融合引擎：** 使用 AI 整合近 100 個全球預報模型，根據地理、時間、天氣類型與近期準確度加權，實現按需 hyper-local 預報 [[16]](https://www.weatherwatch.co.nz/content/ibm-forecast-data-ai-used-by-weatherwatch-ruralweather-deemed-worlds-most-accurate-once-again/)
- **IBM Watson：** Watson Media and Weather、Watson IoT Business Unit、Watsonx 地理空間 AI 模型 (IBM 保留 Weather Company 數據用於氣候相關用例)
- **專有 AI 產品：** Weather Agent for Indices & Triggers、Weatherverse Sim (通過 API 以 Unreal Engine 可視化真實天氣)、Weather Targeting (基於天氣的商業洞察)
- **新一代 AI 預報：** 與 NVIDIA 合作創建首個千米尺度 AI 數值天氣預報模型，初期覆蓋美國與歐洲，最終全球化，旨在彌補當前 AI 模型缺乏歷史風暴尺度數據以預測極端事件的短板 [[17]](https://www.weathercompany.com/news/the-weather-company-expands-collaboration-with-nvidia-to-advance-ai-based-weather-forecasting-and-visualization-capabilities/)
- **開放社區：** JEDI (Joint Effort for Data Assimilation Integration) 開源框架，7 年研發，整合雷達、衛星、探空、飛機、氣象站等異步觀測，實現最高質量大氣現狀分析，預計提升預報準確度達 15% [[18]](https://www.weathercompany.com/news/twco-adopts-jedi-to-improve-everyday-forecasts/)

## 8. 科技操作系統與服務器生態產業鏈

**操作系統支持聲明：** The Weather Channel – weather.com 支持最新兩個版本的 iOS、Android、Windows 與 OSX，瀏覽器支持最新兩版 Chrome、Firefox、Apple Safari 與 Microsoft Edge。

**服務器與雲：**
- IBM Cloud、IBM Cloud Object Storage (weather.com 與 wunderground.com 使用)、IBM Cloud Kubernetes 託管服務 (顯著降低 DevOps 負擔)
- Amazon Web Services (AWS)：The Weather Company 曾為 AWS 標杆客戶，處理 20TB/日數據，日均 260 億預報，後轉向多雲策略
- Verizon Cloud Compute 與 Verizon Cloud Storage：對象可尋址、多租戶存儲平台
- 數據中心：從 10 個自有數據中心遷移至雲端

**應用層：**
- iOS、Android 原生應用：The Weather Channel App (美國下載量第一天氣應用，5000 萬日活)、Storm Radar、Weather Underground
- 桌面與 OTT：Roku、Amazon Fire TV、Apple TV、Android TV、Samsung Smart TV Tizen
- 企業集成：Redfin iOS 與 Android、JetBlue、American Airlines、United Airlines 嵌入式氣象服務

## 9. 宇航生態產業鏈

- **航空公司：** United Airlines (15 年以上合作，2026 年 3 月續簽多年協議，氣象學家 24/7 嵌入 Network Operations Center，工具包括 Pilotbrief 互動飛行甲板工具與 Maverick WXAlert 自動駕艙警報系統，通過 ACARS 傳輸) [[19]](https://www.weathercompany.com/news/the-weather-company-renews-multi-year-relationship-with-united-airlines-to-advance-weather-driven-aviation-innovation/)、JetBlue、American Airlines、British Airways
- **航空工業：** Panasonic Avionics (天氣支援合約)、Collins Aerospace、Honeywell Aerospace、WSI Fusion、Flight Explorer
- **監管與政府：** Federal Aviation Administration (FAA)、National Transportation Safety Board (NTSB) 氣象組、ICAO
- **衛星與發射：** Spire Global (為美國軍種、U.S. Space Force、NGA、NASA、NOAA 提供無線電掩星數據)、NOAA GOES、NASA Earth Science Division
- **跨行業：** BAE Systems 等國防工業探索 Weatherverse 用於任務規劃，與果敢無人機走私鏈條形成合法對照

The Weather Company 支持每日 25,000 架次航班，服務北美多數商業航空公司。

## 10. 完整實體總表（公司、集團、組織、研究所、教育機構、政府單位）

| 類別 | 實體名稱 | 生態歸屬 | 備註 |
| --- | --- | --- | --- |
| 集團/私募 | Francisco Partners | 地緣、AI、服務器 | 2024 年收購方，管理資本約 450 億美元 |
| 集團/科技 | IBM Corporation | 全部七鏈 | 2016-2024 所有者，POWER9、Watson、Cloud |
| 公司/氣象 | The Weather Company / weather.com / Weather Underground / Storm Radar | 核心 | 服務 3.6 億月活，GRAF、DROP、Weatherverse |
| 公司/廣播 | The Weather Channel (Allen Media Group) | 地緣、信息 | 電視網絡，使用數據分析 |
| 公司/科技 | Apple Inc. | 電信、OS、AI | WeatherKit，多源融合仍含 TWC |
| 公司/科技 | Samsung Electronics | 電信、OS | Galaxy 默認，Bixby 驅動 |
| 公司/科技 | Amazon (AWS, Alexa) | 電信、OS、服務器 | 早期大數據平台承載方 |
| 公司/電信 | AT&T | 電信 | 2005 年贏得帶寬與緩存合同 |
| 公司/電信 | Verizon / Verizon Business / Verizon Cloud | 電信、服務器 | 雲轉型夥伴，NWS 基礎設施 7770 萬訂單 |
| 公司/電信 | Sprint PCS, T-Mobile | 電信 | 歷史移動天氣分發 |
| 公司/地產科技 | Redfin Corporation | 信息、OS | 獨家歷史天氣，iOS/Android 上線 |
| 公司/航空 | United Airlines | 宇航、國防 | 嵌入式氣象，15 年+合作 |
| 公司/航空 | JetBlue, American Airlines, British Airways | 宇航 | 同類嵌入 |
| 公司/航空電子 | Panasonic Avionics, Collins Aerospace | 宇航 | 天氣支援 |
| 公司/國防 | BAE Systems, SimCentric Technologies | 軍工、宇航 | Weatherverse 探索 |
| 公司/半導體 | NVIDIA Corporation | 神經網絡、AI | Earth-2、Omniverse、V100 |
| 公司/AI 數據 | MITRE Corporation | AI、軍工 | Weather 1K 7PB，Federal AI Sandbox |
| 公司/建模 | TempoQuest (AceCast) | AI、神經網絡 | MITRE 合作 |
| 公司/能源零售 | EcoFlow, The Home Depot, National Grid | 地緣 | 廣告與供應鏈用例 |
| 組織/多邊 | JCSDA | 地緣、軍工、AI | NOAA、NASA、海軍、空軍聯合 |
| 組織/學術聯盟 | UCAR | 地緣、研究 | 管理 NCAR，130+ 高校 |
| 研究所 | NCAR / NSF NCAR | 地緣、AI | MPAS 模型開發 |
| 研究所 | Los Alamos National Laboratory | 地緣 | MPAS 共同開發 |
| 教育機構 | University of Wyoming Dept. Electrical & Computer Engineering | 神經網絡 | GPU 加速 |
| 教育機構 | University of Colorado Boulder | 地緣 | NWSC 夥伴 |
| 政府/美國 | NOAA, NWS, NASA, U.S. Navy, U.S. Air Force, U.S. Space Force, NGA, FAA, Department of Interior | 全部 | JEDI 夥伴與客戶 |
| 政府/英國 | U.K. Met Office | 地緣、AI | JCSDA 合作 |
| 政府/全球 | 168 國政府客戶、ISO 3166 249 國 NMHS | 地緣 | 包括 ECMWF、DWD、Météo-France、JMA、CMA 等 |
| 雲/服務器 | IBM Cloud Object Storage, IBM Cloud Kubernetes, AWS S3 | 服務器 | 大數據存儲與計算 |

## 11. 與果敢模式對比結論

果敢地區產業鏈特徵為武裝、博弈與跨境電信詐騙並存，依賴地緣割據、灰色電信通道及非國家武裝保護。weather.com 所屬七大生態鏈雖在功能上覆蓋相同領域（地緣情報、電信分發、軍工決策、神經網絡計算、AI 預報、操作系統分發、宇航保障），但其機制為：

- **地緣：** 以 WMO 及 JCSDA 多邊合作取代單邊控制
- **電信：** 以 AT&T、Verizon 合規帶寬與雲服務取代灰色中繼
- **軍工：** 以 DROP 的 OPSEC-hardened 共享作戰圖像與 BAE、MITRE 合規研發取代武裝護航
- **神經網絡/AI：** 以 NVIDIA Earth-2、IBM POWER9、Weather 1K 開放科學取代封閉詐騙模型
- **OS/服務器：** 以 iOS/Android/Windows 官方商店與 IBM Cloud/AWS/Verizon Cloud 合規分發取代側載與地下服務器
- **宇航：** 以 FAA、United 嵌入式氣象與 Spire 合法衛星數據取代走私無人機

因此，weather.com 不存在類似果敢的非法電信與信息學生態產業鏈，其所有業務均可在上述公司、集團、組織、研究所、教育機構、政府單位中追溯，無缺漏。

## Sources
[1] Business Wire — [Francisco Partners Completes Acquisition of The Weather Company](https://www.businesswire.com/news/home/20240201709190/en/Francisco-Partners-Completes-Acquisition-of-The-Weather-Company)
[2] The Weather Company — [The Weather Company makes higher quality weather forecasts available worldwide](https://www.weathercompany.com/news/ibms-the-weather-company-makes-higher-quality-weather-forecasts-available-worldwide/)
[3] The Weather Company — [The Weather Company makes higher quality weather forecasts available worldwide](https://www.weathercompany.com/news/ibms-the-weather-company-makes-higher-quality-weather-forecasts-available-worldwide/)
[4] Business Wire — [Francisco Partners Completes Acquisition of The Weather Company](https://www.businesswire.com/news/home/20240201709190/en/Francisco-Partners-Completes-Acquisition-of-The-Weather-Company)
[5] The Weather Company — [The Weather Company makes higher quality weather forecasts available worldwide](https://www.weathercompany.com/news/ibms-the-weather-company-makes-higher-quality-weather-forecasts-available-worldwide/)
[6] The Weather Company — [The Weather Company advances global weather forecasting with first implementation of JEDI system](https://www.weathercompany.com/news/twco-adopts-jedi-to-improve-everyday-forecasts/)
[7] The Weather Company — [The Weather Company advances global weather forecasting with first implementation of JEDI system](https://www.weathercompany.com/news/twco-adopts-jedi-to-improve-everyday-forecasts/)
[8] WRAL TechWire — [AT&T Wins Weather.com Data Contract](https://wraltechwire.com/2005/02/11/att-wins-weather-com-data-contract/?amp=1)
[9] Telecom Ramblings — [The Weather Company: Verizon Cloud to Enable the Transformation of our Business](https://newswire.telecomramblings.com/2013/10/weather-company-verizon-cloud-enable-transformation-business/)
[10] MacRumors — [Apple Weather and Snow: What's Behind the Forecast?](https://www.macrumors.com/2026/01/22/apple-weather-app-snow/)
[11] The Weather Company — [Redfin partners with The Weather Company to bring weather data to every home listing](https://www.weathercompany.com/news/redfin-partners-with-the-weather-company/)
[12] PR Newswire — [The Weather Company Appoints Tech Executive Jay Humphlett to Lead Aviation and Public Sector Businesses](https://www.prnewswire.com/news-releases/the-weather-company-appoints-tech-executive-jay-humphlett-to-lead-aviation-and-public-sector-businesses-302807420.html)
[13] The Weather Company — [How weather forecast accuracy helps businesses plan smarter](https://www.weathercompany.com/blog/weather-forecast-accuracy-business-value-across-key-industries/)
[14] The Weather Company — [The Weather Company expands collaboration with NVIDIA to advance AI-based weather forecasting and visualization capabilities](https://www.weathercompany.com/news/the-weather-company-expands-collaboration-with-nvidia-to-advance-ai-based-weather-forecasting-and-visualization-capabilities/)
[15] ExecutiveBiz — [MITRE, The Weather Company to Advance AI-Driven Forecasting](https://www.executivebiz.com/articles/mitre-twco-weather-1k-ai-forecasting-collaboration)
[16] WeatherWatch — [IBM forecast data & AI used by WeatherWatch / RuralWeather deemed world's most accurate once again](https://www.weatherwatch.co.nz/content/ibm-forecast-data-ai-used-by-weatherwatch-ruralweather-deemed-worlds-most-accurate-once-again/)
[17] The Weather Company — [The Weather Company expands collaboration with NVIDIA to advance AI-based weather forecasting and visualization capabilities](https://www.weathercompany.com/news/the-weather-company-expands-collaboration-with-nvidia-to-advance-ai-based-weather-forecasting-and-visualization-capabilities/)
[18] The Weather Company — [The Weather Company advances global weather forecasting with first implementation of JEDI system](https://www.weathercompany.com/news/twco-adopts-jedi-to-improve-everyday-forecasts/)
[19] The Weather Company — [The Weather Company renews multi-year relationship with United Airlines to advance weather-driven aviation innovation](https://www.weathercompany.com/news/the-weather-company-renews-multi-year-relationship-with-united-airlines-to-advance-weather-driven-aviation-innovation/)
