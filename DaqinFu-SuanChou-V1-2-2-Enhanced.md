---
title: "《大秦赋算筹》"
subtitle: "v1.2.2 合并斧正版 · 斧正 D-15~D-18 强化" · 诸子百家量化科技 × GDI-OS × 礼逆袭（Linux）× 操作系统 × 云端服务器 × 半导体/存储 × AI算力 × 人工智能 × 强化学习 × 量化生态 × 脑机接口 × 国安/公安/国防/宇航科研生态 × 数据安全 × 密码学总纲"
author: "雷歐（Ryo Eng）"

date: 2026-09-30
date-format: "YYYY[年]M[月]D[日]"
# 斧正 D-4：原农历标注「丙午马年八月十九，丁酉月・丙午日」未经独立历法核实，
#          已自 date-format 移出，改列 §0.4 待核清单 U-11。丙午年（2026）本身正确。

lang: zh-CN

format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 3
    toc-location: left
    number-sections: true
    embed-resources: true
    page-layout: full
    code-fold: true
    code-tools: true
    code-summary: "查看代碼"
  pdf:
    toc: true
execute:
  echo: true
  warning: false
  message: false

language:
  title-block-author-single: "作者"
  title-block-published: "发布于"
---


# 0. 签发说明：这是一份“总纲”，不是机械拼接

> **核心定位**：把《大秦赋》仓库中可验证的“算筹 / 统筹法 / 运筹学 / 礼逆袭（Linux） / 中文编程 / 云端服务器 / 系统工程”技术血统，与当前完美真人百家乐、量化科技、人工智能、强化学习、安全治理、宇航/深地/量子研究资料，统一成一个**证据分级、可审计、可复现、可迁移、可逐步落地**的技术总纲。
>
> **安全边界**：当前仍执行“不连接/不实测 Superset、DolphinScheduler、StarRocks、生产博彩站点；不把生产原始数据提交外部 AI”的现行边界。允许离线、脱敏/模拟数据、代码/架构审查与正式授权测试线。
>
> **内容净化原则**：GitHub 仓库中与技术研究无关、含仇恨、歧视、暴力或针对现实群体/个人的政治化段落**不复制进本技术总纲**。这些内容不构成操作系统、量化、人工智能、科研或服务器工程证据；本件只登记“来源中存在非技术材料，已隔离”，不让其污染研究结论。

## 0.1 术语

- **礼逆袭（Linux）**：本件按用户约定，均指 Linux。
- **视窗（Windows）**：微软 Windows；服务器版单独写作 Windows Server。
- **云端服务器（Cloud Infrastructure / Cloud Platform）**：AWS、Microsoft Azure、Google Cloud 等不是“操作系统”；它们是 IaaS/PaaS/SaaS 平台，其虚拟机/容器节点通常运行 Windows 或 Linux。
- **算筹**：在本件中作为“统计、运筹、量化、优化、实验、治理与可计算决策体系”的总称；不把未经验证的玄学主张混入工程事实。
- **GDI-OS**：Gaming Decision Intelligence Operating System；是业务决策与治理“操作系统”的架构名，不是替代 Linux/Windows 的内核操作系统。
- **群联电子（Phison Electronics）**：台湾 NAND 控制芯片、SSD 与存储解决方案厂商；本件同时登记其 2026 年 `Pascari aiDAPTIV™`、AI Data Platform 与 HCI 路线，但性能/成本改善数字仍按厂商口径处理。
- **辉达 / 英伟达（NVIDIA）**：同一家公司之不同中文惯称；本件统一写作“辉达/英伟达（NVIDIA）”。
- **灵均投资**：用户原称“灵均资本”；公开官网主体为宁波灵均投资管理合伙企业（有限合伙），本件采用官网正名。
- **明汯投资**：用户原写“明竑”；公开官网主体为上海明汯投资管理有限公司，本件采用“汯”字。
- **Neuralink（脑机接口，Brain-Computer Interface, BCI）**：不是“Neurolink 神经网络”。本件将其列入神经科技/脑机接口产业链，和 TensorFlow/PyTorch 等神经网络软件框架分开。
- **凯盛娱乐 / 劲博 / 开云**：均先作为“用户给名的博彩/娱乐候选主体”进入身份解析登记册；若无法用牌照主体、公司注册号、官方域名三者闭环，不把同名站、代理站或镜像站的宣称升级为事实。

## 0.2 证据等级

| 等级 | 定义 | 本件使用规则 |
|---|---|---|
| P0 VERIFIED-REG | 法律、监管正文、SEC/法定申报、正式标准 | 可作制度硬基线 |
| P1 VERIFIED-FIRST-PARTY | 厂商年报、官方产品/文档、正式公告 | 可确认“存在/能力”，效果数字仍须看口径 |
| P2 OBSERVED-SECONDARY/PARTNER | 可信合作方、行业媒体、案例 | 可作趋势/采购线索 |
| P3 UNKNOWN/UNVERIFIED | 代理站、营销页、缺失来源、冲突资料 | 只保留主体，不填能力 |
| P4 ADVERSARIAL-CLAIM | 攻击者、玩家端预测器、优势玩法宣称 | 只用于防御威胁模型 |
| T1 THEORETICAL | 理论上可讨论、未工程验证 | 不进入 SLA / 采购能力 |
| S0 SPECULATIVE | 科幻、无可检验证据 | 只入前沿假说登记册 |


## 0.3 本件六元组自指约定（新增 · 斧正 D-5）

沿用 DRAFT v0.2.0 §0.1 之约定：**文件内不写本件自身 MD5 与字节数**，六元组以落盘实测、随交付回执给出，避免自指悖论。

父件（`_大秦赋算筹_.qmd`）之实测六元组已由本轮独立实例核验，登记于 §1.2。任何编辑（含空白、LF↔CRLF）均使指纹失效，须重签。本件：**LF · UTF-8 无 BOM · 末字节 `\n`**。

遇 MD5 不合，先查字节差是否等于行数（CRLF 二次保存征兆），再判版本冲突 —— 此为项目铁律，不得跳步。

## 0.4 证据双轴（斧正 D-10：原 §0.2 把两条正交轴压成一条阶梯）

**原 §0.2 的缺陷**：`P0…P4` 度量的是**来源权威性**，`T1 / S0` 度量的是**技术成熟度**。二者正交——一份 P1 官方文件完全可以描述一项 T1 理论工作（例：Caltech 官网说明虫洞动力学实验，来源 P1、成熟度 T1）。压成单一阶梯会诱导「P 级高 ⇒ 可落地」的错误推论。

自本版起拆为两轴，任一主张须同时标注 `P?·M?`：

### 轴一 · 来源权威（P 轴，沿用不变）

| 等级 | 定义 |
|---|---|
| P0 VERIFIED-REG | 法律、监管正文、SEC/法定申报、正式标准 |
| P1 VERIFIED-FIRST-PARTY | 厂商年报、官方产品/文档、正式公告、同行评议论文 |
| P2 OBSERVED-SECONDARY | 可信合作方、行业媒体、案例 |
| P3 UNKNOWN/UNVERIFIED | 代理站、营销页、缺失来源、冲突资料 |
| P4 ADVERSARIAL-CLAIM | 攻击者、玩家端预测器、优势玩法宣称 |

### 轴二 · 技术成熟度（M 轴，新增 · 六层，对应原 C-32）

| 等级 | 定义 | 可否进入采购/SLA |
|---|---|---|
| M5 规模化运行 | 已在生产规模长期运行 | ✅ |
| M4 工程示范 | 有可交付工程系统 | ✅ 附条件 |
| M3 原理样机 | 实验室或场地原型 | ⚠ 仅试点 |
| M2 实验观测 | 已发表可复现实验 | ❌ |
| M1 物理允许 | 理论上不违反已知物理 | ❌ |
| M0 数学存在 | 仅方程解存在 | ❌ |

> **闸门**：`M ≤ M2` 者一律不得写入采购能力、生产 SLA、商业承诺或工程交付期限。原 `T1 THEORETICAL ≈ M0/M1`、`S0 SPECULATIVE ≈ 无 M 级（不可证伪者不入轴）`。

**双轴示例**：
- 墨子号地面→卫星量子传态 = **P1·M2**（Nature 论文；已实验观测，非工程部署）
- INTEGRITY-178B 用于 F-35 = **P1·M5**（厂商公告；已规模化运行）
- 可穿越虫洞 = **P1·M0**（官方文献讨论；仅数学解）
- 外星地下科研院 = **不入轴**（无可证伪命题）


### 轴三 · 本机实证（LO 轴，v1.2.0 新增）

P 轴解决「外部来源有多权威」，M 轴解决「技术成熟到哪一步」；但本机测速、PowerShell、证书库、进程/服务状态属于**用户设备的一手实证**，既不是外部 P1，也不能硬塞进 M 轴。自 v1.2.0 起增设 `LO`（Local Observation）标签：

| 等级 | 定义 | 典型证据 | 可支持的结论 |
|---|---|---|---|
| **LO1 单次观测** | 一张截图、一次命令、一次测速 | Speedtest 单次结果、`Get-MpComputerStatus` | 证明「当时观察到」；**不作因果** |
| **LO2 受控重复** | 固定服务器/网络/顺序后 ≥5 组交错 A/B | Browser↔App、Chrome↔Edge | 可支持稳定差异与效应量 |
| **LO3 仪器化追踪** | ETW/WFP/ProcMon/证书链/进程 CPU/网络 trace 与重复实验一致 | 过滤驱动、TLS issuer、进程耗时 | 可进入根因归因候选 |

> **闸门**：`LO1 ≠ causality`。根证书存在 ≠ 当前每条 HTTPS 都被解密；安全软件注册 ≠ 两套完整实时引擎正在扫描同一对象；无显式 Proxy ≠ 无透明过滤/WFP/NDIS/VPN。只有 `LO2 + LO3` 与机制证据同向时，才可把「相关」升级为「高可信根因」。

## 0.5 已知偏离登记（新增 · 斧正 D-14）

项目呈现纪律要求「图表必须可交互（ECharts / Plotly / DT），禁止静态图」。本件全篇采用 ```` ```text ```` ASCII 框图与 Markdown 表格，**构成已知偏离**。

| 偏离 | 理由 | 补偿 | 复审 |
|---|---|---|---|
| 架构图用 ASCII 而非交互图 | 纯文本在 `.qmd` 中零依赖、可 diff、可复现、指纹稳定；交互图引入运行时依赖会破坏六元组稳定性 | 表格数据侧保留 `kable`/`gt`/`DT` 通道，架构图不承载数据 | 落盘为 HTML 交付物时复审 |
| 未用 Mermaid | Mermaid 渲染为静态 SVG，既不交互又引入依赖，两头不讨好 | 同上 | — |

**偏离经登记后成立；未登记的偏离一律视为违规。**

---


## 0.6 标准框架锚（新增 · v1.2.2 · 全件此前缺失）

> **缺陷**：本件在 §10 谈零信任、KMS/HSM、PQC，在 §30 谈终身身份，却**无一处集中登记所适用的规范性标准**。全件仅两处提及 EU AI Act，`ISO/IEC 42001` 零处，`eIDAS` 零处。按项目铁律「一切分析默认采用最严之适用国际标准；多标准并存时取最严者」，须立此锚。

### 0.6.1 三层永久区分（不得混谈）

| 层 | 定义 | 例 |
|---|---|---|
| **① 规范性标准** | ISO/IEC、法规、监管正文 | ISO/IEC 42001 · EU AI Act · **eIDAS 2.0** · NIST SP 800-63 |
| **② 最佳专业实务** | 顶尖银行、量化基金、研究机构 | DoD CAC/PKI 运作规程 · Renaissance 冗余纪律 |
| **③ 项目内部铁律** | 经核实后内部采纳 | 六元组指纹 · 三族铁律 · 出口闸 |

**自定规则永不得冒充国际标准。** 标准本身亦受红队审查，无标准豁免。

### 0.6.2 适用标准清单（按域）

| 域 | 标准 | 状态 |
|---|---|---|
| AI 管理体系 | **ISO/IEC 42001** | 现行 |
| AI 监管 | **EU AI Act** | 分阶段生效 |
| **数字身份** | **Regulation (EU) 2024/1183（eIDAS 2.0）** | **2024-05-20 生效；成员国钱包 2026-12-24 法定上线** |
| 身份认证 | **NIST SP 800-63**（现行 800-63-4） | 现行 |
| 差分隐私 | **NIST SP 800-226** | 2025-03-06 正式发布 |
| 数据质量 | ISO/IEC 25012 · ISO/IEC 5259 · ISO 8000 | 现行 |
| 风险管理 | ISO 31000:2018 · **NIST AI RMF**（Govern–Map–Measure–Manage） | 现行 |
| 模型风险 | **SR 26-2**（取代 SR 11-7） | 现行 |
| 风险数据聚合 | BCBS 239 | 现行 |
| 信息安全 | ISO/IEC 27001 · ISO/IEC 27701 | 现行 |
| 航电安全关键 | DO-178C · **ARINC 653** | 现行 |
| 原则 | OECD AI Principles | 现行 |


### 0.6.4 本次 v1.2.2 -> v1.2.2 强化补丁（D-15~D-18）

| 补丁 | 内容 | 等级 |
|---|---|---|
| D-15 | 标题与副标题版本不一致已修正：文件名为 v1_2_2，标题原写 v1.2.1，现统一为 v1.2.2 | P0 |
| D-16 | §4.2 版本锚 13 项复核结论回填：macOS 26 Tahoe 已由 Golden Gate 接替，OpenBSD 7.8 落后 7.9，Ubuntu 升点至 26.04.1，FreeBSD 主线切 15.1 | P1·M5 |
| D-17 | C-DAQIN-14 撞号已登记，C-DAQIN-33 为 U-12 复核完成正本，14 保留为 LO1 Speedtest 差异 | P0 |
| D-18 | 新增 §0.7 三白皮书血统链：V3.0.0 -> V3.1.0 (1,072行) -> 本件，v0_2_0_DRAFT -> v0_3_0_DRAFT (855行) -> 本件，禁止退化映射表已补 §1.4 | P0 |


### 0.6.3 ⚠ 时效告警：eIDAS 2.0 距法定期限 **85 天**

Regulation (EU) 2024/1183 第 5a 条要求 **27 个成员国于 2026-12-24 前各提供至少一个认证的 EUDI 钱包**；受规管私营方（含**电信**、银行、金融、交通、能源、医疗、数字基建及超大型平台）须于相关实施法案后 36 个月内接受。

**须标注三点，避免把政策目标当已部署：**
1. 2026-12-24 是**通报期限**（至少一个钱包获认证、列册、可用），**非全欧功能互通期限**
2. **法人钱包**是该法对商业身份验证最关键的部分，**也是最不可能于该日广泛可用者**
3. 丹麦 AltID 预定 2026 春季上线，但首发为**年龄验证优先**，完整身份功能延后

> **挂日历闸**：2026-12-24 后强制复核 27 国实际达成率（**U-26**）。

---

---

# 1. 本轮源件审计：当前文件已经发生版本漂移

以下是**本轮实际挂载文件**的字节级指纹，不沿用旧稿自报值：

| 文件 | 行数（LF） | 字节 | MD5 | 换行 | UTF-8 BOM |
|---|---:|---:|---|---|---|
| `Inteligent_egaming_platform_ref_v000.000.001(1).qmd` | 22,718 | 1,198,233 | `671438d8cd5165c72930841bde6c0d41` | LF=22,718 / CR=0 | 无 |
| `電腦已昇級至視窗11版（工欲善其事必先利其器）(1).qmd` | 11,627 | 504,093 | `41cdec343b7f2ce0318f5a90c3828f12` | LF=11,627 / CR=0 | 无 |
| `Whitepaper-Perfect-Baccarat-AI-Quant-Governance-V3-1-0.md` | 1,072 | 77,922 | `abcf84c709780f49818684d66edaa487` | LF=1,072 / CR=0 | 无 |
| `在线博彩娱乐白皮书_完美真人百家乐_三价值统一架构_v0_3_0_DRAFT.md` | 855 | 83,241 | `d4f2555ac6cc5b0980a9362bb98f0f47` | LF=855 / CR=0 | 无 |
| `顶级在线百家乐平台_AI与跨行业量化科技_移植总表_v1_0_0.md` | 892 | 79,482 | `1f28a39616dfa9c1bbf0b9c2e49b3d98` | LF=892 / CR=0 | 无 |
| `perfect-baccarat-report.md` | 222 | 23,608 | `2df6994f6e2ddc9d1aa4e75d4600e18c` | LF=222 / CR=0 | 无 |
| `Baccarat-Ai-Automation-Report.md` | 111 | 17,647 | `d61d68b8b4fc3fdc959c8c3573deaf24` | LF=111 / CR=0 | 无 |

## 1.1 关键版本更正

### C-DAQIN-01：`Inteligent_egaming_platform_ref` 已明显新于 V3.1 登记快照

V3.1 内登记的旧快照是：

```text
15,934 行
817,632 bytes
MD5 5b504053...
```

而本轮实际文件是：

```text
22,718 行
1,198,233 bytes
MD5 671438d8cd5165c72930841bde6c0d41
```

因此 **V3.1 不能再被当作“已吞掉最新 Inteligent 全量内容”的最终证明**。本件已额外检查 15,935 行之后的新增区域。

### C-DAQIN-02：新增实质内容集中在提问十一～十三

新增内容主要包括：

1. 国家级 IT 的“自研—采购—集成—主权控制”模式；
2. AWS / Azure / Google Cloud / 阿里云 / 腾讯云 / Hetzner / Contabo 等服务器与云安全；
3. SpaceX / Tesla / OpenAI / Anthropic 等前沿企业的保密边界讨论；
4. Windows / Linux / RTOS / 航电与安全关键操作系统；
5. 台湾、英国、Renaissance Technologies 等组织模式；
6. 深地实验室、量子信息、月火地下空间与“理论—实验—工程”分层。

**提问十四～卅五在当前文件中仅为结构化空白模板，无实质答复；因此没有被遗漏的技术主张。**

### C-DAQIN-03：旧回答中的绝对化句子降级

例如“国家都外购”“公仆科学家不自研”“商用云等于国家系统”等说法均过强。当前采用：

> **任务方/政府掌握需求、数据、授权、认证、安全边界与最终责任；通用硬件、操作系统、云、数据库和中间件大量采购商业/开源产品；安全关键内核、任务软件、密码系统、验证规程与特种系统可以自研或共同研发。**

这比“全自研”或“全外购”的二分法更符合公开证据。


## 1.2 源基补登与本轮独立实测（新增 · 斧正 D-6）

**缺陷**：§1 表登记 7 件，较 DRAFT v0.2.0 §0.4 的 9 件**少 2 件**，且未登记本件父版血统。按「禁止退化」令，源基收窄即退化，须补。

### 1.2.1 补登：DRAFT v0.2.0 已登记而 §1 遗漏者

| # | 文件 | 行数 | 字节 | MD5 | 处置 |
|---|---|---:|---:|---|---|
| S-8 | `Aerospace_Ecosystem_Report.qmd` | 135 | 6,865 | `39d9e98172848c2a47402eee6bbd7217` | **本会话独立实例六元组 6/6 实测 PASS** |
| S-9 | `在线博彩娱乐白皮书…v0_2_0_DRAFT.md` | 730 | 76,206 | 未实测 | v0.3.0 之父版，血统链节点 |
| S-10 | `Whitepaper-…-V3-0-0.md` | 780 | 57,644 | 未实测 | V3.1 之父版，§26 正文实际来源 |

### 1.2.2 `Aerospace_Ecosystem_Report.qmd` 六元组实测（P1·M5）

| 元 | 登记值 | 实测值 | 判定 |
|---|---|---|---|
| 档名 | `Aerospace_Ecosystem_Report.qmd` | 同 | ✓ |
| 行数 | 135 | 135 | ✓ |
| 字节 | 6,865 | 6,865 | ✓ |
| MD5 | `39d9e98172848c2a47402eee6bbd7217` | 同 | ✓ |
| 换行 | CR=0 | CR=0 · LF=135 · CRLF=0 | ✓ |
| 编码 | UTF-8 无 BOM | 合法 · BOM=False · NUL=0 · 末字节 `\n` | ✓ |

**这是全语料首件六元组六项逐位吻合者。** 对照 `a168 SQL 总包 HF9e` 的 MD5 登记冲突（行数字节双吻合而摘要不合，至今未裁定），本件证明指纹纪律在 `.qmd` 侧有效。

### 1.2.3 该件须先解之两条内部矛盾（引入正本前的硬前置）

| ID | 矛盾 | 位置 |
|---|---|---|
| **AERO-01** | §一 判 DolphinScheduler「无公开证据·未进国际航天白名单」→ §五 却将 Dolphin 列为中国大陆宇航数据栈 | 42 行 vs 118 行 |
| **AERO-02** | §一/§四 判 StarRocks 不适合航天核心 → **§六.2 却称「现有 StarRocks+Superset+Airflow+Echarts 即标准答案，可直接与星河动力等合作」** | 41/96 行 vs 131 行 |

**AERO-02 为论证与建议反向**，根因是「技术适配性」与「商务可行性」两个立场混写未分层。**在解除前，该件仅可作附录级参考，不得并入正本**——否则矛盾随血统传播。

> 其余缺陷（§五「10 地」实为 6 行/9 国之三套计数并存、全件零证据分级、Sift 归属疑误植、`lang: zh-TW` 与简体正文不符、as-of 2026-07-30 与本件跨两月）另见 §1.3 C-DAQIN 增补。

## 1.3 C-DAQIN 增补（C-DAQIN-04 ～ C-DAQIN-42 · 编号单点发号处）

| ID | 待校正/待登记 | v1.1.0 当前口径 |
|---|---|---|
| **C-DAQIN-04** | §26 章名「继承的 **V3.1** 正文」 | **章名与正文版本不符。** 该章内嵌正文第二行即自称「白皮书 **v3.0.0**」，且 §1 表登记的 `V3-1-0.md` 为 1,072 行 / 77,922 字节，与内嵌文本量不符。已改章名为「继承之白皮书正文（v3.0.0 主体 + v3.1.0 增量层）」，**不删任何内容** |
| **C-DAQIN-05** | 顶层章号碰撞 | **实测：`# 1.` ～ `# 21.` 各出现 2 次，共 42 个标题碰撞。** 在 `number-sections: true` 下 Quarto 按位置重编号，全件交叉引用（「见 §21.5」等）必然错位。已将 §26 区间内 **72 个标题整体降一级并重编号为 `26.N[.M]`**，碰撞归零 |
| **C-DAQIN-06** | `lang: zh-TW` 而正文为简体 | 已改 `zh-CN`；标题块「發佈於」改「发布于」。**此缺陷在 `Aerospace_Ecosystem_Report.qmd` 同样存在，属系统性习惯问题，非偶发** |
| **C-DAQIN-07** | 农历日柱未核实 | 丙午年（2026）正确；「八月十九·丁酉月·丙午日」未经独立历法核实，已移出 `date-format`，列 U-11 |
| **C-DAQIN-08** | 证据等级单轴 | 拆为 P 轴（来源权威）× M 轴（技术成熟度），见 §0.4。原 `T1/S0` 保留并给出映射 |
| **C-DAQIN-09** | 源基较 DRAFT v0.2.0 收窄 2 件 | 已补登 S-8/S-9/S-10，见 §1.2 |
| **C-DAQIN-10** | `OGDIL` ↔ `GDI-OS` 命名分叉（**立 X-21**） | `OGDIL` 见于 `Aerospace_Ecosystem_Report.qmd` 三处（副标题 / §六 / 来源行）且**全件未展开全称**；本件与两份白皮书一律用 `GDI-OS`。**与 DRAFT 之 X-20（`registry_risk_typology` ↔ `topology`）完全同型，须与 P-5 同批裁定**，本件不越权改名 |
| **C-DAQIN-11** | **U-2「礼逆袭操作系统」原词 —— 结案** | 前轮登记为 `UNPARSEABLE`。§0.1 已给出约定：**礼逆袭 ≡ Linux**（用户自创音译）。故前轮之问「战斗机 OS 比礼逆袭高端」即「比 Linux 高端」，其答案已由 **C-17** 正确裁定为**类别错误**。**U-2 CLOSED** |
| **C-DAQIN-12** | §4.2 版本锚 | 表中 12 项版本/日期**本实例无法独立核实**（多项落在本实例可靠知识边界之后）。已加标注：**采购前须逐项回官方生命周期页复核**，不得据本表下单。已列 U-12 |
| **C-DAQIN-13** | 缺「不退化映射表」 | DRAFT v0.2.0 有 §0.6 逐章映射以自证不退化；本件吞并多件却无对应表，**无法自证未退化**。已补 §1.4 |
| **C-DAQIN-14** | 浏览器 Speedtest 与原生 App 单次实测差异未入账 | **已登记为 LO1**：Browser 183.33/199.59 Mbps、8 ms；Windows App 339.63/191.79 Mbps、6 ms。浏览器下载相对 App 低 **46.02%**；App 相对 Browser 高 **85.26%**。但截图只能确认两者均显示 MagtiCom/Tbilisi，**未确认完全相同的 Ookla server instance**，故不得直接归因安全软件 |
| **C-DAQIN-15** | Defender 状态此前只按「装有」描述 | 本轮 PowerShell 实测 `AMRunningMode=Normal`、`AntivirusEnabled=True`、`RealTimeProtectionEnabled=True`、`NISEnabled=True`、`IoavProtectionEnabled=True`。按 Microsoft 官方文档，`Normal` = Defender Antivirus **主动模式**；此为 LO1 + P1 机制证据 |
| **C-DAQIN-16** | Kaspersky 根证书与 HTTPS 解密能力易被偷换为「正在解密全部流量」 | 本机证书库实见 `Kaspersky Endpoint Security Personal Certification Authority` 两条；Kaspersky 官方文档证实 KES 可使用根证书解密/分析 TLS 1.0–1.3，并有「不扫描/按组件需要/始终扫描」三模式。**证书存在只证明能力与信任链，不能证明 speedtest.net 当次实际被 MITM** |
| **C-DAQIN-17** | 「无 Proxy = 无中间过滤」错误 | 本轮 `netsh winhttp show proxy` = 直接访问；用户代理 `ProxyEnable=0` 且 PAC 为空。只能排除**显式 WinHTTP/User Proxy/PAC**，不能排除 WFP/NDIS/透明网关/VPN/DLP/安全过滤驱动 |
| **C-DAQIN-18** | 把 Browser 183 Mbps 归因于「浏览器天然上限」 | Google Fiber/Ookla 指引称一般浏览器约在 **3 Gbps** 级才可能成为明显上限；本机 App 仅约 340 Mbps，远低于该量级。故「浏览器通用吞吐上限」**不能解释 46% 下载差**，须转查浏览器特定路径、扩展、安全扫描、协议/服务器选择与排队 |
| **C-DAQIN-19** | James Simons / Renaissance 保密史料过薄 | 已以 Simons Foundation、IDA、Renaissance 官方资料补强：Simons 1964 加入 IDA Communications Research Division，从事 code breaking/cryptographic problems；Simons Foundation 2024 进一步称其为 NSA code breaker。现今 IDA CCC 为 **NSA 赞助的 FFRDC**，研究 cryptology/cybersecurity/HPC；这**不等于 Renaissance 继承 NSA 内部系统** |
| **C-DAQIN-20** | 「Renaissance 是否天下第一保密」用单一总分容易伪精确 | 改为**公开证据覆盖评分**，明确它衡量「可公开核验程度」而非真实秘密能力。Renaissance 2026 官网已公开 Security Engineer 控制面（firewall/AV-EDR/IDS-IPS/encryption/vulnerability/IAM/governance/IR）及 >50,000 cores、>200 Gbps、40 TB/day、冗余设施；但内部密钥层次、PQC、零信任细节仍未公开，故不得裁定「天下第一」 |


### 1.3.2 C-DAQIN 增补（C-DAQIN-33 ～ C-DAQIN-36 · v1.2.1 合并斧正）

| ID | 发现 | v1.2.1 当前口径 |
|---|---|---|
| **C-DAQIN-33** | **U-12 §4.2 版本锚复核完成** | 13 项逐项回一手源复核：**8 PASS · 3 失准 · 2 硬错**。硬错：`macOS 26 Tahoe` 于 2026-09-14 已由 **macOS Golden Gate** 接替（早于原签发日 15 天）；`OpenBSD 7.8` 落后当前版 **7.9 / 2026-05-19** 逾四个月。失准：Ubuntu 未升点版（**26.04.1 / 2026-08-27**）、FreeBSD 角色误标（**15.1 / 2026-06-16** 才是主线，14.5 为维护分支）、SLES GA 日未证。**U-12 CLOSED；§4.2 自 P3 升 P1（8 项），禁止下单告警解除** |
| **C-DAQIN-34** | **C-DAQIN 编号跨分支撞号** | v1.1.1 已占用 `C-DAQIN-14`（内容＝U-12 复核完成）；v1.2.001 在另一分支独立把 `C-DAQIN-14` 指派给「Speedtest Browser/App 差异 LO1」。**同号两义**，违反「更正须公开登记、旧说不得静默改写」之铁律。**裁定**：v1.2.001 之指派因已公开发布而保留；U-12 复核改编为 **C-DAQIN-33**，并于此显式记载撞号事实，双方皆可追。**制度补丁**：C-DAQIN 编号自本版起由 §1.3 单点发号，分支合并前须先对号 |
| **C-DAQIN-35** | **v1.1.1 → v1.2.001 发生实质退化** | v1.2.001 以 **v1.1.0** 而非 v1.1.1 为基线合并，致 §4.2 的 U-12 复核成果整体丢失、两项硬错回归、日历闸缺失、§27.1 之 U-12 仍记「待核」。**已于本版全数回填。** 根因：合并未以 §1.4 不退化映射表逐节对账 |
| **C-DAQIN-36** | **主体身份锚缺位**（v1.1.2 增量） | 原 §10 只治**系统**身份（Zero Trust / KMS / HSM / PQC），未治**主体**身份。已补 §10.5。触发实例：用户自陈 GitHub 与多个中国公开账号无法登录，典型为「2FA 绑手机号 → 号码失效 → 恢复邮箱亦绑同号 → 全链断」。经查证，**真正终身制电话号码不存在**（见 §10.5.2） |

