# OGDIL Development Standards

Version: 0.1.0

---

## 1. Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable production-ready code |
| `develop` | Daily integration branch |
| `feature/customer360` | Customer360 module |
| `feature/feature-store` | Feature Store |
| `feature/statistics` | Statistical modeling |
| `feature/ml` | Machine Learning |
| `feature/dashboard` | Visualization |
| `feature/api` | API services |

**Rules**:
- Never commit directly to `main`
- All features must go through Pull Request
- Require at least one review before merge

---

## 2. Language Standards

### R
- Style: `styler`
- Linting: `lintr`
- Package structure preferred for reusable code
- Always use `renv` or `pak` for dependency management

### Python
- Formatter: `black` + `ruff`
- Testing: `pytest`
- Type hints encouraged
- Use `uv` or `poetry` for dependency management

### SQL
- Naming: `snake_case`
- Layer prefix: `ods_`, `dwd_`, `dws_`, `ads_`
- Every ADS table must have a Data Contract
- Comments required for complex logic

---

## 3. Documentation Standards

- All public functions must have documentation
- Use Markdown + Mermaid for architecture diagrams
- Every major module must have a `README.md`
- Data Contracts are mandatory for ADS tables

---

## 4. Testing Requirements

- Unit tests for core functions
- Integration tests for data pipelines
- Statistical models must have validation reports
- Minimum coverage target: to be defined per module

---

## 5. Versioning

Follow **Semantic Versioning**:

- `MAJOR.MINOR.PATCH`
- Example: `v0.1.0` → `v0.2.0` → `v1.0.0`

---

## 6. Commit Message Convention

```
type(scope): description

feat: new feature
fix: bug fix
docs: documentation
style: formatting
refactor: code restructuring
test: adding tests
chore: maintenance
```

---

## 7. Data Contract Template (ADS)

Every ADS table must define:

- **Owner**
- **Description**
- **Primary Key**
- **Refresh Frequency**
- **Quality Rules**
- **Business Rules**
- **Statistic Rules**

---

**These standards are mandatory for all OGDIL contributions.**