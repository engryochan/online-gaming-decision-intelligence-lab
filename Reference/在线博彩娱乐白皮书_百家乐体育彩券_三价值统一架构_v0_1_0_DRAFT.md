# 在线博彩娱乐白皮书 · 百家乐 / 体育 / 彩券 — 三价值 × 三垂直统一架构

> **版本**：v0.1.0 **DRAFT**（未定稿；定稿前置见 §0.3）
> **编制日期**：2026-09-27
> **适用项目**：a168（真人百家乐风控与商业分析系统）· 世博量化® / Scibrokes Trading®
> **编制依据**：六份上载附件的跨件审计（redteam/critic/killcritic/blindspot/actionplan）+ 两项当期供应商版图检索（体育 / 彩券）
> **骨架来源**：《顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1.0.0》（六件中唯一达到"证据分级 + 矛盾台账 + 自更正"可交付标准者）
> **文件类型**：并入型章节（供 `.qmd` include 或粘贴）
> **文件性质**：参考资料，**不构成第四份权威文件**（三份权威文件地位不变：SQL 总包 + 两份 QMD 商业报告）

---

## §0 交付说明

### 0.1 六元组指纹的自指约定（沿用移植总表 §0.1）

本项目铁律要求每份交付件附六元组身份锚（文件名 + 行数 + 字节数 + MD5 + 换行符 + 编码）。指纹无法写在被指纹的文件内部（写入即改变字节数与 MD5），故：

- 文件内**不写** MD5 与字节数；
- 六元组指纹**随交付回执给出**，以落盘后实测值为准；
- 本件一经落盘，任何编辑（含空白/换行符转换）均使指纹失效，须重签。

已知固定项：换行符 = LF（与源一致）；编码 = UTF-8 无 BOM；行数/字节数/MD5 见回执。
遇 MD5 不合时，先检查字节差是否等于行数（CRLF 二次保存征兆），再判版本冲突。

### 0.2 与三份权威文件的关系

本件为外部对标与架构设计基线，供采购与技术选型使用；不改动、不覆盖、不并入三份权威文件。任何数据颗粒、门槛、台账以权威文件为准。

### 0.3 定稿前置（未解除前本件维持 DRAFT）

| # | 前置 | 阻塞对象 | 现状 |
|---|---|---|---|
| P-1 | **裁定 `house_edge`**，解锁 `theo`/`adt`/`nmpt`/`esi` 经济路径 | 一切"止损金额 / ROI / 年损"KPI | `house_edge = NULL` · `economic_path_status = NOT_ESTABLISHED` |
| P-2 | 裁定 **M-2 / M-3 / M-4**（ARC 标记数 / BetBuddy 辖区数 / Smartico 收购） | 相关主体证据等级 | UNRESOLVED |
| P-3 | 生产禁令解除或另辟受控测试环境 | L0–L2（采集/传输/存储）全部无法验证 | 禁连生产，仅纸上设计 |
| P-4 | 体育 / 彩券 AI 宣称的一手核实（§4B/§4C 挂 INFERRED 者） | 两新垂直证据等级 | 仅公司存在性为 OBSERVED |

---

## §1 证据分级与三条不可逾越铁律

### 1.1 证据分级（强制，每条主张必带等级）

| 等级 | 定义 |
|---|---|
| **OBSERVED** | 一手来源（官网、年报、监管文件、SEC 申报、公开融资公告） |
| **INFERRED** | 第三方转述、行业媒体、供应商博客，或已知事实推论；引用须标注转述链 |
| **UNKNOWN** | 检索后无可查证技术披露；**不得填充推测**，须显式留白 |
| **CONDITIONAL** | 成立取决于未裁定前提；须写明前提 |

证据等级不因重复计算或再找一个二手源而升级。`NULL`（未测/未定义）≠ `0`（实测零）≠ 缺失。

### 1.2 三条铁律（三垂直通用，不因任何技术先进性放宽）

1. **AI 永不进入博弈结果**
   - 百家乐：不得对单一玩家调整赔率、牌靴、发牌、RNG、派彩或结果。
   - 体育：不得对单一客户篡改结算、作废合法赢注、或以惩罚为目的把其个人线口移出已公示边际之外。（**合法灰带见 §5.1B**）
   - 彩券：不得触碰开奖、RNG、奖池或中奖判定。
