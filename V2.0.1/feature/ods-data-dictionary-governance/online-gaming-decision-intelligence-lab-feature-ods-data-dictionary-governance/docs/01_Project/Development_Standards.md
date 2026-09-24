# OGDIL 开发规范

版本：0.1.0

---

## 1. 分支策略

| 分支 | 用途 |
|--------|---------|
| `main` | 稳定的生产就绪代码 |
| `develop` | 日常集成分支 |
| `feature/customer360` | 客户360（Customer360）模块 |
| `feature/feature-store` | 特征存储 |
| `feature/statistics` | 统计建模 |
| `feature/ml` | 机器学习 |
| `feature/dashboard` | 可视化 |
| `feature/api` | API 服务 |

**规则**：
- 禁止直接向 `main` 提交
- 所有功能必须通过 Pull Request 合并
- 合并前至少需要一次评审

---

## 2. 语言规范

### R
- 风格规范：`styler`
- 静态检查：`lintr`
- 可复用代码优先采用 Package 结构
- 依赖管理统一使用 `renv` 或 `pak`

### Python
- 格式化工具：`black` + `ruff`
- 测试框架：`pytest`
- 鼓励使用类型标注（Type Hints）
- 依赖管理统一使用 `uv` 或 `poetry`

### SQL
- 命名规范：`snake_case`
- 分层前缀：`ods_`、`dwd_`、`dws_`、`ads_`
- 每张 ADS 表必须有数据契约（Data Contract）
- 复杂逻辑必须添加注释

---

## 3. 文档规范

- 所有公开函数必须有文档说明
- 架构图统一使用 Markdown + Mermaid
- 每个主要模块必须有一份 `README.md`
- ADS 表必须提供数据契约（Data Contract）

---

## 4. 测试要求

- 核心函数必须有单元测试
- 数据管道必须有集成测试
- 统计模型必须提供验证报告
- 最低覆盖率目标：按模块另行制定

---

## 5. 版本管理

采用**语义化版本**（Semantic Versioning）：

- `主版本号.次版本号.修订号`
- 示例：`v0.1.0` → `v0.2.0` → `v1.0.0`

---

## 6. 提交信息规范

```
类型(范围): 描述

feat: 新功能
fix: 缺陷修复
docs: 文档变更
style: 代码格式调整
refactor: 代码重构
test: 新增测试
chore: 日常维护
```

---

## 7. 数据契约模板（ADS）

每张 ADS 表必须定义：

- **责任人（Owner）**
- **说明（Description）**
- **主键（Primary Key）**
- **刷新频率（Refresh Frequency）**
- **质量规则（Quality Rules）**
- **业务规则（Business Rules）**
- **统计规则（Statistic Rules）**

---

**以上规范为 OGDIL 所有贡献的强制要求。**