### 1.3.1 C-DAQIN 增补（C-DAQIN-21 ～ C-DAQIN-32 · v1.2.0 前沿生态强化）

| ID | 发现 | v1.2.0 强化口径 |
|---|---|---|
| **C-DAQIN-21** | `Phison` 未入主体图谱 | 正名为**群联电子（Phison Electronics）**；纳入半导体/存储与 AI 基础设施双分类。NAND 控制器/SSD 为成熟主业；`Pascari aiDAPTIV™`、AI Data Platform/HCI 为 2026 官方公开路线，厂商效果数字不自动视为独立实证 |
| **C-DAQIN-22** | “Neurolink 神经网络”概念混淆 | 更正为 **Neuralink（脑机接口，BCI）**。`N1 Implant + R1 Robot + user app` 属侵入式 BCI 临床研究；**不得与 neural network 软件框架混类** |
| **C-DAQIN-23** | “灵均资本”命名 | 官方公开主体为**灵均投资**；官网披露 100,000+ 数据种类、10PB+ 存储及量化选股/指数增强/多空多策略/市场中性。规模/效果仍以官方自报口径标记 |
| **C-DAQIN-24** | “明竑”命名 | 更正为**明汯投资**；官网公开数据挖掘、统计分析、AI/ML/DL 与量化资管路线，内部 alpha、训练数据与真实生产拓扑 **UNKNOWN** |
| **C-DAQIN-25** | 聚宽平台与聚宽投资易混淆 | 分开登记：**JoinQuant 聚宽量化研究平台**是研究/数据/回测平台；**聚宽投资**是私募管理机构（官网称 P1066435），不可将平台用户策略等同基金生产策略 |
| **C-DAQIN-26** | 幻方量化 / High-Flyer 与 DeepSeek 易被过度合并 | 幻方/High-Flyer 纳入量化机构；DeepSeek 纳入前沿 AI 实验室/模型生态。二者公开历史关联可登记，但**量化生产栈、模型训练栈与组织边界须分别取证** |
| **C-DAQIN-27** | AMD / NVIDIA 在旧稿只是零散出现 | 新增为独立“AI 算力与机密计算”类别：AMD `Instinct + ROCm + SEV-SNP`；NVIDIA `Hopper/Blackwell/Vera Rubin + CUDA + Confidential Computing` |
| **C-DAQIN-28** | Tesla 仅作汽车/AI主体名 | 加入 2026 官方投资者披露：`Cortex 2` 已上线训练工作负载，继续扩建现场 AI training infrastructure，并研发 `Dojo 3` 自研硅；**不据此猜测内部网络、密钥或服务器拓扑** |
| **C-DAQIN-29** | 礼逆袭只列发行版、缺开源治理组织 | 新增 Linux Foundation、kernel.org/Linux kernel 社群、CNCF、OpenSSF、Confidential Computing Consortium、OpenChain、PQCA、SPDX、FINOS、LF AI & Data、Yocto、Zephyr，并列 Apache/Eclipse/FSF/Debian/Fedora/OCI 等相邻治理组织 |
| **C-DAQIN-30** | 凯盛娱乐 / 劲博 / 开云身份污染风险 | 三者进入 `entity_resolution_status`。**凯盛娱乐：未唯一解析；劲博：可能指 JBO，但中文别名未闭环；开云体育：公开站点/镜像/同名品牌多，且须与奢侈品 Kering（开云集团）完全隔离。** 未解析前不写牌照、股东或“顶级”能力 |
| **C-DAQIN-31** | 国安/公安/国防/宇航主体混成一个“军工”篮子 | 拆为四链：①国家安全/密码/情报科研；②公安/公共安全/身份与取证；③国防科技/商业技术导入；④宇航/空间科学与高可靠计算。只收公开、防御性、科研与治理能力，不重建敏感作战拓扑 |
| **C-DAQIN-32** | “前沿科技公司”容易无限堆名词 | 新增供应链六层：`芯片/IP/制造 → 存储/网络 → 系统/服务器 → OS/云/容器 → 数据/AI/模型 → 安全/科研/应用`；每个主体必须有 `entity_type / evidence / maturity / transferable_pattern / non-transferable_boundary` |


### 1.3.3 C-DAQIN 增补（C-DAQIN-37 ～ C-DAQIN-42 · v1.2.2 实证强化）

| ID | 发现 | v1.2.2 当前口径 |
|---|---|---|
| **C-DAQIN-37** | **RNK「Phone for Life」实证** | 商业终身承诺的完整证伪案例。2004-11/12 推出（US$999 住宅版含电话号码、911/411、携号转入），2007 被 Wave2Wave 以 4,470 万美元收购，**2012-02-17 Chapter 11 → 2012-09-27 §363 资产售予 Signal Point → 2012-11-13 转 Chapter 7 清算，法人解散**。**存续 8 年；买单的客户活过了卖方。** 全时间线见 §10.5.5-E |
| **C-DAQIN-38** | **前版对 RNK 的归类错误** | 前版称其「不是号码」—— **错误**。该方案明确包含电话号码。正确的证伪理由是「**给了号码，但公司八年后被清算**」。登记 **SC-ζ / SC-η**，见 §29.6 |
| **C-DAQIN-39** | **标识符 ≠ 凭证** | EDIPI 公开印在 CAC 卡背面，ORCID 公开可查；认证靠 PKI 证书。**禁止把 L2 持久标识符当密码用。** 已列为 §10.5.3 第三条硬禁令 |
| **C-DAQIN-40** | **`member_id` ↔ EDIPI 同构** | EDIPI 的设计原则是「**多角色单标识**」：一人可同时为现役／文职／承包商／退休者／眷属，**角色变而标识不变**，角色细节由独立的 DBN 管理。**a168 的 `member_id` 扮演同一角色**——双管线 `q ⊆ e` 之所以成立，正因 `member_id` 是跨 IP、跨会话、跨链路的单一锚。此血统链此前未接上，补记 |
| **C-DAQIN-41** | **标准框架全件缺失** | 本件谈零信任、PQC、终身身份，却无集中的适用标准登记；`ISO/IEC 42001` 零处、`eIDAS` 零处。**已补 §0.6**，含三层永久区分与十二项标准清单 |
| **C-DAQIN-42** | **eIDAS 2.0 时效告警** | Regulation (EU) 2024/1183 第 5a 条要求 27 国于 **2026-12-24** 前各提供至少一个认证 EUDI 钱包，受规管私营方（含**电信**）须于实施法案后 36 个月内接受。**距今 85 天**，而本件合规叙事此前完全未涵盖。须标注：该日为**通报期限非互通期限**；**法人钱包最不可能按期广泛可用**。已挂日历闸（U-26） |

## 1.4 不退化映射表（新增 · 斧正 D-12）

| 来源件 | 在本件之位置 | 处置 |
|---|---|---|
| `Whitepaper-…-V3-0-0/V3-1-0` 正文 | **§26.0～§26.21**（原 §0～§21，整体降级重编号） | **全文保留，零删减**；仅改标题层级与编号 |
| `…v0_3_0_DRAFT.md` | §27 隔离登记 | 只吸收方法/待办/冲突登记；**DRAFT 状态不偷换为已验证** |
| `移植总表_v1_0_0.md` | §16 主体登记册（经 V3.x 继承） | 保留 |
| `Inteligent_egaming…qmd`（22,718 行新版） | §15 主体补录 + §1.1 C-DAQIN-01/02 | 15,935 行后新增区已检 |
| `電腦已昇級至視窗11版…qmd` | §4～§7、§23～§24 | 工程纪律已吸收 |
| `Aerospace_Ecosystem_Report.qmd` | **§1.2 补登（附录级）** | **因 AERO-01/02 内部矛盾未解，暂不并入正本** |
| `perfect-baccarat-report.md` / `Baccarat-Ai-Automation-Report.md` | 经 DRAFT 之 X-1/X-2 污染台账继承 | 污染台账保留 |

**自证条款**：本次斧正仅执行「**改层级、改编号、改元数据、增章节**」四类操作，**未删除任何原有段落、表格、条目或来源链接**。原件应改名加 `_superseded` 后缀保留，不删除。

---

# 2. GitHub《大秦赋算筹》技术血统：以仓库实物为准

仓库 `engryochan/zhongkehongqi` 默认分支为 `世博量化研究院`。本轮树检索**没有发现一个现成、单独命名为 `《大秦赋算筹》.qmd` 的源文件**；相关技术资产分散在：

- `README.md`
- `国学论.qmd`
- `大秦宫.qmd`
- `统筹法 - 系统工程学.Rmd`
- `运筹帷幄 - 阿里.Rmd`
- `秦谏.qmd`
- `中科红旗∙兵工厂/`
- `云端服务器/`
- `内核/`
- `华罗庚/`
- `秦人操作系统与电子仪器/`
- `礼逆袭应用仓库/`

因此本件正式把这些技术血统收束成“《大秦赋算筹》”。

## 2.1 可保留的技术母题

| 仓库母题 | 本件斧正后的工程含义 |
|---|---|
| 华罗庚统筹法 / 优选法 | 运筹学（Operations Research）、网络计划、约束优化、资源配置、实验设计 |
| 高频量化 / 对冲 | 时间序列、风险度量、执行成本、回测纪律、概率决策 |
| R 鄀统计编程 | 统计建模、可复现报告、Shiny、因果/生存/贝叶斯 |
| 中文编程 | 中文文档、术语治理、DSL/注释/界面本地化；代码标识保持行业标准 |
| 中科红旗 / 礼逆袭 | Linux 内核、发行版、服务器、开源供应链、国产/主权计算 |
| 内核/ISO/编译 | OS 构建、内核配置、软件供应链、镜像与可复现环境 |
| 云端服务器/Kubernetes | 云原生、容器编排、弹性计算、基础设施即代码 |
| 系统工程 | 架构分层、可靠性、冗余、故障隔离、回放、治理 |
| 算筹 | 把统计、运筹、优化、仿真、因果、AI、治理统一为“可计算决策” |

## 2.2 不应继续混写的内容

- 历史文化叙事 ≠ 技术事实；
- 政治口号 ≠ 科研证据；
- 玄学/占卜 ≠ 已验证统计方法；
- 国防/宇航类比 ≠ 博彩行业监管要求；
- 科幻概念 ≠ 可采购工程能力；
- 某厂商“产品存在” ≠ 模型有效；
- 某政府“允许使用某云” ≠ 所有机密系统都运行在该云。

---

# 3. 《大秦赋算筹》统一技术总架构

```text
L0  证据与来源
    official docs | regulations | papers | source files | hashes
      ↓
L1  计算底座
    Windows / Linux / BSD / macOS / RTOS / Cloud / Bare Metal / HPC
      ↓
L2  安全与密码
    IAM | Zero Trust | KMS/HSM | TLS/mTLS | disk encryption | PQC | SBOM
      ↓
L3  数据真相
    canonical events | point-in-time | contracts | lineage | DQ | replay
      ↓
L4  算筹方法
    statistics | OR | Bayesian | survival | HMM/state-space | graph | causal
      ↓
L5  AI/ML
    GLM → GBDT → graph/sequence → Transformer → constrained bandit/RL
      ↓
L6  决策治理
    eligibility | policy veto | uncertainty | human review | appeal | rollback
      ↓
L7  业务价值
    止损 | 增效 | 合规
      ↓
L8  验证
    IQ | OQ | PQ | MQ | shadow | OOT | stress | independent review
```

---

# 4. 操作系统全景：先纠正“云 = OS”的类别错误

AWS、Azure、Google Cloud 属于云平台；它们可提供 Windows Server、RHEL、Ubuntu、Debian、SUSE、Oracle Linux、Amazon Linux 等镜像，也有自有容器/宿主系统。真正要比较“操作系统”，应拆成下列家族。

## 4.1 主流操作系统家族总表

| 家族 | 代表 | 核心优势 | 核心局限 | 最合适场景 |
|---|---|---|---|---|
| Windows 桌面 | Windows 11 | 商业软件/硬件兼容极强、Office/AD/企业生态、游戏/桌面应用强 | 许可证、遥测/策略复杂、服务器化不如 Linux 轻量 | 办公、开发工作站、企业终端 |
| Windows Server | Windows Server 2025 | AD DS、Group Policy、Windows 身份域、Hyper-V、.NET/SQL Server 生态 | 许可证成本、更新/重启与资源开销、自动化习惯与 Linux 不同 | Microsoft-heavy 企业、域控、文件/应用服务器 |
| macOS | macOS 26 Tahoe | Apple Silicon 能效、Unix 基础、开发体验、iOS/macOS 构建链 | 硬件绑定、无现代通用服务器产品、数据中心生态有限 | 创作、移动应用开发、个人科研工作站 |
| 礼逆袭（Linux）企业版 | RHEL、SLES、Ubuntu Pro | 服务器/HPC/云/容器事实标准、自动化强、开源、可审计 | 需 Linux 运维能力；不同发行版生命周期与软件版本差异大 | 云、数据库、AI、HPC、企业服务器 |
| 礼逆袭社区稳定版 | Debian、Ubuntu LTS、Rocky、Alma | 成本低、社区大、可复现、云镜像丰富 | 商业支持依发行版而异 | 科研、通用服务器、开发 |
| 礼逆袭滚动/前沿 | Fedora、Arch、Tumbleweed、Gentoo | 新内核/新编译器/新硬件支持快 | 变动快，不适合未经验证直接放核心生产 | 开发、测试、前沿硬件 |
| BSD | FreeBSD、OpenBSD、NetBSD | 网络栈、ZFS/系统一致性、安全文化 | 软件/驱动生态较 Linux 小 | 网络、安全、存储、专用服务 |
| 商用 UNIX | IBM AIX、Oracle Solaris、HP-UX | 大型机/关键业务成熟、长期稳定 | 昂贵、生态收缩、厂商锁定 | 遗留金融/电信/大型企业 |
| 大型机 OS | z/OS、IBM i | 极高事务一致性、可靠性、审计、批处理能力 | 成本和技能门槛高 | 银行、保险、政府大型核心系统 |
| 移动 OS | Android、iOS/iPadOS | 移动生态、沙箱、安全启动 | 不适合作通用服务器 | 手机/平板/边缘终端 |
| ChromeOS | ChromeOS / ChromeOS Flex | 管理简单、零接触部署、浏览器/云优先 | 专业本地软件生态有限 | 教育、轻办公、受管终端 |
| 安全关键 RTOS | INTEGRITY-178、VxWorks 653、LynxOS-178、QNX、RTEMS | 硬实时、确定性、时空隔离、认证 | 开发/认证昂贵、生态专用 | 航电、铁路、工业、宇航 |
| MCU/嵌入式 RTOS | FreeRTOS、Zephyr | 小型、实时、IoT 生态 | 非通用服务器 | 传感器、IoT、嵌入式 |

## 4.2 当前主流版本锚（U-12 复核完成 · 复核日 2026-09-29 · 沿用至 2026-09-30）

> **⚠ 退化回填告警（R-1）**：v1.2.001 的本节为 **v1.1.0 旧表**，v1.1.1 已完成的 U-12 逐项复核成果在合并中**整体丢失**，两项硬错（macOS、OpenBSD）随之回归。本版已回填，并登记为 **C-DAQIN-35**。
>
> **本节状态：P3 → P1（8 项）。** 已逐项回官方生命周期页与一手发布公告复核。
>
> **复核结论：13 项中 8 项 PASS · 3 项失准 · 2 项硬错。**

### 4.2.1 U-12 复核结果总表

| # | 系统 | 原登记（v1.1.0 / v1.2.001） | 复核实测 | 判定 | 等级 |
|---|---|---|---|---|---|
| 1 | Windows 11 | 26H1 / 25H2 / 24H2 为现行服务频道 | 26H1 GA 2026-02-10（build 28000），最新 28000.3086 / 2026-09-22；25H2 build 26200.9445；**26H2（build 26300）已在 Release Preview** | ⚠ **即将变动** | P1·M5 |
| 2 | Windows 11 26H1 性质 | 非常规就地升级 | 微软明文：**仅随 Snapdragon X2 等新硅设备出厂，不经 Windows Update 提供，且无法升至 2026 下半年年度功能更新**（核心平台 Bromine ≠ Germanium） | ✅ **PASS** | P0·M5 |
| 3 | Windows Server | Windows Server 2025 | 现行第十四版；最新 24H2 build 10.0.26100.33296 / 2026-08-11 | ✅ **PASS** | P1·M5 |
| 4 | **macOS** | **macOS 26 Tahoe**，2025-09 发布 | **Tahoe GA 2025-09-15，末版 26.7 / 2026-09-14；同日已由 macOS Golden Gate 接替** | ❌ **FAIL — 已非当前版** | — |
| 5 | RHEL | 10.2 文档现行 | **RHEL 10.2 / 2026-05-20**（9.8 同日；8.10 / 2024-05-22） | ✅ **PASS**（补日期） | P1·M5 |
| 6 | Ubuntu | 26.04 LTS，2026-04-23 | 26.04 LTS "Resolute Raccoon" 2026-04 发布；**当前点版为 26.04.1 LTS / 2026-08-27**；标准维护至 2031-05 | ⚠ **须升点版** | P1·M5 |
| 7 | Debian | **13.7 "trixie"，2026-09-12** | **13.7 "Trixie" / 2026-09-12** | ✅ **PASS 逐位吻合** | P1·M5 |
| 8 | Fedora | **44，2026-04-28** | **Fedora Linux 44 / 2026-04-28**；**Fedora 45 Beta 已于 2026-09 释出** | ✅ **PASS**（45 在途） | P1·M5 |
| 9 | SLES | 16.0，2025-11 GA | 16.0 为现行受支持版（NVIDIA 数据中心驱动验证矩阵列 SLES 16 / 16.0）；**GA 日期未取得一手证** | ⚠ **部分** | P2·M5 |
| 10 | Oracle Linux | 10.2 文档现行 | **10.2 现行**（`relnotes10.2` 在线）；OCI 镜像 `Oracle-Linux-10.2-aarch64-2026.08.14-0` | ✅ **PASS** | P1·M5 |
| 11 | Rocky Linux | **10.2，2026-05-29** | **10.2 GA**：官网新闻稿署 2026-05-28，官方发行文档登记 **2026-05-29**，内核 6.12.0-211.16.1，RHEL 基线 2026-05-19（延迟 9 天） | ✅ **PASS** | P1·M5 |
| 12 | FreeBSD | 14.5，2026-09-08 | **14.5 / 2026-09-08 属实**，**但 15.1 / 2026-06-16 才是当前主线**；14.x 为维护分支 | ⚠ **角色误标** | P1·M5 |
| 13 | **OpenBSD** | **7.8，2025-10-22** | 7.8 日期属实（安全支持至 2026-11-01），**但当前版为 7.9 / 2026-05-19（第 60 版）**，含 OpenSSH 10.3、LibreSSL 4.3.0 | ❌ **FAIL — 落后一版** | — |

### 4.2.2 斧正后之版本锚（可用于采购）

| 系统 | **当前版本** | 日期 | 备注 |
|---|---|---|---|
| Windows 11 | 26H1 / 25H2 / 24H2（GA 频道） | 26H1: 2026-02-10 | **26H2 在 Release Preview，下单前须确认频道** |
| Windows Server | 2025 | build 26100.33296 / 2026-08-11 | — |
| **macOS** | **Golden Gate（27）** | **2026-09-14** | **Tahoe（26）已退居前代；末版 26.7** |
| RHEL | 10.2 | 2026-05-20 | 9.8 同日 |
| Ubuntu | **26.04.1 LTS** | **2026-08-27** | 维护至 2031-05；24.04.5 LTS 亦在支持内 |
| Debian | 13.7 "Trixie" | 2026-09-12 | 支持至 2030 |
| Fedora | 44 | 2026-04-28 | 45 Beta 在途 |
| SLES | 16.0 | GA 日待证 | — |
| Oracle Linux | 10.2 | 镜像 2026-08-14 | — |
| Rocky Linux | 10.2 | 2026-05-29 | EOL 2035-05-31 |
| **FreeBSD** | **15.1（主线）** | **2026-06-16** | 14.5 / 2026-09-08 为 14.x 维护分支 |
| **OpenBSD** | **7.9** | **2026-05-19** | 第 60 版；7.8 安全支持至 2026-11-01 |

### 4.2.3 复核所依一手源

| 系统 | 源 |
|---|---|
| Windows 11 | `learn.microsoft.com/windows/release-health/windows11-release-information` · `.../status-windows-11-26h1` · Windows IT Pro Blog |
| macOS | Wikipedia `MacOS_Tahoe`（载 Golden Gate 接替日 2026-09-14） |
| RHEL | Wikipedia `Red_Hat_Enterprise_Linux` 发行表 |
| Ubuntu / Debian / Fedora | Wikipedia `Ubuntu` / `Debian`；Fedora 44 官方发布记录 2026-04-28 |
| Rocky | `rockylinux.org/news/rocky-linux-10-2-ga-release` · `docs.rockylinux.org/10/releases/` |
| Oracle Linux | `docs.oracle.com/iaas/images/oracle-linux-10x/...` |
| FreeBSD | Wikipedia `FreeBSD`（15.1 / 2026-06-16；14.5 / 2026-09-08） |
| OpenBSD | `openbsd.org` 首页 · `endoflife.date/openbsd` |

### 4.2.4 日历闸（制度补丁 · 防复发）

两项硬错的共同特征是**发布节奏固定而文档无复核触发器**：

| 窗口 | 涉及 | 触发后动作 |
|---|---|---|
| **每年 4 月下旬** | Ubuntu LTS/interim · Fedora | 复核 §4.2.2 |
| **每年 5 月中** | RHEL · Rocky · SLES · OpenBSD | 同上 |
| **每年 9 月中** | **macOS**（苹果年度大版）· Debian 点版 | 同上 |
| **每年 10 月下旬** | **OpenBSD**（半年周期第二档）· Fedora | 同上 |

> 与 §26.12.2 之 T_true 预检法同型：**把一次性核查固化为可复用的常驻探针**，不依赖人工记起。

---

# 5. 礼逆袭（Linux）发行版：以家族与生产用途实现“实务全覆盖”

全球活跃/历史 Linux 衍生版有数百种；逐个罗列所有短命 fork 并无工程价值。本件采用**家族级完整 + 生产相关长名单**。

## 5.1 企业与服务器主线

| 发行版 | 家族/治理 | 优势 | 局限 |
|---|---|---|---|
| Red Hat Enterprise Linux (RHEL) | Red Hat / Fedora 系 | 10 年级生命周期、SELinux、认证生态、Satellite/Ansible、混合云、FIPS/PQC 路线 | 订阅成本；包较保守 |
| CentOS Stream | RHEL 上游流 | 最接近未来 RHEL、开发/兼容验证好 | 不是传统“RHEL 免费克隆” |
| Rocky Linux | RHEL 兼容 | 社区/企业兼容、HPC 常见 | 与上游节奏绑定 |
| AlmaLinux | RHEL 兼容 | 社区治理、云镜像丰富 | 与 RHEL ABI/生态关系需持续跟踪 |
| Oracle Linux | RHEL 系 + UEK | Oracle DB/SAP/Oracle Cloud 强、可选 UEK | Oracle 生态偏重 |
| SUSE Linux Enterprise Server | SUSE | SAP/HANA、HA、欧洲企业市场、管理工具 | 生态规模小于 RHEL/Ubuntu |
| Ubuntu Server / Ubuntu Pro | Debian 系 | 云镜像最多之一、开发者生态、K8s/AI 友好、LTS/ESM | 企业治理/包版本策略与 RHEL 不同 |
| Debian | Debian | 极稳、自由、架构广、云/HPC 可靠 | 单一商业厂商支持不是默认 |
| Amazon Linux | AWS | 与 EC2/AWS 集成、镜像优化 | AWS 倾向明显 |
| Azure Linux | Microsoft | 微软云/容器场景精简 | 通用桌面/传统企业生态小 |
| Alibaba Cloud Linux | Alibaba | 阿里云适配 | 跨云可移植性/国际生态较弱 |
| TencentOS Server | Tencent | 腾讯云/中国生态 | 国际第三方认证与生态需逐项核对 |
| OpenCloudOS | 社区/腾讯生态 | 中国服务器生态、开源 | 全球认证/ISV 覆盖不及 RHEL |
| openEuler | 开放原子/社区生态 | ARM/鲲鹏、服务器、云、国产生态 | 生态碎片化与兼容验证成本 |
| KylinOS / 银河麒麟 | 中国商用 | 党政/企业国产生态、国产硬件适配 | 国际软件生态/许可证/采购依场景 |
| UOS Server / 统信服务器 | 中国商用 | 国产终端/服务器生态 | 同上 |
| Red Flag Linux / 中科红旗 | 中国 Linux 历史/现行产品线 | 中文化与国产 Linux 历史价值 | 产品版本、支持周期、ISV 认证须采购时重新核实 |

## 5.2 桌面/开发者/滚动发行

- Fedora Workstation / Server
- openSUSE Leap / Tumbleweed
- Arch Linux
- Manjaro
- EndeavourOS
- Gentoo
- Linux Mint
- Pop!_OS
- Zorin OS
- elementary OS
- Deepin
- openKylin
- KDE neon
- MX Linux

**优点**：新硬件、新桌面、新编译器、新内核进入快。  
**缺点**：滚动版/前沿版不应未经 OQ/PQ 直接作为核心生产服务器。

## 5.3 云原生/不可变/容器宿主

- Fedora CoreOS
- Flatcar Container Linux
- Bottlerocket
- Google Container-Optimized OS
- Talos Linux
- openSUSE MicroOS
- Ubuntu Core

适合 Kubernetes/容器节点、不可变基础设施（Immutable Infrastructure）与减少攻击面；不适合作为传统“什么都装”的万能服务器。

## 5.4 极简、嵌入式与网络

- Alpine Linux
- OpenWrt
- Yocto Project（严格说是构建体系，不是单一发行版）
- Buildroot（同上）
- Raspberry Pi OS
- Gentoo（可高度裁剪）

## 5.5 安全、隐私与取证

- Kali Linux
- Parrot OS
- Tails
- Whonix
- Qubes OS（Xen 隔离架构，不宜简单等同普通 Linux distro）

这些系统用于**授权安全测试/隔离/隐私**，不是生产博彩站点攻击工具。

## 5.6 函数式/声明式系统

- NixOS
- GNU Guix System

优势是环境可复现、声明式配置、回滚强；缺点是学习曲线与传统运维/商业 ISV 适配。

---

# 6. 商用版与“民用/社区版”如何选

| 需求 | 首选 | 原因 |
|---|---|---|
| 普通个人 Windows 工作站 | Windows 11 Pro | 软件兼容/驱动/办公最省事 |
| 高端数据分析本机 | Windows 11 + WSL2 Ubuntu / Linux VM | 同时保留桌面兼容与 Linux 生产一致性 |
| 免费稳定服务器 | Debian / Ubuntu LTS / Rocky / Alma | 成本低、生态成熟 |
| 有审计/合规/厂商 SLA | RHEL / SLES / Ubuntu Pro / Windows Server | 生命周期、补丁、支持、认证 |
| SAP/HANA | SLES 或 RHEL | 官方生态成熟 |
| Microsoft AD/.NET/SQL Server 深度绑定 | Windows Server | 身份与企业生态强 |
| Kubernetes 节点 | RHEL CoreOS / Fedora CoreOS / Bottlerocket / Talos / Ubuntu | 不可变/容器化 |
| HPC/科研 | Rocky/RHEL/Ubuntu/Debian | MPI/GPU/Slurm 生态成熟 |
| Apple 软件构建 | macOS | Xcode/Apple 平台唯一正规主机 |
| 航电/硬实时 | INTEGRITY/VxWorks/LynxOS/QNX/RTEMS | 认证/确定性优先，不与通用 Linux 比“高级/低级” |

---

# 7. 云端服务器全景：AWS / Azure / Google Cloud 不是单台“服务器”

## 7.1 超大规模云与企业云

| 平台 | 强项 | 安全/主权能力 | 局限 |
|---|---|---|---|
| AWS | 服务广度、EC2/S3/RDS/EKS/Lambda、Nitro、生态最大之一 | GovCloud、DoD IL5；KMS/CloudHSM、Nitro Enclaves、IAM | 成本模型复杂、egress、服务太多、锁定风险 |
| Microsoft Azure | Windows/AD/M365/.NET、企业混合云、Arc、AKS | Azure Government IL4/IL5；Azure Government Secret IL6 | 许可证/门户/产品命名复杂 |
| Google Cloud | BigQuery、GKE、Vertex AI、数据/AI、零信任文化 | DoD IL5；Google Distributed Cloud 可服务更高密级授权场景 | 企业生态/地区覆盖部分领域小于 AWS/Azure |
| Oracle Cloud Infrastructure | Oracle DB、Exadata、裸金属、网络定价 | 政府/专用区域产品 | 第三方生态较小 |
| IBM Cloud | Red Hat/OpenShift、主机/企业、金融行业 | 企业/受监管行业经验 | 公有云规模与开发者生态较前三小 |
| Alibaba Cloud | 中国/亚洲、大数据、电商、弹性计算 | 中国本地合规/地域生态 | 跨境、国际监管、供应商地缘风险需评估 |
| Tencent Cloud | 中国社交/游戏/媒体、实时音视频 | 中国本地生态 | 国际覆盖与认证视地区 |
| Huawei Cloud | 电信/政企/AI/昇腾生态 | 主权/本地部署选项丰富 | 地缘、出口管制、跨国采购限制需评估 |

## 7.2 性价比 VPS / 裸金属

| 平台 | 优势 | 局限 | 适合 |
|---|---|---|---|
| Hetzner | 欧洲低价高性能、裸金属性价比高 | 托管服务/政府认证/全球区少于 hyperscaler | 测试线、通用服务、科研 |
| Contabo | 大内存/存储便宜 | 性能一致性、支持与高级安全服务不能与 hyperscaler 等同 | 非关键测试、备份、低成本节点 |
| OVHcloud | 欧盟数据主权、裸金属、网络产品 | PaaS/AI breadth 较 AWS/Azure/GCP 小 | 欧洲主权/裸金属 |
| DigitalOcean | 简单、开发者友好 | 大型企业治理/高级托管服务较少 | 中小应用 |
| Akamai Connected Cloud / Linode | 价格直观、边缘网络 | 大型受监管生态较少 | 边缘/通用云 |
| Vultr | 多地域、简单实例/GPU | 合规/托管服务生态相对小 | 开发、推理、边缘 |

