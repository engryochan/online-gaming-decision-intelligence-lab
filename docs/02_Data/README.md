# OGDIL Data Foundation

本目录负责 OGDIL 的数据架构、ODS 治理、数据字典、数据血缘与 Data Contract。

## Core Documents

- `ODS_Data_Foundation.md` — ODS Truth Layer 治理规范
- `ODS_to_ADS_Architecture.md` — ODS → DWD → DWS → ADS 架构
- `ODS_Subject_Domain_Map.md` — ODS 主题域第一版映射
- `ADS_Data_Contract_Template.md` — ADS 数据契约模板

## Data Dictionary Assets

计划纳入：

- `../../data_dictionary/01_ODS_TABLE_LIST.csv`
- `../../data_dictionary/02_ODS_FULL_DATA_DICTIONARY.csv`

## Engineering Principle

```text
Source
  ↓
ODS Truth Layer
  ↓
DWD Atomic Detail
  ↓
DWS Subject Layer
  ↓
Feature Store / ADS
  ↓
Statistics · AI · Quant · BI · Decision Intelligence
```

所有分析数据产品必须保留完整的数据血缘与可审计性。
