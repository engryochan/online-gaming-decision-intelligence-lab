# 在线博彩娱乐白皮书 · 完美真人百家乐为主轴 / 体育 / 彩券 — 三价值 × 三垂直统一架构

> **版本**：v0.2.0 **DRAFT**（前版 v0.1.0 DRAFT 之严格超集；定稿前置见 §0.3）
> **编制日期**：2026-09-28
> **适用项目**：a168（真人百家乐风控与商业分析系统）· 世博量化® / Scibrokes Trading®
> **编制依据**：九件输入件逐件指纹与跨件对账（§0.4）+ 本轮一手核实四项（Smartico 收购状态、EU AI Act 数字综合法、Featurespace 并购完成、Playtech 出售 Snaitech）
> **骨架**：v0.1.0（Claude）为主干；并入 `全球…白皮书_2026-09-27`（ChatGPT）之更正 A–H、GDI-OS 架构、验收协议、采购问卷；并入 `Whitepaper V2.0.0`（Meta AI）中经核实无误之增量；源件 `Inteligent_egaming…qmd` 提問八九家 AI 答复全数过筛
> **禁止退化声明**：v0.1.0 全部章节、主体、铁律、台账、前置、清单均完整保留于本件（映射见 §0.6）；本件只增不删，改动一律以更正编号（SC-/X-/M-）公开登记
> **骨架来源**：v0.1.0（其骨架来源为《移植总表 v1.0.0》——六件中唯一达到「证据分级 + 矛盾台账 + 自更正」可交付标准者）
> **文件类型**：并入型章节（供 `.qmd` include 或粘贴）
> **文件性质**：参考资料，**不构成第四份权威文件**（三份权威文件地位不变：SQL 总包 + 两份 QMD 商业报告）
> **白皮书正文一律采用"斧正后"口径。**

---

## §0 交付说明

### 0.1 六元组指纹自指约定（沿用）

文件内**不写**本件 MD5 与字节数；六元组以落盘实测、随交付回执给出为准。任何编辑（含空白、LF↔CRLF）均使指纹失效，须重签。遇 MD5 不合，先查字节差是否等于行数（CRLF 二次保存征兆），再判版本冲突。本件：LF · UTF-8 无 BOM。

### 0.2 与三份权威文件的关系（沿用）

本件为外部对标、架构设计与采购尽调基线；不覆盖、不并入权威文件。数据颗粒、门槛、台账一律以权威文件为准。

### 0.3 定稿前置（v0.1.0 P-1~P-4 保留，新增 P-5~P-7）

| # | 前置 | 阻塞对象 | 现状 |
|---|---|---|---|
| P-1 | **裁定 `house_edge`**，解锁 `theo`/`adt`/`nmpt`/`esi` | 一切止损金额 / ROI / 返水 theo 化（§9） | `house_edge = NULL` · `economic_path_status = NOT_ESTABLISHED` |
| P-2 | 裁定 M-2 / M-3 / X-4 | 相关主体证据等级 | M-2、M-3、X-4 UNRESOLVED；**M-4 本轮部分裁定**（§3.3） |
| P-3 | 生产禁令解除或获授权测试线 | ARCH-L0~L2 全部不可验证 | 禁连生产，仅纸上设计 |
| P-4 | 体育 / 彩券 AI 宣称一手核实 | §4J/§4K INFERRED 者 | 公司存在性与部分年报能力已 OBSERVED |
| **P-5** | **裁定 `registry_risk_typology` ↔ `registry_risk_topology` 标识（X-20）** | 风险注册表身份字段、血统链 | 两名并存于四件源 |
| **P-6** | **确认「完美真人」与 WM Casino / WM Perfect Group 是否同一主体（B-12）** | 名册 #7 应否移出竞争者、改为自评基线 | 源件多处并称，未经用户确认 |
| **P-7** | **独立实例执行 R4 复核**（本件五段仍由单一实例产出，属 self-audit） | 转正 | 未执行 |

### 0.4 输入件指纹与血统（本轮实测）

| # | 文件 | 行数 | 字节 | MD5（实测） | CR 字节 | 出处 / 性质 |
|---|---|---|---|---|---|---|
| 1 | `電腦已昇級至視窗11版_工欲善其事必先利其器_.qmd` | 11,627 | 504,093 | `41cdec343b7f2ce0318f5a90c3828f12` | 0 | 九家 AI 问答原始底稿（**较前轮 9,643 行增长**，X-13） |
| 2 | `Inteligent_egaming_platform_ref_v000_000_001.qmd` | 15,934 | 817,632 | `5b504053c9166bdbf3acccef800b4093` | 0 | 九家 AI 问答底稿（**较前轮 13,149 行 / `bf88567a…` 增长**，X-12） |
| 3 | `顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1_0_0.md` | 892 | 79,482 | `1f28a39616dfa9c1bbf0b9c2e49b3d98` | 0 | 移植总表（证据分级骨架） |
| 4 | `全球在线博彩娱乐_AI量化科技与安全治理白皮书_2026-09-27.md` | 828 | 37,999 | `2898284dd57e0271961570e80bf506f1` | 0 | ChatGPT 产出；**与其自报 MD5/字节/行数逐位吻合（R1 PASS）** |
| 5 | `Whitepaper-Online-Gaming-Baccarat-AI-V2-0-0.md` | 350 | 26,736 | `01bc19dbd069b5bc6aee4a26b9e45017` | 0 | **Meta AI 产出**（据源件 #2 提問八 Meta 段自述 v2.0.0 溯得） |
| 6 | `在线博彩娱乐白皮书_百家乐体育彩券_三价值统一架构_v0_1_0_DRAFT.md` | 286 | 25,187 | `2f2c388559414131f52d8919b5defb24` | 0 | Claude 前版；**与前轮交付回执逐位吻合（R1 PASS）** |
| 7 | `perfect-baccarat-report.md` | 222 | 23,608 | `2df6994f6e2ddc9d1aa4e75d4600e18c` | 0 | 旧代稿（X-1） |
| 8 | `Baccarat-Ai-Automation-Report.md` | 111 | 17,647 | `d61d68b8b4fc3fdc959c8c3573deaf24` | 0 | 旧代稿，含 M-1 污染（X-2） |
| 9 | `Aerospace_Ecosystem_Report.qmd` | 135 | 6,865 | `39d9e98172848c2a47402eee6bbd7217` | 0 | 宇航国防数据栈对比 |

> 九件均为 UTF-8 无 BOM、全 LF、无 NUL、以 LF 结尾（Python 逐字节实测）。
>
> **源件 #2 提問八**（第 13,026~15,112 行）为九家 AI 对同一白皮书任务之答复：Claude（v0.1.0 之对话文本）、ChatGPT（全球件）、Kimi（空）、Perplexity（**自陈仅读到 1/6 附件**，X-19）、Grok、DeepSeek、Gemini、Copilot、Meta AI（V2.0.0）。提問九~卅 仍为空占位。

### 0.5 血统分叉裁定

同日出现三条并行白皮书线：v0.1.0（Claude）/ V2.0.0（Meta）/ 全球 2026-09-27（ChatGPT）。版本号是身份标识而非序号，「V2.0.0」不因号大而居上。本件 v0.2.0 为**合流线**：取三者经核实之最强项，公开登记其各自退化与错误（§3）。
**建议（须用户裁定，本件不越权改名）**：V2.0.0 与全球件落盘时加 `_superseded` 后缀保留，不删除。

### 0.6 不退化映射（v0.1.0 → v0.2.0）

| v0.1.0 | v0.2.0 位置 | 处置 |
|---|---|---|
| §0.1~0.3 | §0.1~0.3 | 保留；P-5~P-7 新增 |
| §1 证据分级 / 三铁律 / 三价值 | §1 | 保留；新增 P0~P3 对照、KPI 准入/禁入清单、合规作约束 |
| §2 范围 | §2 | 保留；新增完美真人主轴 |
| §3 X-1~X-9（X-n 系列） | §3.1 | 保留全部；新增 X-10~X-20、SC-D~SC-H、M 系列现状；v0.1.0 之「M-2 / M-3 / M-4」前置中 **M-4 UNRESOLVED → 本件部分裁定**（§3.3） |
| §4A~4E 名册 | §4A~4M | 保留全部主体；**自足化**（不再「承接移植总表不重列」，SC-H） |
| §5 L0–L5 与 §5.1A/B/C（5.1A 百家乐 · 5.1B 体育博彩 · 5.1C 彩券） | §5（冠名 ARCH-L0~L5）+ §5.4A/B/C | 保留并加厚；新增 GDI-OS 与红队 L 轴对照、注册表双对象 |
| §6 十三行业映射 | §6 | 保留；新增媒体、加密、支付、流媒体、精算、证券监管 |
| §7 攻击面 | §7 | 保留；并入全球件 18 条并去重；新增 9 条 |
| §8 IQ/OQ/PQ + 审计字段 | §8 | 保留；并入挑战者阶梯、统一验收协议、`registry_risk_topology` schema |
| §9 行动计划 | §14 | 保留全部条目；并入全球件 Phase 0~4 |
| §10 须一手核实清单 | §16 | 保留；更新状态 |
| §11 收束 | §17 | 保留 |
| §12 变更历史 | §18 | 追加 v0.2.0 |
| — | §9 返水科学裁定 · §10 竞争缺口→对策矩阵 · §11 蓝图 · §12 速查卡 · §13 本件之红队 · §15 尽调问卷 | **新增** |

---

## §1 证据分级、三条铁律、三价值

### 1.1 证据分级（项目四级为正本，P0~P3 为细分注记，取其严者）

| 项目正本 | 全球件对照 | 定义 | 用法 |
|---|---|---|---|
| **OBSERVED[P0]** | P0 / VERIFIED | 法律文本、监管机构、SEC 申报、上市公司年报 | 事实基线 |
| **OBSERVED[P1]** | P1 | 发行人自身公告、官网产品页、融资公告（厂商自述须注测量口径） | 可引用，注明「自述」 |
| **INFERRED[P2]** | P2 | 行业媒体、第三方转述、供应商博客、AI 转述 | 线索；注转述链 |
| **UNKNOWN[P3]** | P3 | 检索无可查证披露 | **不得填充推测**，显式留白；**UNKNOWN ≠ 未使用**（全球件 §11） |
| **CONDITIONAL** | CONDITIONAL | 取决于未裁定前提（牌照、法域、合同、法律意见） | 写明前提 |

任何数字须携：**主体 · 时点 · 样本 · 分母 · 口径 · 地区 · 来源 · 是否自述**（全球件 §1.1，采纳）。等级不因重复计算或再找一个二手源而升级。`NULL`（未测）≠ `0`（实测零）≠ 缺失。**「宣布签约」≠「完成交割」**（M-4 教训）。

### 1.2 三条铁律（三垂直通用，沿用 v0.1.0，不因技术先进性放宽）