## 7.3 私有云/混合云

- OpenStack
- VMware Cloud Foundation
- Nutanix Cloud Platform
- OpenShift
- Kubernetes + Ceph
- Proxmox VE（中小规模/实验室）

**优点**：数据主权、控制权、可定制。  
**缺点**：你自己承担 SRE、容量、补丁、硬件、灾备、密钥、人才与 24×7 值守。

---

# 8. 国家级/政商民采用：必须区分“已使用”“获授权”“可采购”

## 8.1 可公开核验的代表性事实

### AWS

- AWS GovCloud (US) 支持 FedRAMP High 与 DoD SRG IL4/IL5 范畴；
- NASA/JPL 公开使用 AWS/GovCloud 处理、分析与分享火星任务数据；
- AWS 公开案例还涉及 NASA、美国人口普查局、退伍军人事务等公共部门。

**正确表述**：AWS 确实进入国家级/宇航/政府工作负载，但不能推导“所有 NASA/DoD 系统都在 AWS”。

### Microsoft Azure

- Azure Government 被 DoD 实体用于多类工作负载；
- Azure Government 支持 DoD IL4/IL5；
- Azure Government Secret 获 DoD IL6 等授权，可支持 Secret 级工作负载。

**正确表述**：Azure 有国家安全专用云产品和授权，不等于任何 Azure 商业区自动满足这些要求。

### Google Cloud

- Google Cloud 公布 DoD IL5 授权能力；
- Google Public Sector 公布 Defense Innovation Unit、美国空军、NASA 等案例；
- Google Distributed Cloud Hosted 已取得面向 Secret/Top Secret 任务的授权能力。

### RHEL / Red Hat

- RHEL 10 是企业 Linux 主线，支持混合云、机密计算与后量子安全准备；
- Zoom for Government 公布其平台运行于 RHEL，以满足 FedRAMP/DoD 严格要求；
- Red Hat 对 DoD 提供公开的现代化与安全解决方案。

**正确表述**：RHEL 是国防/政府生态中的重要商用 Linux，但具体武器/情报系统是否采用、采用哪一版本，仍须逐项目一手证据。

## 8.2 “国家为什么愿意用商业产品？”

因为国家安全并不等于“每个零件都由公务员从零写”：

```text
商业/开源底座
+ 国家/任务方认证
+ 数据分级
+ 专用网络/区域/气隙
+ 本国/授权人员
+ 密钥主权
+ 最小权限
+ 审计
+ 独立验证
+ 任务软件
= 可接受的国家级系统
```

---

# 9. 航电、宇航、军舰、雷达：不要用“比 Linux 高级”这种比较

## 9.1 真正比较维度

- 硬实时（Hard Real-Time）
- 最坏执行时间（WCET）
- 确定性调度
- 时间/空间分区
- 最小可信计算基（TCB）
- 安全完整性等级
- DO-178C / ARINC 653 / IEC 61508 / ISO 26262 等相应认证
- 故障隔离与降级
- 可证明启动/固件信任链
- 供应链与配置管理

## 9.2 典型 RTOS / 安全关键系统

| 系统 | 类型 | 长处 | 不适合 |
|---|---|---|---|
| INTEGRITY-178 | 分离内核/航空安全关键 RTOS | 高安全等级、分区、认证 | 通用服务器 |
| VxWorks / VxWorks 653 | RTOS | 航空航天/工业生态强 | 通用数据平台 |
| LynxOS-178 | 安全关键 RTOS | 分区与认证 | 大规模通用云 |
| QNX | 微内核 RTOS | 汽车/工业/嵌入式 | 通用数据仓库 |
| RTEMS | 开源 RTOS | 宇航/科研、可定制 | 企业桌面/一般 Web |
| RedHawk Linux | 实时 Linux | 仿真、HIL、低延迟数据采集等 | 不应无证据写成某战机“核心飞控 OS” |
| Linux PREEMPT_RT | 实时化 Linux | 工业/边缘、生态大 | 安全关键认证需按项目评估 |

---

# 10. 数据安全与密码学：世界级不是“装一个防毒软件”

## 10.1 零信任（Zero Trust Architecture, ZTA）

NIST SP 800-207 的核心是：**不因网络位置、设备归属或“在内网”而默认信任**。每次访问围绕身份、设备、资源、策略重新认证与授权。

## 10.2 密码学与密钥治理矩阵

| 层 | 推荐技术 | 要点 |
|---|---|---|
| 传输加密 | TLS 1.3、mTLS、IPsec、WireGuard | 禁止明文管理面 |
| 静态加密 | BitLocker、LUKS2、FileVault、云磁盘加密 | 密钥与数据分域 |
| 密钥 | KMS、HSM、CloudHSM、Managed HSM、Vault | 双人控制、轮换、审计、禁把 key 与 data 放一起 |
| 身份 | FIDO2/WebAuthn/passkeys、MFA、OIDC/OAuth2、SAML | 管理员尽量抗钓鱼 MFA |
| 服务身份 | SPIFFE/SPIRE、mTLS、短期凭证 | 不用长期共享密码 |
| 机密计算 | AMD SEV-SNP、Intel TDX/SGX、Nitro Enclaves 等 | 降低云管理员/宿主侧可见性；仍非万能 |
| 软件供应链 | SBOM、SLSA、Sigstore/cosign、TUF、锁版/哈希 | 防依赖污染与构建漂移 |
| 数据防泄漏 | 分类标签、DLP、列/行权限、tokenization、脱敏 | 默认最小可见 |
| 不可变审计 | WORM/对象锁、集中日志、签名、时间同步 | 谁/何时/为何/读了什么都要可追 |
| 后量子密码 | ML-KEM、ML-DSA、SLH-DSA；crypto-agility | NIST 已定稿的第一批 PQC 标准可进入迁移规划 |

## 10.3 后量子密码（Post-Quantum Cryptography, PQC）

NIST 已定稿：

- FIPS 203：ML-KEM
- FIPS 204：ML-DSA
- FIPS 205：SLH-DSA

工程重点不是“今天全部换掉 RSA/ECC”，而是：

1. 做密码资产清册（crypto inventory）；
2. 实现密码敏捷性（crypto-agility）；
3. 先处理“现在截获、未来解密”的长寿命数据；
4. 用标准混合/迁移方案逐步上线；
5. 禁止自创密码算法。


## 10.4 本机端点安全 × Speedtest 实证专题（2026-09-30 · v1.2.0）

### 10.4.1 本轮 LO1 观测账：先把事实与推论分开

| 观测 | Browser Speedtest | Windows Speedtest App | 当前证据 |
|---|---:|---:|---|
| 下载 | **183.33 Mbps** | **339.63 Mbps** | LO1 |
| 上传 | **199.59 Mbps** | **191.79 Mbps** | LO1 |
| Idle Ping | **8 ms** | **6 ms** | LO1 |
| Browser 下载负载延迟 | **50 ms** | 截图未提供 | LO1 |
| Browser 上传负载延迟 | **7 ms** | 截图未提供 | LO1 |
| 测试标签 | MagtiCom / Tbilisi | MagtiCom / Tbilisi | **同供应商/城市；未证明同一物理节点** |

派生量：

\[
\text{Browser download penalty}=1-\frac{183.33}{339.63}=46.02\%
\]

\[
\text{App uplift vs Browser}=\frac{339.63-183.33}{183.33}=85.26\%
\]

\[
\text{Browser upload vs App}=\frac{199.59-191.79}{191.79}=+4.07\%
\]

**当前只允许的解释**：差异高度集中于**下载路径**，物理链路至少在当时能达到约 340 Mbps；但单次截图仍无法把差异归因于 Chrome、Kaspersky、Defender、亿赛通、协议差异、server instance、测试并发策略或短时拥塞中的任何一个。

Google Fiber 对 Ookla 的官方使用指引建议最准确时优先桌面 App，并指出浏览器测试在约 3 Gbps 以上可能低估；本机仅 0.34 Gbps，故**通用浏览器上限不是这次 46% 差异的充分解释**。

### 10.4.2 本轮 PowerShell 观测账

| 检查 | 实测 | 严密解释 |
|---|---|---|
| SecurityCenter2 AV 登记 | Windows Defender + Kaspersky Endpoint Security for Windows | 两产品均被 Windows Security Center 看见；**不等于两套完整实时 AV 已同时扫描同一流量** |
| Defender | `AMRunningMode=Normal` | Microsoft 官方：`Normal` = Defender Antivirus 主动模式 |
| Defender RTP | `RealTimeProtectionEnabled=True` | 实时防护已开 |
| Defender NIS | `NISEnabled=True` | 网络检查系统已开 |
| Defender IOAV | `IoavProtectionEnabled=True` | Internet/附件相关扫描能力已开 |
| Kaspersky CA | `Kaspersky Endpoint Security Personal Certification Authority` ×2 | KES 根证书存在；**仍须查证书库位置/Thumbprint 与实际站点 issuer** |
| WinHTTP Proxy | Direct access | 无显式 WinHTTP Proxy |
| User Proxy | `ProxyEnable=0` | 无显式当前用户代理 |
| PAC | 空 | 无显式 AutoConfigURL |

Microsoft 官方文档另指出：Windows Security 会汇总第三方防毒状态；在一般情形，安装且维持更新的第三方 AV 会使 Microsoft Defender Antivirus 被禁用或进入相应非主动角色。**本机却观测到 Defender = Normal，而 Kaspersky 同时被注册**，因此这是一个必须继续核实的状态组合，而不是直接宣告「双 AV 冲突已证实」。下一步必须读取 Windows Security 的 *Manage Providers*、Kaspersky 服务/进程与本地策略状态。

### 10.4.3 Kaspersky TLS 检查：什么已证实，什么尚未证实

Kaspersky Endpoint Security 官方文档明确给出三种加密连接扫描模式：

1. **Do not scan encrypted connections**；
2. **Scan encrypted connections upon request from protection components**；
3. **Always scan encrypted connections**。

同一文档明确说明 KES 使用 Kaspersky root certificate **decrypt and analyze encrypted traffic**，且覆盖 TLS 1.0–1.3。故：

```text
[已证实]
本机存在 Kaspersky 根 CA
+ KES 产品家族具备 TLS 解密/检查能力

[尚未证实]
当次 speedtest.net 是否实际被 Kaspersky 重新签发
当次下载数据是否逐流经过 KES 内容解密
KES 当前到底是哪一种 encrypted-scan mode
两条 Kaspersky CA 是否只是 LocalMachine/CurrentUser 的同一证书副本
```

**最关键一刀**：检查 Chrome 中 `speedtest.net` 的实际 certificate issuer / chain。若 issuer 变为 Kaspersky CA，才把「当次 Browser TLS interception」升级为 LO3 候选；若仍为公网 CA，则根证书存在不能证明该站被解密。

### 10.4.4 Microsoft Defender：网络保护 ≠ Kaspersky 式全文 HTTPS MITM

Microsoft Defender Network Protection 的官方实现说明：对非 Edge 浏览器，它可通过 TCP/TLS 握手中的 `ClientHello` 判断 HTTPS 连接的 FQDN；该能力要求 QUIC/ECH 等条件配合。此机制与「本地根 CA 重新签发站点证书、解密正文」不是同一层。

因此必须分开写：

```text
Defender Network Protection
= TLS handshake / FQDN 级检查与策略执行（公开机制）

Kaspersky Encrypted Connections Scan
= 可用产品根 CA 解密并分析 TLS 内容（配置启用时）
```

**禁止**把 `NISEnabled=True` 直接翻译成「Microsoft 正在解密所有 HTTPS 正文」。

### 10.4.5 redteam/ —— 这次网速诊断最容易掉进的坑

1. 两边都写 MagtiCom/Tbilisi，却未确认同一 Ookla server instance；
2. Browser 与 App 可能使用不同并发数、协议、连接复用或实现；
3. Browser 扩展、Chrome sandbox、JS/worker、缓存/下载扫描会影响接收路径；
4. Kaspersky Web Threat Protection / encrypted scan 可能介入，但须以实际 issuer/trace 证明；
5. 亿赛通 CDG/DLP 可能位于文件/浏览器/WFP/NDIS 数据路径，但本轮无根 CA 或代理证据足以证明 TLS MITM；
6. Defender 主动模式已证实，但其公开网络保护机制不能等同全文解密；
7. 一次先 Browser 后 App 可能叠加短时无线/ISP/服务器负载变化；
8. 下载 loaded latency 50 ms 是排队线索，不是「有人监控」证据；
9. Kaspersky CA 存在 ≠ Kaspersky 公司总部拿到明文；本机检查与云端遥测须分证据链；
10. `ProxyEnable=0` ≠ 无透明过滤；WFP/NDIS/VPN/透明网关均可绕过该设置。

### 10.4.6 critic/ —— 对前轮初步判断的斧正

- **前轮「浏览器本身可能是主因」须降级。** 官方指引把一般浏览器吞吐瓶颈放在约 3 Gbps 级；本机只到 340 Mbps，故浏览器通用上限不足以解释 183 Mbps。
- **「下载差大、上传接近」只是一种诊断形态，不是因果证明。** 安全扫描、接收缓冲、server implementation、协议、Wi-Fi 队列都可能造成方向不对称。
- **「Defender + Kaspersky 双实时扫描」目前仍未闭环。** Defender 主动已证实；Kaspersky 仅证实注册与根 CA 存在，仍须服务/进程/设置页与 Windows Security Provider 状态。
- **没有显式 Proxy 的证据很强，但只削弱远端显式代理假说。** 不能排除本机过滤驱动或透明网络设备。

### 10.4.7 killcritic/ —— 网络诊断一票否决

任一出现即视为过度归因：

- ❌ 根 CA 存在 ⇒ 「厂商总部正在阅读全部明文」；
- ❌ `AMRunningMode=Normal` + Kaspersky 已注册 ⇒ 「两套 AV 已证实逐包重复扫描」；
- ❌ `ProxyEnable=0` ⇒ 「不存在任何中间过滤」；
- ❌ 一次 Speedtest ⇒ 「已证明某安全软件导致 46% 损失」；
- ❌ Browser 比 App 慢 ⇒ 「TLS 密码算法太慢」；
- ❌ Loaded latency 高 ⇒ 「网络被政府/厂商远程监控」；
- ❌ 未经组织授权关闭 EDR/DLP/AV 来追求测速分数。

### 10.4.8 blindspot/ —— 仍缺的关键证据

- Kaspersky `avp` 服务/进程是否 Running；
- Kaspersky Encrypted Connections Scan 当前具体模式；
- `speedtest.net` 当次证书 issuer / chain；
- 两条 Kaspersky CA 的 `PSParentPath` 与 Thumbprint 是否相同；
- Windows Security → Manage Providers 中谁是 primary AV；
- 是否存在 Defender for Endpoint / tamper protection / 组织策略导致 Defender 保持 Normal；
- Chrome 与 Edge 是否同样约 180 Mbps；
- 同一**精确 Ookla server ID**下 5×交错 A/B 是否复现；
- Browser/App 测试时 `avp.exe`、`MsMpEng.exe`、亿赛通进程 CPU/IO 是否同步抬升；
- ETW/WFP/ProcMon 是否显示额外过滤/排队；
- Wi-Fi PHY rate、RSSI、驱动、路由器 bufferbloat 是否稳定。

### 10.4.9 cheatsheet/ —— 只读诊断命令

```powershell
# 谁被 Windows Security Center 登记为 AV
Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct |
  Select-Object displayName, productState, pathToSignedProductExe

# Defender 角色
Get-MpComputerStatus |
  Select-Object AMRunningMode,AMServiceEnabled,AntivirusEnabled,
                RealTimeProtectionEnabled,BehaviorMonitorEnabled,
                NISEnabled,IoavProtectionEnabled

# Kaspersky 服务 / 进程
Get-Service |
  Where-Object {$_.DisplayName -match 'Kaspersky' -or $_.Name -match 'Kaspersky|AVP'} |
  Select-Object Status,Name,DisplayName

Get-Process -ErrorAction SilentlyContinue |
  Where-Object {$_.ProcessName -match 'avp|kaspersky'} |
  Select-Object ProcessName,Id,CPU,WorkingSet64,Path

# Kaspersky CA 位置/指纹
Get-ChildItem Cert:\LocalMachine\Root, Cert:\CurrentUser\Root |
  Where-Object {$_.Subject -match 'Kaspersky'} |
  Select-Object PSParentPath,Subject,Issuer,Thumbprint,NotBefore,NotAfter |
  Format-List

# 显式代理 / PAC
netsh winhttp show proxy
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
  Select-Object ProxyEnable,ProxyServer,AutoConfigURL
```

### 10.4.10 blueprint/ —— 从「测速差」到「根因」的证据晋级

```text
LO1 单次结果
Browser 183 / App 340
        ↓
固定 exact Ookla server + 同网络 + 同位置
        ↓
LO2：5× 交错 A/B
Browser ↔ App
        ↓
Chrome ↔ Edge ↔ App 三角测试
        ↓
证书 issuer / Kaspersky scan mode / Provider role
        ↓
进程 CPU/IO + ETW/WFP/ProcMon
        ↓
LO3：机制 + 重复效应同向
        ↓
仅在组织授权下做 one-factor-at-a-time 消融
        ↓
根因 / 非根因 / 未裁定
```

### 10.4.11 actionplan/ —— 当前最小正确下一步

1. **不关闭** Defender/Kaspersky/亿赛通，保留现状作为 baseline；
2. 查 Kaspersky service/process、scan mode、两条 CA thumbprint；
3. 查 `speedtest.net` 实际 certificate issuer；
4. 固定同一 exact server，做 `Browser→App→App→Browser` 交错 **各 ≥5 次**，记录下载/上传/ping/loaded latency；
5. 加 Edge 形成 Chrome/Edge/App 三角；
6. 同时采集 `avp.exe`、`MsMpEng.exe`、亿赛通进程 CPU/IO；
7. 若差异稳定且与安全进程/证书链同向，再升级 LO3；
8. 任何停用/排除策略只在设备所有者/组织管理员授权后，一次只改一个变量，并立即恢复。

---

## 10.5 主体身份锚（Principal Identity Anchor · v1.1.2 增量 · C-DAQIN-36）

> **§10.1–§10.4 治的是「系统」的身份**（零信任、KMS/HSM、PQC、端点）。
> **本节治的是「人」的身份** —— 即：当补丁、风控、2FA 全部正常工作时，**主人自己被锁在门外**。
> 这与 §13 的出口闸是对称的：**出口闸防数据出去，身份锚防主人进不来。**

### 10.5.1 失效模式：安全措施把主人锁在门外

系统认的从来不是「主人」，是**凭证与行为模式**。凭证断、模式变，它就不认得你——**它从来就不认得你，只认得那串东西**。

| 机制 | 本意 | 失效表现 | 等级 |
|---|---|---|---|
| 设备指纹 / 风控评分 | 挡盗号者 | 换机、换 IP、跨国登录 → 被判为盗号者 | P1·M5 |
| 2FA 绑手机号 | 多一道锁 | 号码停用 → **锁与钥匙一起丢** | P1·M5 |
| 异地登录冻结 | 防撞库 | 人在国外 → 冻结 | P1·M5 |
| 自动补丁重置策略 | 修漏洞 | 覆盖手改的例外规则 | P2·M5 |
| TPM / BitLocker / FileVault | 防物理盗取 | **固件更新 → 密封密钥失效 → 要恢复密钥，而当初没存** | P1·M5 |

> **对「AI 会否因数据安全而不认主人」之裁定**：不会因安全而产生敌意，但**会因身份链断裂而无法确认你是你**——**效果相同，成因不同**。这是**身份锚设计问题**，不是意图问题。不得写成「AI 背叛主人」。

### 10.5.2 终身制电话号码 —— 查证结论：**不存在**（P1·M5）

| 宣称 | 实测 | 判定 |
|---|---|---|
| Keepgo「Lifetime World SIM」 | 官方 FAQ 明文：**纯数据卡，不附带电话号码** | ❌ 不是号码 |
| 印度 Airtel / Jio / BSNL「终身有效」 | 已重构为长期套餐——「终身」实为 **3 / 6 / 12 个月** | ❌ 营销词 |
| TSIM「Lifetime validity permanent SIM」 | 同为**数据卡**；「终身」指余额不过期 | ❌ 不是号码 |
| RNK Telecom「Phone for Life」US$999 | 早期 VoIP 方案，**「life」指公司存续期** | ❌ 已成历史 |
| 马斯克 / 马云「终身免费号码」 | **未检得任何一手证据** | **UNKNOWN，不入轴** |

**结构性原因**：电话号码不是财产，是**主权国家的编号资源，租给你用**。

```text
ITU E.164 国际编号计划
    ↓ 分配
各国监管机构（🇲🇾 MCMC · 🇺🇸 FCC/NANPA · 🇨🇳 MIIT）
    ↓ 划拨号段
电信运营商
    ↓ 租用（附条件：持续缴费、实名、在网）
主体（你）
```

**任何公司都无法承诺终身号码，因为它自己也只是承租方。** 运营商倒闭、被并购、退出市场、号段回收，号码即失。这不是商业诚信问题，是**资源产权层面的不可能**。

> **衍生禁令（并入 §21 Blindspot）**：停机满期后号码将**回收再分配给新用户**。故**禁止**把 2FA 或账户恢复的唯一通道绑定于手机号——**那个号码将来会属于别人**。

### 10.5.3 五层身份锚（强制 · v1.2.2 由三层升五层）

> **v1.1.2 原为三层（L1 密码学 / L2 自有域名 / L3 离线恢复码）。本版新增 L0 与 L3，理由见 §10.5.5：
> 顶尖体系的分水岭不在「终身 vs 非终身」，而在「**租用命名空间 vs 自有命名空间**」——L0 决定上面四层能否终身。**

```text
L0  命名空间产权 ← 决定性的一层
    自有 ✓  |  租用 ✗
     │
L1  密码学凭证（认证）     PKI / Passkey / Hardware Key / DID / PGP
     │                      ← DoD: CAC 证书 | EU: EUDI 钱包
L2  持久标识符（识别，非认证）  EDIPI · ORCID · ISNI · 自有域名
     │                      ← 可公开，绝不可当密码
L3  可携通道（联络）        MNP · 自有域名邮箱
     │                      ← 抗换服务商，不抗欠费停机
L4  离线恢复（最后防线）    纸本恢复码 · 保险箱
                            ← 不依赖任何在线通道
```

#### 命名空间产权判别表（L0）

| 租用者（必失效） | 自有者（可终身） |
|---|---|
| 电话号码（ITU E.164） | DoD EDIPI |
| 免费邮箱地址 | ORCID / ISNI |
| 平台账号 | 自有域名 |
| 社交媒体 handle | 密码学密钥对（L1） |

**所有顶尖体系的共同动作，就是从左栏搬到右栏。**

#### 原三层对照（保留，不删）

| 层 | 手段 | 永久性来源 | 强度 |
|---|---|---|---|
| **L1 密码学** | 硬件密钥 / Passkey / PGP / DID | **无发行方，数学自证** | ⭐⭐⭐⭐⭐ |
| **L2 自有域名** | `you@yourdomain.com` | **域名在手，邮箱可跨服务商携带** | ⭐⭐⭐⭐ 最实际 |
| **L4 离线恢复码** | 纸本 + 保险箱 | 不依赖任何在线通道 | ⭐⭐⭐⭐ |
| 参考 | 国家数字身份（Aadhaar / Singpass / e-Residency / **EUDI**） | 主权发行 | ⭐⭐⭐ 绑一法域 |
| 参考 | 号码携转 MNP | 跨运营商保号 | ⭐⭐ 不抗停机 |

#### 三条硬禁令（原两条 + 新增一条）

1. **禁止**把 L1/L2/L4 全部绑在同一条通道上（单点失效）。
2. **禁止**把恢复邮箱绑在需手机验证的免费邮箱上（**循环依赖**）。
3. **禁止**把 L2 持久标识符当作凭证使用 —— **EDIPI 印在卡背面、ORCID 公开可查；标识 ≠ 认证**（C-DAQIN-39）。



### 10.5.4 ActionPlan（主体侧，非系统侧）

| 序 | 动作 | 说明 |
|---|---|---|
| 1 | **购自有域名** | 根治。此后换国、换号、换服务商，恢复通道不动 |
| 2 | **全账号恢复邮箱迁至自有域名** | L2 落地 |
| 3 | **导出并离线保存全部恢复码** | 唯一不依赖号码与邮箱的凭证 |
| 4 | **导出 BitLocker / FileVault 恢复密钥** | §10.5.1 最后一行的直接对策 |
| 5 | GitHub 恢复走 `github.com/contact` | **提供旧 SSH 公钥指纹或历史 commit 签名** —— GitHub 认可的非手机凭证 |
| 6 | **公开仓库清除 C4 级个人数据** | 见 §27.3 |
| 7 | **申请 ORCID iD** | **L2 层，零成本，永久。** 主体已具条件（已发表研究 + ResearchGate）却从未申请。有了 ORCID，研究身份即与任何机构、平台、电话号码脱钩（U-27） |
| 8 | **买域名 = L0 动作** | 前六项皆建于此。**L0 不动，L1–L4 全部是在租来的地基上盖楼** |

---

### 10.5.5 顶尖体系实证对照（新增 · v1.2.2 · 非菲印锚定）

> **须先说清方法论**：前版以菲律宾、印度为例，**不是挑小国，而是全天下仅此两个司法管辖区把「终身号码」写进公开监管正文并作出裁定**。本节补齐顶尖电信、科研院、军工宇航链、科技与军事强国的实际做法。
>
> **总裁定：顶尖体系压根不玩「终身电话号码」，他们把电话号码整个踢出身份体系，自发一套命名空间。**

#### A. 美国国防部 — EDIPI：**真正的终身编号（P0·M5）**

| 项 | 实测 |
|---|---|
| 名称 | EDIPI（Electronic Data Interchange Personal Identifier）／DoD ID Number |
| 结构 | **10 位**：前 9 位顺序分配，自 `100000000` 起；第 10 位为校验位 |
| **永久性** | **前 9 位终身分配，永不重新分配** |
| 跨身份持续 | **不论转换军种或部门，整个 DoD/USCG 生涯保持不变；退役军人转任 DoD 文职或承包商时随之延续** |
| 生命周期 | 使军事医疗系统得以在**单一标识符下追踪一个人的整个生命跨度** |
| 起源 | 2011 年起换发新证时以 DoD ID 取代 SSN |
| 载体 | CAC 正反面条码 + 内嵌芯片；退休者与眷属持 USID 卡 |
| 主体范围 | 现役、后备、国民警卫、文职、承包商、退休人员、合格眷属 |
| 角色分离 | 角色细节由独立的 **DoD Benefits Number（DBN，11 位）** 管理，**多重身份不产生重复标识符** |

**与电话号码的结构性对比：**

| | 电话号码 | **EDIPI** |
|---|---|---|
| 产权 | 国家编号资源，**租用** | 发行机构**自有命名空间** |
| 回收 | 停机后**回收再分配给新人** | **永不重新分配** |
| 条件 | 持续缴费、实名、在网 | **无** |
| 跨角色 | 不适用 | 跨军种、跨退役、跨文职、跨承包商 |

> **⚠ C-DAQIN-39：EDIPI 是标识符，不是凭证。** 它公开印在卡背面；认证靠 CAC 芯片内的 PKI 证书。**把 EDIPI 当密码用是灾难性误用。** 此即 §10.5.3 之 L1/L2 分层的教科书实例。

#### B. 欧盟 — eIDAS 2.0 / EUDI 钱包（P0·M3→M4）

详见 **§0.6.3**（含 2026-12-24 法定期限与三点时效告警）。要点：

- 自然人必备身份属性：姓、名、出生日期、**唯一标识符（Unique Identifier）**
- 三条设计铁律：**选择性披露 · 无中心化数据系统 · 用户控制访问**
- 技术路线：可验证凭证（VC）；**W3C DID**（无中心注册表即可解析密钥）在部分生态中使用
- 2030 目标：52–85% 公民持有活跃钱包

#### C. 科研体系 — ORCID / ISNI（P1·M5）

| 项 | 实测 |
|---|---|
| ORCID | 开放、跨学科的社群努力，提供研究者唯一标识符的**自主声明注册表** |
| ISNI | 为研究者、发明人、作家、艺术家、表演者、出版者的公开名称**分配持久唯一识别码**，以解决检索中的姓名歧义 |
| 格式 | **两者使用同一套 16 位标识符格式** |
| 互通 | 双方备忘录同意通过标识符互链与公开数据共享实现互操作 |

> **科研界的终身身份不是电话，是 ORCID。** 换机构、换国家、改名，iD 不变。
> **与 §30.13「科研代码托管」互补**：该节主张 `canonical author identity + signed commits + mirror + archive`——**ORCID 正是那个 canonical author identity 的现成国际实现**。

#### D. 英国 070「个人号码」— 失败教训（P1·M5）

FleXtel 于 1993-12 推出英国首个个人电话号码服务，可路由至任何其他号码含国际移动号码；《纽约时报》1992 年报道标题即为「Lifetime Telephone Numbers」。

**结局**：070 号码在国际上被识别为英国号码，**即使实际终结于任何地方的移动号码——此特性被用于各种诈骗**。

> **教训**：一个可任意重路由却无强认证绑定的「终身号码」，**灵活性即攻击面**。
> 此条直接支持 §30.12 之裁定：LCI 不得承诺「全世界每个人永远免费占有一个受监管电话号码」。

#### E. RNK Telecom「Phone for Life」— 商业终身承诺的完整证伪（P0·M5）

**上一版把该方案归入「不是号码」一类，此为错误，见 SC-ζ。** 它**确实给号码**：住宅用户获得 VoIP 线路、话机、**电话号码**、完整功能集与无限进出通话；RNK 提供 911 与 411 服务，并可将既有号码携入。