2. **RL / bandit 的 reward 只能是保护性指标**：风险下降、限额采纳、冷静期完成、投诉减少、人工审核质量。**禁止** GGR / NGR / 入金 / 投注额 / 游戏时长 / 回流投注 / 返水转化 作为 reward。
3. **RG 数据与营销系统必须格结构或物理隔离**（Bell-LaPadula 不上读不下写 / 数据二极管），而非"制度禁止"。

### 1.3 三类价值判准（通用）

| 价值 | 合法且可验证目标 | 核心 KPI（非 GGR） | 绝不可计入的"收益" |
|---|---|---|---|
| **止损** | 减少经**人工确认**的欺诈、串通、套利、红利滥用、支付异常与流程差错损失 | 确认损失避免额、Precision@人工产能、漏报率、案件时长、**误伤率** | 因限制正常会员减少的正常派彩；拒付合法提款 |
| **增效** | 同等人力处理更多更高质量案件；降低处理/排查/对账/报告成本 | 每审核人日闭环案件数、结案时长、自动证据覆盖率、每确认案件成本 | 脆弱会员投注增加、回流投注、追损延长 |
| **合规** | 更早识别风险、降低伤害与审计缺陷，处置可解释可撤销 | 强信号响应时延、人工复核率（须 100%）、申诉成功率、审计证据完备率、限额/冷静期采纳率 | 将 RG 风险分数用于 VIP / 奖励 / 优惠 / 定向营销 |

---

## §2 范围与统一原则

本白皮书覆盖三垂直，共用同一 L0–L5 参考架构（§5），仅 **L4 判决层的域模型**与**攻击面**因垂直而异。

| 垂直 | 结果生成机制 | 边际（house edge）性质 | 头号止损标的 | 主护城河 |
|---|---|---|---|---|
| **真人百家乐** | 荷官发牌（真人）/ 认证 RNG（AI 荷官） | **固定**（免佣/龙宝/边注各异） | 边注 AI 算牌（亚洲年损量级 5–7 亿美元，INFERRED）· 同桌串通 | 受规牌照 > 流动性 > IP > 技术 |
| **体育博彩** | 真实赛事结果 | **动态**（overround/margin 主动管理） | sharp/套利/courtsiding · match-fixing | **官方数据版权** > 定价模型 > 交易团队 |
| **彩券** | 物理开奖 / 认证 RNG | **固定**（定额 / pari-mutuel） | AML（FATF 洗钱载体）· claim fraud · 内幕 | **政府特许 + 开奖公信力** |

> **统一原则**：三垂直的**风控数学同构**（UEBA / 图 / 实体解析 / 异常检测 / 生存分析），差异只在**域标签与结果生成**。故一套 L0–L3 底座 + 三套 L4 域模型即可覆盖，无须三套独立系统。

---

## §3 跨件审计结论台账（携入白皮书，须随本件流转）

以下为六件跨件对账新发现（X-n），与移植总表旧账（M-1~M-11、SC-A~C）并列生效。**白皮书正文一律采用"斧正后"口径。**

| 编号 | 内容 | 白皮书采用口径 |
|---|---|---|
| **X-1** | 六件含两代认知；旧两件（Baccarat-Ai / perfect-baccarat）带已撤回结论 | 仅以移植总表 v1.0.0 为骨架 |
| **X-2** | 旧件把 newcasinorank/illawiki/bisd 当 Evolution "官方列"（M-1 污染未标记） | Evolution AI 宣称一律 **INFERRED** |
| **X-3** | 公司计数 58↔70 互斥、无编号交叉表 | 采 **70 家 + 9 类**（SC-A），并补体育/彩券新增 |
| **X-4** | Mindway 900万↔1,470万、Better Collective↔ARC 冲突 | 两组并列出列，标 UNRESOLVED，须一手核实 |
| **X-5** | Smartico 收购一处当事实一处当悬案 | 采 **M-4 UNRESOLVED** |
| **X-6** | 旧件落地图推荐 StarRocks/DolphinScheduler（违 M-7 禁令） | **全面剔除**；本件不含任何禁令工具 |
| **X-7** | 两大源件含大量空占位（提問八~十全空、Meta 区块重复） | 不按行数计证据密度 |
| **X-8** | 编依"7,184行/七区块"与实测"9,643行/九区块"不符 | 编依量化描述须重签 |
| **X-9** | 六件皆百家乐单垂直，体育/彩券空白 | 本件**新建**两垂直（§4B/§4C、§5.1、§6） |