1. **AI 永不进入博弈结果** — 百家乐：不对单一玩家调整赔率、牌靴、发牌、RNG、派彩、结果；体育：不篡改结算、不作废合法赢注、不以惩罚为目的把个人线口移出已公示边际（合法灰带见 §5.1B）；彩券：不触碰开奖、RNG、奖池、中奖判定。
2. **RL / bandit 的 reward 只能是保护性指标**：风险下降、限额采纳、冷静期完成、投诉减少、人工审核质量。**禁止** GGR / NGR / 入金 / 投注额 / 游戏时长 / 回流投注 / 返水转化 / 留存 作为 reward（X-16 登记源件违例）。
3. **RG 数据与营销系统必须格结构或物理隔离**（Bell-LaPadula 不上读不下写 / 数据二极管），而非「制度禁止」。

**RG 为硬约束而非可被收入抵消之权重**（全球件执行摘要第 2 条，采纳）：

```text
maximize  E[ legitimate economic value + confirmed loss prevention ]
subject to  RG_status ∉ prohibited_marketing_states
            KYC_pass = TRUE ;  AML_constraints = PASS ;  jurisdiction ∈ allowed
            game_integrity = intact ;  human_review = required_for_high_impact
```

### 1.3 三类价值判准（沿用）+ KPI 准入 / 禁入清单（新增）

| 价值 | 合法可验证目标 | 核心 KPI（非 GGR） | 绝不可计入 |
|---|---|---|---|
| **止损** | 减少经人工确认之欺诈、串通、套利、红利滥用、支付异常、流程差错损失 | 确认损失避免额、Precision@人工产能、漏报率、案件时长、误伤率 | 因限制正常会员而少付之正常派彩；拒付合法提款 |
| **增效** | 同人力处理更多更高质量案件；降低排查/对账/报告成本 | 每审核人日闭环案件、中位/p95 结案时长、自动证据覆盖率、每确认案件成本、管线运行时长、对账异常处理时长、模型上线前置时间 | 脆弱会员投注增加、回流投注、追损延长 |
| **合规** | 更早识别风险，降低伤害与审计缺陷，可解释可撤销 | 强信号响应时延、人工复核率（高影响 100%）、申诉成功率/推翻率、回滚率、审计证据完备率、限额/冷静期采纳率、**RG→营销泄漏 = 0** | RG 风险分数用于 VIP / 奖励 / 优惠 / 定向营销 |

**净止损账**（全球件 §9.1，采纳）：`Net = Confirmed Avoided Loss − False-Positive Cost − Review Cost − Vendor/Infra Cost`。

> **禁入裁定（X-10c）**：「月活、独立存款人、NGR、忠诚客户毛收入」可作经营观测，**不得记入三价值账、不得作 reward、不得作风控/AI 系统成功判据**。V2.0.0 §8.4 与 `perfect-baccarat-report` §7.4 将其列为「增效 KPI」，与其自身 §1.3 表自相矛盾，本件不采纳。

---

## §2 范围与统一原则

| 垂直 | 结果生成 | 边际性质 | 头号止损标的 | 主护城河 |
|---|---|---|---|---|
| **真人百家乐（主轴）** | 荷官发牌（真人）/ 认证 RNG（AI 荷官） | **固定且可闭式计算**（规则表 × 付彩表 × 副数 × 抽水；边注依牌靴状态而变） | 边注 AI 算牌（亚洲年损量级 5–7 亿美元，INFERRED）· 同桌串通 · 返水对打套利（§9） | 受规牌照 > 流动性 > IP > 技术 |
| **体育** | 真实赛事 | **动态**（overround/margin 主动管理） | sharp / 套利 / courtsiding · match-fixing | **官方数据版权** > 定价 > 交易团队 |
| **彩券** | 物理开奖 / 认证 RNG | 固定（定额 / pari-mutuel） | AML（FATF 洗钱载体）· claim fraud · 内幕 · 零售商舞弊 | **政府特许 + 开奖公信力** |

**统一原则（沿用 v0.1.0 原文）**：三垂直共用同一 L0–L5 参考架构（本件冠名 ARCH-L0~L5，§5），仅 **L4 判决层的域模型**与攻击面因垂直而异；三垂直的风控数学同构（UEBA / 图 / 实体解析 / 异常检测 / 生存分析），差异只在**域标签与结果生成**。故一套 ARCH-L0~L3 底座 + 三套 L4 域模型即可覆盖，无须三套独立系统。**但「同一套模型」是错误**（全球件 §11 采纳）：平台层可共用，定价、完整性、风险与监管对象各异。

**百家乐四层分离**（全球件 §2，采纳）：游戏层（规则、牌靴/RNG、结果、结算、认证）｜体验层（视频、延迟、切桌、多语言、路单、辅助统计）｜经营层（玩家、代理、支付、奖金、风控、RG、CRM、客服）｜决策层（风险、价值、资格、动作、人工案件、效果回流）。**路单为描述性信息，不得包装为预测工具**。

---

## §3 审计台账

### 3.1 跨件新发现 X 系列（X-1~X-9 沿用；X-10~X-20 本轮新增）

| 编号 | S | 内容 | 本件采用口径 |
|---|---|---|---|
| X-1 | S1 | 源件含两代认知；旧两件带已撤回结论 | 以核实为准，不以版本新旧 |
| X-2 | S1 | 旧件把 newcasinorank / illawiki / bisd 当 Evolution 官方（M-1 污染） | Evolution AI 宣称一律 INFERRED |
| X-3 | S2 | 计数 58↔70 互斥 | 70 + 扩展；本件编号自足（§4） |
| X-4 | S2 | Mindway 900万↔1,470万；Better Collective↔Entain ARC 归属 | 并列出列 UNRESOLVED；**全球件对此冲突沉默，V2.0.0 于同一条目兼载两数**（X-10f） |
| X-5 | S2 | Smartico 收购一处事实一处悬案 | **本轮部分裁定**（§3.3） |
| X-6 | S1 | 落地图推荐 StarRocks / DolphinScheduler（违 M-7） | 全面剔除；**本轮再现两次**（X-10a、X-14a） |
| X-7 | S2 | 源件大量空占位 | 保留；**时点已变**（SC-E） |
| X-8 | S2 | 移植总表编依「7,184 行 / 七区块」与实测不符 | 保留；差距扩大至 11,627 行（X-13） |
| X-9 | S3 | 六件皆百家乐单垂直 | v0.1.0 新建体育/彩券；本件并入全球件 SEC/年报级材料加厚 |
| **X-10** | **S1** | **V2.0.0（Meta）退化清单**：(a) L1 重新写入 StarRocks/ClickHouse（X-6 复发）；(b) 0–30 日即「接入 Kafka→Flink」，与其自身 §7「L0–L2 一行验证不了」相矛盾；(c) §8.4 把 月活/独立存款人/NGR/忠诚毛收入 列为增效 KPI（违 §1.3）；(d) **将「60FPS YOLO 读牌 + Flink 100ms 派彩」归于 Evolution**——此为 DeepSeek/Gemini 通用设计，非 Evolution 披露，属新一例 M-1 型归因错误；(e) 编号冲突（#61~#63 重复使用）致「70 家」不可复算；(f) Mindway 同条兼载 1,470 万与 900 万；(g) Featurespace 写「Visa 2024 年**拟**收购」——已于 2024-12-19 完成（§3.3）；(h) Smartico 写「已被收购、独立性下降」——双方公告明言继续独立运营；(i) M-4「CityBiz/Finsmes 交叉验证」误引（Finsmes 为 BetHog 融资源）；(j) 自报「Inteligent 13156 行」与当时实测 13,149 不符；(k) 在 `house_edge=NULL` 下自称「定版」 | 逐项不采纳；V2.0.0 中经核实无误之增量（如「假台盗用」风险、Angel Group 部署、体育返水低赔率规则之提问）经本件重新定级后吸收 |
| **X-11** | S2 | **全球件（ChatGPT）缺口**：(a) 无版本身份号，仅日期；(b) 附件名带「(1)」「(2)」副本后缀，未给指纹，不可判所据版本；(c) 未载 EU AI Act 数字综合法（高风险延期）；(d) 采用 `registry_risk_topology`，与移植总表 `registry_risk_typology` 不一致（X-20）；(e) GDI-OS 之 L0~L10 与项目红队 L1~L9、v0.1.0 之 L0~L5 三套「L」命名冲撞；(f) 对 `house_edge=NULL` 仅泛称「Economic anchor」，**弱于移植总表之 D 盲区**；(g) 机器约束（BLAS/TinyTeX/磁盘/常驻代理）未载；(h) 扩展主体 14 家未逐家定级 | (a)(b) 登记；(c) 本件补；(d) P-5；(e) 本件以 ARCH- 前缀与对照表化解；(f)(g) 以移植总表口径恢复；(h) 本件 §4 逐家定级 |
| **X-12** | S2 | 源件 #2 在两轮间由 13,149 行 / `bf88567a…` 增至 15,934 行 / `5b504053…`；提問八 已填入九家答复 | 以本轮指纹为据；前轮 X-7 之「提問八全空」为当时版本之真，登记 SC-E |
| **X-13** | S3 | 源件 #1 由 9,643 行增至 11,627 行 | 移植总表编依须重签 |
| **X-14** | S1 | **Gemini 答复（源件 #2 提問八）**：(a) 以 DolphinScheduler + StarRocks + Superset 为底座（X-6 复发）；(b)「1,700 万级全局真实观测值」无分母口径，与项目锚 `n_in_snapshot = 125,654,711`、`T_true = 723,442` 均对不上；(c) 指标 #7「House Edge Deviation」预设 house_edge 已知，与 P-1 冲突；(d)「Rebate ROI = ΔIncremental GGR」违 §1.3；(e) Track B 净输返水以「提高 VIP 粘性与 LTV」为目的 | 不采纳 (a)(b)(c)(d)；(e) 由 §9 裁定 |
| **X-15** | S1 | **返水口径互斥**：DeepSeek「不得制造亏损越大返越多」↔ Gemini「R_L = r_L × max(−NetLoss,0)」 | §9 以数学裁定 |
| **X-16** | S1 | 源件 #2 中 RL 示例 reward 列入「留存、NGR 增量」 | 违铁律 2，不采纳 |
| **X-17** | S3 | Angel Group 部署口径：「Sands China 千张」↔「澳门/新加坡/菲律宾/澳洲约 2,000 张（金沙澳门与新加坡、Solaire、SkyCity）」 | 非矛盾，系分母不同；引用须带地域与客户范围 |
| **X-18** | S2 | 源件 #2 中 B2C 站点宣称 SEO 级：Baccarat888「每局庄闲胜率 AI 预测」（**对独立同分布结果的预测宣传属误导，列反面案例**）；188BET/Frosmo「推荐点击率 >70%、转化率 >60%」量级不可信；GoldenTiger VIP、BTCC 等条款 | 一律 UNKNOWN；Baccarat888 类宣传入 KillCritic |
| **X-19** | S2 | Perplexity 自陈仅读到 1/6 附件 | 其答复不得作全件审计证据 |
| **X-20** | S1 | **身份字段漂移**：`registry_risk_typology`（移植总表 ×2、源件 #2 ×2）↔ `registry_risk_topology`（全球件 ×3、源件 #2 ×7） | 本件提出**双对象**解（§5.3），由 P-5 裁定 |

### 3.2 本实例自我更正（SC 系列，公开登记，不静默改写）

