# ADS Data Contract Template

> 所有生产级 ADS 数据产品必须在发布前完成此模板。

## 1. Dataset Identity

- Dataset Name:
- Version:
- Owner:
- Domain:
- Status:

## 2. Business Definition

- Description:
- Business Purpose:
- Intended Users:
- Refresh Frequency:
- SLA / Freshness:

## 3. Grain

- One row represents:
- Primary Key:
- Deduplication Rule:

## 4. Source Lineage

| ADS Field | DWS Field | DWD Field | ODS Table | ODS Column | Source DB |
|---|---|---|---|---|---|
| | | | | | |

## 5. Data Types

| Field | Type | Nullable | Description |
|---|---|---|---|
| | | | |

## 6. Quality Rules

- Primary key uniqueness:
- Null-rate threshold:
- Freshness threshold:
- Valid-value rules:
- Range rules:
- Referential integrity:
- Source-to-target reconciliation:

## 7. Business Rules

- Rule 1:
- Rule 2:

## 8. Statistical Rules

- Observation window:
- Inclusion criteria:
- Exclusion criteria:
- Population definition:
- Aggregation method:
- Time zone:

## 9. Privacy & Security

- Sensitive fields:
- Masking / hashing:
- Access level:
- Retention:

## 10. Model Usage

- Features derived from this dataset:
- Label definitions:
- Point-in-time correctness:
- Training / inference usage:

## 11. Change Management

- Breaking change policy:
- Backward compatibility:
- Deprecation policy:
- Changelog:

## 12. Validation

- [ ] Data quality checks passed
- [ ] Lineage verified
- [ ] Privacy review completed
- [ ] Statistical definition reviewed
- [ ] Owner approved
- [ ] Code review completed