---

## §4 竞争主体全名册（三垂直 · 一个不漏但强制挂等级）

> **完整性×严谨性调和声明**：以下"一个不漏"地列出，但每主体强制挂证据等级。列入 ≠ 已核实；UNKNOWN/INFERRED 者不得在对外材料写成"业界标准"或"已投产"。

### 4A. 百家乐 / 真人娱乐（承接移植总表 §2，70 家不再重列，仅列骨干）

| 类 | 骨干主体 | 证据要点 | 等级 |
|---|---|---|---|
| B2B 真人内容 | **Evolution**（含 Ezugi/NetEnt Live） | 真人地位一手；AI 宣称经 SEO 站转述 | 地位 OBSERVED / AI **INFERRED（M-1）** |
| B2B 真人内容 | **Playtech Live**（BetBuddy / Featurespace ARIC / IMS） | BetBuddy、ARIC 整合有一手 | OBSERVED |
| B2B 真人内容 | **Pragmatic Play Live**（Bet Behind Pro 7-Bot / Auto-Roulette） | 半自动化一手；AI 运营 INFERRED | 混合 |
| 亚洲系 12 家 | SA/AG/DG/WM/Sexy/Pretty/Venus/Big/eBet/BetGames/KingMaker/AllBet | 无模型卡/数据集/审计报告 | **UNKNOWN**（仅作去荷官速度对标，不纳入 AI 采购） |
| AI 荷官新势力 | **Octane Studios** · **Sentient Studios（原 BetHog）** | 融资/发布一手；RNG 与渲染强制分离 | OBSERVED（独立成章，不与 Evolution 同表 · M-9） |
| 平台/CRM | **SOFTSWISS**（Anti-Fraud/BM3/DOSSIER）· **EveryMatrix Bonus Guardian** · **Smartico**（RL/MAB 唯一明确落地）· **Optimove Opti-X** | 有一手或准一手 | OBSERVED（Smartico 收购状态 M-4 UNRESOLVED） |
| 责任博彩 | **Mindway AI** · **Neccton Mentor** · **Sportradar Bettor Sense** · Playtech BetBuddy · Entain ARC · Kindred PS-EDS | 供应商自述为主 | OBSERVED（数字冲突见 X-4/M-2/M-3） |
| 敌方工具 | FPLAY / Mysports.AI / Oracle / BACC.BOT / BaccaratAI / Differential Labs(研究方) | 反制对象，非采购对象 | INFERRED |

### 4B. 体育博彩（本件新建 · OBSERVED 为"公司存在与业务线"，AI 宣称为 INFERRED）

| 类 | 主体 | 业务要点 | 等级 |
|---|---|---|---|
| **数据 + 交易 + 诚信** | **Sportradar**（NASDAQ:SRAD） | Betradar 赔率、**Managed Trading Services (MTS)**、**Integrity Services / UFDS AI**（AI 反假球，330+ 伙伴、70+ 运动）；NBA/NHL/NFL 数据与诚信伙伴 | 业务 OBSERVED / UFDS "AI" 程度 INFERRED |
| **数据 + 诚信** | **Genius Sports**（Betgenius 源） | **NFL 官方数据版权**；诚信服务；2026-02 收购 Legend | OBSERVED |
| 数据/统计 | **Stats Perform** · **IMG Arena** · **SIS** · **Oddin.gg**（电竞） | 数据/赛事馈送 | OBSERVED |
| 定价/交易/风控引擎 | **Kambi**（托管，40+ 运营商）· **OpenBet**（L&W）· **SBTech**（DraftKings）· **BetConstruct** · **OpticOdds** · **Don Best** · Metric/Amelco | liability management、in-play margin engine、**sharp-bettor 行为 ML 检测**、盘口挂起 | 引擎 OBSERVED / "ML" 细节 INFERRED |
| 运营商 AI 治理 | Flutter(RTI) · Entain(ARC) · Kindred(PS-EDS) · bet365 · DraftKings（**反面案例**：NYT 称用 ML 找最易输者定向发券，M-5 转述） | 责任博彩 AI 有一手；剥削性目标函数 INFERRED | 混合 |

