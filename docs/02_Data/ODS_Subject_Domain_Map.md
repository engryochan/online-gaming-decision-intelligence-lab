# OGDIL ODS Subject Domain Map

本文件是 ODS 表主题域的第一版人工治理映射。它不替代完整数据字典；最终映射应由 `01_ODS_TABLE_LIST.csv` 与 `02_ODS_FULL_DATA_DICTIONARY.csv` 自动生成并经过人工审核。

| Domain | Representative ODS Tables | Primary Analytical Purpose |
|---|---|---|
| Identity & Access | `ods_a168_permissionsgroup`, `ods_a168_roles`, `ods_a168_subagent_permissionrole` | 权限、角色、组织关系 |
| Game & Table Operations | `ods_a168_play_set`, `ods_a168_shuffle_gid`, `ods_a168_shuffle_info`, `ods_a168_tablelimit`, `ods_a168_tablelimit_third` | 游戏、桌台、洗牌、限额与第三方桌台 |
| Real-time Activity | `ods_a168_realtimebet`, `ods_a168_realtimelobby`, `ods_a168_realtimelog` | 实时行为、在线状态与运行监控 |
| Risk & Governance | `ods_a168_risklist`, `ods_a168_white_list` | 风险与白名单治理 |
| Wallet & Financial Operations | `ods_a168_wallet_dtl`, `ods_a168_wallet_feedbackerr`, `ods_a168_wallet_reporter`, `ods_a168_wallet_reporter_copy` | 钱包交易、反馈、失败与处理状态 |
| Platform Configuration | `ods_a168_site`, `ods_a168_sms_setting`, `ods_a168_stream`, `ods_a168_symbol`, `ods_a168_urllist`, `ods_a168_wechat_url` | 平台配置与基础设施 |
| Temporary / Auxiliary | `ods_a168_temp_id_list` | 临时或辅助性数据 |
| Sync Governance | `sync_checkpoint` | 增量同步断点与任务治理 |

## Important Semantic Notes

### `ods_a168_wallet_dtl`

字段语义显示其承担钱包请求、响应、金额、当前余额、处理状态与反馈状态等信息。建议作为 Wallet Intelligence 的核心 ODS 来源之一，但不得直接把 `status` 或 `feedback_status` 当作业务成功率指标，必须先定义统计窗口与去重规则。

### `ods_a168_wallet_feedbackerr`

包含交易流水、金额、类型、重试次数、错误码、错误信息及成功标识。适合建立钱包异常与稳定性数据产品。`errorMessage` 等文本字段进入模型前应进行脱敏与规范化。

### `ods_a168_realtimebet`

包含场次、子场次、桌号、IP、登录时间、下注金额、下注内容、当前额度、User-Agent 等字段。该表具有较高实时风控与行为建模价值；IP、User-Agent 与下注内容需按敏感数据策略处理。

### `ods_a168_shuffle_info`

包含洗牌状态、游戏、桌台、频率以及多阶段人员签到/签退时间。适合建立桌台运营效率与流程时长分析，但需先定义各状态的业务状态机。

### `ods_a168_tablelimit` / `ods_a168_tablelimit_third`

适合构建桌台配置、下注限额、第三方桌台状态与供应商运营分析。建议后续建立统一的 table / game / vendor 维度模型。

### `sync_checkpoint`

这是数据工程治理表，而非业务事实表。建议进入数据平台监控域，用于增量同步断点、任务恢复、延迟监控与数据新鲜度指标。

## Mapping Confidence

- `High`：表名与字段语义能够直接支持主题域判断。
- `Medium`：需要结合完整数据字典或源系统业务规则确认。
- `Low`：仅凭表名无法可靠判断，必须补充业务定义。

当前第一版主要采用 High / Medium 判断。正式生产建模前，应对 Medium 项进行业务确认。
