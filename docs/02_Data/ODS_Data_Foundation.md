# OGDIL ODS Data Foundation

Version: 0.2.0  
Date: 2026-07-26  
Status: Active / Foundation Draft

## 1. Purpose

本文件定义 Online Gaming Decision Intelligence Lab（OGDIL）的 ODS 数据基础层治理原则，并作为 `01_ODS_TABLE_LIST.csv` 与 `02_ODS_FULL_DATA_DICTIONARY.csv` 的上层规范。

ODS（Operational Data Store）是 OGDIL 的 **Truth Layer**。ODS 负责保留来源系统语义、来源表关系、同步元数据与可追溯性；业务分析、机器学习、统计建模与决策应用不得直接依赖未经治理的原始业务表。

总体链路：

```text
Source Systems
    ↓
ODS / Truth Layer
    ↓
DWD / Atomic Detail
    ↓
DWS / Subject Aggregation
    ↓
ADS / Decision Data Products
    ↓
AI · Statistics · Quant · BI · Decision Intelligence
```

## 2. Source Metadata Contract

当前 ODS 表统一采用以下治理字段：

| Field | Meaning | Rule |
|---|---|---|
| `__source_pk` | 源行唯一键 | 优先源主键/唯一键 MD5；无主键时使用整行 MD5 |
| `dt` | StarRocks 日分区日期 | 优先来源业务时间；无时间字段时使用同步当天 |
| `source_db` | 来源库 | 保留来源数据库标识 |
| `source_table` | 来源表 | 保留来源表名 |
| `ods_table_name` | ODS 表名 | 记录目标 ODS 表 |
| `sync_time` | 同步时间 | 记录进入 ODS 的同步时间 |

## 3. Data Dictionary Authority

OGDIL 的 ODS 数据字典以以下两个文件作为基础资产：

- `01_ODS_TABLE_LIST.csv`：ODS 表级目录与资产清单。
- `02_ODS_FULL_DATA_DICTIONARY.csv`：ODS 字段级数据字典、来源类型与业务说明。

任何 DWD/DWS/ADS 设计都应能够回溯到这两个资产中的来源表与字段。若字段语义无法由数据字典支持，应标记为 `TBD`，不得在数据产品中静默推断为确定业务含义。

## 4. Initial Subject Domains

基于当前已整理的 ODS 表命名与字段语义，建议建立以下主题域。该分类用于数据架构导航，不改变来源系统原始语义：

1. **Identity & Access**：权限群组、角色、子代理权限关系。
2. **Game & Table Operations**：游戏、桌台、洗牌、桌台限制与第三方桌台。
3. **Betting & Real-time Activity**：实时投注、实时大厅、投注相关活动。
4. **Wallet & Financial Operations**：钱包明细、反馈错误、报告处理状态。
5. **Risk & Governance**：风险名单、白名单及相关治理信息。
6. **Configuration & Platform**：站点、SMS、Stream、URL、Symbol 等配置资产。
7. **Operational Monitoring**：实时日志、状态与系统运行指标。
8. **Reference / Temporary Assets**：临时 ID 列表及其他辅助性表。

主题域仅用于后续 DWD/DWS/ADS 建模；ODS 层仍保持一表一来源的可追溯原则。

## 5. High-value Analytical Domains

在进入 DWD/DWS/ADS 之前，应优先围绕以下分析方向建立数据产品：

### 5.1 Customer / Player 360

目标：形成用户、代理、游戏行为、资金行为与风险状态的统一实体视图。

候选能力：

- 用户生命周期
- 活跃度与留存
- 游戏偏好
- 投注行为
- 钱包资金行为
- 风险状态
- 代理关系

### 5.2 Risk Intelligence

目标：支持风险识别、异常检测与可解释决策。

候选能力：

- 风险名单关联
- 白名单治理
- 异常投注模式
- 钱包交易异常
- 高频失败/重试行为
- 实时行为风险特征

### 5.3 Gaming Operations Intelligence

目标：支持游戏、桌台、洗牌、第三方供应商与运营效率分析。