### 4C. 彩券（本件新建 · 版图 2025–2026 变动大，须随时复核）

| 类 | 主体 | 业务要点 | 等级 |
|---|---|---|---|
| 技术 + 系统 | **Brightstar Lottery**（NYSE:BRSL，原 IGT 彩券；2025-07 将 Gaming&Digital 售予 Apollo，转纯彩券；服务 ~90 客户、美国 46 辖区中 26 个主供、~6,000 员工） | 中央系统、终端、即开票、iLottery、OMNIA 平台 | OBSERVED（**终极控股说法冲突**：一处称 BlackRock、一处称 Apollo 仅购 Gaming 段 → 须一手核实） |
| 技术 + 即开票 | **Scientific Games**（2022 拆分后 Brookfield 拥有的纯彩券体，与 Light & Wonder 分立）· **Pollard Banknote** · **Inspired Entertainment** · **Instant Win Gaming** | 系统、即开票印制、eInstant | OBSERVED |
| 系统 | **Intralot**（"Bally's Intralot S.A."）· **Genlot** · **AGTech** · **NeoPollard** | 中央系统、托管服务 | OBSERVED |
| 运营商 | **Allwyn**（并 OPAP，UK National Lottery 现营运方，替代 Camelot；已迁瑞士）· **FDJ United** · Sisal · Lotto NZ · Macau SLOT | 特许运营 | OBSERVED |

### 4D. 跨垂直风控 / KYC / AML / 客服供应商（承接移植总表 §2D，22 家不重列）

Featurespace ARIC（Visa 已收购）· SEON · GeoComply · Sumsub/Onfido/Jumio/Veriff/iDenfy/Shufti · Sift · Group-IB · cside · Flagright · ComplyAdvantage · NICE Actimize · **Quantexa（跨行业 AML 标杆）** · Cevro/Moveo/InteractiveAI（客服 Agent）等。全部 INFERRED（供应商披露），采购前须要求可独立验证基准。

### 4E. 监管、标准与学术（9 类，通用三垂直）

MGA AI Gaming Charter（2026-09-18，**自愿**，警告 AI-washing）· UKGC LCCP 3.4.3 · **EU AI Act**（欺诈检测/行为追踪/个性化/聊天机器人可能高风险，第 12 条记录）· GDPR 第 22 条 · NIST AI RMF · ISO/IEC 42001 · 认证机构 GLI/eCOGRA/BMM/Gaming Labs · 牌照机构 PAGCOR/MGA/UKGC/WCGRB · 学术（WVU 博彩研发中心、PMC 论文、Springer《AI-Enabled Player Risk Detection 需基准》）。
**体育诚信另加**：各联盟 official-data/integrity 框架、IBIA、ESSA。**彩券另加**：WLA（World Lottery Association）Security Control Standard、GLI-11、开奖 draw integrity 规范。

---

## §5 统一参考架构 L0–L5

L0–L5 与移植总表 §10 一致（此处不重画全图），**三垂直共用**；差异集中在 L4。

```
L0 采集：授时(PTP+GNSS) · 客户端指纹(JA4+/FingerprintJS) · 机器人管理 · 蜜罐+Canary token · 视觉(百家乐牌面 / 彩券即开票核验)
L1 传输：Disruptor(ns) → Aeron/Chronicle(μs) → Redpanda/Kafka(ms,无GC) → Flink CEP  ⚠禁令下仅平台侧
L2 存储：热(ArcticDB/QuestDB) · 温(Iceberg+Parquet) · 冷(S3+WORM) · 研究(DuckDB+Arrow) · 时间旅行=as-of重放 · 六元组指纹+SBOM
L3 特征：Feast(在线/离线一致,point-in-time) · 数据契约+OpenLineage · ALCOA+ · DQ Gate(GE/pandera)
L4 判决：三管线隔离(Bell-LaPadula + 数据二极管) —— 域模型按垂直专化(§5.1)
L5 治理：模型清册+Challenger(SR 26-2) · Model Card+AIBOM · IQ/OQ/PQ门禁 · 21 CFR Part 11双人复核+HSM不可篡改 · SHAP/反事实→申诉 · ADWIN漂移→FDIR降级 · CPCV+PBO+Deflated SR · 负对照+E-value · OODA/F2T2EA闭环Assess回流标签
```

