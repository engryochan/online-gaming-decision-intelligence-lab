# OGDIL Charter
**Online Gaming Decision Intelligence Lab**

Version: 0.1.0  
Date: 2026-07-26  
Status: Active

---

## 1. Mission

建立一个以**统计科学、人工智能、因果推断、决策智能**为核心的开放式研究实验室，开发可验证、可部署、可持续迭代的数据科学方法与平台，服务在线游戏平台，并可迁移至电商、金融科技、SaaS 等领域的决策支持。

## 2. Vision

**五年目标**：建立世界级 **Online Decision Intelligence Research Platform**。

核心能力包括：

- **Customer360**：完整会员画像与生命周期
- **Decision Intelligence**：可落地的决策支持系统
- **Bayesian AI**：贝叶斯统计与不确定性量化
- **Causal AI**：因果推断与干预效果评估
- **Survival AI**：生存分析与流失预测
- **Experiment Platform**：科学实验注册与管理系统
- **Knowledge Graph**：实体关系与知识推理

## 3. Scientific Principles

所有研究与工程必须严格遵循：

| Principle | Description |
|-----------|-------------|
| **Reproducible** | 任何结果必须可被他人完整复现 |
| **Explainable** | 模型与决策过程必须可解释 |
| **Testable** | 代码与假设必须可测试 |
| **Deployable** | 研究成果必须能部署到生产环境 |
| **Scalable** | 架构与方法必须支持规模扩展 |

## 4. Data Architecture Principle

**ODS is the Truth Layer.**

```
Source → ODS (Truth) → DWD → DWS → ADS → Applications
```

- 所有分析、AI、Dashboard、Positron **只允许读取 ADS**
- 禁止直接查询原始业务表（如 `bet01`）
- 每张 ADS 表必须有完整 Data Contract

## 5. Research Workflow

每一个科学实验必须遵循：

```
Experiment ID
    ↓
Question
    ↓
Hypothesis
    ↓
SQL / Data Extraction
    ↓
EDA
    ↓
Statistics
    ↓
Machine Learning
    ↓
Bayesian / Causal Analysis
    ↓
Validation
    ↓
Conclusion
    ↓
Deployment
```

## 6. Governance

- 使用 Semantic Versioning
- 采用 GitHub 企业级分支策略（main / develop / feature/*）
- 强制 Code Review
- 强制文档与测试覆盖

## 7. Scope

**In Scope**：
- 在线游戏决策智能
- 可迁移至电商、金融科技、SaaS 的方法

**Out of Scope**（初期）：
- 纯前端产品开发
- 非数据驱动的运营工具

---

**This Charter is the foundational document of OGDIL.**  
All contributors must adhere to its principles.