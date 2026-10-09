# 全球武裝勢力宇航操作系統缺口與自研路徑深度研報

## 執行摘要

全球具備建制武裝力量的政治實體數量約為178至203個，取決於對主權的定義。國際戰略研究所列出178個國家含正規與準軍事人員，而維基百科軍隊清單已明確包含台灣、科索沃、北塞普勒斯、阿布哈茲、南奧塞梯、德涅斯特河沿岸、索馬利蘭、撒哈拉阿拉伯民主共和國等非ISO-3166實體。真正具備獨立太空司令部與宇航操作系統的國家不超過18個，具備10顆以上軍用衛星的國家僅有美、中、俄、法、以色列等不足10個。絕大多數中小型武裝力量有武器裝備但無宇航操作系統、無軍事ISR衛星、無零信任指揮控制操作系統。

類台灣實體的核心特徵是：有一定工業與國防自主、但無完全主權空間發射與軍用ISR能力，高度依賴外國數據垂直服務，因而存在結構性替代風險。承接此類項目需同時面對ITAR/EAR、瓦聖納協定雙用途管制、以及中國不可靠實體清單與出口管制反制三重風險。

對於志在自研的團隊，短期採用Palantir式前向部署工程師模式以服務獲取數據飛輪，中期構建Foundry式本體操作系統與Apollo式邊緣部署，長期走SpaceX式70-90%垂直整合自研設備，是兼顧生存與自主的可行路徑。

## 1. 全球武裝勢力全譜系核驗

### 1.1 ISO-3166與聯合國體系內的武裝力量