> **禁令下的可行性分界（移植总表盲区 B 结论）**：L0–L2 属平台侧，现禁令下**一行都验证不了**；L3–L5 在现有 R+Python+DuckDB 环境**今天就能跑**，且那才是 a168 缺口所在。**跨行业移植精力全部压在 L3–L5。**

### 5.1 L4 判决层 · 三垂直域模型专化

**5.1A 百家乐**（承接移植总表 §9.1/§9.2）
- 反诈/串通：Sigma 规则 → PU Learning+Snorkel 弱监督 → k-core/Leiden/TGN 团伙 → 元标签（是否出手）→ TEWA 分配。
- 边注 AI 算牌对抗：**主动识别**（剩余牌分布异常投注序列）而非仅规则阉割。
- 荷官审计：UEBA **同伴群组分析**（同班次/同桌型/同限红比，而非与全体比）+ 航空 **Just Culture**（区分操作失误 vs 故意舞弊）。

**5.1B 体育博彩**（本件新增）
- **liability management（合法灰带 · 铁律一边界）**：按 sharpness/流动性对客户降注/限额是**行业标准且合法**，但必须——(a) 依据 sharp/套利/liability，**绝不用 RG 脆弱性分数**；(b) 全程可审计、可申诉；(c) 与 RG 管线格隔离。**越此三条即触铁律一。**
- **match-fixing / 诚信**：betting-pattern 异常检测（对齐 Sportradar UFDS 思路）= **图 + 异常 + 突变点**，与百家乐串通同构。
- **courtsiding / 延迟套利** = 体育版"迟下注"= HFT **共置/时钟同步**问题：靠 PTP 授时 + 盘口挂起时延（p99.9 在下注窗内）而非纳秒。
- **sharp/套利/matched-betting**：金融市场微结构（线口移动 ≡ 价格发现）+ 实体解析（同一自然人多账户）。

**5.1C 彩券**（本件新增）
- **draw integrity（头等）**：物理开奖 + 认证 RNG（GLI-11/WLA SCS）；用**确定性系统思想**（形式化验证 `z3-solver`/TLA+ 验开奖不变量、TMR 三模冗余表决、WORM+HSM 不可篡改日志）——航天/核能链移植最对口。
- **AML（头号止损）**：彩券为 FATF 明列洗钱载体（大额现金、中奖匿名、二次销售、structuring）→ Quantexa 式实体解析 + 图谱 + SAR 闭环；与银行业 AML 栈同源。
- **claim fraud / 内幕**：中奖核验 = KYC；内幕 = 同伴群组 + 时序异常（购票时点相对开奖）。
- **iLottery / 快开彩**：行为近赌场 → RG 风控直接套用 5.1A 的责任博彩管线。

---

## §6 跨行业移植 → 三垂直映射（承接移植总表 §4 十三行业，标注垂直适配）

| 移植来源 | 落地一件事 | 百家乐 | 体育 | 彩券 |
|---|---|---|---|---|
| 金融/HFT | 元标签 + CPCV/PBO/Deflated SR 防过拟合 | ★★★★★ | ★★★★★（线口=价格发现） | ★★★☆ |
| 银行业 | **拒绝推断** + WOE/IV 评分卡 + 逆向压力测试 | ★★★★★ | ★★★★☆ | ★★★★☆ |
| 电商 | CUPED 方差缩减 + point-in-time 特征 | ★★★★☆ | ★★★★☆ | ★★★☆ |
| SRE/数据工程 | **OpenLineage 血缘 + `targets` 编排** | ★★★★★ | ★★★★★ | ★★★★★ |
| 资安/网管 | **Sigma + MITRE ATT&CK 三层 registry + UEBA 同伴群组** | ★★★★★ | ★★★★★（诚信监控） | ★★★★☆ |
| 反恐/反诈 | **Splink 实体解析（三档阈值）+ k-core/Leiden/TGN** | ★★★★★ | ★★★★★（多账户 sharp） | ★★★★★（AML 图谱） |
| 人工智能 | **PU Learning + Snorkel + 主动学习**（攻标签缺口） | ★★★★★ | ★★★★★ | ★★★★☆ |
| 宇航 | IMM 在线状态估计 + FDIR 自动降级 | ★★★★☆ | ★★★★☆ | ★★★☆ |
| 军工 | TEWA 最优分配（取代按分排序取前 K）+ MHT 多假设 | ★★★★★ | ★★★★★ | ★★★★☆ |
| 制药/电力/航空/核能 | **ALCOA+ + 21 CFR Part 11 + IQ/OQ/PQ + FMEA RPN**；**确定性/形式化验证** | ★★★★★ | ★★★★☆ | **★★★★★（开奖公信力）** |
| 科研院 | 预注册 + **负对照结局 + E-value** + OpenBLAS | ★★★★★ | ★★★★★ | ★★★★☆ |
| 确定性系统 | 优雅降级优于失败 | ★★★★★ | ★★★★★ | ★★★★★ |
| 供应链安全 | **SBOM（CycloneDX）+ SLSA + Sigstore** | ★★★★☆ | ★★★★☆ | ★★★★☆ |

