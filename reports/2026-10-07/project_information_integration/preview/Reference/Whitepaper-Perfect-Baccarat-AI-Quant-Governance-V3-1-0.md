
<!-- INTEGRATION_20261007_BEGIN -->
## 2026-10-07 整合與審校說明

本輪整合日期：2026-10-07。原主文件正文與換行保留；本節及文末「來源增補」為新增內容。來源增補保存舊版與附件中尚未出現在主文的段落，以來源、行號及雜湊追溯；舊說法、模型答覆、程式碼及商業構想均屬歷史資料，不能因收錄而視作已核實事實。重複段落的覆蓋位置見整合台帳，原始來源檔仍保留。

本輪完成的是本地版本與內容覆蓋校對，並對下列關鍵主張作審校。其餘逐項外部事實核實尚未完成；未核實能力、數值、收入、合規及排名維持 UNKNOWN／待審。來源類別 P0/P1、模型引用標記、廠商宣傳及舊驗收回執均不等於 VERIFIED。

各版本相互矛盾時保留兩者，依主張、版本、時間、場景及證據裁決，不能用最新檔名自動判定真偽。主文件的版本名稱保留，整合日期另記。

<!-- INTEGRATION_20261007_END -->
# v3.1.0 增量签发说明（2026-09-29）

> 本文件完整保留其后 `v3.0.0` 父版正文，并在末尾追加 §21。当前解释冲突以 §21 的 C-17～C-32 为准；父版不静默改写。

# 完美真人百家乐 AI × 量化科技 × 安全治理白皮书 v3.0.0

> **副标题**：Baccarat-Core Gaming Decision Intelligence Operating System（GDI-OS）  
> **范围**：完美真人 / WM Perfect 为核心研究对象；体育博彩、彩票/iLottery 为相邻垂直；金融、银行、资安、电商、科研、宇航/安全关键系统为方法论迁移来源  
> **as-of**：2026-09-28  
> **版本原则**：**只增不减；保留已成立内容；纠错只降低错误主张，不删除历史台账；UNKNOWN 不以推测填空。**  
> **现行工程边界**：不连接/不实测 Superset、DolphinScheduler、StarRocks、生产博彩站点；不把生产原始数据提交外部 AI。仅做离线、脱敏/模拟数据、代码与架构审查，以及经正式授权的测试线工作。  
> **性质**：研究、架构、采购尽调与治理白皮书；不是牌照意见、法律意见或任何公司未公开生产能力的证明。

---

## 0. 本版为什么是“强化版”而不是重写版

v3.0.0 同时继承并上收以下资产：

1. v1.0.0 移植总表的 **70 主体 + 9 类监管/标准体系、M-1～M-11、SC-A～SC-C、13 行业迁移、IQ/OQ/PQ、软件/硬件候选**。
2. v2.0.0 的 **RedTeam / Critic / KillCritic / Blindspot / ActionPlan、三价值边界、AI Dealer 独立成章**。
3. 2026-09-27 全球白皮书的 **P0/P1/P2/P3 证据分层、GDI-OS、`registry_risk_topology`、模型 Challenger ladder、体育/彩票补全、采购尽调问卷**。
4. 三价值 DRAFT 的 **P-1～P-4 定稿前置、X-1～X-9 跨件冲突、三垂直 L4 域模型差异**。
5. 最新 `Inteligent_egaming_platform_ref` 新增的 **Playtech Virtual Host、BetConstruct KISS AI、Winfinity、Sentient Gaming Group、SkyGaming、Future Anthem/EveryMatrix、Stake/BC.Game/1xBet/Dafabet 等扩展主体**。
6. Windows 11 QMD 中对本机环境、R BLAS、TinyTeX、权限/安全代理和“验收看真正跑出来的结果”的工程纪律。

### 0.1 本轮六份主附件指纹

| 来源文件 | 行数 | 字节 | MD5 |
| --- | --- | --- | --- |
| Inteligent_egaming_platform_ref_v000.000.001.qmd | 15934 | 817632 | 5b504053c9166bdbf3acccef800b4093 |
| Whitepaper-Online-Gaming-Baccarat-AI-V2-0-0.md | 350 | 26736 | 01bc19dbd069b5bc6aee4a26b9e45017 |
| 顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1_0_0.md | 892 | 79482 | 1f28a39616dfa9c1bbf0b9c2e49b3d98 |
| 全球在线博彩娱乐_AI量化科技与安全治理白皮书_2026-09-27(1).md | 828 | 37999 | 2898284dd57e0271961570e80bf506f1 |
| 在线博彩娱乐白皮书_百家乐体育彩券_三价值统一架构_v0_1_0_DRAFT.md | 286 | 25187 | 2f2c388559414131f52d8919b5defb24 |
| 電腦已昇級至視窗11版（工欲善其事必先利其器）.qmd | 11627 | 504093 | 41cdec343b7f2ce0318f5a90c3828f12 |

> 指纹是来源身份锚；本白皮书自身的 MD5/字节数在交付回执中给出，避免自指悖论。

---

# 1. Executive Thesis

真正世界级的真人百家乐平台，不是“AI 模型最多”，而是同时满足六个条件：

1. **Game Integrity**：牌局结果与 AI/CRM/风险模型隔离；物理牌或认证 RNG 的结果链可审计。
2. **Canonical Event Truth**：下注、开注、封注、发牌、识牌、结算、钱包、风控、人工处置拥有统一事件 ID、时间戳和版本。
3. **Decision Intelligence**：规则 → 统计基线 → GBDT → Survival/HMM → Graph/Sequence → 受约束 Bandit/RL，逐级以 OOT 证据晋级。
4. **Human Governance**：高影响动作具人工复核、理由码、申诉、回滚、独立验证和 outcome analysis。
5. **Responsible Gambling Firewall**：RG/脆弱性信息是硬约束，不得回流到促销、返水、VIP、催存或“让用户多玩”的模型。
6. **Evidence Discipline**：厂商营销、行业媒体、供应商案例、年报/监管文件严格分层；数字不跨主体、不跨年份、不跨分母偷换。

因此目标不是“AI Casino”，而是：

> **一个可证明、可重放、可审计、可申诉、可降级、可量化增量价值、且结果完整性与营销目标相隔离的 Gaming Decision Intelligence Operating System。**

---

# 2. 证据模型：P0–P4 + Current-State Ledger

| 等级 | 定义 | 使用规则 |
|---|---|---|
| **P0 VERIFIED-REG** | 法律/监管正文、SEC/法定申报、正式监管公告 | 可作为制度/公司状态基线 |
| **P1 VERIFIED-FIRST-PARTY** | 公司年报、官方产品页、正式公告、官方技术文档 | 可直接引用，但厂商效果数字须注明“自述” |
| **P2 OBSERVED-SECONDARY/PARTNER** | 合作伙伴公告、可信行业媒体、供应商案例 | 可做趋势/采购线索，不升级成行业事实 |
| **P3 UNKNOWN/UNVERIFIED** | 仅代理站、营销页、来源缺失或相互冲突 | 只保留主体，不填充能力 |
| **P4 ADVERSARIAL-CLAIM** | 玩家端工具、预测器、攻击者/优势玩法宣称 | 仅用于防御威胁模型，不视为有效性证明 |
| **CONDITIONAL** | 结论取决于司法辖区、牌照、合同、产品版本、数据授权 | 必须列条件 |

## 2.1 Current-State Correction Ledger（C-01～C-16）

| ID | 旧稿/冲突 | 2026-09-28 采用口径 |
|---|---|---|
| C-01 | Featurespace “Visa 拟收购” | **已于 2024-12-19 完成收购**，现属于 Visa Risk and Identity Solutions。 |
| C-02 | Smartico “2026-04 已完成收购” | 可核实的是 Optimove **2026-04-06 签署收购协议**，公告称预计数周内完成且双方继续独立运营；本轮未找到一手 completion 公告，状态保持 `SIGNED / COMPLETION_NOT_INDEPENDENTLY_VERIFIED`。 |
| C-03 | Sentient Studios “12 语言、百家乐年底才上线” | 当前官网已列 **Blackjack / Roulette / Baccarat**，并宣称 **70+ languages**；旧数字保留为历史时点，不再当当前事实。 |
| C-04 | Sentient Studios 与 Sentient Gaming Group 混为一体 | **拆成两个独立主体**。Sentient Gaming Group 通过 QTech 于 2026-03 发布 AI Roulette，并称 Baccarat 等后续。 |
| C-05 | “只有 Octane + Sentient 两家 AI Dealer” | 作为 2026 年早期判断已过时；现加入 Playtech Virtual Host、Sentient Gaming Group、SkyGaming、BetConstruct KISS AI、Avanti 等**不同成熟度**的 AI/Virtual Dealer 队列。 |
| C-06 | Playtech AI Live 仅为路线图 | 2026 H1 结果明确：**2026-07 已向多个客户上线 AI-powered Live Virtual Host**。 |
| C-07 | Winfinity 视觉识牌为二手推测 | 官方资料明确：Baccarat 使用自研 video recognition + ANN，牌无需条码；升级为 P1（能力存在），效果仍需独立基准。 |
| C-08 | Evolution “AI-Powered Fraud Detection/biometric”被写成官方 | 继续执行 M-1：未有 Evolution 一手证据的具体 AI 功能不得写成官方。当前可硬确认 2025 年报约 **2,000 Live tables、22 个新 Live games**。 |
| C-09 | EU AI Act = “博彩 AI 一律高风险” | **错误**。按 Article 6 + Annex III + intended purpose 判定；不能按行业一刀切。 |
| C-10 | UKGC 自动化可无人裁决 | LCCP 3.4.3：强风险指标须及时自动化处理，但**每个受影响客户必须人工复核，并可 contest 自动决定**；强 harm indicators 下还须阻止营销/新 bonus。 |
| C-11 | Mindway 900 万 vs 1,470 万 | 当前 Mindway 官方访谈给出 **14.7m active players/month**；9m 视为旧时点/旧口径。效果率仍视为供应商自述。 |
| C-12 | Kindred 仍作为独立集团 | 2024 被 FDJ 收购；2025-03 集团更名 **FDJ UNITED**。历史系统写作 `FDJ UNITED / legacy Kindred PS-EDS`。 |
| C-13 | Brightstar 归属混乱 | SEC 2025 20-F：2025-07 IGT → **Brightstar Lottery PLC**；完成 Gaming & Digital 出售后成为 pure-play global lottery。Apollo Funds 买的是被出售 Gaming & Digital 的买方。 |
| C-14 | Kambi AI trading 仅行业传闻 | 2025 年报官方：**AI-driven trading accounted for 48% of bets in 2025**。 |
| C-15 | Sports AI 证据不足 | Genius 2025 20-F 和 Sportradar 2025 20-F 已把 AI/ML、computer vision、liability-driven odds adjustment、risk management 写入法定申报，升级为 P1。 |
| C-16 | `house_edge` 作为单一标量 | **升级为 `economic_contract_registry`**：按 game × bet_type × ruleset × commission × market × currency × effective_time 管理。 |

---

# 3. 三条铁律 v3

## 3.1 Game Integrity Firewall

**AI/ML/RL/CRM 不得按个体玩家改变：**

- 牌靴、物理发牌；
- RNG 结果；
- 结算逻辑；
- 已公示派彩；
- 已公示体育结算规则；
- 彩票开奖或中奖判定。

AI Dealer 若为 RNG 型产品，结果引擎与生成式人物/语音/渲染层必须形成**独立信任域**；真人物理牌产品则以摄像/机器视觉作为**观测与核验**，不得反向控制结果。

## 3.2 Responsible Gambling Firewall

RG 信号只能用于降低暴露、限额/暂停、冷静期、自我排除、保护性信息、人工关怀、申诉与援助。

不得用于 VIP 升级、催存、返水增发、连败后奖励、追损召回、增加投注额/时长或利用脆弱状态营销。

### 工程实现

`Purpose-bound ABAC / OPA-Rego → domain-specific feature views → policy tags → DLP → immutable access log → forbidden-feature tests`

**物理数据二极管**保留为极高敏感场景选项，不再误写为所有平台的唯一实现。

## 3.3 High-Impact Human Governance

账户永久限制、提款冻结、舞弊定性、SAR/STR 升级、荷官调查/停职等高影响动作：

- 必须可解释；
- 必须有人工复核；
- 必须记录 override；
- 必须可申诉；
- 必须可回滚（法律强制不可逆者除外）；
- 必须记录模型、规则、特征快照和证据链；
- 必须做 outcome analysis。

---

# 4. 三价值 v3：止损 × 增效 × 合规

| 价值 | 允许优化目标 | 核心 KPI | 禁止伪收益 |
|---|---|---|---|
| **止损** | 已确认 fraud/bonus abuse/account takeover/collusion/payment anomaly/process error 的真实损失减少 | confirmed avoided loss、Precision@review-capacity、Recall@FP-budget、case cycle、false-positive cost | 正常玩家被限制后少派彩；拒付合法提款；把 house edge 当“模型收益” |
| **增效** | 同等人力处理更多、证据更完整、数据/对账/调查更快 | cases/analyst-day、automation evidence coverage、p50/p95 cycle time、reconciliation time、deployment lead time | 高风险玩家投注增加、追损延长、RG 人群回流 |
| **合规** | 更早保护、更完整审计、更低权限滥用、更强模型治理 | strong-risk latency、manual review coverage、appeal SLA、reason-code completeness、RG→marketing leakage=0、audit completeness | 将合规当可被利润抵消的“软权重” |

## 4.1 `economic_contract_registry`

```text
product_vertical
game_id
game_version
bet_type
ruleset_id
commission_rule
theoretical_rtp
theoretical_edge
fee_rate
jackpot_contribution
promo_cost_rule
jurisdiction
currency
effective_from
effective_to
source_document
approval_status
```

---

# 5. 完整主体登记册：来源完整性优先

> `列入 ≠ 推荐 ≠ 已投产 ≠ 证据升级`。P3/P4 主体被保留，是为了满足来源完整性与威胁建模，不是替其背书。

| ID | 类别 | 主体 | 角色 | 证据 | 优势/可确认强项 | 局限/不足 | 对完美真人可迁移 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LC-01 | Live/Baccarat | Evolution / Ezugi | 全球 Live Casino B2B / RNG 内容 | P1/P2 | 全球 Studio、Live 产品工程、多地区运营、约 2,000 张 Live tables（2025 年报） | 附件旧稿部分 AI 宣称曾由 SEO/内容农场污染；不得把未公开模型写成官方事实 | QoE、Studio capacity、游戏版本治理、多地区容灾、专属桌/品牌化 |
| LC-02 | Live/Baccarat | Playtech Live | Live + PAM+ + safer gambling + managed services | P1 | 2025 年报：50+ regulated jurisdictions、200+ B2B clients、28 brands 使用 BetBuddy；2026-07 AI-powered Live Virtual Host 已上线多个客户 | 平台复杂、整合和供应商锁定成本高；AI 主张仍需逐产品验证 | PAM/Live/RG/Case 一体化、Virtual Host、模型治理、人机协同 |
| LC-03 | Live/Baccarat | Pragmatic Play Live | Live 内容与移动端产品 | P1/P2 | 产品化速度、移动 UX、多语言和内容包装强 | Auto-Roulette/Bot 不等于 AI 决策；公开 AI/RL 中台证据有限 | 移动体验、快速内容交付、统一运营工具 |
| LC-04 | Live/Baccarat | SA Gaming | 亚洲真人内容 | P3 | 亚洲本地化、桌台和玩法覆盖 | 公开 AI/ML 模型卡、数据集、审计证据不足 | 产品/地区化/桌台密度 benchmark；AI 能力采购前尽调 |
| LC-05 | Live/Baccarat | Dream Gaming (DG) | 亚洲真人内容 | P3 | 竞咪、亚洲仪式感和玩法覆盖 | 外部技术透明度低 | 产品体验 benchmark；AI/风控不作事实推断 |
| LC-06 | Live/Baccarat | WM Casino / WM Perfect Group | 真人百家乐 / Streaming / Ecosystem | P3 | 最贴近本项目实际业务语境，可构建 Player–Dealer–Table–Agent 多实体分析 | 公开技术白皮书、模型卡和独立审计不足 | 作为内部 GDI-OS 主体；外部比较必须证据分层 |
| LC-07 | Live/Baccarat | Asia Gaming (AG) | 亚洲真人内容 | P3 | VIP / Interactive Bid 等本地化产品 | 公开 AI 证据不足 | 高限额/包房/节奏的产品 benchmark |
| LC-08 | Live/Baccarat | AllBet | 亚洲真人内容 | P3 | 百家乐/路单体验 | 多为营销/代理信息，技术透明度低 | 仅作产品 benchmark |
| LC-09 | Live/Baccarat | Sexy Baccarat / AE Sexy | 亚洲真人内容 | P3 | 娱乐化、本地化 | 假站/代理混淆风险、监管与技术证据需独立核验 | 品牌/UX benchmark，不继承任何 AI 宣称 |
| LC-10 | Live/Baccarat | Pretty Gaming | 亚洲真人内容 | P3 | 区域化真人桌 | 技术披露有限 | 产品 benchmark |
| LC-11 | Live/Baccarat | Venus Casino | 亚洲真人内容 | P3 | 区域化真人桌 | 技术披露有限 | 产品 benchmark |
| LC-12 | Live/Baccarat | Big Gaming | 亚洲真人内容 | P3 | 区域化真人桌 | 技术披露有限 | 产品 benchmark |
| LC-13 | Live/Baccarat | eBet | 亚洲真人内容 | P3 | 区域化真人桌 | 技术披露有限 | 产品 benchmark |
| LC-14 | Live/Baccarat | BetGames.TV | Live / hosted games | P2/P3 | 主持类内容和直播产品经验 | 与传统百家乐 Studio 模式不同；AI 宣称须另证 | 直播内容产品化 |
| LC-15 | Live/Baccarat | KingMaker | 亚洲内容聚合/桌游 | P3 | 区域化游戏覆盖 | 公开 AI 技术细节不足 | 内容 benchmark |
| LC-16 | Live/Baccarat | Octane Studios | AI Dealer / AI Baccarat 新势力 | P2 | AI Dealer 作为前台表现层、品牌化、弹性扩展概念前沿 | 规模、长期稳定性、监管路径、独立认证仍需尽调 | 仅在测试线 Pilot；RNG/结果引擎与生成式表现层隔离 |
| LC-17 | Live/Baccarat | Sentient Studios | AI Dealer | P1/P2 | 官网现列 Blackjack / Roulette / Baccarat，70+ languages、品牌化与自动扩容 | 厂商自述为主；历史资料“12 语言/百家乐尚未上线”已过时；需独立认证和性能证据 | AI Dealer UX、低额私人桌、多语言；严格隔离结果与人格层 |
| LC-18 | Live/Baccarat | Sentient Gaming Group | AI Live Casino / AI croupier | P2 | QTech 2026 已上线 AI Roulette，并公开 Baccarat 等后续产品方向 | 与 Sentient Studios 名称近似但不是同一主体；不可混并 | AI croupier 渠道分发和互动层 benchmark |
| LC-19 | Live/Baccarat | SkyGaming | AI Live Dealer | P2/P3 | 公开宣传 24/7、多语言、无限桌/座位 | 成熟度、牌照、RNG/认证、真实客户规模需独立核验 | 候选 Pilot，不作为行业标准 |
| LC-20 | Live/Baccarat | BetConstruct / BetConstruct AI / KISS AI Live Casino | 平台 + AI Live 产品 | P1/P2 | 2026 KISS AI Live Casino 有官方客户区活动/产品存在性证据；BetConstruct 有完整平台生态 | “实时改变 Dealer/桌面/视觉”等细节多为营销表述，缺技术白皮书 | 平台化、产品编排、AI Live Pilot；高影响动作需治理 |
| LC-21 | Live/Baccarat | Winfinity | AI Computer Vision baccarat | P1 | 官方资料明确用 in-house video recognition / ANN 识别实体牌，减少条码依赖 | 供应商规模和跨场景泛化需验证 | 物理牌面机器视觉、冗余识别、结算证据链 |
| LC-22 | Live/Baccarat | Angel Group | 智能桌 / RFID / 视觉 | P2 | 实体桌数据化、RFID/姿态/牌桌状态可观测 | 硬件资本开支、摄像数据隐私、线上场景不同 | 事件化、桌台数字孪生、实体世界数据质量 |
| LC-23 | Live/Baccarat | IDX Games | 桌游分析 / chatbot | P2/P3 | 运营洞察概念 | 公开独立基准有限 | 辅助分析，不作自动裁决 |
| LC-24 | Live/Baccarat | Arb Labs / ChipVue | 桌面视觉/数据采集 | P2/P3 | 附件提及实时桌面数据自动收集 | 准确率和部署规模为供应商/合作方口径 | 桌面遥测、旁路观测；先做独立测试 |
| LC-25 | Live/Baccarat | Avanti Studios | 数字/AI 荷官 | P2/P3 | 3D/数字克隆式荷官概念 | 监管、信任、成熟度和真实部署需核验 | 生成式表现层实验 |
| OP-01 | B2C/Operator | Entain | B2C 多品牌运营 / ARC | P1 | ARC/Protector、玩家保护数据科学公开度高 | 公开资料偏集团级 RG，不能外推到每张百家乐桌；准确率等数字需样本定义 | 集团级 Responsible Gambling、实时交互、模型治理 |
| OP-02 | B2C/Operator | Flutter Entertainment | B2C 集团 | P1 | 多品牌、体育/赌场/交易所生态；Responsible AI / safer gambling 能力 | 并购和多品牌技术栈复杂；集团能力≠单品牌/单游戏能力 | 跨品牌治理、实时干预、模型/政策标准化 |
| OP-03 | B2C/Operator | FanDuel | Flutter 旗下体育/赌场 | P1 | 美国受监管市场、地理围栏、规模化运营 | 美国州级规则不能直接外推全球 | 体育/赌场统一账户治理、地理合规 |
| OP-04 | B2C/Operator | PokerStars | Flutter 旗下扑克/赌场 | P1 | 全球在线游戏品牌和账户风控经验 | 扑克风险结构与百家乐不同 | 账户/支付/多市场治理 |
| OP-05 | B2C/Operator | Sportsbet | Flutter 澳大利亚品牌 | P1 | Real Time Intervention 源头之一 | 地域监管语境强 | 实时玩家保护和人机协同 |
| OP-06 | B2C/Operator | Betfair | Flutter 交易所 | P1/P2 | 交易所微结构、异常交易和市场数据经验 | 交易所与庄家模式不同 | 市场微结构、对冲/套利识别、风险限额 |
| OP-07 | B2C/Operator | FDJ UNITED / legacy Kindred Group | 欧洲彩票+在线博彩集团 | P1 | 2024 收购 Kindred，2025 更名 FDJ UNITED；兼具 lottery 和 online betting/gaming | 历史 Kindred/Unibet 指标需标注时期；集团重组后口径变化 | 跨垂直集团治理、PS-EDS lineage、彩票公共信任 |
| OP-08 | B2C/Operator | Unibet | FDJ UNITED/legacy Kindred 品牌 | P1 | PS-EDS 历史与在线博彩运营 | 品牌≠集团；历史证据须按时间归属 | 玩家安全、跨产品身份 |
| OP-09 | B2C/Operator | BetMGM | 受监管 B2C | P1/P2 | 美国合规、MGM 生态、CRM 供应商案例 | 州级隔离、外部供应商案例不能当自研能力 | 地理围栏、赌场品牌/线上融合 |
| OP-10 | B2C/Operator | DraftKings | 体育/赌场 B2C | P1/P2 | 大规模数据、体育/赌场产品、美国合规 | 附件包含剥削性目标函数的二手争议案例；必须区分事实与报道 | 正向借鉴数据平台；反向借鉴目标函数治理 |
| OP-11 | B2C/Operator | Sisal | 彩票/博彩运营 | P1/P2 | 彩票与数字博彩融合；Optimove 案例 | 供应商案例指标不可作独立 SLA | 跨垂直 CRM/运营 |
| OP-12 | B2C/Operator | Stardust | 运营商品牌 / Optimove 案例 | P2 | CRM 案例有量化效果 | 案例可能受选择偏差/厂商口径影响 | 实验设计 benchmark |
| OP-13 | B2C/Operator | OPAP | 希腊彩票/博彩运营 | P1/P2 | 彩票/博彩、多渠道；合规技术案例 | 集团结构已与 Allwyn 组合发生变化 | omnichannel 与集团治理 |
| OP-14 | B2C/Operator | Stake | 加密/在线博彩品牌 | P2/P3 | 产品速度、加密支付、全球化体验常被行业对标 | 牌照/地区合规、KYC/提现投诉等需逐司法辖区核验；不可用论坛投诉作系统性事实 | 只借鉴可验证 UX/工程，不复制监管套利 |
| OP-15 | B2C/Operator | BC.Game | 加密博彩品牌 | P2/P3 | 产品/加密生态知名度 | 监管、法人、牌照和投诉需时点化核验 | 竞品 UX 观察，不作技术事实外推 |
| OP-16 | B2C/Operator | 1xBet | 大型国际博彩品牌 | P2/P3 | 广泛体育/赌场覆盖 | 监管/牌照争议跨地区差异大 | 仅作市场/产品结构 benchmark |
| OP-17 | B2C/Operator | Dafabet | 亚洲体育/赌场品牌 | P2/P3 | 亚洲本地化、体育+赌场 | 公开技术栈较少 | 区域化和支付体验 benchmark |
| OP-18 | B2C/Operator | bet365 | 全球体育/赌场运营 | P1/P2 | 体育交易、规模、产品成熟度 | 核心技术高度闭源 | 体育风险、实时交易和运营 benchmark |
| OP-19 | B2C/Operator | 888.com | 在线博彩品牌 | P2 | 附件提及推荐系统案例 | 旧品牌/集团结构和技术口径需当前核验 | 推荐/内容发现仅作线索 |
| OP-20 | B2C/Operator | Golden Matrix Group | B2B/B2C gaming group | P2 | 附件提及个性化内容推荐 | 供应商自述为主 | 推荐/运营案例线索 |
| OP-21 | B2C/Operator | 188BET | 亚洲体育/赌场品牌 | P2/P3 | 亚洲市场、本地化 | 附件中的 Frosmo/预测数字缺一手验证 | 只保留为 INFERRED 案例，不作为 KPI |
| OP-22 | B2C/Operator | HENGPLAY | 附件提及平台 | P3 | 自动支付/安全宣传 | 技术、牌照、AI 事实证据弱 | 仅入名册，采购前尽调 |
| OP-23 | B2C/Operator | LeoVegas | 受监管在线赌场品牌 | P1/P2 | 欧洲受监管市场经验 | 附件仅作为平台示例，非核心技术来源 | 合规/UX benchmark |
| OP-24 | B2C/Operator | Caesars Entertainment / Caesars Sportsbook | 综合赌场/体育 | P1 | 受监管实体赌场+数字体育 | 美国市场结构特殊 | omnichannel、合规和地理围栏 |
| OP-25 | B2C/Operator | Rivalry | 电竞/体育博彩品牌 | P2/P3 | 电竞与年轻用户产品 | 规模/盈利/地区覆盖需当前核验 | 电竞数据产品 benchmark |
| PL-01 | B2B/PAM/CRM | SOFTSWISS | B2B casino platform / anti-fraud | P1 | 官方 2025 1–8 月称 prevented €15M+ fraudulent transactions、56k+ tasks；平台/运营工具完整 | 跨年度请求量与“节省额”口径不可直接同比；厂商数据需独立审计 | 案件化反欺诈、运营指标监控、人工复核 |
| PL-02 | B2B/PAM/CRM | EveryMatrix | CasinoEngine / EngageSuite / Bonus Guardian | P1 | Bonus Guardian 官方 AI/ML；Future Anthem 2026 内容推荐已向 EveryMatrix 客户开放 | 提款 hold 等高影响动作必须人工/政策约束；uplift 为供应商案例 | Bonus abuse、实时推荐、平台整合 |
| PL-03 | B2B/PAM/CRM | Smartico | CRM + gamification | P1/P2 | gamification-led CRM、实时运营成熟 | 2026-04 可核实的是 Optimove 签署收购协议，未找到独立 completion 公告；RL/MAB 细节逐版本验证 | CRM 编排、gamification；RG firewall 强制 |
| PL-04 | B2B/PAM/CRM | Optimove | CRM / AI decisioning / personalization | P1 | 2026 AI decisioning agents、营销编排能力公开 | 营销优化容易与玩家保护目标冲突 | 实验/编排/推荐，但 RG 风险绝不进入促销目标 |
| PL-05 | B2B/PAM/CRM | GiG | B2B 平台 | P2/P3 | 平台/推荐生态 | 附件 AI 效果多为二手/供应商口径 | 作为采购候选，先取模型卡/SLA |
| PL-06 | B2B/PAM/CRM | NuxGame | B2B 平台 | P2 | 与 KYC/identity 供应商整合 | AI 内核公开度有限 | KYC/AML 编排候选 |
| PL-07 | B2B/PAM/CRM | Future Anthem | 实时 AI 个性化 | P1/P2 | EveryMatrix 官方 2026 集成；25k+ games 模型元数据；5–8% NGR uplift 为厂商案例 | 效果数字非独立审计，且营收目标不可与 RG 混用 | 实时推荐、实验方法、API 设计 |
| PL-08 | B2B/PAM/CRM | SCCG Management | 咨询/渠道合作 | P2 | 生态合作与市场进入 | 不是核心 AI 技术提供商 | 合作尽调/市场情报，不作模型能力来源 |
| PL-09 | B2B/PAM/CRM | CleverBet Labs | 附件扩展主体 | P3 | 列入研究池 | 当前公开证据不足 | 保留，不臆测 |
| PL-10 | B2B/PAM/CRM | Track360 | 附件扩展主体 | P3 | 列入研究池 | 当前公开证据不足 | 保留，不臆测 |
| RK-01 | Fraud/KYC/AML | Visa / Featurespace ARIC | 支付欺诈 / 实时行为建模 | P1 | Visa 2024-12-19 已完成收购；Featurespace 为实时 AI 风险评分成熟标杆 | 支付欺诈标签/成本结构不同于博彩串通；阈值不可照搬 | 实时行为画像、adaptive risk scoring、模型治理 |
| RK-02 | Fraud/KYC/AML | SEON | device / digital footprint fraud | P2 | 设备、账户、红利滥用情报 | 供应商口径，隐私/误伤需评估 | 设备风险与实体解析 |
| RK-03 | Fraud/KYC/AML | GeoComply | geolocation / device integrity | P1/P2 | 地理围栏与设备风控成熟 | 强地域依赖，数据/SDK隐私和成本 | 地理合规、设备完整性 |
| RK-04 | Fraud/KYC/AML | Sumsub | KYC / identity / deepfake | P2 | 身份、活体、深伪检测 | 供应商锁定、误拒、数据跨境 | KYC 编排、deepfake 防御 |
| RK-05 | Fraud/KYC/AML | Onfido | KYC / identity | P2 | 身份验证成熟 | 同类替代多，采购看覆盖/误拒/SLA | 身份验证候选 |
| RK-06 | Fraud/KYC/AML | Jumio | KYC / identity | P2 | 全球身份验证 | 同上 | 身份验证候选 |
| RK-07 | Fraud/KYC/AML | Veriff | KYC / identity | P2 | 身份验证/活体 | 同上 | 身份验证候选 |
| RK-08 | Fraud/KYC/AML | iDenfy | KYC / identity | P2 | iGaming 集成案例 | 供应商自述 | 身份验证候选 |
| RK-09 | Fraud/KYC/AML | Shufti | KYC / identity | P2 | 身份/AML 与客服生态 | 供应商自述 | 身份验证候选 |
| RK-10 | Fraud/KYC/AML | CrossClassify | account takeover / fraud | P2/P3 | 行为/账户异常方向 | 独立博彩基准有限 | 挑战者模型候选 |
| RK-11 | Fraud/KYC/AML | Sift | digital trust / payment fraud | P2 | 成熟反欺诈平台 | 电商/支付标签与博彩不同 | 实时风控、设备/行为特征 |
| RK-12 | Fraud/KYC/AML | Group-IB | cyber/fraud intelligence | P2 | 安全与欺诈情报/XAI | 与业务风控边界需明确 | 账户接管、威胁情报 |
| RK-13 | Fraud/KYC/AML | cside | browser supply-chain / bot signals | P2 | 浏览器层信号、第三方脚本风险 | 供应商自述和环境依赖 | 前端供应链与自动化检测 |
| RK-14 | Fraud/KYC/AML | Flagright | AML / case management | P2 | AML workflow、案件与审计 | 博彩专用效果需验证 | AML case management |
| RK-15 | Fraud/KYC/AML | ComplyAdvantage | AML / sanctions / PEP | P2 | 制裁/PEP/负面新闻数据 | 数据覆盖与误报成本 | AML screening |
| RK-16 | Fraud/KYC/AML | NICE Actimize | AML / financial crime | P1/P2 | 银行业成熟交易监控 | 成本高、实施重、博彩阈值需重标定 | AML model governance/case workflow |
| RK-17 | Fraud/KYC/AML | ACT / Fraud Rings | graph / syndicate visualization | P2/P3 | 团伙图谱方向高度同构 | 具体产品/基准证据有限 | 图谱调查界面思路 |
| RK-18 | Fraud/KYC/AML | Infocredit Group / ComplianceSuite.ai | compliance platform | P2 | 合规/AML 工作流 | 奖项/客户不等于模型效果 | 合规工作流候选 |
| RK-19 | Fraud/KYC/AML | Cevro AI | customer service agent | P2/P3 | 多语言客服 Agent 概念 | 80–90% 工单等数字需独立验证；高风险事项不可自动处置 | 低风险 FAQ/流程自动化 |
| RK-20 | Fraud/KYC/AML | InteractiveAI | customer service agent | P2/P3 | 受边界约束 Agent | 公开基准有限 | 客服低风险自动化 |
| RK-21 | Fraud/KYC/AML | Moveo.AI | customer service agent | P2/P3 | 多系统集成 | 公开博彩基准有限 | 客服辅助 |
| RK-22 | Fraud/KYC/AML | Quantexa | entity resolution / graph / AML | P1/P2 | 金融犯罪实体解析和图谱成熟 | 成本/实施复杂；不能把概率关联当事实身份 | 概率实体解析、网络情报、AML |
| RG-01 | Responsible Gambling | Mindway AI / GameScanner / Gamalyze | responsible gambling | P1/P2 | 官方 2026 资料称 GameScanner 每月监测 14.7m active players；神经科学+AI定位清晰 | 效果数字多为供应商自述；跨市场阈值/公平性需独立验证 | RG 风险评分、专家回标、干预优先级 |
| RG-02 | Responsible Gambling | Neccton / Mentor | responsible gambling | P2 | 早期风险检测方向 | 独立基准有限 | RG challenger |
| RG-03 | Responsible Gambling | Sportradar / Bettor Sense | responsible gambling / sports data | P1/P2 | 体育数据和 RG 产品生态 | Bettor Sense 效果需按客户验证 | session 风险、体育 RG |
| RG-04 | Responsible Gambling | Playtech BetBuddy / Playtech Protect | responsible gambling | P1 | 2025 年报明确 AI-driven behavioural analytics；28 brands 使用 BetBuddy | 品牌数≠效果；高风险自动决策需人工救济 | RG 模型、case workflow、解释与干预 |
| RG-05 | Responsible Gambling | Entain ARC | responsible gambling | P1 | 集团级保护框架和实时交互 | 26/近30 markers 等历史数字时点冲突；模型性能缺统一基准 | RG policy engine、实时保护 |
| RG-06 | Responsible Gambling | FDJ UNITED / legacy Kindred PS-EDS | responsible gambling | P1/P2 | Kindred 历史早期检测体系；现归 FDJ UNITED 语境 | 历史模型与当前集团治理需区分 | RG 早期检测、集团整合 |
| AD-01 | Adversarial/Research | FPLAY | player-side automation | P3/P4 | 可作为 bot/automation 威胁模型线索 | 工具宣传不可当效果事实；不可用于未经授权自动下注 | 仅用于防御性特征设计 |
| AD-02 | Adversarial/Research | Mysports.AI | player-side automation / advantage claims | P3/P4 | 作为剩余牌/自动读取类威胁模型 | 宣称真实性与合法性不确定 | 仅用于防御性红队假设 |
| AD-03 | Adversarial/Research | Oracle Baccarat Predictor | player-side predictor | P3/P4 | 代表“ML 预测路单”市场叙事 | 不证明可持续超额优势 | 用于识别虚假胜率宣称与 bot 行为 |
| AD-04 | Adversarial/Research | BACC.BOT | player-side predictor | P3/P4 | 代表深度学习营销叙事 | 独立证据不足 | 威胁建模 |
| AD-05 | Adversarial/Research | BaccaratAI | player-side predictor | P3/P4 | 代表 AI predictor 类别 | 独立证据不足 | 威胁建模 |
| AD-06 | Adversarial/Research | Differential Labs | research / advantage-play analysis | P2 | 附件引用边注 AI 优势玩法研究 | 年损/收入比例属研究估计，不可直接当自家 ROI | 形成 side-bet exposure stress test，不作因果结论 |
| SP-01 | Sports | Genius Sports / GeniusIQ | official sports data / AI / trading tech | P1 | 2025 20-F：AI、computer vision、official data、real-time capture；400+ leagues/federations、550+ sportsbook brands | 数据权成本高、单一官方 feed 依赖；广告优化与 RG 必须隔离 | official-data governance、fail-safe capture、低延迟、AI data layer |
| SP-02 | Sports | Sportradar | sports data / odds / risk / integrity | P1 | 2025 20-F 明确 ML/AI liability-driven odds adjustment 和 sportsbook risk management | 复杂供应商依赖、数据/模型闭源 | odds/liability、bet acceptance、integrity、real-time inferencing |
| SP-03 | Sports | Kambi | sportsbook platform/trading | P1 | 2025 年报：AI-driven trading 占 48% bets | AI coverage≠完全自治，需 trader oversight | 人机混合 trading、risk/odds SLO |
| SP-04 | Sports | Stats Perform | sports data | P1/P2 | 大规模体育数据/Opta生态 | 数据权/成本和赛事覆盖差异 | 体育数据质量与特征工程 |
| SP-05 | Sports | IMG ARENA | sports data/streaming | P1/P2 | 赛事数据与 streaming 权利 | 版权依赖 | 官方/准官方数据接入治理 |
| SP-06 | Sports | SIS (Sports Information Services) | sports data/content | P1/P2 | 赛事内容/数据服务 | 覆盖结构特定 | 多源 feed 冗余 |
| SP-07 | Sports | Oddin.gg | esports betting data/trading | P1/P2 | 电竞赔率/风险垂直 | 电竞标签与传统体育不同 | 电竞域专化 |
| SP-08 | Sports | OpenBet | sportsbook platform | P1/P2 | 大型 sportsbook 平台 | 平台锁定/集成复杂 | buy-vs-build benchmark |
| SP-09 | Sports | SBTech (DraftKings legacy) | sportsbook technology lineage | P2 | 体育平台/交易技术历史 | 当前归属与产品已演化 | 架构历史 benchmark |
| SP-10 | Sports | OpticOdds | sports odds/data | P2 | 赔率数据/聚合 | 独立 AI 证据有限 | feed redundancy |
| SP-11 | Sports | Don Best | odds/data lineage | P2 | 赔率数据历史品牌 | 技术代际/归属需当前核验 | 赔率基准 |
| SP-12 | Sports | Metric Gaming | sportsbook tech | P2/P3 | 定价/交易技术候选 | 公开细节有限 | 候选 benchmark |
| SP-13 | Sports | Amelco | sportsbook/platform | P2 | 交易/平台解决方案 | 公开模型细节有限 | buy-vs-build benchmark |
| LT-01 | Lottery | Brightstar Lottery (former IGT Lottery) | pure-play lottery | P1 | 2025 改名；SEC 2025 20-F 明确 pure-play global lottery；零售/数字/运营完整 | 政府合同重、转换周期长 | lottery core、retail/digital、审计、高可用 |
| LT-02 | Lottery | Scientific Games | lottery systems / instant / iLottery | P1/P2 | 全球彩票技术、即开票、数字化和 omnichannel | 政府采购周期长、供应商锁定 | PAM/wallet/CRM/Healthy Play、central system |
| LT-03 | Lottery | Pollard Banknote | instant tickets / lottery tech | P1/P2 | 即开票和数字彩票生态 | 业务偏彩票垂直 | ticket lifecycle / secure print / digital |
| LT-04 | Lottery | Inspired Entertainment | lottery/virtual/content | P1/P2 | 虚拟/彩票内容 | 与中央彩票系统不同 | 内容层 benchmark |
| LT-05 | Lottery | Instant Win Gaming (IWG) | eInstant/iLottery content | P1/P2 | eInstant 专长 | 内容层不等于 central system | 数字彩票产品 |
| LT-06 | Lottery | Intralot | lottery/sports systems | P1 | 中央系统/零售/托管经验 | 大型政府系统复杂 | central system / terminal / managed services |
| LT-07 | Lottery | Genlot | lottery systems | P2 | 彩票系统供应商 | 公开国际基准有限 | 系统候选 |
| LT-08 | Lottery | AGTech | lottery/digital tech | P1/P2 | 亚洲彩票/数字生态 | 地区和监管差异 | 亚洲彩票 benchmark |
| LT-09 | Lottery | NeoPollard Interactive | iLottery | P1/P2 | 数字彩票/账户平台 | 市场集中 | iLottery account / content |
| LT-10 | Lottery | Allwyn | lottery/gaming operator | P1 | 大型欧洲彩票运营集团；2026 与 OPAP 组合完成（按公开报告） | 并购后口径快速变化 | 集团治理、特许经营、omnichannel |
| LT-11 | Lottery | FDJ UNITED | lottery + betting/gaming | P1 | 法国/爱尔兰彩票 + 欧洲线上博彩；Kindred 已并入 | 集团口径变化 | 彩票公共信任+数字博彩治理 |
| LT-12 | Lottery | Sisal | lottery/gaming operator | P1/P2 | 彩票/博彩运营经验 | 市场/集团归属需按时点 | omnichannel |
| LT-13 | Lottery | Lotto NZ | lottery operator | P1/P2 | 国家彩票运营 | 市场规模小、监管语境独特 | Responsible Play / public-trust benchmark |
| LT-14 | Lottery | Macau SLOT | sports/lottery-style operator | P2/P3 | 地区性运营 | 范围/法规特殊 | 区域 benchmark |
| LT-15 | Lottery | Camelot (legacy UK National Lottery operator) | lottery operator lineage | P1 | 英国国家彩票历史运营经验 | 已非当前 UK National Lottery 运营主体 | 迁移 legacy transition / contract handover lessons |
| XI-01 | Cross-Industry | Palantir | data integration / ontology / defense-industry benchmark | P1/P2 | 实体/事件/权限/ontology 一体化思路 | 成本、闭源、国防语境不可照搬 | 实体图谱、case workspace、policy-aware data integration |
| XI-02 | Cross-Industry | SpaceX | aerospace software/operations benchmark | P2 | 高可靠、遥测、快速工程迭代 | 大量内部栈闭源，附件二手资料不可视为完整事实 | SLO、telemetry、replay、fail-safe |
| XI-03 | Cross-Industry | Blue Origin | aerospace benchmark | P1/P2 | 安全关键工程 | 业务完全不同 | 验证文化/供应链 |
| XI-04 | Cross-Industry | Rocket Lab | aerospace benchmark | P1/P2 | 垂直整合与快速迭代 | 业务不同 | 工程/遥测思路 |
| XI-05 | Cross-Industry | Airbus | aerospace / industrial data | P1 | 制造、数字孪生、Skywise生态 | 强行业专用 | asset/data governance |
| XI-06 | Cross-Industry | Boeing | aerospace benchmark | P1 | 大型安全关键供应链 | 不可把航空认证直接当博彩法规 | 变更控制/供应链质量 |
| XI-07 | Cross-Industry | Lockheed Martin | defense/aerospace | P1 | 高可靠和复杂系统工程 | 军工管制/成本远超博彩 | assurance / FMEA |
| XI-08 | Cross-Industry | Anduril | defense software/hardware | P1/P2 | 实时传感/软件定义系统 | 军事用途不可照搬 | 实时融合、可观测性 |
| XI-09 | Cross-Industry | Thales | aerospace/defense/transport | P1 | 安全关键系统与遥测 | 业务差异 | FDIR / monitoring |
| XI-10 | Cross-Industry | Eutelsat | satellite operator | P1 | 大规模遥测运营 | 业务差异 | time-series operations |
| XI-11 | Cross-Industry | C3 AI | enterprise AI | P1/P2 | 工业 AI 平台经验 | 采购成本/闭源 | model ops benchmark |
| XI-12 | Cross-Industry | Oracle | database / AML / enterprise | P1 | 企业数据库和金融犯罪产品成熟 | 成本/锁定 | transactional integrity / AML |
| XI-13 | Cross-Industry | BAE Systems | defense/aerospace | P1 | 安全关键/供应链 | 军工语境 | assurance benchmark |
| XI-14 | Cross-Industry | ST Engineering | aerospace/MRO | P1 | MRO/工程运营 | 行业不同 | asset reliability / operational governance |
| XI-15 | Cross-Industry | SAP | ERP / enterprise data | P1 | 财务/供应链治理成熟 | 重实施 | 财务主数据/采购/供应商治理 |
| XI-16 | Cross-Industry | Snowflake | cloud data platform | P1 | 数据治理/共享/warehouse | 成本和云锁定 | governed analytics |
| XI-17 | Cross-Industry | Databricks | lakehouse / ML | P1 | lakehouse/MLOps | 平台复杂/成本 | feature/model lifecycle |
| XI-18 | Cross-Industry | Microsoft | cloud/security/data | P1 | 企业 IAM/安全/数据生态 | 供应商锁定 | identity/zero trust/observability |
| XI-19 | Cross-Industry | AWS | cloud infrastructure | P1 | 全球云、事件/安全服务 | 成本、跨境/监管 | resilience / managed services |
| XI-20 | Cross-Industry | Google Cloud | cloud/data/AI | P1 | 数据/AI/安全 | 同上 | analytics/AI platform benchmark |
| XI-21 | Cross-Industry | NVIDIA | GPU / AI infrastructure | P1 | 推理/训练生态 | GPU 并非所有风控必需 | CV/GNN/LLM only when justified |
| XI-22 | Cross-Industry | TSMC | semiconductor benchmark | P1 | 先进制造/质量管理 | 与博彩软件直接同构度低 | 供应链风险/质量纪律 |
| XI-23 | Cross-Industry | CrowdStrike | cybersecurity | P1 | EDR/threat intelligence | 安全告警阈值不可直接映射客户风控 | Detection-as-Code/telemetry culture |
| XI-24 | Cross-Industry | Palo Alto Networks | cybersecurity | P1 | 网络/云安全与 SOC | 同上 | zero trust / SOC |
| XI-25 | Cross-Industry | Citadel | quant/HFT benchmark | P2 | 低延迟、研究纪律、风险管理 | 交易 alpha 不可移植为玩家剥削 | time-aware validation / tail latency |
| XI-26 | Cross-Industry | Jane Street | quant/HFT benchmark | P2 | 概率/交易系统与工程文化 | 同上 | simulation / risk controls |
| XI-27 | Cross-Industry | Two Sigma | quant/data science benchmark | P2 | 大规模研究/数据平台 | 同上 | research reproducibility / model monitoring |
| XI-28 | Cross-Industry | Frosmo | personalization platform | P2 | 附件关联 188BET 推荐案例 | 具体数字缺一手独立验证 | 作为历史推荐系统线索 |
| XI-29 | Cross-Industry | Las Vegas Sands / Sands China | land-based casino operator | P1/P2 | 实体赌场运营规模 | 实体与线上差异 | smart-table / floor operations benchmark |
| XI-30 | Cross-Industry | Bloomberry Resorts / Solaire | land-based casino operator | P1/P2 | 亚洲实体赌场 | 附件 AI 部署数字需独立核验 | 实体 smart-table benchmark |
| XI-31 | Cross-Industry | SkyCity Entertainment | casino operator | P1/P2 | 实体赌场运营 | 附件 AI 部署数字需独立核验 | 实体 smart-table benchmark |
| XI-32 | Cross-Industry | Light & Wonder | gaming technology/content | P1 | 内容、平台和赌场技术 | 附件仅扩展对标 | content/platform benchmark |

---

# 6. 竞争版图：能力拼图

## 6.1 Live Casino / Baccarat

### Evolution
借鉴 Live Studio 工程、游戏版本治理、QoE、多区域容灾、专属桌/品牌化、规模化运营。未有一手证据的具体 AI 功能继续保持 P2/P3。

### Playtech
最值得拆解的是 `PAM+ + Live + BetBuddy + Managed Services + AI Virtual Host`。2026-07 Virtual Host 已由半年报确认向多个客户上线。

### Pragmatic Play
借鉴移动端、快速产品化、内容包装、多语言；Auto-Roulette/Bot 不等于机器学习/RL。

### AI/Virtual Dealer 队列必须拆层
`Outcome Engine / Perception / Render / Dialogue / Personalization / Studio Ops`

Sentient Studios、Sentient Gaming Group、Playtech Virtual Host、BetConstruct KISS AI、SkyGaming、Avanti、Octane 的成熟度、监管路径与证据等级不同，禁止并成一个“AI Dealer 已成熟”结论。

Winfinity 归入 **Perception / Computer Vision**，不是人格型 AI Dealer。

---

# 7. GDI-OS v3 Blueprint

```text
L0  SOURCE / TRUST ZONES
    Game | Video | Bet | Wallet | Payment | KYC | Agent | RG | Support
      ↓
L1  CANONICAL EVENT LEDGER
    event_id | event_time | ingest_time | source_seq | schema_ver | hash
      ↓
L2  QUALITY / REPLAY / POINT-IN-TIME
    data contracts | DQ gates | reconciliation | late events | lineage
      ↓
L3  ENTITY + FEATURE
    player/account/device/payment/agent/table/dealer/session/round graph
      ↓
L4  DETECTION / PREDICTION
    rules → GLM/scorecard → GBDT → survival/HMM → graph → sequence
      ↓
L5  registry_risk_topology
    entity × risk × time × probability × severity × confidence × evidence
      ↓
L6  CONSTRAINED DECISION ENGINE
    policy eligibility | RG/AML veto | jurisdiction | economic contract
      ↓
L7  CASE + HUMAN REVIEW
    evidence | reason codes | explanations | dual control | appeal | rollback
      ↓
L8  ACTION
    observe | verify | review-hold | limit | RG interaction | no-action
      ↓
L9  OUTCOME LEDGER
    D+1/D+7/D+30 | confirmed outcome | cost | complaint | appeal | RG result
      ↓
L10 EVALUATION / LEARNING
    A/B | CUPED | switchback | DR/uplift | calibration | drift | fairness
```

## 7.1 `registry_risk_topology` v3

```text
as_of_time
entity_type
entity_id
entity_resolution_version
risk_domain
risk_taxonomy
risk_subtype
tactic
technique
procedure
rule_id
rule_version
model_id
model_version
feature_snapshot_hash
probability
calibrated_probability
severity
confidence
uncertainty
ood_score
evidence_count
evidence_refs
first_seen
last_seen
trend
peer_group
jurisdiction
economic_contract_id
eligibility
policy_vetoes
recommended_action
human_review_required
reviewer
reviewed_at
decision_status
appeal_status
rollback_flag
outcome_status
outcome_date
label_quality
```

## 7.2 三管线强制隔离
1. Fraud / Collusion / Bonus Abuse
2. AML / Financial Crime
3. Responsible Gambling

---

# 8. 模型路线：禁止 Transformer-first

| Level | 模型 | 晋级条件 |
|---|---|---|
| 0 | 规则、Wilson、EWMA、GLM/scorecard | DQ、定义与 calibration 基线稳定 |
| 1 | XGBoost/LightGBM/CatBoost | OOT 优于 Level 0 且 FP 成本可控 |
| 2 | Survival / competing risks | 事件时点比静态分类有增量 |
| 3 | HMM / state-space / IMM | 状态转移稳定、跨窗口可复现 |
| 4 | Graph / entity resolution | 图增量超过简单统计/peer group |
| 5 | Sequence / Transformer | 严格 walk-forward 下长期稳定增量 |
| 6 | Contextual bandit / constrained RL | OPE + causal baseline + safe action set + compliance sign-off |

## 8.1 “140 表 → 15 风险类”只强化不删除

`7 windows × modules → feature snapshots → risk topology → 15 risk-domain materialized views`

15 张风险表继续保留为业务交付视图，但不再是系统唯一真相。

---

# 9. IQ / OQ / PQ / MQ 四门

## IQ
SBOM、seed、source fingerprint、data contract、DAG replay、权限与依赖。

## OQ
DQ、point-in-time、PR-AUC、Precision@capacity、Recall@FP-budget、Brier/ECE、purged walk-forward、negative controls、OOD。

## PQ
p95/p99/p99.9、peak load、backpressure、no-event-loss、reconciliation、fallback、replay exactness、audit completeness。

## MQ（v3 新增）
model inventory、conceptual soundness、independent validation、vendor model DD、challenger、ongoing monitoring、outcome analysis、override governance、retirement。

> SR 26-2、ALCOA+、21 CFR Part 11、DO-178C 等均作为**借鉴型最佳实践**；不是博彩业法定要求。

---

# 10. RedTeam v3 — 32 个攻击面

1. SEO/affiliate 伪装官方来源。
2. 两个二手源复制同一错误。
3. 厂商 uplift 无 holdout/denominator。
4. B2B/B2C/RG 规模口径混加。
5. 收购/更名/剥离状态过时。
6. 产品存在偷换成模型有效。
7. 时间泄漏。
8. 排序/分页导致重复或缺失。
9. Join coverage 崩溃。
10. currency/timezone/DST 错位。
11. late event 破坏封注判断。
12. 图谱误合并。
13. 未标注误当负样本。
14. 处置后 selection/censoring bias。
15. 合成数据缺稀有结构。
16. bot 低额流量污染基线。
17. AUC 高但 calibration 差。
18. class imbalance 下 ROC-AUC 虚高。
19. Transformer 记住身份而非行为。
20. GNN 放大共享 IP 假阳性。
21. PU prior π 敏感。
22. drift 不触发 fallback。
23. SHAP 代替证据链。
24. targeting bias 被当 uplift。
25. 模型 outage 阻塞核心交易。
26. A/V 延迟引发操纵争议。
27. AI Dealer hallucination 与规则冲突。
28. KYC/支付供应商单点失败。
29. 自动 freeze/limit 无救济。
30. RG 泄漏到营销。
31. SDK/依赖供应链攻击。
32. 未授权测试竞品/第三方系统。

---

# 11. Critic v3

1. 70 家是来源完整性名册，不是“70 家都验证”。
2. AI 能力必须逐产品证明，不能集团级外推。
3. “Smartico 是唯一 RL 落地”表述过强，v3 降为公开 contextual-decisioning 候选之一。
4. AI Dealer 赛道在 2026 快速变化，旧“两家”判断已过时。
5. 供应商 ROI/uplift 不是独立因果证据。
6. 21 CFR Part 11 / DO-178C / SR 26-2 不得偷换成博彩法规。
7. 物理数据二极管不是所有 RG 隔离的唯一实现。
8. PTP/GNSS 不是所有部署的强制硬件；强制的是 clock-quality SLO。
9. Canary/honeypot 不是绝对“零假阳性”。
10. OpenBLAS 的巨大加速是特定机器/工作负载实测，不是普遍承诺。
11. StarRocks/ClickHouse 是否进入热路径必须 load test；当前禁令下不实测。
12. TEWA/MHT 仅保留为数学类比，生产术语改为 capacity-constrained allocation / multi-hypothesis resolution。

---

# 12. KillCritic v3 — 20 个 NO-GO

任一成立，不得上线：

1. 影响 RNG/牌局/派彩结果。
2. RG 风险用于促销/VIP/催存。
3. RL reward 含 GGR/NGR/亏损/投注额/时长。
4. 黑箱永久封号。
5. 黑箱提款冻结且无人工救济。
6. 无 appeal。
7. 无 rollback/override 记录。
8. 无 point-in-time 证据。
9. 无 model/rule version。
10. 无 feature snapshot hash。
11. 无 OOT validation。
12. 只报 AUC。
13. 无 denominator 的供应商案例写成 SLA。
14. P2/P3 写成官方已部署。
15. 跨辖区直接复制政策。
16. RG/AML/Fraud 三管线无边界。
17. 未批准生产数据送外部 AI。
18. 未授权测试竞品/第三方。
19. 模型故障无 deterministic fallback。
20. 核心账务/牌局不能 replay/reconcile。

---

# 13. Blindspot v3

1. Label governance。
2. Economic contract completeness。
3. Intervention bias。
4. Censoring。
5. 多账户自然人身份不确定性。
6. Agent/payment/entity 多层关系。
7. 荷官失误 vs 故意舞弊。
8. AI Dealer 的具体牌照/认证路径。
9. 供应商跨客户训练。
10. 供应商退出可移植性。
11. 云/KYC/支付单点故障。
12. Clock-quality 与 late-event budget。
13. Video/Game/Wallet 的 round_id 一致性。
14. Bonus 与 RG 用途冲突。
15. 体育 official-data rights 依赖。
16. 彩票 draw integrity。
17. 模型静默漂移。
18. 人工 reviewer 真实产能不足。

---

# 14. Cheatsheet

| 问题 | 默认答案 |
|---|---|
| 第一优先 | Event truth + label truth + outcome truth |
| 最先建表 | canonical_event_ledger / economic_contract_registry / registry_risk_topology / case_outcome_ledger |
| 第一模型 | GLM/scorecard + GBDT |
| 时间验证 | rolling/expanding walk-forward + purge/embargo |
| 类不平衡 | PR-AUC + Precision@capacity + Recall@FP-budget |
| 概率质量 | Brier + ECE + reliability |
| 图谱顺序 | probabilistic entity resolution + peer-group → graph ML |
| Transformer | 只有 OOT 稳定增量才上 |
| RL | OPE + causal baseline + safe actions + approval 后 |
| AI Dealer | Outcome/Perception/Render/Dialogue 分域 |
| RG | hard veto + purpose-bound access |
| 高影响动作 | human review + appeal + rollback + immutable audit |
| 红队范围 | 自家/书面授权测试线 |
| 合成数据 | 可压测，不可证明检测召回 |
| 当前生产连接 | 禁止 |
| 护城河 | 可信数据 + 可审计决策 + 可证明效果 + 高可靠运营 |

---

# 15. Blueprint — 十域

1. Game Integrity Domain
2. Live Media Domain
3. Bet & Wallet Domain
4. Player Identity Domain
5. Agent Network Domain
6. Fraud/Collusion Domain
7. AML Domain
8. Responsible Gambling Domain
9. Decision & Case Domain
10. Evidence & Governance Domain

四本不可替代 Ledger：
- `canonical_event_ledger`
- `wallet_accounting_ledger`
- `case_outcome_ledger`
- `model_decision_ledger`

---

# 16. 跨行业迁移 v3

| 来源 | 迁移项 | 优势 | 不照搬之处 | WM 落点 |
|---|---|---|---|---|
| HFT/量化 | time-aware validation、tail latency、meta-labeling | 时序纪律极强 | 纳秒/FPGA 多数过度；alpha 不能变玩家剥削 | as-of、p99.9、case meta-label |
| 银行 | SR 26-2 式 MRM、AML、entity resolution | 模型治理成熟 | 银行拒绝阈值不可照搬 | inventory、challenger、vendor DD |
| 电商 | feature store、CUPED、推荐 | 实验和个性化强 | retention 与 RG 可能冲突 | 非脆弱人群服务推荐 |
| 资安 | Sigma/MITRE、UEBA、zero trust | Detection engineering 强 | 默认“敌人”语义会误伤客户 | rule-as-code、peer groups |
| 反诈 | probabilistic linkage、graph | 团伙识别强 | 关联不等于身份事实 | entity resolution + human review |
| 科研 | preregistration、negative controls、E-value | 抗 p-hacking | 速度较慢 | 模型/干预验收 |
| 制药 | ALCOA+、IQ/OQ/PQ | 数据完整性强 | 非博彩法规、全套过慢 | 高影响流程分级借鉴 |
| 宇航 | FDIR、replay、worst-case | 高可靠/自愈 | 成本和认证过度 | graceful degradation |
| 军事运筹 | assignment/MHT 数学 | 有限资源优化 | 语义不适合客户运营 | case allocation |
| 供应链 | SBOM/SLSA/signing | 依赖可追溯 | CI/CD 成本 | model/package provenance |

---

# 17. 采购尽调 40 问

1. Rule/ML/DL/bandit/RL？
2. production version？
3. training window？
4. label 定义？
5. prevalence？
6. point-in-time？
7. calibration？
8. OOT/walk-forward？
9. drift？
10. OOD？
11. FP cost？
12. uncertainty？
13. challenger？
14. model card？
15. datasheet？
16. 自动动作？
17. 强制人工动作？
18. override 记录？
19. appeal？
20. rollback？
21. reason code？
22. raw evidence 可导出？
23. case history 可导出？
24. data residency？
25. subprocessors？
26. cross-client training？
27. PII retention？
28. encryption/HSM？
29. RBAC/ABAC？
30. breach notification？
31. SBOM？
32. vulnerability SLA？
33. p95/p99/p99.9？
34. peak throughput？
35. RTO/RPO？
36. feature/model fallback？
37. replay/reconciliation？
38. backpressure？
39. game result 与 AI 是否隔离？
40. RG→marketing 是否可技术证明为禁止？

---

# 18. ActionPlan v3

## Phase 0 — 现在
- 冻结来源指纹；
- `entity_product_jurisdiction_registry`；
- `economic_contract_registry`；
- risk taxonomy；
- model inventory；
- M/SC/X/C 台账；
- `targets`/Snakemake 离线 DAG；
- SBOM；
- DQ contracts；
- 15 风险表映射为 topology views。

**Gate**：每个数字能回答 who/when/denominator/version/jurisdiction/source。

## Phase 1 — 0–90 天：Label & Baseline
PU learning、weak supervision、active learning、GLM/GBDT、calibration、entity resolution、peer-group、outcome ledger、negative controls。

## Phase 2 — 授权测试线：Shadow Real-time
event bus、clock-quality SLO、point-in-time features、shadow scoring、case management、SLO/backpressure、replay、synthetic load。

## Phase 3 — 3–9 个月：Baccarat Risk Intelligence
Dealer/Table/Player/Agent/Payment/Bonus/RG；graph/temporal risk；HMM/IMM；side-bet exposure stress；bot/device；causal evaluation。

## Phase 4 — 6–12 个月：Perception / AI Dealer Pilot
Winfinity-style CV challenger；双读；AI Virtual Host/Dealer 测试线；Outcome 与 Render/Dialogue 分域；认证/监管尽调。

## Phase 5 — 12–24 个月：Constrained Decision Intelligence
uplift/CATE；contextual bandit OPE；safe actions；小流量；独立验证；model risk committee；retirement/reapproval。

**禁止直接跳 autonomous RL。**

---

# 19. 最终战略

1. Truth before AI。
2. Labels before Deep Learning。
3. Calibration before ranking glory。
4. Point-in-Time before backtest performance。
5. Case & Appeal before automation。
6. RG Firewall before personalization。
7. Replay before real-time。
8. Challenger before Transformer。
9. OPE before RL。
10. Evidence before marketing claims。

> **世界级不是让 AI 更会“经营玩家”，而是让平台能够证明：每一次牌局、资金变化、风险判断、人工处置和模型升级，为什么发生、依据什么、是否正确、能否回放、能否申诉，以及是否真正产生止损/增效/合规的增量价值。**

---

# 20. 公开核验来源（截至 2026-09-28）

- Evolution Annual Report 2025  
  https://www.evolution.com/wp-content/uploads/2026/04/Annual_Report_English_2026_04_01.pdf
- Playtech Annual Report 2025  
  https://ar25.playtech.com/
- Playtech H1 2026 / AI-powered Live Virtual Host  
  https://www.investegate.info/announcement/rns/playtech--ptec/2026-half-year-results/9764419
- EveryMatrix Bonus Guardian  
  https://everymatrix.com/news/everymatrix-launches-bonus-guardian-to-stamp-out-bonus-abuse-with-ai-precision/
- EveryMatrix × Future Anthem  
  https://everymatrix.com/news/future-anthem-expands-everymatrix-content-recommendations/
- SOFTSWISS Anti-Fraud 2025  
  https://www.softswiss.com/news/softswiss-helps-operators-save-15m-in-2025/
- Optimove announcement to acquire Smartico  
  https://www.globenewswire.com/news-release/2026/04/06/3268555/0/en/optimove-to-acquire-smartico.html
- Visa completes Featurespace acquisition  
  https://investor.visa.com/news/news-details/2024/Visa-Completes-Acquisition-of-Featurespace/default.aspx
- Mindway AI  
  https://mindway.ai/news_and_knowledge/rasmus-kjaergaard-in-an-interview-neuroscience-ai-and-player-protection/
- Sentient Studios  
  https://www.sentientstudios.ai/
- QTech × Sentient Gaming Group  
  https://qtechgames.com/qtech-games-adds-deeper-ai-realism-to-its-live-casino-suite-via-sentient-gaming-group/
- BetConstruct KISS AI evidence  
  https://clientzone.betconstruct.com/t/35ypgpb/kiss-ai-live-casino-tournament
- Winfinity presentation  
  https://winfinity.live/storage/presentation/PRESENTATION.pdf
- EU AI Act  
  https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
- UKGC LCCP 3.4.3  
  https://www.gamblingcommission.gov.uk/licensees-and-businesses/lccp/condition/3-4-3-remote-customer-interaction
- Federal Reserve SR 26-2  
  https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm
- Genius Sports 2025 20-F  
  https://www.sec.gov/Archives/edgar/data/1834489/000119312526110749/geni-20251231.htm
- Sportradar 2025 20-F  
  https://www.sec.gov/Archives/edgar/data/1836470/000110465926035485/srad-20251231x20f.htm
- Kambi 2025 Annual Report  
  https://www.kambi.com/press_release/kambi-group-plc-publishes-2025-annual-report-and-accounts/
- Brightstar Lottery 2025 20-F  
  https://www.sec.gov/Archives/edgar/data/1619762/000162828026011083/igt-20251231.htm
- FDJ UNITED corporate transition  
  https://www.fdjunited.com/presse/fdj-becomes-a-european-group-and-changes-its-name-to-fdj-united/

# 21. 深地科学 × 宇航 × 量子信息 × 时空边界增量（v3.1.0 · 2026-09-29）

> **版本关系**：本章为 v3.0.0 的严格增量层；原 v3.0.0 正文全部保留。与旧说冲突时，以本章的更正编号 C-17～C-32 为当前口径；旧说保留为血统记录，不静默删除。
>
> **证据纪律扩展**：现实深地设施、已发表实验与官方工程文件继续使用 P0～P4；“尚无观测证据但物理理论允许”的内容另标 `T1 THEORETICAL`；“仅科幻设定/无可检验证据”标 `S0 SPECULATIVE`。`T1/S0` **不得**升级为生产技术、采购能力、工程 SLA 或公司能力事实。

## 21.1 语义澄清：稷下学宫与“地下世界”分轨

1. **历史稷下学宫只有战国齐国临淄这一历史对象。** 2022 年山东考古工作认定淄博市临淄区齐都镇小徐村西、齐故城小城西门外建筑基址群为稷下学宫遗址范围。本项目以后不再寻找所谓“云南第二稷下学宫”。
2. 本轮所谓“地下世界 / 地下科学研究院”是现代**深地科学设施（Deep Underground Science Facilities）**、地下空间工程与行星地下栖居研究，不与历史稷下学宫混称。
3. “地下与外太空连接”必须拆为五种不同技术：
   - **观测连接**：地下探测器观测来自太阳、超新星、宇宙线、引力波等宇宙信号；
   - **数据连接**：地下实验室与地面/卫星通过光纤、互联网、时间同步和科研网络交换数据；
   - **训练连接**：以洞穴/矿井作为月球、火星、深空任务类比环境；
   - **量子信息连接**：量子态/量子信息可在地面—卫星链路间传送；
   - **宏观物质连接**：人、飞行器或物体“瞬间转移”——截至本版**无已验证工程技术**。

## 21.2 Current-State Correction Ledger 增量（C-17～C-32）

| ID | 待校正说法 | v3.1.0 当前口径 |
|---|---|---|
| **C-17** | “战斗机 OS 比 Linux 高级” | 类别错误。应比较硬实时、确定性、时间/空间隔离、TCB、WCET、认证与失效模式；不是一般意义的“高低”。 |
| **C-18** | RedHawk Linux = 某先进战机已证实核心 OS | RedHawk 是实时 Linux 家族；具体战机是否采用必须逐平台、逐子系统有一手证据，未知不得补。 |
| **C-19** | 飞机/卫星/军舰只有一个 OS | 现代复杂平台通常为 RTOS、Linux/Unix、分离内核/Hypervisor、FPGA/裸机等混合系统之系统。 |
| **C-20** | NASA cFS 是操作系统 | **错误**。cFS 是飞行软件框架；OSAL 抽象 Linux/RTEMS/VxWorks/QNX 等底层 OS。 |
| **C-21** | 前沿国防/宇航技术只能“国家全自研”或“全部商业采购” | 现实是政府/任务方掌握任务、数据、认证与安全边界，科研机构做核心科学，产业提供商业与专用技术的混合生态。 |
| **C-22** | 云南另有历史稷下学宫 | 当前历史/考古正本只认齐国临淄稷下学宫；现代同名机构必须标 `MODERN_NAMING`。 |
| **C-23** | 已知外星集团/外星科研院拥有前沿科技 | **无可信观测证据**。NASA 当前公开口径亦未发现可信外星生命证据，UAP 无外星技术证据。 |
| **C-24** | 高达式人工磁浮岛/万能胶囊已有现实等价物 | 不成立。现实只能拆成可展开结构、自组装、原位制造、人工重力、磁悬浮机构等子能力。 |
| **C-25** | “地下科学研究院”主要属于秘密/传说世界 | 不成立。全球公开存在成熟深地科学网络，包括 CJPL、SNOLAB、SURF、LNGS、Kamioka/KAGRA、Boulby 等。 |
| **C-26** | 地下设施已能把人/物体直接传送到太空 | **无证据**。当前可证实的是观测、科研网络、类比训练、机器人/行星地下研究和量子信息连接。 |
| **C-27** | 量子传态 = 物质瞬移 | **错误**。量子传态传送量子态/量子信息，并需要经典通信；不传送物质，也不允许超光速信息。 |
| **C-28** | 地面—卫星“传态”只是科幻 | **错误**。2017 墨子号完成独立单光子量子态地面→低轨卫星传态，最远约 1,400 km；但仍不是宏观物质传送。 |
| **C-29** | “穿越时空”全部纯科幻 | 需拆分：相对论**时间膨胀已被实验反复验证**，可理解为不同世界线的“向未来时间差”；可控返回过去的时间机器无工程证据。 |
| **C-30** | 量子电脑已制造真实虫洞 | **错误**。Caltech 团队明确说明其量子处理器实验没有制造现实空间中的时空裂隙或真实虫洞，只实现与某类可穿越虫洞动力学数学等价的量子过程。 |
| **C-31** | 月球地下洞穴 = 人工地下基地 | 2024 Nature Astronomy 给出 Mare Tranquillitatis Pit 通向数十米地下洞道的雷达证据；这是**自然地质洞道证据**，不是外星/人工基地证据。 |
| **C-32** | “理论可写出方程”即可进入技术路线图 | 禁止。必须分开 `数学存在 → 物理允许 → 实验观测 → 原理样机 → 工程示范 → 规模化运行` 六层成熟度。 |

## 21.3 深地科学前沿地图（现实层）

| 设施 | 地下尺度/环境 | 主要科学 | 与宇航/宇宙的真实连接 | 证据 |
|---|---|---|---|---|
| **中国锦屏地下实验室（CJPL）/锦屏深地科学中心** | 四川锦屏山，约 2400 m 岩石覆盖；极低宇宙线本底 | 暗物质、中微子、核天体物理、深地岩体/医学；低本底环境亦用于量子相关研究 | 在地下屏蔽宇宙线，反过来研究来自宇宙的稀有粒子与宇宙线对量子器件的影响 | P0/P1 |
| **SNOLAB（加拿大）** | 约 2 km 地下；约 5000 m² 洁净空间 | 中微子、暗物质、量子技术、生命科学、核安全 | 深地低辐射环境直接服务宇宙基本粒子与量子器件研究 | P1 |
| **SURF（美国）** | 4850 ft（约 1.48 km）层位 | DUNE、中微子、暗物质、核天体物理、地下生命、地热 | DUNE 以地下远端探测器研究中微子；地下生命研究也关联行星宜居性 | P1 |
| **LNGS Gran Sasso（意大利）** | 平均约 1400 m 岩石覆盖；约 180,000 m³ | 中微子、暗物质、核天体物理 | 宇宙线通量约降 10^6，构成宇宙稀有事件观测窗口 | P1 |
| **Kamioka / Super-Kamiokande（日本）** | Super-K 约 1000 m 地下 | 中微子、质子衰变 | 直接观测太阳、超新星等宇宙来源中微子 | P1 |
| **KAGRA（日本）** | 约 200 m 地下；两条 3 km 干涉臂 | 引力波 | 地下低地震噪声环境用于“听”遥远黑洞/中子星并合 | P1 |
| **Boulby Underground Laboratory（英国）** | 约 1.1 km 地下 | 暗物质、低本底物理、量子技术、天体生物学、行星探索、地下农业 | 矿井地质用于火星/月球类比、极端环境机器人及 off-planet habitation 研究 | P1 |

> **核心洞见**：现实中最接近“地下研究院连接宇宙”的东西，并不是秘密传送门，而是**把地表噪声隔离掉，让地下成为观察宇宙、验证量子器件、训练航天员、测试行星机器人与研究地下栖居的特殊实验环境**。

## 21.4 “地下 ↔ 外太空”的六级连接成熟度

| Level | 连接形式 | 2026-09 状态 | 例子 |
|---|---|---|---|
| **D0 已运行** | 地下实验室 ↔ 地面科研网络 | PROVEN | 全球地下实验数据远程传输、控制、归档 |
| **D1 已运行** | 地下探测器 ↔ 宇宙信号 | PROVEN | Super-K、KAGRA、CJPL、LNGS |
| **D2 已运行** | 地下类比环境 ↔ 航天训练/行星技术 | PROVEN | ESA CAVES；Boulby 行星探索/机器人 |
| **D3 已实验** | 地面 ↔ 卫星量子信息 | PROVEN-EXPERIMENT | 墨子号 1,400 km 量子态传态 |
| **D4 工程研究** | 月球/火星地下洞穴 ↔ 栖居/机器人 | OBSERVED + R&D | 月海静海坑地下洞道雷达证据；洞穴探测任务概念 |
| **D5 无证据** | 地下基地 ↔ 太空的人/宏观物体瞬移 | SPECULATIVE | 无已知装置、无工程示范 |
| **D6 理论/科幻** | 可控虫洞、返回过去、宏观时空门 | THEORETICAL / SPECULATIVE | 方程与量子模拟不等于现实虫洞 |

## 21.5 量子传态、瞬间转移与穿越时空：严密分界

### A. 量子传态（Quantum Teleportation）——已实验验证

协议本质：

```text
预共享纠缠 + 本地联合测量 + 经典通信
→ 远端重构未知量子态
```

因此：
- 被传的是**量子态信息**，不是原来的粒子/人/物体；
- 原状态按量子力学规则被破坏，不能复制；
- 需要经典比特，所以**不能借此超光速通信**；
- 地面—卫星远距离量子传态已被实验证实，是全球量子网络的重要路线。

### B. “瞬间移动人/物体”——当前不存在

宏观人体若要按科幻方式“扫描—发送—重建”，不仅面临不可思议的数据量、量子态不可克隆、测量扰动、材料重构和身份连续性问题，而且目前没有任何可工作的物理装置或工程原理验证。

### C. 时间旅行——必须拆成两个问题

1. **相对论时间膨胀：PROVEN。** 不同速度/不同引力势的时钟积累不同固有时；NIST/JILA 已在毫米高度差上测得引力时间膨胀。
2. **返回过去：UNKNOWN / 无工程证据。** 广义相对论某些解含闭合类时曲线/虫洞数学结构，但从“数学解存在”到“自然存在、可稳定、可穿越、可控制”之间仍有巨大且未跨越的物理鸿沟。

### D. “量子虫洞实验”——不得新闻标题化

2022 年 Sycamore 量子处理器工作研究的是与可穿越虫洞理论相联系的量子动力学。研究团队明确说明：
- 没有在现实空间创造时空裂隙；
- 没有产生 3+1 维真实虫洞；
- 观察到的过程亦可描述为一种量子传态。

故本项目登记为 `T1 THEORY-ANALOGUE`, **不得写成“人类已制造虫洞”**。

## 21.6 月球/行星“地下世界”：现实最值得追踪的路线

2024 年同行评议研究以 LRO Mini-RF 雷达资料给出 Mare Tranquillitatis Pit 下方存在**可进入的地下洞道、尺度达数十米**的证据。其工程意义是：
- 地下天然屏蔽温差、辐射和微陨石；
- 可作为未来机器人侦察和潜在月球基地位置；
- 研究对象是**自然熔岩管/洞道**，不是人工建筑。

因此“地下世界 × 宇航”的现实研发主轴应是：

```text
地球深地实验室
→ 洞穴/矿井类比训练
→ 自主地下机器人
→ 月/火洞穴遥感
→ 机器人下放与建图
→ 原位资源/生命支持
→ 地下/熔岩管栖居
```

而不是先假设存在传送门或外星地下基地。

## 21.7 台湾、英国与 Renaissance Technologies：前沿组织模式增量

### 台湾
公开资料显示其国防 AI 路线明确采用 GPU/NPU/FPGA 边缘计算、异构多源资料融合、HPC 与人机协同，并强调最终任务控制责任保留给人；2026 年国防创新单位亦公开承担国内外成熟商业技术的评估与导入。这里可迁移的是**商用前沿技术快速吸收 + 人在回路 + 数据分级 + 任务安全边界**，不是军事用途本身。

### 英国
Dstl 是英国国防部体系内科研机构，人员主要为公务员，主体是科学家与工程师，同时制度化与产业、大学、政府和盟国合作。其模式再次否定“公共科研机构必须全自研”的二分法。

### Renaissance Technologies
当前公开招聘显示其生产基础设施大量使用 Linux、Slurm、PostgreSQL 与内部/本地 LLM 部署等成熟组件。应迁移的是**研究—生产分离、HPC、冗余、可重复性、运维与安全纪律**；不要把顶尖量化误解为“所有底层都必须秘密自研”。

## 21.8 外星文明与“地下世界”证据闸门

NASA 当前公开口径：
- 尚无可信的地外生命证据；
- 没有数据证明 UAP 是外星技术；
- 科学界可研究 technosignatures（窄带无线电、激光、人工大气化学物、巨型工程如 Dyson sphere 等），但这些是**搜索目标**，不是发现。

因此新增：

```text
speculative_horizon_registry
- hypothesis_id
- claim
- domain
- mathematical_status
- physical_status
- observational_status
- experimental_status
- engineering_status
- evidence_grade
- falsifiable_test
- production_eligible = FALSE
```

## 21.9 RedTeam v3.1 — 深地/量子/时空专项

1. 把真实地下实验室误写成“秘密地下文明”。
2. 把自然洞穴误写成人工/外星基地。
3. 把量子态传态误写成物质瞬移。
4. 把相关性或理论等价误写成实体虫洞。
5. 把时间膨胀误写成“可回到过去”。
6. 用“机密所以无法证明”反过来当作存在证明。
7. 把 UFO/UAP 的“未识别”偷换成“外星”。
8. 把科研机构宣传的未来目标写成当前部署。
9. 把类比训练（cave analogue）写成真实月火任务能力。
10. 把“地下低宇宙线”错误理解为“隔绝一切宇宙信息”。

## 21.10 Critic v3.1

- 地下科研设施的价值恰恰来自**控制背景噪声**，不是“越深技术越高级”；不同实验最优深度不同。
- 量子传态距离纪录对“人类传送”几乎没有直接工程外推价值。
- 月球洞穴即便确认存在，也还需解决进入、通信、粉尘、热控、辐射、能源、生命支持与救援。
- 深地设施、量子网络、空间基地是三个相邻但独立的工程体系，不能因“都很前沿”而自动拼成一条技术链。
- 未公开国防/航天系统只能写 `UNKNOWN`，不能以“必然更先进”代替证据。

## 21.11 KillCritic v3.1 — 新增 NO-GO

任一出现即阻断对外发布：
- “量子传态已可传送人/物体”；
- “人类已制造真实虫洞”；
- “已有技术能返回过去”；
- “存在已证实外星地下基地/科研院”；
- “UAP = 外星飞船”；
- “月球洞穴 = 人工基地”；
- “稷下学宫在云南另有历史本体”；
- 将 `T1/S0` 内容写入采购能力、生产 SLA 或商业承诺。

## 21.12 Blindspot v3.1

新增必须长期追踪：
- 极低本底辐射对量子芯片错误率、材料与生物的真实效应；
- 地下通信定位（GNSS 不可用）、时钟同步与机器人自治；
- 地下设施灾害、通风、涌水、火灾与逃生；
- 月/火地下空间的通信中继与自主建图；
- 量子网络的纠缠分发、量子中继器、存储器和经典控制平面；
- 理论时空模型中的能量条件、稳定性、量子反作用与因果性保护；
- “未知”类研究的可证伪实验设计，防止科研叙事滑向不可证伪。

## 21.13 Cheatsheet v3.1

| 问题 | 当前正本 |
|---|---|
| 历史稷下学宫有几个？ | 历史本体按临淄一处处理 |
| 地下有没有真正科学研究院？ | 有，而且是成熟国际科学网络 |
| 地下能研究宇宙吗？ | 能；中微子、暗物质、引力波、核天体物理等 |
| 地下能训练宇航员吗？ | 能；ESA CAVES 为公开实例 |
| 地下能测试月/火技术吗？ | 能；Boulby 等有行星探索/机器人研究 |
| 地下能“连卫星”吗？ | 数据/通信当然可；量子态地面—卫星传态也已实验 |
| 能瞬移人到太空吗？ | 不能；无已验证技术 |
| 能穿越到未来吗？ | 时间膨胀使不同世界线时间积累不同，物理上已证实 |
| 能回到过去吗？ | 无工程证据；理论问题未转化为现实技术 |
| 虫洞造出来了吗？ | 没有 |
| 外星高科技被证实了吗？ | 没有 |
| 科幻能不能研究？ | 能，但必须放在 `speculative_horizon_registry`，不可冒充事实 |

## 21.14 Blueprint v3.1 — Deep-Earth × Space Research Stack

```text
L0 REALITY / CLAIM INTAKE
   official facility docs | peer-reviewed papers | mission docs | hypothesis
        ↓
L1 EVIDENCE GRADE
   P0/P1/P2/P3/P4 | T1 theoretical | S0 speculative
        ↓
L2 PHYSICAL LAYER
   underground geology | low-background environment | clocks | communications
        ↓
L3 OBSERVATION
   neutrino | dark matter | gravitational wave | radiation | astrobiology
        ↓
L4 ROBOTICS / ANALOGUE
   cave mapping | autonomous rover | extreme-environment operations
        ↓
L5 SPACE LINK
   classical network | satellite data | quantum communication
        ↓
L6 PLANETARY SUBSURFACE
   lunar/Mars caves | access | mapping | habitation R&D
        ↓
L7 FRONTIER THEORY
   wormholes | CTC | technosignatures
        ↓
L8 GOVERNANCE
   falsifiability | provenance | replication | no-hype gate
```

**与 GDI-OS 的可迁移部分**仅限：证据分级、低噪声实验思想、冗余、可回放、状态估计、故障隔离、形式化验证、数据血统和假说晋级门槛。不得把宇航/国防的具体任务控制或武器逻辑迁入玩家处置。

## 21.15 ActionPlan v3.1

**Phase F0 — 证据注册**：建立 `frontier_technology_registry` 与 `speculative_horizon_registry`；所有“地下/量子/时空/外星”主张必须有 `source_date / evidence_grade / experimental_status / engineering_status`。

**Phase F1 — 深地科学对标**：固定跟踪 CJPL、SNOLAB、SURF、LNGS、Kamioka/KAGRA、Boulby；每季度更新设施、科研方向与公开技术。

**Phase F2 — 地下×宇航专题**：追踪 ESA CAVES、Boulby planetary exploration、月球/火星洞穴遥感与自主机器人；只收公开科研与民用航天资料。

**Phase F3 — 量子网络**：以量子态传态、纠缠分发、量子中继器、卫星量子链路为对象；任何“物质瞬移”单独保持 `S0`。

**Phase F4 — 时空物理**：将时间膨胀列 `P0/P1 PROVEN`；虫洞/CTC 按理论研究记录，不设工程交付期限，不写商业能力。

**Gate**：任何结论必须回答——`它是数学？物理理论？实验观测？原型？工程部署？还是纯假说？`

## 21.16 本章公开来源（核验日期 2026-09-29）

- 山东稷下学宫遗址范围认定：https://www.sdxc.gov.cn/sy/spzb/202202/t20220226_9876487.htm
- Jinping Neutrino Experiment：https://jinping.hep.tsinghua.edu.cn/
- NSFC Jinping programme：https://www.nsfc.gov.cn/english/site_1/international/D6/2025/07-04/433.html
- 锦屏深地科学中心（新华社）：https://www.xinhuanet.com/20251223/7ebd5c02a80e4de090fce4f62cbaa312/c.html
- SNOLAB：https://www.snolab.ca/about/about-snolab/
- SURF：https://sanfordlab.org/about-the-facility
- LNGS：https://www.lngs.infn.it/en/lngs-overview
- ICRR Kamioka/KAGRA：https://www.icrr.u-tokyo.ac.jp/en/facility/
- Boulby Underground Laboratory：https://www.boulby.stfc.ac.uk/about/
- ESA CAVES：https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/CAVES_and_Pangaea/What_is_CAVES
- Nature Astronomy lunar cave：https://www.nature.com/articles/s41550-024-02302-y
- Nature ground-to-satellite quantum teleportation：https://www.nature.com/articles/nature23675
- IBM Quantum teleportation：https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation
- NIST gravitational time dilation：https://www.nist.gov/news-events/news/2022/02/jila-atomic-clocks-measure-einsteins-general-relativity-millimeter-scale
- Caltech wormhole experiment clarification：https://www.caltech.edu/about/news/physicists-observe-wormhole-dynamics-using-a-quantum-computer
- NASA UAP FAQ：https://science.nasa.gov/uap/faqs/
- NASA technosignatures：https://science.nasa.gov/universe/search-for-life/searching-for-signs-of-intelligent-life-technosignatures/
- Taiwan MND AI applications：https://www.mnd.gov.tw/en/dioen/AI%20ApplicationsEn.html
- UK Dstl framework：https://www.gov.uk/government/publications/defence-science-and-technology-laboratory-framework-document/defence-science-and-technology-laboratory-dstl-framework-document-july-2021
- Renaissance Technologies systems engineering：https://www.rentec.com/Careers.action?jobs=true&selectedPosition=systemsEngineerEs

---

<!-- SOURCE_ANNEX_20261007_BEGIN -->
## 2026-10-07 來源增補與歷史差異

本章保留 509 個先前未覆蓋段落。段落可能反映不同時期或相互矛盾的觀點；以來源台帳與審校說明解讀。簽名網址的查詢憑證只在原始本地來源保存，閱讀副本作遮蔽。

### 來源：Reference/Whitepaper-Perfect-Baccarat-AI-Quant-Governance-V3-0-0.md

[原始來源](<Whitepaper-Perfect-Baccarat-AI-Quant-Governance-V3-0-0.md>)；SHA256：`7032791b121fff57cbca9a05c0b15645eb64a78ff985f3f6be77e0cc48af5e81`。下列為未覆蓋段落；歷史主張未經收錄自動驗證。

::: {.callout-note collapse="true"}
來源第 739 行；段落 7140191e8091fad8；UNKNOWN_INHERITED。

```text
- Evolution Annual Report 2025  
  https://www.evolution.com/wp-content/uploads/2026/04/Annual_Report_English_2026_04_01.pdf
- Playtech Annual Report 2025  
  https://ar25.playtech.com/
- Playtech H1 2026 / AI-powered Live Virtual Host  
  https://www.investegate.info/announcement/rns/playtech--ptec/2026-half-year-results/9764419
- EveryMatrix Bonus Guardian  
  https://everymatrix.com/news/everymatrix-launches-bonus-guardian-to-stamp-out-bonus-abuse-with-ai-precision/
- EveryMatrix × Future Anthem  
  https://everymatrix.com/news/future-anthem-expands-everymatrix-content-recommendations/
- SOFTSWISS Anti-Fraud 2025  
  https://www.softswiss.com/news/softswiss-helps-operators-save-15m-in-2025/
- Optimove announcement to acquire Smartico  
  https://www.globenewswire.com/news-release/2026/04/06/3268555/0/en/optimove-to-acquire-smartico.html
- Visa completes Featurespace acquisition  
  https://investor.visa.com/news/news-details/2024/Visa-Completes-Acquisition-of-Featurespace/default.aspx
- Mindway AI  
  https://mindway.ai/news_and_knowledge/rasmus-kjaergaard-in-an-interview-neuroscience-ai-and-player-protection/
- Sentient Studios  
  https://www.sentientstudios.ai/
- QTech × Sentient Gaming Group  
  https://qtechgames.com/qtech-games-adds-deeper-ai-realism-to-its-live-casino-suite-via-sentient-gaming-group/
- BetConstruct KISS AI evidence  
  https://clientzone.betconstruct.com/t/35ypgpb/kiss-ai-live-casino-tournament
- Winfinity presentation  
  https://winfinity.live/storage/presentation/PRESENTATION.pdf
- EU AI Act  
  https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
- UKGC LCCP 3.4.3  
  https://www.gamblingcommission.gov.uk/licensees-and-businesses/lccp/condition/3-4-3-remote-customer-interaction
- Federal Reserve SR 26-2  
  https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm
- Genius Sports 2025 20-F  
  https://www.sec.gov/Archives/edgar/data/1834489/000119312526110749/geni-20251231.htm
- Sportradar 2025 20-F  
  https://www.sec.gov/Archives/edgar/data/1836470/000110465926035485/srad-20251231x20f.htm
- Kambi 2025 Annual Report  
  https://www.kambi.com/press_release/kambi-group-plc-publishes-2025-annual-report-and-accounts/
- Brightstar Lottery 2025 20-F  
  https://www.sec.gov/Archives/edgar/data/1619762/000162828026011083/igt-20251231.htm
- FDJ UNITED corporate transition  
  https://www.fdjunited.com/presse/fdj-becomes-a-european-group-and-changes-its-name-to-fdj-united/
```
::: 

### 來源：Reference/Whitepaper-Online-Gaming-Baccarat-AI-V2-0-0.md

[原始來源](<Whitepaper-Online-Gaming-Baccarat-AI-V2-0-0.md>)；SHA256：`277da83ccd939731d33896c651f927bf234ff6a40f6d0eeeee996951066e0008`。下列為未覆蓋段落；歷史主張未經收錄自動驗證。

::: {.callout-note collapse="true"}
來源第 1 行；段落 93ca0d79ff22807f；UNKNOWN_INHERITED。

```text
# 顶级在线博彩娱乐（体育·彩票·百家乐）AI与跨行业量化科技移植白皮书 v2.0.0

```
::: 

::: {.callout-note collapse="true"}
來源第 3 行；段落 7f3d797cbb094c2c；UNKNOWN_INHERITED。

```text
> **编制**：Ryo Eng（雷欧）实验室交叉核验版 · 基于您上传的6份附件全量校对  
> **附件指纹**：电脑已升级至视窗11版 9643行 / Aerospace_Ecosystem_Report 135行 / Baccarat-Ai-Automation-Report 111行 / Inteligent_egaming_platform_ref 13156行 / perfect-baccarat-report 222行 / 顶级移植总表 892行  
> **日期**：2026-09-26 校核，2026-09-27 定版  
> **标准**：科学研究院级证据分级 + 航天级可靠性 + 金融级合规 + AI伦理可审计

```
::: 

::: {.callout-note collapse="true"}
來源第 10 行；段落 f1dce970c9969fc5；UNKNOWN_INHERITED。

```text
## 执行摘要

```
::: 

::: {.callout-note collapse="true"}
來源第 12 行；段落 4cea850cfb282191；UNKNOWN_INHERITED。

```text
经对6份附件逐行交叉核验，结论高度一致：

```
::: 

::: {.callout-note collapse="true"}
來源第 14 行；段落 cab3f5a2b7e291b4；UNKNOWN_INHERITED。

```text
1. **真人百家乐前台发牌从未被AI/RL接管**。唯一公开声称并落地的AI Dealer是2026年新势力 **Octane Studios（百家乐首发）** 和 **Sentient Studios（原BetHog，FanDuel联创Nigel Eccles，$10M A轮，AI荷官Sunny，10倍参与度）**，架构均为 **RNG引擎与渲染引擎强制分离**，监管路径为RNG产品而非Live。

```
::: 

::: {.callout-note collapse="true"}
來源第 16 行；段落 af0c11fbc90e69c2；UNKNOWN_INHERITED。

```text
2. **顶级平台的AI全部在中后台**：Evolution / Playtech / Pragmatic Play / Ezugi 的重心是 **AI-Powered Fraud Detection、Biometric Dealer Auth、Advanced AI Monitoring、GLI Certified RNG + 计算机视觉读牌（YOLOv8 60FPS）+ Flink 100ms派彩**；B2B平台层 **SOFTSWISS Anti-Fraud 2022年61,810请求节省€16M+，2023年10万+请求节省€13M**；CRM层 **Smartico唯一明确的RL落地：contextual bandits / MAB奖金优化 + RNN 7/14/30天流失预测准确率75.94%**，2026-04已被Optimove收购。

```
::: 

::: {.callout-note collapse="true"}
來源第 18 行；段落 6e92a5eaa39744db；UNKNOWN_INHERITED。

```text
3. **亚洲系12家（SA Gaming / Dream Gaming / WM / AG / AllBet / Sexy / Pretty / Venus / Big Gaming / eBet / BetGames.TV / KingMaker）在PAGCOR认证与公开渠道** 仅列桌台数量与边注，无模型卡、数据集、审计报告，其“自动”仅指无荷官机械臂发牌，非智能决策，**不得列为AI平台，属营销误植**，仅作速度与桌台密度对标。

```
::: 

::: {.callout-note collapse="true"}
來源第 20 行；段落 0fe6cee39c60241b；UNKNOWN_INHERITED。

```text
4. **RL全面控制百家乐核心结果无可验证案例**。可信路径是四层架构：实时流 + 规则引擎 + ML/图谱排序 + 人工高影响复核 + 不可变审计。

```
::: 

::: {.callout-note collapse="true"}
來源第 22 行；段落 10abdad9b6afb5aa；UNKNOWN_INHERITED。

```text
本白皮书以您项目铁律为准绳，生成可落地的体育、彩票、百家乐统一平台方案。

```
::: 

::: {.callout-note collapse="true"}
來源第 26 行；段落 e3f15f3ac2e56b09；UNKNOWN_INHERITED。

```text
## §1 证据分级与三条不可逾越铁律

```
::: 

::: {.callout-note collapse="true"}
來源第 28 行；段落 c57e3cee9d984a0f；UNKNOWN_INHERITED。

```text
### 1.1 证据分级（每条主张必带）

```
::: 

::: {.callout-note collapse="true"}
來源第 30 行；段落 024ed1c6793da5a7；UNKNOWN_INHERITED。

```text
| 等级 | 定义 | 用法 |
|---|---|---|
| OBSERVED | 一手来源：官网、年报、监管文件、融资公告 | 可直接引用 |
| INFERRED | 第三方转述、行业媒体、供应商博客 | 须标注转述链 |
| UNKNOWN | 检索后无披露 | 显式留白，不得填充 |
| CONDITIONAL | 取决于未裁定前提 | 写明前提 |

```
::: 

::: {.callout-note collapse="true"}
來源第 37 行；段落 32a1c6c982ba4643；UNKNOWN_INHERITED。

```text
### 1.2 三条铁律

```
::: 

::: {.callout-note collapse="true"}
來源第 39 行；段落 9420bf8df89b08b4；UNKNOWN_INHERITED。

```text
1. **AI永不进入牌局结果**：不得对单一玩家调整赔率、牌靴、发牌、RNG、派彩、游戏结果。
2. **RL/bandit的reward只能是保护性指标**：风险下降、限额采纳、冷静期完成、投诉减少、人工审核质量。**禁止** GGR/NGR/入金/投注额/时长/回流/返水转化。
3. **RG数据与营销系统必须结构隔离或物理隔离**（Bell-LaPadula不上读不下写 / 数据二极管），非制度禁止。

```
::: 

::: {.callout-note collapse="true"}
來源第 43 行；段落 83891271de381714；UNKNOWN_INHERITED。

```text
### 1.3 三类价值判准

```
::: 

::: {.callout-note collapse="true"}
來源第 45 行；段落 3423b02e2dbe85ad；UNKNOWN_INHERITED。

```text
| 价值 | 合法可验证目标 | 核心KPI | 绝不可计入的收益 |
|---|---|---|---|
| 止损 | 减少经人工确认的欺诈、串通、代理套利、红利滥用、支付异常 | 确认损失避免额、Precision@人工产能、误伤率、漏报率 | 限制正常会员而减少的正常派彩 |
| 增效 | 同人力处理更多高质量案件，降低排查对账成本 | 每人日闭环案件数、结案时长、证据覆盖率 | 高风险/脆弱会员投注增加、追损延长 |
| 合规 | 更早识别风险，降低伤害与审计缺陷 | 强风险信号响应时延、人工复核率100%、申诉成功率、限额采纳率 | 将RG风险分数用于VIP/奖励/营销 |

```
::: 

::: {.callout-note collapse="true"}
來源第 53 行；段落 55ed696cbd20f6cf；UNKNOWN_INHERITED。

```text
## §2 主体全名册（70家 + 9类监管标准体系）- 一个不漏

```
::: 

::: {.callout-note collapse="true"}
來源第 55 行；段落 c4acb8818d8e5cec；UNKNOWN_INHERITED。

```text
### A. B2B真人内容与直播供应商（16家）

```
::: 

::: {.callout-note collapse="true"}
來源第 57 行；段落 f3522a8c14292b4f；UNKNOWN_INHERITED。

```text
1. **Evolution** - Speed/Lightning/First Person Baccarat。60FPS YOLO读牌+Flink 100ms派彩，AI-Powered Fraud Detection / Biometric Dealer Auth。OBSERVED地位，AI宣称INFERRED。**优势**：全球60%+市占，技术最稳，多机位4K。**劣势**：成本最高，高峰排队，创新变体RTP略低。
2. **Ezugi** - EZ Baccarat, Ultimate Auto Roulette全自动。优势：hands-per-hour最快，多语言。劣势：1080P为主，被收购后独立性下降。
3. **Playtech Live** - Prestige Baccarat, IMS自适应欺诈模型, BetBuddy AI, Featurespace ARIC, Playtech Protect。优势：负责任博彩三层模型最成熟，15-17司法管辖区验证。劣势：界面传统，创新慢。
4. **Pragmatic Play Live** - Mega Baccarat, 7个Bot按基础策略坐桌（Bet Behind Pro）, Auto-Roulette。优势：移动端最好，节奏快。劣势：AI运营证据INFERRED。
5. **SA Gaming** - 百家乐/龙虎/骰宝等，PAGCOR认证，南非WCGRB新牌照。**UNKNOWN**无一手AI披露。优势：东南亚线路优化，桌多。劣势：UI旧，无模型卡。
6. **Dream Gaming DG** - 竞咪百家乐，直播自泰国金冠赌场，Curaçao牌照。UNKNOWN。优势：咪牌仪式感。劣势：审计不透明。
7. **WM Casino / WM Perfect Group** - Live Provider+Streaming+Ecosystem三合一。UNKNOWN。优势：生态全，玩家/荷官/桌台/代理/风控五维适合XGBoost/HMM。劣势：公开技术白皮书缺失。
8. **Asia Gaming AG** - 首创Interactive Bid Baccarat，VIP包房可控节奏。UNKNOWN。优势：高限红。劣势：欧美牌照少，假台盗用多。
9. **AllBet** - 真人百家乐。UNKNOWN。优势：路单全。劣势：营销站为主。
10. **Sexy Baccarat / AE Sexy** - UNKNOWN。优势：娱乐化强。劣势：监管弱，假站最多。
11. **Pretty Gaming** - 同上。
12. **Venus Casino** - 同上。
13. **Big Gaming** - 同上。
14. **eBet** - 同上。
15. **BetGames.TV** - 同上。
16. **KingMaker** - 同上。

```
::: 

::: {.callout-note collapse="true"}
來源第 74 行；段落 dd77f74dc4bcef93；UNKNOWN_INHERITED。

```text
> **采购裁定**：#5-#16仅作去荷官速度与桌台密度对标，不纳入AI采购。

```
::: 

::: {.callout-note collapse="true"}
來源第 76 行；段落 5becbd875ebf5d41；UNKNOWN_INHERITED。

```text
### B. B2C运营商与集团（13家）

```
::: 

::: {.callout-note collapse="true"}
來源第 78 行；段落 5e84827228ce6c24；UNKNOWN_INHERITED。

```text
17. **Entain** - ARC + Protector Model, 26-30行为标记，22市场第一阶段，准确度>90%宣称，已整合Mindway。OBSERVED。优势：ESG披露最全。劣势：数字冲突未公开基准。
18. **Flutter** - RTI Real Time Intervention / Real Time Check In, 年报确认ML/AI用于基础设施，Responsible AI政策。优势：集团化复制。劣势：不可外推到每张百家乐桌。
19. **FanDuel** - 集团RTI覆盖。
20. **PokerStars** - 同上。
21. **Sportsbet** - RTI发源地。
22. **Betfair** - AI用于欺诈检测。INFERRED。
23. **Kindred Group** - PS-EDS早期检测。OBSERVED。优势：学术合作多。劣势：公开样本少。
24. **Unibet** - PS-EDS覆盖。
25. **BetMGM** - Optimove客户，量化案例。
26. **DraftKings** - ⚠反面案例，NYT调查ML识别最可能输钱客户定向免费投注，问题博彩工具被搁置。INFERRED转述。**局限**：剥削性目标函数教科书案例。
27. **Sisal** - Optimove客户，未来价值+36%/存款+23%/NGR+28%/忠诚毛收入+89%。
28. **Stardust** - MAU x3/独立存款人+37%/净收入+51%。
29. **OPAP** - ComplianceSuite.ai客户，自动化风险管理。

```
::: 

::: {.callout-note collapse="true"}
來源第 92 行；段落 4f305289da32debc；UNKNOWN_INHERITED。

```text
### C. B2B平台/PAM/CRM（6家，RL唯一公开落地处）

```
::: 

::: {.callout-note collapse="true"}
來源第 94 行；段落 bfdb5ffc517352b9；UNKNOWN_INHERITED。

```text
30. **SOFTSWISS** - Anti-Fraud实时ML+人工复核，BM3业务指标监控，DOSSIER LTV预测，可揭示卡号-账户-邮箱-设备指纹钱骡链。OBSERVED，2022省€16M+。优势：止损标杆。劣势：COO明言最终决策须留给专家。
31. **EveryMatrix** - CasinoEngine/Bonus Guardian，用已知滥用者历史训练ML，按角色配置奖金排除/提款冻结。优势：红利滥用专精。劣势：不等同串通/洗钱检测。
32. **Smartico** - **全对话唯一明确RL落地**，contextual bandits/RL工作台自适应难度/时机/奖励，MAB实时选最优奖励，RNN预测流失75.94%。优势：RL证据最硬。劣势：已被收购，独立性下降。
33. **Optimove / Opti-X** - 20+推荐模型，700+游戏，AI搜索+动态个性化，52% EGR Power50客户。
34. **GiG** - AI推荐引擎提升留存降低假阳性。INFERRED。
35. **NuxGame + iDenfy** - AI文档分析嵌入赌场软件，自动化KYC/AML。

```
::: 

::: {.callout-note collapse="true"}
來源第 101 行；段落 089466732bb68354；UNKNOWN_INHERITED。

```text
### D. AI风控/反欺诈/KYC/AML供应商（22家）

```
::: 

::: {.callout-note collapse="true"}
來源第 103 行；段落 9df92d3015d3f3c0；UNKNOWN_INHERITED。

```text
36. **Featurespace ARIC** - 剑桥创立，自适应行为分析，Betfair 2008年首用，Visa 2024年拟收购。优势：银行业验证。劣势：阈值需重标定。
37. **SEON** - 设备指纹+数字足迹。
38. **GeoComply** - 2亿+设备网络ML威胁检测。
39. **Sumsub** - KYC文档+活体+深伪检测。
40. **Onfido** - 同上。
41. **Jumio** - 同上。
42. **Veriff** - 同上。
43. **iDenfy** - 与NuxGame集成。
44. **Shufti + Cevro AI** - 与客服Agent集成。
45. **CrossClassify** - 账户盗用。
46. **Sift** - 行为/支付风险情报。
47. **Group-IB** - 含可解释AI XAI。
48. **cside** - 每会话250+浏览器信号，识别OpenAI Operator/Claude for Chrome/Playwright/Puppeteer/Selenium，注册前拦截。
49. **Flagright** - AML+RG统一案件管理。
50. **ComplyAdvantage** - 制裁/PEP筛查。
51. **NICE Actimize** - 交易监控SAR/STR。
52. **ACT Fraud Rings** - 2026新增syndicate可视化，设备/IP/行为关联。
53. **Infocredit ComplianceSuite.ai** - 2025 AML/CFT金奖白金奖。
54. **Cevro AI** - 域专用LLM，解决80-90%复杂工单，100+语言，内置信任层。
55. **InteractiveAI** - 受合规边界约束AI代理。
56. **Moveo.AI** - 与SOFTSWISS/Smartico/Zendesk集成。
57. **Quantexa** - 实体解析+图谱，银行业AML标杆跨行业引入。

```
::: 

::: {.callout-note collapse="true"}
來源第 126 行；段落 bf3fd0f3f0ceb1d9；UNKNOWN_INHERITED。

```text
### E. 责任博彩AI（6项）

```
::: 

::: {.callout-note collapse="true"}
來源第 128 行；段落 46853c5ed357b3b7；UNKNOWN_INHERITED。

```text
58. **Mindway AI GameScanner/Gamalyze** - 虚拟心理学家，神经科学游戏化自测，1470万活跃玩家监测（跨运营商汇总），≥87%专家级检出。优势：每月900万+监测。劣势：供应商自述数字。
59. **Neccton Mentor** - 问题赌博早期检测。
60. **Sportradar Bettor Sense** - 模式识别+session分析。
61. **Playtech BetBuddy** - 三层风险评级，提前数周预测，15%高风险1小时内主动设限，对照试验验证。
62. **Entain ARC** - 见上。
63. **Kindred PS-EDS** - 见上。

```
::: 

::: {.callout-note collapse="true"}
來源第 135 行；段落 3fd44abe4487ec9a；UNKNOWN_INHERITED。

```text
### F. AI荷官新势力（2家，独立成章）

```
::: 

::: {.callout-note collapse="true"}
來源第 137 行；段落 b19715dd5fd9d7d0；UNKNOWN_INHERITED。

```text
61. **Octane Studios** - AI Baccarat首发，可定制品牌化，认证RNG+provably fair，数日交付。优势：1-10000桌弹性。劣势：监管路径为RNG非Live，需教育玩家。
62. **Sentient Studios** - FanDuel联创Nigel Eccles，AI荷官Sunny实时对话+表情+肢体，10倍参与度，12语言，$10M A轮，Blackjack 2025-10已上线，百家乐/轮盘2026年底。优势：低额碎片化玩家更愿向AI提问。劣势：音频过清晰需故意脏化，否则破剧场信任。

```
::: 

::: {.callout-note collapse="true"}
來源第 140 行；段落 2ab517f16c4168c0；UNKNOWN_INHERITED。

```text
### G. 实体/混合智慧桌（2家）

```
::: 

::: {.callout-note collapse="true"}
來源第 142 行；段落 c6a0279536c15d02；UNKNOWN_INHERITED。

```text
63. **Angel Group** - AI+RFID混合+姿势辨识，已在澳门Sands China千张百家乐桌部署，超越传统RFID。优势：楼面数据品质跃升。劣势：硬件成本高。
64. **IDX Games** - AI chatbot分析桌游数据。

```
::: 

::: {.callout-note collapse="true"}
來源第 145 行；段落 84111bd4854752f5；UNKNOWN_INHERITED。

```text
### H. 玩家端第三方工具（敌方，必须反制，6项）

```
::: 

::: {.callout-note collapse="true"}
來源第 147 行；段落 1821c06ffa011023；UNKNOWN_INHERITED。

```text
65. **FPLAY** - 多平台API自动下注，支持DG/WM/AllBet/WG。
66. **Mysports.AI** - 自动读牌+剩余牌分布计算+Telegram推播高EV。
67. **Oracle Baccarat Predictor** - ML预测路单。
68. **BACC.BOT** - 深度学习。
69. **BaccaratAI** - 深度学习。
70. **Differential Labs** - 研究方，边注占亚洲赌场40-60%收入，AI辅助算牌已成优势玩家工具，亚洲年损估计5-7亿美元。

```
::: 

::: {.callout-note collapse="true"}
來源第 154 行；段落 c0d16fdf6355dc6e；UNKNOWN_INHERITED。

```text
**补充**：BetConstruct AI, Winfinity（计算机视觉读牌）, 188BET, 888.com等在附件中出现但证据等级INFERRED，已纳入上表同类对标。

```
::: 

::: {.callout-note collapse="true"}
來源第 156 行；段落 6f775be41327e104；UNKNOWN_INHERITED。

```text
### I. 9类监管与标准体系

```
::: 

::: {.callout-note collapse="true"}
來源第 158 行；段落 75df617aa1357f77；UNKNOWN_INHERITED。

```text
1. **MGA AI Gaming Charter 2026-09-18** - 马耳他博彩管理局+MDIA发布，48页，自愿原则，补充EU AI Act+GDPR，涵盖玩家保护/反欺诈/客户交互/运营决策，要求高影响AI文档/测试/人工监督/持续监控，无新增法律义务。OBSERVED。
2. **EU AI Act** - 欺诈检测/行为追踪/个性化推荐/聊天机器人均可能高风险，需技术参数/透明度/风险管理/人工监督。
3. **UKGC LCCP 3.4.3** - 强风险指标及时自动化处理，个案仍需人工审核并允许异议。
4. **GDPR** - 第22条自动化决策+第12条日志。
5. **ISO/IEC 42001** - AI管理体系。
6. **NIST AI RMF** - 风险管理框架。
7. **ALCOA+ / 21 CFR Part 11** - 数据完整性与电子签名。
8. **DO-178C** - 航天级软件可靠性，精神是最小化而非最大化功能。
9. **PAGCOR / GLI / BMM Testlabs / eCOGRA** - 实验室认证。

```
::: 

::: {.callout-note collapse="true"}
來源第 170 行；段落 dc89cd01d9e885fa；UNKNOWN_INHERITED。

```text
## §3 跨行业量化科技移植总表（13行业）

```
::: 

::: {.callout-note collapse="true"}
來源第 172 行；段落 8e9cf1879bb563f8；UNKNOWN_INHERITED。

```text
| 行业 | 标杆 | 可移植到博彩的杀手锏 | 博彩专用改造 |
|---|---|---|---|
| **航天国防** | Palantir Warp Core/Foundry/Gotham, SpaceX WARPDRIVE | **时序库** QuestDB/InfluxDB/TimescaleDB/TDengine/IoTDB每秒百万点（StarRocks不适合核心遥测）；**实体解析** Splink+Quantexa概率链接IP/设备/钱包；**供应链情报融合** Palantir模式 | 航天级ITAR白名单→博彩需过GLI；纳秒诉求是伪需求，追p99.9尾延迟 |
| **银行业** | Featurespace ARIC, Visa收购逻辑 | 自适应行为链揭示钱骡网络，动态风险评分 | 阈值必须重标定，安全行业默认封禁策略不可用于正常会员 |
| **电商** | Optimove Opti-X, Smartico MAB | 多臂老虎机奖励分配，RNN流失预测 | Reward禁止GGR，只能是限额采纳/冷静期完成 |
| **安全** | Sigma规则+MITRE ATT&CK | 规则工程标准化，250+浏览器信号cside | 社区默认高敏阈值会误封会员，需重标定 |
| **医疗** | Mindway神经科学 | 虚拟心理学家GameScanner≥87%检出 | 不得用于营销定向 |
| **制造** | SAP+Palantir Foundry | Airflow/Dagster ETL标配 | - |
| **体育博彩** | Sportradar Bettor Sense | 实时异常投注检测 | 体育1.5以下赔率不算有效投注陷阱 |
| **彩票** | 随机数审计 | Provably fair RNG+渲染分离 | 彩票需额外熵源审计 |

```
::: 

::: {.callout-note collapse="true"}
來源第 183 行；段落 7836a590795953db；UNKNOWN_INHERITED。

```text
**关键教训来自Aerospace_Ecosystem_Report**：StarRocks/Superset/DolphinScheduler/Echarts在通用商业航天地面数仓有应用，但在星载高频遥测、飞控、军事指挥核心层非主流，核心是InfluxDB/IoTDB+Kafka/Flink+Grafana+NASA cFS/COSMOS+K8s。博彩L1实时流同理，**StarRocks适合DWS聚合，不适合L0毫秒级投注流**。

```
::: 

::: {.callout-note collapse="true"}
來源第 187 行；段落 ad65b646e5bb9a38；UNKNOWN_INHERITED。

```text
## §4 RedTeam - 攻击面与失效模式（可执行演练）

```
::: 

::: {.callout-note collapse="true"}
來源第 189 行；段落 790ce650330d33fd；UNKNOWN_INHERITED。

```text
1. **信任瓦解攻击**：AI荷官音频过清晰需故意脏化加背景噪声；渲染延迟>2秒口型不同步被弹幕放大为操纵证据。演练：注入2秒音视频不同步故障，观察社群信任崩溃速度。
2. **优势玩家AI对抗**：边注40-60%收入，AI辅助算牌年损5-7亿。演练：用Mysports.AI类工具扫描边注EV，测试自家异常检测延迟。
3. **浏览器AI代理绕过**：OpenAI Operator/Claude for Chrome/Playwright/Puppeteer/Selenium。演练：cside类250+信号在注册前拦截率。
4. **奖励优化反噬**：RL在连败后发安慰奖延长痛苦游戏，降低有意识控制。演练：审计reward是否含GGR/投注额。
5. **数据投毒与BM3操纵**：机器人刷低额投注污染训练数据掩盖套利。演练：注入低额机器人流观察Precision@产能漂移。
6. **供应链攻击**：60+包（snorkel/stone-soup/kuzu等）小众包CVE响应慢。必须先过grype/trivy。
7. **标签泄漏**：随机切分导致同一玩家跨期资讯泄漏，需purge/embargo。
8. **PU Learning先验π敏感**：π估错召回整体偏移，需外部锚。

```
::: 

::: {.callout-note collapse="true"}
來源第 200 行；段落 277f144f5e6e613f；UNKNOWN_INHERITED。

```text
## §5 Critic - 证据弱点与叙事裂缝

```
::: 

::: {.callout-note collapse="true"}
來源第 202 行；段落 409a7284f51850e8；UNKNOWN_INHERITED。

```text
- Entain/Flutter AI材料集中于责任博彩，非真人百家乐分游戏公开验证，集团层不可外推到每个百家乐产品。
- Entain >90%准确度未公开基准样本/正负类定义/置信区间/漂移评估，不可当KPI。
- Mindway ≥87%是供应商宣告，只能作shortlist线索，非SLA。
- EveryMatrix Bonus Guardian聚焦红利滥用≠串通/荷官异常/洗钱。
- 亚洲供应商AI叙事真空，公开渠道无模型卡/数据集/审计报告。
- 自动化=效率忽视人工监督成本，SOFTSWISS COO明言最终决策留给专家。
- 寡头创新者困境：Evolution曾贬低AI荷官为deepfake，60%+ Live市占护城河依赖真人工作室。
- 本清单约七成技术从未在受监管博彩业公开落地，属跨行业推论INFERRED，对外不可写成业界标准做法。
- mlfinlab已转商业授权，元标签与CPCV需自实现。
- 纳秒级事件总线收益仅单机内成立，跨机网络RTT吃掉三个数量级。

```
::: 

::: {.callout-note collapse="true"}
來源第 215 行；段落 326e6ae195809965；UNKNOWN_INHERITED。

```text
## §6 KillCritic - 对批判的反驳与证伪

```
::: 

::: {.callout-note collapse="true"}
來源第 217 行；段落 ea93a000c3c2e490；UNKNOWN_INHERITED。

```text
1. **AI更人性化**：BetHog实测新玩家不敢在真人台问规则，反愿向AI提问并使用问荷官按钮，信任来源从物理牌转向品牌与可证明公平RNG。
2. **AI可用于保护**：BetBuddy已被17司法管辖区信任，三层风险评级提前数周预测，对照试验15%高风险1小时内主动设限；Mindway每月监测900万+活跃，≥87%检出；DraftKings 2026-01集成Gamalyze自测。
3. **RL非营销话术**：Smartico/Optimove收购案官宣，客户案例Stardust/BetMGM/Sisal有量化增效，产品套件含AI驱动LTV预测与A/B框架。
4. **SOFTSWISS COO自证**：AI实时分析大数据，但最终决策留给专家，否则财务损失，证明人工监督是成熟治理非否定AI。
5. **成本与规模反证**：Sentient称AI台更吸引低额碎片化玩家，10倍参与度颠覆Live仅服务VIP假设；Octane数日交付品牌化桌台，1-10000桌弹性。

```
::: 

::: {.callout-note collapse="true"}
來源第 225 行；段落 dbbd3e65c734abbe；UNKNOWN_INHERITED。

```text
## §7 Blindspot - 盲区（行业+本项目）

```
::: 

::: {.callout-note collapse="true"}
來源第 227 行；段落 8c29f7227e0f83d4；UNKNOWN_INHERITED。

```text
**行业盲区**：
- MGA Charter自愿性陷阱，2026-2027高风险义务生效前可选择性披露模型。
- EU AI Act高风险定性已落，多数百家乐平台未公开模型审计。
- 剥削性目标函数（DraftKings案例）现有法规几乎空白。
- 内部真实模型架构与RL reward设计是最不可知部分。
- SA市场双重叙事：SOFTSWISS称AI可遏制欺诈但承认无法完全防止，仅实时监测。

```
::: 

::: {.callout-note collapse="true"}
來源第 234 行；段落 f2cfda2212a3b764；UNKNOWN_INHERITED。

```text
**本项目盲区（来自电脑已升级至视窗11版附件实测）**：
| 项 | 现状 | 约束 |
|---|---|---|
| 磁盘 | 单块237GB，可用约43GB | Iceberg本地湖千万级Parquet全量落盘装不下，必须按日分区+分批+预聚合 |
| R BLAS | 参考BLAS（La_library()返回空） | 矩阵运算慢一个数量级，当前投入产出比最高的单项修复 |
| LaTeX | 完全没有（pdflatex/xelatex/tlmgr全缺），偏好use_tinytex:true | Quarto/Rmd转PDF当场失败 |
| 常驻代理 | 亿赛通CDG+Kaspersky+Defender | DPDK/内核旁路/常驻服务/容器运行时基本不可行，任何需驱动级或提权的技术全部出局 |
| 连接禁令 | 禁止连接Superset/Dolphin/StarRocks/任何博彩站点，禁止实测 | L0-L2全部无法验证，只能纸上设计与静态评审 |
| Python环境 | C:\work\envs\ds已有190包，15项真算冒烟测试全过 | L3-L5绝大多数技术可立即跑起来 |

```
::: 

::: {.callout-note collapse="true"}
來源第 244 行；段落 d28cad0ad79baf9e；UNKNOWN_INHERITED。

```text
> **结论**：L0-L2采集/传输/存储是公司平台侧的事，一行都验证不了；L3-L5特征/判决/治理今天就能做，那才是a168缺口。把精力压在L3-L5，是唯一不自欺的选择。

```
::: 

::: {.callout-note collapse="true"}
來源第 246 行；段落 f1ea014c09df7e33；UNKNOWN_INHERITED。

```text
**最大盲区-标签**：所有技术都假设有标签，a168真实瓶颈是case outcome与申诉/回滚的标签回流，直击该瓶颈的只有五项：**PU Learning · Snorkel弱监督 · 主动学习 · 蜜罐Canary token · 拒绝推断**，这五项价值高于其余全部技术之和。

```
::: 

::: {.callout-note collapse="true"}
來源第 248 行；段落 e79f963597ae232c；UNKNOWN_INHERITED。

```text
**第二盲区-经济锚**：`house_edge=NULL`与`economic_path_status=NOT_ESTABLISHED`未解除前，`theo/adt/nmpt/esi`不在可执行代码中，任何止损金额估算都缺经济锚，必须先解。

```
::: 

::: {.callout-note collapse="true"}
來源第 252 行；段落 7eeefd51c44093f5；UNKNOWN_INHERITED。

```text
## §8 ActionPlan - 自强追赶天下最顶尖，三价值四层落地路线图

```
::: 

::: {.callout-note collapse="true"}
來源第 254 行；段落 3440c412592571ee；UNKNOWN_INHERITED。

```text
### 8.1 核心原则
AI只做排序、预警与低风险自动化；高影响决策（封号、限额、提款冻结、干预）必须保留人工覆核与完整审计轨迹，AI永不进入百家乐牌局结果与对脆弱玩家的营销决策。

```
::: 

::: {.callout-note collapse="true"}
來源第 257 行；段落 3179e6a3c2da733b；UNKNOWN_INHERITED。

```text
### 8.2 四层架构（L0-L5）

```
::: 

::: {.callout-note collapse="true"}
來源第 259 行；段落 08e0789f619a3cc2；UNKNOWN_INHERITED。

```text
| 层级 | 技术组件 | 对应目标 | 来源 |
|---|---|---|---|
| L0 采集 | Angel Group姿势辨识+RFID智慧桌，YOLOv8边缘 | 实时牌面/下注事件 | Angel Group OBSERVED |
| L1 数据摄取 | Kafka+Flink+Iceberg+StarRocks/ClickHouse（批流一体） | 实时事件流 | DeepSeek/Gemini |
| L2 特征与模型 | Scikit-Learn/XGBoost/LightGBM + TensorFlow/PyTorch + PyG RGCN/GraphSAGE + Isolation Forest + YOLOv8/CRNN + TensorRT/ONNX + Polars/DuckDB | 欺诈/串通/流失/风险评分/牌面识别 | 全量 |
| L3 商业智能 | Bonus Guardian / Smartico/Optimove Opti-X / BetBuddy / Mindway / SEON / Featurespace ARIC / ACT Fraud Rings syndicate可视化 | 奖金风控、RL留存优化、责任博彩 | 全量 |
| L4 合规与审计 | Sumsub/Onfido+ Cevro AI / ComplianceSuite.ai / AI Decision Logger + MGA Charter + ISO/IEC 42001 + ALCOA+ IQ/OQ/PQ | KYC/AML自动化、审计追踪 | DeepSeek/Grok/Gemini |
| L5 治理 | `targets`+OpenLineage血统，Sigma+MITRE规则工程，Splink概率实体解析，E-value+负对照结局因果可信 | 可复现、可解释、可撤销 | 跨行业移植 |

```
::: 

::: {.callout-note collapse="true"}
來源第 268 行；段落 9d33eae895d1b3a3；UNKNOWN_INHERITED。

```text
### 8.3 分阶段实施（RPN优先级）

```
::: 

::: {.callout-note collapse="true"}
來源第 270 行；段落 dd67ee0e6dd3c1ad；UNKNOWN_INHERITED。

```text
**立即落地 0-30天 - 止损优先（RPN最高）**
- Mindway GameScanner或BetBuddy + Sumsub/SEON + 基本案件管理系统 + AI Decision Logger
- 建立AI系统清单、问责人、人工覆盖能力日志，满足MGA Charter高影响系统要求
- 接入Kafka→Flink实时管道，ODS→DWS特征工程，规则层秒级拦截KYC未完成/极端迟下注/已知黑名单
- 部署 **PU Learning + Snorkel** 解决标签瓶颈，Canary token蜜罐

```
::: 

::: {.callout-note collapse="true"}
來源第 276 行；段落 5b6c0b1b83402d4c；UNKNOWN_INHERITED。

```text
**3-6个月 - 增效（RPN中）**
- 接入Smartico/Optimove做合规导向CRM，contextual bandits测试奖励时机，Reward=限额采纳/冷静期完成/风险下降，禁止GGR
- 评估SOFTSWISS Casino Platform + BM3 + EveryMatrix Bonus Guardian，对接PAM实时API
- 试点YOLOv8/v10+CRNN+TensorRT边缘推理，物理牌面识读+电子路纸自动渲染，目标100ms派彩
- 修复R BLAS→OpenBLAS/MKL，性能提升10倍，立即执行

```
::: 

::: {.callout-note collapse="true"}
來源第 282 行；段落 90afb1b6371a105e；UNKNOWN_INHERITED。

```text
**6-12个月 - 规模化与自研**
- 试点Sentient/Octane AI荷官降低真人桌成本，数日交付多语言品牌化桌台，测试低额碎片化玩家留存
- 自建Dealer Anomaly Detection（荷官异常）、Player Risk（玩家风险）、Live Casino Analytics、Agent Network Intelligence（代理层级图谱GNN RGCN/GraphSAGE）
- 建立purge walk-forward验收：Precision@人工产能、误伤预算、可回滚率、人工复核率100%、模型漂移监控
- 磁盘按日分区+预聚合解决43GB瓶颈

```
::: 

::: {.callout-note collapse="true"}
來源第 288 行；段落 9d7619b989738bed；UNKNOWN_INHERITED。

```text
**长期 - 持续自强**
- 三管线隔离：反诈/串通、AML、责任博彩数据与处置完全分离
- RL仅离线沙盒：固定保护性动作集、因果评估、合规审批后小流量，reward禁止GGR/投注额
- 每周固定as-of日期，只使用当时可见数据建特征，预测未来7/14/30日明确结果：人工确认串通、KYC证据成立、SAR升级、责任博彩实质升级
- LaTeX环境补齐，Quarto转PDF打通

```
::: 

::: {.callout-note collapse="true"}
來源第 294 行；段落 61330920379db5c7；UNKNOWN_INHERITED。

```text
### 8.4 自强KPI（非GGR）

```
::: 

::: {.callout-note collapse="true"}
來源第 296 行；段落 a12a4e74b87b26e7；UNKNOWN_INHERITED。

```text
- **止损**：奖金滥用拦截率、误伤率、5-7亿美元边注优势玩法损失降低、钱骡链揭示数、61,810请求级节省、Precision@产能
- **增效**：7日流失率、30天LTV、月活、独立存款人、NGR、忠诚客户毛收入、桌台弹性扩容成本、每人日闭环案件数
- **合规**：强风险信号响应时延、人工复核率100%、理由码留存率100%、RG资料未流向营销的隔离稽核、限额/冷静期采纳率、申诉成功率、审计证据完备率

```
::: 

::: {.callout-note collapse="true"}
來源第 300 行；段落 00e2dc0f73330b34；UNKNOWN_INHERITED。

```text
### 8.5 最终判断与一句话收束

```
::: 

::: {.callout-note collapse="true"}
來源第 302 行；段落 3a5816587afff37a；UNKNOWN_INHERITED。

```text
> **别追纳秒，追确定性；别追模型，追标签；别追全栈，追那三层你今天就能动的。**
> **止损靠标签，增效靠编排，合规靠血统。**

```
::: 

::: {.callout-note collapse="true"}
來源第 305 行；段落 769f5fae20c14ea8；UNKNOWN_INHERITED。

```text
70家主体、13个行业、60余个软件包里，真正能让a168在三格上同时跃迁的只有六件：

```
::: 

::: {.callout-note collapse="true"}
來源第 307 行；段落 f0928afaf13a008e；UNKNOWN_INHERITED。

```text
| # | 六件核心 | 归格 |
|---|---|---|
| 1 | **PU Learning + Snorkel**（标签） | 止损 |
| 2 | **`targets` + OpenLineage**（编排与血统） | 增效+合规 |
| 3 | **Sigma + MITRE ATT&CK**（规则工程） | 止损+合规 |
| 4 | **Splink**（概率实体解析） | 止损 |
| 5 | **E-value + 负对照结局**（因果可信） | 合规 |
| 6 | **ALCOA+ 与 IQ/OQ/PQ**（治理规格） | 合规 |

```
::: 

::: {.callout-note collapse="true"}
來源第 316 行；段落 8cf8895435762d59；UNKNOWN_INHERITED。

```text
这六件全部可在现有R+Python+DuckDB环境、不连接任何生产系统前提下今天开始。其余五十余项是这六件成立后的放大器，提前上只会放大噪声。

```
::: 

::: {.callout-note collapse="true"}
來源第 320 行；段落 c122f4df77693cf7；UNKNOWN_INHERITED。

```text
## §9 体育与彩票的差异化移植

```
::: 

::: {.callout-note collapse="true"}
來源第 322 行；段落 2306e717ab062ed9；UNKNOWN_INHERITED。

```text
**体育**：Opta数据+Featurespace异常投注检测+Betfair式对冲模型，需处理1.5以下赔率不算有效投注的返水定义陷阱。RL可用于赔率管理自动化（非针对个人）。

```
::: 

::: {.callout-note collapse="true"}
來源第 324 行；段落 93c64cdc837a85ae；UNKNOWN_INHERITED。

```text
**彩票**：重点在RNG熵源审计+provably fair+反合谋（同一团伙包号），Mindway类模型不适用，需引入航天级QuestDB时序监控开奖机物理状态。

```
::: 

::: {.callout-note collapse="true"}
來源第 326 行；段落 301ec06a32893788；UNKNOWN_INHERITED。

```text
**百家乐**：核心是荷官异常+边注AI对抗+路单统计自动化，YOLO读牌+Angel Group姿势辨识是唯一可直接提升结算速度的路径。

```
::: 

::: {.callout-note collapse="true"}
來源第 330 行；段落 8eb2d418a1891b7d；UNKNOWN_INHERITED。

```text
## §10 合规交付与矛盾清单

```
::: 

::: {.callout-note collapse="true"}
來源第 332 行；段落 f0c2659cebd043dd；UNKNOWN_INHERITED。

```text
**矛盾清单M-1~M-11已在总表登记**：
- M-1：Evolution AI宣称归因错误，SEO站不可作官方列
- M-2：Entain 26 vs 近30标记冲突
- M-4：Smartico被Optimove收购官宣，CityBiz/Finsmes交叉验证
- M-5：DraftKings ML定向最可能输钱客户为聚合站转述NYT，非NYT原文，证据降级为INFERRED

```
::: 

::: {.callout-note collapse="true"}
來源第 338 行；段落 8b5ca8a0a9f9be7f；UNKNOWN_INHERITED。

```text
**自我更正SC-A~SC-C**：61家→实测70家，原结论过窄撤回扩充。

```
::: 

::: {.callout-note collapse="true"}
來源第 340 行；段落 6aa88e19673964ac；UNKNOWN_INHERITED。

```text
**六元组指纹铁律**：本白皮书落盘后任何编辑（含空白字符、CRLF转换）指纹失效，须重新签发。

```
::: 

::: {.callout-note collapse="true"}
來源第 344 行；段落 1d1a1518dcdad19f；UNKNOWN_INHERITED。

```text
## 引用源（按主体顺序，一手可回溯）

```
::: 

::: {.callout-note collapse="true"}
來源第 346 行；段落 0be6a6acabaee538；UNKNOWN_INHERITED。

```text
[1] SOFTSWISS Anti-Fraud 2022省€16M+ [2] Optimove收购Smartico 2026-04 [3] Octane Studios AI Baccarat首发 [4] MGA AI Gaming Charter 2026-09-18 [5] Sentient Studios $10M A轮 [6] Playtech BetBuddy [7] Featurespace [8] Angel Group澳门Sands千张智慧百家乐桌 [9] Mindway AI ≥87% [10] Differential Labs边注40-60%收入年损5-7亿 [11] MGA Charter 48页自愿框架 [12] EU AI Act高风险定性 [13] UKGC LCCP 3.4.3

```
::: 

::: {.callout-note collapse="true"}
來源第 350 行；段落 1d980b55c1ca71e7；UNKNOWN_INHERITED。

```text
*Powered by Scibrokes® 世博量化® · 本件为参考资料，需配合GLI/eCOGRA认证、MGA/Isle of Man/PAGCOR牌照、资金隔离审计后方可商用。AI永不进入牌局结果，RG数据与营销系统物理隔离，RL reward仅限保护性指标。*
```
::: 

### 來源：Reference/全球在线博彩娱乐_AI量化科技与安全治理白皮书_2026-09-27.md

[原始來源](<全球在线博彩娱乐_AI量化科技与安全治理白皮书_2026-09-27.md>)；SHA256：`1bf00f46508ab44ba121f9abe9f516c1590d0abe4181342fa9122bb38018548c`。下列為未覆蓋段落；歷史主張未經收錄自動驗證。

::: {.callout-note collapse="true"}
來源第 1 行；段落 3ab8c2182a1a1d59；UNKNOWN_INHERITED。

```text
# 全球在线博彩娱乐智能化与量化治理白皮书（2026-09-27）

```
::: 

::: {.callout-note collapse="true"}
來源第 3 行；段落 767e72ddef93e6a6；UNKNOWN_INHERITED。

```text
> 体育博彩 · 彩票 / iLottery · 真人赌场 / 百家樂 | AI、量化风控、实时数据、责任博彩与跨行业技术迁移

```
::: 

::: {.callout-note collapse="true"}
來源第 5 行；段落 7eb70257593da06f；UNKNOWN_INHERITED。

```text

```
::: 

::: {.callout-note collapse="true"}
來源第 6 行；段落 ece2ee8b2ec8e3fa；UNKNOWN_INHERITED。

```text
# 执行摘要

```
::: 

::: {.callout-note collapse="true"}
來源第 8 行；段落 2aa55d8a2a0412b8；UNKNOWN_INHERITED。

```text
本白皮书以六份附件为研究底稿：

```
::: 

::: {.callout-note collapse="true"}
來源第 10 行；段落 3ad6ecafad8a1828；UNKNOWN_INHERITED。

```text
1. `電腦已昇級至視窗11版（工欲善其事必先利其器）(2).qmd`
2. `Aerospace_Ecosystem_Report.qmd`
3. `Baccarat-Ai-Automation-Report(1).md`
4. `Inteligent_egaming_platform_ref_v000.000.001.qmd`
5. `perfect-baccarat-report(1).md`
6. `顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1_0_0(1).md`

```
::: 

::: {.callout-note collapse="true"}
來源第 17 行；段落 14ad43a728e0ef79；UNKNOWN_INHERITED。

```text
并以 2026-09-27 为 **as-of date**，对核心监管条款、上市公司年报、官方产品页、SEC / 公司公告进行二次校正。

```
::: 

::: {.callout-note collapse="true"}
來源第 19 行；段落 74c0a57d2dcd42ff；UNKNOWN_INHERITED。

```text
本白皮书的核心判断不是“哪家公司用了最多 AI”，而是：

```
::: 

::: {.callout-note collapse="true"}
來源第 21 行；段落 53b5a7e2aa597243；UNKNOWN_INHERITED。

```text
> **世界级在线博彩平台的护城河，是可信数据底座 + 低延迟事件处理 + 风险/价值模型 + 可解释决策 + 人工高影响复核 + 责任博彩硬约束 + 效果回流，而不是单一大模型、Transformer 或 RL。**

```
::: 

::: {.callout-note collapse="true"}
來源第 23 行；段落 7a7fa5713f0d3c01；UNKNOWN_INHERITED。

```text
对完美真人及其未来“体育 + 彩票 + 真人赌场/百家乐”综合娱乐平台，建议建设统一的 **Gaming Decision Intelligence Operating System（GDI-OS）**：

```
::: 

::: {.callout-note collapse="true"}
來源第 25 行；段落 30be41968e0ca752；UNKNOWN_INHERITED。

```text
`Event Ledger → Point-in-Time Feature Store → Risk/Value Models → Constrained Decision Engine → Case/Human Review → Action → Outcome Ledger → Causal Evaluation → Monitoring/Learning`

```
::: 

::: {.callout-note collapse="true"}
來源第 27 行；段落 ed3beea22cf1f734；UNKNOWN_INHERITED。

```text
其中必须遵守三条硬边界：

```
::: 

::: {.callout-note collapse="true"}
來源第 29 行；段落 6932b73fa056500d；UNKNOWN_INHERITED。

```text
1. **AI 不进入游戏结果**：不得按玩家个体改变 RNG、牌靴、发牌、赔率、结算、派彩或结果。
2. **责任博彩（RG）是硬约束，不是可被收入抵消的加权分数**：强风险状态不得进入营销、VIP、返水、催存、召回模型。
3. **高影响动作保留人工复核、申诉、回滚与完整审计轨迹**；自动化以排序、预警、低风险动作与证据整合为主。

```
::: 

::: {.callout-note collapse="true"}
來源第 35 行；段落 91719b35ad39ca0d；UNKNOWN_INHERITED。

```text
# 1. 审阅方法与证据纪律

```
::: 

::: {.callout-note collapse="true"}
來源第 37 行；段落 5cbbb0f9f1eff5d8；UNKNOWN_INHERITED。

```text
## 1.1 证据等级

```
::: 

::: {.callout-note collapse="true"}
來源第 39 行；段落 f680aad150cd01c0；UNKNOWN_INHERITED。

```text
本白皮书沿用并强化附件中的分层：

```
::: 

::: {.callout-note collapse="true"}
來源第 41 行；段落 3bbf46fa152a7209；UNKNOWN_INHERITED。

```text
| 等级 | 定义 | 可用于何种结论 |
|---|---|---|
| **P0 / VERIFIED** | 监管机构、法律文本、上市公司年报、SEC、公司官方技术/产品资料 | 可作为事实基线 |
| **P1 / OBSERVED** | 一手公告、官方案例、公开融资/合作资料 | 可引用，但需注明为厂商自述时的测量口径 |
| **P2 / INFERRED** | 高质量行业媒体、供应商案例、二手技术报道 | 只能作为线索或趋势 |
| **P3 / UNKNOWN** | 附件出现但未找到可靠技术披露 | 明确留白，禁止脑补 |
| **CONDITIONAL** | 取决于牌照、司法辖区、合同、数据授权或测试条件 | 必须列前提 |

```
::: 

::: {.callout-note collapse="true"}
來源第 49 行；段落 fb1dab33708c9d73；UNKNOWN_INHERITED。

```text
任何指标都必须携带：**主体、时点、样本、分母、口径、地区、来源、是否供应商自述**。重复出现不会自动提升证据等级。

```
::: 

::: {.callout-note collapse="true"}
來源第 51 行；段落 b80c8e9f9c3ec611；UNKNOWN_INHERITED。

```text
## 1.2 本次校对的关键更正

```
::: 

::: {.callout-note collapse="true"}
來源第 53 行；段落 67d5f99141477c91；UNKNOWN_INHERITED。

```text
### 更正 A：Evolution 的若干“官方 AI”宣称必须降级

```
::: 

::: {.callout-note collapse="true"}
來源第 55 行；段落 7c4c635ad4a8c2ef；UNKNOWN_INHERITED。

```text
附件已经识别出：部分 “AI-Powered Fraud Detection / Biometric Dealer Authentication / Advanced AI Monitoring” 的引文实际上来自 SEO / 内容农场而非 Evolution 官方资料。因此，本白皮书只确认 Evolution 的**全球真人娱乐规模、Studio 网络、Live/RNG 产品与公开年报能力**；未有 P0/P1 证据的 AI 功能全部保持 P2/P3。

```
::: 

::: {.callout-note collapse="true"}
來源第 57 行；段落 57e0af668e045d22；UNKNOWN_INHERITED。

```text
可确认的 2025 年末规模：Evolution 官方年报称约 **2,000 张 Live tables、22,000+ 员工**；2026 年继续扩建美国 Live Studio。

```
::: 

::: {.callout-note collapse="true"}
來源第 59 行；段落 515151095fbd4095；UNKNOWN_INHERITED。

```text
### 更正 B：“只有三家具名案例”已经过时

```
::: 

::: {.callout-note collapse="true"}
來源第 61 行；段落 274986313db35abb；UNKNOWN_INHERITED。

```text
Playtech/BetBuddy、SOFTSWISS、EveryMatrix Bonus Guardian、FDJ UNITED/legacy Kindred PS-EDS、Entain ARC、Flutter safer-gambling体系、Mindway、Optimove/Smartico、Sportradar 等均形成可查证的 AI / ML / 风控 / 玩家保护证据链；但其成熟度、应用层与证据等级不同，不能混成“RL 全自动运营”。

```
::: 

::: {.callout-note collapse="true"}
來源第 63 行；段落 99aa3e2984754aa2；UNKNOWN_INHERITED。

```text
### 更正 C：Smartico 不是简单写成“已完成收购”

```
::: 

::: {.callout-note collapse="true"}
來源第 65 行；段落 6c7180667634d6fa；UNKNOWN_INHERITED。

```text
2026-04-06 Optimove 官方公告是 **signed an agreement to acquire Smartico**，并称交易预计随后数周完成；公告同时明确双方继续独立经营。若没有后续完成公告，不应把“签署协议”写成“已完成并表”。

```
::: 

::: {.callout-note collapse="true"}
來源第 67 行；段落 f494b82b7474d13b；UNKNOWN_INHERITED。

```text
### 更正 D：Kindred 的当前公司语境必须更新

```
::: 

::: {.callout-note collapse="true"}
來源第 69 行；段落 c35aa6a9fcb2d265；UNKNOWN_INHERITED。

```text
FDJ 于 2024 年收购 Kindred，2025-03 更名为 **FDJ UNITED**。因此 PS-EDS 应写作 **FDJ UNITED / legacy Kindred PS-EDS**，而不是把 Kindred Group 当作仍独立存在的集团来比较。

```
::: 

::: {.callout-note collapse="true"}
來源第 71 行；段落 1c6158b872bb5b31；UNKNOWN_INHERITED。

```text
### 更正 E：EU AI Act 不能写成“博彩 AI 一律高风险”

```
::: 

::: {.callout-note collapse="true"}
來源第 73 行；段落 224dbee0d29f3234；UNKNOWN_INHERITED。

```text
EU AI Act 的 high-risk 分类依赖 **Article 6 + Annex III** 的具体用途；博彩欺诈检测、推荐、聊天机器人并不会因为属于博彩行业自动成为 high-risk。聊天机器人等特定系统自 **2026-08-02** 起主要受 Article 50 透明度义务影响。若某系统落入 Annex III、进行自然人 profiling 并实质影响受保护决策，则需按具体场景评估。

```
::: 

::: {.callout-note collapse="true"}
來源第 75 行；段落 c5cdc9cff70c0061；UNKNOWN_INHERITED。

```text
### 更正 F：UKGC LCCP 3.4.3 的准确含义

```
::: 

::: {.callout-note collapse="true"}
來源第 77 行；段落 3e4d8e4b2f84663b；UNKNOWN_INHERITED。

```text
英国博彩委员会要求强伤害指标被**及时自动化处理**；但自动流程应用后，牌照持有人仍须**逐个客户人工审查其运行，并允许客户质疑影响自己的自动决定**。这直接支持“自动化 + 人工救济”架构。

```
::: 

::: {.callout-note collapse="true"}
來源第 79 行；段落 f5e2a9b2c4a9bb1a；UNKNOWN_INHERITED。

```text
### 更正 G：银行模型治理引用更新

```
::: 

::: {.callout-note collapse="true"}
來源第 81 行；段落 e08d49059e92ad41；UNKNOWN_INHERITED。

```text
美国联储 **SR 26-2（2026-04-17）**确实 supersede / replace SR 11-7 与 SR 21-8，强调 risk-based model risk management、vendor model validation、ongoing monitoring 与 outcome analysis。附件此处是正确且很有价值的跨行业更新。

```
::: 

::: {.callout-note collapse="true"}
來源第 83 行；段落 564eb8075fcd588b；UNKNOWN_INHERITED。

```text
### 更正 H：B2B 与 B2C 规模指标不可混加

```
::: 

::: {.callout-note collapse="true"}
來源第 85 行；段落 8c443052b3fe7970；UNKNOWN_INHERITED。

```text
Evolution / EveryMatrix 等 B2B 供应商的规模应看：运营商数、桌台数、请求量、事件量、市场/牌照覆盖；Flutter / FDJ UNITED 等 B2C 才可谈玩家/账户。Mindway 的“监测玩家数”又是跨客户汇总。三类分母不能相加。

```
::: 

::: {.callout-note collapse="true"}
來源第 89 行；段落 46d6619d509a3c7c；UNKNOWN_INHERITED。

```text
# 2. 2026 世界级竞争版图：不是一张排行榜，而是能力拼图

```
::: 

::: {.callout-note collapse="true"}
來源第 91 行；段落 af5c32ae6133b5c5；UNKNOWN_INHERITED。

```text
## 2.1 真人赌场 / 百家樂核心供应商

```
::: 

::: {.callout-note collapse="true"}
來源第 93 行；段落 7028a5e6504c3116；UNKNOWN_INHERITED。

```text
| 主体 | 可确认强项 | 局限 / 风险 | 完美真人应迁移的能力 |
|---|---|---|---|
| **Evolution / Ezugi** | 全球 Studio 与 Live tables 规模；成熟 Live 产品族；多地区本地化；专属桌与多品牌内容 | Live 是重运营、重 Studio；部分附件 AI 宣称证据不足；大规模网络也暴露网络攻击/地区运营风险 | QoE、Studio capacity、产品族管理、跨地区容灾、桌台运营指标、专属桌体系 |
| **Playtech Live + PAM+ + BetBuddy** | Live + PAM + safer gambling + managed services 一体化；2025 年报称 200+ B2B 客户、50+ regulated jurisdictions、28 个品牌使用 BetBuddy | 平台复杂、实施/迁移成本高；供应商锁定风险；并非每项“AI”都公开模型细节 | 把 Live、PAM、RG、案件运营放在同一数据闭环；模型治理与人工干预 |
| **Pragmatic Play Live** | 产品迭代、Live UX、多语言、产品包装、快速内容交付 | 公开 AI/RL 中台证据弱于 Playtech；不应把 Auto-Roulette/机器人等同“AI 决策” | 产品化速度、移动端 UX、统一接入与运营工具 |
| **SA Gaming / Dream Gaming / Asia Gaming / AllBet / Sexy Baccarat / Pretty / Venus / Big / eBet / BetGames.TV / KingMaker / WM Perfect** | 亚洲真人桌、本地化、百家乐用户习惯与桌台密度是重要对标维度 | 附件中多数 AI/ML 能力缺少 P0/P1 技术披露；不能把“自动”“稳定”“AI 推荐”宣传当事实 | 把这些主体作为 **产品/桌台/地区化 benchmark**，AI 能力一律采购前尽调 |
| **Octane Studios / Sentient Studios** | AI Dealer / AI croupier 是 2026 的前沿实验方向；可扩展、多语言、品牌化 | 商业规模、监管接受度、长期玩家信任、延迟/口型/渲染一致性仍需验证；不能当成熟工业标准 | 只在测试线做可逆 Pilot；RNG/结果引擎与 AI 表现层彻底分离 |
| **Angel Group / IDX Games** | 实体智慧桌、RFID/视觉/行为数据让实体桌走向高质量事件化 | 实体硬件与线上架构并非同一问题；摄像/身份数据合规成本高 | 迁移“事件可观测性、身份归属概率、桌台状态数字化”理念 |

```
::: 

::: {.callout-note collapse="true"}
來源第 102 行；段落 a62aa330b2229f61；UNKNOWN_INHERITED。

```text
### 对百家樂最重要的产品结论

```
::: 

::: {.callout-note collapse="true"}
來源第 104 行；段落 30163bfaaf3c0f58；UNKNOWN_INHERITED。

```text
真正值得做的不是“再做一张路纸”，而是将 **牌局展示层** 与 **经营决策层** 分离：

```
::: 

::: {.callout-note collapse="true"}
來源第 106 行；段落 6db67bffd8c4c81f；UNKNOWN_INHERITED。

```text
- 游戏层：规则、牌靴/RNG、结果、结算、认证。
- 体验层：视频、延迟、桌台切换、多语言、roadmap、辅助统计。
- 经营层：玩家、代理、支付、奖金、风控、RG、CRM、客服。
- 决策层：风险、价值、资格、动作、人工案件、效果回流。

```
::: 

::: {.callout-note collapse="true"}
來源第 111 行；段落 095aa28347001669；UNKNOWN_INHERITED。

```text
百家乐历史 road map 属描述性信息，不应被包装为保证未来结果的预测工具。

```
::: 

::: {.callout-note collapse="true"}
來源第 115 行；段落 da0e30c6c5e5e975；UNKNOWN_INHERITED。

```text
# 3. B2B 平台、CRM、反欺诈与责任博彩

```
::: 

::: {.callout-note collapse="true"}
來源第 117 行；段落 4bdebd16b7e23622；UNKNOWN_INHERITED。

```text
## 3.1 B2B / PAM / CRM

```
::: 

::: {.callout-note collapse="true"}
來源第 119 行；段落 b9cc406b6c8932f1；UNKNOWN_INHERITED。

```text
| 主体 | 公开能力 | 优势 | 局限 / 采购问法 |
|---|---|---|---|
| **SOFTSWISS** | Anti-Fraud、平台、业务指标监控等；官方称 2025 年 1–8 月阻止 €15M+ 欺诈交易、关闭 56k+ tasks | 反欺诈运营闭环与案件化思维 | 历年“请求数/节省额”口径不同，不得直接同比；索要 precision、false-positive、人工复核、SLA |
| **EveryMatrix** | Bonus Guardian 官方称使用 AI/ML、持续分析玩家行为、角色式响应 | 把检测嵌入 Bonus/Engage 业务动作 | “持续学习”必须问是否在线学习、训练周期、回滚与人工审批；withdrawal hold 等高影响动作应有人审 |
| **Optimove / Smartico** | CRM、gamification、推荐、营销自动化；2026-04 宣布收购协议 | 实验、CRM 编排、推荐与玩家生命周期 | RL/contextual-bandit 证据需逐产品/版本核实；禁止把 RG 风险用于刺激投注 |
| **GiG / NuxGame / Future Anthem / BetConstruct 等** | 附件列为推荐/平台/AI运营候选 | 可作为组合式采购池 | 采购必须回到 P0/P1 的模型卡、数据字典、SLA、审计与案例 |

```
::: 

::: {.callout-note collapse="true"}
來源第 126 行；段落 2c9196b1b4efbe1a；UNKNOWN_INHERITED。

```text
## 3.2 Fraud / KYC / AML / Bot / RG 完整能力池

```
::: 

::: {.callout-note collapse="true"}
來源第 128 行；段落 cc4e986b5ed82247；UNKNOWN_INHERITED。

```text
附件明确列出的供应商必须保留在尽调池中：

```
::: 

::: {.callout-note collapse="true"}
來源第 130 行；段落 72cad61763c18334；UNKNOWN_INHERITED。

```text
- **交易/行为欺诈**：Featurespace ARIC、SEON、Sift、CrossClassify、Group-IB、SOFTSWISS、EveryMatrix Bonus Guardian。
- **地理/设备/机器人**：GeoComply、cside，以及平台侧 JA4/JA4+、设备指纹与行为时序。
- **KYC / identity**：Sumsub、Onfido、Jumio、Veriff、iDenfy、Shufti。
- **AML / entity intelligence**：NICE Actimize、ComplyAdvantage、Flagright、Quantexa、ComplianceSuite.ai / Infocredit。
- **责任博彩**：Playtech BetBuddy、Mindway AI GameScanner/Gamalyze、FDJ UNITED/legacy Kindred PS-EDS、Entain ARC、Sportradar Bettor Sense、Neccton Mentor。
- **客服 / Agent**：Cevro AI、InteractiveAI、Moveo.AI。

```
::: 

::: {.callout-note collapse="true"}
來源第 137 行；段落 135394452f43b6ee；UNKNOWN_INHERITED。

```text
采购原则不是“功能最多者胜”，而是必须回答：

```
::: 

::: {.callout-note collapse="true"}
來源第 139 行；段落 411d0aab1ec0d82a；UNKNOWN_INHERITED。

```text
`数据来自哪里 → 标签如何定义 → 模型如何验证 → 误伤如何量化 → 谁能覆盖模型 → 是否可申诉 → 如何回滚 → 是否可导出审计证据 → 数据是否跨境/二次使用`

```
::: 

::: {.callout-note collapse="true"}
來源第 143 行；段落 b3932c5f464e9311；UNKNOWN_INHERITED。

```text
# 4. 体育博彩：应从“赔率网站”升级为实时数据与交易风险系统

```
::: 

::: {.callout-note collapse="true"}
來源第 145 行；段落 fd35d0c5513b6100；UNKNOWN_INHERITED。

```text
体育博彩的技术核心和百家乐不同。核心不是 Dealer，而是：

```
::: 

::: {.callout-note collapse="true"}
來源第 147 行；段落 77c982708a5db0c7；UNKNOWN_INHERITED。

```text
`Official Data → Event Ingestion → Pricing/Odds → Liability/Risk → Bet Acceptance → Settlement → Integrity Monitoring`

```
::: 

::: {.callout-note collapse="true"}
來源第 149 行；段落 cafc67938da9f869；UNKNOWN_INHERITED。

```text
## 4.1 2026 值得对标的体育基础设施

```
::: 

::: {.callout-note collapse="true"}
來源第 151 行；段落 174d2f96f359183d；UNKNOWN_INHERITED。

```text
| 主体 | 公开能力 | 对平台的启示 |
|---|---|---|
| **Genius Sports / GeniusIQ** | SEC 2025 20-F 明确披露 AI/ML、计算机视觉、官方数据、实时赛事采集、赔率与 integrity；官方数据覆盖大量赛事 | 官方数据权、低延迟采集、统一 AI/data layer 是护城河，不只是模型 |
| **Sportradar** | 2025 年报披露实时 AI inferencing、低延迟数据网络、AI/ML liability-driven odds adjustment 与 sportsbook risk management；UFDS 用于 integrity | 赔率风险、投注接受、完整性监控必须共用实时数据但保持治理隔离 |
| **Kambi** | 2025 年报称 AI-driven trading 持续增长，48% bets 由 AI-driven trading 覆盖 | 人机混合交易台：AI定价/风险 + trader oversight，比完全无人更现实 |
| **Playtech Sports / EveryMatrix / BetConstruct 等** | 可提供 turnkey / PAM / managed services | 适合“买平台 + 自研风险/数据层”模式，避免全栈从零造轮子 |

```
::: 

::: {.callout-note collapse="true"}
來源第 158 行；段落 ee443bd32ea4fb9f；UNKNOWN_INHERITED。

```text
## 4.2 体育博彩必须比百家乐额外增加的模型

```
::: 

::: {.callout-note collapse="true"}
來源第 160 行；段落 01dd74b9d8ecb348；UNKNOWN_INHERITED。

```text
- Event-time / market-time 对齐与 clock quality。
- Official feed quality、延迟、缺包、异常 score update。
- Odds / fair-price / margin / liability engine。
- Bet acceptance 与 exposure limits。
- Arbitrage / latency exploitation / suspicious market detection。
- Match integrity 与异常市场联动。
- 结算规则引擎与赛事取消/更正重放。

```
::: 

::: {.callout-note collapse="true"}
來源第 168 行；段落 542e7fb85f31d40d；UNKNOWN_INHERITED。

```text
核心 KPI 不是只有 GGR，而应包括：feed latency p99.9、stale-odds exposure、manual trading load、accepted-bet rate、price error、settlement exception、integrity alerts precision。

```
::: 

::: {.callout-note collapse="true"}
來源第 172 行；段落 046dac693952b506；UNKNOWN_INHERITED。

```text
# 5. 彩票 / iLottery：应学习“中央系统 + 零售 + 数字账户 + Responsible Play”

```
::: 

::: {.callout-note collapse="true"}
來源第 174 行；段落 3e69dddc2f910844；UNKNOWN_INHERITED。

```text
彩票的技术重心与赌场又不同：

```
::: 

::: {.callout-note collapse="true"}
來源第 176 行；段落 d056b7c8020cb879；UNKNOWN_INHERITED。

```text
`Central Gaming System → Retailer Network → Ticket/Draw Integrity → PAM/Wallet → Digital/eInstant → CRM/Loyalty → Responsible Play`

```
::: 

::: {.callout-note collapse="true"}
來源第 178 行；段落 7cac2a8156cf8f57；UNKNOWN_INHERITED。

```text
## 5.1 2026 主要对标

```
::: 

::: {.callout-note collapse="true"}
來源第 180 行；段落 5e79bc7a8337c4e7；UNKNOWN_INHERITED。

```text
| 主体 | 可确认能力 | 值得迁移 |
|---|---|---|
| **Scientific Games** | 2026 Arizona / Minnesota 部署 Momentum；Delaware iLottery 采用 SG PAM、wallet、CRM、bonus engine、Healthy Play 与 KYC | 真正的 omnichannel：零售与数字统一账户、忠诚、风控、RG |
| **Brightstar Lottery**（前 IGT Lottery） | 2025 年改名，成为 pure-play global lottery；iLottery 继续扩展 | lottery core、零售终端、数字化、长期政府合同与高可用 |
| **Allwyn** | 2026-03 完成与 OPAP 组合，成为大型上市 lottery/gaming operator | 跨市场运营、数字与零售整合、集团治理 |
| **FDJ UNITED** | 法国/爱尔兰 lottery + 欧洲 online betting/gaming；整合 legacy Kindred | lottery 的公共信任/责任框架与线上博彩能力整合 |

```
::: 

::: {.callout-note collapse="true"}
來源第 187 行；段落 81eaf79475bc5ce2；UNKNOWN_INHERITED。

```text
## 5.2 彩票风控的优先级

```
::: 

::: {.callout-note collapse="true"}
來源第 189 行；段落 a85a8b8f08a9312e；UNKNOWN_INHERITED。

```text
- Draw / RNG / ticket integrity。
- retailer fraud、claim fraud、account takeover。
- ticket lifecycle / serial / audit。
- KYC、wallet、payment、self-exclusion。
- 游戏风险评估与 Responsible Play。
- 数字与零售统一但权限分离的 customer 360。

```
::: 

::: {.callout-note collapse="true"}
來源第 196 行；段落 f44eac3adcc955c8；UNKNOWN_INHERITED。

```text
彩票不应照搬赌场“提升游戏时长”的增长目标；公共信任与 Responsible Play 是一级目标。

```
::: 

::: {.callout-note collapse="true"}
來源第 200 行；段落 24b5c9b229acf2ac；UNKNOWN_INHERITED。

```text
# 6. 跨行业技术迁移：只迁移“同构问题”，不迁移炫技

```
::: 

::: {.callout-note collapse="true"}
來源第 202 行；段落 8f4c3cad972f4825；UNKNOWN_INHERITED。

```text
## 6.1 金融 / 高频交易

```
::: 

::: {.callout-note collapse="true"}
來源第 204 行；段落 6a9ce11778c812c2；UNKNOWN_INHERITED。

```text
**可迁移：**

```
::: 

::: {.callout-note collapse="true"}
來源第 206 行；段落 12fce05404b67a9e；UNKNOWN_INHERITED。

```text
- PTP / 高质量时间戳、事件序列号。
- p99/p99.9 tail latency 与 backpressure，而不是追求虚假的“会员纳秒互动”。
- Meta-labeling：第一层识别异常，第二层决定是否升级人工。
- Purged walk-forward / embargo / CPCV 思想用于防时间泄漏和调参过拟合。
- Model challenger、压力测试、reverse stress test。

```
::: 

::: {.callout-note collapse="true"}
來源第 212 行；段落 8ed42802f96829ba；UNKNOWN_INHERITED。

```text
**不应盲迁移：**

```
::: 

::: {.callout-note collapse="true"}
來源第 214 行；段落 309b3258d851a583；UNKNOWN_INHERITED。

```text
- FPGA / RDMA / kernel bypass 除非压力测试证明通用流处理无法满足 SLA。
- Kelly、交易 alpha 等不能直接映射为“让玩家更输”的博彩目标。

```
::: 

::: {.callout-note collapse="true"}
來源第 217 行；段落 4367697125dcf270；UNKNOWN_INHERITED。

```text
## 6.2 银行业

```
::: 

::: {.callout-note collapse="true"}
來源第 219 行；段落 93f5cbc9cbc998f4；UNKNOWN_INHERITED。

```text
2026 的 **SR 26-2** 是更合适的模型治理模板：

```
::: 

::: {.callout-note collapse="true"}
來源第 221 行；段落 b74ba5fa761d39e9；UNKNOWN_INHERITED。

```text
- model inventory；
- conceptual soundness；
- independent validation；
- vendor-model due diligence；
- ongoing monitoring；
- outcome analysis；
- overrides / overlays 可解释；
- model retirement。

```
::: 

::: {.callout-note collapse="true"}
來源第 230 行；段落 a9963da5b9ed919d；UNKNOWN_INHERITED。

```text
这比“哪个模型 AUC 高”重要得多。

```
::: 

::: {.callout-note collapse="true"}
來源第 232 行；段落 15f4a85f77332337；UNKNOWN_INHERITED。

```text
## 6.3 电商与广告科技

```
::: 

::: {.callout-note collapse="true"}
來源第 234 行；段落 931fded70a275bf5；UNKNOWN_INHERITED。

```text
可迁移：

```
::: 

::: {.callout-note collapse="true"}
來源第 236 行；段落 7620d44cf74db5b2；UNKNOWN_INHERITED。

```text
- Point-in-time feature correctness。
- Feature store online/offline consistency。
- CUPED、switchback、sequential testing、FDR。
- 推荐系统的召回/排序架构。

```
::: 

::: {.callout-note collapse="true"}
來源第 241 行；段落 417fe7f19cf6c890；UNKNOWN_INHERITED。

```text
必须切断：

```
::: 

::: {.callout-note collapse="true"}
來源第 243 行；段落 9e5e73f93b0c431e；UNKNOWN_INHERITED。

```text
- 不得把 RG 风险、追损、脆弱性作为促销/推荐特征。
- 不得以“投注时长/亏损/入金”为 RL reward。

```
::: 

::: {.callout-note collapse="true"}
來源第 246 行；段落 339a6bb2fb3dfd90；UNKNOWN_INHERITED。

```text
## 6.4 资安 / 反欺诈

```
::: 

::: {.callout-note collapse="true"}
來源第 250 行；段落 12a6860f5f17075c；UNKNOWN_INHERITED。

```text
- Detection-as-Code。
- Sigma / MITRE ATT&CK 式“战术—技术—程序”风险知识图谱。
- UEBA peer-group analysis。
- probabilistic entity resolution。
- graph communities、temporal graph。
- bot / device / TLS / browser fingerprinting。
- Zero Trust、least privilege、immutable audit。

```
::: 

::: {.callout-note collapse="true"}
來源第 258 行；段落 1abb7e3d2713a2e9；UNKNOWN_INHERITED。

```text
这里的 red-team 目标应是**自己的测试线与防御能力**，而不是未经授权测试竞争对手系统。

```
::: 

::: {.callout-note collapse="true"}
來源第 260 行；段落 47faf4650599a010；UNKNOWN_INHERITED。

```text
## 6.5 AI / 科学研究

```
::: 

::: {.callout-note collapse="true"}
來源第 264 行；段落 9e2f910441e3128f；UNKNOWN_INHERITED。

```text
- PU Learning：未标注 ≠ 负样本。
- Weak supervision / Snorkel。
- Active learning：把人工审查分配给最有信息价值的案件。
- Drift / calibration monitoring。
- Model Cards / Datasheets。
- preregistration、negative controls、FDR、effect size、E-value。
- 可重复分析：Quarto + `renv` + Docker/Apptainer + `targets` / Snakemake / Nextflow。

```
::: 

::: {.callout-note collapse="true"}
來源第 272 行；段落 1b74fad3b55781c5；UNKNOWN_INHERITED。

```text
## 6.6 宇航 / 安全关键系统

```
::: 

::: {.callout-note collapse="true"}
來源第 274 行；段落 bf44401730b68984；UNKNOWN_INHERITED。

```text
附件的宇航报告最大价值，不在于把 Palantir、SpaceX 的专有栈照搬进博彩，而在于以下工程原则：

```
::: 

::: {.callout-note collapse="true"}
來源第 276 行；段落 fc103a3df74e657a；UNKNOWN_INHERITED。

```text
- FDIR：检测—隔离—恢复/降级。
- 明确的 telemetry schema、timestamp、sequence。
- graceful degradation：模型失效→规则；规则失效→人工。
- immutable replay / “黑匣子”。
- worst-case / tail-latency 设计。
- FMEA / fault tree / change control。

```
::: 

::: {.callout-note collapse="true"}
來源第 283 行；段落 476b42f9f92f6fab；UNKNOWN_INHERITED。

```text
这些是线上博彩最值得吸收的“安全关键系统思维”。

```
::: 

::: {.callout-note collapse="true"}
來源第 287 行；段落 0010333257831160；UNKNOWN_INHERITED。

```text
# 7. 目标架构：Gaming Decision Intelligence OS

```
::: 

::: {.callout-note collapse="true"}
來源第 289 行；段落 fa9532f76e538ab1；UNKNOWN_INHERITED。

````text
```text
L0  Source
    Live Casino / Sports / Lottery / Account / Payment / Bonus / Agent / RG
        ↓
L1  Immutable Event Ledger
    event_id, event_time, ingest_time, schema_version, source, checksum
        ↓
L2  Data Quality + Point-in-Time Layer
    contract / dedup / late event / reconciliation / lineage
        ↓
L3  Feature & Entity Layer
    player, device, account, agent, table, dealer, payment, event, graph
        ↓
L4  Detection / Prediction
    rules + GLM + GBDT + survival/HMM + graph + sequence model
        ↓
L5  registry_risk_topology
    entity × risk × time × probability × severity × confidence × evidence
        ↓
L6  Constrained Decision Engine
    eligibility + policy + expected incremental value + RG/AML hard veto
        ↓
L7  Case Management / Human Review
    evidence timeline + reason codes + model version + appeal + rollback
        ↓
L8  Action
    observe / ask / verify / hold-for-review / limit / RG interaction
        ↓
L9  Outcome Ledger
    D+1 / D+7 / D+30 / confirmed fraud / complaints / RG outcomes / cost
        ↓
L10 Causal Evaluation + Monitoring
    A/B, CUPED, switchback, DR/uplift, calibration, drift, fairness, SLO
```

````
::: 

::: {.callout-note collapse="true"}
來源第 324 行；段落 bded32b649b2d33d；UNKNOWN_INHERITED。

```text
## 7.1 `registry_risk_topology` 的建议正式 schema

```
::: 

::: {.callout-note collapse="true"}
來源第 326 行；段落 5101693f2ef4301f；UNKNOWN_INHERITED。

````text
```text
as_of_time
entity_type
entity_id
risk_taxonomy
risk_subtype
model_id
model_version
rule_version
probability
calibrated_probability
severity
confidence
evidence_count
evidence_refs
first_seen
last_seen
trend
uncertainty
eligibility
recommended_action
human_review_required
decision_status
appeal_status
rollback_flag
outcome_status
```

````
::: 

::: {.callout-note collapse="true"}
來源第 354 行；段落 de01a3cfa39e0fa9；UNKNOWN_INHERITED。

```text
这比“15 张风险名单”成熟，因为它保留时间、概率、严重度、不确定度、证据与处置状态。

```
::: 

::: {.callout-note collapse="true"}
來源第 358 行；段落 c217e263baf54bcd；UNKNOWN_INHERITED。

```text
# 8. 模型体系：从 baseline 到 Transformer，而不是反过来

```
::: 

::: {.callout-note collapse="true"}
來源第 360 行；段落 9f96f98c9e578e6f；UNKNOWN_INHERITED。

```text
## 8.1 Challenger ladder

```
::: 

::: {.callout-note collapse="true"}
來源第 362 行；段落 e6fe5bafa5f25459；UNKNOWN_INHERITED。

```text
1. **规则 / 统计基线**：rate、Wilson interval、EWMA、GLM / scorecard。
2. **GBDT**：XGBoost / LightGBM / CatBoost。
3. **Survival / competing risks**：预测“何时发生”而非只问会不会。
4. **HMM / state-space**：识别“正常→加速→风险”状态。
5. **Graph / entity resolution**：多账户、设备、支付、代理、同桌网络。
6. **Sequence / Transformer**：只有当长序列带来稳定 OOT 增益才上。
7. **Contextual bandit / RL**：只在动作可控、reward 合规、OPE 通过、因果基础可靠后小流量运行。

```
::: 

::: {.callout-note collapse="true"}
來源第 370 行；段落 0a444dabb1a79189；UNKNOWN_INHERITED。

```text
## 8.2 统一验收协议

```
::: 

::: {.callout-note collapse="true"}
來源第 372 行；段落 7ece7ec9b0dd7c96；UNKNOWN_INHERITED。

```text
### 时间切分

```
::: 

::: {.callout-note collapse="true"}
來源第 374 行；段落 86ca81b621901bb7；UNKNOWN_INHERITED。

```text
- rolling / expanding walk-forward；
- purge + embargo；
- 所有 feature 必须 `feature_time <= as_of_time`；
- 禁止随机 train/test split 作为时序系统最终证据。

```
::: 

::: {.callout-note collapse="true"}
來源第 379 行；段落 c49a46b256d4ea7d；UNKNOWN_INHERITED。

```text
### 预测质量

```
::: 

::: {.callout-note collapse="true"}
來源第 381 行；段落 d4c97ef8d4387ff3；UNKNOWN_INHERITED。

```text
- PR-AUC（类不平衡优先）；
- ROC-AUC（辅助）；
- Brier score；
- ECE / reliability curve；
- Precision@人工产能；
- Recall at false-positive budget；
- cost-weighted utility；
- drift / stability。

```
::: 

::: {.callout-note collapse="true"}
來源第 390 行；段落 95129d63d772bb89；UNKNOWN_INHERITED。

```text
### 时序预测

```
::: 

::: {.callout-note collapse="true"}
來源第 392 行；段落 5154ec2a4ed37b0a；UNKNOWN_INHERITED。

```text
- MASE / RMSSE；
- probabilistic forecast 用 CRPS / pinball loss；
- 不能只用 MAE 比不同量纲。

```
::: 

::: {.callout-note collapse="true"}
來源第 396 行；段落 c2a04683da42599a；UNKNOWN_INHERITED。

```text
### 决策质量

```
::: 

::: {.callout-note collapse="true"}
來源第 398 行；段落 38a09f76dfec3777；UNKNOWN_INHERITED。

```text
- confirmed loss avoided；
- false-positive cost；
- case closure time；
- reviews per analyst-day；
- appeal overturn rate；
- rollback rate。

```
::: 

::: {.callout-note collapse="true"}
來源第 405 行；段落 2a08e43abde2efc7；UNKNOWN_INHERITED。

```text
### 因果效果

```
::: 

::: {.callout-note collapse="true"}
來源第 407 行；段落 eb073d6c0ed0bbb1；UNKNOWN_INHERITED。

```text
- ATE / CATE；
- CUPED；
- switchback；
- doubly robust；
- negative control；
- sensitivity / E-value。

```
::: 

::: {.callout-note collapse="true"}
來源第 416 行；段落 320c39f2d3ea9979；UNKNOWN_INHERITED。

```text
# 9. 三类价值：止损、增效、合规必须拆账

```
::: 

::: {.callout-note collapse="true"}
來源第 418 行；段落 85b3350ab0c0f09f；UNKNOWN_INHERITED。

```text
## 9.1 止损账

```
::: 

::: {.callout-note collapse="true"}
來源第 420 行；段落 bdf4ba48e18ee9d5；UNKNOWN_INHERITED。

````text
```text
Confirmed Avoided Loss
- False Positive Cost
- Review Cost
- Vendor/Infra Cost
= Net Loss Prevention Value
```

````
::: 

::: {.callout-note collapse="true"}
來源第 428 行；段落 615e3b6b5abf1b5c；UNKNOWN_INHERITED。

```text
禁止把“限制正常玩家导致少派彩”记为止损。

```
::: 

::: {.callout-note collapse="true"}
來源第 430 行；段落 5079ad02306c204a；UNKNOWN_INHERITED。

```text
## 9.2 增效账

```
::: 

::: {.callout-note collapse="true"}
來源第 432 行；段落 fb8f718ca5794388；UNKNOWN_INHERITED。

```text
衡量：

```
::: 

::: {.callout-note collapse="true"}
來源第 434 行；段落 ab5fe1ada0b86e35；UNKNOWN_INHERITED。

```text
- analyst cases/day；
- evidence automation coverage；
- median / p95 case cycle time；
- data pipeline run time；
- reconciliation exception time；
- model deployment lead time；
- customer-service deflection（仅低风险事务）。

```
::: 

::: {.callout-note collapse="true"}
來源第 442 行；段落 721c951c57afddfe；UNKNOWN_INHERITED。

```text
## 9.3 合规账

```
::: 

::: {.callout-note collapse="true"}
來源第 444 行；段落 c0594e7ec0404c29；UNKNOWN_INHERITED。

```text
合规不是利润权重，而是 **constraint / veto**：

```
::: 

::: {.callout-note collapse="true"}
來源第 446 行；段落 a9734ca9962084bf；UNKNOWN_INHERITED。

````text
```text
maximize Expected(legitimate economic value + loss prevention)
subject to:
  RG_status ∉ prohibited_marketing_states
  KYC_pass = TRUE
  AML_constraints = PASS
  jurisdiction = allowed
  game_integrity = intact
  human_review = required_for_high_impact
```

````
::: 

::: {.callout-note collapse="true"}
來源第 457 行；段落 896fc18e23171d92；UNKNOWN_INHERITED。

```text
关键 KPI：

```
::: 

::: {.callout-note collapse="true"}
來源第 459 行；段落 27f73ef320f064ec；UNKNOWN_INHERITED。

```text
- strong-risk response latency；
- manual-review coverage；
- decision-reason completeness；
- appeal turnaround；
- data-access violations；
- RG→marketing leakage = 0；
- model/document audit completeness。

```
::: 

::: {.callout-note collapse="true"}
來源第 469 行；段落 dc69b74ef78d5158；UNKNOWN_INHERITED。

```text
# 10. RedTeam：真正要攻击的是自己的假设

```
::: 

::: {.callout-note collapse="true"}
來源第 471 行；段落 ecf93752d518341b；UNKNOWN_INHERITED。

```text
1. **AI-washing**：规则引擎、推荐、自动化脚本被包装为“RL”。
2. **来源污染**：SEO/affiliate 文当公司官方资料。
3. **时间泄漏**：训练用了未来事件或干预后的信息。
4. **标签偏差**：被抓到的作弊者 ≠ 全部作弊者；未标注 ≠ 正常。
5. **处置反馈偏差**：封禁后行为不可观察，形成 censoring / selection bias。
6. **图谱误合并**：共享 IP / VPN / 家庭设备造成团伙误判。
7. **数据投毒**：机器人产生低价值噪声干扰基线。
8. **Bot / automation**：异常节奏、代理、设备伪装。
9. **优势玩法 / 延迟套利**：尤其体育赔率与特定边注。
10. **模型漂移**：活动、地区、产品、季节改变分布。
11. **供应商锁定**：核心标签、特征、案件证据不能导出。
12. **黑箱高影响动作**：账户/提款限制无原因码、不可申诉。
13. **奖励优化反噬**：模型学会利用损失后脆弱时点刺激继续投注。
14. **QoE 失真**：直播 A/V 不同步、丢帧、settlement delay 被误解为操纵。
15. **不可比较 KPI**：跨年份、跨产品、跨 B2B/B2C 分母混用。
16. **过度工程**：FPGA、GNN、Transformer、RL 同时上线，无法归因。
17. **灾难降级失败**：模型服务不可用导致核心投注/结算阻塞。
18. **依赖链风险**：模型包、浏览器 SDK、第三方 KYC/CRM 的供应链漏洞。

```
::: 

::: {.callout-note collapse="true"}
來源第 492 行；段落 1db134c82ff96aa7；UNKNOWN_INHERITED。

```text
# 11. Critic：附件里最需要继续收紧的地方

```
::: 

::: {.callout-note collapse="true"}
來源第 494 行；段落 e9426fa69daef19b；UNKNOWN_INHERITED。

```text
- “AI 已深度嵌入所有顶级平台”不应作为统一事实；应按公司/产品逐项证明。
- “RL 已用于奖励优化”不能从第三方博客升级成工业标准；需直接产品文档、模型说明、线上实验或审计证据。
- “亚洲供应商没有披露”只代表 **UNKNOWN**，不代表“没有使用”。
- “准确率 75.94%”“检出率 ≥87%”“10× engagement”等厂商数字，没有样本/阈值/基线就不能跨公司排名。
- “AI Dealer = 降本”忽视监管、信任、渲染、品牌、人力监督与内容成本。
- “体育/赌场/彩票同一套模型”是错误：可共用平台层，但定价、完整性、风险与监管对象不同。
- 宇航/军工技术只应迁移**工程方法论**；不要把昂贵专用技术当作先进性的象征。

```
::: 

::: {.callout-note collapse="true"}
來源第 504 行；段落 5061cf92c8d7d289；UNKNOWN_INHERITED。

```text
# 12. KillCritic：任何一条突破，都应阻止上线

```
::: 

::: {.callout-note collapse="true"}
來源第 506 行；段落 49ffe04fd0a834bf；UNKNOWN_INHERITED。

```text
- 禁止个体化操纵 RNG / 牌局结果 / 派彩。
- 禁止用 RG 风险分数营销、催存、返利、VIP 升级。
- 禁止 RL reward = GGR / NGR / deposit / bet volume / time-on-game。
- 禁止仅凭黑箱模型自动冻结提款、封号或指控舞弊。
- 禁止只报 AUC、不报 calibration、precision@capacity、误伤成本。
- 禁止把玩家历史 road/streak 描述成能保证百家乐未来结果。
- 禁止未经授权对竞争平台做渗透、绕过、自动下注或漏洞利用。
- 禁止生产数据未经批准送入外部 AI。
- 禁止无 rollback / appeal / audit 的高影响自动化。
- 禁止把 P2/P3 营销资料写成“官方已部署”。

```
::: 

::: {.callout-note collapse="true"}
來源第 519 行；段落 a60bef7fd9d5c826；UNKNOWN_INHERITED。

```text
# 13. Blindspot：真正可能决定成败的九个盲区

```
::: 

::: {.callout-note collapse="true"}
來源第 521 行；段落 39a4fa1b95edadac；UNKNOWN_INHERITED。

```text
1. **Label governance**：谁能定义“欺诈/串通/伤害/正常”？
2. **Economic anchor**：每类产品的理论收益、成本、责任准备金、bonus cost 是否统一？
3. **Intervention bias**：动作改变了后续数据，模型怎么区分“预测准”还是“动作有效”？
4. **Cross-product identity**：赌场、体育、彩票是不是同一自然人/钱包/设备？
5. **Jurisdiction policy**：同一动作在不同牌照地是否允许？
6. **Responsible-gambling firewall**：技术上能否证明 RG 数据没有进入营销？
7. **Vendor model risk**：供应商不给训练数据/逻辑，如何独立验证？
8. **Tail latency / replay**：故障时能否完整重建下注、视频、赔率/牌局与处置时间线？
9. **Unit economics**：模型提升是否覆盖人力、云、供应商与误伤成本？

```
::: 

::: {.callout-note collapse="true"}
來源第 533 行；段落 d8610d7b1bdda011；UNKNOWN_INHERITED。

```text
# 14. ActionPlan：可执行路线图

```
::: 

::: {.callout-note collapse="true"}
來源第 535 行；段落 b665a72c9d8b9715；UNKNOWN_INHERITED。

```text
## Phase 0：0–30 天——证据与治理先行

```
::: 

::: {.callout-note collapse="true"}
來源第 537 行；段落 a360493d8bcebc7e；UNKNOWN_INHERITED。

```text
不接生产博彩站、不接现行禁用的 Superset / DolphinScheduler / StarRocks；只使用批准的离线快照、脱敏/模拟数据与测试线。

```
::: 

::: {.callout-note collapse="true"}
來源第 539 行；段落 fd3fb88eb8fd8674；UNKNOWN_INHERITED。

```text
交付物：

```
::: 

::: {.callout-note collapse="true"}
來源第 541 行；段落 ce5a87de3f9fb335；UNKNOWN_INHERITED。

```text
- Entity / Product / Jurisdiction register。
- 统一 Data Dictionary + data contract。
- 统一 Risk Taxonomy。
- AI / model inventory。
- 证据等级表与 conflict ledger。
- RG / AML / Fraud / Marketing 数据权限矩阵。
- KPI 字典与分母定义。
- 版本、依赖、SBOM、模型卡模板。

```
::: 

::: {.callout-note collapse="true"}
來源第 550 行；段落 68bff374233938fe；UNKNOWN_INHERITED。

```text
Gate：任何指标都能回答“谁、何时、什么数据、什么版本、什么分母”。

```
::: 

::: {.callout-note collapse="true"}
來源第 552 行；段落 19307e46376da02b；UNKNOWN_INHERITED。

```text
## Phase 1：30–90 天——离线基线与数据质量

```
::: 

::: {.callout-note collapse="true"}
來源第 554 行；段落 a6a5f335e441254c；UNKNOWN_INHERITED。

```text
技术：

```
::: 

::: {.callout-note collapse="true"}
來源第 556 行；段落 bb7082a5d21ec410；UNKNOWN_INHERITED。

```text
- Parquet + DuckDB/Arrow/Polars 本地研究；
- `targets` / Snakemake 生成可重放 DAG；
- schema / missing / duplicate / reconciliation Gates；
- baseline GLM/scorecard + GBDT；
- entity resolution / graph；
- calibration；
- rolling walk-forward。

```
::: 

::: {.callout-note collapse="true"}
來源第 564 行；段落 4a887dc12d46a81b；UNKNOWN_INHERITED。

```text
Gate：

```
::: 

::: {.callout-note collapse="true"}
來源第 566 行；段落 76c828d6c5d0d174；UNKNOWN_INHERITED。

```text
- leakage test = PASS；
- reconciliation = PASS；
- reproducibility = PASS；
- model beats baseline out-of-time；
- false-positive budget 明确。

```
::: 

::: {.callout-note collapse="true"}
來源第 572 行；段落 7d2b6fbb523b289c；UNKNOWN_INHERITED。

```text
## Phase 2：3–6 个月——测试线实时化

```
::: 

::: {.callout-note collapse="true"}
來源第 574 行；段落 5cf851a996457eee；UNKNOWN_INHERITED。

```text
在正式授权的**测试专用服务器**：

```
::: 

::: {.callout-note collapse="true"}
來源第 576 行；段落 8c2d6e4e986d2315；UNKNOWN_INHERITED。

```text
- event bus；
- point-in-time feature layer；
- rule + ML rank；
- case management；
- reason code / SHAP；
- human review / appeal / rollback；
- SLO、backpressure、graceful degradation；
- synthetic-load test。

```
::: 

::: {.callout-note collapse="true"}
來源第 587 行；段落 d314e137316c9df5；UNKNOWN_INHERITED。

```text
- p99.9 latency 达标；
- peak load 不丢事件；
- model outage 可自动退规则；
- rule outage 可退人工；
- high-impact 100% 可审计。

```
::: 

::: {.callout-note collapse="true"}
來源第 593 行；段落 3e9385ef110619fc；UNKNOWN_INHERITED。

```text
## Phase 3：6–12 个月——效果评估与三产品线

```
::: 

::: {.callout-note collapse="true"}
來源第 595 行；段落 4ae23de792078b30；UNKNOWN_INHERITED。

```text
### 百家樂
Dealer/Table/Player/Agent/Payment/Bonus/RG 分管线，建立风险拓扑与 outcome ledger。

```
::: 

::: {.callout-note collapse="true"}
來源第 598 行；段落 bfc2aab0e46cc63e；UNKNOWN_INHERITED。

```text
### 体育
接入合法 official data / odds sandbox，构建 pricing-risk-integrity 三层，不直接复用百家乐模型。

```
::: 

::: {.callout-note collapse="true"}
來源第 601 行；段落 a518810d03af8e72；UNKNOWN_INHERITED。

```text
### 彩票
构建 ticket/draw/retail/PAM/wallet/CRM/RG 一体化原型，学习 Scientific Games / Brightstar 的 omnichannel 结构。

```
::: 

::: {.callout-note collapse="true"}
來源第 604 行；段落 43a7da2b9eb53c0c；UNKNOWN_INHERITED。

```text
Gate：所有干预都有 counterfactual / control 或合理准实验设计。

```
::: 

::: {.callout-note collapse="true"}
來源第 606 行；段落 23354c2483dcd514；UNKNOWN_INHERITED。

```text
## Phase 4：12–24 个月——受控智能决策

```
::: 

::: {.callout-note collapse="true"}
來源第 608 行；段落 df656e814ca9ddd1；UNKNOWN_INHERITED。

```text
- uplift / CATE；
- contextual bandit **offline OPE**；
- 保护性 action set；
- 小流量、可停止；
- AI Dealer / CV 等独立 Pilot；
- 独立 model validation / red-team / compliance sign-off。

```
::: 

::: {.callout-note collapse="true"}
來源第 615 行；段落 b1289ee374b45224；UNKNOWN_INHERITED。

```text
禁止直接跳到 autonomous RL。

```
::: 

::: {.callout-note collapse="true"}
來源第 619 行；段落 9b4dfa06980fd3de；UNKNOWN_INHERITED。

```text
# 15. “完美真人”目标产品蓝图

```
::: 

::: {.callout-note collapse="true"}
來源第 621 行；段落 c56a1da0b8697f53；UNKNOWN_INHERITED。

```text
不是“复制 Evolution”，而是组合各类标杆的最强项：

```
::: 

::: {.callout-note collapse="true"}
來源第 623 行；段落 d86b961c2f786f0c；UNKNOWN_INHERITED。

```text
- **Evolution**：Live Studio / QoE / 产品工程。
- **Playtech**：PAM + Live + safer gambling + managed-service governance。
- **Pragmatic**：内容速度 / UI / mobile productization。
- **SOFTSWISS / EveryMatrix**：反欺诈 / Bonus abuse / case-oriented operations。
- **Optimove / Smartico / Future Anthem**：CRM / experimentation / recommendation，但套 RG firewall。
- **Genius Sports / Sportradar / Kambi**：体育 official data + pricing + liability + integrity。
- **Scientific Games / Brightstar / Allwyn / FDJ UNITED**：彩票中央系统、零售数字融合、PAM/wallet、Responsible Play。
- **银行 SR 26-2**：model inventory / independent validation / vendor model governance。
- **金融量化**：time-aware validation / tail latency / stress testing。
- **SRE**：SLO / lineage / data contract / graceful degradation。
- **资安**：Detection-as-Code / zero trust / UEBA / bot & graph intelligence。
- **科学研究**：preregistration / causal inference / negative controls / reproducibility。
- **宇航/安全关键系统**：FDIR / replay / FMEA / deterministic fallback。
- **供应链安全**：SBOM / SLSA / signed artifacts。

```
::: 

::: {.callout-note collapse="true"}
來源第 638 行；段落 e6226ac4bcdfa378；UNKNOWN_INHERITED。

```text
最终产品不是“AI casino”，而是：

```
::: 

::: {.callout-note collapse="true"}
來源第 640 行；段落 fbbfb6f256981bce；UNKNOWN_INHERITED。

```text
> **可证明、可回放、可审计、可申诉、可降级、可量化增量价值的博彩决策智能平台。**

```
::: 

::: {.callout-note collapse="true"}
來源第 644 行；段落 b593afe1bd18cda1；UNKNOWN_INHERITED。

```text
# 16. 采购与技术尽调问卷（必须逐厂商回答）

```
::: 

::: {.callout-note collapse="true"}
來源第 646 行；段落 5f535f201a69dace；UNKNOWN_INHERITED。

```text
每个供应商至少回答：

```
::: 

::: {.callout-note collapse="true"}
來源第 648 行；段落 35cb88f1ccd55739；UNKNOWN_INHERITED。

```text
1. 这是 rule、supervised ML、deep learning、bandit 还是 RL？
2. 当前 production version 是什么？
3. training / validation time window？
4. 标签来自人工确认、chargeback、KYC、投诉还是代理规则？
5. false-positive / false-negative 如何定义？
6. 是否做 calibration？
7. 是否做 OOT / rolling validation？
8. 是否提供 model card？
9. 是否可导出 raw reason codes / evidence？
10. 是否支持人工 override？
11. override 是否进入模型反馈？
12. 高影响动作是否可申诉/回滚？
13. 数据保存与数据驻留在哪里？
14. 是否使用客户数据训练跨客户模型？
15. third-party subprocessors？
16. 数据跨境机制？
17. disaster recovery RTO/RPO？
18. p95/p99/p99.9 latency？
19. throughput / backpressure 机制？
20. feature outage / model outage 如何降级？
21. regulatory certifications / game certifications？
22. RNG/game result 是否与 AI 表现层强制隔离？
23. RG 数据能否技术上阻止流向营销？
24. audit log 是否 immutable / signed？
25. contract termination 后模型、标签、案件证据能否完整导出？

```
::: 

::: {.callout-note collapse="true"}
來源第 676 行；段落 bf02c21e8da0cf15；UNKNOWN_INHERITED。

```text
# 17. 附件主体全量索引：博彩 / 风控 / AI

```
::: 

::: {.callout-note collapse="true"}
來源第 678 行；段落 dae41b0451a4c41c；UNKNOWN_INHERITED。

```text
以下保留附件《移植总表》编号 1–70，不因本次外部核实而删除；证据不足者继续标记 UNKNOWN/P2，而不是填补。

```
::: 

::: {.callout-note collapse="true"}
來源第 680 行；段落 bbfe948c4b0d9c37；UNKNOWN_INHERITED。

```text
**A. Live / Casino（1–16）**  
Evolution；Ezugi；Playtech；Pragmatic Play Live；SA Gaming；Dream Gaming (DG)；WM Casino / WM Perfect Group；Asia Gaming (AG)；AllBet；Sexy Baccarat / AE Sexy；Pretty Gaming；Venus Casino；Big Gaming；eBet；BetGames.TV；KingMaker。

```
::: 

::: {.callout-note collapse="true"}
來源第 683 行；段落 930aefd6ffa1a8b2；UNKNOWN_INHERITED。

```text
**B. B2C / Operators（17–29）**  
Entain；Flutter Entertainment；FanDuel；PokerStars；Sportsbet；Betfair；Kindred Group（现应放在 FDJ UNITED 历史/子品牌语境）；Unibet；BetMGM；DraftKings；Sisal；Stardust；OPAP。

```
::: 

::: {.callout-note collapse="true"}
來源第 686 行；段落 010f9afb03c6f1d1；UNKNOWN_INHERITED。

```text
**C. B2B / PAM / CRM（30–35）**  
SOFTSWISS；EveryMatrix；Smartico；Optimove；GiG；NuxGame。

```
::: 

::: {.callout-note collapse="true"}
來源第 689 行；段落 55512156b4ba2c36；UNKNOWN_INHERITED。

```text
**D. Fraud / KYC / AML / Customer Ops（36–57）**  
Featurespace ARIC；SEON；GeoComply；Sumsub；Onfido；Jumio；Veriff；iDenfy；Shufti；CrossClassify；Sift；Group-IB；cside；Flagright；ComplyAdvantage；NICE Actimize；ACT / Fraud Rings；Infocredit Group / ComplianceSuite.ai；Cevro AI；InteractiveAI；Moveo.AI；Quantexa。

```
::: 

::: {.callout-note collapse="true"}
來源第 692 行；段落 74529b7552668c4d；UNKNOWN_INHERITED。

```text
**E. Responsible Gambling（58–60 + cross-products）**  
Mindway AI（GameScanner / Gamalyze）；Neccton（Mentor）；Sportradar（Bettor Sense）；Playtech BetBuddy；Entain ARC；FDJ UNITED / legacy Kindred PS-EDS。

```
::: 

::: {.callout-note collapse="true"}
來源第 695 行；段落 b18df02ea80429a2；UNKNOWN_INHERITED。

```text
**F. AI Dealer（61–62）**  
Octane Studios；Sentient Studios（BetHog lineage）。

```
::: 

::: {.callout-note collapse="true"}
來源第 698 行；段落 4a249d6901e009e3；UNKNOWN_INHERITED。

```text
**G. Smart Table（63–64）**  
Angel Group；IDX Games。

```
::: 

::: {.callout-note collapse="true"}
來源第 701 行；段落 e37aba087bfae6d2；UNKNOWN_INHERITED。

```text
**H. Player-side / adversarial tools & research（65–70）**  
FPLAY；Mysports.AI；Oracle Baccarat Predictor；BACC.BOT；BaccaratAI；Differential Labs。

```
::: 

::: {.callout-note collapse="true"}
來源第 706 行；段落 7fa8285349c6c2ef；UNKNOWN_INHERITED。

```text
# 18. 附件扩展提及主体：继续保留但分层核实

```
::: 

::: {.callout-note collapse="true"}
來源第 708 行；段落 cc718911e08a9bc3；UNKNOWN_INHERITED。

```text
`Inteligent_egaming_platform_ref_v000.000.001.qmd` 还明确提及或纳入对标池的主体包括：

```
::: 

::: {.callout-note collapse="true"}
來源第 710 行；段落 ea986c0bb0085cbb；UNKNOWN_INHERITED。

```text
- BetConstruct AI
- Winfinity
- Sentient Gaming Group
- Arb Labs / ChipVue
- Avanti Studios
- HENGPLAY
- Future Anthem
- bet365
- 888.com
- Golden Matrix Group
- SCCG Management
- CleverBet Labs
- Track360
- Rivalry

```
::: 

::: {.callout-note collapse="true"}
來源第 725 行；段落 e2027e6b7f66b49f；UNKNOWN_INHERITED。

```text
这些主体在本白皮书中不自动继承附件内所有能力宣称；正式采购/论文引用前必须按 P0/P1 重新验证。

```
::: 

::: {.callout-note collapse="true"}
來源第 727 行；段落 7acf8f6d87ddb3d8；UNKNOWN_INHERITED。

```text
本次为补足“体育 / 彩票”加入的当前关键基准：

```
::: 

::: {.callout-note collapse="true"}
來源第 729 行；段落 2a41f2a57ffd8d10；UNKNOWN_INHERITED。

```text
- Genius Sports / GeniusIQ
- Sportradar
- Kambi
- Scientific Games
- Brightstar Lottery
- Allwyn
- FDJ UNITED

```
::: 

::: {.callout-note collapse="true"}
來源第 739 行；段落 0686be43d92cdfe9；UNKNOWN_INHERITED。

```text
# 19. 跨行业主体索引：只作为方法论与工程对标

```
::: 

::: {.callout-note collapse="true"}
來源第 741 行；段落 897483fbed65cce6；UNKNOWN_INHERITED。

```text
附件宇航与跨行业章节明确提及的代表主体包括：

```
::: 

::: {.callout-note collapse="true"}
來源第 743 行；段落 6dad8df7fc3e5cef；UNKNOWN_INHERITED。

```text
- SpaceX、Blue Origin、Rocket Lab、Airbus、Boeing、Lockheed Martin、Anduril、Thales、Eutelsat
- Palantir、C3 AI、Oracle、BAE Systems、ST Engineering
- Snowflake、Databricks、SAP、Microsoft、AWS、Google
- NVIDIA、TSMC
- CrowdStrike、Palo Alto
- Citadel、Jane Street、Two Sigma
- NASA / US Space Force 等公共机构与生态

```
::: 

::: {.callout-note collapse="true"}
來源第 751 行；段落 a2b35f289184067a；UNKNOWN_INHERITED。

```text
使用原则：**迁移数据完整性、低延迟、可回放、模型治理、容灾、供应链与实验方法，不把军工/宇航专用系统的高成本实现照搬到博彩。**

```
::: 

::: {.callout-note collapse="true"}
來源第 755 行；段落 ab1d489749f4d2d3；UNKNOWN_INHERITED。

```text
# 20. 参考标准与公开校正来源

```
::: 

::: {.callout-note collapse="true"}
來源第 757 行；段落 a9541acf2b433977；UNKNOWN_INHERITED。

```text
## 监管 / 标准

```
::: 

::: {.callout-note collapse="true"}
來源第 759 行；段落 8ba733df8332fb0c；UNKNOWN_INHERITED。

```text
- Malta Gaming Authority, *AI Gaming Charter*, 2026-09-18  
  https://www.mga.org.mt/mga-launches-ai-gaming-charter-following-extensive-industry-collaboration/
- UK Gambling Commission, LCCP 3.4.3 Remote customer interaction  
  https://www.gamblingcommission.gov.uk/licensees-and-businesses/lccp/condition/3-4-3-remote-customer-interaction
- EU AI Act, Regulation (EU) 2024/1689 / consolidated text  
  https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689
- European Commission, Article 50 transparency guidelines, 2026  
  https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems
- Federal Reserve, SR 26-2 Revised Guidance on Model Risk Management, 2026-04-17  
  https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm
- NIST AI RMF / Generative AI Profile  
  https://www.nist.gov/itl/ai-risk-management-framework

```
::: 

::: {.callout-note collapse="true"}
來源第 772 行；段落 f7c1e16376909856；UNKNOWN_INHERITED。

```text
## Casino / Platform

```
::: 

::: {.callout-note collapse="true"}
來源第 774 行；段落 becc846d338c8e92；UNKNOWN_INHERITED。

```text
- Evolution Annual Report 2025  
  https://www.evolution.com/investors/financial-publications/reports
- Playtech Annual Report 2025  
  https://www.investors.playtech.com/annual-reports
- EveryMatrix Bonus Guardian  
  https://everymatrix.com/bonus-guardian/
- SOFTSWISS Anti-Fraud 2025  
  https://www.softswiss.com/news/softswiss-helps-operators-save-15m-in-2025/
- Optimove / Smartico acquisition announcement  
  https://www.globenewswire.com/news-release/2026/04/06/3268555/0/en/optimove-to-acquire-smartico.html
- FDJ UNITED proactive intervention / PS-EDS lineage  
  https://www.fdjunited.com/proactive-intervention/

```
::: 

::: {.callout-note collapse="true"}
來源第 787 行；段落 ac8a90ad17d94a17；UNKNOWN_INHERITED。

```text
## Sports

```
::: 

::: {.callout-note collapse="true"}
來源第 789 行；段落 994955bf06bfaf3b；UNKNOWN_INHERITED。

```text
- Genius Sports 2025 Form 20-F  
  https://www.sec.gov/Archives/edgar/data/1834489/000119312526110749/geni-20251231.htm
- Sportradar 2025 Form 20-F  
  https://www.sec.gov/Archives/edgar/data/1836470/000110465926035485/srad-20251231x20f.htm
- Kambi Annual Report 2025  
  https://www.kambi.com/annualreport2025/

```
::: 

::: {.callout-note collapse="true"}
來源第 796 行；段落 57c95b9fe7625b18；UNKNOWN_INHERITED。

```text
## Lottery

```
::: 

::: {.callout-note collapse="true"}
來源第 798 行；段落 95156bc4777928e7；UNKNOWN_INHERITED。

```text
- Scientific Games Momentum / Arizona 2026  
  https://www.scientificgames.com/news/media-releases/all-systems-go-scientific-games-launches-new-advanced-technology-for-arizona-lottery/
- Delaware Lottery + Scientific Games iLottery / SG PAM, 2026  
  https://www.delottery.com/Media-Center/Press-Releases/2026/01/15
- Brightstar Lottery 2025 Form 20-F  
  https://www.sec.gov/Archives/edgar/data/1619762/000162828026011083/igt-20251231.htm
- Allwyn Annual Report 2025  
  https://www.allwyn.com/report/2025
- FDJ UNITED corporate transition / Kindred integration  
  https://www.fdjunited.com/presse/fdj-becomes-a-european-group-and-changes-its-name-to-fdj-united/

```
::: 

::: {.callout-note collapse="true"}
來源第 811 行；段落 cecd615678ef81c2；UNKNOWN_INHERITED。

```text
# 21. 最终裁定

```
::: 

::: {.callout-note collapse="true"}
來源第 813 行；段落 f678bfee3bcb0d41；UNKNOWN_INHERITED。

```text
若目标是让“完美真人”长期追赶甚至在部分层面超越世界级平台，最不应该做的是一次性堆叠 Transformer、GNN、RL、FPGA、LLM Agent。

```
::: 

::: {.callout-note collapse="true"}
來源第 815 行；段落 06311664677e6ac6；UNKNOWN_INHERITED。

```text
最高优先级应是：

```
::: 

::: {.callout-note collapse="true"}
來源第 817 行；段落 68af8644a503a538；UNKNOWN_INHERITED。

```text
1. **Evidence Registry**：所有竞争情报可追溯。
2. **Canonical Event Ledger**：赌场、体育、彩票统一事件语义。
3. **Point-in-Time correctness**：堵住时间泄漏。
4. **`registry_risk_topology`**：从名单升级为概率化、时间化、证据化风险拓扑。
5. **Case + Human Review + Appeal + Rollback**。
6. **Outcome Ledger + causal evaluation**：证明每个动作有没有增量价值。
7. **RG firewall**：风险保护与营销真正隔离。
8. **Model Risk Management**：基线、挑战者、独立验证、漂移、退役。
9. **SLO / replay / graceful degradation**：把博彩平台当高可靠实时系统管理。
10. **最后才是 RL / autonomous agent**，而且只在受约束、可审计、保护性目标下使用。

```
::: 

::: {.callout-note collapse="true"}
來源第 828 行；段落 8ce8b139f754c708；UNKNOWN_INHERITED。

```text
这十项比“拥有最多 AI 模型”更接近真正的世界级平台能力。
```
::: 

### 來源：Reference/perfect-baccarat-report.md

[原始來源](<perfect-baccarat-report.md>)；SHA256：`3b1816fdbfec834fa413f5e32fe8fb7c28c4e28331072226c9a3948ea942bc33`。下列為未覆蓋段落；歷史主張未經收錄自動驗證。

::: {.callout-note collapse="true"}
來源第 1 行；段落 58e144af5f34c4fc；UNKNOWN_INHERITED。

```text
# 完美真人在线百家乐平台 自强追赶计划 - 附件QMD全量前沿公司与技术整合报告

```
::: 

::: {.callout-note collapse="true"}
來源第 3 行；段落 ff905bd524792e8a；UNKNOWN_INHERITED。

```text
## Executive Summary

```
::: 

::: {.callout-note collapse="true"}
來源第 5 行；段落 386edb02b6c26729；UNKNOWN_INHERITED。

```text
附件 `電腦已昇級至視窗11版（工欲善其事必先利其器）.qmd` 全量约20万字，聚合了 Claude / ChatGPT / Perplexity / Meta / Kimi / DeepSeek / Copilot / Grok / Gemini 九方对“顶级在线百家乐平台 AI/RL 自动化运营”的查证。其高度一致的结论是：顶级平台已将 AI 深度嵌入风控、反欺诈、AML、KYC、责任博彩、CRM 与视觉结算，但强化学习（RL）全面控制百家乐核心结果无可验证案例。

```
::: 

::: {.callout-note collapse="true"}
來源第 7 行；段落 d759afb6e71780c6；UNKNOWN_INHERITED。

```text
真正可追赶的路径是复制顶级平台的四层架构：实时流 + 规则引擎 + ML/图谱排序 + 人工高影响复核 + 不可变审计。本报告将附件中出现的所有公司与技术实体全部抽取、去重、交叉验证，并映射到止损、增效、合规三价值，提出可执行路线图。

```
::: 

::: {.callout-note collapse="true"}
來源第 9 行；段落 b4e054d5234e1d13；UNKNOWN_INHERITED。

```text
核心发现：
- 附件共提及 **58家** 前沿博彩/技术公司与 **63项** AI/数据技术
- 止损层商业标杆为 SOFTSWISS Anti-Fraud（2022年处理61,810请求，节省超1600万欧元）[[1]](https://www.softswiss.com/?p=46815)
- 增效层商业标杆为 Smartico（已被 Optimove 于2026年4月收购）[[2]](https://www.citybiz.co/article/828787/optimove-to-acquire-smartico-2/) 与 Sentient Studios / Octane Studios 的 AI 荷官首发百家乐[[3]](http://news.bettingstartups.com/p/octane-studios-ai-dealers-betting-gaming)
- 合规层监管框架为 MGA 与 MDIA 于2026年9月18日发布的自愿性 AI Gaming Charter，48页，无新增法律义务[[4]](https://www.mga.org.mt/mga-launches-ai-gaming-charter-following-extensive-industry-collaboration/) [[5]](https://europeangaming.eu/portal/latest-news/2026/09/22/214529/mga-mdia-ai-gaming-charter-launch/)

```
::: 

::: {.callout-note collapse="true"}
來源第 15 行；段落 2f552ce7eb8ffcdc；UNKNOWN_INHERITED。

```text
## 1. 全量前沿公司图谱（附件去重 58家）

```
::: 

::: {.callout-note collapse="true"}
來源第 17 行；段落 f40b39ef47f0e4e5；UNKNOWN_INHERITED。

```text
### 1.1 世界级 B2B 真人娱乐核心供应商

```
::: 

::: {.callout-note collapse="true"}
來源第 19 行；段落 953f491d0c1c1e84；UNKNOWN_INHERITED。

```text
| 公司 | 附件提及频次 | 可验证能力 | 对完美百家乐的复用点 |
|---|---|---|---|
| Evolution | 38 | AI监控、反作弊、异常投注检测、荷官质量监控，投入5000万欧元加码亚洲基础设施 | 60FPS YOLO读牌 + Flink 100ms派彩架构 |
| Playtech Live | 35 | 旗舰负责任博彩工具 BetBuddy，AI驱动行为监控与预测风险建模[[6]](https://www.playtech.com/services-2/)，2017年收购BetBuddy，集成 Featurespace ARIC 自适应欺诈检测[[7]](https://www.featurespace.com/newsroom/sks365-selects-featurespaces-adaptive-behavioural-analytics-to-predict-and-identify-fraudulent-activity/) | BetBuddy三层风险评级 + ARIC行为链揭示钱骡网络 |
| Pragmatic Play Live | 11 | Opti-X 集成20+推荐模型覆盖700+游戏，AI运营分析与生命周期管理 | 个性化大厅与奖金自动化 |
| Ezugi (Evolution旗下) | 3 | Ultimate Auto Roulette 全自动无荷官 | 去荷官自动化降低成本对照组 |

```
::: 

::: {.callout-note collapse="true"}
來源第 26 行；段落 02388ff6888420a1；UNKNOWN_INHERITED。

```text
### 1.2 亚洲真人百家乐巨头（WM生态重点）

```
::: 

::: {.callout-note collapse="true"}
來源第 28 行；段落 66b2dec2b6322403；UNKNOWN_INHERITED。

```text
| 公司 | 证据强度 | 附件描述 | 自强要点 |
|---|---|---|---|
| WM Casino / WM Perfect Group | 中 | Live Casino Provider + Streaming + Ecosystem，Dealer Anomaly / Player Risk / Live Casino Analytics，官方宣称 AI 与数据分析个性化推荐 | 玩家行为/荷官行为/桌台运营/代理层级/风控五维天然适合 XGBoost/HMM/Transformer |
| SA Gaming | 中低 | PAGCOR认证文件仅列桌台与边注，无AI白皮书 | 需自建风控替代第三方 |
| Dream Gaming | 中低 | 自称创新使用AI，Curaçao牌照，直播自泰国金冠赌场 | 同上 |
| AllBet / Asia Gaming / Sexy Baccarat / 188BET / 888.com | 低 | 路单自动化、边注、高 RTP宣传 | 代理营销站点多，无公开技术文档 |

```
::: 

::: {.callout-note collapse="true"}
來源第 35 行；段落 756afe1ba8fa1fe2；UNKNOWN_INHERITED。

```text
### 1.3 B2B 平台 / CRM / 运营自动化

```
::: 

::: {.callout-note collapse="true"}
來源第 37 行；段落 d42959ebb68d387d；UNKNOWN_INHERITED。

```text
| 公司 | 核心数据 |
|---|---|
| SOFTSWISS Casino Platform + BM3 | 2022年61,810请求节省16M+欧元，Q4较Q1近翻倍，70%为奖金滥用[[1]](https://www.softswiss.com/?p=46815) |
| EveryMatrix CasinoEngine / Bonus Guardian | 基于角色响应，ML训练已知滥用者历史 |
| Smartico | 31次提及，RL游戏化引擎自适应难度/时机/奖励，RNN预测7/14/30天流失准确率75.94%，2026年4月被Optimove收购[[2]](https://www.citybiz.co/article/828787/optimove-to-acquire-smartico-2/) [[8]](https://markets.financialcontent.com/lethbridgeherald/article/gnwcq-2026-4-6-optimove-to-acquire-smartico) |
| Optimove / Opti-X | 52% EGR Power 50运营商客户，Positionless Marketing |
| GiG | AI推荐引擎提升留存降低假阳性 |

```
::: 

::: {.callout-note collapse="true"}
來源第 45 行；段落 20cc78d954fbbec4；UNKNOWN_INHERITED。

```text
### 1.4 新兴 AI 荷官 - 2026年前台自动化新势力

```
::: 

::: {.callout-note collapse="true"}
來源第 47 行；段落 6f997dfdc695c947；UNKNOWN_INHERITED。

```text
| 公司 | 进展 |
|---|---|
| Sentient Studios (原 BetHog, FanDuel联创 Nigel Eccles) | 10M美元A轮[[9]](https://parameter.io/bethog-secures-10m-series-a-to-revolutionize-online-casino-gaming-with-ai-dealers/)，拟真AI荷官 Sunny，12语言，首发Blackjack 2025年10月，百家乐/轮盘计划2026年底，10倍于真人台参与度，BetHog于7月31日关闭专注B2B[[10]](https://news.bettingstartups.com/archive?page=-18) |
| Octane Studios | 可定制AI荷官平台，首发百家乐[[3]](http://news.bettingstartups.com/p/octane-studios-ai-dealers-betting-gaming)，品牌化、数日交付、 provably fair，RNG与渲染分离 |

```
::: 

::: {.callout-note collapse="true"}
來源第 52 行；段落 82f9905602d46420；UNKNOWN_INHERITED。

```text
关键架构共识：发牌结果由已认证 RNG 决定，AI仅负责拟真表达与互动，监管路径为RNG产品而非Live。

```
::: 

::: {.callout-note collapse="true"}
來源第 54 行；段落 c95fd618e85d65d7；UNKNOWN_INHERITED。

```text
### 1.5 实体智慧桌

```
::: 

::: {.callout-note collapse="true"}
來源第 56 行；段落 0125f358ca5ee3d2；UNKNOWN_INHERITED。

```text
| 公司 | 验证 |
|---|---|
| Angel Group | AI + RFID混合方案，姿态识别通过身体运动而非仅芯片数据识别下注[[11]](https://agbrief.com/news/macau/28/05/2026/smart-tables-open-new-frontier-in-patron-data-for-sands/) [[12]](https://agbrief.com/intel/deep-dive/21/05/2026/smart-gaming-tables-pose-recognition-takes-baccarat-to-a-different-level-angel-cto-says/)，已在澳门Sands China千张百家乐桌部署[[13]](https://focusgn.com/asia-pacific/angel-group-completes-implementation-of-baccarat-smart-tables-for-sands-china)，超越传统RFID提升数据品质与合规监控 |

```
::: 

::: {.callout-note collapse="true"}
來源第 60 行；段落 cfbef00587e9047e；UNKNOWN_INHERITED。

```text
### 1.6 B2C 营运商集团（AI治理标杆）

```
::: 

::: {.callout-note collapse="true"}
來源第 62 行；段落 0753fc8b0c412abd；UNKNOWN_INHERITED。

```text
| 集团 | AI应用 |
|---|---|
| Entain | ARC (Advanced Responsibility & Care)，26个保护标记，80%风险评估准确率[[14]](https://www.gamblinginsider.com/in-depth/15760/entain-makes-big-sustainability-strides-but-lags-on-gender-pay-gap)，Protector Model涵盖26标记[[15]](https://www.lse.co.uk/rns/ENT/entainsustain-esg-showcase-event-3qo7obdn2c9rwpg.html) |
| Flutter (FanDuel, PokerStars, Sportsbet) | Real Time Intervention, ML用于产品与基础设施，Responsible AI政策 |
| Kindred Group / Unibet | PS-EDS Player Safety Early Detection System |
| BetMGM / Stardust / Sisal / OPAP | Optimove客户案例，未来价值+36%、NGR+28%等 |

```
::: 

::: {.callout-note collapse="true"}
來源第 69 行；段落 b538d9057b046bdb；UNKNOWN_INHERITED。

```text
### 1.7 AI风控 / KYC / AML / 合规 / 客服 全量供应商

```
::: 

::: {.callout-note collapse="true"}
來源第 71 行；段落 1462f74385c25e69；UNKNOWN_INHERITED。

```text
- **行为欺诈/多账号/奖金滥用**：SEON, SOFTSWISS Anti-Fraud, ACT Fraud Rings (2026新增syndicate可视化), EveryMatrix Bonus Guardian, Sift, Group-IB, GeoComply (2亿+设备网络), cside (每会话250+浏览器信号识别OpenAI Operator等)
- **交易监控/AML**：Featurespace ARIC (Adaptive Behavioral Analytics，Betfair 2008年首创，Visa 2024年宣布收购)[[16]](https://github.com/api-evangelist/featurespace)，Flagright, ComplyAdvantage, NICE Actimize, ComplianceSuite.ai
- **KYC/身份验证**：Sumsub, Onfido, Jumio, Veriff, Shufti + Cevro AI, NuxGame + iDenfy
- **责任博彩**：Mindway AI GameScanner (虚拟心理学家，检测至少87%风险案例)[[17]](https://www.cdcgaming.com/focus-on-mindway-ai-getting-ahead-of-problem-gambling-with-ai-expert-assessments/) 与 Gamalyze (神经科学游戏化自测)[[18]](https://aytomallen.com/united-kingdom-gambling-commission/mindway-ai-rolls-out-responsible-gambling-solutions-across-dutch-market/)，每月监测超900万活跃用户[[19]](https://www.pasa365.com/en/main/info/news/detail/718433715646136433)，已被Better Collective收购，DraftKings 2026年1月集成Gamalyze[[20]](https://www.cdcgaming.com/mindway-ais-gamalyze-tool-to-be-integrated-by-draftkings-responsible-gaming-center/)，Playtech BetBuddy，Sportradar Bettor Sense, Neccton Mentor
- **客服/后台代理**：Cevro, InteractiveAI, Moveo.AI
- **审计**：AI Decision Logger (满足EU AI Act第12条与GDPR第22条)

```
::: 

::: {.callout-note collapse="true"}
來源第 78 行；段落 8b086aa8f5f3d888；UNKNOWN_INHERITED。

```text
### 1.8 第三方玩家工具（非平台官方，需警惕）

```
::: 

::: {.callout-note collapse="true"}
來源第 80 行；段落 8d1a760ad2d89b48；UNKNOWN_INHERITED。

```text
FPLAY, Mysports.AI, Oracle Baccarat Predictor, BACC.BOT, BaccaratAI 等，多声称ML/深度学习/RL自动分析路单与API自动下注，平台通常禁止，百家乐长期house edge固定。

```
::: 

::: {.callout-note collapse="true"}
來源第 82 行；段落 8796b5b37ff0122d；UNKNOWN_INHERITED。

```text
## 2. 全量前沿技术栈（附件去重 63项）

```
::: 

::: {.callout-note collapse="true"}
來源第 84 行；段落 ecf0515e741a5692；UNKNOWN_INHERITED。

```text
### 2.1 开源框架与程序包

```
::: 

::: {.callout-note collapse="true"}
來源第 86 行；段落 67a885613e9bf1d4；UNKNOWN_INHERITED。

```text
| 层级 | 技术 | 用途 |
|---|---|---|
| 传统ML | Scikit-Learn, XGBoost, LightGBM, Random Forest, Logistic Regression, arch, linearmodels, optuna | 风控监督分类、流失预测、风险评分、GARCH波动率、面板IV/2SLS |
| 深度学习 | TensorFlow, PyTorch, torch_geometric (PyTorch Geometric), RGCN, GraphSAGE | Autoencoder异常检测、图神经网络捕捉IP-设备-钱包-时间团伙 |
| 图分析 | Graph Analytics, ACT Fraud Rings, Isolation Forest, data.table, Polars, DuckDB | 设备/IP/行为关联可视化，高吞吐特征工程 |
| 时序/序列 | RNN, HMM, Transformer, lifelines, survival, JMbayes2, brms | LTV与沉迷突变点生存分析，联合建模 |
| 强化学习 | Q-learning, SARSA, Contextual Bandit / Multi-armed Bandit, DQN, PPO, MAB, Bandit工作台 | 奖金/任务难度/时机优化，探索-利用平衡，学术有用RL研究百家乐投注策略但非平台核心 |
| 视觉/OCR | YOLOv8/v10 + CRNN, PaddleOCR, OpenCV, ultralytics, TensorRT, ONNX Runtime, FP16/INT8量化 | 60FPS实时定位扑克牌与点数识别，<50ms低延迟推理，电子路纸渲染 |
| 流处理/存储 | Kafka, Flink, Iceberg, StarRocks/ClickHouse, SeaTunnel/DolphinScheduler, Spark/Hive | 高吞吐事件摄取、实时特征计算、CEP复杂事件处理、批流一体ACID湖仓 |
| XAI/合规 | SHAP, LIME, pydantic, TREPAN, AI Decision Logger | 可解释归因、决策树抽取、数据契约验证、不可变审计日志 |
| 统计/因果 | EconML (DML), survival analysis | ATE估计，风险建模 |

```
::: 

::: {.callout-note collapse="true"}
來源第 98 行；段落 934cb17d421d63f9；UNKNOWN_INHERITED。

```text
### 2.2 商业技术架构

```
::: 

::: {.callout-note collapse="true"}
來源第 100 行；段落 818208ad1bcad7a7；UNKNOWN_INHERITED。

````text
```
[前端：60FPS低延迟视频流 + 投注流]
   ↓ YOLOv8 + TensorRT + ONNX Runtime 边缘推理 (~3-5ms)
[增效层：Kafka + Flink + StarRocks 100ms自动派彩与对账]
   ├→ [止损层：GNN图谱 + XGBoost + Isolation Forest + SEON设备指纹 + Featurespace ARIC 自适应行为]
   └→ [合规层：SHAP归因 + lifelines生存分析 + BetBuddy/Mindway GameScanner 26标记]
         ↓
[存储中台：Iceberg + DWS特征 + R/Python建模]
         ↓
[案件队列 + 人工复核 + 可回滚 + 申诉通道 + AI Decision Logger]
```

````
::: 

::: {.callout-note collapse="true"}
來源第 112 行；段落 4736a8335194e0dd；UNKNOWN_INHERITED。

```text
### 2.3 算法边界

```
::: 

::: {.callout-note collapse="true"}
來源第 114 行；段落 af706a6406e4c358；UNKNOWN_INHERITED。

```text
- **止损目标函数**：max_θ E[Revenue - FraudLoss(θ) - FalsePositiveCost(θ)]
- **RL可行**：CRM/游戏化层 contextual bandits，Reward=留存/限额采纳/风险下降/投诉减少，禁止GGR/投注额
- **RL不可行**：用RL改变RTP/赔率/牌靴/RNG/派彩/针对个人调结果

```
::: 

::: {.callout-note collapse="true"}
來源第 118 行；段落 7a18f20907b70244；UNKNOWN_INHERITED。

```text
## 3. RedTeam：攻击面与失效模式

```
::: 

::: {.callout-note collapse="true"}
來源第 120 行；段落 6a91edf57261ff5e；UNKNOWN_INHERITED。

```text
1. **信任瓦解攻击**：AI荷官音频过清晰破坏剧场感需故意脏化，渲染延迟>2秒口型与牌面不同步被弹幕放大为操纵证据[[9]](https://parameter.io/bethog-secures-10m-series-a-to-revolutionize-online-casino-gaming-with-ai-dealers/)
2. **优势玩家AI对抗**：边注占亚洲赌场40-60%收入，AI辅助算牌已成优势玩家工具，亚洲市场年损失估计5-7亿美元，若仅阉割规则而非AI主动识别将持续流失
3. **浏览器AI代理绕过**：OpenAI Operator、Claude for Chrome、Playwright、Puppeteer、Selenium等可在注册请求到达服务器前被cside类250+信号检测拦截
4. **奖励优化反噬**：RL在最优发奖时机触发冲动，降低有意识控制，连败后发安慰奖延长痛苦游戏
5. **数据投毒与BM3操纵**：机器人刷低额投注污染训练数据掩盖套利
6. **规则引擎误认AI**：把规则引擎当AI、推荐系统当负责任AI、供应商可接入当已全面投产

```
::: 

::: {.callout-note collapse="true"}
來源第 127 行；段落 c784b6cf5423f744；UNKNOWN_INHERITED。

```text
## 4. Critic：主流叙事的裂缝

```
::: 

::: {.callout-note collapse="true"}
來源第 129 行；段落 f841dcd06f821ea2；UNKNOWN_INHERITED。

```text
- **证据等级不一致**：Evolution/Playtech/Entain/Flutter证据等级高，有官方披露与并购时间线；WM/SA/Dream仅有代理营销页面与“稳定运营”宣传语，无AI/RL白皮书；Octane/Sentient属OBSERVED而非PROVEN INDUSTRY STANDARD
- **RL与AI混为一谈**：Rule Engine → ML → Deep Learning → Bandit → RL为不同成熟度，公开可验证多停留在监督学习/异常检测/推荐/流失预测，真正RL仅在Bonus Engine/CRM/Contextual Bandits
- **寡头创新者困境**：Evolution 60%+ Live市占，公开贬低AI为deepfake，后再拥抱将自我蚕食
- **亚洲供应商透明度真空**：SA/AG/DG在PAGCOR文件仅列桌台数量与边注种类，无模型卡、数据集或审计报告
- **准确率数字陷阱**：75.94%流失预测、15%高风险设限等需看基准样本与漂移，缺乏purge walk-forward验证
- **运营自动化与玩家保护混淆**：Entain ARC、Kindred EDS公开案例集中于责任博彩，本质监管合规叙事，非运营效率证据

```
::: 

::: {.callout-note collapse="true"}
來源第 136 行；段落 20aceeb2d19c917f；UNKNOWN_INHERITED。

```text
## 5. KillCritic：对批判的反驳与证伪

```
::: 

::: {.callout-note collapse="true"}
來源第 138 行；段落 c76cf890cea34cb6；UNKNOWN_INHERITED。

```text
1. **AI更人性化反证**：BetHog实测新玩家因害怕在真人台问怎么玩而退缩，反愿向AI提问并使用问荷官按钮，AI提供比人类更低门槛体验，信任来源从物理牌转向品牌与可证明公平RNG
2. **AI可用于保护反证**：BetBuddy已被17司法管辖区信任，三层风险评级模型可提前数周预测，对照试验15%高风险玩家1小时内主动设限；Mindway每月监测超900万活跃用户，≥87%专家级检出率[[17]](https://www.cdcgaming.com/focus-on-mindway-ai-getting-ahead-of-problem-gambling-with-ai-expert-assessments/)
3. **RL非营销话术反证**：Smartico/Optimove产品套件含AI驱动LTV预测与风险建模，且2026年4月收购案已官宣[[2]](https://www.citybiz.co/article/828787/optimove-to-acquire-smartico-2/)，非空口号，客户案例Stardust/BetMGM/Sisal有量化增效
4. **SOFTSWISS COO自证**：AI虽能实时分析大数据，但最终决策仍留专家，否则不可预见后果导致财务损失，证明人工监督非否定AI而是成熟治理
5. **成本与规模反证**：Sentient称AI台更吸引低额碎片化玩家，10倍参与度颠覆Live仅服务高额VIP假设；Octane数日交付品牌化桌台，容量可1到10000桌弹性伸缩

```
::: 

::: {.callout-note collapse="true"}
來源第 144 行；段落 708fad483349c332；UNKNOWN_INHERITED。

```text
## 6. Blindspot：监管、伦理与证据盲区

```
::: 

::: {.callout-note collapse="true"}
來源第 146 行；段落 2a45bbd3d0a4bd65；UNKNOWN_INHERITED。

```text
- **MGA AI Gaming Charter自愿性陷阱**：马耳他博彩管理局与数字创新局2026年9月18日发布，48页，自愿、基于原则框架，补充EU AI Act与GDPR，涵盖玩家保护、反欺诈、客户交互与运营决策，要求高影响AI强化文档、测试、人工监督与持续监控，无新增法律义务[[4]](https://www.mga.org.mt/mga-launches-ai-gaming-charter-following-extensive-industry-collaboration/) [[5]](https://europeangaming.eu/portal/latest-news/2026/09/22/214529/mga-mdia-ai-gaming-charter-launch/) [[21]](https://igaming-times.com/news/regulatory/maltas-regulator-publishes-a-voluntary-ai-charter-for-gaming-operators)
- **EU AI Act高风险定性**：欺诈检测、行为追踪、个性化推荐、聊天机器人均可能归为高风险，需要技术参数、透明度、风险管理与人工监督
- **UKGC LCCP 3.4.3**：要求强风险指标及时自动化处理，但个案仍需人工审核并允许客户提出异议
- **剥削性目标函数**：纽约时报调查DraftKings用ML识别最可能输钱客户定向发放免费投注，而问题博彩检测工具被搁置，专家警告AI可识别脆弱性并最大化利润，现有法规几乎空白，伦理活在目标函数而非架构
- **数据隔离红线**：责任博彩风险分数与营销/返水系统必须物理或逻辑隔离，风险分数不得用于促销、返水、VIP升级、催存、召回
- **亚洲市场双重叙事**：SOFTSWISS称AI可遏制日益增长iGaming欺诈并灌输负责任博彩，但同时承认AI无法完全防止欺诈，仅能实时监测

```
::: 

::: {.callout-note collapse="true"}
來源第 153 行；段落 369fdc50a68228cc；UNKNOWN_INHERITED。

```text
## 7. ActionPlan：自强追赶天下最顶尖 - 三价值四层落地路线图

```
::: 

::: {.callout-note collapse="true"}
來源第 155 行；段落 94a52ca72fe9e37c；UNKNOWN_INHERITED。

```text
### 7.1 核心原则

```
::: 

::: {.callout-note collapse="true"}
來源第 157 行；段落 97d8bbdc3bc2ffc4；UNKNOWN_INHERITED。

```text
AI只做排序、预警与低风险自动化；高影响决策（封号、限额、提款冻结、干预）必须保留人工覆核与完整审计轨迹，AI永不进入百家乐牌局结果与对脆弱玩家的营销决策

```
::: 

::: {.callout-note collapse="true"}
來源第 159 行；段落 1802b20f1e8178a3；UNKNOWN_INHERITED。

```text
### 7.2 四层架构

```
::: 

::: {.callout-note collapse="true"}
來源第 161 行；段落 36a24a0f8fc2ce9a；UNKNOWN_INHERITED。

```text
| 层级 | 技术组件 | 对应目标 | 附件来源 |
|---|---|---|---|
| L1 数据摄取 | Kafka + Flink + Iceberg + StarRocks/ClickHouse | 实时事件流 + 批流一体存储 | DeepSeek/Gemini |
| L2 特征与模型 | Scikit-Learn/XGBoost/LightGBM + TensorFlow/PyTorch + GNN + Isolation Forest + YOLOv8 + PaddleOCR | 欺诈检测、流失预测、风险评分、牌面识别 | DeepSeek/Gemini/Copilot |
| L3 商业智能 | Bonus Guardian / Smartico/Optimove Opti-X / BetBuddy / Mindway GameScanner / SEON / Featurespace ARIC | 奖金风控、RL留存优化、责任博彩 | 全量 |
| L4 合规与审计 | Shufti+Cevro AI / ComplianceSuite.ai / AI Decision Logger + MGA Charter + ISO/IEC 42001 | KYC/AML自动化、审计追踪、EU合规 | DeepSeek/Grok/Gemini |

```
::: 

::: {.callout-note collapse="true"}
來源第 168 行；段落 b64a91eb0ebd6002；UNKNOWN_INHERITED。

```text
### 7.3 分阶段实施

```
::: 

::: {.callout-note collapse="true"}
來源第 170 行；段落 d7f0c97ad02f395c；UNKNOWN_INHERITED。

```text
**立即落地 (0-30天) - 止损优先**
- Mindway GameScanner或BetBuddy + Sumsub/SEON + 基本案件管理系统 + AI Decision Logger
- 建立AI系统清单、问责人、人工覆盖能力日志，满足MGA Charter对高影响系统要求
- 接入Kafka → Flink实时管道，ODS→DWS特征工程，规则层秒级拦截KYC未完成/极端迟下注/已知黑名单

```
::: 

::: {.callout-note collapse="true"}
來源第 175 行；段落 0b3741df389bb0a0；UNKNOWN_INHERITED。

```text
**3-6个月 - 增效**
- 接入Smartico/Optimove做合规导向CRM自动化，contextual bandits测试奖励时机，Reward=限额采纳/冷静期完成/风险下降
- 评估SOFTSWISS Casino Platform + BM3 + EveryMatrix Bonus Guardian，对接PAM实时API
- 试点YOLOv8/v10 + CRNN + TensorRT边缘推理，实现物理牌面识读与电子路纸自动渲染，目标100ms派彩

```
::: 

::: {.callout-note collapse="true"}
來源第 180 行；段落 dfac75e560ed8ca0；UNKNOWN_INHERITED。

```text
**6-12个月 - 规模化与自研**
- 试点Sentient/Octane AI荷官降低真人桌成本，数日交付多语言品牌化桌台，测试低额碎片化玩家留存
- 自建Dealer Anomaly Detection (荷官异常)、Player Risk (玩家风险)、Live Casino Analytics、Agent Network Intelligence (代理层级图谱，GNN RGCN/GraphSAGE)
- 建立purge walk-forward验收：Precision@人工产能、误伤预算、可回滚率、人工复核率100%、模型漂移监控

```
::: 

::: {.callout-note collapse="true"}
來源第 185 行；段落 67021e71e9e7b997；UNKNOWN_INHERITED。

```text
**长期 - 持续自强**
- 三管线隔离：反诈/串通、AML、责任博彩数据与处置完全分离
- RL仅离线沙盒：固定保护性动作集、因果评估、合规审批后小流量，reward禁止GGR/投注额
- 每周固定as-of日期，只使用当时可见数据建特征，预测未来7/14/30日明确结果：人工确认串通、KYC证据成立、SAR升级、责任博彩实质升级

```
::: 

::: {.callout-note collapse="true"}
來源第 190 行；段落 7971e0e1b7e00b3c；UNKNOWN_INHERITED。

```text
### 7.4 对标顶级平台的自强KPI（非GGR）

```
::: 

::: {.callout-note collapse="true"}
來源第 192 行；段落 c958281d4a2957c0；UNKNOWN_INHERITED。

```text
- **止损**：奖金滥用拦截率、误伤率、5-7亿美元边注优势玩法损失降低、钱骡链揭示数、61,810请求级节省
- **增效**：7日流失率、30天LTV、月活、独立存款人、NGR、忠诚客户毛收入、桌台弹性扩容成本
- **合规**：强风险信号响应时延、人工复核率100%、理由码留存率100%、责任博彩资料未流向行销的隔离稽核、限额/冷静期采纳率、申诉成功率

```
::: 

::: {.callout-note collapse="true"}
來源第 196 行；段落 908ac4ef9522a777；UNKNOWN_INHERITED。

```text
### 7.5 最终判断

```
::: 

::: {.callout-note collapse="true"}
來源第 198 行；段落 bf6de17ec3be1692；UNKNOWN_INHERITED。

```text
截至2026年9月可公开验证资料，AI驱动营运已被证实，RL控制百家乐核心运营仍属证据不足。最可信趋势：AI负责玩家、账户、交易与营运流程；游戏规则、发牌结果、RNG、派彩与百家乐胜负逻辑仍受监管、认证与审计体系约束。对标顶级不是追求一句我们用了RL口号，而是可信资料底座 + 可解释排序 + 受控自动化 + 人工救济 + 时间外推实证。

```
::: 

::: {.callout-note collapse="true"}
來源第 200 行；段落 99003000ac1faa3f；UNKNOWN_INHERITED。

```text
## Sources

```
::: 

::: {.callout-note collapse="true"}
來源第 202 行；段落 ca089303c01bc6d9；UNKNOWN_INHERITED。

```text
[1] SOFTSWISS — [Anti-Fraud Team Helped Operators Save €16m+ in 2022](https://www.softswiss.com/?p=46815)
[2] CityBiz — [Optimove to Acquire Smartico](https://www.citybiz.co/article/828787/optimove-to-acquire-smartico-2/)
[3] BettingStartups News — [Octane Studios launches customizable AI dealers, starting with baccarat](http://news.bettingstartups.com/p/octane-studios-ai-dealers-betting-gaming)
[4] Malta Gaming Authority — [MGA launches AI Gaming Charter following extensive industry collaboration](https://www.mga.org.mt/mga-launches-ai-gaming-charter-following-extensive-industry-collaboration/)
[5] European Gaming — [Malta's AI Gaming Charter: What licensees need to know](https://europeangaming.eu/portal/latest-news/2026/09/22/214529/mga-mdia-ai-gaming-charter-launch/)
[6] Playtech — [Services - Player Protection Services with BetBuddy](https://www.playtech.com/services-2/)
[7] Featurespace — [SKS365 Selects Featurespace's Adaptive Behavioural Analytics](https://www.featurespace.com/newsroom/sks365-selects-featurespaces-adaptive-behavioural-analytics-to-predict-and-identify-fraudulent-activity/)
[8] FinancialContent — [Optimove to Acquire Smartico](https://markets.financialcontent.com/lethbridgeherald/article/gnwcq-2026-4-6-optimove-to-acquire-smartico)
[9] Parameter — [BetHog Secures $10M Series A to Revolutionize Online Casino Gaming with AI Dealers](https://parameter.io/bethog-secures-10m-series-a-to-revolutionize-online-casino-gaming-with-ai-dealers/)
[10] BettingStartups News Archive — [BetHog shuts down July 31 to go all-in on Sentient Studios’ AI dealers](https://news.bettingstartups.com/archive?page=-18)
[11] AGBrief — [Smart tables feed new frontier in patron data for Sands](https://agbrief.com/news/macau/28/05/2026/smart-tables-open-new-frontier-in-patron-data-for-sands/)
[12] AGBrief — [Smart gaming tables' pose recognition takes baccarat to a different level](https://agbrief.com/intel/deep-dive/21/05/2026/smart-gaming-tables-pose-recognition-takes-baccarat-to-a-different-level-angel-cto-says/)
[13] Focus Gaming News — [Angel Group completes implementation of baccarat smart tables for Sands China](https://focusgn.com/asia-pacific/angel-group-completes-implementation-of-baccarat-smart-tables-for-sands-china)
[14] Gambling Insider — [Entain makes big sustainability strides but lags on gender pay gap](https://www.gamblinginsider.com/in-depth/15760/entain-makes-big-sustainability-strides-but-lags-on-gender-pay-gap)
[15] London Stock Exchange — [Entain Regulatory News - ARC's Protector Model encompasses 26 markers](https://www.lse.co.uk/rns/ENT/entainsustain-esg-showcase-event-3qo7obdn2c9rwpg.html?page=12)
[16] GitHub API Evangelist — [Featurespace - Adaptive Behavioral Analytics](https://github.com/api-evangelist/featurespace)
[17] CDC Gaming — [Focus on Mindway AI: Getting ahead of problem gambling](https://www.cdcgaming.com/focus-on-mindway-ai-getting-ahead-of-problem-gambling-with-ai-expert-assessments/)
[18] AytomAllen — [Mindway AI rolls out responsible gambling solutions across Dutch market](https://aytomallen.com/united-kingdom-gambling-commission/mindway-ai-rolls-out-responsible-gambling-solutions-across-dutch-market/)
[19] PASA365 — [Better Collective leverages Mindway AI](https://www.pasa365.com/en/main/info/news/detail/718433715646136433)
[20] CDC Gaming — [Mindway AI’s Gamalyze tool to be integrated by DraftKings Responsible Gaming Center](https://www.cdcgaming.com/mindway-ais-gamalyze-tool-to-be-integrated-by-draftkings-responsible-gaming-center/)
[21] iGaming Times — [Malta's Regulator Publishes a Voluntary AI Charter](https://igaming-times.com/news/regulatory/maltas-regulator-publishes-a-voluntary-ai-charter-for-gaming-operators)
```
::: 

### 來源：Reference/Baccarat-Ai-Automation-Report.md

[原始來源](<Baccarat-Ai-Automation-Report.md>)；SHA256：`a01032f8169a43bac4c024c7a1c8add890647f0eeae43272fb6a88a27616d6f7`。下列為未覆蓋段落；歷史主張未經收錄自動驗證。

::: {.callout-note collapse="true"}
來源第 1 行；段落 da9289659d1eac0a；UNKNOWN_INHERITED。

```text
# 頂級在線百家樂平台 AI 與強化學習自動化運營查證報告

```
::: 

::: {.callout-note collapse="true"}
來源第 5 行；段落 153690c2aeb649eb；UNKNOWN_INHERITED。

```text
頂級在線百家樂已從純人力直播演進為混合自動化系統。查證顯示，真正公開宣稱並落地 AI Dealer 取代人力的廠商僅為新興勢力：Octane Studios 與 Sentient Studios（前 BetHog），兩者均以百家樂為首發品類，提供認證 RNG、可定制品牌化、7x24 無限擴容能力 [[1]](http://news.bettingstartups.com/p/octane-studios-ai-dealers-betting-gaming) [[2]](https://igamingbusiness.com/tech-innovation/artificial-intelligence/nigel-eccles-all-in-ai-live-dealer-bethog/)。傳統寡頭 Evolution、Pragmatic Play、Ezugi、Playtech 的自動化重心不在發牌本身，而在運營中台：AI 驅動的反欺詐、風控、CRM、負責任博彩檢測與內容個性化。平台層 SOFTSWISS 與 CRM 層 Smartico 則構成了強化學習（RL）落地的核心：多臂老虎機（Multi-armed Bandit）算法優化獎勵、強化學習驅動遊戲化引擎調整難度與時機 [[3]](https://ideausher.com/blog/ai-for-casino-player-retention-like-smartico-ai-development/) [[4]](https://www.smartico.ai/blog-post/predictive-churn-analytics-ai-driven-player-retention)。

```
::: 

::: {.callout-note collapse="true"}
來源第 7 行；段落 6a904e13e3b52109；UNKNOWN_INHERITED。

```text
亞洲主流供應商 SA Gaming、Asia Gaming、Dream Gaming 官方資料未顯示自研 AI Dealer，自動化仍停留在 Auto Roulette 等去荷官變種與路單統計自動化階段。

```
::: 

::: {.callout-note collapse="true"}
來源第 9 行；段落 e1cacc573dac11f0；UNKNOWN_INHERITED。

```text
## 1. 頂級平台版圖與自動化定位

```
::: 

::: {.callout-note collapse="true"}
來源第 11 行；段落 ed3178b6d70e5830；UNKNOWN_INHERITED。

```text
| 平台 / 技術提供商 | 百家樂產品 | AI/RL 自動化宣稱與實證 | 自動化層級 |
| --- | --- | --- | --- |
| **Octane Studios** | AI Baccarat 首發 | 可定制 AI 荷官，認證 RNG， provably fair，品牌方數日內交付 [[1]](http://news.bettingstartups.com/p/octane-studios-ai-dealers-betting-gaming) | 前台發牌自動化 |
| **Sentient Studios (BetHog)** | AI Blackjack Sunny，已宣布 2026 年底上線 Baccarat/Roulette | 擬真 AI 荷官，實時對話、表情、肢體同步，10倍於真人台的參與度，12 語言，10M 美元 A 輪融資支撐 [[2]](https://igamingbusiness.com/tech-innovation/artificial-intelligence/nigel-eccles-all-in-ai-live-dealer-bethog/) [[5]](https://www.finsmes.com/2026/04/bethog-raises-10m-in-series-a-funding.html) | 前台發牌自動化 + 個性化交互 |
| **Evolution** | Speed Baccarat, Lightning Baccarat, First Person Baccarat | 官方列 AI-Powered Fraud Detection、Biometric Dealer Authentication、實時模式分析；CPO Todd Haushalter 公開談 AI 革新 Slot 生產 [[6]](http://newcasinorank.com/evolution-gaming/) [[7]](https://evolution-baccarat-site60539.illawiki.com/1213401/the_leading_reasons_why_people_achieve_in_the_evolution_gaming_industry) | 中台風控與生產自動化 |
| **Pragmatic Play** | Mega Baccarat, Auto-Roulette, Bet Behind Pro Blackjack | 7 個 Bot 坐桌，使用基礎策略自動決策，玩家可 Bet Behind；Auto-Roulette 無需荷官自動發球 [[8]](https://gaming-awards.com/NEWS/pragmatic-play-transforms-live-casino-classic/) [[9]](https://gaming-awards.com/NEWS/pragmatic-play-goes-live-casino-auto-roulette/) | 半自動化 Bot 荷官 |
| **Ezugi (Evolution 旗下)** | EZ Baccarat, Ultimate Auto Roulette | Ultimate Auto Roulette 為全自動無荷官；EZ Baccarat 主打 hands-per-hour 最快的自動化節奏 | 去荷官自動化 |
| **Playtech** | Prestige Baccarat | BetBuddy AI 行為監測與預測風險建模，Featurespace ML 實時反欺詐；托管服務宣稱 AI-Driven Automation、實時監控 [[10]](https://www.playtech.com/services-2/) | 負責任博彩與風控自動化 |
| **SOFTSWISS (B2B 平台)** | 為上百家百家樂運營商提供後台 | Anti-Fraud Service 實時 ML 檢測可疑，2022 年處理 61,810 請求，節省運營商 16M+ 歐元；BM3 業務指標監控；DOSSIER 玩家行為預測 LTV [[11]](https://focusgn.com/softswiss-highlights-igaming-areas-in-which-ai-outperforms-humans) [[12]](https://www.softswiss.com/news/ai-trends-igaming-softswiss-2025/) | 運營中台全面自動化 |
| **Smartico / Optimove** | CRM 覆蓋百家樂桌台事件 | 強化學習驅動遊戲化引擎自適應難度與獎勵時機，多臂老虎機算法實時獎勵優化，集成預測流失模型準確率 75.94% [[3]](https://ideausher.com/blog/ai-for-casino-player-retention-like-smartico-ai-development/) [[4]](https://www.smartico.ai/blog-post/predictive-churn-analytics-ai-driven-player-retention) | RL 驅動留存與獎勵自動化 |
| **Kindred/Unibet** | 運營商層 | PS-EDS Player Safety Early Detection System，使用智能算法識別有害行為演變 [[13]](https://ggbmagazine.com/articles/technology-responsible-gamings-front-line/) | 負責任博彩自動化 |

```
::: 

::: {.callout-note collapse="true"}
來源第 23 行；段落 6b75e0a68a4c87b0；UNKNOWN_INHERITED。

```text
> **註**：SA Gaming、Asia Gaming、Dream Gaming 在 PAGCOR 認證文件與主流評測中僅列出桌台數量與邊注種類，未檢索到自研 AI/RL 公開技術白皮書。

```
::: 

::: {.callout-note collapse="true"}
來源第 25 行；段落 2a11f19976129920；UNKNOWN_INHERITED。

```text
## 2. 強化學習與自動化的技術堆棧解剖

```
::: 

::: {.callout-note collapse="true"}
來源第 27 行；段落 f8d93e1cb3e9b81e；UNKNOWN_INHERITED。

```text
### 2.1 前台：生成式 AI 荷官
Octane 與 Sentient 的架構共識是：**RNG 引擎與渲染引擎分離**。發牌結果由已認證 RNG 決定，AI 僅負責擬真表達、對話與情緒同步，以規避「AI 知道底牌」的信任風險 [[2]](https://igamingbusiness.com/tech-innovation/artificial-intelligence/nigel-eccles-all-in-ai-live-dealer-bethog/)。這解釋了為何其監管路徑被描述為「本質上是 RNG 產品」而非 Live。

```
::: 

::: {.callout-note collapse="true"}
來源第 30 行；段落 05cb6512e81280d6；UNKNOWN_INHERITED。

```text
Sentient 稱 AI 台更吸引低額、碎片化玩家，顛覆 Live 僅服務高額 VIP 的假設，導致 10 倍參與度差異 [[2]](https://igamingbusiness.com/tech-innovation/artificial-intelligence/nigel-eccles-all-in-ai-live-dealer-bethog/)。

```
::: 

::: {.callout-note collapse="true"}
來源第 32 行；段落 9556b0330d638755；UNKNOWN_INHERITED。

```text
### 2.2 中台：風控與反欺詐
SOFTSWISS Anti-Fraud Service 被描述為實時數據分析工具，利用機器學習模型檢測可疑案件並提交人工複核，2023 年處理 100,000+ 請求，節省 1300 萬歐元 [[14]](https://igamingfuture.com/softswiss-unveils-vision-for-ai-powered-business-at-reflect-festival-2025/)。Evolution 官方渠道同樣列出 Advanced AI Monitoring、Strict KYC + AML 與 GLI Certified RNG + Live Dealer 並行 [[15]](https://bisd.rs/quantum-roulette-and-fraud-detection-systems-what-every-aussie-newcomer-should-know/)。

```
::: 

::: {.callout-note collapse="true"}
來源第 35 行；段落 ebe457d7efd253f0；UNKNOWN_INHERITED。

```text
### 2.3 後台：CRM 與強化學習
這是 RL 真正落地的領域。Smartico 文檔明確指出：
- 遊戲化引擎使用強化學習調整任務難度、時機與獎勵以維持心流 [[3]](https://ideausher.com/blog/ai-for-casino-player-retention-like-smartico-ai-development/)。
- 上下文獎勵優化使用多臂老虎機算法，測試多種獎勵類型並自動選擇對個體最有效的方案 [[3]](https://ideausher.com/blog/ai-for-casino-player-retention-like-smartico-ai-development/)。
- 流失預測使用 RNN 處理時序行為，預測 7/14/30 天流失概率，並觸發動態獎勵、渠道選擇與慷慨度分級 [[4]](https://www.smartico.ai/blog-post/predictive-churn-analytics-ai-driven-player-retention)。

```
::: 

::: {.callout-note collapse="true"}
來源第 41 行；段落 8b3bc2de0a724553；UNKNOWN_INHERITED。

```text
SOFTSWISS 2025 趨勢報告也將「自動化複雜決策」列為核心，點名玩家支持聊天機器人、SumSub 反欺詐異常標記與實時決策自動化 [[12]](https://www.softswiss.com/news/ai-trends-igaming-softswiss-2025/)。

```
::: 

::: {.callout-note collapse="true"}
來源第 43 行；段落 740678c2fa240a51；UNKNOWN_INHERITED。

```text
## 3. RedTeam：攻擊面與失效模式

```
::: 

::: {.callout-note collapse="true"}
來源第 45 行；段落 cce02b03136c21d4；UNKNOWN_INHERITED。

```text
1. **信任瓦解攻擊**：AI 荷官音頻質量過高反而破壞劇場感，需刻意加入背景噪聲做髒化處理，否則玩家感知為假 [[2]](https://igamingbusiness.com/tech-innovation/artificial-intelligence/nigel-eccles-all-in-ai-live-dealer-bethog/)。若渲染延遲超過 2 秒，口型與牌面不同步，將被直播彈幕放大為「操縱」證據。
2. **優勢玩家 AI 對抗**：Differential Labs 研究指出百家樂邊注占亞洲賭場 40-60% 收入，AI 輔助算牌已成為優勢玩家新工具 [[16]](https://asgam.com/2026/08/30/study-finds-ai-backed-advantage-play-on-baccarat-side-bets-becoming-an-increasing-problem-for-casinos-in-asia/)。若運營方僅用規則閹割而非 AI 主動識別，將流失高價值桌台利潤。
3. **獎勵優化反噬**：強化學習識別最優發獎時機以觸發衝動，文獻指出可能降低用戶對投注行為的有意識控制 [[17]](https://pmc.ncbi.nlm.nih.gov/articles/PMC12189489/)。若目標函數僅最大化短期 LTV，模型將學會在連敗後發放「安慰獎」延長痛苦遊戲。
4. **數據投毒**：SOFTSWISS BM3 依賴關鍵業務指標異常檢測，若攻擊者通過機器人刷低額投注污染訓練數據，可掩蓋真實套利行為。

```
::: 

::: {.callout-note collapse="true"}
來源第 50 行；段落 b2f8f780727814f4；UNKNOWN_INHERITED。

```text
## 4. Critic：主流敘事的裂縫

```
::: 

::: {.callout-note collapse="true"}
來源第 52 行；段落 3e7e19e5b0ced314；UNKNOWN_INHERITED。

```text
- **「AI 取代荷官 = 降本」敘事過簡**：Evolution 60%+ Live 市占與高 EBITDA 護城河依賴真人工作室與品牌信任。Eccles 類比 De Beers 實驗室鑽石戰略，指出寡頭存在創新者困境，公開貶低 AI 為 deepfake 後再擁抱將自我蠶食 [[2]](https://igamingbusiness.com/tech-innovation/artificial-intelligence/nigel-eccles-all-in-ai-live-dealer-bethog/)。
- **「自動化 = 效率」忽視人工監督成本**：SOFTSWISS COO 明言 AI 雖能實時分析大數據集，但最終決策仍應留給專家，否則不可預見後果可能導致財務損失 [[11]](https://focusgn.com/softswiss-highlights-igaming-areas-in-which-ai-outperforms-humans)。
- **亞洲供應商 AI 敘事真空**：SA Gaming、AG、DG 在公開渠道未提供模型卡、數據集或審計報告，其「自動」僅指無荷官機械臂發牌，而非智能決策。將其列為 AI 平台屬營銷誤植。

```
::: 

::: {.callout-note collapse="true"}
來源第 56 行；段落 1c48afaaf35e297f；UNKNOWN_INHERITED。

```text
## 5. KillCritic：對批判的反駁與證偽

```
::: 

::: {.callout-note collapse="true"}
來源第 58 行；段落 326fe7229f6afcab；UNKNOWN_INHERITED。

```text
1. **反駁「AI 荷官無人信」**：BetHog 實測顯示新玩家因害怕在真人台問「該怎麼玩」而退縮，反而願意向 AI 提問並使用「問荷官」按鈕，AI 提供了比人類更人性化的體驗 [[2]](https://igamingbusiness.com/tech-innovation/artificial-intelligence/nigel-eccles-all-in-ai-live-dealer-bethog/)。信任來源從物理牌轉向品牌與可證明公平 RNG。
2. **反駁「AI 必然剝削」**：Playtech BetBuddy 被 17 個司法管轄區運營商信任，作為 AI 驅動的負責任博彩檢測，證明同一技術棧可反向用於保護 [[10]](https://www.playtech.com/services-2/)。SOFTSWISS 同步部署負責任博彩觸發器。
3. **反駁「RL 僅是營銷話術」**：Smartico 與 Optimove 的收購案中披露產品套件包含 AI 驅動 LTV 預測與風險建模，且公開準確率與 A/B 測試框架，非空口號 [[3]](https://ideausher.com/blog/ai-for-casino-player-retention-like-smartico-ai-development/)。

```
::: 

::: {.callout-note collapse="true"}
來源第 62 行；段落 5da3ccdda4c10c6f；UNKNOWN_INHERITED。

```text
## 6. Blindspot：監管與倫理盲區

```
::: 

::: {.callout-note collapse="true"}
來源第 64 行；段落 ba2772c05f47ae5d；UNKNOWN_INHERITED。

```text
- **MGA AI Gaming Charter 的自願性陷阱**：馬耳他博彩管理局與馬耳他數字創新局於 2026 年 9 月 18 日發布 AI Gaming Charter，明確為自願、基於原則的框架，補充 EU AI Act 與 GDPR，涵蓋玩家保護、反欺詐、客戶交互與運營決策 [[18]](https://igaming-times.com/news/regulatory/maltas-regulator-publishes-a-voluntary-ai-charter-for-gaming-operators) [[19]](https://www.mga.org.mt/mga-launches-ai-gaming-charter-following-extensive-industry-collaboration/)。自願意味著在 2026-2027 高風險系統義務生效前，運營商可選擇性披露模型。
- **EU AI Act 對博彩的高風險定性**：欺詐檢測、行為追蹤、個性化推薦與聊天機器人均可能被歸為高風險，需要技術參數、透明度、風險管理與人工監督 [[20]](https://gamblingclub.be/en/digital-compliance-eu-whats-stake-for-gambling/)。目前多數百家樂平台未公開模型審計。
- **剝削性目標函數**：紐約時報調查 DraftKings 使用機器學習識別最可能輸錢的客戶並定向發放免費投注，而原本用於檢測問題博彩的預測工具被擱置 [[21]](https://getaibook.com/news/draftkings-ai-target-gamblers-likely-to-lose/)。專家警告 AI 可識別脆弱性並最大化利潤，現有法規幾乎空白 [[22]](http://casinobeats.com/2025/06/19/experts-warn-ai-in-casinos-could-exploit-problem-gamblers/)。
- **SA 市場的雙重敘事**：SOFTSWISS 稱 AI 可遏制 SA 日益增長的 iGaming 欺詐並灌輸負責任博彩，但同時承認 AI 無法完全防止欺詐，僅能實時監測 [[23]](https://www.itweb.co.za/article/ai-can-help-curb-fraud-in-sas-booming-igaming-sector/6GxRKMYQEABMb3Wj)。

```
::: 

::: {.callout-note collapse="true"}
來源第 69 行；段落 16acaf7f9718f56f；UNKNOWN_INHERITED。

```text
## 7. ActionPlan：可執行的查證與部署路徑

```
::: 

::: {.callout-note collapse="true"}
來源第 71 行；段落 24877bbe46cf010b；UNKNOWN_INHERITED。

```text
**階段一：平台分級查證**
- Tier 1 AI-Native：Octane Studios、Sentient Studios，要求提供 RNG 認證（GLI/eCOGRA）與可證明公平報告 [[1]](http://news.bettingstartups.com/p/octane-studios-ai-dealers-betting-gaming)。
- Tier 2 混合自動化：Evolution、Pragmatic Play、Playtech、SOFTSWISS，要求提供反欺詐攔截率、誤殺率與人工複核 SLA。
- Tier 3 傳統自動化：SA Gaming、AG、DG，僅作去荷官速度優化對標，不納入 AI 採購。

```
::: 

::: {.callout-note collapse="true"}
來源第 76 行；段落 24ec6d4239b42fba；UNKNOWN_INHERITED。

```text
**階段二：RL 落地實驗**
- 在 Smartico 類 CRM 中啟用多臂老虎機獎勵分配，設置對照組，度量 30 天 LTV 與 7 日流失率，參考已披露 30-50% 流失降低與 75.94% 準確率基線 [[4]](https://www.smartico.ai/blog-post/predictive-churn-analytics-ai-driven-player-retention)。
- 部署 PS-EDS 或 BetBuddy 克隆，監測連敗追逐、重訪促銷頁等觸發器，強制人工干預閾值。

```
::: 

::: {.callout-note collapse="true"}
來源第 80 行；段落 9ad2fb897b4b4e6d；UNKNOWN_INHERITED。

```text
**階段三：合規加固**
- 對照 MGA AI Charter 與 EU AI Act 要求，建立 AI 系統清單、問責人、人工覆蓋能力與日誌可解釋性文檔 [[18]](https://igaming-times.com/news/regulatory/maltas-regulator-publishes-a-voluntary-ai-charter-for-gaming-operators)。
- 禁止將「最可能輸錢」作為獎勵定向目標函數，引入獨立倫理審計。

```
::: 

::: {.callout-note collapse="true"}
來源第 84 行；段落 4dd8f91102db608e；UNKNOWN_INHERITED。

```text
**階段四：紅隊演練**
- 模擬 AI 優勢玩家對邊注掃描，測試自家異常檢測延遲。
- 進行音視頻同步故障注入，觀察社群信任崩潰速度。

```
::: 

::: {.callout-note collapse="true"}
來源第 88 行；段落 266052ce3e67ece4；UNKNOWN_INHERITED。

```text
## Sources
[1] BettingStartups — [Octane Studios launches customizable AI dealers, starting with baccarat](http://news.bettingstartups.com/p/octane-studios-ai-dealers-betting-gaming)
[2] iGaming Business — [Why Nigel Eccles is going all in on AI live dealer](https://igamingbusiness.com/tech-innovation/artificial-intelligence/nigel-eccles-all-in-ai-live-dealer-bethog/)
[3] IdeaUsher — [How Smartico.ai Uses AI for Casino Player Retention](https://ideausher.com/blog/ai-for-casino-player-retention-like-smartico-ai-development/)
[4] Smartico — [Predictive Churn Analytics: AI-Driven Player Retention](https://www.smartico.ai/blog-post/predictive-churn-analytics-ai-driven-player-retention)
[5] Finsmes — [BetHog Raises $10M in Series A Funding](https://www.finsmes.com/2026/04/bethog-raises-10m-in-series-a-funding.html)
[6] NewCasinoRank — [Evolution Gaming New Casino](http://newcasinorank.com/evolution-gaming/)
[7] illawiki — [The Leading Reasons Why People Achieve In The Evolution Gaming Industry](https://evolution-baccarat-site60539.illawiki.com/1213401/the_leading_reasons_why_people_achieve_in_the_evolution_gaming_industry)
[8] Gaming Awards — [Pragmatic Play Transforms Live Casino Classic](https://gaming-awards.com/NEWS/pragmatic-play-transforms-live-casino-classic/)
[9] Gaming Awards — [Pragmatic Play Goes Live Casino Auto-Roulette](https://gaming-awards.com/NEWS/pragmatic-play-goes-live-casino-auto-roulette/)
[10] Playtech — [Services - Playtech](https://www.playtech.com/services-2/)
[11] FocusGN — [SOFTSWISS highlights igaming areas in which AI outperforms humans](https://focusgn.com/softswiss-highlights-igaming-areas-in-which-ai-outperforms-humans)
[12] SOFTSWISS — [AI Trends in iGaming 2025: From Hype to Practical Implementation](https://www.softswiss.com/news/ai-trends-igaming-softswiss-2025/)
[13] GGB Magazine — [Technology: Responsible Gaming's Front Line](https://ggbmagazine.com/articles/technology-responsible-gamings-front-line/)
[14] iGaming Future — [SOFTSWISS Unveils Vision for AI-Powered Business at Reflect Festival 2025](https://igamingfuture.com/softswiss-unveils-vision-for-ai-powered-business-at-reflect-festival-2025/)
[15] BISD — [Quantum Roulette and Fraud Detection Systems](https://bisd.rs/quantum-roulette-and-fraud-detection-systems-what-every-aussie-newcomer-should-know/)
[16] ASGAM — [Study finds AI-backed advantage play on baccarat side bets becoming an increasing problem for casinos in Asia](https://asgam.com/2026/08/30/study-finds-ai-backed-advantage-play-on-baccarat-side-bets-becoming-an-increasing-problem-for-casinos-in-asia/)
[17] PMC — [AI Personalization and Its Influence on Online Gamblers' Behavior](https://pmc.ncbi.nlm.nih.gov/articles/PMC12189489/)
[18] iGaming Times — [Malta's Regulator Publishes a Voluntary AI Charter for Gaming Operators](https://igaming-times.com/news/regulatory/maltas-regulator-publishes-a-voluntary-ai-charter-for-gaming-operators)
[19] Malta Gaming Authority — [MGA launches AI Gaming Charter following extensive industry collaboration](https://www.mga.org.mt/mga-launches-ai-gaming-charter-following-extensive-industry-collaboration/)
[20] GamblingClub.be — [Digital compliance in the EU: what's at stake for gambling?](https://gamblingclub.be/en/digital-compliance-eu-whats-stake-for-gambling/)
[21] getaibook.com — [DraftKings Used AI to Find the Gamblers Most Likely to Lose, Then Targeted Them](https://getaibook.com/news/draftkings-ai-target-gamblers-likely-to-lose/)
[22] CasinoBeats — [Experts Warn AI in Casinos Could Exploit Problem Gamblers](http://casinobeats.com/2025/06/19/experts-warn-ai-in-casinos-could-exploit-problem-gamblers/)
[23] ITWeb — [AI can help curb fraud in SA's booming iGaming sector](https://www.itweb.co.za/article/ai-can-help-curb-fraud-in-sas-booming-igaming-sector/6GxRKMYQEABMb3Wj)
```
::: 

### 來源：Reference/顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1_0_0.md

[原始來源](<顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1_0_0.md>)；SHA256：`3774d18854770171e81c9323aa40962fe06f9acffd2d2c1a910db08d9d3c8f7e`。下列為未覆蓋段落；歷史主張未經收錄自動驗證。

::: {.callout-note collapse="true"}
來源第 1 行；段落 b06e932b9d74ec6c；UNKNOWN_INHERITED。

```text
# 顶级在线百家乐平台 · AI 与跨行业量化科技移植总表

```
::: 

::: {.callout-note collapse="true"}
來源第 3 行；段落 f2393c14bcf2e289；UNKNOWN_INHERITED。

```text
> **版本**：v1.0.0
> **编制日期**：2026-09-26
> **适用项目**：a168（真人百家乐风控与商业分析系统）· 世博量化® / Scibrokes Trading®
> **编制依据**：《電腦已昇級至視窗11版（工欲善其事必先利其器）.qmd》全文 7,184 行，七个 AI 区块（Claude 提问十五、Perplexity 提问三/四、DeepSeek 提问一、Copilot 提问一、Grok 提问一/二、Gemini 提问一、Meta 提问一）+ 本轮跨行业扩展
> **文件类型**：并入型章节（供 `.qmd` 直接 include 或粘贴）

```
::: 

::: {.callout-note collapse="true"}
來源第 11 行；段落 970eee58d9c19328；UNKNOWN_INHERITED。

```text
## §0 交付说明与指纹约定

```
::: 

::: {.callout-note collapse="true"}
來源第 13 行；段落 051a7b514f72a61b；UNKNOWN_INHERITED。

```text
### 0.1 六元组指纹的自指问题（须先声明）

```
::: 

::: {.callout-note collapse="true"}
來源第 15 行；段落 0307cc29c83c2915；UNKNOWN_INHERITED。

```text
本项目铁律要求每份交付件附**六元组身份锚**：文件名 + 行数 + 字节数 + MD5 + 换行符 + 编码。

```
::: 

::: {.callout-note collapse="true"}
來源第 17 行；段落 9f2d307598c2bfd0；UNKNOWN_INHERITED。

```text
但**指纹无法写在被指纹的文件内部**——写入即改变字节数与 MD5，形成自指悖论。故本件处理方式为：

```
::: 

::: {.callout-note collapse="true"}
來源第 19 行；段落 e76d44788ab0e146；UNKNOWN_INHERITED。

```text
- 文件内**不写** MD5 与字节数；
- 六元组指纹**随交付回执一并给出**，以落盘后的实测值为准；
- 本件一经落盘，**任何编辑（含空白字符、换行符转换）均使指纹失效**，须重新签发。

```
::: 

::: {.callout-note collapse="true"}
來源第 23 行；段落 604efa88786605f5；UNKNOWN_INHERITED。

```text
已知固定项：

```
::: 

::: {.callout-note collapse="true"}
來源第 25 行；段落 f01f8d9ed10b7e1d；UNKNOWN_INHERITED。

```text
| 项 | 值 |
|---|---|
| 文件名 | `顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1_0_0.md` |
| 换行符 | LF（与源 `.qmd` 一致，非 CRLF） |
| 编码 | UTF-8 无 BOM |
| 行数 / 字节数 / MD5 | 见交付回执 |

```
::: 

::: {.callout-note collapse="true"}
來源第 32 行；段落 95f62aee1ce01c13；UNKNOWN_INHERITED。

```text
> **换行符提醒**：若本件被 Windows 工具（记事本、部分 PowerShell 重定向）二次保存为 CRLF，字节数将增加恰等于行数，MD5 随之改变。按本项目铁律，遇 MD5 不合时**应先检查字节差是否等于行数**，再判定版本冲突。

```
::: 

::: {.callout-note collapse="true"}
來源第 34 行；段落 698db7d948affddf；UNKNOWN_INHERITED。

```text
### 0.2 本件与三文档铁律的关系

```
::: 

::: {.callout-note collapse="true"}
來源第 36 行；段落 364cba60eeb0824b；UNKNOWN_INHERITED。

```text
本件为**参考资料**，不是权威文档，不构成「第四份权威文件」。三份权威文件（SQL 总包 + 两份 QMD 商业报告）地位不变。本件的作用是为其提供采购与技术选型的外部对标基线。

```
::: 

::: {.callout-note collapse="true"}
來源第 38 行；段落 206b97dd4a4da412；UNKNOWN_INHERITED。

```text
### 0.3 自我更正登记

```
::: 

::: {.callout-note collapse="true"}
來源第 40 行；段落 09a0800c523625f5；UNKNOWN_INHERITED。

```text
| 编号 | 内容 |
|---|---|
| **SC-A** | 前轮对话称「主体全名册共 61 家」。本件逐一编号后**实测为 70 家**（另加 9 类监管标准体系）。原 61 为估数，未经逐条清点，属未验证陈述，现予更正。 |
| **SC-B** | 前轮对话（本对话第一轮）结论「能站得住脚的只有 Playtech、Entain、Kindred 三个具名案例」**过窄**。经全文梳理，另有 SOFTSWISS、EveryMatrix Bonus Guardian、Smartico/Optimove、Mindway AI、Octane Studios、Sentient Studios 六项具备一手或准一手证据。原结论撤回并扩充。 |
| **SC-C** | 前轮对话未指出 Meta 区块将 Evolution 的 AI 宣称标注为「官方列」系归因错误。本件以 **M-1** 正式登记。 |

```
::: 

::: {.callout-note collapse="true"}
來源第 48 行；段落 49f2217d322594b4；UNKNOWN_INHERITED。

```text
## §1 证据分级图例与三条不可逾越铁律

```
::: 

::: {.callout-note collapse="true"}
來源第 50 行；段落 b17b2a64231c6966；UNKNOWN_INHERITED。

```text
### 1.1 证据分级（强制，每条主张必带等级）

```
::: 

::: {.callout-note collapse="true"}
來源第 52 行；段落 426106020859184d；UNKNOWN_INHERITED。

```text
| 等级 | 定义 | 本件用法 |
|---|---|---|
| **OBSERVED** | 有一手来源（公司官网、年报、监管文件、公开融资公告） | 可直接引用 |
| **INFERRED** | 经第三方转述、行业媒体、供应商博客，或由已知事实推论 | 引用须标注转述链 |
| **UNKNOWN** | 检索后无任何可查证技术披露 | **不得填充推测**，须显式留白 |
| **CONDITIONAL** | 成立与否取决于未裁定的前提 | 须写明前提 |

```
::: 

::: {.callout-note collapse="true"}
來源第 59 行；段落 d5b9e888c5ecb702；UNKNOWN_INHERITED。

```text
**证据等级不因重复计算而自动升级。** 实测为零的层照常出列。`NULL`（未定义/未测）≠ `0`（实测零）≠ 缺失。

```
::: 

::: {.callout-note collapse="true"}
來源第 61 行；段落 4c31fdd2c0f29160；UNKNOWN_INHERITED。

```text
### 1.2 三条铁律（贯穿全表，不因任何技术先进性放宽）

```
::: 

::: {.callout-note collapse="true"}
來源第 63 行；段落 556900a2255d3cb3；UNKNOWN_INHERITED。

```text
1. **AI 永不进入牌局结果**：不得对单一玩家调整赔率、牌靴、发牌、RNG、派彩或游戏结果。
2. **RL / bandit 的 reward 只能是保护性指标**：风险下降、限额采纳、冷静期完成、投诉减少、人工审核质量。**禁止** GGR / NGR / 入金 / 投注额 / 游戏时长 / 回流投注 / 返水转化。
3. **RG 数据与营销系统必须格结构或物理隔离**（Bell-LaPadula 不上读不下写 / 数据二极管），而非「制度禁止」。

```
::: 

::: {.callout-note collapse="true"}
來源第 69 行；段落 b666e96296f30dff；UNKNOWN_INHERITED。

```text
| 价值 | 合法且可验证的目标 | 核心 KPI | **绝不可计入的「收益」** |
|---|---|---|---|
| **止损** | 减少经**人工确认**的欺诈、串通、代理套利、红利滥用、支付异常与流程差错损失 | 确认损失避免额、Precision@人工产能、漏报率、案件处理时长、**误伤率** | 因限制正常会员而减少的正常派彩；拒绝合法提款 |
| **增效** | 同等人力处理更多、更高质量案件；降低数据处理、排查、对账、报告成本 | 每审核人日闭环案件数、平均结案时长、自动证据覆盖率、人工复核命中率、每确认案件成本 | 高风险/脆弱会员投注增加、回流投注、追损延长 |
| **合规** | 更早识别风险、降低伤害与审计缺陷，处置可解释、可撤销 | 强风险信号响应时延、人工复核率（须 100%）、申诉成功率、审计证据完备率、限额/冷静期采纳率 | 将 RG 风险分数用于 VIP、奖励、优惠或定向营销 |

```
::: 

::: {.callout-note collapse="true"}
來源第 77 行；段落 20db7ce02df1bd08；UNKNOWN_INHERITED。

```text
## §2 主体全名册（70 家 + 9 类监管标准体系）

```
::: 

::: {.callout-note collapse="true"}
來源第 79 行；段落 3ba5e8e9ce2e3fe7；UNKNOWN_INHERITED。

```text
### A. B2B 真人内容与直播供应商（16 家 · 与真人百家乐最直接）

```
::: 

::: {.callout-note collapse="true"}
來源第 81 行；段落 38afb39ee9ec3a08；UNKNOWN_INHERITED。

```text
| # | 主体 | 百家乐产品 | 所载 AI / 自动化 | 证据等级 |
|---|---|---|---|---|
| 1 | **Evolution** | Speed / Lightning / First Person Baccarat | 摄像头→计算机视觉→牌面识别→实时结算→自动风控→后台告警；宣称 AI-Powered Fraud Detection、Biometric Dealer Authentication、Advanced AI Monitoring、GLI Certified RNG；CPO Todd Haushalter 谈 AI 革新老虎机生产；招聘要求数据科学家掌握 Scikit-Learn / TensorFlow / PyTorch / Pandas / Spark，用于推荐系统、欺诈检测、聊天文本分析 | 真人娱乐地位 **OBSERVED**；AI 宣称 **INFERRED**（见 M-1） |
| 2 | **Ezugi**（Evolution 旗下） | EZ Baccarat、Ultimate Auto Roulette（全自动无荷官） | EZ Baccarat 主打 hands-per-hour 最快的自动化节奏 | OBSERVED |
| 3 | **Playtech**（Playtech Live） | Prestige Baccarat | IMS 平台自适应欺诈模型与玩家推荐；BetBuddy AI；Featurespace ML 实时反欺诈整合；Playtech Protect；托管服务宣称 AI-Driven Automation | OBSERVED |
| 4 | **Pragmatic Play Live** | Mega Baccarat | Bet Behind Pro Blackjack 用 **7 个 Bot** 坐桌按基础策略自动决策；Auto-Roulette 无荷官自动发球；AI 运营分析、自动营销、CLM、风险模型 | 半自动化 **OBSERVED**；AI 运营 **INFERRED** |
| 5 | **SA Gaming** | 百家乐、龙虎、骰宝、炸金花、牛牛等 | Copilot 称有自动风险监控、自动赔率管理、实时告警；PAGCOR 牌照；Gaming Labs / BMM Testlabs 认证；新获南非 WCGRB 牌照 | **UNKNOWN**（无一手技术披露） |
| 6 | **Dream Gaming (DG)** | 百家乐、竞咪百家乐、龙虎、牛牛、骰宝、炸金花、轮盘、色碟、鱼虾蟹 | 推测 AI Fraud Detection + AML Monitoring + Player Segmentation | **UNKNOWN** |
| 7 | **WM Casino（完美真人 / WM Perfect Group）** | 真人百家乐 | 定位为 Live Casino Provider + Streaming Platform + Gaming Ecosystem 三合一 | **UNKNOWN** |
| 8 | **Asia Gaming (AG)** | 首创 Interactive Bid Baccarat；VIP 包房可控游戏节奏与荷官 | 无 | **UNKNOWN** |
| 9 | **AllBet** | 真人百家乐 | 无 | **UNKNOWN** |
| 10 | **Sexy Baccarat / AE Sexy** | 真人百家乐 | 仅见于东南亚代理导流站列举 | **UNKNOWN** |
| 11 | **Pretty Gaming** | 真人桌台 | 同上 | **UNKNOWN** |
| 12 | **Venus Casino** | 真人桌台 | 同上 | **UNKNOWN** |
| 13 | **Big Gaming** | 真人桌台 | 同上 | **UNKNOWN** |
| 14 | **eBet** | 真人桌台 | 同上 | **UNKNOWN** |
| 15 | **BetGames.TV** | 真人桌台 | 同上 | **UNKNOWN** |
| 16 | **KingMaker** | 真人桌台 | 同上 | **UNKNOWN** |

```
::: 

::: {.callout-note collapse="true"}
來源第 100 行；段落 175c11bb8aff7d99；UNKNOWN_INHERITED。

```text
> **采购裁定**：#5–#16 共 12 家（亚洲系）**仅作去荷官速度与桌台密度对标，不纳入 AI 采购**。其公开渠道无模型卡、数据集或审计报告；其「自动」仅指无荷官机械发牌，非智能决策。将其列为 AI 平台属营销误植。

```
::: 

::: {.callout-note collapse="true"}
來源第 102 行；段落 ee5eb80ec9f9ed05；UNKNOWN_INHERITED。

```text
### B. B2C 运营商与集团（13 家）

```
::: 

::: {.callout-note collapse="true"}
來源第 104 行；段落 c1bd34ef4a9b80b8；UNKNOWN_INHERITED。

```text
| # | 主体 | AI 系统 | 关键参数 | 证据等级 |
|---|---|---|---|---|
| 17 | **Entain** | **ARC**（Advanced Responsibility & Care）+ Protector Model | 26 个保护标记（Perplexity）／近 30 个行为标记（Forbes，M-2）；22 市场第一阶段、9 市场第二阶段实时互动；准确度宣称 >90%；已整合 Mindway | OBSERVED（数字冲突） |
| 18 | **Flutter Entertainment** | **Real Time Intervention (RTI)** / Real Time Check In | 自 Sportsbet 起源扩展至集团品牌；年报确认 ML/AI/数据科学用于产品、服务、基础设施；有 Responsible AI 政策 | OBSERVED |
| 19 | **FanDuel**（Flutter 旗下） | 集团 RTI 覆盖 | — | OBSERVED |
| 20 | **PokerStars**（Flutter 旗下） | 集团 RTI 覆盖 | — | OBSERVED |
| 21 | **Sportsbet**（Flutter 旗下） | **RTI 发源地** | — | OBSERVED |
| 22 | **Betfair**（Flutter 旗下） | AI 用于欺诈检测、客户支持、用户体验 | — | INFERRED |
| 23 | **Kindred Group** | **PS-EDS**（Player Safety – Early Detection System） | 智能算法识别有害行为演变；另用于客户分层、欺诈防范 | OBSERVED |
| 24 | **Unibet**（Kindred 旗下） | PS-EDS 覆盖 | — | OBSERVED |
| 25 | **BetMGM** | Optimove 客户 | 全渠道营销自动化、预测模型与队列分析 | OBSERVED（供应商案例） |
| 26 | **DraftKings** | ⚠ **反面案例** | 纽约时报调查：用 ML 识别**最可能输钱**的客户并定向发放免费投注，问题博彩检测工具被搁置 | **INFERRED**（经 getaibook.com 转述，非 NYT 原文，M-5） |
| 27 | **Sisal** | Optimove 客户 | 玩家未来价值 +36%、总存款 +23%、NGR +28%、忠诚客户毛收入 +89% | 供应商案例 |
| 28 | **Stardust** | Optimove 客户 | MAU ×3、独立存款人 +37%、净收入 +51% | 供应商案例 |
| 29 | **OPAP** | ComplianceSuite.ai 客户 | 自动化可扩展风险管理 | 供应商案例 |

```
::: 

::: {.callout-note collapse="true"}
來源第 120 行；段落 2b9d5474491da9ff；UNKNOWN_INHERITED。

```text
### C. B2B 平台 / PAM / CRM（6 家 · RL 唯一公开落地处）

```
::: 

::: {.callout-note collapse="true"}
來源第 122 行；段落 03c37e85aae655b3；UNKNOWN_INHERITED。

```text
| # | 主体 | 产品 | 能力 | 证据等级 |
|---|---|---|---|---|
| 30 | **SOFTSWISS** | Casino Platform、**Anti-Fraud Service**、**BM3**（业务指标监控）、**DOSSIER**（玩家 LTV 预测） | 实时 ML 检测可疑案件提交人工复核；2022 处理 61,810 请求省 €16M+；2023 处理 100,000+ 请求省 €13M；2025 续有 €15M+ 级防护；AI 可连接卡号—账户—邮箱—设备指纹揭示钱骡链与有组织犯罪网络；COO 明言最终决策仍应留给专家 | OBSERVED |
| 31 | **EveryMatrix** | **CasinoEngine**、**Bonus Guardian** | 用已知滥用者历史训练 ML，分析大量行为模式，标记红利滥用，按角色配置条件与动作（奖金排除、提款冻结） | OBSERVED |
| 32 | **Smartico**（据称已被 Optimove 收购，M-4） | 游戏化引擎、CRM | **文档明确写有 contextual bandits / RL 工作台**：RL 调整任务难度、时机与奖励以维持心流；MAB 算法实时测试多种奖励类型自动选最优；RNN 时序模型预测 7/14/30 天流失（准确率 75.94%）；触发动态奖励、渠道选择与慷慨度分级 | **全对话唯一明确的 RL 落地证据** |
| 33 | **Optimove** | **Opti-X** | Pragmatic Play 采用；集成 20+ ML 推荐模型；AI 站内搜索与动态内容个性化；覆盖 700+ 游戏标题；实时玩家推荐与可扩展奖金执行 | OBSERVED |
| 34 | **GiG** | AI 推荐引擎 | 报告可提升留存、降低假阳性 | INFERRED |
| 35 | **NuxGame** | 配 iDenfy | AI 文档分析嵌入赌场软件，自动化 KYC/AML | OBSERVED |

```
::: 

::: {.callout-note collapse="true"}
來源第 131 行；段落 a1011802b187b1de；UNKNOWN_INHERITED。

```text
### D. AI 风控 / 反欺诈 / KYC / AML 供应商（22 家）

```
::: 

::: {.callout-note collapse="true"}
來源第 133 行；段落 49423ef5102900b3；UNKNOWN_INHERITED。

```text
| # | 主体 | 类别 | 能力要点 | 证据等级 |
|---|---|---|---|---|
| 36 | **Featurespace ARIC** | 交易监控 | 剑桥 Bill Fitzgerald 创立；自适应行为分析、动态风险评分；Playtech 2018-01 完成整合；原服务银行业 | OBSERVED |
| 37 | **SEON** | 设备/行为 | 设备指纹、数字足迹、账户盗用、红利滥用 | INFERRED（供应商披露） |
| 38 | **GeoComply** | 地理位置 | 基于 **2 亿+ 设备安装网络**的 ML 威胁检测 | INFERRED |
| 39 | **Sumsub** | KYC | 文档+活体+生物识别、持续再筛查、深伪检测 | INFERRED |
| 40 | **Onfido** | KYC | 同上 | INFERRED |
| 41 | **Jumio** | KYC | 同上 | INFERRED |
| 42 | **Veriff** | KYC | 同上 | INFERRED |
| 43 | **iDenfy** | KYC | 与 NuxGame 集成 | OBSERVED |
| 44 | **Shufti** | KYC | 与 Cevro AI 集成 | OBSERVED |
| 45 | **CrossClassify** | 设备/行为 | 账户盗用与异常交易 | INFERRED |
| 46 | **Sift** | 行为/支付 | 实时行为与支付风险情报 | INFERRED |
| 47 | **Group-IB** | 客户端反欺诈 | 含可解释 AI（XAI） | INFERRED |
| 48 | **cside** | 浏览器层 | 每会话分析 **250+ 浏览器信号**，可识别 OpenAI Operator、Claude for Chrome、Playwright、Puppeteer、Selenium，在注册请求到达服务器前完成标记 | INFERRED |
| 49 | **Flagright** | AML+RG 统一 | 统一案件管理，共享玩家上下文、审计日志、SAR 起草 | INFERRED |
| 50 | **ComplyAdvantage** | AML | 制裁与 PEP 筛查 | INFERRED |
| 51 | **NICE Actimize** | AML | 交易监控、SAR/STR | INFERRED |
| 52 | **ACT（Fraud Rings）** | 图谱串通 | 2026 年新增 syndicate 可视化，设备/IP/行为关联 | INFERRED |
| 53 | **Infocredit Group（ComplianceSuite.ai）** | 合规平台 | 2025 Compliance Awards AML/CFT 金奖与白金奖；OPAP 采用 | INFERRED |
| 54 | **Cevro AI** | 客服 Agent | 域专用 LLM（基于 iGaming 工作流与合规框架训练），自主解决 **80–90%** 复杂工单，支持 **100+ 语言**，内置信任层控制 | INFERRED |
| 55 | **InteractiveAI** | 客服 Agent | 受合规边界约束的 AI 代理 | INFERRED |
| 56 | **Moveo.AI** | 客服 Agent | 同上；与 SOFTSWISS / Smartico / Zendesk 集成 | INFERRED |
| 57 | **Quantexa** | 实体解析+图谱 | 银行业 AML 标杆（跨行业引入） | 跨行业 OBSERVED |

```
::: 

::: {.callout-note collapse="true"}
來源第 158 行；段落 d34e844d6a0fe18e；UNKNOWN_INHERITED。

```text
### E. 责任博彩 AI（新增 3 家 + 3 项已计入主体的产品）

```
::: 

::: {.callout-note collapse="true"}
來源第 160 行；段落 97b9cbea956290c2；UNKNOWN_INHERITED。

```text
| # | 主体 / 产品 | 能力 | 关键参数 | 证据等级 |
|---|---|---|---|---|
| 58 | **Mindway AI**（GameScanner / Gamalyze） | AI + 神经科学 + 专家评估的「虚拟心理学家」；Gamalyze 为神经科学游戏化自测 | 每月监测全球 **1,470 万活跃玩家**（跨多运营商汇总，**非自有会员**）；宣称检出人类专家案例的 **≥87%**；已成 Entain ARC 组成部分 | OBSERVED（数字为供应商自述） |
| 59 | **Neccton**（Mentor） | 问题赌博早期检测 | — | INFERRED |
| 60 | **Sportradar**（Bettor Sense） | 模式识别 + session 分析，主动检测伤害早期迹象 | — | INFERRED |
| — | **Playtech BetBuddy**（#3 产品） | 三层风险评级模型；ML **提前数周**预测风险；个性化干预 | 三大洲 **15 或 17** 个司法管辖区（M-3）；对照试验显示 **15% 高风险玩家在收到 AI 个性化消息后一小时内主动设置存款限额**；与西弗吉尼亚大学博彩研究与发展中心合作 | OBSERVED |
| — | **Entain ARC**（#17 产品） | 见 B 区 | — | OBSERVED |
| — | **Kindred PS-EDS**（#23 产品） | 见 B 区 | — | OBSERVED |

```
::: 

::: {.callout-note collapse="true"}
來源第 169 行；段落 43e16ccec41c38c5；UNKNOWN_INHERITED。

```text
### F. AI 荷官新势力（2 家 · 2026 年前台自动化，**独立成章，不得与 Evolution 同表**）

```
::: 

::: {.callout-note collapse="true"}
來源第 171 行；段落 e06d01e045879184；UNKNOWN_INHERITED。

```text
| # | 主体 | 状态 | 证据等级 |
|---|---|---|---|
| 61 | **Octane Studios** | **AI Baccarat 首发**；可定制品牌化 AI 荷官；认证 RNG + provably fair；品牌方数日内交付 | OBSERVED（行业媒体 + 产品发布） |
| 62 | **Sentient Studios（原 BetHog）** | FanDuel 联创 **Nigel Eccles** 关闭 crypto 赌场全力转 B2B；AI 荷官 **Sunny** 实时对话+表情+肢体同步；宣称参与度为真人台 **10 倍**；**12 种语言**；**$10M A 轮**（2026-04）；Blackjack 已上线，**百家乐与轮盘预计 2026 年底** | OBSERVED（融资公告 + iGB 专访） |

```
::: 

::: {.callout-note collapse="true"}
來源第 176 行；段落 0ce16fb92be55e3e；UNKNOWN_INHERITED。

```text
**二者共同架构原则（唯一可接受的形态）**：
> **RNG 引擎与渲染引擎强制分离** —— 发牌结果由**已认证 RNG** 决定，AI 仅负责拟真表达、对话与情绪同步，以规避「AI 知道底牌」的信任风险。其监管路径被描述为「本质上是 RNG 产品」而非 Live。

```
::: 

::: {.callout-note collapse="true"}
來源第 179 行；段落 d1cd0e8e128a3c9e；UNKNOWN_INHERITED。

```text
**Evolution 的态度**：高层保留，曾贬低 AI 荷官为 deepfake；Eccles 以 De Beers 对实验室钻石类比，指其存在**创新者困境**（60%+ Live 市占与高 EBITDA 护城河依赖真人工作室与品牌信任，公开贬低后再拥抱将自我蚕食）。

```
::: 

::: {.callout-note collapse="true"}
來源第 181 行；段落 52fecd87484a37ca；UNKNOWN_INHERITED。

```text
### G. 实体 / 混合智慧桌（2 家）

```
::: 

::: {.callout-note collapse="true"}
來源第 183 行；段落 b5cfb42bbb55fc63；UNKNOWN_INHERITED。

```text
| # | 主体 | 能力 | 证据等级 |
|---|---|---|---|
| 63 | **Angel Group** | AI 智慧百家乐桌（已在澳门等地部署），**姿势辨识 + RFID** 追踪下注与玩家，超越传统 RFID，提升数据品质、合规监控与楼面分析 | OBSERVED |
| 64 | **IDX Games** | AI chatbot 分析百家乐等桌游数据，提供运营洞察 | INFERRED |

```
::: 

::: {.callout-note collapse="true"}
來源第 188 行；段落 baeb21cd88025547；UNKNOWN_INHERITED。

```text
### H. 玩家端第三方工具（6 项 · **敌方，必须反制的对象**）

```
::: 

::: {.callout-note collapse="true"}
來源第 190 行；段落 4338f25acb97fb65；UNKNOWN_INHERITED。

```text
| # | 工具 / 主体 | 宣称能力 | 证据等级 |
|---|---|---|---|
| 65 | **FPLAY** | 多平台 API 自动下注、智能决策；支持 DG、WM、AllBet、DG、WG 等 | INFERRED（工具官网） |
| 66 | **Mysports.AI** | 自动读牌、**剩余牌分布计算**、Telegram 推播高 EV 机会、多桌支持 | INFERRED |
| 67 | **Oracle Baccarat Predictor** | ML 预测路单 | INFERRED |
| 68 | **BACC.BOT** | 深度学习模型 | INFERRED |
| 69 | **BaccaratAI** | 深度学习模型 | INFERRED |
| 70 | **Differential Labs**（研究方） | 百家乐**边注占亚洲赌场 40–60% 收入**；AI 辅助算牌已成优势玩家新工具；亚洲市场估计**年损 5–7 亿美元** | OBSERVED（ASGAM 2026-08-30 报导） |

```
::: 

::: {.callout-note collapse="true"}
來源第 199 行；段落 08bd938e3e64d632；UNKNOWN_INHERITED。

```text
**附：cside 可识别的自动化代理**（非公司，为技术栈）：OpenAI Operator、Claude for Chrome、Playwright、Puppeteer、Selenium。

```
::: 

::: {.callout-note collapse="true"}
來源第 201 行；段落 8327fe54210b533d；UNKNOWN_INHERITED。

```text
> **裁定**：此类工具是平台的**对抗方**，不是可采购对象。**#70 的「年损 5–7 亿美元」是本对话中最大的单一止损标的。** 平台通常禁止或限制 bot 与自动化投注。

```
::: 

::: {.callout-note collapse="true"}
來源第 203 行；段落 75ae12d422d5f421；UNKNOWN_INHERITED。

```text
### I. 监管、标准与学术（9 类体系）

```
::: 

::: {.callout-note collapse="true"}
來源第 205 行；段落 4e8856920ac4fc87；UNKNOWN_INHERITED。

```text
| 类 | 体系 | 强制性 | 核心要求 |
|---|---|---|---|
| I-1 | **MGA AI Gaming Charter**（2026-09-18，与马耳他数字创新局联合发布） | **自愿** | AI 系统清单、问责人、人工覆盖、透明度、非歧视、审计轨迹；涵盖玩家保护、反欺诈、客户交互、运营决策；**明确警告「AI washing」** |
| I-2 | **UKGC LCCP 3.4.3** | 强制 | 强风险指标须**及时自动化处理**，**但个案须人工审核并允许客户异议** |
| I-3 | **EU AI Act** | 强制 | 欺诈检测、行为追踪、个性化推荐、聊天机器人可能归类**高风险**；**第 12 条记录保存**；需技术参数、透明度、风险管理、人工监督 |
| I-4 | **GDPR 第 22 条** | 强制 | 自动化决策的解释权与异议权 |
| I-5 | **NIST AI RMF** | 框架 | Govern → Map → Measure → Manage |
| I-6 | **ISO/IEC 42001** | 认证 | AI 管理体系 |
| I-7 | **游戏认证机构** | 强制 | **GLI、eCOGRA、BMM Testlabs、Gaming Labs** —— RNG 与游戏公平性认证 |
| I-8 | **牌照机构** | 强制 | **PAGCOR**（菲律宾）、**WCGRB**（南非西开普）、MGA、UKGC |
| I-9 | **学术** | — | **西弗吉尼亚大学博彩研究与发展中心**（与 Playtech BetBuddy 合作）；**PMC 论文**《AI Personalization and Its Influence on Online Gamblers' Behavior》 |

```
::: 

::: {.callout-note collapse="true"}
來源第 217 行；段落 fb1c4f65655c4a1c；UNKNOWN_INHERITED。

```text
**跨行业引入的标准体系**（本件 §4 展开）：
ALCOA+ · 21 CFR Part 11 · GAMP 5 / IQ-OQ-PQ · DO-178C · IEC 61508 SIL · ISO 26262 ASIL · NERC CIP · CCSDS · ECSS-E-ST-40 · BCBS 239 · SR 26-2（取代 SR 11-7）· FATF 40 建议 · ISO 20022 · ISO/IEC 25012 · ISO/IEC 5259 · ISO 8000 · ISO 31000:2018 · OECD AI Principles · MITRE ATT&CK · Sigma · SLSA · SPDX / CycloneDX · STAC-M3 · FAIR 原则

```
::: 

::: {.callout-note collapse="true"}
來源第 222 行；段落 d7d7848581c730e0；UNKNOWN_INHERITED。

```text
## §3 矛盾清单（跨 AI 说法冲突，采购与引用前须裁定）

```
::: 

::: {.callout-note collapse="true"}
來源第 224 行；段落 2ee5922f44b9f45e；UNKNOWN_INHERITED。

```text
| 编号 | 冲突内容 | 裁定建议 | 状态 |
|---|---|---|---|
| **M-1** | Meta 区块称「Evolution **官方列** AI-Powered Fraud Detection、Biometric Dealer Authentication」，但其引注 [6] newcasinorank.com、[7] **illawiki.com**、[15] bisd.rs —— 三者均为联盟营销 / SEO 内容农场，**非 evolution.com** | **归因错误，必须降级**。Evolution 的 AI 宣称目前只能定为 INFERRED，不得写成「官方披露」。**这是全文最严重的证据污染** | 已裁定 |
| **M-2** | Entain ARC 行为标记数：Perplexity 称 **26 个**，Claude 引 Forbes 称**近 30 个** | 二者时点不同（2022 vs 后续），**须注明时点，不可择一**（三读法全出列） | UNRESOLVED |
| **M-3** | BetBuddy 司法管辖区数：DeepSeek 称**三大洲 15 个**，Meta 称 **17 个** | 未裁定前**并列出列** | UNRESOLVED |
| **M-4** | Grok 与 Meta 称「Smartico 已被 Optimove 收购」，DeepSeek 与 Gemini 仍将二者并列为独立产品 | **采购前须独立核实** | UNRESOLVED |
| **M-5** | DraftKings 案例引自 getaibook.com（聚合站）转述纽约时报，非 NYT 原文 | 降级为 INFERRED；引用须回溯原始报导 | 已裁定 |
| **M-6** | SOFTSWISS 2023 年请求量（100,000+）**高于** 2022 年（61,810），节省金额却**低于**（€13M < €16M） | 单位/口径不可比，**禁止跨年度比较**；与本项目「161,156 分母已作废」同类问题 | 已裁定 |
| **M-7** | Gemini 推荐 **StarRocks / ClickHouse / SeaTunnel / DolphinScheduler**；Perplexity 明确写「鉴于您要求不连接 Superset、DolphinScheduler、StarRocks」 | **Gemini 的建议直接违反本项目现行禁令，不得采纳** | 已裁定 |
| **M-8** | 前轮 Claude 结论「只有 Playtech、Entain、Kindred 三个具名案例站得住脚」 | **本件撤回并扩充为九项**（见 SC-B） | 已裁定 |
| **M-9** | Copilot 建议将 Octane / Sentient / AI Dealer 独立成章，不与 Evolution 同层 | **采纳**，证据层级不同不得并表 | 已裁定 |
| **M-10** | 「Flutter、Evolution、EveryMatrix、Mindway 活跃会员超 1,400 万」 | **口径错误**：Mindway 的 1,470 万是**跨多家运营商汇总的每月监测玩家数**，非自有会员；Evolution 与 EveryMatrix 属 B2B，**不持有会员账户**；Flutter 为 AMP 月均活跃玩家。**四者分属三种商业模式，不可并列更不可相加** | 已裁定 |
| **M-11** | 「每个会员都需要以纳秒速度互动」 | **物理上不成立**：真人百家乐的会员互动被视频（LL-HLS 2–10 s / WebRTC 0.2–1 s）与人眼（反应时间 200–300 ms）锁死在数百毫秒以上，比纳秒慢 6–7 个数量级。**纳秒只存在于 CPU 缓存（1–10 ns）、无锁环形队列（20–100 ns）、FPGA 线到线（10–100 ns）**。正确指标是**吞吐 × 扇出 × 尾延迟**，而非 latency 本身 | 已裁定，见 §4.0 |

```
::: 

::: {.callout-note collapse="true"}
來源第 240 行；段落 6224593df414de20；UNKNOWN_INHERITED。

```text
## §4 跨行业技术移植图（13 个行业）

```
::: 

::: {.callout-note collapse="true"}
來源第 242 行；段落 a55af31f4aadc8a6；UNKNOWN_INHERITED。

```text
### 4.0 前置：延迟阶梯与真实规模锚（斧正 M-11）

```
::: 

::: {.callout-note collapse="true"}
來源第 244 行；段落 a64e53e7fe973af4；UNKNOWN_INHERITED。

```text
| 环节 | 真实延迟 | 量级 |
|---|---|---|
| CPU L1/L2 缓存命中 | 1–10 ns | **ns** |
| 无锁环形队列（Disruptor / Aeron）单次入出队 | 20–100 ns | **ns** |
| 内存随机访问（DRAM） | 80–100 ns | **ns** |
| FPGA 线到线（金融撮合 / 做市） | 10–100 ns | **ns** |
| 本机 IPC（Chronicle Queue） | 100 ns – 1 μs | μs |
| 内核旁路网络收发（DPDK / ef_vi） | 1–5 μs | μs |
| RDMA 单边读 | 1–2 μs | μs |
| 内存 KV 网络往返（Redis） | 50–200 μs | μs |
| 同城网络 RTT | 0.5–2 ms | ms |
| Kafka 端到端 p99 | 2–20 ms | ms |
| Flink 有状态算子 | 1–50 ms | ms |
| OLAP 交互查询（ClickHouse / StarRocks） | 50–500 ms | ms |
| **人类反应时间** | **200–300 ms** | ms |
| WebRTC 低延迟直播 | 200 ms – 1 s | s |
| LL-HLS / HLS 直播 | 2–10 s | s |
| 跨洲 RTT | 100–300 ms | ms |
| **百家乐单局（Speed Baccarat ~27 s）** | **25–48 s** | s |
| **下注窗口** | **12–20 s** | s |

```
::: 

::: {.callout-note collapse="true"}
來源第 265 行；段落 3f4392baaeeae536；UNKNOWN_INHERITED。

```text
**结论：纳秒该花在平台内部的事件总线与风控内存计算上，让风控判决在下注窗口关闭前完成；花在「会员互动」上会被视频流与人眼全部吃掉。**

```
::: 

::: {.callout-note collapse="true"}
來源第 267 行；段落 693e4d63ebf9348d；UNKNOWN_INHERITED。

```text
**规模锚粗算**（以 1,400 万注册、并发活跃 3–5% 为例）：

```
::: 

::: {.callout-note collapse="true"}
來源第 269 行；段落 3e7686a71f3a96b9；UNKNOWN_INHERITED。

````text
```
在线并发      ≈ 1.4e7 × 4%           ≈ 5.6e5
注单写入峰值  ≈ 5.6e5 × 1.5 注/分 ÷ 60 ≈ 1.4e4 TPS
风控特征扇出  ≈ 1.4e4 × 30 特征       ≈ 4.2e5 events/s
```

````
::: 

::: {.callout-note collapse="true"}
來源第 275 行；段落 001c97dd2a8224fd；UNKNOWN_INHERITED。

```text
**此量级不需要 FPGA。** Kafka / Redpanda + Flink 或内存状态即可胜任。真正难点是三件：
① **p99.9 尾延迟**须稳定在下注窗口内；
② **扇出后的状态一致性**（同一会员在 8 张桌同时下注）；
③ **突发峰值**（大赛事、大额会员进场）下的背压与降级。

```
::: 

::: {.callout-note collapse="true"}
來源第 280 行；段落 172e2f94d0e83922；UNKNOWN_INHERITED。

```text
> **B2B 供应商的规模指标是「承载运营商数 × 桌台数 × 每小时局数」，B2C 运营商才有会员数。** a168 属前者下游，规模锚应为**桌台 × 局 × 注单**。

```
::: 

::: {.callout-note collapse="true"}
來源第 282 行；段落 f2d9e40156212e10；UNKNOWN_INHERITED。

```text
### 4.1 十三行业移植总表

```
::: 

::: {.callout-note collapse="true"}
來源第 284 行；段落 b78b841b3d71112f；UNKNOWN_INHERITED。

```text
| # | 行业 | 最值得落地的**一件事** | 软件 / 程序包 | 归格 | 同构度 |
|---|---|---|---|---|---|
| 1 | **金融 / 量化 / HFT** | **元标签**（一层判异常，二层判该不该出手）+ **CPCV + PBO + Deflated Sharpe** 防回测过拟合 | 自实现 purged CV；`arch`、`linearmodels`、`skfolio`；⚠ `mlfinlab` 已转商业授权，勿入依赖 | 止损+合规 | ★★★★★ |
| 2 | **银行业** | **拒绝推断**（被封禁会员无后续行为→选择偏差；银行业解了四十年）+ **WOE/IV 评分卡**作可解释基准 | `scorecardpy`、`optbinning`、`toad`；R `scorecard`、`smbinning` | 止损+合规 | ★★★★★ |
| 3 | **电商业** | **CUPED 方差缩减**（等效样本 ×2–5）+ **point-in-time 特征一致性** | `feast`；CUPED 手工实现；`confseq`（永远有效 p 值） | 增效+合规 | ★★★★☆ |
| 4 | **科技 / SRE / 数据工程** | **OpenLineage 血缘** —— 「血统关系」的机器可读完全形态 | `openlineage-python`、`marquez`、`datahub`、`dbt`；**R 原生首选 `targets`** | 增效+合规 | ★★★★★ |
| 5 | **资安 / 网管** | **Sigma 规则 + MITRE ATT&CK 三层重构 registry** + **UEBA 同伴群组分析** | `pySigma`、`sigma-cli`、`mitreattack-python`、ATT&CK Navigator | 止损+合规 | ★★★★★ |
| 6 | **反恐 / 反诈骗风控** | **Splink 概率实体解析**（千万级，输出匹配概率而非布尔）+ **k-core / Leiden / TGN** | `splink`、`cdlib`、`leidenalg`、`graspologic`、`torch-geometric-temporal`；R `fastLink`、`reclin2` | 止损 | ★★★★★ |
| 7 | **人工智能业** | **PU Learning + Snorkel 弱监督 + 主动学习** —— 直击 a168 唯一致命缺口 | `pulearn`、`snorkel`、`modAL`、`small-text`、`baal`；漂移 `river`、`frouros`、`alibi-detect` | 止损+增效 | ★★★★★ |
| 8 | **宇航生态产业链** | **IMM 交互多模型状态估计**（风险非静态分数，而是带不确定度的在线状态）+ **FDIR 自动降级** | **`stone-soup`**（Dstl 开源，含 MHT/JPDA/IMM）、`filterpy`、`pykalman` | 止损+合规 | ★★★★☆ |
| 9 | **军工 / 国防生态产业链** | **TEWA 最优分配**取代「按分排序取前 K」+ **MHT 多假设**取代一次性聚类 | `ortools`、`scipy.optimize.linear_sum_assignment`、`stone-soup` | 增效 | ★★★★★ |
| 10 | **民生与管制（制药/电力/航空/核能）** | **ALCOA+ 九原则** + **21 CFR Part 11** + **IQ/OQ/PQ 门禁** + **FMEA RPN** | 规范落地（无需软件）；不变量机器验证 `z3-solver` | 合规 | ★★★★★ |
| 11 | **科学研究院** | **预注册** + **负对照结局 + E-value** 量化未测量混杂 | R **`EValue`**、`sensemakr`；`targets` 保证可重复；`p.adjust` / `statsmodels.stats.multitest` | 合规 | ★★★★★ |
| 12 | **确定性系统（三链共通）** | **优雅降级优于失败**：模型不可用→退规则，规则不可用→退人工队列 | 架构约束 | 合规 | ★★★★★ |
| 13 | **供应链安全** | **SBOM**（`renv.lock` + `requirements.lock` → CycloneDX） | `cyclonedx-python`、`syft`、`grype`、`trivy`；R `renv` | 合规 | ★★★★☆ |

```
::: 

::: {.callout-note collapse="true"}
來源第 300 行；段落 12bde207840520b8；UNKNOWN_INHERITED。

```text
### 4.2 各行业技术细目

```
::: 

::: {.callout-note collapse="true"}
來源第 302 行；段落 35320ce46af5b543；UNKNOWN_INHERITED。

```text
#### 4.2.1 金融业 / 高频交易 / 量化投资基金 ★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 304 行；段落 c93e2d18814363ff；UNKNOWN_INHERITED。

```text
**同构映射**：注单流 ≡ tick stream｜会员 ≡ instrument｜桌台/荷官 ≡ venue / market maker｜同桌串通 ≡ wash trading / 关联交易｜ROI 分层持续性 ≡ 因子 IC 衰减与半衰期。

```
::: 

::: {.callout-note collapse="true"}
來源第 306 行；段落 aa184a453c43e8e0；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **硬件** | FPGA（AMD Alveo、Intel Agilex）、SmartNIC/DPU（NVIDIA BlueField、Xilinx X2/X3 + Onload）、**PTP/PPS 授时**（White Rabbit 可达亚纳秒）、原子钟 / GNSS 守时 | **授时是刚需**：`bet06`（开注）、`bet08`（下注）、结算时间若跨机房时钟漂移 >10 ms，「迟下注」判定即失效。**PTP grandmaster 是最低成本最高回报的硬件投入；FPGA 不需要** |
| **确定性低延迟** | CPU pinning、`isolcpus`、HugePages、NUMA 亲和、禁用 C-state、内核旁路（DPDK / ef_vi）、RDMA / RoCEv2 | 用于风控判决路径，使 p99.9 可预测 |
| **无锁与消息** | **LMAX Disruptor**、**Aeron**、**Chronicle Queue/Map**（堆外持久化，无 GC）、**Redpanda**（C++ Kafka 兼容，无 JVM GC 抖动）、Seastar / ScyllaDB | Disruptor 是「纳秒」在百家乐里唯一成立的落点：注单事件总线 |
| **Tick 数据库** | **kdb+/q**、**ArcticDB**（Man Group 开源）、**QuestDB**、**DolphinDB**、TimescaleDB、**Arrow Flight**、Substrait | ArcticDB 免费且 Python 原生，是 kdb+ 的现实替代 |
| **方法论** | **三重障碍法 + 元标签**（López de Prado）、**分数阶差分**、**Purged K-Fold + Embargo**、**CPCV**、**PBO**、**Deflated Sharpe Ratio**、**TCA**、Almgren-Chriss、Kelly | **元标签是 a168 关键武器**：第一层判「是否异常」，第二层判「该不该出手」—— 恰好解决有限人工产能下的出手/不出手问题。CPCV 与 PBO 直接对治「多窗口择优」过拟合 |
| **基准** | **STAC-M3**、STAC-A2 | 选型 tick 库时的中立比较框架 |

```
::: 

::: {.callout-note collapse="true"}
來源第 315 行；段落 40fdb34a4b4b969b；UNKNOWN_INHERITED。

```text
> ⚠ **前提校验**：CPCV 有效的前提是样本近似同分布且可重采样。百家乐 ROI 的 CV 可达 ~8、严重非 i.i.d.（已锁定），**须先用实测 Var(ROI|n) 校准，不可用 1/√n**。

```
::: 

::: {.callout-note collapse="true"}
來源第 317 行；段落 ed29593a6f3b25c6；UNKNOWN_INHERITED。

```text
#### 4.2.2 银行业 ★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 319 行；段落 d34d95a8d65e028e；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **监管标准** | **BCBS 239**（风险数据聚合与报告 11 原则）、**SR 26-2**（取代 SR 11-7）、IFRS 9 ECL 分阶段、FATF 40 建议、ISO 20022 | 已在标准框架内，但**尚未逐条对照落表** |
| **模型治理** | 三道防线、**模型清册**、独立验证、**挑战者模型（challenger）**、模型退役流程 | `registry_risk_typology` 是 model inventory 雏形，**缺 challenger** |
| **评分卡工程** | **WOE / IV 分箱**、**PSI**、**拒绝推断**、评分卡刻度（PDO / base odds）、KS / Gini / Lift | **拒绝推断是 a168 标签缺口的银行业标准解**：被封禁会员无后续行为→选择偏差；银行业用 fuzzy augmentation、parceling、Heckman 两步法处理了四十年 |
| **反洗钱** | **Quantexa**、NICE Actimize、Oracle FCCM、SAS AML、Palantir Foundry | 与博彩业 AML 栈同源 |
| **压力测试** | CCAR / DFAST 情景设计、**逆向压力测试** | **逆向压力测试**问「什么情况会让风控完全失效」—— 比正向情景更适合找红队攻击面 |

```
::: 

::: {.callout-note collapse="true"}
來源第 327 行；段落 6878f59ae20798c7；UNKNOWN_INHERITED。

```text
#### 4.2.3 电商业 ★★★★☆

```
::: 

::: {.callout-note collapse="true"}
來源第 329 行；段落 f040f048fbb47f81；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **实时特征平台** | **Feast**、Tecton、Feathr、Michelangelo；核心概念：**在线/离线特征一致性**、**point-in-time correctness** | 直接解决「训练用了未来信息」这一头号杀手；point-in-time join 是 as-of history 的工业实现 |
| **向量检索** | **Faiss**、ScaNN、**HNSW**、Milvus、Qdrant | 会员行为向量近邻检索 —— 找「行为极相似的一组账户」比图谱更快 |
| **序列建模** | DIN / DIEN、**SASRec / BERT4Rec**、Transformer4Rec | 注单序列建模（替代固定窗口聚合），捕捉「稳定→加速→失控」状态转换 |
| **实验方法** | **CUPED**、**Switchback 实验**、**Interleaving**、**序贯检验 / mSPRT**、FDR 多重校正 | **CUPED 对 a168 价值极高**：干预样本稀缺，方差缩减等价于省一半样本；switchback 适合桌台级 / 时段级干预 |
| **反滥用** | 优惠券薅羊毛识别、黑产团伙图谱、设备指纹、行为序列异常 | 与红利滥用（Bonus Guardian）同构 |

```
::: 

::: {.callout-note collapse="true"}
來源第 337 行；段落 da647ce79deeb696；UNKNOWN_INHERITED。

```text
#### 4.2.4 科技业 / SRE / 数据工程 ★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 339 行；段落 94025d788e28b6d9；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **可观测性** | **OpenTelemetry**、**eBPF**（Cilium、Pixie、Parca）、Prometheus + Grafana | eBPF 可在不改代码前提下观测注单链路每一跳真实耗时 |
| **数据血缘** | **OpenLineage + Marquez**、**DataHub**、Apache Atlas、**dbt** + exposures | **「血统关系」的工业标准实现**。140 件 SQL 交付件的依赖应机器可读地表达，而非人工维护 |
| **数据契约** | **Data Contracts**（schema + SLA + 语义 + owner，版本化）、Protobuf / Avro schema registry | registry 与 `配置/paths_a168.R` 已具雏形，**缺机器可校验的契约** |
| **湖仓** | **Iceberg / Delta Lake / Hudi**（ACID、时间旅行、schema evolution）、Arrow、Parquet | **时间旅行直接实现 as-of 可重放** |
| **发布工程** | **特征开关**、金丝雀、**影子流量**、渐进式发布、**混沌工程**（Chaos Mesh / Gremlin） | 影子运行已在 61–90 日计划；混沌工程验证风控部分失效时的降级 |
| **编排与算力** | Ray、Dask、Kubernetes + KEDA、Slurm | Ray 适合本地多核并行回测（`Ncpus=10`） |

```
::: 

::: {.callout-note collapse="true"}
來源第 348 行；段落 164c1d4ce285a64f；UNKNOWN_INHERITED。

```text
#### 4.2.5 资安业 / 网管业 ★★★★★（被严重低估的同构行业）

```
::: 

::: {.callout-note collapse="true"}
來源第 350 行；段落 4d377f49137911b1；UNKNOWN_INHERITED。

```text
> **核心洞见：UEBA（用户实体行为分析）与博彩会员风控在数学上是同一个问题。**

```
::: 

::: {.callout-note collapse="true"}
來源第 352 行；段落 6251b45a06d309cd；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **规则标准** | **Sigma 规则**（YAML 通用检测规则语言，社区共享、可版本化、可转译任意后端） | **直接作为 a168 规则引擎的表达标准** —— 优于自定义 YAML，因有现成工具链与社区验证 |
| **威胁框架** | **MITRE ATT&CK**（战术 → 技术 → 程序 三层） | **`registry_risk_typology` 应按此三层重构**：风险目的（战术）→ 手法（技术）→ 具体实现（程序）。会让 66 条准则从平铺变成可导航矩阵 |
| **检测工程** | SIEM / SOAR（Splunk ES、Elastic Security、Sentinel、Chronicle）、**Detection-as-Code**、**DML 检测成熟度等级**、告警疲劳治理 | 规则进 Git、有测试、有 CI —— 正是可审计所需 |
| **实体行为分析** | **UEBA**：基线建模、**同伴群组分析（peer group analysis）**、低频高危检测 | **同伴群组分析是荷官审计的正解**：不与全体比，只与同班次、同桌型、同限红的同伴比 |
| **客户端指纹** | **JA3 / JA4 / JA4+**（TLS 指纹）、HTTP/2 指纹、Canvas / WebGL 指纹、**FingerprintJS** | **可识别 FPLAY、Mysports.AI 这类自动下注客户端** —— 其 TLS 栈与真实浏览器不同 |
| **机器人管理** | Cloudflare Bot Management、HUMAN Security、Akamai Bot Manager、**cside**（250+ 信号） | 前置拦截，在注单进入 ODS 前打标 |
| **网络检测** | Zeek、Suricata、NDR | 代理层异常流量 |
| **诱捕** | **Canary token**、蜜罐桌台、蜜罐会员 | 埋设只有作弊工具才触发的信号，**产出零假阳性黄金标签 —— 标签缺口最便宜的解** |
| **零信任** | BeyondCorp、最小权限、持续验证 | RG 数据不可达营销系统的技术保障 |

```
::: 

::: {.callout-note collapse="true"}
來源第 364 行；段落 dbc6fcbb86d1c659；UNKNOWN_INHERITED。

```text
> ⚠ **语义错配警告**：网络安全的「攻击者」是外部敌人，博彩的「异常会员」多数是正常客户。**安全行业的高敏感度默认值直接搬来会产生灾难级误伤，阈值必须重标定。**

```
::: 

::: {.callout-note collapse="true"}
來源第 366 行；段落 dee443d6bf1bbcc7；UNKNOWN_INHERITED。

```text
#### 4.2.6 反恐 / 反诈骗风控业 ★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 368 行；段落 7f8385209cb5b57e；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **实体解析** | **Splink**（英国司法部开源，Fellegi-Sunter 概率记录链接，千万级）、Senzing、Zingg、Dedupe | 会员去重与同一自然人多账户识别，输出匹配概率而非布尔 |
| **图算法** | **k-core**、**betweenness**、**motif / graphlet 计数**、**Leiden / Infomap**（优于 Louvain 的分辨率极限）、标签传播 | 已警告不可用连通分量；**k-core 是识别紧密团伙的最强单一指标** |
| **时序图神经网络** | **TGN**、DySAT、**PyTorch Geometric Temporal** | 同桌关系随时间演化，静态图会丢失「何时结伙」 |
| **GNN 反洗钱** | Elliptic 数据集与基准、GraphSAGE / RGCN 在交易图上的标准做法 | 有公开基准可对照，避免自说自话 |
| **隐私计算** | **联邦学习**、MPC、同态加密、差分隐私 | **跨运营商共享串通团伙特征而不交换 PII** —— 博彩业未普及、金融业已成熟，**是真正的超车点** |
| **弱标签** | SAR 反馈闭环、案件结论回流 | a168 缺的正是这个闭环 |

```
::: 

::: {.callout-note collapse="true"}
來源第 377 行；段落 a382936cc147b1ef；UNKNOWN_INHERITED。

```text
> ⚠ **Splink 误合并不可逆**：把两个真实不同的人判为同一人 → 封错账户 → 消费者权益事件。**必须设三档阈值：自动合并 / 人工审核 / 自动拒绝。**

```
::: 

::: {.callout-note collapse="true"}
來源第 379 行；段落 74abf6ff897b1ccd；UNKNOWN_INHERITED。

```text
#### 4.2.7 人工智能业 ★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 381 行；段落 e06e450525c66bef；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明（直击 a168 标签缺口） |
|---|---|---|
| **PU Learning** | Elkan-Noto、nnPU、Spy technique | **a168 标签困境的精确数学表述**：只有人工确认的作弊者是正样本（P），其余海量会员是「未标注」（U）**而非负样本**。用普通二分类会系统性低估召回 |
| **弱监督** | **Snorkel**（多条噪声规则生成概率标签，再用生成模型去噪） | **把现有规则（含 registry 66 条准则）直接变成训练标签源，无需等人工标注积累** |
| **主动学习** | 不确定性采样、期望模型变化、多样性采样、**批量主动学习** | 有限人工产能下，让模型自己决定「下一个最该看哪 50 个案件」 |
| **漂移检测** | **ADWIN**、DDM、EDDM、Page-Hinkley、**KSWIN**；`river`、`alibi-detect`、`frouros` | 比周期性 PSI 更灵敏，且在线 |
| **可解释性** | SHAP、LIME、**Anchors**、**反事实解释（DiCE）**、TREPAN、TCAV | **反事实解释直接回答申诉**：「你需要改变什么，评分才会降到阈值下」 |
| **模型治理** | **Model Cards**、**Datasheets for Datasets**、NIST AI RMF、ISO/IEC 42001、**AIBOM** | 已在标准框架，缺模板落地 |
| **推理服务** | ONNX、TensorRT、**Triton**、vLLM、蒸馏与量化 | 若要在下注窗口内完成评分，量化 + Triton 是标准路径 |
| **合成数据** | **SDV**、CTGAN、TVAE、差分隐私合成、**Gretel**；R `synthpop` | **禁令下做架构压测的唯一合法数据源**，且不涉真实会员 PII |

```
::: 

::: {.callout-note collapse="true"}
來源第 392 行；段落 65c1656e47f86bdc；UNKNOWN_INHERITED。

```text
> ⚠ **PU Learning 的先验 π 是敏感参数**：π 估错，召回估计整体偏移；而 π 恰恰无法从数据本身识别，**需外部锚**。
> ⚠ **合成数据分布外陷阱**：能过统计检验，却不含真实作弊团伙的稀有结构。**用它压测可以，用它验证检测算法会得出虚假高召回。**

```
::: 

::: {.callout-note collapse="true"}
來源第 395 行；段落 97694180b992f93d；UNKNOWN_INHERITED。

```text
#### 4.2.8 宇航生态产业链 ★★★★☆

```
::: 

::: {.callout-note collapse="true"}
來源第 397 行；段落 933545d7e85de414；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **FDIR** | Fault Detection, Isolation and Recovery | **风控系统的自愈规范**：模型漂移超阈值时自动降级为纯规则模式，而非继续输出不可信分数 |
| **冗余表决** | **TMR 三模冗余**、N 版本编程、拜占庭容错 | **对应「三读法全出列，不择一」**：三套独立实现的指标计算互相表决，不一致即告警。**把认识论铁律变成系统架构** |
| **形式化验证** | **TLA+**、SPARK/Ada、Frama-C、Alloy、**Z3** | **可形式化验证结算恒等式** `bet17 = bet14 − bet13 + bet16`（H16）在所有状态转换下成立，而非靠抽样检查 |
| **状态估计** | **卡尔曼 / 扩展卡尔曼 / 粒子滤波**、**IMM（交互多模型）** | 会员风险不是静态分数，而是**带不确定度的在线状态估计**；IMM 可同时维持「正常/加速/失控」多模型并自动切换 —— **比固定移动窗口强得多** |
| **遥测规范** | CCSDS 包遥测、时间戳与序列号强制、下行带宽预算 | 事件 schema 强约束与丢包检测 |
| **软件保证** | DO-178C DAL 等级、ECSS-E-ST-40 | 分级验证框架 |
| **数字孪生** | 系统级仿真、硬件在环（HIL） | 用合成数据构建平台数字孪生，做红队演练 |

```
::: 

::: {.callout-note collapse="true"}
來源第 407 行；段落 d58735fa70f748c6；UNKNOWN_INHERITED。

```text
#### 4.2.9 军工 / 国防生态产业链 ★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 409 行；段落 534a4ca1248bc6a2；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **JDL 数据融合模型** | L0 子对象 → L1 对象 → L2 态势 → L3 影响/威胁 → L4 过程优化 → L5 人机认知 | **与 a168 的 L1–L9 红队分层直接对应且更成熟**，可用来校准层级定义 |
| **OODA 循环** | Observe–Orient–Decide–Act | 风控本质就是比作弊团伙的 OODA 更快 |
| **多假设跟踪 MHT / JPDA** | 同时维持多个数据关联假设，延迟决策至证据充分 | **同一自然人多账户识别的正解**：不一次性聚类，而是维持多个「这些账户属于同一人」的假设，随证据累积更新后验 —— **完全对应证据分级铁律** |
| **TEWA** | 威胁评估与武器分配 | **有限人工产能对多案件的分配，数学上就是 TEWA**：军方已有匈牙利算法、拍卖算法、MDP 建模，**远优于「按分数排序取前 K」** |
| **杀伤链 F2T2EA** | Find–Fix–Track–Target–Engage–**Assess** | **Assess（效果评估）是绝大多数风控系统缺失的一环** —— 「标签回流」正是 Assess |
| **兵棋推演 / 红蓝对抗** | 结构化对抗演练、Assumption-Based Planning | redteam 框架的方法论母体 |
| **强制访问控制** | **Bell-LaPadula**（不上读、不下写）、Biba 完整性模型、MLS | **三管线隔离的形式化表达**：RG 数据标密后，营销系统在格结构上无读取权限 —— **从「制度禁止」升级为「数学上不可能」** |
| **数据二极管** | 单向物理传输 | RG → 营销的物理不可达 |
| **供应链安全** | **SBOM**（SPDX / CycloneDX）、**SLSA** 等级、制品签名（Sigstore） | `renv.lock` 是 R 版 SBOM 雏形，可升级为标准 SBOM |

```
::: 

::: {.callout-note collapse="true"}
來源第 421 行；段落 258381001abb5096；UNKNOWN_INHERITED。

```text
#### 4.2.10 民生与管制生态产业链（制药 / 电力 / 航空 / 核能）★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 423 行；段落 8002738204674fa7；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **ALCOA+ 数据完整性九原则** | **A**ttributable（可归属）、**L**egible（清晰）、**C**ontemporaneous（同步）、**O**riginal（原始）、**A**ccurate（准确）+ Complete、Consistent、Enduring、Available | **全世界最严格的数据完整性宪章，制药业被 FDA 强制执行数十年。直接可作 a168 数据治理最高纲领**，严于任何 IT 行业的「数据质量六维」 |
| **21 CFR Part 11** | 电子记录与电子签名：不可篡改审计追踪、双人复核、权限分离、记录保留 | **L4 人工高影响决策的现成规范**，含申诉与回滚的法定要求 |
| **CSV 验证** | **IQ / OQ / PQ** 三阶段 | **直接作为模型上线门槛框架**：IQ = 环境与依赖确认，OQ = 受控数据上功能正确，PQ = 真实负载下达到预期性能 |
| **变更控制** | 变更申请—影响评估—批准—实施—验证—关闭 | 对应「版本号是身份标识不是序号」 |
| **FMEA / FMECA / FTA / HAZOP** | RPN = 严重度 × 发生度 × 探测度 | **系统化枚举风控失效模式**，比临时头脑风暴的红队完备得多 |
| **功能安全** | IEC 61508 SIL 1–4、ISO 26262 ASIL | 按后果严重度分级配置冗余与验证强度 |
| **电网** | NERC CIP、WAMS 广域测量（PMU + GPS 同步相量） | **PMU 的微秒级同步测量理念可移植到跨桌台事件对齐** |
| **航空** | ADS-B、ACAS/TCAS 防撞逻辑、**SMS 安全管理体系**、**Just Culture（公正文化）** | **Just Culture 对荷官审计至关重要**：必须在制度上区分「操作失误」与「故意舞弊」，否则审计会摧毁荷官队伍 |

```
::: 

::: {.callout-note collapse="true"}
來源第 434 行；段落 cc7d8cfd7cbe69b9；UNKNOWN_INHERITED。

```text
> ⚠ **严格性有代价**：制药业一次变更的验证周期以月计。**必须按后果严重度分级引用** —— L4 高影响决策用 Part 11 强度，探索性分析不用，否则迭代速度归零。

```
::: 

::: {.callout-note collapse="true"}
來源第 436 行；段落 5bbb5ad44bb218fd；UNKNOWN_INHERITED。

```text
#### 4.2.11 科学研究院 ★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 438 行；段落 0a2d578e206ed804；UNKNOWN_INHERITED。

```text
| 类别 | 具体技术 | 移植说明 |
|---|---|---|
| **预注册** | Pre-registration、Registered Report、分析计划锁定 | **防止「事后找显著」** —— 迟投注假设被四重检验证伪，正说明预注册价值；应在跑数前锁定假设与判据 |
| **可重复性** | **Quarto**（已在用）、Jupyter Book、Binder、**Docker / Apptainer**、`renv`（已在用）、随机种子固化 | 已达标，缺容器化 |
| **工作流编排** | **Snakemake / Nextflow / CWL**（DAG、断点续跑、provenance 自动记录）；**R 原生 `targets`** | **可编排 140 件 SQL 交付件**，自动产出血统图；**不依赖 DolphinScheduler，在禁令外** |
| **FAIR 原则** | Findable、Accessible、Interoperable、Reusable；DOI / Zenodo | 交付件元数据规范 |
| **统计严谨** | **Benjamini-Hochberg FDR**、效应量与置信区间优先于 p 值、**ASA p 值声明**、贝叶斯因子、**负对照结局**、**E-value**、敏感性分析、元分析 | **负对照是验证风控信号真实性的最强手段**：用理论上应无关的属性（如注册月份尾数）跑同一管线，若也显著，说明管线有系统性偏差。**E-value 让「可能有混杂」从定性变定量** |
| **HPC** | Slurm、MPI、OpenMP、**OpenBLAS / Intel MKL** | **当前 R 用参考 BLAS，矩阵运算慢一个数量级 —— 换 OpenBLAS 是投入产出比最高的单项优化** |

```
::: 

::: {.callout-note collapse="true"}
來源第 447 行；段落 b758ac71eb0e6e66；UNKNOWN_INHERITED。

```text
#### 4.2.12 确定性系统思想（宇航 / 军工 / 民生三链共通）★★★★★

```
::: 

::: {.callout-note collapse="true"}
來源第 449 行；段落 7880e939cc461b1d；UNKNOWN_INHERITED。

```text
> 三者共享一条被 IT 业普遍忽视的原则：**在安全关键系统中，可预测性优先于平均性能。**

```
::: 

::: {.callout-note collapse="true"}
來源第 451 行；段落 0695f88e148c2813；UNKNOWN_INHERITED。

```text
| 思想 | 对博彩风控的含义 |
|---|---|
| 时间触发架构（TTA）优于事件触发 | 风控评分按固定节拍运行，而非被事件洪峰拖垮 |
| 静态内存分配、无动态分配 | 避免 GC 停顿导致尾延迟尖刺（Redpanda 相对 Kafka 的核心优势） |
| 最坏情况执行时间（WCET）分析 | 承诺的不是平均 50 ms，而是**保证 p99.99 < 200 ms** |
| **优雅降级优于失败** | 模型不可用→退规则，规则不可用→退人工队列，而非停机 |

```
::: 

::: {.callout-note collapse="true"}
來源第 458 行；段落 ebb672d984307463；UNKNOWN_INHERITED。

```text
#### 4.2.13 供应链与合规（宇航链 / 国防链）★★★★☆

```
::: 

::: {.callout-note collapse="true"}
來源第 460 行；段落 50b5663270bb07df；UNKNOWN_INHERITED。

```text
SBOM（SPDX / CycloneDX）· SLSA 构建完整性等级 · 制品签名（Sigstore / cosign）· 可重现构建 · 依赖漏洞扫描（Trivy、Grype）· ITAR/EAR 式数据出境管控。

```
::: 

::: {.callout-note collapse="true"}
來源第 462 行；段落 31a46cccda2b1c05；UNKNOWN_INHERITED。

```text
**直接意义**：`renv.lock`（R）+ `python-ds-requirements.lock.txt`（Python）已是雏形；升级为标准 SBOM 后，**任何分析结论都能追溯到当时的完整依赖树哈希 —— 这才是「血统关系」的完全形态**。

```
::: 

::: {.callout-note collapse="true"}
來源第 466 行；段落 2a206d1bbb7ba461；UNKNOWN_INHERITED。

```text
## §5 设备与装置层（硬件清单，按投入产出比排序）

```
::: 

::: {.callout-note collapse="true"}
來源第 468 行；段落 e8b42808fb905892；UNKNOWN_INHERITED。

```text
| 优先级 | 设备 | 用途 | 投入产出评语 |
|---|---|---|---|
| ★★★★★ | **PTP/PPS 授时 grandmaster + GNSS 天线** | 全平台时钟统一到 μs 级 | **极高** —— 所有时序判据（迟下注、同桌同步）的地基，缺它一切时序分析不可信 |
| ★★★★★ | **大内存单机（512 GB – 2 TB DDR5）** | 千万级会员的全量特征驻留内存 | **极高** —— 绝大多数所谓「大数据」问题在 1 TB 内存单机上是内存问题 |
| ★★★★☆ | **NVMe SSD 阵列（U.2 / E1.S，PCIe 5.0）+ ZNS** | Parquet / Iceberg 本地湖 | 高 |
| ★★★★☆ | **SmartNIC / DPU（NVIDIA BlueField-3）** | 卸载网络栈、线速加密、内核旁路 | 中高 —— 扇出 4.2e5 events/s 时显著 |
| ★★★★☆ | **HSM / TPM** | 审计日志签名、密钥保管、不可篡改 | 高 —— 21 CFR Part 11 式不可篡改审计的硬件根 |
| ★★★★☆ | **数据二极管 / 单向网关** | RG 数据物理不可达营销 | 高 —— **把合规红线变成物理定律** |
| ★★★☆☆ | **GPU（NVIDIA L40S / H100；开发用 RTX 级）** | GNN 训练、牌面识别推理、向量检索 | 中 —— 仅在上 GNN 或视觉时必要 |
| ★★★☆☆ | **CXL 内存扩展** | 内存池化，突破单机内存墙 | 中 —— 前沿但生态尚新 |
| ★★★☆☆ | **WORM 存储** | 审计证据保全 | 中高 —— 监管取证要求 |
| ★★☆☆☆ | **FPGA** | 线到线纳秒 | **低 —— 百家乐场景不需要，勿被「纳秒」话术带偏** |

```
::: 

::: {.callout-note collapse="true"}
來源第 483 行；段落 5d2782d7a500e041；UNKNOWN_INHERITED。

```text
## §6 统一软件包总清单（三格 × 可执行性）

```
::: 

::: {.callout-note collapse="true"}
來源第 485 行；段落 960e78b3bf0b8dd7；UNKNOWN_INHERITED。

```text
**图例**：✅ 本机今天可跑｜⚠ 需平台侧｜⛔ 现行禁令或机器约束下不可行

```
::: 

::: {.callout-note collapse="true"}
來源第 487 行；段落 8bd1c10f920dbfc9；UNKNOWN_INHERITED。

```text
### 6.1 止损

```
::: 

::: {.callout-note collapse="true"}
來源第 489 行；段落 9776d412cfc4c58a；UNKNOWN_INHERITED。

```text
| 层 | 包 | 可执行性 |
|---|---|---|
| 标签生成 | `pulearn`、`snorkel`、`modAL`、`small-text`、`baal` | ✅ |
| 实体解析 | `splink`；R `fastLink`、`reclin2` | ✅ |
| 图谱 | `kuzu`（**嵌入式图库，无需服务端**）、`networkx`、`igraph`、`cdlib`、`leidenalg`、`graspologic` | ✅ |
| 时序图 | `torch-geometric`、`torch-geometric-temporal`、`dgl` | ✅（CPU 慢，可小图验证） |
| 异常检测 | `pyod`、`alibi-detect`、`isotree`；R `isotree`、`stray` | ✅ |
| 监督排序 | `xgboost`、`lightgbm`、`catboost`（已装）；R `ranger`、`xgboost` | ✅ |
| 评分卡 | `scorecardpy`、`optbinning`、`toad`；R `scorecard`、`smbinning` | ✅ |
| 状态估计 | `stone-soup`、`filterpy`、`pykalman`；R `depmixS4`（已装） | ✅ |
| 突变点 | `ruptures`；R `changepoint`、`bcp` | ✅ |
| 时序签名 | `scipy.stats`（KS / Anderson-Darling）、`tick`（Hawkes 过程） | ✅ |
| 客户端指纹 | JA4 / JA4+（FoxIO 开源）、FingerprintJS、cside | ⚠ |
| 流式 CEP | Kafka / Redpanda + Flink；Disruptor / Aeron / Chronicle | ⚠ / ⛔（常驻管控代理） |

```
::: 

::: {.callout-note collapse="true"}
來源第 504 行；段落 c9e63188709bcad1；UNKNOWN_INHERITED。

```text
### 6.2 增效

```
::: 

::: {.callout-note collapse="true"}
來源第 506 行；段落 f10ed10a56fac50d；UNKNOWN_INHERITED。

```text
| 层 | 包 | 可执行性 |
|---|---|---|
| 本地底座 | `duckdb`、`polars`、`pyarrow`（已装）；R `duckdb`、`arrow`、`data.table` | ✅ |
| Tick 存储 | `arcticdb`、`questdb`（嵌入模式） | ✅ |
| 并行 | `ray`、`dask`；R `future` / `furrr`（`Ncpus=10`） | ✅ |
| **流水线编排** | **`targets` + `tarchetypes`（R 原生，最契合）**；`snakemake`、`nextflow`、`prefect`、`dagster` | ✅（**不依赖 DolphinScheduler，在禁令外**） |
| 案件分配 | `ortools`、`scipy.optimize.linear_sum_assignment` | ✅ |
| Bandit / RL | `vowpalwabbit`、`contextualbandits`、`river` | ✅（**仅离线沙盒**） |
| 推荐 | `implicit`、`faiss`、`recbole` | ✅ |
| 预测 | `sktime`、`darts`、`statsforecast`；R `fable`、`tsibble` | ✅ |
| 特征平台 | `feast` | ⚠ |
| 推理服务 | `onnxruntime`、`bentoml`、Triton | ⚠ |
| 合成数据 | `sdv`、`ctgan`、`synthcity`；R `synthpop` | ✅（**禁令下压测唯一合法数据源**） |
| 视觉 | `ultralytics`（YOLOv10）、`opencv-python`、`torchvision`、`PaddleOCR`、TensorRT | ⚠（平台侧）／✅（离线验证） |

```
::: 

::: {.callout-note collapse="true"}
來源第 521 行；段落 25540e02394a61a4；UNKNOWN_INHERITED。

```text
### 6.3 合规

```
::: 

::: {.callout-note collapse="true"}
來源第 523 行；段落 29f0e26078f9d7f8；UNKNOWN_INHERITED。

```text
| 层 | 包 | 可执行性 |
|---|---|---|
| 数据质量 | `great_expectations`、`soda-core`、`pandera`；R `pointblank`、`validate` | ✅ |
| 血缘 | `openlineage-python`、`marquez`、`datahub`、`dbt` | ✅（本地模式） |
| 规则工程 | `pySigma`、`sigma-cli`、`mitreattack-python` | ✅ |
| 可解释 | `shap`、`lime`、`alibi`（Anchors）、`dice-ml`（反事实）、`interpret`、`captum`；R `DALEX`、`iml`、`fastshap`、`modelStudio` | ✅ |
| 因果 | `econml`（已装）、`dowhy`、`causalml`；R `grf`、`MatchIt`、`fixest`、`did` | ✅ |
| **敏感性** | **R `EValue`、`sensemakr`** | ✅ |
| 序贯检验 | `confseq`；多重校正 `statsmodels.stats.multitest`、R `p.adjust` | ✅ |
| 漂移 | `river`、`frouros`、`alibi-detect`、`evidently` | ✅ |
| 治理文档 | `model-card-toolkit`、AI Decision Logger（开源不可变审计日志） | ✅ |
| SBOM | `cyclonedx-python`、`syft`、`grype`、`trivy`；R `renv` | ✅ |
| 形式化 | `z3-solver`（验证 H16 等不变量）、TLA+ | ✅ |
| 隐私计算 | `opendp`、`diffprivlib`、`flower`、`tenseal` | ✅（研究级） |
| 追踪 | `mlflow`、`dvc`、Git、**Quarto**（已在用） | ✅ |
| 量化建模 | `arch`、`linearmodels`、`optuna`、`cvxpy`（**均已装**）；R `rugarch`、`PerformanceAnalytics`、`brms` | ✅ |

```
::: 

::: {.callout-note collapse="true"}
來源第 542 行；段落 a592f879b6958a16；UNKNOWN_INHERITED。

```text
## §7 最小可行集（安装清单）

```
::: 

::: {.callout-note collapse="true"}
來源第 544 行；段落 ecee1c8de7d52b95；UNKNOWN_INHERITED。

````text
```text
# ── Python（装入 C:\work\envs\ds，现有 190 包基础上增补）────────
pulearn snorkel modAL small-text baal
splink kuzu cdlib leidenalg graspologic
scorecardpy optbinning toad
stone-soup filterpy ruptures
pySigma sigma-cli mitreattack-python
dice-ml alibi shap
river frouros alibi-detect evidently
great-expectations pandera
sdv synthcity
cyclonedx-bom z3-solver confseq ortools arcticdb
openlineage-python

# ── R（renv 内）────────────────────────────────────────────
targets tarchetypes
pointblank validate
DALEX iml fastshap modelStudio
EValue sensemakr
scorecard smbinning fastLink reclin2
isotree stray changepoint bcp
flexsurv JMbayes2 synthpop yardstick

# ── 已有（无须重装）────────────────────────────────────────
# R : data.table dplyr ggplot2 kableExtra gt DT plotly echarts4r
#     PerformanceAnalytics PortfolioAnalytics rugarch depmixS4
#     igraph survival survminer MatchIt fixest grf duckdb arrow renv quarto
# Py: numpy pandas polars pyarrow duckdb statsmodels scikit-learn
#     matplotlib xgboost lightgbm econml arch linearmodels optuna cvxpy
```

````
::: 

::: {.callout-note collapse="true"}
來源第 575 行；段落 704afe4d2f061a04；UNKNOWN_INHERITED。

```text
### 7.1 三项零成本前置机器修复（须先做）

```
::: 

::: {.callout-note collapse="true"}
來源第 577 行；段落 3f50a4ee35893fbd；UNKNOWN_INHERITED。

```text
| # | 动作 | 理由 |
|---|---|---|
| 1 | **换 OpenBLAS** —— 备份 `C:\Program Files\R\R-4.6.1\bin\x64\Rblas.dll` 后替换（需管理员，**单独立项**） | 当前 `La_library()` 返回空 = 参考 BLAS，矩阵运算慢一个数量级。**投入产出比最高的单项优化** |
| 2 | **装 TinyTeX 或改 `use_tinytex: false`** | 机器上无任何 LaTeX（pdflatex / xelatex / tlmgr 全缺），而 RStudio 偏好写着 `use_tinytex: true` → **任何 Quarto / Rmd 转 PDF 当场失败** |
| 3 | **`renv.lock` + `python-ds-requirements.lock.txt` → CycloneDX SBOM** | 使任一结论可追溯到完整依赖树哈希 —— 血统关系的完全形态 |

```
::: 

::: {.callout-note collapse="true"}
來源第 585 行；段落 0c58149ff9436ec9；UNKNOWN_INHERITED。

```text
## §8 IQ / OQ / PQ 上线门禁（替代或并入现有 G01–G05 五闸）

```
::: 

::: {.callout-note collapse="true"}
來源第 587 行；段落 db9ed7fe1e6b0341；UNKNOWN_INHERITED。

```text
| 阶段 | 门槛 | 最低要求 |
|---|---|---|
| **IQ**<br>安装确认 | 环境 | SBOM 完整；随机种子固化；`targets` DAG 可断点续跑；**六元组指纹齐备** |
| **IQ** | 数据 | DQ Gate 通过：行数核对、唯一键重复率、字段缺失率、**跨表 join 覆盖率**、时间连续性、币种归一（`bet11` 逐行汇率）、PSI 漂移 |
| **OQ**<br>运行确认 | 预测 | 报告 **PR-AUC、Precision@人工产能、Recall@固定误伤预算、校准曲线**；**禁止只报 AUC** |
| **OQ** | 稳定 | **purged walk-forward ≥ 3 个连续窗口**；CPCV + PBO 报告过拟合概率；PSI 超阈则冻结或降级 |
| **OQ** | 因果 | **负对照结局**通过；**E-value** 报告需多强未测量混杂才能推翻结论 |
| **OQ** | 时序 | 预测类交付件一律以 **MASE** 为误差指标，**禁裸 MAE** |
| **PQ**<br>性能确认 | 经济 | 仅计 **确认后的损失避免额 − 审核与技术成本**；⚠ **前置：`house_edge` 未裁定前无经济锚** |
| **PQ** | 公平 | 按币种、地区、游戏类型、代理、设备质量**分层检查误报率差异** |
| **PQ** | 合规 | 高影响处置 **100% 人工复核**；理由码留存 100%；**RG → 营销隔离稽核通过**；申诉与回滚记录完整 |
| **PQ** | 安全 | 最小权限、去标识化、访问日志、密钥管理、数据保留期均落实 |

```
::: 

::: {.callout-note collapse="true"}
來源第 600 行；段落 3028911551b73fb6；UNKNOWN_INHERITED。

```text
### 8.1 永久审计字段规范

```
::: 

::: {.callout-note collapse="true"}
來源第 602 行；段落 cab60deb540691d0；UNKNOWN_INHERITED。

````text
```text
case_id
subject_type / subject_id
risk_domain                  # RG | anti-fraud | AML | dealer-audit
as_of_timestamp
feature_snapshot_hash
rule_version
model_version
risk_score / confidence
top_drivers
recommended_action
human_reviewer / reviewed_at
final_disposition
appeal_status / rollback_flag
```

````
::: 

::: {.callout-note collapse="true"}
來源第 620 行；段落 c8e8092dd8d4f58f；UNKNOWN_INHERITED。

```text
## §9 行动计划（FMEA 式 RPN 排序：严重度 × 发生度 × 探测难度）

```
::: 

::: {.callout-note collapse="true"}
來源第 622 行；段落 278de123a3f1d0ff；UNKNOWN_INHERITED。

```text
| # | 动作 | 归格 | 前置条件 | 本机可行 |
|---|---|---|---|---|
| **1** | **裁定 `house_edge`，解锁经济路径**（`theo` / `adt` / `nmpt` / `esi`）—— 否则一切止损金额无锚 | 止损 | 业务方输入（F-26） | — |
| **2** | **PU Learning + Snorkel + 拒绝推断**三件套攻标签缺口 | 止损+增效 | 无 | ✅ |
| **3** | **蜜罐桌台 + Canary token 设计**（纸上）→ 零假阳性黄金标签 | 止损 | 无 | ✅ |
| **4** | **OpenBLAS + TinyTeX + SBOM** 三项机器修复 | 合规 | 管理员权限 | ✅ |
| **5** | **`targets` 编排 140 件 SQL** + OpenLineage 血缘 | 增效+合规 | 无 | ✅ |
| **6** | **registry 按 MITRE ATT&CK 三层重构**（战术—技术—程序） | 合规 | 无 | ✅ |
| **7** | **规则迁移到 Sigma 格式**进 Git 配 CI（Detection-as-Code），**阈值重标定** | 止损+合规 | 无 | ✅ |
| **8** | **元标签 + CPCV + PBO + Deflated SR** ⚠ 须先用实测 Var(ROI\|n) 校准，不可用 1/√n | 合规 | 无 | ✅ |
| **9** | **负对照结局 + E-value** 对每条已锁定发现做安慰剂检验与混杂敏感度量化 | 合规 | 无 | ✅ |
| **10** | **Splink 实体解析**（三档阈值）+ **k-core / Leiden / TGN** 团伙识别 | 止损 | 无 | ✅ |
| **11** | **IMM 状态估计**（`stone-soup`）：风险从静态分数 → 带不确定度的在线状态 | 止损 | 无 | ✅ |
| **12** | **TEWA 最优分配**（`ortools`）取代按分排序取前 K | 增效 | 案件表 | ✅ |
| **13** | **ALCOA+ 落为数据治理宪章；L4 对照 21 CFR Part 11；IQ/OQ/PQ 作门禁** | 合规 | 无 | ✅ |
| **14** | **FMEA 枚举风控失效模式，算 RPN** | 合规 | 无 | ✅ |
| **15** | **`z3-solver` 验证 H16 恒等式**等不变量在所有状态转换下成立 | 合规 | 无 | ✅ |
| **16** | **合成数据（SDV）**做架构压测，**绝不用于验证检测算法** | 增效 | 无 | ✅ |
| **17** | **CUPED + switchback + confseq** 为将来的干预实验预置 | 合规 | 无 | ✅ |
| **18** | **离线沙盒 contextual bandit**（`vowpalwabbit`），reward 仅保护性，须 OPE 验证 | 增效 | 1–17 完成 | ✅ |
| **P** | **平台侧（待禁令解除后提交公司）**：PTP 授时 grandmaster（最高优先）→ Redpanda / Disruptor 事件总线 → Feast 特征平台 → Iceberg 湖仓 → JA4+ 与 Bot 管理 → 数据二极管 RG/营销物理隔离 → HSM 审计签名 | — | 公司决策 | ⚠ |

```
::: 

::: {.callout-note collapse="true"}
來源第 644 行；段落 a9bc1289a3d61bb5；UNKNOWN_INHERITED。

```text
### 9.1 四层判决架构（与六层商业版对齐）

```
::: 

::: {.callout-note collapse="true"}
來源第 646 行；段落 21d287cd8acb4eca；UNKNOWN_INHERITED。

````text
```
ODS → DWD 清洗去重 → DWS 特征 → ( 规则 L1 + ML 排序 L2 + 案件 L3 + 人工 L4 )
```

````
::: 

::: {.callout-note collapse="true"}
來源第 650 行；段落 110b9785401f8d5f；UNKNOWN_INHERITED。

```text
- **L1 规则层（秒级）**：KYC 未完成、同设备多账户、异常提款、支付拒绝、极端迟下注、同桌高同步
- **L2 ML 层（排序而非裁决）**：XGBoost / Isolation Forest / 图谱社群，把有限人工产能配置到高价值高可信案件
- **L3 Case Management**：命中规则、关联账户、时间线、金额、模型版本、SHAP 前五因子、建议动作
- **L4 人工高影响决策**：提款冻结、账户限制、荷官调查、代理结算暂停 —— **双人复核、可申诉、可回滚**

```
::: 

::: {.callout-note collapse="true"}
來源第 655 行；段落 81b70b96c35347f2；UNKNOWN_INHERITED。

```text
### 9.2 三管线强制隔离

```
::: 

::: {.callout-note collapse="true"}
來源第 657 行；段落 c66de8a479f4b657；UNKNOWN_INHERITED。

```text
| 管线 | 目标函数 | 可自动化动作 | **绝对禁止** |
|---|---|---|---|
| 反诈 / 反串通 | 降低确认欺诈、红利滥用、团伙与技术利用损失 | 案件分流、加强验证、短时交易暂停、人工审核 | 依玩家输赢改变游戏结果 |
| AML / 资金完整性 | 降低可疑资金漏检与误报 | KYC 补件、SOW / SOF 工作流、可疑案件排队 | 无证据永久扣款或拒绝合法提款 |
| 责任博彩 | 降低可观察伤害、提高限额 / 冷静期采纳 | 提醒、限额入口、冷静期、人工关怀与升级 | **使用风险分数促销、返水、VIP 升级、催存** |

```
::: 

::: {.callout-note collapse="true"}
來源第 665 行；段落 7162a572032c1a98；UNKNOWN_INHERITED。

```text
## §10 参考架构全景

```
::: 

::: {.callout-note collapse="true"}
來源第 667 行；段落 586a567396348c61；UNKNOWN_INHERITED。

````text
```
┌─ L0 采集层 ────────────────────────────────────────────────────┐
│ 授时: PTP grandmaster + GNSS   │ 客户端指纹: JA4+ / FingerprintJS │
│ 机器人管理: Cloudflare / HUMAN │ 蜜罐桌台 + Canary token          │
│ 视觉: YOLOv10 + CRNN + TensorRT (牌面识别 <50 ms)                │
└──────────────────────────────┬─────────────────────────────────┘
                               ▼
┌─ L1 传输层（纳秒—微秒的真正落点）──────────────────────────────┐
│ LMAX Disruptor (ns 环形队列) → Aeron / Chronicle (μs IPC)        │
│ → Redpanda / Kafka (ms, 无 GC 抖动) → Flink CEP (有状态, ms)     │
│ 内核旁路 DPDK/ef_vi │ 背压与优雅降级 (FDIR) │ WCET 承诺 p99.99   │
└──────────────────────────────┬─────────────────────────────────┘
                               ▼
┌─ L2 存储层 ────────────────────────────────────────────────────┐
│ 热: ArcticDB / QuestDB / kdb+  │ 温: Iceberg + Parquet           │
│ 冷: S3 + WORM                  │ 本地研究: DuckDB + Arrow（现有）│
│ 时间旅行 = as-of 可重放 │ 六元组指纹 + SBOM 锁定血统            │
└──────────────────────────────┬─────────────────────────────────┘
                               ▼
┌─ L3 特征层 ────────────────────────────────────────────────────┐
│ Feast 特征平台（在线/离线一致，point-in-time correctness）       │
│ 数据契约 + OpenLineage 血缘 │ ALCOA+ 完整性 │ DQ Gate (GE/pandera)│
└──────────────────────────────┬─────────────────────────────────┘
                               ▼
┌─ L4 判决层（三管线隔离，Bell-LaPadula 格约束 + 数据二极管）────┐
│ 反诈/串通         │ AML/资金           │ 责任博彩               │
│ Sigma 规则        │ Splink 实体解析    │ 生存分析 + IMM 状态估计│
│ k-core + Leiden   │ GNN (TGN / RGCN)   │ （物理隔离营销系统）   │
│ PU Learning + Snorkel 弱监督 + 主动学习 ← 补标签缺口            │
│ 元标签（是否出手）│ TEWA 最优分配（取代按分排序取前 K）         │
│ TMR 三模冗余表决 ← 对应「三读法全出列，不择一」                 │
└──────────────────────────────┬─────────────────────────────────┘
                               ▼
┌─ L5 治理层 ────────────────────────────────────────────────────┐
│ 模型清册 + Challenger (SR 26-2) │ Model Card + AIBOM             │
│ IQ/OQ/PQ 上线门禁 │ 21 CFR Part 11 双人复核 + 不可篡改审计(HSM)  │
│ SHAP / Anchors / 反事实解释 → 申诉 │ ADWIN 漂移 → FDIR 自动降级  │
│ CPCV + PBO + Deflated SR 防过拟合 │ 负对照 + E-value 防伪因果    │
│ OODA / F2T2EA 闭环，Assess 环节回流标签                         │
└────────────────────────────────────────────────────────────────┘
```

````
::: 

::: {.callout-note collapse="true"}
來源第 711 行；段落 93c2c3914fdce558；UNKNOWN_INHERITED。

```text
## §11 数字总账（全部量化宣称 + 来源强度）

```
::: 

::: {.callout-note collapse="true"}
來源第 713 行；段落 85dba939ffee0d5f；UNKNOWN_INHERITED。

```text
| 数字 | 主体 | 来源强度 |
|---|---|---|
| 61,810 请求 / 省 €16M+（2022）；100,000+ 请求 / 省 €13M（2023）；€15M+ 级（2025） | SOFTSWISS Anti-Fraud | 供应商自述（M-6 口径不可比） |
| 流失预测准确率 **75.94%**；流失降低 30–50% | Smartico | 第三方博客（IdeaUsher）转述 |
| 20+ ML 推荐模型、700+ 游戏标题 | Optimove Opti-X | 供应商自述 |
| Stardust：MAU ×3、独立存款人 +37%、净收入 +51% | Optimove 案例 | 供应商案例 |
| Sisal：未来价值 +36%、总存款 +23%、NGR +28%、忠诚客户毛收入 +89% | Optimove 案例 | 供应商案例 |
| ARC 26 个保护标记 / 22 市场 / 9 市场实时互动 / 准确度 >90% | Entain | 公司一手披露（M-2） |
| BetBuddy：15 或 17 个司法管辖区、三大洲；15% 高风险玩家一小时内自设限额 | Playtech | 公司自述（M-3） |
| Mindway：≥87% 专家级检出；每月 1,470 万活跃玩家 | Mindway AI | 供应商自述（M-10 口径） |
| Cevro AI：自主解决 80–90% 复杂工单、100+ 语言 | Shufti + Cevro | 供应商自述 |
| cside：每会话 250+ 浏览器信号 | cside | 供应商自述 |
| GeoComply：2 亿+ 设备安装网络 | GeoComply | 供应商自述 |
| Sentient：参与度真人台 10 倍、12 语言、$10M A 轮 | Sentient / BetHog | 媒体报导 + 融资公告 |
| 边注占亚洲赌场 **40–60% 收入**；AI 优势玩法**年损 5–7 亿美元** | Differential Labs / ASGAM | 行业研究报导 |
| 全球博彩 AI 市场 2024 年 33 亿美元 → 2033 年 510 亿美元（CAGR ~36%）；欧洲 7.95 亿 → 103 亿 | 市场研究 | 估算 |

```
::: 

::: {.callout-note collapse="true"}
來源第 730 行；段落 d983fc0706373736；UNKNOWN_INHERITED。

```text
> **统一裁定**：以上数字**全部是自述或第三方转述，只能作采购 shortlist 线索，不是 SLA**。采购合同中须要求供应商提供可独立验证的基准样本、正负类定义、置信区间与漂移情况。

```
::: 

::: {.callout-note collapse="true"}
來源第 734 行；段落 1c7ecb351fb186b3；UNKNOWN_INHERITED。

```text
## §12 redteam / critic / killcritic / blindspot

```
::: 

::: {.callout-note collapse="true"}
來源第 736 行；段落 e950566935f5dfbd；UNKNOWN_INHERITED。

```text
### 12.1 redteam —— 攻击面（合并全对话，去重后 18 条）

```
::: 

::: {.callout-note collapse="true"}
來源第 738 行；段落 cc5bdb5190310e19；UNKNOWN_INHERITED。

```text
**A. 行业既有攻击面（11 条）**
1. **虚假宣称五型**：规则引擎冒充 AI；推荐 / CRM 个性化偷换成「负责任 AI」；供应商「可接入」冒充「已投产」；游戏供应商与运营商混为一谈；宣称「AI 破解百家乐胜率」。
2. **AI 荷官信任瓦解**：音频质量过高反破坏剧场感，须刻意加背景噪声脏化；渲染延迟 >2 s 则口型与牌面不同步，被弹幕放大为「操纵」证据。
3. **优势玩家 AI 对抗**：边注是亚洲 40–60% 收入来源，已成 AI 算牌首要目标；仅用规则阉割而非主动识别，将流失高价值桌台利润。
4. **奖励优化反噬**：RL 学会在连败后发「安慰奖」延长痛苦游戏；文献指出可降低用户对投注行为的有意识控制。
5. **数据投毒**：机器人刷低额注单污染指标监控（如 BM3）训练数据，掩盖真实套利。
6. **Bot 代理绕过**：OpenAI Operator、Claude for Chrome、Playwright、Puppeteer、Selenium 直接驱动前端。
7. **图谱假阳性**：共享网络、网吧、家庭、代理环境造成误连边。
8. **黑箱处置**：以分数直接封禁、冻结提款而无证据链、人工复核、申诉与回滚。
9. **用途冲突**：同一风险分数同时服务保护与营销。
10. **模型验收偷懒**：只报 AUC，不报 PR-AUC / Precision@产能 / 校准曲线。
11. **随机切分泄漏**：不做 purge / embargo，同一玩家跨期资讯泄漏。

```
::: 

::: {.callout-note collapse="true"}
來源第 751 行；段落 a8829390b0fa3f3d；UNKNOWN_INHERITED。

```text
**B. 跨行业移植新增攻击面（7 条）**
12. **清单本身就是攻击面**：60+ 个包 = 60+ 条供应链风险。`snorkel`、`stone-soup`、`kuzu` 这类小众包的维护活跃度与 CVE 响应远不如 `scikit-learn`，**必须先过 `grype` / `trivy` 再进环境**。
13. **PU Learning 的先验 π 是敏感参数**：π 估错则召回估计整体偏移，而 π 无法从数据本身识别，需外部锚。
14. **Splink 误合并不可逆**：必须三档阈值（自动合并 / 人工审 / 自动拒绝）。
15. **Sigma 规则从安全行业搬来会过敏**：安全行业默认高敏感度（误封一个 IP 成本低），博彩误封一个会员是权益问题。**阈值必须重标定，不可继承社区默认值。**
16. **合成数据的分布外陷阱**：能过统计检验却不含真实作弊团伙的稀有结构。**压测可以，验证检测算法会得出虚假高召回。**
17. **`targets` 缓存失效语义**：若特征函数内部依赖未被 `targets` 追踪的全局状态（系统时间、环境变量），会产生「看似复现实则不同」的最危险失败。
18. **「纳秒」是被供应商话术污染的诉求**：会追着把预算烧在无回报处，而真正瓶颈（p99.9 尾延迟、扇出状态一致性、峰值背压）无人管。

```
::: 

::: {.callout-note collapse="true"}
來源第 760 行；段落 873b664449482503；UNKNOWN_INHERITED。

```text
### 12.2 critic —— 证据弱点

```
::: 

::: {.callout-note collapse="true"}
來源第 762 行；段落 f27af90e0c6780ae；UNKNOWN_INHERITED。

```text
- Entain / Flutter 的 AI 材料**集中于责任博彩**，不是真人百家乐的分游戏公开验证；集团层宣称不可外推到每个百家乐产品。
- Entain >90% 准确度未公开基准样本、正负类定义、置信区间、漂移与外部可重现评估，**不可当作可复制 KPI**。
- Mindway ≥87% 是供应商宣告，只能作采购 shortlist 线索，**不是 SLA**。
- EveryMatrix Bonus Guardian 聚焦**红利滥用**，不等同于可识别同桌串通、荷官异常、洗钱或百家乐下注策略风险。
- **亚洲供应商 AI 叙事真空**：SA / AG / DG / WM 在公开渠道无模型卡、数据集或审计报告；其「自动」仅指无荷官机械发牌。
- 「自动化 = 效率」忽视人工监督成本 —— SOFTSWISS COO 明言最终决策应留给专家。
- 寡头存在**创新者困境**（Evolution 的 De Beers 类比）。
- **本清单约七成技术从未在受监管博彩业公开落地**，属跨行业推论（INFERRED），**对外材料中不可写成「业界标准做法」**。
- ALCOA+ / 21 CFR Part 11 / DO-178C 的严格性有代价，**须按后果严重度分级引用**。
- `mlfinlab` 已转商业授权，元标签与 CPCV 需自实现或找替代，**不要写进依赖清单**。
- STAC / TPC 等基准是**厂商选型工具**，数字由厂商在调优环境产出，不等于你的负载表现。
- 「纳秒级事件总线」（Disruptor / Aeron）的收益只在**单机内**成立；一旦跨机，网络 RTT 立刻吃掉三个数量级。

```
::: 

::: {.callout-note collapse="true"}
來源第 775 行；段落 8f197cbbb468719c；UNKNOWN_INHERITED。

```text
### 12.3 killcritic —— 不可逾越的红线（任一被突破则整份清单作废）

```
::: 

::: {.callout-note collapse="true"}
來源第 777 行；段落 de127d24ae1bf78d；UNKNOWN_INHERITED。

```text
1. ❌ 对单一玩家调整真人百家乐赔率、牌靴、发牌、RNG、派彩或游戏结果。
2. ❌ 用责任博彩 / 心理脆弱性 / 追损特征计算返水、发券、催存、召回或提高 VIP 等级。
3. ❌ 让 RL 对高风险客户探索哪种促销最能提高投注 / 回流。
4. ❌ 以黑箱分数直接封禁、冻结提款或永久限制账户，而无证据链、人工复核、申诉与回滚。
5. ❌ 把「模型 AUC 高」当作上线理由。
6. ❌ 把电商 CTR / 转化目标函数用于任何面向会员的推送。
7. ❌ 把资安业「默认封禁、事后申诉」策略用于正常会员。
8. ❌ 用军工「无人值守自动交战」模式做高影响处置。
9. ❌ 以「达到航天级可靠性」为名把未验证的复杂系统推上生产 —— **复杂度本身即失效来源，DO-178C 的精神是最小化而非最大化功能**。

```
::: 

::: {.callout-note collapse="true"}
來源第 787 行；段落 4aa502cece0b29d9；UNKNOWN_INHERITED。

```text
### 12.4 blindspot —— 盲区

```
::: 

::: {.callout-note collapse="true"}
來源第 789 行；段落 609061846bcd2f33；UNKNOWN_INHERITED。

```text
**A. 行业盲区**
- **MGA Charter 的自愿性陷阱**：2026–2027 高风险义务生效前，运营商可选择性披露模型。
- **EU AI Act 高风险定性**已落，但多数百家乐平台未公开模型审计。
- **剥削性目标函数**（DraftKings 案例）现有法规几乎空白。
- 内部真实模型架构与 **RL 在生产环境的 reward 设计**是最不可知的部分。

```
::: 

::: {.callout-note collapse="true"}
來源第 795 行；段落 7f006af182940f8c；UNKNOWN_INHERITED。

```text
**B. 本项目盲区 —— 机器与禁令约束**

```
::: 

::: {.callout-note collapse="true"}
來源第 797 行；段落 8d51a65396240069；UNKNOWN_INHERITED。

```text
| 项 | 现状 | 对移植计划的约束 |
|---|---|---|
| 磁盘 | 单块 237 GB，可用约 43 GB | Iceberg 本地湖、千万级 Parquet 全量落盘**装不下**；必须按日分区 + 分批 + 预聚合 |
| R BLAS | **参考 BLAS**（`La_library()` 返回空） | 矩阵运算慢一个数量级 —— **当前投入产出比最高的单项修复** |
| LaTeX | **完全没有**（pdflatex / xelatex / tlmgr 全缺），而偏好写着 `use_tinytex: true` | 任何 Quarto / Rmd 转 PDF 当场失败 |
| 常驻代理 | 亿赛通 CDG + Kaspersky + Defender | **DPDK、内核旁路、常驻服务、容器运行时基本不可行**；任何需驱动级或提权的技术全部出局 |
| 连接禁令 | 禁止连接 Superset / DolphinScheduler / StarRocks / 任何博彩站点，禁止实测 | **L0–L2 全部无法验证**，只能纸上设计与静态评审 |
| Python 环境 | `C:\work\envs\ds` 已有 190 包，15 项真算冒烟测试全过 | **L3–L5 的绝大多数技术可以立即在本机跑起来** |

```
::: 

::: {.callout-note collapse="true"}
來源第 806 行；段落 cc7214117ed7a821；UNKNOWN_INHERITED。

```text
> **结论：L0–L2（采集/传输/存储）是公司平台侧的事，你现在一行都验证不了；L3–L5（特征/判决/治理）这台机器今天就能做，且那才是 a168 缺口所在。把跨行业移植的精力全部压在 L3–L5，是唯一不自欺的选择。**

```
::: 

::: {.callout-note collapse="true"}
來源第 808 行；段落 6ca3a3ff6d180ec4；UNKNOWN_INHERITED。

```text
**C. 最大盲区 —— 标签**

```
::: 

::: {.callout-note collapse="true"}
來源第 810 行；段落 0761edb413b7967d；UNKNOWN_INHERITED。

```text
上述所有技术都假设**有标签**。a168 的真实瓶颈始终是 **case outcome 与申诉 / 回滚的标签回流**。全表中直击该瓶颈的只有五项：

```
::: 

::: {.callout-note collapse="true"}
來源第 812 行；段落 e84d18a7ee4f76ac；UNKNOWN_INHERITED。

```text
> **PU Learning · Snorkel 弱监督 · 主动学习 · 蜜罐 Canary token · 拒绝推断**

```
::: 

::: {.callout-note collapse="true"}
來源第 814 行；段落 79e8aa2266a04350；UNKNOWN_INHERITED。

```text
**这五项的价值高于其余全部技术之和。**

```
::: 

::: {.callout-note collapse="true"}
來源第 816 行；段落 50adec44855f5c26；UNKNOWN_INHERITED。

```text
**D. 第二盲区 —— 经济锚**

```
::: 

::: {.callout-note collapse="true"}
來源第 818 行；段落 579f3418d6159f93；UNKNOWN_INHERITED。

```text
**`house_edge = NULL` 与 `economic_path_status = NOT_ESTABLISHED` 未解除前**，`theo` / `adt` / `nmpt` / `esi` 不在可执行代码中 —— **任何「止损金额」的估算都缺经济锚，清单再全也算不出 ROI**。这是必须先解的前置（对应 §9 第 1 项）。

```
::: 

::: {.callout-note collapse="true"}
來源第 822 行；段落 686580fa4f63e19f；UNKNOWN_INHERITED。

```text
## §13 一句话收束

```
::: 

::: {.callout-note collapse="true"}
來源第 824 行；段落 b279c7f1cab88a2b；UNKNOWN_INHERITED。

```text
> **别追纳秒，追确定性；别追模型，追标签；别追全栈，追那三层你今天就能动的。**
>
> **止损靠标签，增效靠编排，合规靠血统。**

```
::: 

::: {.callout-note collapse="true"}
來源第 828 行；段落 b3a14b6523bc4cb3；UNKNOWN_INHERITED。

```text
70 家主体、13 个行业、60 余个软件包里，真正能让 a168 在三格上同时跃迁的只有**六件**：

```
::: 

::: {.callout-note collapse="true"}
來源第 830 行；段落 c1b362dccd3c0296；UNKNOWN_INHERITED。

```text
| # | 六件核心 | 归格 |
|---|---|---|
| 1 | **PU Learning + Snorkel**（标签） | 止损 |
| 2 | **`targets` + OpenLineage**（编排与血统） | 增效 + 合规 |
| 3 | **Sigma + MITRE ATT&CK**（规则工程） | 止损 + 合规 |
| 4 | **Splink**（概率实体解析） | 止损 |
| 5 | **E-value + 负对照结局**（因果可信） | 合规 |
| 6 | **ALCOA+ 与 IQ/OQ/PQ**（治理规格） | 合规 |

```
::: 

::: {.callout-note collapse="true"}
來源第 839 行；段落 81b900895fa94a8d；UNKNOWN_INHERITED。

```text
这六件全部可在现有 R + Python + DuckDB 环境、**不连接任何生产系统**的前提下今天开始。其余五十余项是这六件成立之后的**放大器**，提前上只会放大噪声。

```
::: 

::: {.callout-note collapse="true"}
來源第 843 行；段落 5759c39c9b5e098d；UNKNOWN_INHERITED。

```text
## §14 引用源清单（按 §2 主体顺序，仅列原文可回溯者）

```
::: 

::: {.callout-note collapse="true"}
來源第 845 行；段落 24af194f4377095b；UNKNOWN_INHERITED。

```text
| 编号 | 来源 |
|---|---|
| [1] | BettingStartups — Octane Studios launches customizable AI dealers, starting with baccarat |
| [2] | iGaming Business — Why Nigel Eccles is going all in on AI live dealer (BetHog) |
| [3] | IdeaUsher — How Smartico.ai Uses AI for Casino Player Retention |
| [4] | Smartico — Predictive Churn Analytics: AI-Driven Player Retention |
| [5] | Finsmes — BetHog Raises $10M in Series A Funding |
| [6] | ⚠ NewCasinoRank — Evolution Gaming New Casino（**SEO 站，M-1**） |
| [7] | ⚠ illawiki — Evolution Gaming Industry（**内容农场，M-1**） |
| [8] | Gaming Awards — Pragmatic Play Transforms Live Casino Classic |
| [9] | Gaming Awards — Pragmatic Play Goes Live Casino Auto-Roulette |
| [10] | Playtech — Services |
| [11] | FocusGN — SOFTSWISS highlights iGaming areas in which AI outperforms humans |
| [12] | SOFTSWISS — AI Trends in iGaming 2025 |
| [13] | GGB Magazine — Technology: Responsible Gaming's Front Line（Kindred PS-EDS） |
| [14] | iGaming Future — SOFTSWISS Unveils Vision for AI-Powered Business |
| [15] | ⚠ BISD — Quantum Roulette and Fraud Detection Systems（**SEO 站，M-1**） |
| [16] | ASGAM — Study finds AI-backed advantage play on baccarat side bets becoming an increasing problem for casinos in Asia（Differential Labs） |
| [17] | PMC — AI Personalization and Its Influence on Online Gamblers' Behavior |
| [18] | iGaming Times — Malta's Regulator Publishes a Voluntary AI Charter for Gaming Operators |
| [19] | Malta Gaming Authority — MGA launches AI Gaming Charter |
| [20] | GamblingClub.be — Digital compliance in the EU |
| [21] | ⚠ getaibook.com — DraftKings Used AI to Find the Gamblers Most Likely to Lose（**聚合站转述 NYT，M-5**） |
| [22] | CasinoBeats — Experts Warn AI in Casinos Could Exploit Problem Gamblers |
| [23] | ITWeb — AI can help curb fraud in SA's booming iGaming sector |
| [24] | Entain Group — ESG Showcase Event（ARC 26 标记 / 22 市场） |
| [25] | Flutter — Responsible Gaming |
| [26] | EveryMatrix — CasinoEngine / Bonus Guardian 新闻稿 |
| [27] | Mindway AI — 官网 |
| [28] | UK Gambling Commission — LCCP 3.4.3 Remote customer interaction |
| [29] | Malta Gaming Authority — AI Gaming Charter 2026 (PDF) |
| [30] | NIST — AI Risk Management Framework |
| [31] | Wikipedia — Playtech（BetBuddy 2017-10 收购 / Featurespace 2018-01 整合） |
| [32] | Springer / Journal of Gambling Studies — The Need for Benchmarks to Advance AI-Enabled Player Risk Detection in Gambling |

```
::: 

::: {.callout-note collapse="true"}
來源第 880 行；段落 888a6fbaef1eee62；UNKNOWN_INHERITED。

```text
> ⚠ 标记者为**证据污染源**，引用前须替换为一手来源或降级为 INFERRED。

```
::: 

::: {.callout-note collapse="true"}
來源第 884 行；段落 2b4bcc4d922163b8；UNKNOWN_INHERITED。

```text
## §15 变更历史

```
::: 

::: {.callout-note collapse="true"}
來源第 886 行；段落 fc40c0efa37f8004；UNKNOWN_INHERITED。

```text
| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0.0 | 2026-09-26 | 初版。合并 A–I 主体名册（70 家 + 9 类标准）、13 行业移植图、软件包总清单、IQ/OQ/PQ 门禁、RPN 行动计划、矛盾清单 M-1~M-11、自我更正 SC-A~SC-C。 |

```
::: 

::: {.callout-note collapse="true"}
來源第 892 行；段落 70112536b79a74ba；UNKNOWN_INHERITED。

```text
*Powered by Scibrokes® 世博量化® · 本件为参考资料，不构成第四份权威文档。*
```
::: 

<!-- SOURCE_ANNEX_20261007_END -->
