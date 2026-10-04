# 第七次复核：跨件对账回执（2026-10-04）

范围：重读全仓后，对两份总纲做非退化增补，并新增可复跑的跨件对账脚本。原文未删一字。

## 实物

- `check_cross_doc.py`：只读检查两份总纲与 DGEF README 中的表数、视图数、实体根号、名录行数、获准训练行是否与 `DGEF/artifacts/build_report.json` 相符；核验账 UNKNOWN 而正文 PASS／◎ 者；本地断链；库行数与完整性。退出码 0 为无未裁定项。
- `before_documents.zip`：修订前两份文件原字节。

## SHA256

| 文件 | 修订前 | 修订后 |
|---|---|---|
| 名录 v2.4 | 50d0415ed7375c6ae111e91d040673da6d9d971312daf398a9a1c01cdd20a35f | 3b57a85e1552abe1130c62bba289fcbb5e46ab6a7e01c50ad019f8e1e33dec58 |
| _大秦赋算筹_v1_3_9.qmd | d1e0d29026976a3e5a7e3c2561308ddffe093a15326e194da65a2720f7e9753e | bbb4ccc539c581a7c70f1631d7c10771f43d47cf5224a3bf2364a08388cbc1aa |

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
