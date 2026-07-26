#!/usr/bin/env python3
"""
OGDIL v0.2 项目生成器
生成 online-gaming-decision-intelligence-lab 完整骨架
"""

import os
from pathlib import Path

# 基础目录
BASE = Path("online-gaming-decision-intelligence-lab")
BASE.mkdir(exist_ok=True)

# ---------- 目录结构 ----------
directories = [
  "docs/01_Project",
  "docs/02_Architecture",
  "docs/03_Data_Dictionary",
  "docs/04_Research",
  "sql/ods",
  "sql/dwd",
  "sql/dws",
  "sql/ads",
  "sql/etl",
  "sql/quality",
  "R/R",
  "R/man",
  "R/tests",
  "python/src/ogdil",
  "python/tests",
  "dashboards",
  "experiments",
  "feature_store",
  "models",
  "notebooks",
  "tests",
  "deployment",
  "docker",
  "website",
  ".github/workflows",
  ".github/ISSUE_TEMPLATE",
]

for d in directories:
  (BASE / d).mkdir(parents=True, exist_ok=True)

# ---------- 文件内容 ----------
files = {}

# 1. 根目录文档
files[".gitignore"] = """# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# R
.Rproj.user
.Rhistory
.RData
.Ruserdata
*.Rproj

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
*.tmp
data/
output/
"""

files[".editorconfig"] = """root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{md,yml,yaml}]
indent_size = 2

[*.{R,r}]
indent_size = 2

[*.py]
indent_size = 4
"""

files["README.md"] = """# OGDIL – Online Gaming Decision Intelligence Lab

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![R](https://img.shields.io/badge/R-4.3-blue)](https://www.r-project.org/)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)

**OGDIL** is an open research laboratory focused on **statistical science**, **artificial intelligence**, **causal inference**, and **decision intelligence**. We build verifiable, deployable, and iterable data science methodologies and platforms for online gaming, e-commerce, fintech, and SaaS.

## 🚀 Mission
Establish a research lab that develops **reproducible**, **explainable**, **testable**, **deployable**, and **scalable** data science solutions.

## 🔭 Vision (5-year)
Build a world-class **Online Decision Intelligence Platform** comprising:
- Customer360
- Decision Intelligence
- Bayesian AI
- Causal AI
- Survival AI
- Experiment Platform
- Knowledge Graph

## 📁 Repository Structure