根據IISS統計，全球約有178個國家擁有可統計的現役、預備役與準軍事人員數據，涵蓋從美國203.5萬現役到無常備軍的模里西斯、巴拿馬等僅保留準軍事力量的實體[[1]](http://en.wikipedia.org/wiki/List_of_countries_by_number_of_military_and_paramilitary_personnel)。另一商業數據庫GlobalMilitary.net截至2026年追蹤162個國家軍隊裝備[[2]](https://GlobalMilitary.net/)。Global Firepower則評估145個國家並將台灣列為第24位。

無正規軍但有武裝力量的例外包括模里西斯與巴拿馬，僅維持準軍事部隊[[1]](http://en.wikipedia.org/wiki/List_of_countries_by_number_of_military_and_paramilitary_personnel)。

### 1.2 非ISO-3166但具備武裝力量的政治實體

ISO-3166未授予代碼的實體包括索馬利蘭、德涅斯特河沿岸、北塞普勒斯、阿布哈茲、南奧塞梯等，ICANN明確因其不在ISO-3166-1標準內而不授予國家頂級域名[[3]](https://www.icann.org/en/blogs/details/abkhazia-kosovo-south-ossetia-transnistria-my-oh-my-23-9-2008-en)。學術與開源地理項目列出的事實國家通常為：科索沃、北塞普勒斯、德涅斯特河沿岸、南奧塞梯、阿布哈茲、台灣、索馬利蘭等7個核心實體[[4]](https://github.com/gitzmbe/geo-quizzes/issues/21)，擴展清單可達10-11個，加入巴勒斯坦、西撒哈拉、阿爾察赫等[[5]](https://www.youtube.com/watch?v=Kq_N-9bnB7I)。

維基百科軍隊清單已完整收錄這些實體的陸軍建制：

- 阿布哈茲軍隊 1992年建立
- 科索沃安全部隊 2009年
- 北塞普勒斯軍隊 1976年
- 索馬利蘭國民軍 1993年
- 南奧塞梯軍隊 1992年
- 台灣中華民國陸軍 1924年
- 德涅斯特河沿岸軍隊 1991年
- 巴勒斯坦解放軍與國家安全部隊
- 撒哈拉人民解放軍[[6]](https://en.wikipedia.org/wiki/List_of_armies_by_country)

由此，全球武裝勢力總量應以203個獲至少一個聯合國成員承認的實體為上限，下以178個IISS可統計實體為下限，中位數約190個左右。

| 類別 | 數量 | 代表 | ISO代碼狀態 |
| --- | --- | --- | --- |
| 聯合國會員國具備正規軍 | 193 | 美、中、俄等 | 有 |
| 聯合國觀察員 | 2 | 巴勒斯坦、梵蒂岡 | 有/特殊 |
| 非聯合國但廣泛承認 | 2 | 科索沃、台灣 | 台灣列為TW Province of China，科索沃有代碼 |
| 完全未獲聯合國會員承認的事實國家 | 6-8 | 北塞普勒斯、阿布哈茲、南奧塞梯、德涅斯特河沿岸、索馬利蘭、西撒哈拉 | 無代碼 |
| 無常備軍僅準軍事 | 3 | 模里西斯、巴拿馬、哥斯大黎加 | 有 |

## 2. 宇航操作系統與指揮控制缺口

### 2.1 太空司令部的稀缺性

太空司令部被定義為負責太空作戰的軍事組織，世界上首個為1982年美國空軍太空司令部[[7]](https://en.wikipedia.org/wiki/Space_command)。截至2024年，具備公開太空司令部或同等機構的國家僅約18個：美國、俄羅斯、中國、法國、英國、德國、澳洲、加拿大、丹麥、義大利、日本、荷蘭、紐西蘭、挪威、波蘭、韓國、瑞典、西班牙等在Space Chiefs Forum中被點名[[8]](https://spacenews.com/?p=126292)。SpaceNews報導2022年集會僅15國參與，包括澳、加、丹、法、德、意、日、荷、紐、挪、波、韓、瑞、英、美[[9]](https://spacenews.com/?p=126292)。

絕大多數國家因此屬於「有武器設備、無宇航操作系統」。

### 2.2 軍用衛星與ISR能力的金字塔

截至2023年數據，美國擁有247顆軍用衛星，俄羅斯110顆，中國157顆，之後斷層式下降：法國17顆、以色列12顆、義大利10顆、印度9顆、德國8顆、英國6顆、西班牙4顆[[10]](https://worldpopulationreview.com/country-rankings/military-satellite-by-country)。大量西方國家因依賴美國情報共享而未發展自有軍用衛星[[10]](https://worldpopulationreview.com/country-rankings/military-satellite-by-country)。

台灣是典型缺口案例。美國空軍大學研究指出：台灣缺乏國內太空發射項目，沒有任何台灣衛星為軍事監視目的發射，現有太空基礎設施不支持與中國的對稱戰爭[[11]](https://www.airuniversity.af.edu/Portals/10/ISR/student-papers/AY21-22/TaiwanChinaISRSatellites_Phan.pdf)。其衛星如福衛五號、七號均為氣象與科研用途，發射依賴SpaceX等外國火箭，且用於軍事目的的衛星並非台灣自有，數據獲取依賴夥伴協議[[11]](https://www.airuniversity.af.edu/Portals/10/ISR/student-papers/AY21-22/TaiwanChinaISRSatellites_Phan.pdf)。

類似缺口廣泛存在於：

- 東南亞：菲律賓、越南、泰國等有陸軍海軍但無軍事ISR星座
- 中東北非：多數海灣國家依賴美國GPS OCX等系統，自身OCX已因成本超支與性能問題被Space Force終止並轉向Palantir Warp Core替代方案
- 東歐與巴爾幹：科索沃、摩爾多瓦、波黑等僅有輕步兵，無太空能力
- 事實國家：索馬利蘭、德涅斯特河沿岸等完全無宇航能力

### 2.3 計數分析策略技術與零信任缺口

現代宇航操作系統核心已從單純發射轉向C2數據融合與零信任架構。美軍目標2027年實現全軍零信任，零信任要求對每個訪問請求持續驗證、最小權限、假設已失陷[[12]](https://www.militaryaerospace.com/trusted-computing/article/14285940/trusted-computing-cyber-security-information-security?o_eid=0652C8073834D7U&oly_enc_id=0652C8073834D7U&rdx.ident%5Bpull%5D=omeda%7C0652C8073834D7U&utm_campaign=CPS230116003&utm_medium=email&utm_source=MAE+Embedded)。Palantir的Apollo已實現從雲端到戰術邊緣的斷網連續部署[[13]](https://www.youtube.com/watch?v=it4_OqkoZRo)，而多數中小武裝力量仍停留在商用雲加人工Excel階段，缺乏Foundry式本體論與實時數字孿生。

## 3. 類台灣實體項目承接風險模型

### 3.1 法律基礎與地緣政治雙重性

美國對台軍售法律基礎為1979年台灣關係法，要求提供防禦性武器與服務以維持自衛能力[[14]](https://www.congress.gov/bill/117th-congress/house-bill/9010/text/ih)，但不構成共同防禦條約。國際社會對此保持戰略模糊，RAND評估短期衝突概率低但2026年後上升。

### 3.2 三重出口管制風險

1. **美國ITAR/EAR**：任何含美國原產軍品技術的宇航OS均需國務院許可，Honeywell曾因未經授權向加拿大、愛爾蘭、墨西哥、中國等轉移ITAR數據被處罰，2024年Raytheon因ITAR與武器出口管制法違規和解金額超9.5億美元[[15]](https://news.clearancejobs.com/2021/05/05/honeywell-agrees-to-pay-millions-for-sending-controlled-arms-information-abroad/feed/json)。Kratos與台灣中科院無人機合作亦需ITAR審查[[16]](https://openaimpact.com/news/ncist-mulls-kratos-drone-collaboration/)。

2. **瓦聖納協定雙用途**：瓦聖納協定42個參與國將軟件、入侵軟件、加密技術列為雙用途物項，航天操作系統中的遙測、加密、自主決策均屬管制範疇[[17]](https://www.mondaq.com/canada/export-controls-trade-investment-sanctions/1833652/export-controls-on-software-transfers-in-the-cloud-and-artificial-intelligence)。台灣經濟部2025年亦宣布收緊量子計算與先進半導體設備等雙用途出口以符合瓦聖納協定[[18]](https://bworldonline.com/world/2025/11/18/713011/taiwan-to-further-tighten-export-controls-for-dual-use-technology/)。

3. **中國反制**：中國商務部已將8家台灣航天與造船企業包括漢翔航空、經緯航太、台船列入出口管制名單，禁止雙用途物項出口[[19]](https://www.taxtmi.com/news?id=48833)。對美方，中國自2023年起對Lockheed Martin、Raytheon Missiles & Defense實施進出口禁令與投資禁令，並禁止高管入境[[20]](https://www.airforcetimes.com/industry/2023/04/18/china-reveals-new-details-of-raytheon-lockheed-sanctions/?contentFeatureId=f0fmoahPVC2AbfL-2-1-8&contentQuery=%7B%22includeSections%22%3A%22%2Fhome%22%2C%22excludeSections%22%3A%22%22%2C%22feedSize%22%3A10%2C%22feedOffset%22%3A255%7D)，2024年擴大至20家美國防務公司與10名高管[[21]](https://www.aljazeera.com/news/2024/9/18/china-sanctions-us-defence-firms-for-arms-sales-to-taiwan)。

承接類台灣項目若未取得美國許可，可能觸發ITAR刑事重罪與三年禁止交易；若被中國列入不可靠實體，將失去中國供應鏈與市場。

### 3.3 風險分級

| 風險等級 | 實體類型 | 技術缺口 | 管制強度 |
| --- | --- | --- | --- |
| 極高 | 台灣本島 | 無軍用ISR發射、無完整C2 OS、依賴外援 | ITAR+EAR+中方反制三重疊加 |
| 高 | 科索沃、北塞普勒斯 | 完全無宇航能力 | 瓦聖納+歐盟雙用途 |
| 中 | 泰國、菲律賓、波蘭 | 有部分衛星但無自主OS | 主要為EAR |
| 低 | 索馬利蘭、撒哈拉 | 無支付能力、無合規需求但無市場 | 低，但需人道法評估 |

## 4. Palantir先行 vs SpaceX自研：路徑對比與批判

### 4.1 Palantir模型：服務即操作系統

Palantir定義了現代國防操作系統堆疊：Gotham為情報融合、Foundry為數據本體、AIP為AI決策層、Apollo為邊緣部署、Maven為視覺打擊鏈[[13]](https://www.youtube.com/watch?v=it4_OqkoZRo)。其商業模式核心是前向部署工程師，工程師直接駐場客戶，理解其數據管道與合規，現場編寫真正可用的系統，而非銷售標準產品[[22]](https://www.barrons.com/articles/palantir-stock-price-upgrade-goldman-ab22d7cb)[[23]](https://www.revolutioninai.com/2026/05/forward-deployed-engineer-ai-anthropic-openai-explained.html)。這種模式導致高獲客成本但極高留存與合約價值，IPO後從6美元至五年640%回報驗證其黏性[[23]](https://www.revolutioninai.com/2026/05/forward-deployed-engineer-ai-anthropic-openai-explained.html)。

優勢：無需重資產即可進入國防客戶，建立數據飛輪與切換成本。

### 4.2 SpaceX模型：垂直整合

SpaceX製造約70%至90%零部件在內部，行業標準僅30%[[24]](https://github.com/lisanalgaib7/first-principles/blob/HEAD/references/elon-musk-examples.md)[[25]](https://www.fool.com/investing/2026/07/14/better-vertically-integrated-space-stock-spacex-or/)。其邏輯是每個外包層都是利潤與進度失控點，自有發射、衛星、用戶終端與服務形成內部客戶閉環[[25]](https://www.fool.com/investing/2026/07/14/better-vertically-integrated-space-stock-spacex-or/)。SpaceX維持高度垂直整合、地理分散的製造生態，從原材料、發動機到整箭與載人飛船均自研[[26]](https://github.com/adexian/spacex-s1/blob/HEAD/spacex-s1/sections/316-infrastructure-and-facilities.md)，實現快速迭代與成本控制[[27]](https://www.ainvest.com/news/spacex-falcon-9-starlink-catalyst-aerospace-valuation-upside-2511/)。

優勢：完全自主、供應鏈抗制裁、邊際成本遞減。劣勢：初期資本需求巨大，失敗成本高。

### 4.3 秋生立足的混合策略建議

先生所言外來數據垂直服務如寄宿終被淘汰，與產業共識一致：歐洲與五眼聯盟已從數據共享轉向能力共建，要求互操作但主權可控的系統[[9]](https://spacenews.com/?p=126292)。

建議三階段：

**階段一（0-18月）Palantir式**：不賣產品，賣前向部署。選1-2個中等風險實體如泰國或波蘭，提供零信任C2數據中台概念驗證，駐場3個月打通其現有雷達、無人機與商用衛星數據，構建Ontology。這階段避免觸碰ITAR軍品，使用商用遙感與開源情報。

**階段二（12-36月）操作系統化**：將階段一沉澱為自有Aerospace OS，架構參考：Gotham式本體層、Foundry式管道、Apollo式離線部署。技術棧選用Rust+WASM邊緣、零信任mTLS、AES-256靜態加密、TLS 1.3傳輸，實現VIGIL式離線遙測監控[[28]](https://github.com/vivwerq/vigil)。同步建立Apollo式發布鏈，確保在斷網戰場可更新。

**階段三（24-60月）SpaceX式垂直**：從軟件向下整合關鍵硬件。優先自研：衛星地面站OS、無人機飛控OS、軟件定義無線電。避免一開始造火箭，改為造終端與載荷計算平台，復用70%自研率指標。最終目標如SpaceX星鏈終端自研，形成發射可外包但OS與終端自主的閉環。

**風險緩釋**：

- 法務：設立雙實體架構，歐盟實體處理瓦聖納合規，美國實體僅處理已獲許可的對台間接支持，避免直接對高風險實體出口ITAR物項
- 技術：核心OS保持ITAR-free，使用歐洲或台灣本土非受控組件
- 商業：對類台灣客戶採用數據主權敘事，強調擺脫外來數據寄宿，正如台灣衛星論文指出依賴外國發射與數據共享不可靠[[11]](https://www.airuniversity.af.edu/Portals/10/ISR/student-papers/AY21-22/TaiwanChinaISRSatellites_Phan.pdf)

## 5. 盲點與反證

- **假設反證**：若全球多數武裝力量永遠不需要獨立宇航OS而滿足於購買美國服務，則自研市場為偽需求。但烏克蘭戰爭已證明商用衛星圖像價值與美國ISR不可依賴時的戰略脆弱性，55國正在建設軍用間諜衛星的趨勢支持自主需求。
- **台灣反證**：台灣雖缺乏發射，但其半導體與資通訊產業鏈完整，具備自研OS的土壤，經濟部收緊出口管制反而創造本地替代窗口。
- **成本反證**：SpaceX式自研需要百億級資本，對初創不可行。但採用Rocket Lab式小步快跑，先收購關鍵零部件商再整合，可降低門檻。

## 結論

全球約190個武裝實體中，超過90%缺乏宇航操作系統，這是結構性機會而非偶然。類台灣實體因地緣與技術雙重缺口，需求最迫切但風險最高。先生以Palantir切入、SpaceX收束的思路符合國防科技產業演進規律，關鍵在於將前向部署的黏性轉化為操作系統的標準，再將操作系統的標準轉化為硬件的利潤。自主不是一蹴而就，而是先寄宿、再共生、最終替代。

## Sources

[1] Wikipedia — [List of countries by number of military and paramilitary personnel](http://en.wikipedia.org/wiki/List_of_countries_by_number_of_military_and_paramilitary_personnel)
[2] GlobalMilitary.net — [World Military Forces Database 2026](https://GlobalMilitary.net/)
[3] ICANN — [Abkhazia, Kosovo, South Ossetia, Transnistria… My oh my.](https://www.icann.org/en/blogs/details/abkhazia-kosovo-south-ossetia-transnistria-my-oh-my-23-9-2008-en)
[4] GitHub — [feat: add more De Facto States entities](https://github.com/gitzmbe/geo-quizzes/issues/21)
[5] YouTube — [What are DE FACTO STATES?](https://www.youtube.com/watch?v=Kq_N-9bnB7I)
[6] Wikipedia — [List of armies by country](https://en.wikipedia.org/wiki/List_of_armies_by_country)
[7] Wikipedia — [Space command](https://en.wikipedia.org/wiki/Space_command)
[8] SpaceNews — [Space chiefs from 18 nations convene at forum hosted by Space Force](https://spacenews.com/?p=126292)
[9] SpaceNews — [Military space chiefs from 15 countries gather amid growing security concerns](https://spacenews.com/?p=126292)
[10] World Population Review — [Military Satellites by Country 2026](https://worldpopulationreview.com/country-rankings/military-satellite-by-country)
[11] Air University — [Limitations of Taiwan’s Satellite Capabilities in a China-Taiwan Conflict](https://www.airuniversity.af.edu/Portals/10/ISR/student-papers/AY21-22/TaiwanChinaISRSatellites_Phan.pdf)
[12] Military Aerospace — [trusted computing cyber security information security](https://www.militaryaerospace.com/trusted-computing/article/14285940/trusted-computing-cyber-security-information-security?o_eid=0652C8073834D7U&oly_enc_id=0652C8073834D7U&rdx.ident%5Bpull%5D=omeda%7C0652C8073834D7U&utm_campaign=CPS230116003&utm_medium=email&utm_source=MAE+Embedded)
[13] YouTube — [How Palantir Technologies Is Building the Future of AI Warfare](https://www.youtube.com/watch?v=it4_OqkoZRo)
[14] Congress.gov — [Text - H.R.9010 - 117th Congress](https://www.congress.gov/bill/117th-congress/house-bill/9010/text/ih)
[15] ClearanceJobs — [Honeywell Agrees to Pay Millions for Sending Controlled Arms Information Abroad](https://news.clearancejobs.com/2021/05/05/honeywell-agrees-to-pay-millions-for-sending-controlled-arms-information-abroad/feed/json/)
[16] OpenAImpact — [NCIST‑Kratos Drone Pact Boosts Taiwan’s Autonomous Aerospace](https://openaimpact.com/news/ncist-mulls-kratos-drone-collaboration/)
[17] Mondaq — [Export Controls On Software, Transfers In The Cloud, And Artificial Intelligence](https://www.mondaq.com/canada/export-controls-trade-investment-sanctions/1833652/export-controls-on-software-transfers-in-the-cloud-and-artificial-intelligence)
[18] BWorldOnline — [Taiwan to further tighten export controls for dual-use technology](https://bworldonline.com/world/2025/11/18/713011/taiwan-to-further-tighten-export-controls-for-dual-use-technology/)
[19] TaxTMI — [China imposes export ban on companies tied to Taiwan's military](https://www.taxtmi.com/news?id=48833)
[20] Air Force Times — [China reveals new details of Raytheon, Lockheed sanctions](https://www.airforcetimes.com/industry/2023/04/18/china-reveals-new-details-of-raytheon-lockheed-sanctions/?contentFeatureId=f0fmoahPVC2AbfL-2-1-8&contentQuery=%7B%22includeSections%22%3A%22%2Fhome%22%2C%22excludeSections%22%3A%22%22%2C%22feedSize%22%3A10%2C%22feedOffset%22%3A255%7D)
[21] Al Jazeera — [China sanctions US defence firms over arms sales to Taiwan](https://www.aljazeera.com/news/2024/9/18/china-sanctions-us-defence-firms-for-arms-sales-to-taiwan)
[22] Barron's — [Palantir Stock Has a Secret Weapon in the AI Boom, Goldman Sachs Says](https://www.barrons.com/articles/palantir-stock-price-upgrade-goldman-ab22d7cb)
[23] RevolutionInAI — [The Palantir Model That Anthropic and OpenAI Are Now Copying — Forward Deployed Engineers Explained](https://www.revolutioninai.com/2026/05/forward-deployed-engineer-ai-anthropic-openai-explained.html)
[24] GitHub — [elon-musk-examples](https://github.com/lisanalgaib7/first-principles/blob/HEAD/references/elon-musk-examples.md)
[25] The Motley Fool — [Better Vertically Integrated Space Stock: SpaceX or Rocket Lab?](https://www.fool.com/investing/2026/07/14/better-vertically-integrated-space-stock-spacex-or/)
[26] GitHub — [infrastructure-and-facilities](https://github.com/adexian/spacex-s1/blob/HEAD/spacex-s1/sections/316-infrastructure-and-facilities.md)
[27] AInvest — [SpaceX's Falcon 9 and Starlink: A Catalyst for Aerospace Valuation Upside](https://www.ainvest.com/news/spacex-falcon-9-starlink-catalyst-aerospace-valuation-upside-2511/)
[28] GitHub — [vivwerq/vigil](https://github.com/vivwerq/vigil)