| 时间 | 事件 |
|---|---|
| 2004-11/12 | RNK Inc.（麻州 Dedham，私人持股 CLEC）推出「Phone for Life」：住宅 **US$999**，通美加及 20 国与另 21 个外国城市；商用 **US$99** 计量版（无限接听，外拨 .019 美分/分钟）；经 MA/NY/NH/RI 经销商销售 |
| 退款条款 | 两个月无条件退款；五年后仍不满意可退一半，扣除部分通话费 |
| 精算 | **印度 TRAI 2006 年谘询文件**载：RNK 查阅了精算表，并同意使该服务**可转让** |
| 当年话术 | 销售方 Tessier：「我们已经营七年，是一家**盈利的、自建设施的**电话公司。」 |
| 2007-10-30 | Wave2Wave 以 **4,470 万美元**收购 RNK 全部股本 |
| 2011-09 | Verizon 与 RNK 就互联结算与接入费争议和解（此前 Verizon 将月款大部分托管，对应逾 400 万美元「声称余额」） |
| **2012-02-17** | RNK、Wave2Wave 及关联方申请 **Chapter 11**（D.N.J. 案号 12-13896 DHS）；资产与负债各达 1 亿美元；起因为 **Verizon 威胁切断其服务** |
| 2012-08-20 | 法院批准依第 363 条转让几乎全部资产及电信牌照之出售程序 |
| **2012-09-27** | 法院批准将 RNK 电信资产与牌照售予 **Signal Point**；含客户合同；**RNK 与 RNK VA 将被解散** |
| **2012-11-13** | RNK 之 Chapter 11 **转为 Chapter 7 清算** |
| 2016-03 | Oak Point Partners 收购该破产财产之剩余资产 |

> **裁定**：「Phone for Life」实际存续约 **8 年**（2004–2012）。**买单的客户，活过了卖方。**
> 客户合同虽随资产售予 Signal Point，但**签约对手方 RNK 已被解散**；Signal Point 是否继续履行终身承诺 —— **UNKNOWN（U-23）**。

#### F. 监管机构对「终身」的官方定义（P0·M5）

印度 TRAI 谘询文件载：这类方案使客户以约 1,000 卢比的一次性付款换取终身接听来电的权利；但**「终身」的实际期限被服务商限定为其获准提供电信服务的许可期限内**。

> **这是全天下最精准的一句官方定义：**
> **「终身」＝ 运营商牌照的有效期，不是人的一生。**

#### G. 菲律宾 — 全球唯一把号码永久性写进法律者（P0·M5）

参议院第 1636 号法案「终身手机号码法」以 **20 票赞成、零弃权零反对**通过，成法为 **RA 11202「手机号码可携法」**。NTC 实施细则：用户可**免费申请永久号码**，前提是**已结清与原服务商的所有义务**，且现用号码已启用满 60 天；电信实体须在 **24 小时**内完成，否则最高罚一百万比索。立法意图是「给消费者选择服务的灵活性，而不必失去他们的**数字身份**」。

> **但注意那个前提：已结清所有义务。**
> **监管保证的是「跨运营商」，不是「跨欠费」。** MNP 抗换商，不抗停机 —— 与 §10.5.3 之 L3 定级一致。

#### H. 五层锚跨体系对照总表

| 体系 | L0 命名空间 | L1 凭证 | L2 持久标识 | L3 可携通道 | L4 离线恢复 |
|---|---|---|---|---|---|
| **美国 DoD** | **自有** | CAC PKI | **EDIPI** | — | — |
| **欧盟 eIDAS 2.0** | **自有** | EUDI 钱包 / VC | Unique Identifier | — | — |
| **科研界** | **自有** | — | **ORCID / ISNI** | — | — |
| **菲律宾 RA 11202** | 租用 | — | — | **MNP 法定** | — |
| **英国 070** | 租用 | **无** | — | 任意重路由 | — |
| **RNK Phone for Life** | 租用 | — | — | ✗ **公司已清算** | — |
| **本件主体现状** | **租用** | ✗ | ✗ | 手机号（已断） | ✗ |

**最末一行是 §10.5.4 全部行动项的落点。**

#### I. 仍属 UNKNOWN 者（不得填空）

| 项 | 状态 |
|---|---|
| 顶尖电信商（AT&T / Verizon / NTT / 中国移动 / Telefónica）内部员工终身标识体系 | **UNKNOWN（U-24）** |
| 中国 MIIT 是否有对标 EDIPI 之统一编号 | **UNKNOWN（U-25）** |
| 俄、以、印、日、韩国防体系对应物 | **UNKNOWN** |
| SpaceX / Anduril / Lockheed 等承包商内部体系 | **UNKNOWN** |

> **按第三轮已登记之 K2 样本偏差铁律**：证据池限于公开招标与官方文件，**「查不到」≠「不存在」**。
> 但反过来，**证伪只需一个反例**：已查到的 DoD EDIPI / EU eIDAS / ORCID 三例，已足以推翻「顶尖体系靠终身电话号码」之假设。

#### J. 讽刺性旁证

**发号码的电信商，自己不用号码认人。** 他们用员工编号、PKI 证书、SSO。**这本身就是最强的证词。**

---

# 11. 数据泄露的真正攻击面

## redteam/

1. 管理员账号被钓鱼；
2. API key / token 写入 Git；
3. CI/CD runner 权限过大；
4. 云存储桶/对象 ACL 配错；
5. 第三方 SaaS/插件过度授权；
6. 终端被植入信息窃取恶意软件；
7. SSH 私钥/浏览器会话 cookie 被盗；
8. 数据导出到个人盘/聊天软件；
9. 内部人员批量查询；
10. 供应链包投毒；
11. 日志本身泄露 PII；
12. 模型训练集/向量库暴露；
13. 备份无加密或长期不清；
14. 测试环境复制生产 PII；
15. 合成数据记忆真实记录；
16. 机密计算被误当作“云厂商绝对看不到任何信息”；
17. 气隙被 USB/供应链/维护设备跨越；
18. DNS/HTTP egress 可作为隐蔽通道；
19. 权限长期不收回；
20. 外部 AI 提示词带出敏感原文。

---

# 12. 人工智能、强化学习与量化：模型阶梯

```text
Rule / Wilson / EWMA / GLM
      ↓
GBDT (XGBoost / LightGBM / CatBoost)
      ↓
Survival / competing risks
      ↓
HMM / state-space / IMM
      ↓
Entity resolution / Graph
      ↓
Sequence / Transformer
      ↓
Contextual Bandit / Constrained RL
```

**铁律**：

- Deep Learning 不是默认首选；
- Transformer 必须证明严格 OOT / walk-forward 稳定增量；
- RL 必须先有安全动作集、离线策略评估（OPE）、因果基线与合规签核；
- 对百家乐牌局结果/RNG/派彩的 AI/RL 控制：**NO-GO**；
- Responsible Gambling 信号进入营销/返水/VIP/催存：**NO-GO**。

---

# 13. 合成数据、真实数据与数据安全统一协议

```text
Z0 REAL DATA VAULT
  原始真实数据 / PII / 生产密钥
      ↓（最小权限、脱敏、tokenization、purpose bound）
Z1 PRIVACY ENGINE
  aggregation / DP / de-identification / feature views
      ↓
Z2 SYNTHETIC LAB
  模拟数据 / 合成数据 / 压测 / 失败演练
      ↓
Z3 MODEL ARTIFACT
  code / weights / model card / SBOM / hash
      ↓
Z4 SEALED REAL GOLD HOLDOUT
  只用于最终真实性验证
      ↓
Z5 SHADOW
  只打分不动作
      ↓
Z6 HUMAN REVIEW
      ↓
Z7 CONTROLLED ROLLOUT
```

## 13.1 合成数据五门

1. Purpose：目的是否明确；
2. Fidelity：统计/依赖/时序/尾部/图结构；
3. Utility：TSTR（Train Synthetic Test Real）；
4. Privacy：DCR、membership inference、linkage、attribute inference、DP；
5. Transfer：到真实 sealed holdout 是否仍成立。

**模拟数据可以证明系统“跑得动”，不能单独证明真实欺诈召回率、真实 ROI 或真实公平性。**

---

# 14. AI/数据/量化科技栈总表

## 14.1 统计与机器学习

- R / Python / SQL
- statsmodels / scikit-learn
- XGBoost / LightGBM / CatBoost
- Random Forest / Isolation Forest
- brms / Stan / PyMC
- survival / lifelines / randomForestSRC
- HMM / state-space / IMM
- GARCH / ARIMA / ETS / TBATS / Prophet
- LSTM / GRU / Transformer
- graph-tool / NetworkX / igraph / PyTorch Geometric / DGL
- Optuna / Bayesian optimization

## 14.2 数据计算

- Polars
- DuckDB
- Apache Arrow / Arrow Flight
- Spark
- Flink
- Kafka / Redpanda
- Iceberg / Delta / Hudi
- StarRocks / ClickHouse
- PostgreSQL / MySQL
- kdb+/q / ArcticDB / QuestDB / TimescaleDB
- Redis / KeyDB
- object storage / S3-compatible storage

## 14.3 调度、血统、可观测

- DolphinScheduler
- Airflow
- Dagster
- Prefect
- targets
- Snakemake
- Nextflow
- OpenLineage / Marquez
- MLflow
- DVC
- Great Expectations / Soda / Pandera
- Prometheus / Grafana / OpenTelemetry

> 当前项目对 StarRocks / DolphinScheduler / Superset 的**连接与实测禁令仍有效**；这里仅做架构登记，不执行连接。

## 14.4 安全工程

- OPA / Rego
- Sigma
- MITRE ATT&CK
- YARA / YARA-L
- SIEM / SOAR
- CrowdStrike / Palo Alto / Mandiant / Sentinel 类能力
- SBOM (CycloneDX / SPDX)
- SLSA
- Sigstore / cosign
- Hashicorp Vault
- KMS / HSM
- secret scanning
- DLP
- EDR/XDR
- CSPM/CNAPP

## 14.5 隐私与可信 AI

- OpenDP
- diffprivlib
- SDV / CTGAN / TVAE
- synthpop
- federated learning / Flower
- homomorphic encryption / TenSEAL
- SHAP / explainability
- Model Cards / Datasheets
- calibration / uncertainty / conformal prediction
- drift / OOD detection

---


## 14.6 半导体、存储与 AI 算力产业链

> **分类纪律**：芯片设计、晶圆制造、封装测试、NAND/DRAM、服务器、GPU 软件栈与云算力属于不同层；“用了 NVIDIA GPU”不能推出“用了 NVIDIA 全套服务器安全架构”。

| 子链 | 代表主体 | 公开强项 / 本件登记 | 证据×成熟度 | 对本项目可迁移 |
|---|---|---|---|---|
| NAND 控制/企业存储 | **群联电子 Phison** | NAND 控制器、SSD/PASCARI；2026 `aiDAPTIV™` 将 SSD/Flash 纳入 AI 内存层，并公开 AI Data Platform/HCI | P1·M4/M5 | 本地 AI、数据驻留、冷热分层、GPU 内存压力测试；**厂商性能数字需复测** |
| GPU/CPU/开放 AI 计算 | **AMD** | Instinct GPU、EPYC、`ROCm 10`；SEV-SNP/机密计算 | P1·M5 | CUDA 单一依赖的 challenger、AI/HPC、多云机密计算 |
| GPU/AI 平台 | **辉达/英伟达 NVIDIA** | CUDA、Hopper/Blackwell/Vera Rubin、NVLink、Spectrum-X、AI Enterprise、机密计算 | P1·M5 | 训练/推理、网络、TEE/attestation；防单一 GPU 供应链锁定 |
| x86/AI PC/Foundry | **Intel** | Xeon/Core Ultra、Gaudi、18A、AMX；与 Phison 合作地端 AI | P1·M4/M5 | CPU/AI PC/边缘推理、供应商多样化 |
| CPU IP | **Arm** | Neoverse / CPU IP / edge-cloud ecosystem | P1·M5 | 高能效服务器/边缘计算 |
| 晶圆制造 | **TSMC / Samsung Foundry / Intel Foundry** | 先进制程与封装制造 | P1·M5 | 供应链韧性；**不直接迁移成软件架构** |
| DRAM/HBM/NAND | **SK hynix / Samsung / Micron / Kioxia** | HBM、DRAM、NAND | P1·M5 | GPU/HPC 容量、带宽、可靠性规划 |
| 光刻/EDA | **ASML / Synopsys / Cadence / Siemens EDA** | 光刻、芯片设计验证工具链 | P1·M5 | 供应链治理、形式验证思想；非业务应用依赖 |
| 网络/交换/互连 | **Broadcom / NVIDIA Networking / Cisco / Arista** | Ethernet/InfiniBand/交换/定制加速互连 | P1·M5 | east-west 网络、训练集群、低延迟与可观测 |
| 服务器/OEM | **HPE / Dell / Lenovo / Supermicro** | 企业/HPC/GPU 服务器 | P1·M5 | 测试线与 AI/HPC 采购竞争基线 |

**Phison 特别校正**：其 2026 官方资料把自身定位从存储供应商扩展为 `AI Enabler`，公开 `Pascari aiDAPTIV™`、AI Data Platform 和 HCI；这证明“**存储可进入 AI memory hierarchy**”已是工程产品方向，但“成本降低多少、性能提高多少”仍应在目标模型/批次/SSD endurance 下自行 benchmark。

**AMD / NVIDIA 双轨原则**：

```text
CUDA / NVIDIA = 当前广度与成熟生态基线
ROCm / AMD     = 开放计算 challenger + 供应链多样化
CPU-only       = 最小可用 fallback
```

任何生产架构不得把“某一张 GPU 型号”写成不可替代的业务真相。

## 14.7 前沿人工智能、机器人与脑机接口

| 分类 | 主体 | 公开方向 | 本件边界 |
|---|---|---|---|
| Frontier AI | OpenAI / Anthropic / Google DeepMind / Meta AI / Microsoft / Amazon / xAI / Mistral / Cohere | 基础模型、Agent、推理、工具调用、企业 AI | 外部 AI 默认不得接触生产原始敏感数据 |
| 中国 AI | DeepSeek / 阿里通义 / 腾讯混元 / 百度文心 / 字节豆包 / 华为盘古 | 模型、云 AI、企业/科研应用 | 模型能力与企业数据安全分别验收 |
| 自动驾驶/具身 AI | **Tesla** / Waymo / Figure / Boston Dynamics / Agility Robotics | 车端 AI、机器人、闭环数据/仿真 | 只迁移数字孪生、shadow、回放、边缘推理；不把道路控制逻辑搬进会员处置 |
| 脑机接口 BCI | **Neuralink** / Synchron / Precision Neuroscience 等 | 神经信号采集、解码、辅助控制 | 属医疗/神经工程；高隐私高安全，**不作为博彩画像输入** |
| 科研 AI | CAS 自动化所 / 计算所、JPL AI、国家实验室/大学 | 多模态、智能系统、HPC、自治、科学 AI | 方法论迁移必须保留安全案例、复现与人类监督 |

**Neuralink 证据锚**：官方 PRIME Study 公开 `N1 Implant` 为侵入式 BCI，1,024 个电极分布在 64 条柔性 threads 上，并由 R1 机器人植入；这是**临床研究中的脑机接口系统**，不是“神经网络软件公司”，更不是可无约束读取思想的技术。

## 14.8 礼逆袭（Linux）与全球开源治理组织

| 组织/社群 | 角色 | 关键价值 |
|---|---|---|
| **Linux Foundation（LF）** | 开源基金会 | Linux 周边生态、治理、培训、基金会托管 |
| **Linux kernel / kernel.org 社群** | 内核开发 | Linux kernel 上游；发行版不等于内核本身 |
| **OpenSSF** | 开源软件安全 | supply-chain security、best practices、Alpha-Omega 等 |
| **CNCF** | 云原生 | Kubernetes、Prometheus、OpenTelemetry 等生态 |
| **Confidential Computing Consortium** | 机密计算 | TEE/attestation 开源协作 |
| **Post-Quantum Cryptography Alliance（PQCA）** | 后量子密码生态 | PQC 开源实现与迁移协作 |
| **OpenChain / SPDX** | 合规 / SBOM | ISO 5230、license/security SBOM |
| **FINOS** | 金融开源 | 金融服务业开源治理 |
| **LF AI & Data** | AI/数据开源 | AI/ML/Data 项目协作 |
| **Yocto Project / Zephyr Project** | 嵌入式 | Linux 构建系统 / RTOS 生态 |
| **Apache Software Foundation** | 数据/中间件 | Kafka、Flink、Airflow 等大量项目 |
| **Eclipse Foundation** | 工具/IoT/开放协作 | 企业级开源治理 |
| **Free Software Foundation / GNU** | 自由软件 | GNU 工具链与自由软件哲学 |
| **Debian Project / Fedora Project** | 发行版社群 | 社区发行版治理与上游集成 |
| **Open Container Initiative（OCI）** | 容器标准 | runtime/image/distribution 规范 |

2026 年 Linux Foundation 还公开宣布由 Anthropic、AWS、GitHub、Google、Google DeepMind、Microsoft、OpenAI 等共同投入 1,250 万美元支持 Alpha-Omega 与 OpenSSF 的开源安全工作。这是“**商业巨头使用开源，同时反向投资公共安全基础设施**”的典型模式。

## 14.9 量化科技：机构、研究平台与基础设施

| 类型 | 主体 | 可公开核实 | 本件学习点 | 不可越界 |
|---|---|---|---|---|
| 国际系统化量化 | Renaissance Technologies | Linux/HPC/Slurm/PostgreSQL/高规模研究基础设施的公开招聘与官网线索 | research→production 分离、冗余、数据工程 | alpha、仓位与执行参数 UNKNOWN |
| 国际量化/做市 | D. E. Shaw / Two Sigma / Citadel Securities / Jane Street / XTX / HRT / Jump / Optiver / IMC / Tower / WorldQuant / Man AHL / Winton / QRT | 公司存在与技术招聘公开 | point-in-time、低延迟、风险限额、研究工程化 | 不据招聘页猜真实 alpha |
| 中国量化 | **灵均投资** | 官网：100,000+ 数据种类、10PB+ 存储；量化选股/指数增强/多空/中性 | 大规模数据治理、策略组合、算力持续投入 | 数字为官网自报；生产拓扑 UNKNOWN |
| 中国量化 | **明汯投资** | 官网：数据挖掘、统计分析、技术研发；ML/DL 与量化；多策略 | AI/统计/工程联合；多策略平台 | 内部特征、交易算法 UNKNOWN |
| 中国量化 | **幻方量化 / High-Flyer** | 官方：全球量化投资管理；公开历史与 AI 投研路线 | AI/HPC 与量化交叉、研究平台化 | 不把 DeepSeek 模型栈等同量化实盘栈 |
| 中国量化 | **聚宽投资** | 官网：P1066435；大数据+量化+AI；因子→模型→优化→决策 | 分层投研工作流、AI 自主投研 challenger | 不把宣传语当投资绩效证明 |
| 量化研究平台 | **JoinQuant 聚宽** | 数据、研究、回测、社区/工具生态 | 教学/研究/原型、point-in-time/回测纪律 | 平台回测 ≠ 实盘收益 |
| 开源量化 | QuantConnect / LEAN、Backtrader、Zipline、vectorbt、Qlib | 研究/回测框架 | 可复现实验、策略接口、基准 | 生产交易仍需券商/OMS/风控 |

**统一验证协议**：

```text
idea
→ point-in-time dataset
→ research
→ purged/embargo CV
→ CPCV/PBO/Deflated Sharpe
→ transaction-cost / slippage stress
→ paper/shadow
→ risk-approved production
```

这条研究纪律可以迁移到博彩风险模型，但**交易 alpha 目标函数不能迁移成“诱导玩家输钱”目标**。

## 14.10 国家安全、公安、国防与宇航科技生态产业链

> 本节只登记**公开、合法、防御性、科研、工程治理与商业技术导入**。不推断机密网络拓扑，不提供攻击、监控滥用或武器运用流程。

### A. 国家安全 / 密码 / 网络安全科研链

| 国家/地区 | 公开组织 | 公开技术方向 | 可迁移方法 |
|---|---|---|---|
| 美国 | **NSA Research / NIST / CISA / National Labs** | 密码数学、数据科学/ML/图分析、可信软硬件、PQC、网络安全标准 | crypto-agility、formal methods、zero trust、标准化 |
| 台湾 | **国家资通安全研究院 NICS** | ZTA、AI 系统安全评测、威胁情资、供应链安全；2026 与中科院 MOU | 公私联防、供应链、AI for Cybersecurity |
| 澳大利亚 | **ASD / ACSC** | ISM、Essential Eight、安全云与国家网络防护 | control baseline、risk acceptance |
| 新加坡 | **CSA / GovTech** | secure-by-design、AI/agentic AI security、量子安全迁移 | 生命周期安全、政府数字平台治理 |
| 马来西亚 | **CyberSecurity Malaysia / MIMOS** | 国家网络安全能力、应用研发、AI/半导体/数字技术 | 本土研发、检测认证、数据主权 |

### B. 公安 / 公共安全科技链

| 组织 | 公开方向 | 本件边界 |
|---|---|---|
| 中国公安部第一研究所、网络安全保卫局等 | 国家网络身份认证公共服务标准、身份信息处理、认证因子、密码/网络/数据安全 | 只迁移身份认证、最小披露、审计、取证/标准化思路 |
| 公安部第三研究所等科研力量 | 网络安全、检测、培训、标准/研究 | 不推断未公开侦查手段或监控能力 |
| INTERPOL / Europol Innovation Lab 等国际协作 | 数字犯罪、取证、AI/网络安全协作 | 仅高层治理与证据链方法 |

截至 2026 年，公安标准化平台显示 `GA/T 2366-2025` 与 `GA/T 1723.1-2025` 已发布并于 2026-05-01 实施，起草单位包括公安部第一研究所、公安部网络安全保卫局与中国标准化研究院。对本项目真正可迁移的是**身份、认证、最小必要数据与审计链**，而非执法权限。

### C. 国防科技 / 商业技术导入链

| 体系 | 代表组织 | 模式 |
|---|---|---|
| 美国 | **DoD CDAO / DIU / DARPA / Service Labs** | 政府定义任务、安全与责任；商业公司提供 AI/ML、autonomy、cyber、human systems、space 等成熟/原型技术 |
| 英国 | **Dstl / MOD** | 公务科学家 + 大学 + 产业 + 商业云/承包商 |
| 台湾 | **国家中山科学研究院 NCSIST + NICS** | 国防科研 + 资安科研协作；零信任/AI 系统安全/关键基础设施 |
| 澳大利亚 | **DSTG / ASD** | 国防科研 + 国家网络安全 + 产业合作 |
| 新加坡 | **DSTA / DSO** | 国防工程、数字/AI、系统集成与科研 |
| 马来西亚 | **STRIDE / MIMOS 等** | 国防研究与国家应用研发的相邻生态；具体敏感能力不推测 |

### D. 宇航 / 空间科技链

| 体系 | 主体 | 公开强项 |
|---|---|---|
| 美国 | **NASA / JPL / SpaceX / Blue Origin / Rocket Lab** | 任务软件、自治、机器人、高性能空间计算、商用发射/卫星 |
| 欧洲 | **ESA / CNES / DLR / Airbus / Thales Alenia Space** | 科学任务、卫星、地面段、可靠工程 |
| 中国 | **CNSA / CASC / CASIC / 中科院相关院所** | 航天工程、卫星、数字化、科研 |
| 日本 | **JAXA** | 科学/载人/深空/可靠任务系统 |
| 印度 | **ISRO** | 卫星、发射、深空任务 |
| 马来西亚 | **MYSA** | 国家空间政策、遥感/卫星数据、空间技术研发 |
| 台湾 | **TASA** | 太空科技、卫星研发与产业生态 |

JPL 公开把**自治系统与 AI、高性能空间计算、量子感测与通信、大数据分析**列为未来能力，并强调 radiation-hardened computing、机器人、异构 CPU/GPU/DSP 与可验证软件。这类系统真正适合迁移到 GDI-OS 的，是 **FDIR、worst-case thinking、deterministic fallback、回放、健康监测、自治的安全边界**。

## 14.11 前沿科技产业链总图

```text
[基础科学/标准]
NIST | NSA Research | CAS | universities | national labs
        ↓
[芯片IP / EDA / 制造]
Arm | Synopsys | Cadence | ASML | TSMC | Samsung | Intel
        ↓
[计算 / 存储 / 网络]
NVIDIA | AMD | Phison | SK hynix | Micron | Broadcom | Arista
        ↓
[服务器 / OS / 云 / 容器]
HPE/Dell/Lenovo/Supermicro
Linux/Windows → AWS/Azure/GCP/Alibaba/Tencent/Huawei
Kubernetes/OpenShift/OpenStack
        ↓
[数据 / AI / 模型]
Kafka/Flink/Spark/Iceberg/StarRocks/ClickHouse
PyTorch/JAX/TensorFlow/XGBoost
OpenAI/Anthropic/DeepMind/DeepSeek/Meta
        ↓
[安全 / 密码 / 治理]
Zero Trust | IAM/PAM | KMS/HSM | TEE
SBOM/SLSA/Sigstore | PQC | SIEM/EDR/DLP
        ↓
[行业]
量化 | 银行 | 博彩 | 公安/公共安全 | 国防 | 宇航 | 医疗/BCI | 科研
        ↓
[验证]
IQ → OQ → PQ → MQ
sealed holdout → shadow → human review → controlled production
```

**最强的产业链不是“一个公司全包”，而是每层有替代、接口有标准、数据有边界、身份和密钥可独立控制、失败时有降级路线。**

---


# 15. 最新 `Inteligent…qmd` 新增主体补录

V3.1 已覆盖博彩、金融、银行、资安、电商、科研、宇航、量化、彩票、体育等大量主体；最新源件新增/强化的跨行业主体如下：

| 类别 | 主体 | 本件纳入方式 |
|---|---|---|
| 超大规模云 | AWS | 云/政府/宇航实例；不等同操作系统 |
| 超大规模云 | Microsoft Azure | Azure Government / Secret、Windows/AD 生态 |
| 超大规模云 | Google Cloud | 数据/AI/Kubernetes、DoD/NASA/空军案例 |
| 中国云 | Alibaba Cloud | 中国/亚洲企业云基准 |
| 中国云 | Tencent Cloud | 游戏/媒体/中国云基准 |
| 中国云 | Huawei Cloud | 电信/政企/AI/国产生态 |
| 低价云 | Hetzner | 成本基准；不与涉密 hyperscaler 直接等同 |
| 低价云 | Contabo | 大内存低价基准；关键负载需冗余 |
| 宇航科技 | SpaceX / Starlink | 遥测/SRE/快速迭代方法；内部安全栈不臆测 |
| 汽车/AI | Tesla | 车端软件、数据闭环方法论；内部服务器细节 UNKNOWN |
| AI 平台 | OpenAI | 企业 AI/模型服务基准；内部保密架构不臆测 |
| AI 平台 | Anthropic | 企业 AI/模型安全基准；内部保密架构不臆测 |
| 量化 | Renaissance Technologies | Linux/HPC/Slurm/PostgreSQL/研究—生产纪律的公开招聘线索 |
| 英国国防科研 | Dstl | “政府科学家 + 产业 + 大学”混合模式 |
| 台湾国防/科研 | 公开国防创新与产业体系 | 只迁移商业技术导入、人在回路、数据分级，不迁移武器逻辑 |
| RTOS | Green Hills / Wind River / Lynx / QNX | 安全关键系统对标 |

---


## 15.1 本轮新增主体登记（按原分类补录）

| 类别 | 主体 | 正本口径 | Evidence × Maturity |
|---|---|---|---|
| 半导体/存储 | **群联电子 Phison** | NAND 控制/SSD + Pascari/aiDAPTIV/AI Data Platform；性能需独立 benchmark | P1·M4/M5 |
| AI算力 | **AMD** | Instinct + ROCm 10 + CPU + SEV-SNP | P1·M5 |
| AI算力 | **辉达/英伟达 NVIDIA** | CUDA + Hopper/Blackwell/Vera Rubin + 网络 + Confidential Computing | P1·M5 |
| 汽车/AI | **Tesla** | 2026 官方披露 Cortex 2 已运行训练工作负载；Dojo 3 开发中 | P1·M4/M5 |
| 脑机接口 | **Neuralink** | N1/R1/BCI 临床研究；不是神经网络框架 | P1·M2/M3 |
| 开源治理 | **Linux Foundation / OpenSSF / CNCF / CCC / PQCA / SPDX / OpenChain** | 礼逆袭与云原生/供应链/机密计算/PQC 公共基础设施 | P1·M5 |
| 中国量化 | **灵均投资** | 100k+ 数据种类、10PB+ 存储等为官网自报；策略类型公开 | P1·M5（机构）；内部技术细节 UNKNOWN |
| 中国量化 | **聚宽投资** | 大数据+量化+AI；因子→模型→优化→决策；P1066435 为官网披露 | P1·M5（机构） |
| 量化研究平台 | **JoinQuant 聚宽** | 数据/研究/回测平台；与聚宽投资分开 | P1·M5 |
| 中国量化 | **明汯投资** | 数据挖掘/统计/AI/ML/DL 与量化；公开多策略产品 | P1·M5（机构） |
| 中国量化/AI | **幻方量化 / High-Flyer** | 量化机构；AI/HPC 历史值得研究，生产 alpha 不公开 | P1·M5（机构） |
| 前沿AI | **DeepSeek** | 单独作为模型/研究生态登记，不以“量化同源”推导生产栈 | P1·M4/M5 |
| 国家安全科研 | **NSA Research / NIST** | 密码数学、AI/数据科学、可信系统、PQC/标准 | P0/P1·M5 |
| 公安/公共安全 | **公安部第一研究所 / 网络安全保卫局等** | 网络身份认证、信息处理、标准与网络安全；不推断敏感侦查能力 | P0/P1·M5 |
| 台湾资安/国防科研 | **NICS / NCSIST** | 2026 MOU：ZTA、AI系统安全、关键基础设施、情资与国防科研协作 | P1·M4/M5 |
| 美国国防创新 | **CDAO / DIU** | 商业技术导入 AI/ML、autonomy、cyber、human systems、space | P1·M5 |
| 宇航科研 | **NASA/JPL** | autonomy/AI、机器人、高性能空间计算、量子/大数据 | P1·M4/M5 |
| 马来西亚科研 | **MIMOS** | 国家应用 R&D 中心；半导体、5G/AI、产业设施与 IP | P1·M4/M5 |
| 马来西亚宇航 | **MYSA** | 国家空间政策、遥感/卫星数据与空间科技 | P1·M5 |

