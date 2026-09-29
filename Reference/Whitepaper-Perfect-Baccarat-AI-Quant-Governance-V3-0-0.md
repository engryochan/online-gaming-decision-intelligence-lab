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