| 编号 | 前说 | 更正 |
|---|---|---|
| **SC-D** | 前轮（第二轮）称 Playtech「集团拆分/治理传闻长期扰动」 | **过时**：Playtech 已于 2025-04-30 完成以 €2.3bn 向 Flutter 出售 Snaitech，转为以 B2B 为主（OBSERVED[P1]，§3.3） |
| **SC-E** | v0.1.0 X-7「Inteligent 提問八/九/十 全空」 | 对 `bf88567a…` 版为真；对 `5b504053…` 版，提問八已填，九~卅仍空 |
| **SC-F** | v0.1.0 §4E「欺诈检测/行为追踪/个性化/聊天机器人可能高风险」 | **不精确**：高风险须依 Art. 6 + Annex III 按具体用途判定；聊天机器人等主受 Art. 50 透明度义务；Annex III 义务已被 Reg (EU) 2026/1744 延至 2027-12-02；另**遗漏 Art. 5 禁止性条款**（§4M） |
| **SC-G** | v0.1.0 写「Kindred PS-EDS」为独立集团 | 依全球件更正 D：Kindred 于 2024 年为 FDJ 收购，2025 年集团更名 FDJ UNITED；应写 `FDJ UNITED / legacy Kindred PS-EDS`（全球件引官方源；本轮未独立复核） |
| **SC-H** | v0.1.0 §4A「承接移植总表 §2，70 家不再重列」 | 违「一个不漏」之自足性；本件全列 |
| **SC-I** | 本轮初测以 shell `grep -c $'\r'` 报源件 #1、#2 有 3 / 1 个「CR 行」 | **测量方法错误**：执行环境为 dash，`$'\r'` 不作 ANSI-C 转义，所计非回车字节；经 Python 逐字节重测，九件 CR 字节均为 0。§0.4 已按重测值更正。前轮 v0.1.0 之「全 LF」结论不受影响 |

### 3.3 本轮一手核实结果

| 命题 | 结论 | 等级 |
|---|---|---|
| Optimove × Smartico | 2026-04-06 双方公告「签署协议 / to acquire」；双方明言各自独立运营、品牌与团队不变；**交割完成之一手证据未见**（Mergr 之「acquired」为聚合站措辞） | 签约 OBSERVED[P1]；交割 UNKNOWN |
| Visa × Featurespace | 2024-09 签署最终协议；**2024-12-19 完成**（Visa 公告 + SEC 8-K） | OBSERVED[P0] |
| EU AI Act 数字综合法 | Reg (EU) 2026/1744，2026-07-24 刊登公报、2026-07-27 生效；Annex III 高风险义务延至 **2027-12-02**，Annex I 延至 **2028-08-02**；Art. 50 透明度义务仍自 **2026-08-02** 适用 | OBSERVED[P2→P0 待原文]（多家律所一致，公报原文本轮未抓取） |
| Playtech × Snaitech | 2025-04-30 完成向 Flutter 出售，€2.3bn | OBSERVED[P1] |

### 3.4 M 系列现状（移植总表 M-1~M-11）

M-1 已裁定（Evolution AI 降级）｜**M-2 UNRESOLVED**（ARC 26↔近 30，须附时点并列）｜**M-3 UNRESOLVED**（BetBuddy 15↔17 辖区；全球件另引 Playtech 2025 年报「28 个品牌使用 BetBuddy」——口径为品牌数而非辖区数，不解 M-3）｜**M-4 部分裁定**（§3.3）｜M-5 已裁定（DraftKings 降 INFERRED）｜M-6 已裁定（SOFTSWISS 跨年不可比；全球件新增「2025 年 1–8 月阻止 €15M+、关闭 56k+ tasks」亦不得与前年比）｜M-7 已裁定（禁令工具）｜M-8 已裁定｜M-9 已裁定（AI 荷官独立成章）｜M-10 已裁定（B2B/B2C/跨客户分母不可加）｜M-11 已裁定（纳秒）。

---

## §4 主体全名册（一个不漏 · 自足编号 · 强制定级）

> **完整性×严谨性调和声明（沿用）**：一个不漏地列出，但每主体强制挂证据等级。列入 ≠ 已核实；UNKNOWN / INFERRED 者不得在对外材料写成「业界标准」或「已投产」。「完美真人可移植/对抗」栏为本件建议。出处注：T=移植总表，G=全球件，V2=V2.0.0，I=源件 #2，Q=源件 #1，D01=v0.1.0，S=本轮检索。

> **计数口径**：v0.1.0 采移植总表「**70 家 + 9 类**」（SC-A）；本件自足编号 #1~#72（部分编号为组，组内逐一点名）+ §4L 跨行业对标 + §4M 十二类监管标准，可复算。

### 4A. 真人内容 B2B 供应商

| # | 主体 | 优势 | 劣势 / 局限 | 等级 | 完美真人可移植 / 对抗 |
|---|---|---|---|---|---|
| 1 | **Evolution**（含 Ezugi、NetEnt Live、Red Tiger、Big Time Gaming） | 全球最大真人规模、成熟产品族（Speed / Lightning / First Person / Salon Privé）、多地工作室与容灾；年报称约 2,000 张 Live tables、22,000+ 员工（G 引年报） | 2026 Q2 亚洲同比下滑、合规尾巴（UKGC AML 披露）、Galaxy 收购终止、格鲁吉亚减员；价格最高；AI 宣称证据污染（M-1） | 地位 OBSERVED[P1]；AI **INFERRED（M-1）** | 移植：QoE、工作室产能、产品族管理、跨区容灾；对抗：以受规×透明条款×华人本地化切其「高价 + 合规负债」 |
| 2 | **Ezugi**（Evolution 旗下） | EZ Baccarat 局速最快、本地化 | 被定位为下沉品牌、迭代优先级低 | OBSERVED | 局速基准；不以速度牺牲下注窗 p99.9 |
| 3 | **Playtech Live**（+ PAM+、IMS、BetBuddy、Featurespace 整合史、Playtech Protect、2026-07 **AI-powered Live Virtual Host**） | Live + PAM + 责任博彩 + 托管一体；2025 年报称 200+ B2B 客户、50+ 受规法域、28 品牌用 BetBuddy（G 引）；2025-04 出售 Snaitech 后转 B2B（S） | 实施/迁移成本高、锁定风险；华人盘口本地化弱；AI Virtual Host 证据为转述（I） | OBSERVED[P1]；Virtual Host INFERRED | 移植：Live×PAM×RG×案件同一数据闭环；对抗：华人本地化×受规之空档 |
| 4 | **Pragmatic Play Live**（Mega Baccarat、Bet Behind Pro 7-Bot、Auto-Roulette；Opti-X 采用方） | 迭代快、移动 UX、多语言、条款较软；Blask 榜 Live Baccarat 居前（D01 检索） | 原创机制薄、跟随式；AI 中台证据弱于 Playtech；Bot 坐桌≠AI 决策 | 半自动 OBSERVED；AI INFERRED | 移植：产品化速度；对抗：原创华人仪式型 IP（§11） |
| 5 | **OnAir Entertainment / Games Global** | 多机位、路单与统计之娱乐化路线（I） | 缺上市级披露 | INFERRED | 娱乐化表现层参考 |
| 6 | **Authentic Gaming** | 实体赌场现场直播，真实性观感好 | 规模小、百家乐深度不足 | INFERRED | 「现场感」对照 |
| 7 | **Vivo Gaming** | 2026 年初东南亚新工作室、泰语/越南语荷官（D01 检索） | 串流与合规履历弱 | INFERRED | 东南亚本地化对标 |
| 8 | **LuckyStreak / Creedroomz / Stakelogic Live / Atmosfera / BetGames(.TV)** | 便宜、可定制、上线快 | 流动性小→单桌人气塌方；财务与容灾存疑 | INFERRED | 反面教材：流动性死亡螺旋 |
| 9 | **Bombay Live / SuperSpade** | 印度向本地化 | 与百家乐主战场弱关 | INFERRED | — |
| 10–21 | **亚洲系 12 家**：SA Gaming、Dream Gaming (DG)、**WM Casino / WM Perfect Group（见 P-6）**、Asia Gaming (AG)、AllBet、Sexy Baccarat / AE Sexy、Pretty Gaming、Venus Casino、Big Gaming、eBet、KingMaker、（BetGames.TV 已列 #8） | 华人玩法（竞咪、切牌、龙宝、牛牛、Interactive Bid Baccarat）、桌台密度、东南亚线路；SA 持 PAGCOR、新获南非 WCGRB（T）；DG 直播自泰国（P） | 无模型卡/数据集/审计报告；欧美牌照少；假台/克隆站盗用（V2，INFERRED）；AI「自动」仅指机械发牌 | **UNKNOWN[P3]**（UNKNOWN ≠ 未使用） | 产品/桌台/地区化 benchmark；AI 一律采购前尽调；对抗：以签名视频与公开核验页击破克隆站（§11.4） |

### 4B. AI 荷官与视觉新势力（独立成章，不与 Evolution 同表 · M-9）

| # | 主体 | 状态 | 等级 | 要点 |
|---|---|---|---|---|
| 22 | **Octane Studios** | AI Baccarat 首发；品牌化、数日交付、认证 RNG + provably fair | OBSERVED[P1] | **RNG 引擎与渲染引擎强制分离**；监管路径为 RNG 产品 |
| 23 | **Sentient Studios（原 BetHog）**（Nigel Eccles） | AI 荷官 Sunny、12 语言、$10M A 轮（2026-04）；Blackjack 已上线，百家乐/轮盘预计 2026 年底；自称参与度 10× | OBSERVED[P1]；10× 为自述 | 音频须刻意脏化；渲染延迟 >2s 口型失同步即信任崩塌 |
| 24 | **Avanti Studios** | AI 生成数字克隆荷官（3D + AI）、云串流（I） | INFERRED | 数字克隆涉肖像权与深伪透明义务（Art. 50） |
| 25 | **BetConstruct**（CRM AI、Umbrella AI、AI Lobby、Betting Mate AI；2026「KISS AI Live Casino」） | 产品线激进 AI 化（I） | INFERRED | 「实时调整荷官/桌面/视觉」须证其不触结果层 |
| 26 | **Winfinity** | 计算机视觉牌桌识别，百家乐直用（I） | INFERRED | 视觉读牌作双读来源之一（§11.2） |
| 27 | **Playtech AI-powered Live Virtual Host** | 见 #3 | INFERRED | 讲解/互动层，非结果层 |

### 4C. 实体智慧桌与陆地营运

| # | 主体 | 要点 | 等级 |
|---|---|---|---|
| 28 | **Angel Group** | AI + RFID + 姿势辨识；Sands China 千张级（P/V2）；另称澳门/新加坡/菲律宾/澳洲约 2,000 张（I）——**分母不同，引用须带范围（X-17）** | OBSERVED[P1]（部署）/ INFERRED（数字） |
| 29 | **Arb Labs（ChipVue）× SCCG Management** | AI 光学识别实时注额，自称 >95% 实时准确率（I） | INFERRED |
| 30 | **IDX Games** | AI chatbot 桌游运营洞察 | INFERRED |
| 31 | **Las Vegas Sands / Sands China、Solaire、SkyCity、MGM、Caesars** | 智慧桌采用方；VIP/生命周期模拟之陆地样板（I） | 采用 INFERRED |

### 4D. B2C 营运商与集团

