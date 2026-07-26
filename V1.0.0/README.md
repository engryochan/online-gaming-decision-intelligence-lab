# OGDIL —— 在线游戏决策智能实验室

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)]()
[![Version](https://img.shields.io/badge/Version-v0.1.0-orange.svg)]()

---

## 使命

建立一个以**统计科学、人工智能、因果推断、决策智能**为核心的开放式研究实验室，开发可验证、可部署、可持续迭代的数据科学方法与平台，服务在线游戏平台，并可迁移至电商、金融科技、SaaS 等领域的决策支持。

## 愿景（五年目标）

建立世界级**在线决策智能研究平台**，包含：

- **客户360（Customer360）**：完整会员画像与生命周期
- **决策智能（Decision Intelligence）**：可落地的决策支持系统
- **贝叶斯智能（Bayesian AI）**：贝叶斯统计与不确定性量化
- **因果智能（Causal AI）**：因果推断与干预效果评估
- **生存智能（Survival AI）**：生存分析与流失预测
- **实验平台（Experiment Platform）**：科学实验注册与管理系统
- **知识图谱（Knowledge Graph）**：实体关系与知识推理

## 科学原则

所有代码与研究必须符合：

- ✅ **可复现**
- ✅ **可解释**
- ✅ **可测试**
- ✅ **可部署**
- ✅ **可扩展**

## 仓库结构

```
online-gaming-decision-intelligence-lab
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── ROADMAP.md
├── docs/
│   └── 01_Project/
│       ├── OGDIL_Charter.md
│       └── Development_Standards.md
├── sql/                  # ODS → DWD → DWS → ADS
├── R/                    # 统计建模
├── python/               # AI / 机器学习 / 特征工程
├── dashboards/           # Superset / Shiny / Positron
├── experiments/          # 科学实验注册表
├── feature_store/        # 特征字典与特征存储
├── models/               # 已训练模型
├── notebooks/            # 探索性分析
├── tests/                # 单元测试与集成测试
├── deployment/           # CI/CD 与部署配置
├── docker/               # 容器化
└── website/              # GitHub Pages
```

## 数据架构

```
源系统
      ↓
     ODS   （真相层）
      ↓
     DWD   （明细数据仓库）
      ↓
     DWS   （汇总数据仓库）
      ↓
     ADS   （应用数据服务）
      ↓
  AI / 仪表盘 / Positron / 决策平台
```

**规则**：所有分析、AI 与仪表盘**只允许读取 ADS**。

## 快速开始

1. 克隆本仓库
2. 阅读 `docs/01_Project/OGDIL_Charter.md`
3. 按照 `ROADMAP.md` 执行
4. 从 `ads_customer360` 模块开始

## 开发流程

- `main` → 稳定生产分支
- `develop` → 日常集成分支
- `feature/*` → 功能分支

## 联系与贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

**OGDIL v0.1.0** | 以科学的严谨与工程的卓越构建。
