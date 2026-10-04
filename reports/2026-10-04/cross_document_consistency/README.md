# 第七次复核：跨件对账回执（2026-10-04）

范围：重读全仓后，对两份总纲做非退化增补，并新增可复跑的跨件对账脚本。原文未删一字。

## 实物

- `check_cross_doc.py`：只读检查两份总纲与 DGEF README 中的表数、视图数、实体根号、名录行数、获准训练行是否与 `DGEF/artifacts/build_report.json` 相符；核验账 UNKNOWN 而正文 PASS／◎ 者；本地断链；库行数与完整性。退出码 0 为无未裁定项。
- `before_documents.zip`：修订前两份文件原字节。

## SHA256

| 文件 | 修订前 | 修订后 |
|---|---|---|
| 名录 v2.4 | 50d0415ed7375c6ae111e91d040673da6d9d971312daf398a9a1c01cdd20a35f | 89a15078015504244db5568b44ae57228f8879d3e45f956927ed437e1c2f1e8b |
| _大秦赋算筹_v1_3_9.qmd | d1e0d29026976a3e5a7e3c2561308ddffe093a15326e194da65a2720f7e9753e | 4ada945439fd18460726bdda15bf774690ad6d26a23ddd31a4baf19a5c08af56 |

## 结论

- 基线运行抓出 IAF 状态冲突 3 处；官网本日复读原句可见，以 CDC-01 裁定 PASS，范围限 IAF 自述会员规模。
- DGEF 库、16 项测试、本地链接、SIPRI、UN 非自治领土与地外生命状态均与正文相符。
- DGEF `verification_sources.json` 未改动；IAF 一行待下次入库转正。
- 未复核 330 条 U 级名录。

## 同日续核

- Quarto 1.10.18 ＋ R 4.6.1 渲染 qmd 副本（暂存目录，不覆盖仓库 HTML）通过；R 块实跑。
- 发现 455 个标题双重且矛盾编号，qmd YAML 斧正 D-R1：`number-sections: false`，复渲染确认 0 处自动号。
- IAF 会员页原始响应存证于 `evidence/`（见 `evidence/manifest.json`），供下批 DGEF 入库；DGEF 本轮不改。
- PDF 渲染未做。

## U 级名录第一批

- 22 条“归属／现况／版本待核”者：13 拟 V、7 止 P、2 仍 U；见 `tables/u_review_batch01.csv`。
- 名录 `strategy_services_registry.csv` 未改；拟定状态待下次重建合并。
- CDC-03：更正 Senturion 之作者归属，并将 JRC SES 与加权博弈模型分列。
- 发现名录 V/P/U 与名录 v2.4 之 ◎/○ 两套标记未对账，列为下批工作。

## CDC-04 两套标记对照

- `build_mark_crosswalk.py` 生成 `tables/mark_crosswalk.csv`：122 个名录 ID 可回指名录 v2.4 目录行。
- 56 条正文 ◎、名录 U 且有分句内来源网址：人工复核升 V 之候选；24 条保持 U（18 无出处、6 仅他方根域）。
- 9 个正文条目（13 个名录 ID）之 ○ 已由名录 V 取代。
- 已并入 `check_cross_doc.py`；名录 CSV 仍未改。

## CDC-05 五十六条候选复核

- `verify_v_candidates.py` 逐一请求来源网址 → `tables/v_candidate_checks.csv`；`adjudicate_v_candidates.py` 合成裁定 → `tables/v_candidate_adjudication.csv`。
- 52 V（39 自动、13 人工）、2 P、2 U；被拒访问之站点均未绕过。
- 出处失效：ECMWF ERA5 页须登录，改据哥白尼 CDS；ILOSTAT 人机验证，改据 ILO 官网；Horizons 改据 DGEF 本地原始响应。
- 两批合计若采纳：名录 V60/P15/U330 → V125/P24/U256。名录 CSV 未改。

## CDC-06／07 名录合并与第二批

- 原名录（SHA256 `3716f378…`）为 DGEF `fabric.py` 已签发输入，覆盖会触发重建拒绝；故原表不动，另出版本化名录。
- r2（`d0451069…`）：第一批＋CDC-05，V125/P24/U256。
- r3（`928ab563…`，现行）：再加第二批 154 条（132 V、2 P、20 U），V257/P26/U122。
- `merge_registry_r2.py r2|r3` 可重建，r2 重跑字节不变；回执 `registry_r2_receipt.json`、`registry_r3_receipt.json`。
- 对账脚本新增：回执哈希须等于实物、已签发版本短哈希须入档、原名录须仍为 DGEF 基线。
- 官网所见变化：人大金仓→电科金仓；NIST CAISI→CAISSI 页面；Salesforce Einstein→Agentforce。

## CDC-08 目录标记写回、第三批与 r4

- 名录 v2.4 目录行就地更正：8 行 `○→◎`，6 行部分核注记，5 行注明复验受阻；旧标记保留可见。
- 第三批 15 条（替代官方页）：12 V、2 P、1 U；含对前批之改判（`supersedes` 栏）。
- r4（`30e97820…`，现行）：V269/P22/U114；r2、r3 重跑字节不变。
- 自我更正：SC-01 PolicyMaker 5 前批判 P 过保守；SC-02 核验快照不宜整批重抓；SC-03 对照脚本旧批叠加缺陷与合并不变量收紧。
- 复渲染 qmd 副本通过；DGEF 16 项测试通过。