| # | 主体 | 要点 | 等级 |
|---|---|---|---|
| 32 | **Entain**（ARC + Protector Model；整合 Mindway） | 26 或近 30 标记（M-2）；22 市场一期、9 市场实时；>90% 准确度无基准 | OBSERVED（数字冲突） |
| 33 | **Flutter**（RTI；FanDuel、PokerStars、Sportsbet、Betfair、**Sisal**、**Snai**（2025-04 收购）） | 集团 Responsible AI；**Sportsbet Jeeves AI**：客户关系服务能力约 400→1,200、人机一致约 72%，终决仍由员工（I） | RTI OBSERVED；Jeeves INFERRED |
| 34 | **FDJ UNITED / legacy Kindred（Unibet；PS-EDS）** | 见 SC-G | OBSERVED（G 引） |
| 35 | **BetMGM、Sisal、Stardust、OPAP** | Optimove / ComplianceSuite 案例；增幅为供应商案例 | 供应商案例 |
| 36 | **DraftKings**（含 DraftKings Casino；2026-01 集成 Gamalyze 据 P） | ⚠ 反面案例：据转述 NYT，以 ML 找「最可能输钱者」定向发券（M-5） | INFERRED |
| 37 | **Allwyn**（2026-03 完成与 OPAP 组合，G） | 彩券/博彩集团治理 | OBSERVED（G 引） |

### 4E. B2C 消费站点（源件 #2 所载，全部定级为线索）

| # | 主体 | 源件所载优势 | 源件所载局限 | 等级 |
|---|---|---|---|---|
| 38 | **Stake**（Stake.com） | 加密货币赌场，真人百家乐以 Evolution 为主；VIP 返水模型据称为「house edge 之 10%」（即 theo 型，§9） | 加密合规与地域限制 | INFERRED |
| 39 | **Pinnacle** | 低边际；代理佣金按 turnover 0.25%–1.5%（I） | — | INFERRED |
| 40 | **Rivalry** | VIP 以促销期**净亏损**为 cashback 基础（I） | 净输返水之追损风险（§9） | INFERRED |
| 41 | **Betway** | 部分市场「首 24 小时按 Net Loss 返还」（I） | 同上 | INFERRED |
| 42 | **Dafabet** | 亚洲老牌，数百张真人桌，供应商多元；Playtech 保险百家乐与 VIP 包桌 | 保险类产品实际提升边际 | INFERRED |
| 43 | **bet365、888.com / Golden Matrix Group、188BET（Frosmo）** | 推荐引擎；Golden Matrix「你试过/你可能喜欢」每日更新 | Frosmo 数字量级不可信（X-18） | UNKNOWN |
| 44 | **BTCC 娱乐城、GoldenTiger VIP** | USDT 入金；返水最高 1.8%；龙虎斗 1:13 | 高门槛；加密波动 | UNKNOWN |
| 45 | **Baccarat888** | —— | **「每局庄闲胜率 AI 预测」为对独立同分布结果之误导宣传——反面案例** | UNKNOWN（宣传） |
| 46 | **CryptoBaccarat** | 「连输 5 局弹出冷却提示」之 RG 雏形 | 仅加密货币 | UNKNOWN |
| 47 | **美国受规州站**：BetMGM、DraftKings Casino、FanDuel Casino、Caesars Palace Online、BetRivers、Borgata Online、Golden Nugget Online | 州级牌照、地理围栏与严格 KYC | 州际隔离、促销附流水与排除条款 | INFERRED |

### 4F. 平台 / PAM / CRM

| # | 主体 | 要点 | 等级 |
|---|---|---|---|
| 48 | **SOFTSWISS**（Anti-Fraud、BM3、DOSSIER） | 2022 61,810 请求 / €16M+；2023 100,000+ / €13M；2025 1–8 月 €15M+、56k+ tasks（G）——**逐年口径不可比（M-6）**；COO：终决留给专家 | OBSERVED（自述） |
| 49 | **EveryMatrix**（CasinoEngine、**EveryMatrix Bonus Guardian**；与 Future Anthem 个性化） | 以已知滥用者历史训练 ML、按角色处置 | OBSERVED；≠ 串通/洗钱检测 |
| 50 | **Smartico** | **唯一明确 RL/MAB 落地文档**（contextual bandits、RNN 7/14/30 天流失 75.94%）；2019 年保加利亚创立 | RL 证据 INFERRED（第三方博客）；收购见 §3.3 |
| 51 | **Optimove / Optimove Opti-X / Optimove Gamify**（Pragmatic Play 采用 Opti-X） | 20+ 推荐模型、700+ 游戏标题（自述） | OBSERVED（自述） |
| 52 | **GiG、NuxGame（+ iDenfy）、Future Anthem、CleverBet Labs、Track360、SCCG Management** | 推荐 / KYC 嵌入 / 个性化 / 联盟风险分层 / 桌游合作 | INFERRED（Track360 为 sharp 旗标驱动之联盟佣金分层，D01 检索） |

### 4G. 风控 / KYC / AML / 反机器人

| # | 主体 | 要点 | 等级 |
|---|---|---|---|
| 53 | **Featurespace ARIC** | 2008 年剑桥创立；Playtech 2018-01 整合；**Visa 2024-12-19 完成收购**，并入 Visa Risk & Identity Solutions（S）；「Betfair 2008 首用」（P/V2）未核 | 并购 OBSERVED[P0]；首用 INFERRED |
| 54 | SEON · GeoComply（2 亿+ 设备网络）· Sift · CrossClassify · Group-IB（XAI）· **cside**（250+ 浏览器信号，识别 Operator / Claude for Chrome / Playwright / Puppeteer / Selenium） | 设备、行为、机器人 | INFERRED（自述） |
| 55 | Sumsub · Onfido · Jumio · Veriff · iDenfy · Shufti（+ Cevro AI） | KYC、活体、深伪检测 | INFERRED / OBSERVED（集成） |
| 56 | Flagright · ComplyAdvantage · NICE Actimize · ACT Fraud Rings（2026 syndicate 可视化）· Infocredit ComplianceSuite.ai · **Quantexa（跨行业 AML 标杆）** | AML、实体情报、统一案件 | INFERRED；Quantexa 跨行业 OBSERVED |
| 57 | Cevro AI（客服 Agent，80–90% 工单自称）· InteractiveAI · Moveo.AI · **HENGPLAY**（AI 交易验证，自称 30 秒存提，I） | 客服代理与支付运营 | INFERRED / UNKNOWN |
| 58 | Cloudflare Bot Management · Akamai · HUMAN Security · FingerprintJS · JA4/JA4+ · Senzing · Zingg · Elliptic | 机器人管理、指纹、实体解析、链上 AML 基准 | INFERRED（跨行业工具） |

### 4H. 责任博彩 AI

| # | 主体 | 要点 | 等级 |
|---|---|---|---|
| 59 | **Mindway AI**（GameScanner / Gamalyze） | ≥87% 专家检出（自述）；**900 万↔1,470 万 / Better Collective↔Entain ARC 冲突未解（X-4）** | OBSERVED（数字 UNRESOLVED） |
| 60 | **Playtech BetBuddy** | 三层风险评级、提前数周预测；15% 高风险玩家收个性化消息一小时内自设存款限额（对照试验，自述）；WVU 合作 | OBSERVED |
| 61 | Neccton Mentor · Sportradar Bettor Sense · Entain ARC · FDJ UNITED PS-EDS · Flutter RTI | 早期检测与实时干预 | OBSERVED / INFERRED |

### 4I. 玩家端对抗工具与研究方（敌方，非采购对象）

| # | 主体 | 宣称 | 等级 |
|---|---|---|---|
| 62 | **FPLAY** | 多平台 API 自动下注（DG / WM / AllBet / WG） | INFERRED |
| 63 | **Mysports.AI** | 自动读牌、**剩余牌分布计算**、Telegram 推送高 EV | INFERRED |
| 64 | Oracle Baccarat Predictor · BACC.BOT · BaccaratAI | 路单 ML / 深度学习「预测」 | INFERRED（主结果预测无科学依据；边注状态依赖 EV 则真实存在） |
| 65 | **Differential Labs** | 边注占亚洲赌场 40–60% 收入；AI 辅助算牌年损 5–7 亿美元（ASGAM 2026-08-30） | OBSERVED（报导）/ 数字 INFERRED |

### 4J. 体育（v0.1.0 全保留 + 全球件 SEC/年报加厚）

| # | 主体 | 要点 | 等级 |
|---|---|---|---|
| 66 | **Sportradar**（类别：数据 + 交易 + 诚信；NASDAQ:SRAD；Betradar 赔率、**Managed Trading Services (MTS)**、**Integrity Services / UFDS AI**；NBA / NHL / NFL 数据与诚信伙伴） | 2025 20-F 披露实时 AI 推理、低延迟网络、**liability-driven odds adjustment**（G）；330+ 诚信伙伴、70+ 运动 | OBSERVED[P0]（20-F）/ UFDS「AI」程度 INFERRED |
| 67 | **Genius Sports / GeniusIQ**（类别：数据 + 诚信；Betgenius 源） | 2025 20-F 披露 AI/ML、计算机视觉、官方数据、赔率与诚信（G）；**NFL 官方数据版权**（美国官方数据独占之结构性路径）；2026-02 收购 Legend | OBSERVED[P0] |
| 68 | **Kambi** | 2025 年报：AI-driven trading 覆盖 48% 注单（G）；40+ 运营商托管 | OBSERVED[P1] |
| 69 | OpenBet（Light & Wonder / L&W）· SBTech（DraftKings）· BetConstruct · Stats Perform · IMG Arena · SIS · Oddin.gg（电竞）· **Opta** · OpticOdds · Don Best · Metric Gaming / Amelco（D01 自补） | 数据、定价、交易引擎：liability management、in-play margin engine、**sharp-bettor 行为 ML 检测**、盘口挂起 | OBSERVED（公司）/ ML 细节 INFERRED |

### 4K. 彩券（v0.1.0 全保留 + 全球件加厚）

| # | 主体 | 要点 | 等级 |
|---|---|---|---|
| 70 | **Brightstar Lottery**（NYSE:BRSL，原 IGT 彩券；2025-07 Gaming&Digital 售予 Apollo 基金；约 90 客户、美国 46 辖区中 26 主供、约 6,000 员工；OMNIA） | 纯彩券技术 | OBSERVED[P0]（6-K）；**终极控股说法冲突**：一处称 BlackRock、一处称 Apollo 仅购 Gaming 段 → 仍待一手核实 |
| 71 | **Scientific Games**（2022 拆分后 Brookfield 拥有之纯彩券体，与 Light & Wonder 分立；Momentum 2026 部署亚利桑那/明尼苏达；特拉华 iLottery 采 SG PAM、钱包、KYC、CRM、奖金引擎、Healthy Play，G）· **Pollard Banknote** · **Inspired Entertainment** · Instant Win Gaming | 全渠道：零售与数字统一账户 | OBSERVED[P1] |
| 72 | Intralot（Bally's Intralot S.A.）· Genlot · AGTech · NeoPollard · FDJ UNITED（v0.1.0 写作 FDJ United）· Sisal · Lotto NZ · Macau SLOT · **Allwyn**（#37；并 OPAP；UK National Lottery 现营运方，替代 Camelot；已迁瑞士） | 中央系统、特许营运 | OBSERVED |