> **禁令工具剔除声明（X-6）**：本表**不含** StarRocks / DolphinScheduler / Superset / SeaTunnel 及任何需驱动级/提权/常驻服务的技术——违 M-7 及机器约束（亿赛通 CDG + Kaspersky + Defender 常驻）。编排一律用 **`targets`/Snakemake**（禁令外）。

---

## §7 三垂直攻击面与止损标的（redteam，携移植总表 §12.1 十八条）

**通用（承接）**：虚假宣称五型 · AI 荷官信任瓦解 · 奖励优化反噬（连败发安慰奖延长痛苦）· 数据投毒污染指标监控 · Bot 代理绕过 · 图谱假阳性 · 黑箱处置 · 用途冲突 · 只报 AUC · 随机切分泄漏 · 清单即供应链风险（先过 grype/trivy）· PU 先验 π 敏感 · Splink 误合并不可逆 · Sigma 阈值须重标定 · 合成数据分布外 · `targets` 缓存失效语义 · "纳秒"话术污染。

**体育专属**：sharp/套利团伙（实体解析）· **courtsiding 延迟套利** · match-fixing（诚信监控滞后）· official-data 单点依赖（版权方即命脉）· in-play 盘口挂起时延失控 · **liability 限额误用 RG 分数（触铁律一）**。

**彩券专属**：**AML structuring / 中奖洗钱**（头号）· claim fraud · 内幕购票 · 二次销售 · 开奖公信力受质（draw integrity 失守 = 特许崩塌）· 快开彩 RG 伤害。

> **止损标的量级**（均 INFERRED，且 **house_edge 未锁前不构成可结算 ROI** — 见 §0.3 P-1）：百家乐边注 AI 算牌亚洲年损 5–7 亿美元（Differential Labs/ASGAM）；体育 sharp/套利与假球损失、彩券 AML 罚没与信誉损失均须自家一手数据定标。

---

## §8 IQ/OQ/PQ 上线门禁 + 永久审计字段（三垂直通用，承接移植总表 §8）

- **IQ**：SBOM 完整 · 随机种子固化 · `targets` DAG 可断点续跑 · 六元组指纹齐备 · DQ Gate（行数/唯一键/缺失率/join 覆盖/时间连续/币种归一/PSI）。
- **OQ**：报 **PR-AUC / Precision@人工产能 / Recall@固定误伤预算 / 校准曲线**（禁只报 AUC）· purged walk-forward ≥3 连续窗口 + CPCV+PBO · **负对照 + E-value** · 预测类以 **MASE** 为误差（禁裸 MAE）。
- **PQ**：经济（仅计确认损失避免额 − 成本；**P-1 未解无经济锚**）· 公平（按币种/地区/游戏/代理/设备分层查误报差异）· 合规（高影响 100% 人工复核、理由码 100%、**RG→营销隔离稽核通过**、申诉与回滚完整）· 安全（最小权限/去标识/访问日志/密钥/保留期）。
- **永久审计字段**：`case_id / subject_type / subject_id / risk_domain / as_of_timestamp / feature_snapshot_hash / rule_version / model_version / risk_score / confidence / top_drivers / recommended_action / human_reviewer / reviewed_at / final_disposition / appeal_status / rollback_flag`。

---

## §9 行动计划（FMEA-RPN 排序 · 本机今日可动者优先）