---

# 16. 博彩与在线百家乐：完整主体以 V3.1 登记册为基础


## 16.1 本轮用户指定博彩/娱乐主体身份解析

| 用户给名 | 当前可解析对象 | 证据状态 | 正本处置 |
|---|---|---|---|
| **凯盛娱乐** | 公开网络存在多个相近中文/拼音主体；本轮未取得足以锁定同一公司的“公司注册主体 + 官方域名 + 监管牌照”三锚 | **P3 UNKNOWN** | **只保留候选名，不写股东、牌照、AI能力或市场份额；不得与“凯时/Kaishi”等相近名自动合并** |
| **劲博** | 可能指 **JBO** 在线体育/娱乐品牌；但本轮未取得一手证据证明“劲博”是 JBO 的唯一/正式中文法定别名 | **P3 identity unresolved** | JBO 可单独登记为在线投注/娱乐候选平台；`劲博 ↔ JBO` 关系待牌照/公司文件闭环 |
| **开云** | 搜索结果混有“开云体育/Kaiyun”站点、镜像/推广站及同名主体；同时“开云集团/Kering”是法国奢侈品集团，二者完全不同 | **P3 UNKNOWN** | 建 `entity_alias` + domain + legal_entity + license_registry；闭环前不写“顶级”“持牌”或技术能力 |

**Identity Resolution Gate**：

```text
brand_name
+ official_domain
+ legal_entity
+ regulator/license_number
+ corporate_registry / audited filing
--------------------------------------
≥ 3 independent anchors agree
→ identity_resolved = TRUE
否则保持 UNKNOWN
```

这三项的最大风险不是“漏掉一家”，而是**把克隆站、代理站、同名集团或营销 SEO 页面并成同一个法律主体**。


本件继承 V3.1 的主体登记册，包括但不限于：

- Evolution / Ezugi
- Playtech Live / BetBuddy / Playtech Protect
- Pragmatic Play Live
- SA Gaming / Dream Gaming / WM Casino / WM Perfect / Asia Gaming / AllBet / Sexy Baccarat / Pretty Gaming / Venus / Big Gaming / eBet / BetGames.TV / KingMaker
- Octane Studios / Sentient Studios / Sentient Gaming Group / SkyGaming / BetConstruct KISS AI / Winfinity / Angel Group / IDX Games / Arb Labs / Avanti
- Entain / Flutter / FanDuel / PokerStars / Sportsbet / Betfair / FDJ UNITED / Unibet / BetMGM / DraftKings / Sisal / OPAP / Stake / BC.Game / 1xBet / Dafabet / bet365 / 888.com / Caesars / Rivalry
- SOFTSWISS / EveryMatrix / Smartico / Optimove / GiG / NuxGame / Future Anthem
- Visa/Featurespace / SEON / GeoComply / Sumsub / Onfido / Jumio / Veriff / iDenfy / Shufti / Sift / Group-IB / Flagright / ComplyAdvantage / NICE Actimize / Quantexa
- Mindway AI / Neccton / Sportradar Bettor Sense
- Genius Sports / Sportradar / Kambi / Stats Perform / IMG ARENA / SIS / Oddin.gg / OpenBet
- Brightstar Lottery / Scientific Games / Pollard Banknote / IWG / Intralot / AGTech / NeoPollard / Allwyn / FDJ UNITED / Lotto NZ
- Palantir / Airbus / Boeing / Lockheed Martin / Anduril / Thales / Eutelsat / C3 AI / Oracle / SAP / Snowflake / Databricks / Microsoft / AWS / Google Cloud / NVIDIA / TSMC / CrowdStrike / Palo Alto / Citadel / Jane Street / Two Sigma
- FPLAY / Mysports.AI / Oracle Baccarat Predictor / BACC.BOT / BaccaratAI 等仅进入防御威胁模型

**主体出现 ≠ 推荐 ≠ 已部署 ≠ 能力被证明。**

---

# 17. 跨行业迁移矩阵

| 来源行业 | 可迁移 | 不可照搬 |
|---|---|---|
| 量化/HFT | point-in-time、purge/embargo、CPCV/PBO、尾延迟、risk limits | alpha/玩家剥削目标 |
| 银行 | MRM、reject inference、AML、case workflow、entity resolution | 银行授信阈值 |
| 电商 | CUPED、实验、feature store、推荐 | 用脆弱性提高投注 |
| 资安 | Detection-as-Code、Sigma/MITRE、UEBA、zero trust | 把普通客户当“敌人” |
| 科研 | 预注册、负控、E-value、复现 | 过慢流程全部照抄 |
| 制药 | ALCOA+、IQ/OQ/PQ、FMEA | 不能冒充博彩法规 |
| 宇航 | FDIR、回放、故障隔离、worst-case | 航天认证成本直接照搬 |
| 军事运筹 | constrained allocation / MHT 数学 | 武器/目标逻辑 |
| SRE | SLO、error budget、backpressure、chaos | 无边界自动化 |
| 密码学 | key lifecycle、HSM、crypto-agility、PQC | 自创算法 |
| 隐私工程 | DP、tokenization、purpose limitation | “合成数据 = 自动匿名” |

---


## 17.1 本轮新增迁移源

| 来源行业/生态 | 可迁移到 GDI-OS / 研究底座 | 不可照搬 |
|---|---|---|
| 半导体/AI算力 | heterogeneous compute、benchmark、memory hierarchy、TEE、供应商多样化 | “最新 GPU = 模型一定更好” |
| NAND/存储 | hot/warm/cold tier、local-AI、KV/cache/数据驻留、endurance/SLA | 用 SSD 扩内存就宣称等同 HBM |
| 开源基金会 | 多方治理、SBOM、供应链安全、security response、标准接口 | “开源 = 自动安全/免费运维” |
| 中国/国际量化 | research→production、point-in-time、组合/风险、HPC、可复现 | 私有 alpha、延迟参数、资金目标 |
| 脑机接口/医疗 | high-sensitivity data governance、human subject safety、device/software co-validation | 神经数据用于玩家营销或风险画像 |
| 国家安全科研 | 密码敏捷、formal methods、可信软硬件、零信任 | 机密任务、SIGINT/监控逻辑 |
| 公安/身份认证 | identity proofing、认证因子、最小数据、evidence chain | 执法权限或监控方法 |
| 国防创新 | commercial-to-government qualification、system safety、human control | 武器目标/作战流程 |
| 宇航 | FDIR、rad-hard thinking、autonomy guardrails、replay、verification | 极端认证成本无脑复制 |
| 前沿AI实验室 | eval、agent sandbox、tool permission、model/system card | 让通用 agent 直接拿生产 root 权限 |


# 18. RedTeam

1. 旧版指纹被当成最新版；
2. 厂商营销被写成“官方部署”；
3. 云平台获某授权被偷换成“所有服务自动合规”；
4. AWS/GCP/Azure 被误写成操作系统；
5. RHEL/Ubuntu/Debian 被误写成同一生命周期；
6. “Linux 开源”被误写成“天然安全”；
7. “Windows 商用”被误写成“不安全”；
8. “国产”被误写成“从零自研”；
9. “政府采购”被误写成“政府不做研发”；
10. RTOS 与通用 OS 做“高级/低级”排名；
11. 气隙被当成终极安全；
12. HSM/KMS 被当成“密钥永不会泄露”；
13. confidential computing 被当成绝对保密；
14. root/admin 长期常驻；
15. 云 egress 未限制；
16. 生产数据复制到测试线；
17. 外部 AI 接触生产原始数据；
18. 合成数据保留真实罕见记录；
19. Membership Inference 成功但仍宣称“匿名”；
20. 只报 AUC，不报 precision@capacity / calibration；
21. Transformer-first；
22. RL reward 用 GGR/NGR/投注额/时长；
23. RG 风险回流营销；
24. 高影响动作无人复核；
25. 依赖没有 SBOM；
26. 不可复现环境；
27. 没有时钟/时区/DST 纪律；
28. 没有不可变审计；
29. 云账单没有预算与配额；
30. 低价 VPS 单机被当高可用；
31. 单云/单区/单 KMS 成为单点；
32. 历史/文化材料混入工程事实。
33. 以根 CA 存在推断「厂商总部正在读全部 HTTPS 明文」；
34. 把 Defender Network Protection 的 TLS/FQDN 检查与 Kaspersky TLS 内容解密混为一谈；
35. 单次 Browser/App Speedtest 差异未经同节点重复，就直接归因安全软件；
36. 为提高测速分数擅自关闭组织管理的 AV/EDR/DLP。

---


### 18.1 本轮新增 RedTeam

37. 把 **Neuralink** 错写成“神经网络框架”，进而把脑机接口临床研究能力套进普通 AI 软件；
38. 把 Phison `aiDAPTIV` 厂商 benchmark 直接写成所有 LLM/所有 SSD/所有 GPU 的通用性能事实；
39. 把 CUDA 生态领先偷换为“AMD/ROCm 不可用”，或反过来以“开源”偷换成“ROCm 全面等价 CUDA”；
40. 把某基金官网写的存储/数据规模当成其真实 alpha 或业绩证明；
41. 把 JoinQuant 社区回测策略当作聚宽投资生产策略；
42. 把 High-Flyer 与 DeepSeek 的历史关联偷换成“同一套生产服务器/同一套模型/同一套数据”；
43. 把“凯盛/劲博/开云”同名或镜像站 SEO 结果直接合并成一个法律主体；
44. 把国家安全/公安/国防/宇航机构的公开研究方向外推成未公开生产部署；
45. 把“国防采用商业技术”偷换成“商业产品默认达到机密级”；
46. 把 Linux Foundation 生态中的一个项目漏洞外推成“礼逆袭整体不安全”，或把 Linux 开源外推成“整体绝对安全”；
47. 把 AI Agent 的工具连接能力当成无需 IAM/PAM/审批的自动授权；
48. 只追求 GPU FLOPS，忽略 VRAM/HBM、网络、CPU、storage、data-loader、checkpoint、功耗和软件兼容造成的系统瓶颈。


# 19. Critic

- **“商用版更强”不是普遍真理。** RHEL 的价值在支持/生命周期/认证；Debian 在自由度、稳定和成本上可能更优。
- **“免费版更便宜”也不一定。** 若缺人力，社区版的隐性运维成本可能大于订阅。
- **Windows 与 Linux 并非互斥。** 最现实是 Windows 工作站 + Linux 服务器/WSL/容器。
- **Mac 不适合替代一般服务器，但在 Apple 构建链无可替代。**
- **Hyperscaler 不等于自动安全。** 云厂商负责云“的安全”，客户仍负责云“中的安全”。
- **国家级认证不等于某个客户已安全部署。** 系统仍需自己的 ATO/风险接受。
- **PQC 不是“量子电脑已破解现有密码”。** 是提前迁移与密码敏捷性。
- **所有操作系统都存在 CVE。** 安全来自配置、补丁、身份、最小权限、供应链、监控与治理的组合。
- **“所有 Linux 发行版”不应理解为把 Distrowatch 每个 fork 都塞进生产白皮书。** 工程上应按家族、生命周期、认证、支持、包管理、内核、硬件与业务适配评价。
- **Speedtest 是诊断，不是取证。** 单次吞吐差只能立假说；须 exact server、交错重复、证书链与进程/过滤追踪后才谈根因。
- **HTTPS inspection 是本机安全机制时，不等于远端组织取得明文。** 必须分别证明本机解密、遥测上传、远端可见字段三条链。
- **Renaissance 的低公开度不能被当成高安全的直接证据。** 保密文化与可公开验证的密码工程是不同维度。

---


### 19.1 本轮 Critic 补强

- **“顶级科技公司”不是一个同质类别。** Phison 的核心是存储、AMD/NVIDIA 是计算平台、ASML 是设备、TSMC 是制造、Linux Foundation 是治理、Neuralink 是医疗/BCI；必须按供应链层评价。
- **AI 算力不是模型治理替代品。** GPU 更强不能修复 label leakage、time leakage、selection bias、bad reward 或缺少 OOT。
- **量化公司的官网只能证明它愿意公开什么。** 公开的“10PB”“AI投研”“机器学习”可作基础设施/研究方向证据，不能作为收益、alpha 或生产安全的独立证明。
- **BCI 是高敏感医疗数据，不是更高级的用户画像。** 对普通商业系统最值得迁移的是 consent、purpose limitation、safety case 和最小权限。
- **国家科技生态的先进性来自组合制度。** 政府研究院、大学、承包商、开源与商业科技长期共存；“全部自研”与“全部外购”同样是错误二分。
- **身份解析是博彩对标的前置门。** 若连法定主体都没有锁定，后续牌照、股东、AI、市场份额比较全是伪精确。


# 20. KillCritic：一票否决

任一成立，不得把系统称为“生产级/国家级/世界级”：

1. 未知版本/未打补丁；
2. root/admin 密码共享；
3. 无 MFA；
4. 生产数据库可直接公网访问；
5. 密钥写进源码/Notebook；
6. 无最小权限；
7. 无备份恢复演练；
8. 无异地/跨故障域设计；
9. 无审计日志；
10. 日志可被同一管理员静默删除；
11. 无 SBOM / 依赖版本；
12. 生产数据送外部 AI；
13. 测试环境带完整真实 PII；
14. 无 DLP / egress 控制；
15. 合成数据未做隐私攻击测试；
16. 模型无 OOT / shadow；
17. 高影响决定无人复核；
18. RL 可直接触发高影响动作；
19. RG 数据用于营销；
20. 把厂商“支持某标准”写成“本系统已合规”；
21. 把云服务认证写成“整个应用自动获认证”；
22. 把理论/科幻能力写进采购 SLA；
23. 把 RTOS/国防逻辑迁入玩家处置；
24. 无 deterministic fallback；
25. 无 replay/reconciliation；
26. 以单次测速或根证书存在指控特定公司/政府「远端解密全部数据」；
27. 未经授权关闭、卸载或绕过企业 AV/EDR/DLP/证书策略；
28. 把「公开证据评分」写成真实保密实力排行榜。

---


### 20.1 本轮新增一票否决

29. 把 `Neurolink`/Neuralink 当神经网络软件并据此设计生产 AI；
30. 凯盛/劲博/开云任一主体在 `identity_resolved = FALSE` 时仍写“官方牌照/老板/AI系统/市场份额”；
31. 量化机构官网自报规模未经口径标记就作为第三方独立事实；
32. AI/HPC 采购没有 CPU/GPU/VRAM/HBM/网络/存储/功耗/软件版本联合 benchmark；
33. GPU/SSD 固件、驱动和 ROCm/CUDA 版本未锁定；
34. Agent 能访问生产数据却没有 tool allowlist、JIT 权限、审批和完整审计；
35. 训练/推理的敏感数据在共享 GPU/云租户环境没有明确隔离与密钥控制；
36. BCI/医疗神经数据被用于博彩营销、个体诱导或非原目的画像；
37. 以“国家安全/公安/国防/宇航”为名把未经授权的敏感能力、攻击逻辑或监控需求塞进商业 GDI-OS；
38. 开源依赖没有 upstream/source/signature/SBOM provenance，却仅因“来自 GitHub”就视为可信。


# 21. Blindspot

- UEFI/固件/BMC 供应链；
- TPM/HSM 固件更新；
- CPU 微码与 speculative execution 漏洞；
- GPU/加速卡固件；
- container escape；
- hypervisor escape；
- SaaS 管理员与供应商支持通道；
- 域名/DNS/证书供应链；
- NTP/PTP/时钟漂移；
- 备份密钥与灾备账户；
- 影子 IT；
- 浏览器扩展；
- AI Agent 工具调用权限；
- MCP/插件 OAuth 权限；
- 数据驻留与跨境；
- egress cost 与 egress exfiltration；
- 低价 VPS noisy neighbor；
- GPU 云的多租户隔离；
- post-quantum migration 中的混合协议互操作；
- “厂商锁定”与“自建运维地狱”之间的双向风险；
- 人工审核产能是真正的系统瓶颈；
- 标签治理仍是 AI 风控最大盲点之一。
- 端点安全叠层（primary AV / passive EDR / DLP / WFP）角色若不清，性能结论会被混杂；
- 根证书安装状态与「当前站点实际被 TLS interception」之间存在证据断层；
- Browser/App 测速若不锁 exact server、协议与顺序，结果不可用于因果归因；
- 高保密机构往往公开信息最少，故「公开证据覆盖」与「真实能力」天然存在反向偏差。

---


### 21.1 本轮新增盲点

- GPU/AI accelerator 的固件、driver、runtime、collective library 与模型框架形成新的四层兼容矩阵；
- SSD 作为 AI memory tier 时必须同时看 endurance、write amplification、latency tail、checkpoint/recovery，而不只看“可运行更大模型”；
- HBM/NAND/先进封装供应集中度会把“软件选型”变成供应链风险；
- confidential computing 的 TEE 不保护所有侧信道、错误配置与授权后的合法滥用；
- 开源基金会治理成熟不等于每个下游 fork 都维持同等级安全；
- 量化机构的 survivorship、capacity、market impact、transaction cost 与 regime drift 无法从官网技术页得出；
- 中国量化主体的中文简称、基金管理人主体、香港/境外关联实体必须分开；
- 博彩品牌跨法域常有 skin、white-label、affiliate、mirror domain；品牌名不是法律实体；
- 公安/国安/国防/宇航公开资料有天然 information asymmetry，“未公开”不能推导“没有”，也不能推导“一定有”；
- BCI 的长期生物兼容性、植入风险、算法更新、device cybersecurity 与 consent 都必须与 AI 模型指标分开；
- AI Agent / MCP / Plugin 让“模型安全”扩展成“身份 + 工具 + 数据 + 网络 + 审批”系统安全问题。


# 22. Cheatsheet

| 问题 | 默认答案 |
|---|---|
| 本机开发 | Windows 11 Pro + WSL2/Linux VM |
| 生产服务器 | RHEL / Ubuntu LTS / Debian / SLES，按认证与预算选 |
| 低成本测试 | Hetzner / 本地虚拟化 / 合规前提下的普通云 |
| 受监管 | RHEL/SLES/Windows Server + hyperscaler/private cloud + 明确控制矩阵 |
| 高保密 | 专用账户/区域/网络 + KMS/HSM + egress deny + JIT + immutable audit |
| AI 数据 | 最小化、脱敏、purpose-bound |
| 合成数据 | 可研发/压测；不能单独证明真实效果 |
| 模型首选 | GLM/GBDT baseline |
| Transformer | OOT 稳定增量后 |
| RL | OPE + safe actions + causal baseline + approval |
| 量化回测 | point-in-time + purge/embargo + CPCV/PBO |
| 密码 | 标准算法，不自创；建立 crypto inventory |
| PQC | ML-KEM / ML-DSA / SLH-DSA 进入迁移计划 |
| 高影响动作 | human review + appeal + rollback |
| 生产禁令 | 当前仍禁止连接旧/生产 Superset、StarRocks、DolphinScheduler、博彩站点 |
| Browser/App 网速差 | 固定 exact Ookla server，≥5 组交错 A/B；再做 Chrome/Edge/App 三角 |
| Kaspersky 根 CA | 只证明 TLS 检查**能力/信任链**；须看实际 issuer + scan mode 才能证明当次 interception |
| Defender `Normal` | Microsoft Defender Antivirus 主动模式；仍须确认第三方 AV 的 primary/实时角色 |
| 无 Proxy/PAC | 只排除显式代理；WFP/NDIS/VPN/透明网关/DLP 仍可能存在 |
| 保密「天下第一」 | 不做真实实力排名；只做公开证据覆盖评分，并显式列 UNKNOWN |

---


## 22.1 本轮速查表

| 问题 | 正本答案 |
|---|---|
| Phison 是什么？ | 群联电子；NAND/SSD/storage，并扩展 AI Data Platform/aiDAPTIV；不是 GPU 厂 |
| AMD 在 AI 栈定位？ | Instinct GPU + ROCm + EPYC + SEV-SNP；作为 NVIDIA challenger/异构算力 |
| NVIDIA 定位？ | CUDA/GPU/网络/AI平台/机密计算；“辉达/英伟达”均指 NVIDIA |
| Tesla 能否当云厂商？ | 不能；本件只把其 AI training/自研 silicon/车端闭环作为方法论来源 |
| Neuralink 是神经网络吗？ | **不是**；是脑机接口（BCI）公司/临床研究系统 |
| 灵均资本？ | 公开官网正名 **灵均投资** |
| 明竑？ | 正名 **明汯投资** |
| 聚宽是一个主体吗？ | 需分 **JoinQuant 研究平台** 与 **聚宽投资** |
| 幻方 = DeepSeek？ | 不能简单等号；分别登记量化机构与 AI 实验室/模型生态 |
| 凯盛/劲博/开云是什么？ | 身份尚未闭环；先 P3 UNKNOWN，禁止编牌照/股东/技术能力 |
| Linux 谁“拥有”？ | 没有单一商业公司“拥有整个 Linux”；内核社群 + Linux Foundation/开源基金会 + 各发行版/厂商共同生态 |
| 国家安全科技只靠公务员？ | 否；政府研究能力 + 国家实验室 + 大学 + 承包商 + 商业/开源技术的混合模式 |
| 公安科技可迁移什么？ | 身份认证、证据链、标准化、网络防御；不迁移执法权限或监控滥用 |
| 国防科技可迁移什么？ | qualification、系统安全、故障隔离、commercial tech infusion；不迁移武器逻辑 |
| 宇航科技可迁移什么？ | FDIR、自治 guardrail、回放、可靠性、worst-case、HIL/digital twin |


# 23. Blueprint：本项目最现实的计算底座

```text
[Windows 11 Workstation]
  BitLocker + 经组织批准的端点安全栈（一个 primary AV；其余按 passive/EDR/DLP 角色） + FIDO2 + WSL2
      │
      ├── R / Python / Quarto / Git
      ├── local DuckDB / Polars / Arrow
      └── isolated VM / container
               │
               ▼
[Test Line Linux Server]
  RHEL 10 / Rocky 10 / Ubuntu 26.04 LTS
  LUKS2 + Secure Boot + SELinux/AppArmor
  rootless Podman/Docker
  egress allowlist
  no production credentials
               │
               ▼
[Data Sandbox]
  synthetic + de-identified snapshots
  contracts + hashes + lineage + DQ
               │
               ▼
[Model Lab]
  GLM/GBDT → Survival/HMM → Graph → Sequence
               │
               ▼
[Artifact Registry]
  model + code + SBOM + seed + metrics + model card
               │
               ▼
[Sealed Real Holdout / Authorized Only]
               │
               ▼
[Shadow]
               │
               ▼
[Human Review]
               │
               ▼
[Controlled Production]
```

---


## 23.1 Blueprint：大秦赋算筹“六层科技生态 + 五道安全闸”

```text
L0 SCIENCE / STANDARDS
NIST | CAS | universities | national labs | LF/OpenSSF
        ↓
L1 SILICON / STORAGE / NETWORK
TSMC/Intel/Samsung | NVIDIA/AMD/Arm | Phison/HBM/NAND | Broadcom/Arista
        ↓
L2 SYSTEM / OS / CLOUD
HPE/Dell/Lenovo | Linux/Windows | AWS/Azure/GCP/Alibaba/Tencent/Huawei
        ↓
L3 DATA / AI / QUANT
Kafka/Flink/Iceberg/StarRocks/ClickHouse
R/Python/XGBoost/PyTorch/JAX
Quant funds / research platforms / frontier AI labs
        ↓
L4 SECURITY / PRIVACY
Zero Trust | IAM/PAM | KMS/HSM | TEE
SBOM/SLSA/Sigstore | PQC | DLP/EDR/SIEM
        ↓
L5 DOMAIN
gaming | finance | public safety | defense | aerospace | science | BCI

五道闸：
G1 ENTITY IDENTITY
G2 EVIDENCE × MATURITY
G3 DATA / PRIVACY / SECURITY
G4 MODEL / SYSTEM VALIDATION
G5 HUMAN / LEGAL / PRODUCTION APPROVAL
```

**供应商替代原则**：

```text
每个关键能力至少回答：
A. primary 是谁？
B. challenger 是谁？
C. open-standard / self-host fallback 是什么？
D. 数据和密钥能否迁走？
E. 失败时如何降级？
```


# 24. ActionPlan

## Phase A0 — 立即：源件与版本治理

- 冻结当前 7 件源文件实际 MD5；
- 把 V3.1 的旧 `Inteligent` 指纹标 `SUPERSEDED-SNAPSHOT`；
- 建 `source_registry`：filename / bytes / line endings / encoding / md5 / as_of / provenance；
- 将提问十四～卅五登记为 `EMPTY_PLACEHOLDER`，避免误以为已有研究结果；
- GitHub 技术来源与非技术历史材料分目录/分 manifest。

## Phase A1 — 本机计算环境

- Windows 11 保持日常桌面；
- 启用 BitLocker、TPM/Secure Boot、FIDO2/Passkey、最小管理员；
- WSL2 或 Linux VM 作为 Linux 兼容层；
- R / Python lockfile；
- Quarto/TinyTeX 分离；
- CycloneDX/SPDX SBOM；
- 定期离线备份 + 恢复演练。
- 用 Windows Security → Manage Providers + PowerShell 明确 `primary AV / passive EDR / DLP` 角色，**不以「都装了」推断「都主动」**；
- 建 `endpoint_security_registry`：provider / role / version / service / TLS-inspection-mode / root-CA-thumbprint / policy-owner / last-verified；
- 对 Browser/App 性能采用 §10.4 的 LO1→LO2→LO3 流程，不以一次测速调安全策略。

## Phase A2 — 测试专用服务器

优先顺序：

1. **RHEL 10 / Rocky 10**：若强调企业治理、SELinux、RHEL 兼容；
2. **Ubuntu 26.04 LTS**：若强调 AI/GPU/开发生态；
3. **Debian 13**：若强调稳定、自由与低成本；
4. **SLES 16**：若 SAP/欧洲企业生态；
5. Windows Server 2025 仅在 AD/.NET/SQL Server/Windows 服务为核心时优先。

## Phase A3 — 安全基线

- deny-by-default egress；
- RBAC/ABAC；
- JIT/JEA/PAM；
- KMS/HSM；
- secrets vault；
- immutable audit；
- EDR/XDR；
- SIEM；
- DLP；
- signed artifacts；
- SBOM；
- vulnerability SLA；
- backup/restore；
- incident playbook。
- 企业 TLS inspection 必须登记 CA、适用域、例外、负责人、日志字段与性能基线；
- 安全软件叠层必须做性能/兼容性基线，避免 primary AV 重叠或重复内容扫描；
- 禁止以测速为由擅自关闭受管理的 EDR/DLP/AV。

## Phase A4 — 数据与模型

- 先 `canonical_event_ledger`；
- 再 point-in-time features；
- 140 表 → 15 风险视图继续保留；
- `registry_risk_topology` 作为系统风险真相；
- baseline → challenger；
- IQ/OQ/PQ/MQ 四门；
- sealed real holdout；
- shadow；
- human review。

## Phase A5 — 云选择

### 若成本第一
Hetzner / 合适的本地服务器 + 开源栈。

### 若全球弹性/服务深度第一
AWS。

### 若 Microsoft 企业生态第一
Azure。

### 若数据/AI/BigQuery/GKE 第一
Google Cloud。

### 若极高合规/主权
先定司法辖区与控制矩阵，再在 AWS GovCloud / Azure Government / Google Public Sector / 私有云中选；**不是先选品牌再找理由。**

## Phase A6 — 后量子与长期保密

- 建 crypto inventory；
- 标记需保密 >10 年的数据；
- 规划 hybrid/PQC；
- 只采用 NIST/行业标准实现；
- 验证库版本、HSM/KMS 支持、协议兼容；
- 设 rollback 与 crypto-agility。

---


## Phase A7 — 本轮新增主体治理

1. 建 `entity_registry_v2`：
   - `canonical_name`
   - `aliases`
   - `entity_type`
   - `legal_entity`
   - `official_domain`
   - `regulator_or_registry`
   - `country_or_region`
   - `technology_domain`
   - `evidence_grade`
   - `maturity_grade`
   - `identity_resolution_status`
   - `last_verified_at`

2. 先处理四个名称冲突：
   - `灵均资本 → 灵均投资`
   - `明竑 → 明汯投资`
   - `Neurolink → Neuralink / BCI`
   - `开云体育 ≠ Kering 开云集团`

3. `凯盛娱乐 / 劲博 / 开云` 建立 **identity quarantine**；没有法定主体与牌照闭环前，不进入竞争力评分。

## Phase A8 — AI/HPC 硬件 Challenger Lab（仅测试线/模拟数据）

- NVIDIA CUDA baseline；
- AMD ROCm challenger；
- CPU fallback；
- 若采用 Phison aiDAPTIV/SSD-memory tier，单独测试：
  - tokens/s / latency p50/p95/p99；
  - VRAM/DRAM/SSD usage；
  - TBW / write amplification；
  - checkpoint/restart；
  - power；
  - model quality 是否完全一致；
- 固定 model / quantization / batch / context / driver / runtime / seed；
- 不用厂商 demo 数字直接写采购结论。

## Phase A9 — 开源供应链治理

- Linux kernel / distro / container / library 分层列 SBOM；
- OpenSSF Scorecard 只作线索，不作绝对安全分；
- artifact signing：Sigstore/cosign；
- provenance：SLSA；
- vulnerability intake：CVE/VEX；
- license：SPDX/OpenChain；
- upstream fork 差异必须有 patch manifest。

## Phase A10 — 国家级科技生态映射

分别维护：

```text
national_security_research_registry
public_safety_technology_registry
defense_innovation_registry
aerospace_science_registry
```

