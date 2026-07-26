# OGDIL Roadmap

## Versioning Strategy

We follow **Semantic Versioning**: `v0.1.0 → v1.0.0`

---

## Phase Overview

| Phase | Focus | Estimated Duration | Target Version |
|-------|-------|--------------------|----------------|
| Phase 1 | Data Foundation | 4 weeks | v0.3 |
| Phase 2 | Feature Store | 4 weeks | v0.4 |
| Phase 3 | Statistics Lab | 6 weeks | v0.5 |
| Phase 4 | Machine Learning | 6 weeks | v0.6 |
| Phase 5 | Decision Intelligence | 8 weeks | v1.0 |

---

## Detailed Roadmap

### Phase 1 — Data Foundation (v0.2 → v0.3)
- [ ] Complete ODS → DWD → DWS → ADS architecture
- [ ] Implement `ads_customer360`
- [ ] Data Quality Rules & Contracts
- [ ] Basic ETL pipelines

### Phase 2 — Feature Store (v0.4)
- [ ] Feature Dictionary (≥300 features initially, target 500+)
- [ ] Feature Store implementation
- [ ] Point-in-time correct features
- [ ] Feature documentation & ownership

### Phase 3 — Statistics Laboratory (v0.5)
- [ ] Bayesian Models (brms / Stan)
- [ ] Survival Analysis (Cox, RSF, Joint Models)
- [ ] Hierarchical Linear Models (HLM / GLMM)
- [ ] Time Series
- [ ] Causal Inference
- [ ] A/B Testing Framework

### Phase 4 — Machine Learning Laboratory (v0.6)
- [ ] XGBoost / LightGBM / CatBoost
- [ ] Deep Learning baselines
- [ ] Graph Neural Networks (GNN)
- [ ] AutoML pipelines
- [ ] Model Registry & Monitoring

### Phase 5 — Decision Intelligence Platform (v1.0)
- [ ] Shiny / Positron Decision Platform
- [ ] Experiment Registry (full scientific workflow)
- [ ] Knowledge Graph
- [ ] Docker one-click deployment
- [ ] GitHub Pages official website
- [ ] API services
- [ ] Production-ready monitoring

---

## OGDIL v1.0 Success Criteria

- ✅ Enterprise-grade Data Warehouse (ODS → ADS)
- ✅ Customer360
- ✅ Feature Store (≥500 features)
- ✅ R Package + Python SDK
- ✅ Positron Project
- ✅ Shiny Decision Platform
- ✅ Docker deployment
- ✅ Experiment Management System
- ✅ Decision Intelligence capabilities

---

## Current Status

**v0.1.0** — Project initialization & Charter (Current)

Next: **v0.2** — Full project infrastructure + Development Standards + CI skeleton.