### 4L. 跨行业对标主体（仅作方法论对标，Q/A/G 所载）

宇航国防：SpaceX（WARPDRIVE、自研遥测）、Blue Origin、Rocket Lab、Airbus（Skywise）、Boeing、Lockheed Martin、Anduril、Thales、Eutelsat、BAE Systems、ST Engineering、NASA（VEDA、cFS/COSMOS）、US Space Force（UDL、Warp Core）｜数据与智能：Palantir（Gotham/Foundry/Warp Core）、C3 AI、Oracle、Snowflake、Databricks、SAP、Microsoft、AWS、Google｜算力：NVIDIA、TSMC｜安全：CrowdStrike、Palo Alto Networks｜量化：Citadel、Jane Street、Two Sigma、Renaissance、DE Shaw、Man Group（ArcticDB）｜支付：Visa（Featurespace）。
**使用原则**：迁移数据完整性、可回放、模型治理、容灾、供应链与实验方法；不把专用高成本实现当先进性象征。

### 4M. 监管、标准与学术（v0.1.0 九类保留，精确化并扩充）

| 类 | 体系 | 强制性 | 本件要点 |
|---|---|---|---|
| M1 | MGA AI Gaming Charter（2026-09-18，与 MDIA，48 页） | 自愿 | 清单、问责、人工覆盖、审计轨迹；警告 AI-washing |
| M2 | UKGC LCCP 3.4.3 | 强制 | 强伤害指标须及时自动化处理；**自动流程施用后须逐客户人工审视，并允许客户质疑**（G 更正 F） |
| M3 | **EU AI Act**（Reg (EU) 2024/1689，经 Reg (EU) 2026/1744 修订） | 强制 | **Art. 5 禁止性条款**（2025-02-02 起，本件新增）：操纵性/欺骗性技术、利用因年龄、残障或特定社会经济处境之脆弱性而实质扭曲行为并致重大伤害——**利用追损脆弱期之定向营销是否落入，属 CONDITIONAL，须法律意见**；**Art. 50** 透明度（聊天机器人、深伪/AI 荷官披露）自 2026-08-02；**Art. 6 + Annex III** 按用途判高风险，义务延至 2027-12-02；博彩非 Annex III 类别本身（G 更正 E）；Annex III 信用评分条对「金融欺诈检测」之除外——原文须核 |
| M4 | GDPR Art. 22 | 强制 | 自动化决策之解释与异议权 |
| M5 | NIST AI RMF（含 GenAI Profile）· ISO/IEC 42001 | 框架/认证 | Govern–Map–Measure–Manage |
| M6 | **SR 26-2**（2026-04-17，取代 SR 11-7 与 SR 21-8；G 引联储官网，本轮未独立复核） | 银行业强制 | 模型清册、概念稳健、独立验证、**供应商模型尽调**、持续监控、结果分析、override 可解释、退役 |
| M7 | GLI（含 GLI-11 RNG）· eCOGRA · BMM · Gaming Labs · 同类实验室 · **WLA（World Lottery Association）Security Control Standard** | 强制 / 行业 | RNG 与开奖完整性；**彩券另加**：开奖 draw integrity 规范 |
| M8 | PAGCOR · MGA · UKGC · WCGRB · Curaçao · Isle of Man | 牌照 | 法域政策矩阵（B-5） |
| M9 | 学术：WVU 博彩研发中心、PMC《AI Personalization…》、Springer《AI-Enabled Player Risk Detection 需基准》 | — | 基准缺失为全行业硬伤 |
| M10 | **澳门第 16/2022 号法律**（博彩中介人） | 强制（澳门） | 据 DeepSeek 转述禁止中介人与承批公司作输赢分成——**INFERRED，法条须核** |
| M11 | **FINRA Rule 2150(b)**（跨行业类比） | 证券业强制 | 禁止对客户「保证不亏」——**净输返水与之同构**（§9） |
| M12 | **体育诚信另加**：IBIA、ESSA、各联盟 official-data / integrity 框架 | 行业 | — |

---

## §5 统一参考架构（ARCH-L0~L5，沿用并化解命名冲撞）

### 5.1 ARCH 层（v0.1.0 原样保留，冠 ARCH- 前缀）

```
ARCH-L0 采集：PTP+GNSS 授时 · JA4+/FingerprintJS · 机器人管理 · 蜜罐+Canary token · 视觉（百家乐牌面 / 彩券票面核验）· 牌局黑匣子录制
ARCH-L1 传输：Disruptor(ns) → Aeron/Chronicle(μs) → Redpanda/Kafka(ms, 无 GC) → Flink CEP   ⚠ 禁令下仅平台侧
ARCH-L2 存储：热 ArcticDB/QuestDB · 温 Iceberg+Parquet · 冷 S3+WORM · 研究 DuckDB+Arrow · as-of 时间旅行 · 六元组+SBOM
ARCH-L3 特征：Feast(point-in-time) · 数据契约 + OpenLineage · ALCOA+ · DQ Gate(GE/pandera)
ARCH-L4 判决：三管线隔离（Bell-LaPadula + 数据二极管）· 域模型按垂直专化（§5.4）
ARCH-L5 治理：模型清册+Challenger(SR 26-2) · Model Card+AIBOM · IQ/OQ/PQ · 21 CFR Part 11 双人复核 + HSM · SHAP/反事实→申诉 · ADWIN→FDIR 降级 · CPCV+PBO+DSR · 负对照+E-value · OODA/F2T2EA 之 Assess 回流标签
```

**禁令下的可行性分界（移植总表盲区 B 结论）· 沿用**：ARCH-L0~L2 属平台侧，现禁令下**一行都验证不了**；ARCH-L3~L5 于现有 R + Python + DuckDB **今天就能跑**，且那才是 a168 缺口所在。**跨行业移植精力全部压在 L3–L5。**
**禁令工具剔除声明（X-6）· 沿用**：本件不含 StarRocks / DolphinScheduler / Superset / SeaTunnel 及任何需驱动级、提权、常驻服务之技术。编排一律 `targets`/Snakemake（禁令外）。

### 5.2 三套「L」之对照（化解 X-11e）

| ARCH（本件） | GDI-OS（全球件） | 红队 L 轴（项目） |
|---|---|---|
| ARCH-L0 采集 | L0 Source | L1 数据真相 |
| ARCH-L1 传输 | L1 Immutable Event Ledger | L1 / L2 |
| ARCH-L2 存储 | L1 Ledger + L2 DQ/Point-in-Time | L1 · L7 数据治理 |
| ARCH-L3 特征 | L2 + L3 Feature & Entity | L2 计算正确 · L3 统计效度 |
| ARCH-L4 判决 | L4 Detection → L5 risk topology → L6 Constrained Decision → L7 Case → L8 Action | L4 因果 · L5 模型科学 · L6 量化决策 |
| ARCH-L5 治理 | L9 Outcome Ledger + L10 Causal Evaluation & Monitoring | L8 模型风险与监控 · L9 决策治理与人工监督 |

> **命名规约**：凡架构层一律写 `ARCH-Ln`；凡 GDI-OS 层写 `GDI-Ln`；凡红队层保留 `T·L·S` 三轴编码。三者不得裸写「L3」。

### 5.3 注册表双对象（X-20 之建议解，P-5 裁定）

两名并非必然重复，而可为两个互补对象：

- **`registry_risk_typology`（分类学）**：风险类型体系本身——按 MITRE ATT&CK 三层（战术 → 技术 → 程序）重构之 15 类 / 66 准则；版本化、低频变更。
- **`registry_risk_topology`（拓扑实例表）**：`实体 × 风险 × 时间 × 概率 × 严重度 × 置信 × 证据 × 处置状态`，高频写入。采纳全球件 §7.1 schema：

```text
as_of_time · entity_type · entity_id · risk_taxonomy · risk_subtype
model_id · model_version · rule_version
probability · calibrated_probability · severity · confidence · uncertainty
evidence_count · evidence_refs · first_seen · last_seen · trend
eligibility · recommended_action · human_review_required
decision_status · appeal_status · rollback_flag · outcome_status
```

外键：`topology.risk_taxonomy → typology.technique_id`。**若权威 SQL 总包已定其一，则以总包为准，本解作废。**

### 5.4 ARCH-L4 域模型专化（v0.1.0 §5.1A/B/C 全保留并加厚）

**A. 百家乐**
- 反诈/串通：Sigma → PU Learning + Snorkel → k-core / Leiden / TGN → 元标签（出手与否）→ TEWA 分配。
- **边注状态依赖 EV 对抗**：侧注边际随靴内剩余牌组成而变（这正是 Mysports.AI / Differential Labs 所利用者）；检测「下注于边注之时点与靴内状态 EV 之相关」——主动识别而非仅规则阉割。
- 荷官审计：UEBA **同伴群组分析**（同班次 / 同桌型 / 同限红比，而非与全体比）+ 航空 Just Culture（区分操作失误与故意舞弊）。
- **返水套利**：对打刷水识别（§9.3 之阈值条件）。
- QoE：视频延迟、丢帧、结算延迟之遥测，防「被误读为操纵」。

**B. 体育博彩**
- **liability management（合法灰带 · 铁律一边界）**：按 sharpness / 流动性对客户降注/限额是**行业标准且合法**，但必须——(a) 依据 sharp / 套利 / liability，**绝不用 RG 脆弱性分数**；(b) 全程可审计、可申诉；(c) 与 RG 管线格隔离。**越此三条即触铁律一。**
- **match-fixing / 诚信**：betting-pattern 异常检测（对齐 Sportradar UFDS 思路）= 图 + 异常 + 突变点，与百家乐串通同构。
- **courtsiding / 延迟套利** = 体育版「迟下注」= HFT **共置/时钟同步**问题：靠 PTP 授时 + 盘口挂起时延（p99.9 在下注窗内）而非纳秒。
- **sharp/套利/matched-betting**：金融市场微结构（线口移动 ≡ 价格发现）+ 实体解析（同一自然人多账户）。
- 须额外建模（全球件 §4.2 采纳）：事件时 / 市场时对齐与时钟质量；官方 feed 质量（延迟、缺包、异常比分更新）；odds / fair price / margin / liability；bet acceptance 与敞口上限；结算规则引擎与赛事取消/更正重放。
- 体育 KPI（采纳）：feed latency p99.9、stale-odds exposure、人工交易负荷、接受率、价格误差、结算异常、诚信告警 precision。

**C. 彩券**
- **draw integrity（头等）**：物理开奖 + 认证 RNG（GLI-11 / WLA SCS）；用**确定性系统思想**（形式化验证 `z3-solver` / TLA+ 验开奖不变量、TMR 三模冗余表决、WORM + HSM 不可篡改日志）——航天/核能链移植最对口。
- **AML（头号止损）**：Quantexa 式实体解析 + 图谱 + SAR 闭环。
- claim fraud / 内幕：中奖核验 = KYC；内幕 = 同伴群组 + 购票时点相对开奖之时序异常。
- 零售商舞弊、票证生命周期 / 序号审计、账户接管（全球件 §5.2 采纳）。
- iLottery / 快开彩：套用百家乐之 RG 管线。**不照搬赌场「提升游戏时长」目标**。

---

## §6 跨行业移植（v0.1.0 十三行业全保留 + 新增七项）