每条只允许登记：
`公开组织 → 公开任务 → 公开技术方向 → 可迁移工程模式 → 明确不可迁移边界`。

严禁用“机密所以我猜……”填 UNKNOWN。

## Phase A11 — 量化科技对标

- 国际组：Renaissance / D.E. Shaw / Two Sigma / Citadel / Jane Street / XTX / HRT / Jump / Optiver / IMC / Man AHL / Winton / QRT / WorldQuant；
- 中国组：灵均 / 聚宽投资 / 明汯 / 幻方；
- 平台组：JoinQuant / QuantConnect / Qlib 等；
- 指标禁止做“谁最好”排名，统一比较：
  - data lineage
  - research reproducibility
  - point-in-time
  - leakage control
  - CV/backtest rigor
  - transaction cost
  - capacity
  - deployment control
  - security/governance
  - disclosed vs UNKNOWN

---


# 25. 官方查证来源（截至 2026-09-30）

## 操作系统

- Microsoft Windows 11 Release Health  
  https://learn.microsoft.com/zh-cn/windows/release-health/windows11-release-information
- Windows Server 2025 — What's New  
  https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025
- Red Hat Enterprise Linux 10  
  https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux-10
- RHEL 10 Documentation  
  https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10
- Ubuntu 26.04 LTS Release Notes  
  https://documentation.ubuntu.com/release-notes/26.04/
- Debian Releases  
  https://www.debian.org/releases/
- Fedora Linux 44  
  https://fedoramagazine.org/announcing-fedora-linux-44/
- SUSE Linux Enterprise Server 16  
  https://www.suse.com/c/what-is-new-in-suse-linux-enterprise-server-16-0/
- Oracle Linux 10  
  https://docs.oracle.com/en/operating-systems/oracle-linux/10/
- Rocky Linux Releases  
  https://docs.rockylinux.org/releases/
- FreeBSD Releases  
  https://www.freebsd.org/releases/
- OpenBSD 7.8  
  https://www.openbsd.org/78.html
- Apple macOS 26 Tahoe  
  https://www.apple.com/newsroom/2025/09/new-versions-of-apples-software-platforms-are-available-today/

## 云/政府

- AWS GovCloud  
  https://aws.amazon.com/govcloud-us/
- AWS DoD IL5  
  https://aws.amazon.com/govcloud-us/dodsrg/
- Azure Government DoD  
  https://learn.microsoft.com/en-us/azure/azure-government/documentation-government-overview-dod
- Azure Government IL5  
  https://learn.microsoft.com/en-us/azure/azure-government/documentation-government-impact-level-5
- Azure Government national security / Secret  
  https://azure.microsoft.com/en-us/explore/global-infrastructure/government/national-security/
- Google Cloud DoD  
  https://cloud.google.com/gov/federal-defense-and-intel
- Google Cloud Government Customer Stories  
  https://cloud.google.com/gov/customer-success-stories
- Google Public Sector Secret/Top Secret authorization  
  https://cloud.google.com/blog/topics/public-sector/google-public-sector-achieves-top-secret-and-secret-cloud-authorization

## 安全/密码

- NIST SP 800-207 Zero Trust Architecture  
  https://csrc.nist.gov/pubs/sp/800/207/final
- NIST Post-Quantum Cryptography  
  https://csrc.nist.gov/projects/post-quantum-cryptography
- NIST PQC Publications / FIPS 203/204/205  
  https://csrc.nist.gov/Projects/post-quantum-cryptography/publications


## 端点安全 / TLS 检查 / Speedtest

- Kaspersky Endpoint Security 12.10 — Network settings / Encrypted connections scan  
  https://support.kaspersky.com/KESWin/12.10/en-US/178483.htm
- Kaspersky Endpoint Security — Scanning encrypted connections with an untrusted certificate  
  https://support.kaspersky.com/KESWin/11.11.0/en-US/229683.htm
- Microsoft Defender Antivirus — `AMRunningMode` / active mode  
  https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-antivirus-windows
- Microsoft Defender Network Protection — TLS handshake / FQDN inspection  
  https://learn.microsoft.com/en-us/defender-endpoint/network-protection
- Windows Security 与第三方防毒的角色说明  
  https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-defender-security-center/windows-defender-security-center
- Google Fiber — Use Speedtest by Ookla（桌面 App 与 Browser 准确性提示）  
  https://support.google.com/fiber/answer/13273666

## James Simons / IDA / Renaissance Technologies

- Simons Foundation — Jim Simons on his career in mathematics（1964 IDA / code breaking / cryptographic problems）  
  https://www.simonsfoundation.org/2012/09/28/simons-foundation-chair-jim-simons-on-his-career-in-mathematics/
- Simons Foundation — Remembering the Life and Careers of Jim Simons（NSA code breaker；2024-05-10 逝世）  
  https://www.simonsfoundation.org/2024/05/10/remembering-the-life-and-careers-of-jim-simons/
- IDA — Center for Communications and Computing（NSA-sponsored FFRDC；cryptology/cybersecurity/HPC）  
  https://www.ida.org/-/media/corporate/files/general/ccc_one-pager.ashx
- Renaissance Technologies — About（40 TB/day；>50,000 cores；>200 Gbps；冗余设施）  
  https://www.rentec.com/Home.action?about=true
- Renaissance Technologies — Security Engineer（firewall / AV-EDR / IDS-IPS / encryption / vulnerability / IAM / governance / IR）  
  https://www.rentec.com/Careers.action?jobs=true&selectedPosition=securityEngineer
- Renaissance Technologies — Systems Engineer（Linux / Slurm / LLM deployments / PostgreSQL 等）  
  https://www.rentec.com/Careers.action?jobs=true&selectedPosition=systemsEngineerEs

## 2026 前沿公开保密工程对标

- Signal — Sparse Post Quantum Ratchet / Triple Ratchet / formal verification in CI  
  https://signal.org/blog/spqr/
- Signal — Automatic Key Verification（2026-08）  
  https://signal.org/blog/automatic-key-verification/
- Cloudflare — Post-quantum cryptography（ML-KEM / ML-DSA；2029 路线）  
  https://developers.cloudflare.com/ssl/post-quantum-cryptography/
- Cloudflare — PQC product status（2026-09-16 更新）  
  https://developers.cloudflare.com/ssl/post-quantum-cryptography/pqc-cloudflare-products/
- Apple Platform Security（2026-03）  
  https://support.apple.com/guide/security/welcome/web
- Microsoft Secure Future Initiative — July 2026 Progress Report  
  https://www.microsoft.com/en-us/security/blog/2026/07/10/securing-our-future-july-2026-progress-report-on-microsofts-secure-future-initiative/

---


## 本轮新增官方/一手来源：半导体、AI、开源、量化与国家科研

### 半导体 / 存储 / AI算力
- Phison COMPUTEX 2026 — AI Enabler / Pascari aiDAPTIV / AI Data Platform  
  https://www.phison.com/phison-unlocks-a-full-scale-ai-deployment-across-industries-building-an-ecosystem-with-pascari-aidaptiv/
- Phison × Intel — Local AI / Core Ultra Series 3 / aiDAPTIV  
  https://www.phison.com/phison-collaborates-with-intel-to-bring-larger-local-ai-workloads-to-intel-ai-pc-platforms/
- AMD ROCm 10 Compatibility Matrix（2026-08-19）  
  https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html
- NVIDIA Confidential Computing  
  https://www.nvidia.com/en-us/data-center/solutions/confidential-computing/
- Tesla Investor Relations — 2026 Q1 supporting infrastructure（Cortex 2 / Dojo 3）  
  https://ir.tesla.com/

### 神经科技
- Neuralink — PRIME Study Progress Update  
  https://neuralink.com/updates/prime-study-progress-update/

### 礼逆袭 / 开源治理
- Linux Foundation — Open Source Security  
  https://www.linuxfoundation.org/
- OpenSSF  
  https://openssf.org/
- CNCF  
  https://www.cncf.io/
- Confidential Computing Consortium  
  https://confidentialcomputing.io/
- Linux Foundation 2026 Open Source Security Grants  
  https://www.linuxfoundation.org/press/linux-foundation-announces-12.5-million-in-grant-funding-from-leading-organizations-to-advance-open-source-security

### 量化科技
- 灵均投资  
  https://www.lingjuninvest.com/
- 聚宽投资  
  https://fund.joinquant.com/
- 明汯投资  
  https://www.mhfunds.com/
- High-Flyer Capital Management  
  https://www.highflyercapital.com/

### 国家安全 / 公安 / 国防 / 宇航科研
- NSA Research — Overview  
  https://www.nsa.gov/Research/Overview/
- 公安部公安标准化信息服务平台 — GA/T 2366-2025 / GA/T 1723.1-2025  
  https://ywtb.mps.gov.cn/gabzh/
- 台湾国家资通安全研究院 NICS — AI for CyberSecurity  
  https://www.nics.nat.gov.tw/
- Defense Innovation Unit — Commercial Solutions Catalog  
  https://www.diu.mil/solutions/portfolio/catalog
- NASA JPL — Autonomous Systems & Artificial Intelligence  
  https://www.jpl.nasa.gov/about/strategic-implementation-plan/capabilities/2/
- NASA JPL — High-Performance Space Computing  
  https://www.jpl.nasa.gov/about/strategic-implementation-plan/capabilities/8/
- Malaysia MIMOS — National Applied R&D Centre  
  https://www.mimos.my/


# 26. 继承之白皮书正文（v3.0.0 主体 + v3.1.0 增量层）

> **斧正 C-DAQIN-04 / C-DAQIN-05（本轮）**
>
> 1. **章名更正**：原名「继承的 V3.1 正文」，但本章内嵌正文自称 v3.0.0（见下方 §26.0b 标题行），v3.1.0 仅为其增量层（§26.21）。章名已按实物更正，正文一字未动。
> 2. **标题层级更正**：原章内 72 个标题为顶层 `#`，与本件 §1～§28 之 `# 1.`～`# 21.` **逐一碰撞共 42 处**；在 `number-sections: true` 下必致全件编号错位。现整体降一级并重编号为 `26.N[.M]`。
> 3. **交叉引用读法**：本章内原文所称「见 §N」「见 §21.5」，在本件应读作 **「见 §26.N」「见 §26.21.5」**。
> 4. 本章内容**零删减**。

> 以下保留当前 `Whitepaper-Perfect-Baccarat-AI-Quant-Governance-V3-1-0.md` 的完整技术正文，作为本总纲的**继承层**。但其 §0.1 关于 `Inteligent_egaming_platform_ref` 的指纹已经被本件 C-DAQIN-01 标记为旧快照；其余冲突仍按 V3.1 自身 C-01～C-32 与本件新增 C-DAQIN 系列解释。



## v3.1.0 增量签发说明（2026-09-29）

> 本文件完整保留其后 `v3.0.0` 父版正文，并在末尾追加 §21。当前解释冲突以 §21 的 C-17～C-32 为准；父版不静默改写。

## 完美真人百家乐 AI × 量化科技 × 安全治理白皮书 v3.0.0

> **副标题**：Baccarat-Core Gaming Decision Intelligence Operating System（GDI-OS）  
> **范围**：完美真人 / WM Perfect 为核心研究对象；体育博彩、彩票/iLottery 为相邻垂直；金融、银行、资安、电商、科研、宇航/安全关键系统为方法论迁移来源  
> **as-of**：2026-09-28  
> **版本原则**：**只增不减；保留已成立内容；纠错只降低错误主张，不删除历史台账；UNKNOWN 不以推测填空。**  
> **现行工程边界**：不连接/不实测 Superset、DolphinScheduler、StarRocks、生产博彩站点；不把生产原始数据提交外部 AI。仅做离线、脱敏/模拟数据、代码与架构审查，以及经正式授权的测试线工作。  
> **性质**：研究、架构、采购尽调与治理白皮书；不是牌照意见、法律意见或任何公司未公开生产能力的证明。

---

### 26.0 本版为什么是“强化版”而不是重写版

v3.0.0 同时继承并上收以下资产：

1. v1.0.0 移植总表的 **70 主体 + 9 类监管/标准体系、M-1～M-11、SC-A～SC-C、13 行业迁移、IQ/OQ/PQ、软件/硬件候选**。
2. v2.0.0 的 **RedTeam / Critic / KillCritic / Blindspot / ActionPlan、三价值边界、AI Dealer 独立成章**。
3. 2026-09-27 全球白皮书的 **P0/P1/P2/P3 证据分层、GDI-OS、`registry_risk_topology`、模型 Challenger ladder、体育/彩票补全、采购尽调问卷**。
4. 三价值 DRAFT 的 **P-1～P-4 定稿前置、X-1～X-9 跨件冲突、三垂直 L4 域模型差异**。
5. 最新 `Inteligent_egaming_platform_ref` 新增的 **Playtech Virtual Host、BetConstruct KISS AI、Winfinity、Sentient Gaming Group、SkyGaming、Future Anthem/EveryMatrix、Stake/BC.Game/1xBet/Dafabet 等扩展主体**。
6. Windows 11 QMD 中对本机环境、R BLAS、TinyTeX、权限/安全代理和“验收看真正跑出来的结果”的工程纪律。

#### 26.0.1 本轮六份主附件指纹

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

## 26.1 Executive Thesis

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

## 26.2 证据模型：P0–P4 + Current-State Ledger

| 等级 | 定义 | 使用规则 |
|---|---|---|
| **P0 VERIFIED-REG** | 法律/监管正文、SEC/法定申报、正式监管公告 | 可作为制度/公司状态基线 |
| **P1 VERIFIED-FIRST-PARTY** | 公司年报、官方产品页、正式公告、官方技术文档 | 可直接引用，但厂商效果数字须注明“自述” |
| **P2 OBSERVED-SECONDARY/PARTNER** | 合作伙伴公告、可信行业媒体、供应商案例 | 可做趋势/采购线索，不升级成行业事实 |
| **P3 UNKNOWN/UNVERIFIED** | 仅代理站、营销页、来源缺失或相互冲突 | 只保留主体，不填充能力 |
| **P4 ADVERSARIAL-CLAIM** | 玩家端工具、预测器、攻击者/优势玩法宣称 | 仅用于防御威胁模型，不视为有效性证明 |
| **CONDITIONAL** | 结论取决于司法辖区、牌照、合同、产品版本、数据授权 | 必须列条件 |

### 26.2.1 Current-State Correction Ledger（C-01～C-16）

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

## 26.3 三条铁律 v3

### 26.3.1 Game Integrity Firewall

**AI/ML/RL/CRM 不得按个体玩家改变：**

- 牌靴、物理发牌；
- RNG 结果；
- 结算逻辑；
- 已公示派彩；
- 已公示体育结算规则；
- 彩票开奖或中奖判定。

AI Dealer 若为 RNG 型产品，结果引擎与生成式人物/语音/渲染层必须形成**独立信任域**；真人物理牌产品则以摄像/机器视觉作为**观测与核验**，不得反向控制结果。

### 26.3.2 Responsible Gambling Firewall

RG 信号只能用于降低暴露、限额/暂停、冷静期、自我排除、保护性信息、人工关怀、申诉与援助。

不得用于 VIP 升级、催存、返水增发、连败后奖励、追损召回、增加投注额/时长或利用脆弱状态营销。

#### 工程实现

`Purpose-bound ABAC / OPA-Rego → domain-specific feature views → policy tags → DLP → immutable access log → forbidden-feature tests`

**物理数据二极管**保留为极高敏感场景选项，不再误写为所有平台的唯一实现。

### 26.3.3 High-Impact Human Governance

账户永久限制、提款冻结、舞弊定性、SAR/STR 升级、荷官调查/停职等高影响动作：

- 必须可解释；
- 必须有人工复核；
- 必须记录 override；
- 必须可申诉；
- 必须可回滚（法律强制不可逆者除外）；
- 必须记录模型、规则、特征快照和证据链；
- 必须做 outcome analysis。

---

## 26.4 三价值 v3：止损 × 增效 × 合规

| 价值 | 允许优化目标 | 核心 KPI | 禁止伪收益 |
|---|---|---|---|
| **止损** | 已确认 fraud/bonus abuse/account takeover/collusion/payment anomaly/process error 的真实损失减少 | confirmed avoided loss、Precision@review-capacity、Recall@FP-budget、case cycle、false-positive cost | 正常玩家被限制后少派彩；拒付合法提款；把 house edge 当“模型收益” |
| **增效** | 同等人力处理更多、证据更完整、数据/对账/调查更快 | cases/analyst-day、automation evidence coverage、p50/p95 cycle time、reconciliation time、deployment lead time | 高风险玩家投注增加、追损延长、RG 人群回流 |
| **合规** | 更早保护、更完整审计、更低权限滥用、更强模型治理 | strong-risk latency、manual review coverage、appeal SLA、reason-code completeness、RG→marketing leakage=0、audit completeness | 将合规当可被利润抵消的“软权重” |

### 26.4.1 `economic_contract_registry`

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

## 26.5 完整主体登记册：来源完整性优先

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

## 26.6 竞争版图：能力拼图

### 26.6.1 Live Casino / Baccarat

#### Evolution
借鉴 Live Studio 工程、游戏版本治理、QoE、多区域容灾、专属桌/品牌化、规模化运营。未有一手证据的具体 AI 功能继续保持 P2/P3。

#### Playtech
最值得拆解的是 `PAM+ + Live + BetBuddy + Managed Services + AI Virtual Host`。2026-07 Virtual Host 已由半年报确认向多个客户上线。

#### Pragmatic Play
借鉴移动端、快速产品化、内容包装、多语言；Auto-Roulette/Bot 不等于机器学习/RL。

#### AI/Virtual Dealer 队列必须拆层
`Outcome Engine / Perception / Render / Dialogue / Personalization / Studio Ops`

Sentient Studios、Sentient Gaming Group、Playtech Virtual Host、BetConstruct KISS AI、SkyGaming、Avanti、Octane 的成熟度、监管路径与证据等级不同，禁止并成一个“AI Dealer 已成熟”结论。

Winfinity 归入 **Perception / Computer Vision**，不是人格型 AI Dealer。

---

## 26.7 GDI-OS v3 Blueprint

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

### 26.7.1 `registry_risk_topology` v3

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

### 26.7.2 三管线强制隔离
1. Fraud / Collusion / Bonus Abuse
2. AML / Financial Crime
3. Responsible Gambling

---

## 26.8 模型路线：禁止 Transformer-first

| Level | 模型 | 晋级条件 |
|---|---|---|
| 0 | 规则、Wilson、EWMA、GLM/scorecard | DQ、定义与 calibration 基线稳定 |
| 1 | XGBoost/LightGBM/CatBoost | OOT 优于 Level 0 且 FP 成本可控 |
| 2 | Survival / competing risks | 事件时点比静态分类有增量 |
| 3 | HMM / state-space / IMM | 状态转移稳定、跨窗口可复现 |
| 4 | Graph / entity resolution | 图增量超过简单统计/peer group |
| 5 | Sequence / Transformer | 严格 walk-forward 下长期稳定增量 |
| 6 | Contextual bandit / constrained RL | OPE + causal baseline + safe action set + compliance sign-off |

### 26.8.1 “140 表 → 15 风险类”只强化不删除

`7 windows × modules → feature snapshots → risk topology → 15 risk-domain materialized views`

15 张风险表继续保留为业务交付视图，但不再是系统唯一真相。

---

## 26.9 IQ / OQ / PQ / MQ 四门

### IQ
SBOM、seed、source fingerprint、data contract、DAG replay、权限与依赖。

### OQ
DQ、point-in-time、PR-AUC、Precision@capacity、Recall@FP-budget、Brier/ECE、purged walk-forward、negative controls、OOD。

### PQ
p95/p99/p99.9、peak load、backpressure、no-event-loss、reconciliation、fallback、replay exactness、audit completeness。

### MQ（v3 新增）
model inventory、conceptual soundness、independent validation、vendor model DD、challenger、ongoing monitoring、outcome analysis、override governance、retirement。

> SR 26-2、ALCOA+、21 CFR Part 11、DO-178C 等均作为**借鉴型最佳实践**；不是博彩业法定要求。

---

## 26.10 RedTeam v3 — 32 个攻击面

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

## 26.11 Critic v3

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

## 26.12 KillCritic v3 — 20 个 NO-GO

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

## 26.13 Blindspot v3

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

## 26.14 Cheatsheet

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

## 26.15 Blueprint — 十域

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

## 26.16 跨行业迁移 v3

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

## 26.17 采购尽调 40 问

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

## 26.18 ActionPlan v3

### Phase 0 — 现在
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

### Phase 1 — 0–90 天：Label & Baseline
PU learning、weak supervision、active learning、GLM/GBDT、calibration、entity resolution、peer-group、outcome ledger、negative controls。

### Phase 2 — 授权测试线：Shadow Real-time
event bus、clock-quality SLO、point-in-time features、shadow scoring、case management、SLO/backpressure、replay、synthetic load。

### Phase 3 — 3–9 个月：Baccarat Risk Intelligence
Dealer/Table/Player/Agent/Payment/Bonus/RG；graph/temporal risk；HMM/IMM；side-bet exposure stress；bot/device；causal evaluation。

### Phase 4 — 6–12 个月：Perception / AI Dealer Pilot
Winfinity-style CV challenger；双读；AI Virtual Host/Dealer 测试线；Outcome 与 Render/Dialogue 分域；认证/监管尽调。

### Phase 5 — 12–24 个月：Constrained Decision Intelligence
uplift/CATE；contextual bandit OPE；safe actions；小流量；独立验证；model risk committee；retirement/reapproval。

**禁止直接跳 autonomous RL。**

---

## 26.19 最终战略

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

## 26.20 公开核验来源（截至 2026-09-28）

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

## 26.21 深地科学 × 宇航 × 量子信息 × 时空边界增量（v3.1.0 · 2026-09-29）

> **版本关系**：本章为 v3.0.0 的严格增量层；原 v3.0.0 正文全部保留。与旧说冲突时，以本章的更正编号 C-17～C-32 为当前口径；旧说保留为血统记录，不静默删除。
>
> **证据纪律扩展**：现实深地设施、已发表实验与官方工程文件继续使用 P0～P4；“尚无观测证据但物理理论允许”的内容另标 `T1 THEORETICAL`；“仅科幻设定/无可检验证据”标 `S0 SPECULATIVE`。`T1/S0` **不得**升级为生产技术、采购能力、工程 SLA 或公司能力事实。

### 26.21.1 语义澄清：稷下学宫与“地下世界”分轨

1. **历史稷下学宫只有战国齐国临淄这一历史对象。** 2022 年山东考古工作认定淄博市临淄区齐都镇小徐村西、齐故城小城西门外建筑基址群为稷下学宫遗址范围。本项目以后不再寻找所谓“云南第二稷下学宫”。
2. 本轮所谓“地下世界 / 地下科学研究院”是现代**深地科学设施（Deep Underground Science Facilities）**、地下空间工程与行星地下栖居研究，不与历史稷下学宫混称。
3. “地下与外太空连接”必须拆为五种不同技术：
   - **观测连接**：地下探测器观测来自太阳、超新星、宇宙线、引力波等宇宙信号；
   - **数据连接**：地下实验室与地面/卫星通过光纤、互联网、时间同步和科研网络交换数据；
   - **训练连接**：以洞穴/矿井作为月球、火星、深空任务类比环境；
   - **量子信息连接**：量子态/量子信息可在地面—卫星链路间传送；
   - **宏观物质连接**：人、飞行器或物体“瞬间转移”——截至本版**无已验证工程技术**。

### 26.21.2 Current-State Correction Ledger 增量（C-17～C-32）

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

### 26.21.3 深地科学前沿地图（现实层）

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

### 26.21.4 “地下 ↔ 外太空”的六级连接成熟度

| Level | 连接形式 | 2026-09 状态 | 例子 |
|---|---|---|---|
| **D0 已运行** | 地下实验室 ↔ 地面科研网络 | PROVEN | 全球地下实验数据远程传输、控制、归档 |
| **D1 已运行** | 地下探测器 ↔ 宇宙信号 | PROVEN | Super-K、KAGRA、CJPL、LNGS |
| **D2 已运行** | 地下类比环境 ↔ 航天训练/行星技术 | PROVEN | ESA CAVES；Boulby 行星探索/机器人 |
| **D3 已实验** | 地面 ↔ 卫星量子信息 | PROVEN-EXPERIMENT | 墨子号 1,400 km 量子态传态 |
| **D4 工程研究** | 月球/火星地下洞穴 ↔ 栖居/机器人 | OBSERVED + R&D | 月海静海坑地下洞道雷达证据；洞穴探测任务概念 |
| **D5 无证据** | 地下基地 ↔ 太空的人/宏观物体瞬移 | SPECULATIVE | 无已知装置、无工程示范 |
| **D6 理论/科幻** | 可控虫洞、返回过去、宏观时空门 | THEORETICAL / SPECULATIVE | 方程与量子模拟不等于现实虫洞 |

### 26.21.5 量子传态、瞬间转移与穿越时空：严密分界

#### A. 量子传态（Quantum Teleportation）——已实验验证

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

#### B. “瞬间移动人/物体”——当前不存在

宏观人体若要按科幻方式“扫描—发送—重建”，不仅面临不可思议的数据量、量子态不可克隆、测量扰动、材料重构和身份连续性问题，而且目前没有任何可工作的物理装置或工程原理验证。

#### C. 时间旅行——必须拆成两个问题

1. **相对论时间膨胀：PROVEN。** 不同速度/不同引力势的时钟积累不同固有时；NIST/JILA 已在毫米高度差上测得引力时间膨胀。
2. **返回过去：UNKNOWN / 无工程证据。** 广义相对论某些解含闭合类时曲线/虫洞数学结构，但从“数学解存在”到“自然存在、可稳定、可穿越、可控制”之间仍有巨大且未跨越的物理鸿沟。

#### D. “量子虫洞实验”——不得新闻标题化

2022 年 Sycamore 量子处理器工作研究的是与可穿越虫洞理论相联系的量子动力学。研究团队明确说明：
- 没有在现实空间创造时空裂隙；
- 没有产生 3+1 维真实虫洞；
- 观察到的过程亦可描述为一种量子传态。

故本项目登记为 `T1 THEORY-ANALOGUE`, **不得写成“人类已制造虫洞”**。

### 26.21.6 月球/行星“地下世界”：现实最值得追踪的路线

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

### 26.21.7 台湾、英国与 Renaissance Technologies：前沿组织模式增量

#### 台湾
公开资料显示其国防 AI 路线明确采用 GPU/NPU/FPGA 边缘计算、异构多源资料融合、HPC 与人机协同，并强调最终任务控制责任保留给人；2026 年国防创新单位亦公开承担国内外成熟商业技术的评估与导入。这里可迁移的是**商用前沿技术快速吸收 + 人在回路 + 数据分级 + 任务安全边界**，不是军事用途本身。

#### 英国
Dstl 是英国国防部体系内科研机构，人员主要为公务员，主体是科学家与工程师，同时制度化与产业、大学、政府和盟国合作。其模式再次否定“公共科研机构必须全自研”的二分法。

#### Renaissance Technologies

**历史先斧正**：James Simons 并非可简单写成「美国国防部内部密码官」。Simons Foundation 一手资料显示，他于 **1964 年加入 Institute for Defense Analyses (IDA) 的 Communications Research Division**，该部门聚焦 code breaking；他开发算法攻击特定 cryptographic problems。Simons Foundation 2024 讣文进一步称其在 IDA 是 **code breaker for the National Security Agency**。现今 IDA 的 Center for Communications and Computing（CCC）是 **NSA 赞助的 FFRDC**，公开研究范围包括 cryptology、sophisticated encryption methods、cybersecurity、HPC 与 large-data analytics。由此能确认的是**国家级密码分析环境对 Simons 的数据建模思想有历史影响**；不能外推为「Renaissance 使用 NSA 内部密码系统」或「Simons/Renaissance 在 2026 是世界第一资安机构」。Simons 已于 **2024-05-10** 去世。

**2026 当前公开工程证据进一步增强**：Renaissance 官网 About 现载其研究资料库每日增长 **40 TB+**、拥有 **50,000+ computer cores**、**200+ Gbps global connectivity**，并有各自足以支持交易运营的**冗余计算设施**。Systems Engineer 招聘公开 Linux、Slurm、LLM deployments、PostgreSQL、Kerberos、OpenSSL 等；Security Engineer 招聘则明确列 firewalls、antivirus/EDR、IDS/IPS、encryption、vulnerability scanning、IAM、security governance 与 incident response。

因此，Renaissance 的公开证据已足以支持：

```text
研究—生产协作
+ Linux/HPC/Slurm/PostgreSQL
+ 大规模数据与冗余设施
+ 企业级 endpoint/network security
+ encryption / IAM / vulnerability / IR 治理
```

但仍**没有公开证据**披露其内部：HSM/KMS 密钥层次、零信任策略细节、机密研究网分区、数据二极管、PQC 迁移、红队频率、SOC 指标或专有加密协议。因此「保密文化顶尖」可作合理描述；「天下第一密码工程/信息安全」**不可证实**。

#### 公开保密能力评分：评分「证据覆盖」，不评分真正秘密实力

为回应「务必评分」又避免伪精确，本件只给 **Public Evidence Coverage Score（公开证据覆盖分）**。每维 `0=未公开 / 1=部分 / 2=一手且具体`，总分 `/10`；**分低可能只是更保密，不表示真实能力低**。

| 主体 | 公开密码协议 | Endpoint/Network/IAM | 规模/韧性 | 可外部验证/形式化 | PQC 公开部署/路线 | 覆盖分 |
|---|---:|---:|---:|---:|---:|---:|
| Cloudflare | 2 | 2 | 2 | 2 | 2 | **10/10** |
| Microsoft | 1 | 2 | 2 | 2 | 2 | **9/10** |
| Signal | 2 | 1 | 0 | 2 | 2 | **7/10** |
| Renaissance Technologies | 0 | 2 | 2 | 1 | 0 | **5/10** |
| IDA CCC（NSA-sponsored FFRDC） | 2 | 1 | 1 | 1 | 0 | **5/10** |