**本机今天可跑（L3–L5，不连生产）**
1. **裁定 `house_edge`** 解锁经济路径（业务方输入 · 阻塞一切 ROI）。
2. **PU Learning + Snorkel + 拒绝推断** 攻标签缺口（三垂直通用）。
3. **蜜罐桌台/蜜罐盘口/蜜罐票 + Canary token** → 零假阳性黄金标签。
4. **OpenBLAS + TinyTeX + CycloneDX SBOM** 三项零成本机器修复。
5. **`targets` 编排 + OpenLineage 血缘**（覆盖 SQL 交付件与三垂直特征）。
6. **registry 按 MITRE ATT&CK 三层重构** + **规则迁 Sigma 进 Git 配 CI**（阈值重标定）。
7. **Splink 实体解析（三档阈值）+ k-core/Leiden/TGN**（百家乐串通 / 体育多账户 / 彩券 AML 图谱）。
8. **元标签 + CPCV + PBO + Deflated SR**（⚠ 先用实测 `Var(ROI|n)` 校准，不用 `1/√n`）。
9. **负对照结局 + E-value** 对每条已锁发现做安慰剂检验与混杂量化。
10. **IMM 状态估计（`stone-soup`）** · **TEWA 分配（`ortools`）** 取代按分排序取前 K。
11. **ALCOA+ 宪章 + 21 CFR Part 11（L4）+ IQ/OQ/PQ 门禁 + FMEA-RPN + `z3` 验不变量**。
12. **合成数据（SDV）** 仅做架构压测，**绝不用于验证检测算法**。

**平台侧（待禁令解除后提交公司）**
PTP 授时 grandmaster（最高优先）→ Redpanda/Disruptor 事件总线 → Feast 特征平台 → Iceberg 湖仓 → JA4+/Bot 管理 → **数据二极管 RG/营销物理隔离** → HSM 审计签名。**体育另加** official-data 馈送冗余、in-play 盘口挂起时延 SLA；**彩券另加** 开奖 draw-integrity 形式化验证 + WORM 存证。

**三管线强制隔离（三垂直通用）**：反诈/反串通 · AML/资金完整性 · 责任博彩，各自目标函数与可自动化动作分离；RG 分数**绝不**用于促销/返水/VIP/催存。

---

## §10 未决与须一手核实清单（定稿前必清）

| 项 | 类型 | 须取得 |
|---|---|---|
| `house_edge` | 经济锚 | 业务方一手输入（P-1） |
| M-2 ARC 标记 26↔30 | 数字冲突 | 附时点并列（不择一） |
| M-3 BetBuddy 15↔17 辖区 | 数字冲突 | 一手核实 |
| M-4 / X-5 Smartico 收购 | 事件冲突 | 收购公告一手 |
| X-4 Mindway 900万↔1,470万 / Better Collective↔ARC | 数字+归属冲突 | 一手核实 |
| Brightstar 终极控股 BlackRock↔Apollo | 归属冲突 | SEC/一手 |
| 体育/彩券 AI 宣称（§4B/§4C INFERRED 者） | 证据升级 | 供应商模型卡/基准/审计 |
| 所有"止损金额/年损" | 经济量化 | 自家一手数据定标（依赖 P-1） |

---

## §11 一句话收束

> **三垂直同数学，异结果与异护城河：百家乐拼受规×本地化，体育拼官方数据×定价，彩券拼特许×开奖公信力。**
> **止损靠标签，增效靠编排，合规靠血统；架构一套底座 + 三套 L4 域模型，别追纳秒，别追全栈，追那三层你今天就能动的。**

三垂直、13 行业、六十余包里，能让 a168 同时在三格跃迁的仍是那**六件核心**（PU+Snorkel / `targets`+OpenLineage / Sigma+MITRE / Splink / E-value+负对照 / ALCOA+ 与 IQ/OQ/PQ），今日可在现有环境、不连生产开始；其余为放大器，提前上只放大噪声。

---

## §12 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1.0 DRAFT | 2026-09-27 | 初稿。以移植总表 v1.0.0 为骨架，携 M-1~M-11/SC-A~C/X-1~X-9 更正；新建体育、彩券两垂直（主体名册 §4B/§4C、L4 专化 §5.1B/C、攻击面 §7、移植映射 §6）；剔除全部禁令工具（X-6）。**未定稿**——P-1~P-4 未解除前不得转正。 |

---

*Powered by Scibrokes® 世博量化® · 本件为参考资料，不构成第四份权威文档 · DRAFT，未经一手核实与生产验证，不得对外定稿引用。*