| 移植来源 | 落地一件事 | 百家乐 | 体育 | 彩券 |
|---|---|---|---|---|
| 金融/HFT | 元标签 + CPCV/PBO/Deflated SR；p99.9 尾延迟与背压 | ★★★★★ | ★★★★★ | ★★★☆ |
| 银行 | **拒绝推断** + WOE/IV + 逆向压力测试 + **SR 26-2 供应商模型尽调** | ★★★★★ | ★★★★☆ | ★★★★☆ |
| 电商 | CUPED + switchback + 序贯检验 + point-in-time | ★★★★☆ | ★★★★☆ | ★★★☆ |
| SRE/数据工程 | **OpenLineage 血缘 + `targets` 编排**；SLO；优雅降级 | ★★★★★ | ★★★★★ | ★★★★★ |
| 资安 | **Sigma + MITRE ATT&CK 三层 registry + UEBA 同伴群组** + Detection-as-Code | ★★★★★ | ★★★★★ | ★★★★☆ |
| 反恐/反诈 | **Splink 实体解析（三档阈值）+ k-core/Leiden/TGN** | ★★★★★ | ★★★★★ | ★★★★★ |
| 人工智能 | **PU Learning + Snorkel + 主动学习**（攻标签缺口） | ★★★★★ | ★★★★★ | ★★★★☆ |
| 宇航 | IMM 在线状态估计 + FDIR 降级 + 黑匣子回放 | ★★★★☆ | ★★★★☆ | ★★★☆ |
| 军工 | TEWA 分配 + MHT 多假设 | ★★★★★ | ★★★★★ | ★★★★☆ |
| 制药/电力/航空/核能 | **ALCOA+ + 21 CFR Part 11 + IQ/OQ/PQ + FMEA RPN**；**确定性/形式化验证** | ★★★★★ | ★★★★☆ | **★★★★★（开奖公信力）** |
| 科研院 | 预注册 + **负对照结局 + E-value**；OpenBLAS | ★★★★★ | ★★★★★ | ★★★★☆ |
| 确定性系统 | 优雅降级优于失败 | ★★★★★ | ★★★★★ | ★★★★★ |
| 供应链安全 | SBOM（CycloneDX）+ SLSA + Sigstore | ★★★★☆ | ★★★★☆ | ★★★★☆ |
| **媒体（新增）** | **C2PA 内容凭证 / 签名串流分段 + 会话水印** → 击破克隆站与「假台」 | ★★★★★ | ★★★☆ | ★★★★☆（开奖直播） |
| **加密博彩（新增）** | **Provably fair 承诺–揭示（commit–reveal）** → 延伸至真人牌靴（§11.3） | ★★★★★ | — | ★★★★☆ |
| **支付（新增）** | Featurespace 型自适应行为分析（Visa 并入后之路线）；钱骡链 | ★★★★★ | ★★★★☆ | ★★★★★ |
| **流媒体（新增）** | LL-HLS / WebRTC QoE 遥测、多区域容灾 | ★★★★★ | ★★★★☆ | ★★★☆ |
| **精算 / 陆地赌场（新增）** | **theo（理论输值）计价**：返水、VIP、评级一律以期望而非实现结果为基 | ★★★★★ | ★★★★★（以 margin 替代 edge） | ★★★☆ |
| **证券监管（新增）** | FINRA 2150(b)「禁保证不亏」→ 净输返水之监管同构警示 | ★★★★☆ | ★★★★☆ | ★★★☆ |
| **医疗 AI（新增）** | 临床决策支持之人在环、误差分析、禁「自动诊断即处置」 | ★★★★☆ | ★★★★☆ | ★★★★☆ |

**不应盲迁移**（全球件 §6.1 采纳）：FPGA / RDMA / 内核旁路（除非压测证明通用流处理不能满足 SLA）；Kelly 与交易 alpha 不得映射为「让玩家更输」之目标。

---

## §7 攻击面（v0.1.0 全保留 + 全球件 18 条去重并入 + 本轮新增）

**通用（承接）** · v0.1.0：虚假宣称五型 · AI 荷官信任瓦解 · 奖励优化反噬 · 数据投毒 · Bot 代理绕过 · 图谱假阳性 · 黑箱处置 · 用途冲突 · 只报 AUC · 随机切分泄漏 · 清单即供应链风险 · PU 先验 π 敏感 · Splink 误合并不可逆 · Sigma 阈值须重标 · 合成数据分布外 · `targets` 缓存失效语义 · 「纳秒」话术污染。
**全球件并入（去重后新增）**：处置反馈偏差（封禁后行为不可观测 → censoring）· 模型漂移（活动/地区/季节）· 供应商锁定（标签、特征、案件证据不可导出）· QoE 失真被误读为操纵 · 不可比 KPI（跨年、跨产品、跨 B2B/B2C 分母）· 过度工程（同时上 FPGA/GNN/Transformer/RL，无法归因）· 灾难降级失败（模型服务不可用阻塞投注结算）。
**体育专属（保留）**：sharp/套利团伙（实体解析）· **courtsiding 延迟套利** · match-fixing（诚信监控滞后）· 官方数据单点依赖（版权方即命脉）· in-play 盘口挂起时延失控 · **liability 限额误用 RG 分数（触铁律一）**。
**彩券专属（保留）**：AML structuring / 中奖洗钱 · claim fraud · 内幕购票 · 二次销售 · 开奖公信力受质 · 快开彩 RG 伤害。
**本轮新增**：
1. **返水对打刷水**：有效投注返水率高于双边合计边际之一半时，对打即正期望（§9.3）。
2. **净输返水之追损补贴**（§9.2）。
3. **克隆站 / 假台**：盗播视频、仿冒品牌、截流资金。
4. **「AI 预测胜率」欺骗性宣传**（Baccarat888 型）——对手与自家营销皆须禁绝。
5. **取消提款挽留**（withdrawal reversal）诱导回投（Perplexity 答复列为行业最危险做法之一）。
6. **身份字段漂移**（X-20）导致血统断链。
7. **分母漂移**（X-14b「1,700 万」之类无口径数字进入决策）。
8. **AI 转述链污染**：九家 AI 互相转述使 INFERRED 数字「看似多源」——**同源多转述不得计作独立证据**。
9. **自评错位**（B-12）：把自家当竞争者用 UNKNOWN 评分，放弃了唯一拥有一手数据的对象。

> **止损标的量级（沿用 v0.1.0）**：均 INFERRED，且 **house_edge 未锁前不构成可结算 ROI**（§0.3 P-1）——百家乐边注 AI 算牌亚洲年损 5–7 亿美元（Differential Labs / ASGAM）；体育 sharp/套利与假球损失、彩券 AML 罚没与信誉损失均须自家一手数据定标。

---

## §8 上线门禁与验收协议

### 8.1 挑战者阶梯（全球件 §8.1 采纳）

规则/统计基线（rate、Wilson 区间、EWMA、GLM/评分卡）→ GBDT（XGBoost/LightGBM/CatBoost）→ 生存/竞争风险 → HMM/状态空间 → 图/实体解析 → 序列/Transformer（**仅当长序列带来稳定 OOT 增益**）→ contextual bandit / RL（**仅当动作可控、reward 合规、OPE 通过、因果基础可靠，小流量**）。

### 8.2 IQ / OQ / PQ（v0.1.0 保留 + 全球件验收协议并入）

- **IQ**：SBOM 完整 · 随机种子固化 · `targets` DAG 可断点续跑 · 六元组齐备 · DQ Gate（行数/唯一键/缺失/join 覆盖/时间连续/币种归一/PSI）· **所有特征 `feature_time ≤ as_of_time`**。
- **OQ**：报 **PR-AUC / Precision@人工产能 / Recall@固定误伤预算 / 校准曲线**（禁只报 AUC）；另加 ROC-AUC（辅）、**Brier、ECE / 可靠性曲线**、成本加权效用；rolling/expanding walk-forward + purge + embargo（**禁随机切分作终证**）；CPCV+PBO；负对照 + E-value；时序以 **MASE / RMSSE**，概率预测以 **CRPS / pinball**（禁裸 MAE 跨量纲比较）。
- **PQ**：经济（Net 止损账；**P-1 未解无经济锚**）· 决策质量（申诉推翻率、回滚率、人日案件数）· 因果（ATE/CATE、CUPED、switchback、doubly robust）· 公平（按币种/地区/游戏/代理/设备分层误报差）· 合规（高影响 100% 人工复核、理由码 100%、**RG→营销隔离稽核通过**、申诉与回滚记录完整）· 安全（最小权限/去标识/访问日志/密钥/保留期）。

### 8.3 永久审计字段（保留）

`case_id / subject_type / subject_id / risk_domain / as_of_timestamp / feature_snapshot_hash / rule_version / model_version / risk_score / confidence / top_drivers / recommended_action / human_reviewer / reviewed_at / final_disposition / appeal_status / rollback_flag`

---

## §9 返水科学裁定（新增 · 化解 X-15）

### 9.1 三族返水之数学性质

设第 i 注注额 $s_i$、该注型之理论边际 $e_i$（由规则表闭式计算），期内实现净输 $L$。

| 族 | 公式 | 与实现结果之关系 | 对打刷水 | 追损补贴 |
|---|---|---|---|---|
| **A 有效投注型** | $R_A = r_A \sum_{i\in \text{valid}} s_i$ | 独立 | **可被套利**（§9.3） | 无 |
| **T 理论输值型（theo）** | $R_T = r_T \sum_i s_i e_i$ | 独立 | **结构上不可套利**（$0<r_T<1$ 时刷水者期望净亏 $(1-r_T)\cdot$theo） | 无 |
| **L 净输型（lossback）** | $R_L = r_L \max(L,0)$ | **依赖实现结果** | 较难刷 | **有**：每多输一单位即退 $r_L$，恰在追损时降低继续投注之边际成本 |

### 9.2 裁定

1. **T 族为科学上占优之默认设计**：结果无关 → 无追损补贴；按边际加权 → 低边际注型贡献小、刷水无正期望；与陆地赌场 theo 评级同源；源件所载 Stake「返 house edge 之 10%」即属此族（INFERRED）。
2. **T 族与 ROI 账共用同一经济锚**：两者都卡在 **P-1**。——**一锚两解**：裁定 house_edge 同时解锁止损金额与最优返水。
3. **L 族**若因市场惯例而保留（Rivalry、Betway 等见于受规市场，INFERRED），须同时满足：固定费率、封顶、事前公示、**不分级递增**、期末结算、**不按 RG 风险个性化**、**RG 为硬否决而非乘数**、不附二次流水。与 FINRA 2150(b)「禁保证不亏」同构，列为监管敏感项。**Gemini 之「以净输返水提高 VIP 粘性与 LTV」动机不予采纳**（X-14e）。
4. 体育「赔率 1.5 以下不计有效投注」之惯例，实为排除低方差刷水注之**粗糙代理**；科学替代为以各市场 margin 计 theo，一式通吃全赔率段。

### 9.3 对打刷水之阈值（百家乐 · 标准规则示意）

标准 8 副、庄家抽水 5% 下之组合数学值：庄约 1.06%、闲约 1.24%、和（8:1）约 14.36%。**此为标准规则之示意，不自动填补本项目之 `house_edge = NULL`**——项目各桌型之规则表、抽水、免佣变体与边注付彩表须由业务方一手提供后闭式计算。