> **KillCritic**：此表不是「谁最安全」排行榜。Renaissance / IDA 的任务天然包含非公开信息，公开覆盖分低有严重的 disclosure bias；Cloudflare/Signal/Microsoft 公开协议、文档和部署状态较多，所以在「可核验」维度得分更高。**不得把这个 10 分制写成真实国家/公司保密实力排序。**

应迁移的仍是**研究—生产分离、HPC、冗余、可重复性、运维、安全治理与最小泄露面**；不要把顶尖量化误解为“所有底层都必须秘密自研”。

### 26.21.8 外星文明与“地下世界”证据闸门

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

### 26.21.9 RedTeam v3.1 — 深地/量子/时空专项

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

### 26.21.10 Critic v3.1

- 地下科研设施的价值恰恰来自**控制背景噪声**，不是“越深技术越高级”；不同实验最优深度不同。
- 量子传态距离纪录对“人类传送”几乎没有直接工程外推价值。
- 月球洞穴即便确认存在，也还需解决进入、通信、粉尘、热控、辐射、能源、生命支持与救援。
- 深地设施、量子网络、空间基地是三个相邻但独立的工程体系，不能因“都很前沿”而自动拼成一条技术链。
- 未公开国防/航天系统只能写 `UNKNOWN`，不能以“必然更先进”代替证据。

### 26.21.11 KillCritic v3.1 — 新增 NO-GO

任一出现即阻断对外发布：
- “量子传态已可传送人/物体”；
- “人类已制造真实虫洞”；
- “已有技术能返回过去”；
- “存在已证实外星地下基地/科研院”；
- “UAP = 外星飞船”；
- “月球洞穴 = 人工基地”；
- “稷下学宫在云南另有历史本体”；
- 将 `T1/S0` 内容写入采购能力、生产 SLA 或商业承诺。

### 26.21.12 Blindspot v3.1

新增必须长期追踪：
- 极低本底辐射对量子芯片错误率、材料与生物的真实效应；
- 地下通信定位（GNSS 不可用）、时钟同步与机器人自治；
- 地下设施灾害、通风、涌水、火灾与逃生；
- 月/火地下空间的通信中继与自主建图；
- 量子网络的纠缠分发、量子中继器、存储器和经典控制平面；
- 理论时空模型中的能量条件、稳定性、量子反作用与因果性保护；
- “未知”类研究的可证伪实验设计，防止科研叙事滑向不可证伪。

### 26.21.13 Cheatsheet v3.1

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

### 26.21.14 Blueprint v3.1 — Deep-Earth × Space Research Stack

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

### 26.21.15 ActionPlan v3.1

**Phase F0 — 证据注册**：建立 `frontier_technology_registry` 与 `speculative_horizon_registry`；所有“地下/量子/时空/外星”主张必须有 `source_date / evidence_grade / experimental_status / engineering_status`。

**Phase F1 — 深地科学对标**：固定跟踪 CJPL、SNOLAB、SURF、LNGS、Kamioka/KAGRA、Boulby；每季度更新设施、科研方向与公开技术。

**Phase F2 — 地下×宇航专题**：追踪 ESA CAVES、Boulby planetary exploration、月球/火星洞穴遥感与自主机器人；只收公开科研与民用航天资料。

**Phase F3 — 量子网络**：以量子态传态、纠缠分发、量子中继器、卫星量子链路为对象；任何“物质瞬移”单独保持 `S0`。

**Phase F4 — 时空物理**：将时间膨胀列 `P0/P1 PROVEN`；虫洞/CTC 按理论研究记录，不设工程交付期限，不写商业能力。

**Gate**：任何结论必须回答——`它是数学？物理理论？实验观测？原型？工程部署？还是纯假说？`

### 26.21.16 本章公开来源（核验日期 2026-09-30）

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
- Renaissance Technologies About：https://www.rentec.com/Home.action?about=true
- Renaissance Technologies Security Engineer：https://www.rentec.com/Careers.action?jobs=true&selectedPosition=securityEngineer
- Renaissance Technologies Systems Engineer：https://www.rentec.com/Careers.action?jobs=true&selectedPosition=systemsEngineerEs
- Simons Foundation career/IDA code breaking：https://www.simonsfoundation.org/2012/09/28/simons-foundation-chair-jim-simons-on-his-career-in-mathematics/
- Simons Foundation 2024 obituary / NSA code breaker：https://www.simonsfoundation.org/2024/05/10/remembering-the-life-and-careers-of-jim-simons/
- IDA CCC official：https://www.ida.org/-/media/corporate/files/general/ccc_one-pager.ashx

---



---

# 27. DRAFT 隔离登记：v0.3.0 不自动转正

`在线博彩娱乐白皮书_完美真人百家乐_三价值统一架构_v0_3_0_DRAFT.md` 当前仍明确声明：

- 父版保持 DRAFT；
- P-1～P-7 未解除前不转正；
- `house_edge`、风险注册表命名、主体身份确认、授权测试线、独立复核等仍有前置；
- 因此本件只吸收其**方法、待办、冲突登记与证据纪律**，不把 DRAFT 状态偷换成“已生产验证”。


## 27.1 待核清单 U 系列（新增 · 跨轮继承并更新）

| # | 项 | 状态 | 负责动作 |
|---|---|---|---|
| U-1 | `Aerospace_Ecosystem_Report.qmd` 全文 | **✅ CLOSED** | 六元组 6/6 PASS，见 §1.2.2 |
| U-2 | 「礼逆袭操作系统」原词 | **✅ CLOSED** | §0.1 约定：礼逆袭 ≡ Linux（C-DAQIN-11） |
| U-3 | RedHawk Linux 实际部署域 | **INFERRED** | 逐平台逐子系统一手证据，无则保持 C-18 |
| U-4 | 英国 Dstl 自研边界 | **P1 部分成立** | §21.7 已引 gov.uk 框架文件 |
| U-5 | 台湾 NCSIST / 国防创新单位结构 | **P1 部分成立** | §21.7 已引 MND 页 |
| U-6 | Renaissance Technologies 保密架构 | **P1 明显增强但仍不完整** | 已有 About + Systems + Security Engineer 一手资料；可证实安全控制类别与冗余/HPC，内部密钥/PQC/零信任细节仍 UNKNOWN |
| U-7 | 云南儒学遗产与「稷下」命名关联 | **✅ CLOSED** | 用户已澄清历史本体仅临淄一处（C-22） |
| U-8 | Sift 是否 SpaceX 自研 | **待核** | 疑为前 SpaceX 工程师另创之独立公司；`Aerospace…qmd` §四 疑误植 |
| U-9 | 九所深地实验室深度参数 | **部分** | 仅 CJPL 之 ~2,400 m / ~360 GeV 缪子有本轮一手实测；余者 P1 引官网但未逐项验算 |
| U-10 | `OGDIL` 全称（X-21） | **待裁定** | 与 P-5（X-20）同批 |
| U-11 | 2026-09-29 农历日柱 | **待核** | 丙午年正确；月柱日柱未验 |
| U-12 | §4.2 版本锚 | **✅ CLOSED** | 13 项复核：8 PASS · 3 失准 · 2 硬错；已斧正并挂日历闸（C-DAQIN-33） |
| U-13 | `Aerospace…qmd` 之 AERO-01/02 内部矛盾 | **待解** | 解除前该件不得并入正本 |
| U-14 | Kaspersky Encrypted Connections Scan 当前模式 | **待核** | 查本地界面/受管策略：Do not / upon request / always |
| U-15 | `speedtest.net` 实际 TLS certificate issuer | **待核** | Chrome 证书链；若 issuer=Kaspersky 才能证实当次 TLS interception 候选 |
| U-16 | Kaspersky 实时服务/进程与 primary AV 角色 | **待核** | `Get-Service` / `Get-Process` + Windows Security → Manage Providers |
| U-17 | Browser/App 网速差的 LO2 重复性 | **待核** | 固定 exact Ookla server，≥5 组交错 A/B + Chrome/Edge/App |
| U-18 | 两条 Kaspersky CA 是否同一证书副本 | **待核** | 比较 `PSParentPath` / `Thumbprint` / validity |
| U-19 | Defender `Normal` 与 Kaspersky 同时注册之原因 | **待核** | 查 MDE/tamper/组织策略/第三方 AV 健康状态；不得先假定双主动冲突 |
| **U-20** | 马斯克 / 马云「终身免费号码、电邮、社交账号」计划 | **UNKNOWN** | 未检得一手证据；有出处再查。Starlink Direct to Cell 属连接层，非号码发放，不可混层 |
| **U-21** | 本主体三层身份锚落地状态 | **待办** | 自有域名是否已购？恢复码是否已离线存？BitLocker 恢复密钥是否已导出？（§10.5.4） |
| **U-22** | SLES 16.0 GA 日期 | **待核** | 版本现行已证，GA 日未取得一手证（§4.2.1 #9） |
| **U-23** | Signal Point 是否续履 RNK 之终身合同 | **UNKNOWN** | 客户合同随 §363 资产出售转移，但 RNK 已解散；未检得履约资料（§10.5.5-E） |
| **U-24** | 顶尖电信商内部员工终身标识体系 | **UNKNOWN** | AT&T / Verizon / NTT / 中国移动 / Telefónica；须查 |
| **U-25** | 中国 MIIT 是否有对标 EDIPI 之统一编号 | **UNKNOWN** | 实名制 ≠ 终身制；须查 |
| **U-26** | eIDAS 2.0 各成员国 2026-12-24 实际达成率 | **待核 · 已挂日历闸** | **85 天后强制复核**；须分开追踪自然人钱包与法人钱包两条曲线 |
| **U-27** | 本主体 ORCID iD 是否已申请 | **待办** | 已具备条件（已发表研究 + ResearchGate），零成本、永久、与任何机构/平台/号码脱钩（§10.5.4 第 5 项） |

## 27.2 血统裁定待办（新增）

| 件 | 建议处置 | 前置 |
|---|---|---|
| 本件 `_大秦赋算筹_v1_2_1.qmd` | **总纲正本** | 无 |
| `_大秦赋算筹_v1_2_001.qmd` | 改名加 `_superseded` 保留 | 已被本版取代（C-DAQIN-35） |
| `_大秦赋算筹_v1_1_1.qmd` | 改名加 `_superseded` 保留 | §4.2 成果已回填入本版 |
| `_大秦赋算筹_v1_1_0.qmd` | 改名加 `_superseded` 保留 | — |
| `_大秦赋算筹_.qmd`（父版） | 改名加 `_superseded` 保留，**不删除** | 无 |
| `Whitepaper-…-V3-1-0.md` | 已内嵌于 §26；独立件加 `_superseded` | 无 |
| `…v0_3_0_DRAFT.md` | **维持 DRAFT** | P-1～P-7 未解 |
| `Aerospace_Ecosystem_Report.qmd` | **附录级参考** | U-13 |

> **版本号是身份标识而非序号**：本件之 `v1.2.1` 不因号小而居于 `V3.1.0` 之下——二者属不同命名空间（总纲 vs 白皮书），不可比大小。

## 27.3 主体侧数据暴露登记（新增 · 与 §10.5 配套）

| 项 | 位置 | 暴露程度 | 状态 |
|---|---|---|---|
| 六国行动电话号码 | `scibrokes/owner` README | **完整可拨** | **待清除** |
| 八个电邮地址 | 同上 | 完整 | **待清除** |
| 出生日期 + 出生地 + 生辰八字 | 同上 | 完整 | **待清除** |

**定级 P1·M5**：一手来源、已被搜索引擎收录、已规模化传播。撤回成本已产生（引擎缓存、Archive、镜像站、GitHub 全量 dataset）。

**处置**：`git rm` **不足** —— 旧 commit 仍可检出，须 `git filter-repo` 或重建仓库；另走 Google / Bing 个人信息移除通道。

> **本项与本件第 §13 出口闸、§10.5 身份锚构成同一命题的三面**：出口闸防数据出去、身份锚防主人进不来、本节记**已经出去了的**。三者缺一，治理不闭环。

---

# 28. 最终总裁定

> **《大秦赋算筹》不是要选一个“天下第一操作系统”，而是建立一个跨 Windows、礼逆袭（Linux）、云、RTOS、量化、AI、密码学与治理的“证据—计算—安全—决策”体系。**

最稳健的工程路线是：

```text
Windows 11 工作站
+ Linux 测试/生产底座
+ 可复现 R/Python
+ 标准数据契约/血统
+ 规则与统计基线
+ GBDT/Survival/HMM/Graph
+ Transformer（有增量才上）
+ constrained Bandit/RL（最后上）
+ Zero Trust
+ KMS/HSM
+ SBOM/SLSA
+ sealed real holdout
+ shadow
+ human review
+ endpoint role registry / TLS-inspection provenance
+ LO1→LO2→LO3 diagnostic discipline
```

**世界级的真正标准不是“用了多少 AI”，而是：**
每个来源能否查证、每次计算能否复现、每个版本能否重放、每项权限能否解释、每把密钥能否追踪、每个模型能否证伪、每个高影响决定能否人工复核与回滚、每项商业收益能否由真实对照与结果账证明。

---

# 29. 斧正变更历史（v1.1.0 → v1.1.1 → v1.2.0 → v1.2.1 → v1.2.2 · 2026-09-29 ~ 30）

| # | 斧正项 | 类别 | 操作 |
|---|---|---|---|
| D-1 | §26 章名与内嵌正文版本不符 | FATAL | 改章名，正文零删减（C-DAQIN-04） |
| D-2 | **顶层章号碰撞 42 处** | FATAL | §26 区间 72 标题降一级并重编号 `26.N[.M]`（C-DAQIN-05） |
| D-3 | `lang: zh-TW` 与简体正文不符 | MAJOR | 改 `zh-CN`（C-DAQIN-06） |
| D-4 | 农历日柱未核实 | MINOR | 移出 `date-format`，列 U-11（C-DAQIN-07） |
| D-5 | 缺六元组自指约定 | MAJOR | 新增 §0.3 |
| D-6 | 源基较 DRAFT 收窄 2 件 | **退化** | 新增 §1.2，补登 S-8/S-9/S-10（C-DAQIN-09） |
| D-7 | `OGDIL` ↔ `GDI-OS` 分叉未登记 | MAJOR | 立 X-21，§1.3（C-DAQIN-10） |
| D-8 | U-2 悬置 | — | 结案：礼逆袭 ≡ Linux（C-DAQIN-11） |
| D-9 | §4.2 版本锚无法核实 | MAJOR | 整表降 P3，加禁止下单告警（C-DAQIN-12） |
| D-10 | 证据等级单轴压两轴 | MAJOR | 拆 P 轴 × M 轴，新增 §0.4（C-DAQIN-08） |
| D-11 | §21.3 深地设施等级平铺 | MINOR | U-9 登记；仅 CJPL 有本轮一手实测 |
| D-12 | 缺不退化映射表 | **方法论缺口** | 新增 §1.4（C-DAQIN-13） |
| D-13 | `Aerospace…qmd` 内部矛盾 | BLOCK | AERO-01/02，U-13，暂不并入正本 |
| D-14 | 静态图偏离呈现纪律未登记 | MINOR | 新增 §0.5 已知偏离登记 |

**本轮操作限于四类**：改层级、改编号、改元数据、增章节。
**未删除任何原有段落、表格、条目或来源链接。**

## 29.1 父版保留

原件 `_大秦赋算筹_.qmd` 之实测六元组（由本轮独立实例测得，供改名归档时登记）：

| 元 | 值 |
|---|---|
| 行数 | 2,195 |
| 字节 | 125,519 |
| MD5 | `8b1cdf7cb48c9dd46a778b354fd72d63` |
| 换行 | CR=0 · LF=2,195 · CRLF=0 |
| 编码 | UTF-8 · BOM=False · NUL=0 · 末字节 `\n` |

按 §1.4 自证条款，父版须改名加 `_superseded` 后缀保留，**不得删除**。

## 29.2 v1.2.0 增量斧正（2026-09-30）

| # | 斧正项 | 类别 | 操作 |
|---|---|---|---|
| D-15 | 缺本机实证等级 | 方法论 | 新增 LO1/LO2/LO3，避免把单次截图当因果 |
| D-16 | Speedtest Browser/App 单次差异未登记 | EVIDENCE | 新增 §10.4；锁定 183.33 vs 339.63 Mbps 与 46.02% 下载差 |
| D-17 | Defender 只写「存在」未写运行角色 | MAJOR | 登记 `AMRunningMode=Normal` 与 RTP/NIS/IOAV True；以 Microsoft P1 解释 Active mode |
| D-18 | Kaspersky 根 CA 容易被过度解释 | MAJOR | 区分「根证书存在 / 产品可解密 / 当次站点实际 interception」三层 |
| D-19 | 无 Proxy 被误读为无过滤 | MAJOR | 仅排除显式 WinHTTP/User Proxy/PAC；保留 WFP/NDIS/VPN/DLP/透明网关 |
| D-20 | 浏览器通用上限被用来解释 183 Mbps | MAJOR | 以官方约 3 Gbps 浏览器量级反证：本机 340 Mbps 远未触及，必须另找本地路径原因 |
| D-21 | Windows 工作站 Blueprint 固写 `Defender` | ARCH | 改为「一个 primary AV + passive/EDR/DLP 角色化端点栈」，避免双主防毒暗示 |
| D-22 | James Simons/IDA 身份与密码经历描述过粗 | FACT | 以 Simons Foundation + IDA 一手资料改为 IDA CRD code breaking / NSA code breaker 语境 |
| D-23 | Renaissance 公开安全证据不足 | EVIDENCE | 补 About + Security Engineer + Systems Engineer；更新为 40 TB/day、>50k cores、>200 Gbps、冗余设施 |
| D-24 | 「天下第一保密」评分伪精确 | METHODOLOGY | 改成 `/10` 公开证据覆盖分，显式声明 disclosure bias，禁止当真实实力排行榜 |
| D-25 | 待核项不足 | GOVERNANCE | 新增 U-14～U-19：KES mode、证书 issuer、AV role、LO2、CA thumbprint、Defender/KES 共存原因 |

### 29.2.1 v1.1.0 输入件实测指纹（本轮）

在升级前对用户上传的 `_大秦赋算筹_v1_1_0.qmd` 直接落盘实测：

| 元 | 值 |
|---|---|
| 行数 | 2,400 |
| 字节 | 141,137 |
| MD5 | `6e4bd08638be2d6eca149574f28159c7` |
| 换行 | CR=0 · LF=2,400 · CRLF=0 |
| 编码 | UTF-8 · BOM=False · 末字节 `\n` |

> v1.2.0 自身 MD5/字节数仍遵守 §0.3：**不写入自身正文**，随交付回执给出。

## 29.3 v1.2.1 合并斧正（2026-09-30）

> **本版之唯一任务**：把 v1.1.1 与 v1.1.2 的成果合并进 v1.2.001，并修复合并本身造成的退化。

| # | 项 | 类别 | 操作 |
|---|---|---|---|
| **R-1** | **§4.2 U-12 复核成果整体丢失**（v1.2.001 以 v1.1.0 为基线） | **FATAL 退化** | 全表回填 + 新增 §4.2.1/4.2.2/4.2.3/4.2.4（C-DAQIN-33 / 35） |
| **R-2** | §27.1 之 U-12 仍记「待核」 | 退化 | 改 **CLOSED** |
| **R-3** | `C-DAQIN-14` 跨分支撞号（U-12 ↔ Speedtest） | **台账冲突** | U-12 改编 C-DAQIN-33；撞号事实显式入册（C-DAQIN-34）；编号改由 §1.3 单点发号 |
| **R-4** | §1.1 排在 §1.2 之后 | 结构 | 顺序复位 |
| **R-5** | v1.1.2「主体身份锚」未并入（§10.4 已被 Speedtest 专题占用） | 缺项 | 新增 **§10.5**，不动既有 §10.4（C-DAQIN-36） |
| **R-6** | §29 章名仍为 v1.1.0 | 元数据 | 改为四版血统全称 |
| **R-7** | §27.2 血统表仍以 v1.1.0 为正本 | 元数据 | 复位为 v1.2.1，并补登三个 `_superseded` |
| **R-8** | 主体侧数据暴露无台账 | 缺项 | 新增 §27.3 |
| **R-9** | 副标题 v1.2.0 与档名 v1_2_001 不符 | 元数据 | 统一为 v1.2.1 |

**本轮操作限于五类**：回填、改序、改元数据、增章节、改编号。
**未删除任何 v1.2.001 原有段落、表格、条目或来源链接**（§10.4 Speedtest 专题、C-DAQIN-14~32 全数保留）。

## 29.4 退化根因与制度补丁

| 根因 | 补丁 |
|---|---|
| 合并未以 §1.4 不退化映射表逐节对账 | **合并前须先跑映射表**，非合并后补 |
| C-DAQIN 编号在分支间各自发号 | **§1.3 单点发号**；分支合并前先对号 |
| 版本锚无复核触发器 | **§4.2.4 日历闸**（4月下 / 5月中 / 9月中 / 10月下） |
| 主体身份依赖租来的标识符 | **§10.5 三层锚**：L1 密码学 / L2 自有域名 / L3 离线恢复码 |

> **本轮最重要的一条教训**：`v1.2.001` 的内容增量（Speedtest 实证、C-DAQIN-21~32 前沿生态、§25 来源扩充）质量很高，**但它是从错误的父版分叉的**。
> **内容做得越多，分叉成本越高。** 血统裁定（§27.2）不是形式主义，它是合并的前置条件。
## 29.5 v1.2.1 · 终身数字身份 / 全民免费数字公共基础设施增量（2026-09-30）

> **增量原则**：本节及 §30 仅追加，不删除、不静默改写父版。  
> **父版输入指纹（本轮落盘实测）**：`218,891 bytes` · `LF=3,492` · `CR=0` · `UTF-8` · `BOM=False` · `MD5=416743f233bb5ab153dd81c9af829204` · `SHA-256=6043dd7ec28c5a0979a508a4dc1adde53c4231f39c9e5416ad53d4e1f1960c74`。  
> **说明**：同一语义版本 `v1.2.1` 发生内容增量时，**必须重新签发文件指纹**；文件名相同不代表字节身份相同。

| # | 增量 | 类别 | 裁定 |
|---|---|---|---|
| C-DAQIN-37 | 终身通信身份证（LCI）从“终身号码”升级为“终身身份 + 可替换端点” | ARCH | **ADOPT** |
| C-DAQIN-38 | 生物识别不再视作根身份证明；依 NIST 作为多因素中的一环 | SECURITY | **ADOPT** |
| C-DAQIN-39 | EEG/脑机认证列研究前沿；不把“远程无接触脑电波认主”写成已工程化事实 | EVIDENCE | **ADOPT** |
| C-DAQIN-40 | “全民免费”改写为 `free-to-user ≠ zero-cost`，建立 60 亿 / 82 亿人口成本包络 | ECON | **ADOPT** |
| C-DAQIN-41 | 建立“身份公益层 + 商业服务层”双层治理，避免单一企业死亡即身份死亡 | GOVERNANCE | **ADOPT** |
| C-DAQIN-42 | 终身账号必须具备导出、迁移、恢复、继承/纪念、停服接管条款 | CONTINUITY | **ADOPT** |
| C-DAQIN-43 | “掌控/监控天下人”改为“用户授权、目的限定、数据最小化、可撤回” | PRIVACY | **ADOPT** |
| C-DAQIN-44 | 电话号、邮箱、社交号、电商号、代码托管号、AI 账号一律降为可替换端点 | IDENTITY | **ADOPT** |
| C-DAQIN-45 | 大规模免费 AI 必须限额、排队、缓存、蒸馏、小模型分流，否则成本不可控 | CAPACITY | **ADOPT** |
| C-DAQIN-46 | 以 2026 hyperscaler CapEx 仅作量级参照，禁止直接当成本/用户换算 | METHODOLOGY | **ADOPT** |

---

# 30. 终身数字身份 × 全民免费数字公共基础设施（LCI / Universal Digital Commons）

## 30.1 总裁定：人的身份不应等于某一家公司、某一个号码或某一张脸

用户提出的方向——**终身电话号、终身电邮、终身社交网、终身电商身份、终身代码托管身份、终身人工智能身份**——技术上可拆解为一个更稳健的母问题：

> **怎样让“人”的数字身份生命周期长于任一运营商、云厂商、社交平台、AI 公司甚至操作系统？**

本件采用以下核心等式：

```text
人的数字身份
≠ 某一个手机号码
≠ 某一个邮箱
≠ 某一个社交账号
≠ 某一个设备
≠ 某一次人脸/指纹识别
≠ 某一家 AI / 云厂商
```

而应设计为：

```text
终身身份根（Lifetime Identity Root）
        ↓
可旋转的密码学凭证 / Passkey / Hardware Key
        ↓
可验证凭证（Verifiable Credentials）
        ↓
可替换端点（phone / email / social / commerce / code / AI）
        ↓
用户授权的数据金库与可迁移服务
```

**真正“终身”的，应是身份连续性与迁移权，不是任何一家公司的服务承诺。**

---

## 30.2 先斧正：人脸、指纹与“远程脑电波”不是万能主人钥匙

### 30.2.1 生物识别（Biometrics）为什么不能单独当根钥匙

美国 NIST SP 800-63B（现行 800-63-4 页面）明确指出：

- 生物特征**不是秘密**；脸可被拍摄，潜在指纹可从接触物取得；
- 生物识别存在测量噪声、姿态/环境变化与阈值问题；
- 人脸识别应实施展示攻击检测（Presentation Attack Detection, PAD）；
- 生物识别应只作为**多因素认证（MFA）的一部分**，并与物理认证器结合；
- 必须提供替代的非生物认证方式。

因此，本件把“脸/指纹偶尔认不出主人”解释为：

```text
False Non-Match / Sensor Noise / Template Drift / Presentation / Device State
```

而不是“AI 忘了主人”。

### 30.2.2 远程人脸识别

“远程摄像头识别人脸”在技术上早已存在，但：

- **识别（identification）**与**认证（authentication）**不是一回事；
- 远距离、低分辨率、角度、光线、遮挡、深伪与重放都会改变错误率；
- 它不应成为终身身份的单一根认证器；
- 远程人脸识别还涉及法域、隐私、比例原则与误伤治理。

**本件不把远程人脸识别视为“终极主人认证”。**

### 30.2.3 EEG / 脑电认证与脑机接口

2025～2026 的学术综述显示，**脑电图（Electroencephalography, EEG）认证**确实是活跃研究方向，可做 1:1 验证或 1:N 识别；但仍面对：

- 跨会话信号漂移；
- 年龄、精神/生理状态、疲劳影响；
- 电极位置与接触品质；
- 设备差异；
- 可复现性、规模化与部署便利性；
- 隐私与神经数据安全。

当前公开研究通常需要**EEG 采集设备/电极或神经接口**，不能据此推出：

> “无需传感器、隔空远程读取某个人脑电波并稳定认主”

已经成为 2026 年的成熟身份技术。

Neuralink 的公开 N1 Implant 是**植入式**脑机接口，使用 1,024 个电极、64 条柔性 threads 记录神经活动；它不是“远程无接触脑电身份证”。

因此：

```text
Passkey / Hardware Key          → 生产成熟
Face/Fingerprint + PAD         → 可作 MFA
EEG Authentication            → 研究/原型前沿
Implant BCI                    → 临床/研究设备
Contactless remote brain ID    → 未建立成熟生产证据
```

---

## 30.3 LCI：终身通信身份证的六层架构

### L0 — 人的终身根标识

根身份不直接暴露手机号码、邮箱或真实姓名。

```text
LCI Root
= stable public identifier
+ rotatable cryptographic keys
+ recovery policy
+ credential history
```

核心要求：

1. 根 ID 长期稳定；
2. 私钥可轮换；
3. 某把钥匙丢失不等于身份死亡；
4. 某家公司倒闭不等于身份死亡；
5. 某手机号回收不等于身份死亡。

### L1 — 密码学认证层

默认组合：

- 通行密钥（Passkey / WebAuthn / FIDO2）；
- 至少两把独立设备或硬件安全密钥；
- 离线恢复码；
- 高价值账号可使用 2-of-3 / 3-of-5 多方恢复；
- 本机 TPM / Secure Enclave / Android StrongBox 等作为密钥保护载体；
- 生物识别只负责本地解锁，不是云端身份根。

GitHub 当前官方做法已经说明这种模式的现实性：同步 Passkey 可由供应商账号恢复；device-bound Passkey 若设备丢失则无法恢复，因此官方建议至少在两个不同设备注册。

### L2 — 可验证凭证层

W3C 于 2025 年把 **Verifiable Credentials 2.0** 发布为 Recommendation，可用于：

- 年龄；
- 学历；
- 执照；
- 会员资格；
- 公司雇员身份；
- 政府证件派生证明；
- “只证明满 18 岁，不泄露生日”等选择性披露场景。

原则：

```text
证明所需事实
≠ 交出全部个人档案
```

### L3 — 可替换通信端点

```text
LCI
├─ +60 / +995 / +1 电话号
├─ 自有域名邮箱
├─ Gmail / Outlook / Proton alias
├─ 微信 / QQ / WhatsApp / Signal / Telegram
└─ 未来卫星直连 / 6G / 新协议
```

电话号码是**端点**，不是根身份。

若号码被回收：

```text
LCI 不变
→ 换绑定号码
→ 旧号码吊销
→ 账户不死亡
```

### L4 — 可迁移服务身份

```text
LCI
├─ 社交：Facebook / Instagram / Threads / 微博 / 小红书 / LinkedIn / ...
├─ 电商：淘宝 / 天猫 / 拼多多 / Shopee / Amazon / ...
├─ 代码：GitHub / GitLab / Gitea / Forgejo / ...
├─ AI：ChatGPT / Gemini / Claude / Grok / DeepSeek / ...
└─ 云：AWS / Azure / Google Cloud / Alibaba Cloud / ...
```

每项服务只应得到**最小必要凭证**。

### L5 — 用户数据金库（Personal Data Vault）

用户的：

- 联系人；
- 购买历史；
-代码项目；
- AI 偏好；
- 社交图谱；
- 账号恢复材料；
- 健康/金融等高敏数据；

不应默认汇成一个任何员工或任何模型都可查询的“全知人物画像”。

应采用：

```text
Encryption at rest
+ per-domain keys
+ purpose limitation
+ consent receipts
+ audit log
+ export
+ revoke
+ delete / archive policy
```

