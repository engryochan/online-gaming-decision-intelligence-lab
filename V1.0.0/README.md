# Online Gaming Decision Intelligence Lab (OGDIL)

**World-class Online Decision Intelligence Research Platform**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)]()
[![Version](https://img.shields.io/badge/Version-v0.1.0-orange.svg)]()

---

## Mission

建立一个以**统计科学、人工智能、因果推断、决策智能**为核心的开放式研究实验室，开发可验证、可部署、可持续迭代的数据科学方法与平台，服务在线游戏平台，并可迁移至电商、金融科技、SaaS 等领域的决策支持。

## Vision (5-Year Goal)

建立世界级 **Online Decision Intelligence Research Platform**，包含：

- Customer360
- Decision Intelligence
- Bayesian AI
- Causal AI
- Survival AI
- Experiment Platform
- Knowledge Graph

## Scientific Principles

所有代码与研究必须符合：

- ✅ **Reproducible**（可复现）
- ✅ **Explainable**（可解释）
- ✅ **Testable**（可测试）
- ✅ **Deployable**（可部署）
- ✅ **Scalable**（可扩展）

## Repository Structure

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
├── R/                    # Statistical modeling
├── python/               # AI / ML / Feature engineering
├── dashboards/           # Superset / Shiny / Positron
├── experiments/          # Scientific Experiment Registry
├── feature_store/        # Feature Dictionary & Store
├── models/               # Trained models
├── notebooks/            # Exploratory analysis
├── tests/                # Unit & integration tests
├── deployment/           # CI/CD & deployment configs
├── docker/               # Containerization
└── website/              # GitHub Pages
```

## Data Architecture

```
Source Systems
      ↓
     ODS   (Truth Layer)
      ↓
     DWD   (Detail Warehouse)
      ↓
     DWS   (Summary Warehouse)
      ↓
     ADS   (Application Data Service)
      ↓
  AI / Dashboard / Positron / Decision Platform
```

**Rule**: All analysis, AI, and dashboards **must only read from ADS**.

## Quick Start

1. Clone the repository
2. Read `docs/01_Project/OGDIL_Charter.md`
3. Follow `ROADMAP.md`
4. Start with `ads_customer360` module

## Development Workflow

- `main` → Stable production
- `develop` → Daily integration
- `feature/*` → Feature branches

## Contact & Contribution

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**OGDIL v0.1.0** | Built with scientific rigor and engineering excellence.