同局以关联账户对押庄闲各 $s$：总有效投注 $2s$，期望损失约 $s(e_B+e_P)\approx 0.0230\,s$，**单位有效投注约 1.15%**。故：

$$r_A > \tfrac{e_B+e_P}{2} \approx 1.15\% \;\Rightarrow\; \text{对打刷水正期望}$$

源件所载亚洲站「返水最高 1.8%」（BTCC，UNKNOWN）若计入对打注即已越线。对策：有效投注定义必须剔除对冲注（同局同桌关联账户反向注），或径改 T 族。

### 9.4 边注之特殊性

边注理论边际为**全靴期望**，但实时边际随靴内剩余牌组成而变——此即 AI 算牌之可乘之机。故：theo 计价用全靴期望；检测用状态依赖 EV（§5.4A）。二者不可混用。

---

## §10 竞争缺口 → 完美真人对策矩阵（blueprint 之输入）

| 对手之缺 | 证据 | 完美真人之对策 |
|---|---|---|
| Evolution：价高、灰产渠道收入被切、合规尾巴 | 季报、UKGC 披露（D01 检索） | 受规 × 透明条款 × 合理价格；合规资产化 |
| Playtech：华人本地化弱 | 产品线 | 华人仪式型玩法 × 受规（**无人占据之交集**） |
| Pragmatic：跟随式复刻 | 产品史 | 原创华人 IP，不追 game show |
| 亚洲系 12 家：无模型卡、审计不透明、克隆站多 | UNKNOWN | **公开模型卡 + 签名串流 + 牌靴承诺–揭示**——把对手之黑箱变为我方之公信 |
| 全行业：round-level 数据不下放、时钟不统一、延迟不可观测 | D01 第一轮 | 可审计 round-level 事件契约 + PTP 统一时钟 + 每客户端 QoE 遥测（分层授权：监管全透明、博弈对手视图脱敏） |
| 全行业：返水多为 A/L 族 | 源件 #2 | T 族返水（待 P-1） |
| AI 荷官新势力：信任、口型、监管路径未定 | OBSERVED + INFERRED | 仅测试线可逆试点；RNG 与渲染强制分离；Art. 50 披露 |
| B2C 站：「AI 预测胜率」误导宣传 | X-18 | 明示「路单为描述性、结果独立」，以诚实为差异化 |

---

## §11 Blueprint · 完美真人百家乐

### 11.1 定位

不是「AI casino」，亦非「复制 Evolution」，而是：
> **可证明、可回放、可审计、可申诉、可降级、可量化增量价值的博彩决策智能平台**（全球件 §15，采纳）——并以**公平、可提款、可退出、可申诉、可审计**为第一层产品竞争力，而非合规补丁（Perplexity 答复，采纳）。

### 11.2 牌局层（游戏层）

- **双读 + 荷官确认 = 三模冗余（TMR）**：RFID/读牌鞋 · 视觉识别（YOLO 类，仅作校验不作结算唯一源）· 荷官确认；不一致即挂起并转人工。
- **下注窗服务器权威时间**：PTP 授时之关注截止；迟到注单按服务器时间拒绝，客户端时间仅作遥测。
- **牌局黑匣子**：每局（视频分段哈希 + 注单 + 牌序 + 各节点时间戳 + 处置）写 WORM，供争议回放。
- **竞咪（squeeze）仪式**：仪式时长与下注窗严格解耦——咪牌开始前下注已封。

### 11.3 公信层（新增 · 本件自提，未见业界落地证据，INFERRED 设计）

- **牌靴承诺–揭示**：具读牌能力之洗牌/验牌设备生成靴序 → 开靴前公示 $H(\text{shoe\_order} \,\|\, \text{salt} \,\|\, \text{table\_id} \,\|\, \text{shoe\_id})$ → 靴毕揭示 salt 与牌序 → 玩家/第三方可验。作用：击破「平台知道底牌/中途换牌」之疑，对真人桌提供与 provably fair RNG 同级之可验性。
- **前提与限制**：须监管批准；须定义坏牌更换、烧牌、读牌失误之协议；承诺值须含高熵 salt 以免泄露牌序（否则反成算牌之助）。
- **签名串流**：C2PA 型内容凭证 + 每会话可见水印 + 公开核验页 → 击破克隆站。

### 11.4 体验层

QoE 遥测（LL-HLS 2–10s / WebRTC 0.2–1s 之选择按桌型）；延迟、丢帧、结算延迟可视化给玩家（「系统状态」而非「神秘」）；多语言；**路单标注「描述性、非预测」**。

### 11.5 经营层

- 返水：T 族（待 P-1）；过渡期 A 族须剔除对冲注。
- CRM：套 RG 防火墙；bandit 仅离线沙盒 + OPE，reward 仅保护性。
- 支付：自适应行为分析 + 钱骡链实体解析；**禁取消提款挽留**。
- RG：限额、冷静期、现实检查（reality check）入口常驻；「连输 N 局」类触发只能导向保护动作，**不得导向促销**。

### 11.6 决策层

ARCH-L3~L5 + `registry_risk_typology/topology` + 案件管理 + 人工复核/申诉/回滚 + 结果账本 + 因果评估。

### 11.7 AI 荷官（独立试点）

仅测试线；RNG 产品路径；Art. 50 披露；音频脏化与口型同步 SLO（渲染延迟 <2s 为下限）。

### 11.8 自评基线（B-12 / P-6）

若完美真人即 WM Casino / WM Perfect Group，则名册 #12（亚洲系中之 WM）移出竞争者，改为**自评基线**：以内部一手资料替换 UNKNOWN，并把 a168 之已知缺口（P-1 经济锚、标签回流、L0–L2 不可验、X-20 身份漂移）列为自评第一页。

---

## §12 Cheatsheet · 速查卡

```text
【三铁律】① AI 不进结果（百家乐/体育/彩券） ② reward 仅保护性（禁 GGR/NGR/入金/投注额/时长/回流/返水转化/留存）③ RG↔营销 格/物理隔离
【证据】OBSERVED[P0/P1] · INFERRED[P2] · UNKNOWN[P3]（≠未使用）· CONDITIONAL；重复不升级；签约≠交割；同源多转述≠多源
【价值】止损=确认避免−误伤−审核−设施；增效=人日案件/时长/覆盖；合规=约束非权重，RG→营销泄漏=0
【禁入 KPI】月活·独立存款人·NGR·忠诚毛收入·Rebate ROI(ΔGGR) —— 可观测，不可记功、不可作 reward
【返水】T 族 theo 为默认（待 P-1）；A 族须剔对冲注，r_A>(e_B+e_P)/2≈1.15% 即刷水正期望；L 族仅固定·封顶·公示·不递增·RG 硬否决
【六件核心】PU+Snorkel · targets+OpenLineage · Sigma+MITRE · Splink · E-value+负对照 · ALCOA+ 与 IQ/OQ/PQ
【标签五件】PU · Snorkel · 主动学习 · 蜜罐 Canary · 拒绝推断（价值高于其余之和）
【命名】ARCH-Ln / GDI-Ln / T·L·S 三轴，禁裸写 L3
【禁令】不连生产；不用 StarRocks/DolphinScheduler/Superset/SeaTunnel；不用驱动级/提权/常驻技术
【机器】OpenBLAS（参考 BLAS 慢一量级）· TinyTeX 或 use_tinytex:false · 磁盘余约 43 GB → 按日分区+预聚合 · CDG+Kaspersky+Defender 常驻
【EU AI Act】Art.5 禁止 2025-02-02 · Art.50 透明 2026-08-02 · Annex III 高风险 2027-12-02 · Annex I 2028-08-02（Reg 2026/1744）
【日期锚】Featurespace→Visa 完成 2024-12-19 · Snaitech→Flutter 完成 2025-04-30 · Optimove×Smartico 签约 2026-04-06（交割 UNKNOWN）· MGA Charter 2026-09-18 · SR 26-2 2026-04-17
【验收】PR-AUC+Brier+ECE+Precision@产能+Recall@误伤预算；walk-forward+purge+embargo；MASE/RMSSE/CRPS；禁只报 AUC、禁随机切分终证
【KillCritic 速记】操纵结果 · RG 营销 · 剥削型 reward · 黑箱封冻 · 只报 AUC · 路单保证未来 · 未授权测对手 · 生产数据外送 AI · 无回滚高影响 · P2/P3 写成官方 · 取消提款挽留 · AI 预测胜率宣传
```

---

## §13 本件之 redteam / critic / killcritic / blindspot（元层）

### 13.1 redteam（对本件）
- 本件 §11.3「牌靴承诺–揭示」为自提设计，无业界落地证据；若监管或设备不支持，属不可实施项。
- §9.3 阈值基于标准规则示意值，项目实际规则未知；越线判断须以 P-1 之闭式结果重算。
- §4E 大量消费站点条目出自单一 AI 转述之评测汇总，可能整批为 SEO 源。

### 13.2 critic
- 全球件 SEC/年报引用（Genius、Sportradar、Kambi、Playtech、Evolution）本轮未逐一抓原文，仅对其一处（全球件自身指纹）完成 R1；**其年报数字仍按 G 引标注**。
- EU AI Act 修订之日期来自多家律所一致转述，公报原文未抓取。

### 13.3 killcritic（任一被突破则本件作废 · v0.1.0 九条保留 + 本轮新增）
操纵结果 · RG 分数营销/返水/VIP/催存 · RL 对高风险客户探索促销 · 黑箱封冻无证据链 · AUC 高即上线 · 电商 CTR 目标用于会员推送 · 资安「默认封禁」用于正常会员 · 军工「无人值守交战」式高影响处置 · 以「航天级」为名上未验证复杂系统 · **路单/AI 保证未来结果之宣传** · **未经授权对竞争平台渗透、绕过、自动下注或漏洞利用**（竞争分析只做产品/服务/条款/合规层） · **生产数据未经批准送入外部 AI** · **把 P2/P3 写成「官方已部署」** · **取消提款挽留** · **净输返水分级递增或按 RG 个性化**。

### 13.4 blindspot（v0.1.0 五条保留 + 全球件九条并入 + 本轮新增）
- **B-1~B-5（保留）**：完美站赢不了有牌照有流动性的站；透明度过度反噬；EU AI Act/SR 26-2 合拢之墙；a168 重建管线本身即 B2B 产品；补全对手短板 = 六边形平庸。
- **B-6~B-10（全球件）**：标签治理（谁定义欺诈/串通/伤害）· 干预偏差（动作改变后续数据）· 跨产品同一自然人 · 法域政策矩阵 · 供应商模型如何独立验证。
- **B-11**：九家 AI 互为转述，形成「共识幻觉」——多家同说 ≠ 多源独立证据。
- **B-12**：**自评错位**——若完美真人即 WM，则所有白皮书把自己列为 UNKNOWN 的竞争者（P-6）。
- **B-13**：**Art. 5 禁止性条款**比「高风险」更早生效、更严，而所有前稿皆以高风险为最高档。
- **B-14**：**一锚两解**——P-1 同时卡住止损金额与最优返水设计，是整份白皮书的单点瓶颈。
- **B-15**：**源件持续增长**（X-12、X-13）——任何白皮书之「编依」若不带指纹，下一轮即失真。