### L6 — 连续性与数字遗产

所谓“终身账号”必须预先回答：

- 公司倒闭怎么办？
- 用户 10 年不用怎么办？
- 用户失踪/死亡怎么办？
- 域名到期怎么办？
- 国家改号怎么办？
- 制裁/跨境法冲突怎么办？
- 服务商被收购怎么办？

因此必须有：

```text
Portability
+ Escrow
+ Open export format
+ Successor operator
+ Foundation takeover
+ Memorial / inheritance state
```

---

## 30.4 现有超级生态可以借鉴什么，不能照搬什么

> **注意**：以下按“产品生态”比较，不把创办人、品牌、投资关系与法定公司边界混成一个主体。

| 生态 | 可借鉴能力 | 不应照搬的风险 |
|---|---|---|
| Google / Alphabet | Google Account、Gmail、Android、Maps、YouTube、Cloud、AI 的统一入口 | 身份对单一供应商依赖；个人 Google Account 连续 2 年不活跃存在删除政策 |
| Meta / Zuckerberg 生态 | Facebook、Instagram、WhatsApp、Messenger、Threads、Meta AI 的社交图谱与通信协同 | 跨域画像、广告依赖、内容治理与单点账号风险 |
| 阿里巴巴及历史关联生态 | 淘宝、天猫、阿里云、菜鸟、企业/电商基础设施；蚂蚁等必须另按法人登记 | 不可把“生态协同”误写成所有数据/公司属同一主体 |
| Musk-related companies | SpaceX/Starlink、Tesla、X、xAI、Neuralink、Boring 等在连接、交通、AI、脑机上的互补 | 它们不是一个无边界共享数据库；法人、权限、数据目的必须拆开 |
| Microsoft | Microsoft Account、Windows、Azure、Outlook、GitHub、Microsoft 365、Copilot | 工作/开发/云身份高度耦合时需防 tenant / account 单点失败 |
| Tencent | 微信、QQ、云、游戏、支付等高频生活入口 | 社交、支付、身份合一后，恢复与风控误判影响面巨大 |
| Amazon | 电商、物流、AWS、设备与 AI | 商业、云与账户服务耦合后，账号治理必须分区 |

**本项目真正应学的是“统一入口 + 跨服务协同”，不是“集中掌控所有人的全部数据”。**

---

## 30.5 “全天下免费”到底是否可行？

先立一个经济学铁律：

```text
Free-to-user ≠ Free-to-operate
```

用户不付钱，不代表：

- 服务器免费；
- GPU 免费；
- 电力免费；
- 海底光缆/卫星免费；
- 号码资源免费；
- 反垃圾/反诈骗免费；
- 内容审核免费；
- 客服免费；
- KYC/合规免费；
- 灾备免费；
- AI 推理免费。

真正可行的方向是：

> **终身身份根永久免费；基础通信/邮箱/社交给足够生活使用的免费额度；重存储、重视频、重 AI、企业能力与商业交易由交叉补贴承担。**

---

## 30.6 全球规模基准：为什么必须先算 60 亿，而不是只算一家公司

国际电信联盟（ITU）《Facts and Figures 2025》估计：

- 2025 年约 **60 亿人**已经上网；
- 约占世界人口 **74%**；
- 约 **22 亿人**仍未联网。

因此：

```text
全球在线免费层：N ≈ 6.0B
真正“全人类”设计：N ≈ 8.2B
```

本件成本一律同时看 60 亿与 82 亿两个数量级。

---

## 30.7 成本模型：先算单位用户，再谈“永久免费”

### 30.7.1 母公式

```text
Annual Cost
=
Active Users × Variable Cost per User
+ Fixed Infra
+ Security / Fraud
+ Compliance
+ Support
+ R&D
+ Depreciation
+ Network / CDN / Telecom
```

任何宣称“永久免费”却不提供这张账的方案，一律不得进入生产。

### 30.7.2 四级规划包络

> **这是工程规划区间（planning envelope），不是云厂商报价。**
> 它用于回答“数量级是否现实”，并明确排除手机终端购置、最后一公里移动宽带、各国号码牌照、税费、版权采购与巨额欺诈损失等高度法域化项目。

| 层级 | 每活跃用户/年粗略规划包络 | 60 亿在线人口 | 82 亿全人口 | 内容 |
|---|---:|---:|---:|---|
| **A. LCI 身份核心** | **US$1.5–5** | **US$9–30B/年** | **US$12.3–41B/年** | 密钥、认证、凭证、恢复、低频日志、目录 |
| **B. 基础数字公共层** | **US$10–30** | **US$60–180B/年** | **US$82–246B/年** | 身份 + 基础邮箱 + 消息 + 少量存储 + 基础客服/风控 |
| **C. 完整免费基础生态** | **US$20–60** | **US$120–360B/年** | **US$164–492B/年** | 再加社交图文、代码基础托管、电商身份、有限 AI |
| **D. 重媒体 + 高额度 AI** | **US$80–250+** | **US$480B–1.5T+/年** | **US$656B–2.05T+/年** | 大视频、百 GB 级存储、语音/图像生成、高频大模型推理 |

### 30.7.3 为什么“无限免费 AI”最危险

传统邮箱、文本消息的边际成本可以极低；但生成式 AI 的成本高度取决于：

- 输入/输出 token；
- 模型尺寸；
- 推理时延；
- 上下文长度；
- 图像/视频/语音生成；
- GPU/加速器利用率；
- KV cache / memory；
- 峰谷负载；
- 安全过滤与重试。

因此“免费 AI”必须至少有：

```text
rate limit
+ daily / monthly compute credits
+ small-model routing
+ cache
+ batch
+ quantization
+ distillation
+ queue
+ premium overflow
```

否则少数重度用户即可把全民免费层拖垮。

---

## 30.8 用 2026 年全球巨头 CapEx 反校“规模感”

这些数字**不能直接当成 LCI 成本**，但能防止严重低估全球基础设施量级：

| 公司 | 2026 公开数据 | 本件用途 |
|---|---:|---|
| Meta | 2026 CapEx 指引 **US$130–145B** | 社交 + AI 亿级/十亿级基础设施量级参照 |
| Alphabet | 2026 CapEx 指引 **US$180–190B** | 搜索、云、视频、AI 的全球技术基础设施参照 |
| Amazon | 截至 2026 Q2 的 TTM property/equipment 净购置约 **US$169B** | AWS + 履约网络 + AI 资本密集度参照 |
| Microsoft | FY2026 Q4 单季 CapEx **US$41B** | 云 + AI 计算资本密集度参照 |

**严格限制**：

```text
Hyperscaler CapEx
≠ 某项服务的年度成本
≠ cost/user
≠ LCI 报价
```

只能说明：

> 全球规模 + AI + 云 + 视频 + 社交若全部“免费且高额度”，年度资本/运营需求必然进入**数百亿美元至数千亿美元**甚至更高量级。

---

## 30.9 真正“永久免费”的最难问题：谁付钱？

建议采用**六路交叉补贴**，而不是卖掉用户的隐私：

### 1. 企业 / 政府 / API 付费

个人基础身份免费：

```text
个人 Free
企业 API / SLA / Audit / Bulk Verification → 付费
```

### 2. 商家交易费

消费者：

```text
注册 / 搜索 / 下单 → 免费
```

商家：

```text
成交 / 广告 / 店铺 SaaS / 物流 → 付费
```

### 3. AI / 存储的 Freemium

```text
基础 AI：免费额度
高级模型 / 大上下文 / 视频生成：付费
基础存储：免费
超额存储：付费
```

### 4. Developer / App Marketplace

第三方开发者可围绕 LCI 建应用：

```text
identity free
marketplace revenue share
enterprise integrations paid
```

### 5. 公共服务 / Universal Service

对：

- 偏远地区；
- 低收入群体；
- 学生；
- 公益科研；

可由政府普遍服务基金、基金会或企业 ESG 共同补贴。

### 6. 广告只能“自愿、最小化、上下文式”

若必须广告变现：

```text
默认不出售敏感画像
不把健康/金融/政治/未成年人等敏感属性用于定向
用户可拒绝跨域画像
优先 contextual ads
```

**“为了免费所以必须掌控所有人”不是经济学必然，而是治理选择。**

---

## 30.10 为什么“掌控所有人的衣食住行”反而会毁掉终身身份

把：

```text
电话
+ 社交
+ 电商
+ AI
+ 支付
+ 位置
+ 健康
+ 代码
+ 工作
```

全部汇入一个超级数据库，会产生：

1. 单点泄露；
2. 单点误封；
3. 单点国家/企业滥权；
4. 内鬼攻击；
5. 画像歧视；
6. 账号接管后的“全人生接管”；
7. AI 错误推断被跨域传播。

所以本件采用：

```text
One Identity
≠ One Database
```

正确结构是：

```text
LCI Root
    │
    ├── Social Vault
    ├── Commerce Vault
    ├── Code Vault
    ├── AI Preference Vault
    ├── Health Vault
    └── Finance Vault
```

默认：

```text
separate keys
separate consent
separate purpose
separate retention
```

只有用户主动授权时，才产生临时跨域视图。

---

## 30.11 “终身账号”的合同与技术定义

**终身（Lifetime）不得定义成“公司永远不会倒”。**

应定义为：

> 只要用户未主动放弃，身份根就具备持续存在、可恢复、可迁移、可由继任运营体接管的制度与技术权利。

### 必须满足

| 条件 | 终身身份要求 |
|---|---|
| Inactivity | 不因多年不登录自动销毁根 ID；内容可转冷存储 |
| Company failure | 可迁移至 Foundation / successor |
| Phone loss | 不影响根 ID |
| Email loss | 不影响根 ID |
| Device loss | 有第二把 key / recovery |
| Provider ban | 有申诉、导出、迁移 |
| Death | memorial / heir / delete policy |
| Country change | 号码、地址、证件可更新 |
| Crypto break | key rotation / PQ migration |
| Name change | 人名可改，根 ID 不变 |

Google 当前个人账号有“连续两年不活跃可删除”的政策，因此它是“长期账号”，**不是本件定义的终身身份根**。

---

## 30.12 免费电话号为什么最难被纳入核心

电话号码：

- 属各国号码规划；
- 依赖运营商互联；
- 有 SIM/eSIM、短信、语音、紧急呼叫、反诈与实名要求；
- 不同国家号码成本、回收政策、携号转网制度不同。

因此 LCI 不应承诺：

> “全世界每个人永远免费占有一个受监管电话号码”

而应承诺：

```text
LCI 免费终身
+ 至少一个可绑定通信端点
+ 支持 MNP / number change
+ 旧号码撤销保护
```

在有公共资金/运营商合作的国家，可再提供免费或低价号码。

---

## 30.13 社交网、电邮、电商、代码托管与 AI 的“终身化”

### 社交

终身的是：

```text
handle
social graph export
posts export
follower/following portability
identity proof
```

不是某一家 UI。

### 电邮

最稳模式：

```text
LCI alias / own-domain alias
        ↓
可替换 Gmail / Outlook / Proton / 自建 MX
```

邮箱地址与托管商分离。

### 电商

终身保存：

- 商家/买家声誉凭证；
- 发票/收据；
- 保固；
- 地址簿；
- 支付 token 引用；

支付卡号、银行账户等仍分域保管。

### 科研代码托管

Git 本身天然支持多 remote：

```text
local repo
├─ GitHub
├─ GitLab
├─ Forgejo
└─ cold archive
```

因此“终身代码身份”的关键不是押注某个 Forge 永生，而是：

```text
canonical author identity
+ signed commits
+ mirror
+ archive
```

### AI

终身 AI 账号应该保存：

- 用户授权的偏好；
- 模型无关的记忆摘要；
- 数据许可；
- Agent 权限；
- 审计日志；

而不是把个人一生原始聊天永久裸存于某家公司。

---

## 30.14 身份恢复：连主人都“认不出”时怎么办？

本件建议最低恢复矩阵：

```text
Primary
├─ Passkey A（手机/电脑）
├─ Passkey B（另一设备）
└─ Hardware Key

Offline
├─ recovery codes
└─ encrypted recovery package

High assurance
├─ verified credential re-proof
├─ regulated in-person / video proofing（按法域）
└─ multi-party recovery
```

### 禁止

```text
SMS-only recovery
Face-only recovery
Fingerprint-only recovery
Single-device passkey only
Single-email recovery only
```

### 生物识别角色

```text
face / fingerprint
→ unlock a cryptographic authenticator
→ not replace the authenticator
```

---

## 30.15 若真的要“全人类免费”，可设双层组织

### A. LCI Foundation / 公益根层

职责：

- 根 ID；
- 开放标准；
- 公钥目录；
- 凭证格式；
- 迁移；
- 恢复规则；
- 开源参考实现；
- 停服接管。

原则：

```text
不可被一家商业公司出售
不可拿用户身份作抵押
不可因广告收入下降而销毁身份
```

### B. Commercial Service Federation / 商业服务联盟

Google、Meta、Alibaba、Tencent、Microsoft、Amazon、Starlink、电信运营商、银行、政府、大学、开源社区等均可：

```text
接入身份
提供服务
竞争价格
竞争体验
```

而不垄断根身份。

这比打造“一家公司掌控全世界”更耐久。

---

## 30.16 若只靠基金永久支付，资本需求有多大？

这是一个故意极端的压力测试。

若 LCI 核心层需要：

```text
US$12.3–41B / year
```

覆盖约 82 亿人口，而基金长期可持续支出率假设仅为 **4%/年**：

```text
Required Endowment
≈ Annual Cost / 0.04
≈ US$307.5B – 1.025T
```

这还只是**身份核心**，不含：

- 全球免费移动网络；
- 无限视频；
- 无限 AI；
- 免费硬件；
- 免费物流；
- 商家补贴。

因此：

> **“全人类、无限、免费、终身”若没有持续商业现金流，仅靠一次性资本极难成立。**

真正可行的是：

```text
终身身份免费
+ 基础数字生活免费
+ 重资源按量/会员/企业/商家付费
+ 弱势群体补贴
```

---

## 30.17 RedTeam

### RT-1：SIM Swap / 号码回收

若手机号仍是唯一恢复方式：

```text
LCI = FAIL
```

### RT-2：Passkey 供应商锁死

同步 Passkey 也可能依赖 Apple / Google / 密码管理器账号。

应至少保留一个**独立 device-bound hardware key**与离线恢复材料。

### RT-3：超级画像数据库

若所有域默认可互查：

```text
one breach → whole-life breach
```

直接违反本件架构。

### RT-4：免费 AI 成本攻击

自动化机器人可制造海量推理调用，必须：

- rate limit；
- proof-of-person / abuse controls；
- quota；
- queue；
- per-model budget。

### RT-5：Sybil / 批量假人

“永久免费”会刺激机器批量注册，需要：

```text
pseudonymous allowed
≠ unlimited anonymous resource consumption
```

身份唯一性、匿名性与资源公平必须拆开。

### RT-6：服务商倒闭

若没有：

- export；
- mirror；
- successor；
- open format；

“终身”只是一句营销词。

### RT-7：国家级封禁 / 数据主权冲突

全球一套数据库会直接撞上：

- 数据本地化；
- 隐私法；
- 电信法；
- 制裁；
- 未成年人；
- 内容法。

因此必须允许**区域数据平面 + 全球身份控制平面**分离。

---

## 30.18 Critic

### C-1：为什么不直接让 Google/Meta/Alibaba/Musk 做完？

因为：

```text
技术能力强
≠ 永久公共治理资格
```

上市公司有：

- 股东义务；
- 商业周期；
- 收购/拆分；
- 地缘限制；
- 产品关停；
- 账号政策变化。

### C-2：为什么不让电话号码就是终身 ID？

因为号码是：

- 可回收；
- 可改号；
- 受国家编号制度约束；
- 易受 SIM swap；
- 不适合无手机人群。

### C-3：为什么不直接用脸？

因为脸：

- 不可轮换；
- 不是秘密；
- 被泄露后无法“换一张脸”；
- 识别错误会误伤。

### C-4：为什么不把所有功能全部免费？

因为“无限免费”会把：

```text
稀缺 GPU / storage / bandwidth
```

变成无价格约束的公共池，最终通常只能靠：

- 广告画像；
- 强制限流；
- 隐性补贴；
- 服务降级；

其中至少一种兜底。

---

## 30.19 KillCritic：一票否决

任一条件成立，本件不得称“终身数字身份”：

1. 根身份只能靠手机号找回；
2. 根身份只能靠脸或指纹找回；
3. 服务商可无申诉永久删除根 ID；
4. 用户无法导出自己的凭证；
5. 公司停运后没有 successor / escrow；
6. 必须同意跨域行为画像才能使用免费基础身份；
7. AI 可默认读取所有社交、电商、健康、金融数据；
8. 没有 key rotation；
9. 没有账号接管后的全域撤销按钮；
10. 没有成本账，却承诺“无限永久免费”。

---

## 30.20 Blindspot

后续长期跟踪：

- 后量子 Passkey / WebAuthn 迁移；
- 可验证凭证的撤销与隐私泄露；
- 全球号码携带与卫星直连；
- 无国籍人士 / 难民数字身份；
- 未成年人终身 ID 与成年后的自主权；
- 数字遗产；
- AI Agent 身份与委托授权；
- 用户自托管与普通人可用性之间的冲突；
- EEG biometrics 的撤销性与模板保护；
- 深伪对远程身份核验的攻击；
- 国家间身份互认；
- 断网/灾难条件的离线凭证。

---

## 30.21 Cheatsheet

| 问题 | 当前正本 |
|---|---|
| 终身手机号能否当身份根？ | **不建议；号码只是端点** |
| 人脸/指纹能否当唯一主人钥匙？ | **不能；只作 MFA 的一环** |
| Passkey 是否更稳？ | **是，但须多设备/硬件备份** |
| EEG 能否认人？ | **研究上可；生产规模化仍有挑战** |
| 能否隔空读脑认主？ | **无成熟生产证据** |
| 终身电邮怎么做？ | **稳定 alias / 自有域名 + 可换托管商** |
| 终身社交怎么做？ | **身份与社交图谱可迁移，不押单一平台永生** |
| 终身代码怎么做？ | **签名身份 + 多 remote + archive** |
| 终身 AI 怎么做？ | **模型无关身份/授权/记忆摘要，可换模型供应商** |
| 全民免费是否可行？ | **基础层可，重媒体/重 AI 必须限额或交叉补贴** |
| 全部数据集中是否更方便？ | **方便但风险极高；采用分域 vault** |
| “免费”是否等于没有成本？ | **绝不等于** |

---

## 30.22 Blueprint

```text
                      ┌───────────────────────────┐
                      │  LCI Foundation / Trust  │
                      └─────────────┬─────────────┘
                                    │
                         Lifetime Root Identifier
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
              Passkeys        Hardware Keys    Recovery / VC
                  │                 │                 │
                  └─────────────────┼─────────────────┘
                                    │
                         User-Controlled Vault
                                    │
       ┌───────────┬───────────┬────┴────┬───────────┬───────────┐
       │           │           │         │           │           │
     Phone       Email       Social   Commerce      Code         AI
   endpoints    aliases      graph     receipts     forge      agents
       │           │           │         │           │           │
       └───────────┴───────────┴────┬────┴───────────┴───────────┘
                                    │
                         Portability / Export
                                    │
                   Competing Commercial Providers
```

治理：

```text
Global identity control plane
+
Regional data planes
+
Purpose-specific vaults
+
User consent
+
Open export
+
Auditable access
```

---

## 30.23 ActionPlan

### Phase 0 — 标准与宪法

先写“身份宪法”，不先写 App：

1. 根 ID 是否永久？
2. 谁能撤销？
3. 用户如何申诉？
4. 用户死亡后怎么办？
5. 国家命令和用户权利如何冲突？
6. 公司倒闭谁接管？
7. 哪些数据永远不可跨域？

### Phase 1 — 10 万用户原型

只做：

```text
LCI
+ 2 Passkeys
+ hardware-key optional
+ recovery
+ email alias
+ basic profile
+ export
```

先证明：

```text
account recovery success
key rotation
provider migration
zero data loss
```

### Phase 2 — 1,000 万用户

加入：

- messaging；
- social graph；
- commerce identity；
- code identity；
- limited AI。

核心 KPI：

```text
cost / MAU
recovery success rate
account takeover rate
false lockout rate
support tickets / 1k users
storage / MAU
egress / MAU
AI compute / MAU
abuse cost / MAU
```

### Phase 3 — 1 亿用户

实施：

- 多区域；
- multi-cloud；
- sovereign data plane；
- OpenID / VC federation；
- telecom number binding；
- fraud graph；
- independent audit。

### Phase 4 — 十亿级

只有当：

```text
基础层 cost/user 可预测
+
安全事件可控
+
跨国合规闭环
+
退出/迁移已真实演练
```

才扩张。

### Phase 5 — 全球公共数字层

目标不是：

> 一家公司拥有全世界人的全部资料。

而是：

> **所有人拥有一个不被某家公司绑死的长期数字身份，并可自由选择服务商。**

---

## 30.24 本节官方 / 一手 / 学术来源（截至 2026-09-30）

### 全球连接规模
- ITU — Facts and Figures 2025：约 60 亿人在线、约 22 亿人离线  
  https://www.itu.int/itu-d/reports/statistics/2025/10/15/ff25-internet-use/
- ITU — Global Connectivity Report 2025  
  https://www.itu.int/itu-d/reports/statistics/global-connectivity-report-2025/

### 身份 / Passkey / 生物识别
- NIST SP 800-63B / Digital Identity Guidelines — Authenticators / Biometrics  
  https://pages.nist.gov/800-63-4/sp800-63b/authenticators/
- FIDO Alliance — The State of Passkeys 2026  
  https://fidoalliance.org/the-state-of-passkeys-2026-global-consumer-and-workforce-report/
- GitHub Docs — Managing your passkeys  
  https://docs.github.com/en/authentication/authenticating-with-a-passkey/managing-your-passkeys
- GitHub Docs — 2FA Recovery  
  https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/recovering-your-account-if-you-lose-your-2fa-credentials

### 可验证凭证
- W3C — Verifiable Credentials 2.0 Recommendation（2025-05-15）  
  https://www.w3.org/TR/vc-data-model/
- W3C — VC 2.0 官方新闻  
  https://www.w3.org/news/2025/the-verifiable-credentials-2-0-family-of-specifications-is-now-a-w3c-recommendation/

### 账号生命周期
- Google — Inactive Google Account Policy（个人账号连续 2 年不活跃可删除）  
  https://support.google.com/accounts/answer/12418290

### 神经科技 / EEG
- Neuralink — PRIME Study Progress Update（N1：1,024 electrodes / 64 threads）  
  https://neuralink.com/updates/prime-study-progress-update/
- PubMed — Brain-Computer Interface for EEG-Based Authentication（2025）  
  https://pubmed.ncbi.nlm.nih.gov/40871810/
- PubMed — Brain Signal for Secure EEG Biometric Authentication: A Comprehensive Survey（2026）  
  https://pubmed.ncbi.nlm.nih.gov/42451287/

### 2026 全球基础设施量级参照
- Meta Q2 2026：2026 CapEx 指引 US$130–145B  
  https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/
- Alphabet June 2026 Investor Presentation：2026 CapEx US$180–190B  
  https://blog.google/alphabet/investor-presentation-june-2026/
- Amazon Q2 2026 Results：TTM property/equipment 净购置约 US$169B  
  https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results/default.aspx
- Microsoft FY2026 Q4 Earnings：单季 CapEx US$41B  
  https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4

---

## 30.25-A 实证锚（新增 · v1.2.2 · 本节架构之经验证据层）

> §30 为**架构设计**（LCI 六层、成本模型、治理组织）；§10.5.5 为**实证对照**（已运行的真实体系）。二者互补，不重复。

| §30 之设计主张 | §10.5.5 之现实印证 | 证据等级 |
|---|---|---|
| L0 终身根标识不应暴露号码/邮箱/真名 | **DoD EDIPI**：10 位，前 9 位自 `100000000` 顺序分配，**终身且永不重分配**；跨军种、跨退役、跨文职、跨承包商不变 | **P0·M5 已运行** |
| L1 密码学认证层 | **CAC 之 PKI 证书**；**EUDI 钱包**（Regulation (EU) 2024/1183） | P0·M5 / P0·M3 |
| L2 可验证凭证层 | **eIDAS 2.0 之 VC + W3C DID**，三铁律：选择性披露 · 无中心化数据系统 · 用户控制 | P0·M3 |
| L4 可迁移服务身份 | **ORCID / ISNI**（同一套 16 位格式，已互通备忘录） | P1·M5 |
| §30.12 不得承诺人人永久免费号码 | **英国 070**：可任意重路由的「终身号码」**沦为诈骗号段**；**RNK Phone for Life** 8 年后 Chapter 7 清算 | P1·M5 |
| §30.11 终身账号的合同定义 | **TRAI 官方定义**：「终身」＝ **运营商牌照有效期**，非人的一生 | **P0·M5** |
| MNP 是可携不是永久 | **菲律宾 RA 11202**：免费永久号码，**前提是已结清所有义务** → 抗换商，不抗欠费 | P0·M5 |
| §30.13「科研代码托管」需 canonical author identity | **ORCID 即该身份的现成国际实现** | P1·M5 |

### 30.25-A.1 一条此前未画出的分水岭

```text
租用命名空间（必失效）        自有命名空间（可终身）
────────────────────        ────────────────────
电话号码 (ITU E.164)          DoD EDIPI
免费邮箱地址                  ORCID / ISNI
平台账号                      自有域名
社交媒体 handle               密码学密钥对
```

**所有顶尖体系的共同动作，就是从左栏搬到右栏。**
**LCI 的全部价值，可以用一句话概括：为没有自有命名空间的人，提供一个自有命名空间。**

---

## 30.25 本节一句话结论

> **“终身免费数字生活”真正可行的核心不是让一家巨头永久掌控所有人的电话、邮箱、社交、电商与 AI，而是建立一个永久免费、可恢复、可迁移、密码学可验证的终身身份根，再让商业服务商围绕它竞争；重 AI、重视频、重存储依靠配额与交叉补贴，个人敏感数据则保持分域、加密、用户授权。**

## 29.5 v1.2.2 实证强化（2026-09-30）

> **本版任务**：把本轮查证所得的顶尖体系实证并入，并补上全件缺失的标准框架锚。**零删减**——§30 全章、§10.4 Speedtest 专题、C-DAQIN-04~36 全数保留。

| # | 新增/改动 | 位置 | 类别 |
|---|---|---|---|
| 1 | **§0.6 标准框架锚**（三层永久区分 + 十二项标准清单 + eIDAS 85 天告警） | §0.6 | **全件此前缺失** |
| 2 | **§10.5.3 三层锚 → 五层锚**（新增 **L0 命名空间产权**） | §10.5.3 | 升级 |
| 3 | **§10.5.5 顶尖体系实证对照**（A–J 十节） | §10.5.5 | 新增 |
| 4 | §10.5.4 补第 7、8 项（ORCID / L0 域名） | §10.5.4 | 补充 |
| 5 | **§30.25-A 实证锚**（§30 架构 ↔ §10.5.5 实证之八行映射 + 分水岭图） | §30 | 新增，交叉引用非重复 |
| 6 | C-DAQIN-37 ～ 42 | §1.3.3 | 新增 |
| 7 | U-23 ～ U-27 | §27.1 | 新增 |
| 8 | SC-ζ / SC-η / SC-θ | §29.6 | 新增 |

### 29.5.1 本版之实证清单（全部本轮一手核实）

| 实证 | 结论 | 等级 |
|---|---|---|
| **DoD EDIPI** | 10 位，前 9 位自 100000000 顺序分配，**终身且永不重分配** | **P0·M5** |
| **eIDAS 2.0** | Reg (EU) 2024/1183；27 国 **2026-12-24** 法定上线；私营方 36 个月内接受 | **P0·M3→M4** |
| **ORCID / ISNI** | 同一套 16 位格式；已签互通备忘录 | P1·M5 |
| **英国 070** | 可重路由「终身号码」沦为诈骗号段 | P1·M5 |
| **RNK Phone for Life** | 2004 推出 → **2012-11-13 Chapter 7 清算**，存续 8 年 | **P0·M5** |
| **TRAI 官方定义** | 「终身」＝ 运营商牌照有效期 | **P0·M5** |
| **菲律宾 RA 11202** | 20:0 通过；免费永久号码，**前提已结清所有义务** | **P0·M5** |

## 29.6 自我更正登记（SC 系列 · 不得静默修订）

| 编号 | 前次主张 | 斧正 |
|---|---|---|
| **SC-ζ** | 把 RNK「Phone for Life」归入「不是号码」一类 | **错误，撤回。** 该方案明确包含电话号码、911/411 与携号转入。正确的证伪理由不是「没给号码」，而是「**给了号码，但公司八年后被清算**」 |
| **SC-η** | 称 RNK 为「早期 VoIP 方案」，年份含糊 | 确切为 **2004 年 11–12 月推出，2012 年 11 月 13 日转 Chapter 7 清算** |
| **SC-θ** | 把 eIDAS「无中心化数据系统」误读为「无中心化签发」 | **错误，撤回。** 实为**不建中心化属性库**；唯一性仍由成员国签发机构保证。二者是不同的事 |
| **SC-ι** | 以菲、印为例被质疑为「锚定小国」 | **理由须前置说明而非事后辩解**：那是全天下**仅有两个把此题写进公开监管正文并作出裁定**的司法管辖区。本版已于 §10.5.5 开篇显式声明此方法论前提 |

## 29.7 本版未做之事（显式登记，避免误以为已完成）

| 项 | 状态 |
|---|---|
| X-21 `OGDIL` 全称裁定 | **仍悬置** |
| AERO-02 §六.2 分层改写（草案已备） | **仍悬置** |
| §26 改 `{{< include >}}` + 指纹校验 | **仍悬置** |
| U-13 `Aerospace…qmd` 之 AERO-01/02 | **仍未解**，该件仍为附录级 |
| §27.3 主体侧数据清除 | **须主体本人执行**，非文档可代 |
| U-27 ORCID 申请 | **须主体本人执行** |