候选能力：

- 桌台利用率
- 游戏运营效率
- 第三方桌台状态
- 洗牌流程时长
- 荷官/流程状态分析
- 桌台限额与下注行为关联

### 5.4 Wallet Intelligence

目标：建立资金处理链路的可观测性与异常分析能力。

候选能力：

- 加点/扣点/余额查询
- 请求与响应延迟
- 交易成功率
- 失败与回滚
- 反馈错误率
- 重试行为

## 6. Sensitive Data Governance

数据字典中可能出现密码、API Key、Secret Key、钱包与资金信息、IP、User-Agent、URL、手机号等敏感或高风险字段。

治理要求：

- ODS 可以按合规要求保留原始字段，但访问必须实施最小权限。
- DWD/DWS/ADS 默认不得暴露明文凭据。
- 密码、API Key、Secret Key 等字段原则上禁止进入分析特征。
- IP、User-Agent、手机号等字段进入分析层前应完成脱敏、哈希或受控访问设计。
- 任何公开科研数据集必须去标识化，并进行隐私风险审查。

## 7. Data Quality Rules

所有进入 DWD 的 ODS 表至少应检查：

1. 主键/唯一键稳定性。
2. `__source_pk` 非空率与唯一性。
3. `dt` 合法性与分区覆盖范围。
4. `sync_time` 新鲜度。
5. 来源字段类型转换失败率。
6. 时间字段时区一致性。
7. 金额字段精度与异常值。
8. 枚举状态值是否超出字典定义。
9. 重复记录率。
10. 源表到 ODS 的行数对账。

## 8. DWD Modeling Rules

DWD 层应：

- 保留来源主键语义。
- 保留必要的来源追踪字段。
- 对来源 `varchar` 类型进行可验证的业务类型转换。
- 时间字段统一时区策略。
- 金额字段使用精确数值类型，不使用浮点近似表示财务金额。
- 枚举与状态字段建立代码字典。
- 对无法可靠转换的字段保留原始值并记录质量异常。

## 9. DWS / ADS Direction

建议优先建设以下数据产品：

- `ads_customer360`
- `ads_player_lifecycle`
- `ads_betting_behavior`
- `ads_wallet_risk`
- `ads_real_time_risk`
- `ads_game_table_operations`
- `ads_vendor_operations`
- `ads_data_quality_monitoring`

每一张 ADS 表必须建立 Data Contract，包括 Owner、Description、Primary Key、Refresh Frequency、Quality Rules、Business Rules 与 Statistic Rules。

## 10. Scientific Research Boundary

OGDIL 的研究与模型必须区分：

- **Observed facts**：ODS/DWD 中直接观测的数据。
- **Derived features**：DWS/Feature Store 计算得到的特征。
- **Predictions**：模型输出的预测概率或评分。
- **Decisions**：业务策略或自动化动作。

不得将模型预测当作事实，也不得在没有标签定义、时间窗口与验证设计的情况下宣称存在“欺诈”“风险”或“因果效果”。

## 11. Next Engineering Tasks

1. 将 `01_ODS_TABLE_LIST.csv` 与 `02_ODS_FULL_DATA_DICTIONARY.csv` 纳入 `data_dictionary/`。
2. 自动生成 ODS 表级目录、字段级目录与主题域映射。
3. 生成敏感字段目录。
4. 生成 ODS → DWD 血缘映射模板。
5. 建立数据质量规则 SQL。
6. 建立 `ads_customer360` Data Contract。
7. 建立 Feature Store 的 point-in-time correctness 规范。
8. 建立 CI 检查：字典完整性、命名规范、Data Contract 完整性。

## 12. Traceability Principle

任何 ADS 指标必须能够沿以下路径追溯：

```text
ADS Metric
  ↓
DWS Feature
  ↓
DWD Column
  ↓
ODS Column
  ↓
Source Table
  ↓
Source Database
```

这条链路是 OGDIL 实现可复现、可解释与可审计决策智能的基础。