---

## §14 Actionplan（v0.1.0 §9 全保留 + 全球件 Phase 0~4 并入 + 本轮新增）

### Phase 0（0–30 日）· 证据与治理先行（不连生产、不用禁令工具）

1. **P-1 裁定 house_edge**：向业务方取每桌型之规则表、抽水、免佣变体、边注付彩表 → 以组合枚举闭式计算（非估计）→ 一锚两解。
2. **P-5 / P-6 两项身份裁定**：注册表双对象；完美真人与 WM 之关系。
3. 实体/产品/法域登记册；统一数据字典 + 数据契约；统一风险分类（typology）；AI/模型清册；证据等级表与冲突台账（本件 §3）；RG/AML/Fraud/Marketing 数据权限矩阵；KPI 字典与分母定义（§1.3 准入/禁入）；SBOM 与模型卡模板。
4. **三项零成本机器修复（OpenBLAS + TinyTeX + CycloneDX SBOM）**：OpenBLAS（管理员单独立项）· TinyTeX 或 `use_tinytex: false` · `renv.lock` + `python-ds-requirements.lock.txt` → CycloneDX SBOM。
5. **Gate**：任一指标可答「谁、何时、什么数据、什么版本、什么分母」。

### Phase 1（30–90 日）· 离线基线与数据质量 —— 本机今天可跑（L3–L5，不连生产）

6. PU Learning + Snorkel + 拒绝推断（标签）。
7. **蜜罐桌台/蜜罐盘口/蜜罐票 + Canary token**（纸上设计 → 零假阳性金标签）。
8. `targets` 编排 + OpenLineage 血缘。
9. **registry 按 MITRE ATT&CK 三层重构**（战术—技术—程序）+ 规则迁 Sigma 进 Git 配 CI（阈值重标定）。
10. Splink（三档阈值）+ k-core / Leiden / TGN。
11. **元标签 + CPCV + PBO + Deflated SR**（⚠ 先以实测 `Var(ROI|n)` 校准，不用 `1/√n`）。
12. **负对照结局 + E-value** 对每条已锁发现做安慰剂检验与混杂量化。
13. IMM 状态估计（`stone-soup`）· TEWA 分配（`ortools`）。
14. ALCOA+ 宪章 + Part 11（L4）+ IQ/OQ/PQ + FMEA-RPN + `z3` 验不变量。
15. 合成数据（SDV）仅作架构压测，**绝不用于验证检测算法**。
16. **对打刷水审计**：以 §9.3 条件扫描现行返水口径是否计入对冲注。
17. **Gate**：泄漏测试 PASS · 对账 PASS · 可复现 PASS · 时间外胜基线 · 误伤预算明确。

### Phase 2（3–6 月）· 获授权测试线实时化

18. 事件总线、point-in-time 特征层、规则 + ML 排序、案件管理、理由码/SHAP、人工复核/申诉/回滚、SLO/背压/优雅降级、合成负载测试。
19. **Gate**：p99.9 达标 · 峰值不丢事件 · 模型故障自动退规则 · 规则故障退人工 · 高影响 100% 可审计。

### Phase 3（6–12 月）· 效果评估与三产品线

20. 百家乐：荷官/桌台/玩家/代理/支付/奖金/RG 分管线，风险拓扑与结果账本；**T 族返水上线（待 P-1）**；牌局黑匣子。
21. 体育：合法官方数据 / 赔率沙盒，定价–风险–诚信三层，不直接复用百家乐模型。
22. 彩券：票证/开奖/零售/PAM/钱包/CRM/RG 一体化原型。
23. **Gate**：所有干预有对照或合理准实验设计。

### Phase 4（12–24 月）· 受控智能决策

24. uplift / CATE；contextual bandit 离线 OPE；保护性动作集；小流量可停止。
25. AI 荷官 / 视觉 / **牌靴承诺–揭示（§11.3）** / 签名串流 独立试点，须监管沟通。
26. 独立模型验证、独立红队、合规签核（**P-7**）。
27. **禁止直接跳到自主 RL**。

### 平台侧（待禁令解除后提交公司）· 保留

PTP grandmaster（最高优先）→ Redpanda/Disruptor → Feast → Iceberg → JA4+/Bot 管理 → **数据二极管 RG/营销物理隔离** → HSM 审计签名；体育另加官方数据馈送冗余与挂起时延 SLA；彩券另加开奖形式化验证 + WORM。

### 三管线强制隔离（三垂直通用）· 沿用 v0.1.0

| 管线 | 目标函数 | 可自动化动作 | 绝对禁止 |
|---|---|---|---|
| 反诈 / 反串通 | 降低确认欺诈、红利滥用、团伙与技术利用损失 | 案件分流、加强验证、短时交易暂停、人工审核 | 依玩家输赢改变游戏结果 |
| AML / 资金完整性 | 降低可疑资金漏检与误报 | KYC 补件、SOW / SOF 工作流、可疑案件排队 | 无证据永久扣款或拒绝合法提款 |
| 责任博彩 | 降低可观察伤害、提高限额 / 冷静期采纳 | 提醒、限额入口、冷静期、人工关怀与升级 | **使用风险分数促销、返水、VIP 升级、催存** |

---

## §15 采购与技术尽调问卷（全球件 25 问采纳 + 百家乐专项 8 问新增）

**通用 25 问**：① rule / supervised ML / DL / bandit / RL？② 生产版本？③ 训练/验证时间窗？④ 标签来源（人工确认 / chargeback / KYC / 投诉 / 代理规则）？⑤ FP/FN 定义？⑥ 是否校准？⑦ OOT / rolling 验证？⑧ 模型卡？⑨ 可导出原始理由码与证据？⑩ 人工 override？⑪ override 是否回流？⑫ 高影响可申诉可回滚？⑬ 数据保存与驻留？⑭ 是否用客户数据训练跨客户模型？⑮ 第三方子处理者？⑯ 跨境机制？⑰ DR 之 RTO/RPO？⑱ p95/p99/p99.9？⑲ 吞吐与背压？⑳ 特征/模型故障如何降级？㉑ 监管与游戏认证？㉒ RNG/结果是否与 AI 表现层强制隔离？㉓ RG 数据能否技术上阻止流向营销？㉔ 审计日志是否不可变、已签名？㉕ 合约终止后模型、标签、案件证据能否完整导出？

**百家乐专项 8 问**：㉖ 每桌型规则表、抽水、免佣变体、边注付彩表是否可提供以闭式计算边际？㉗ 读牌是否双源（RFID/视觉）+ 荷官确认，不一致如何处置？㉘ 下注截止是否服务器权威时间、授时精度与漂移告警？㉙ round-level 事件（牌序、各节点时间戳）是否下放、以何授权分层？㉚ 每客户端串流延迟是否可观测？㉛ 视频分段是否签名、能否对抗盗播克隆？㉜ 返水口径属 A / T / L 何族，是否剔除对冲注？㉝ 边注状态依赖 EV 之监测能力与告警时延？

---

## §16 未决与须一手核实清单（v0.1.0 全保留，更新状态）

| 项 | 类型 | 须取得 | 状态 |
|---|---|---|---|
| `house_edge`（P-1） | 经济锚 | 业务方规则表 → 闭式计算 | 未解 |
| M-2 ARC 26↔30 | 数字 | 附时点并列 | 未解 |
| M-3 BetBuddy 15↔17 辖区 | 数字 | 一手 | 未解（28 品牌为另一口径） |
| M-4 / X-5 Smartico | 事件 | 交割公告 | **签约已核；交割未见** |
| X-4 Mindway 900万↔1,470万 / 归属 | 数字+归属 | 一手 | 未解 |
| Brightstar 终极控股 | 归属 | SEC/一手 | 未解 |
| 体育/彩券 AI 宣称 | 等级 | 模型卡/基准/审计 | 部分由 20-F/年报提升（G 引，原文待抓） |
| **X-20 typology/topology（P-5）** | 身份 | 权威 SQL 总包 | **新增** |
| **完美真人 = WM？（P-6）** | 身份 | 用户确认 | **新增** |
| **EU AI Act 公报原文**（Reg 2026/1744；Annex III 金融欺诈除外条） | 法条 | EUR-Lex | **新增** |
| **澳门第 16/2022 号法律输赢分成条** | 法条 | 法条原文 | **新增** |
| **SR 26-2 原文** | 法规 | 联储官网 | 新增（G 引） |
| **Evolution「约 2,000 张桌」、Playtech「28 品牌」、Kambi「48%」、SOFTSWISS 2025** | 年报数字 | 年报原文 | 新增（G 引） |
| **Angel Group 部署范围** | 分母 | 一手 | 新增（X-17） |
| 所有「止损金额 / 年损」 | 经济量化 | 自家一手（依赖 P-1） | 未解 |
| **独立 R4 复核（P-7）** | 治理 | 独立实例 | **新增** |

---

## §17 一句话收束

> **三垂直同数学，异结果与异护城河：百家乐拼受规×本地化，体育拼官方数据×定价，彩券拼特许×开奖公信力。**（v0.1.0 原句）
> **强化**：百家乐再加「× 公信」——受规 × 本地化 × 可验证公信（§11.3）。
> **止损靠标签，增效靠编排，合规靠血统；架构一套底座 + 三套 L4 域模型，别追纳秒，别追全栈，追那三层你今天就能动的。**（v0.1.0 原句）
> **止损靠标签，增效靠编排，合规靠血统；返水靠 theo，公信靠承诺。**
> **一锚（house_edge）两解（止损金额 · 最优返水）——先解锚，再谈白皮书转正。**

六件核心（PU+Snorkel / `targets`+OpenLineage / Sigma+MITRE / Splink / E-value+负对照 / ALCOA+ 与 IQ/OQ/PQ）今日可在现有环境、不连生产开始；其余为放大器，提前上只放大噪声。

---

## §18 变更历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1.0 DRAFT | 2026-09-27 | 初稿。移植总表为骨架；携 M-1~M-11 / SC-A~C / X-1~X-9；新建体育、彩券两垂直；剔除禁令工具。 |
| v0.2.0 DRAFT | 2026-09-28 | 严格超集合流。九件输入件指纹与血统（§0.4~0.6）；新增 X-10~X-20、SC-D~SC-I、一手核实四项（Smartico、Featurespace、EU AI Act 数字综合法、Snaitech）；名册自足化并扩至 72 编号 + 跨行业对标；ARCH/GDI/红队三套 L 对照；注册表双对象解；**返水科学裁定（A/T/L 三族、对打刷水阈值、一锚两解）**；竞争缺口→对策矩阵；完美真人蓝图（TMR 读牌、服务器权威截止、牌局黑匣子、牌靴承诺–揭示、签名串流、自评基线）；速查卡；本件元层四段；Phase 0~4 行动计划；尽调问卷 33 问；新增前置 P-5~P-7。**未定稿**——P-1~P-7 未解除前不得转正。 |

---

*Powered by Scibrokes® 世博量化® · 参考资料，不构成第四份权威文档 · DRAFT：未经全部一手核实与生产验证，不得对外定稿引用 · 竞争分析仅限产品、服务、条款与合规层，不含任何对他方系统之未授权测试。*
