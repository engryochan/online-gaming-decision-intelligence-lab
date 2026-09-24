# 元数据治理

本目录用于管理在线游戏决策智能实验室（OGDIL）的元数据治理体系。总纲请见
[METADATA_GOVERNANCE_FRAMEWORK.md](METADATA_GOVERNANCE_FRAMEWORK.md)。

## 目录下的文档

| 文档 | 内容 |
|------|------|
| [METADATA_GOVERNANCE_FRAMEWORK.md](METADATA_GOVERNANCE_FRAMEWORK.md) | 治理体系总纲：范围、角色、体系地图、成熟度路线 |
| [DATA_CLASSIFICATION_STANDARD.md](DATA_CLASSIFICATION_STANDARD.md) | 数据分类标准（L0～L3），决定数据可公开的范围 |
| [DATA_LINEAGE_STANDARD.md](DATA_LINEAGE_STANDARD.md) | 数据血缘记录范围与粒度 |
| [DATA_QUALITY_STANDARD.md](DATA_QUALITY_STANDARD.md) | 数据质量六大维度与分层要求 |
| [METADATA_CHANGE_POLICY.md](METADATA_CHANGE_POLICY.md) | 元数据变更的审批、通知与回滚流程 |

另见 `docs/03_Data_Dictionary/` 下的 ODS 数据字典治理规范与 Schema 版本管理规范——
两者是 ODS 层专属规范，与本目录的通用治理规范互为补充。

## 权威数据源

- `docs/03_Data_Dictionary/01_ODS_TABLE_LIST.csv`
- `docs/03_Data_Dictionary/02_ODS_FULL_DATA_DICTIONARY.csv`

## 治理原则

所有自动生成的元数据资产应尽可能来源于权威数据字典。
