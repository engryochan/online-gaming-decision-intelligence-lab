# 禮逆襲作業系統全域選型：Kubuntu、NixOS、RedHawk、RHEL與星盾／Palantir 查證

研究截至：**2026-10-11**。本研究以公開一手資訊為界；無法獲取機密衛星系統映像或 Palantir 全部私有節點之版本。所有未證實主張均保留 UNKNOWN。

## 一、可查證結論

1. **若目標是完整 KDE Plasma 桌面，Kubuntu 比 Ubuntu GNOME 裝完整 KDE 更自然。**截至當日應選 Kubuntu **26.04.1 LTS**（Plasma 6.6；26.10 仍是 Beta、正式版預計 10 月 15 日）。Kubuntu 社群提供維護至 **2029 年 4 月**。
2. **WSL2 不是可代替 Windows 登入管理器的完整 Linux 主機系統**；Kubuntu 即使作為 WSL 發行版亦無法直接替換 Windows 鎖定或登入畫面。要完整 SDDM 與 Plasma 可使用虛擬機（驗證）、獨立實體 Linux 或有備份條件的雙系統。
3. **NixOS 26.05**（2026-05-30）支援宣告式設定、系統配置世代與回退，安全更新至 2026-12-31；不是五年 LTS。Ubuntu/Kubuntu 上安裝 Nix 套件管理器，可先獲得環境一致性，不必立即替換作業系統。
4. **RedHawk Linux** 是 Concurrent Real-Time 的專業即時 Linux 產品，不是 RHEL 本身。9.6 Gold 支援 RHEL/Rocky/Oracle 9.6、Ubuntu 24.04；已公布 **9.6.2**（2026-06-22），9.2 系列則 **9.2.12**（2026-09-23）。不可僅按發布日期把 9.2.12 稱為比 9.6.2「版本更高」。
5. **RHEL** 截至 2026-10-11 的公開 GA 次版本包括 **10.2** 與 **9.8**（兩者皆於 2026-05-19 發布）；企業訂閱／合規支援是優勢，若需確定性低延遲可另評估 RHEL for Real Time，不能以普通 RHEL 等同硬即時。
6. **SpaceX Starshield** 的官方職缺確認維護 **Linux、Buildroot、U-Boot** 等開源組件之公司內部分支，但沒有說明全部衛星、載荷、地面站採 Ubuntu、Kubuntu、RHEL、RedHawk、NixOS 或確切版號。**Buildroot 是建構嵌入式 Linux 的工具，不是證明採用 Ubuntu 的證據；U-Boot 是引導載入器而非 Linux 發行版。**
7. **Palantir Rubix** 官方明言使用開源或商業現成 Linux 與 Kubernetes 發行版的安全加固組合，**不是自製 Linux 發行版**。Foundry **資料連接代理**建議 RHEL 8+／Ubuntu 22.04+ 或同級，但不能據此確定 Rubix／Gotham／Foundry／AIP 所有節點之版號。

## 二、四系統決策矩陣

| 分布／產品 | 當前已核實版本（截至10月11日） | KDE完整登入桌面 | 技術強項 | 成本與風險 | 適合本研究的角色 |
|---|---|---|---|---|---|
| Kubuntu | **26.04.1 LTS，Plasma 6.6** | **原生預設** Plasma／SDDM | GUI、圖形、GIS、開發者工具、Ubuntu 生態 | 無 OS 授權費；桌面社群支援至 2029-04；不保證 WSL 取代 Windows 登入 | **桌面首選** |
| NixOS | **26.05** | 可經 `services.displayManager.sddm.enable` 等宣告式設定啟用 | 配置即程式、版本鎖定、世代回滾、批量重建 | 無 OS 授權費；學習門檻／部分驅動整合成本較高，半年更新 | **測試與可重現部署** |
| RedHawk Linux | **9.6.2；另一支線9.2.12** | 依底層發行版與廠商支援配置；非 KDE 優先產品 | 即時排程、確定性延遲、專用硬體／測試 | 商務支援與相容性需詢價；WSL2 下無法據此取得實體硬即時保證 | **後期專用實驗室** |
| RHEL | **10.2／9.8** | RHEL 10 官方主推 GNOME | 長期企業支援、SELinux、治理／合規、Podman | 可能需訂閱；個人與開發方案依授權規則；KDE 非官方桌面首選 | **企業伺服器／客戶驗證** |

## 三、針對本項目的選型與分階段路線

**階段 A：Windows 11 + 現有 WSL2，不動磁碟。** 使用 `wsl --status`、`wsl --list --verbose`、`wsl --list --online` 先做唯讀檢查；沿用現有 Ubuntu Python/R、DuckDB、地理視覺化；在 Windows 瀏覽器上展示 MapLibre/Cesium；不在 WSL 內啟動 SDDM 作 Windows 登入管理器。

**階段 B：在 VM 中試驗 Kubuntu 26.04.1 LTS。** 檢查 Plasma／Wayland、SDDM 背景、登入前影像、KDE 地圖應用、Quarto/R/Python、GPU 及網路相容性；虛擬機內測試成功後再評估裸機或獨立硬碟。避免在未備份且仍依賴 Windows 工作之裝置上強制重分割磁碟。

**階段 C：可重現環境與企業伺服器。** 先在 Kubuntu／WSL2 建立 Nix flake、容器與版本鎖定；需要多伺服器可重現基線時試 NixOS；有大企業訂單或相應合規義務時考慮 RHEL；只在有實測 p99 延遲及實體 I/O 時限指標要求時詢價 RedHawk／RHEL for Real Time。

**核心紅隊警告：**RedHawk 9.6 雖列有 Ubuntu **24.04** 支援，但不能自行推斷它在 **Kubuntu 26.04** 或 WSL2 可得到相同廠商支援或確定性延遲。

## 四、軍工軟體版本證據表

| 主張 | 判定 | 一手證據限制 |
|---|---|---|
| 星盾工程團隊維護 Linux／Buildroot／U-Boot 內部分支 | CONFIRMED | 職缺公開要求；不代表所有設備之同款 Linux |
| 星盾使用 Ubuntu 24.04／RHEL 9.6／RedHawk 9.6／Kubuntu／NixOS 其中一款 | **UNKNOWN** | 無第一手官方完整映像／公開 SBOM／型號版本對照 |
| Palantir Rubix 在 Linux＋Kubernetes 基礎上運作 | CONFIRMED | 官方自述，不是特定發行版名冊 |
| Rubix 是 Palantir 專有 Linux 發行版 | **CONTRADICTED** | 官網明確否定 |
| Palantir Foundry Agent 推薦 RHEL 8+／Ubuntu 22.04+ | CONFIRMED | 僅限資料連接代理，不可泛化至 Gotham、AIP 全部節點 |
| Rubix 支持公有雲與自有機房 | CONFIRMED | 表示可部署於 AWS/Azure/GCP/VMWare/Oracle/裸機，不表示所有客戶均如此 |

## 五、工程驗收及反證條件

1. **登入驗收**：Kubuntu 實機開機至 SDDM、顯示授權來源地球背景、登入 Plasma Wayland，且本地使用者權限與遠端存取配置最小化。WSL2 此項標示不適用，不得「測試失敗」誤判為 Kubuntu 不支援。
2. **開發驗收**：Python/R/Quarto/GeoPandas/GDAL/Cesium/MapLibre 在相同樣本和相同軟件版本下，確定性輸出及效能記錄。
3. **穩定驗收**：依實際業務測 p50/p95/p99 延遲、CPU/記憶體峰值、圖形幀率、崩潰恢復、升級及回滾，保存機器配置與測試時間。
4. **保安驗收**：最小權限、磁碟加密、系統更新、來源清單、離線備份、密鑰管理、審計日誌和授權。
5. **企業廠商驗收**：只有出現 Starshield／Palantir 官方具名 OS 發行版與版號（或可信同等直接證據）才由 UNKNOWN 升為 CONFIRMED。
6. **安全邊界**：沒有連接 Superset、StarRocks、DolphinScheduler、任何博彩網站或公司機密原始數據；使用公開文件進行桌面／伺服器選型。

## 六、一手參考連結

- [Kubuntu 26.04 LTS 發行公告](https://kubuntu.org/news/kubuntu-26-04-release-notes/)
- [Kubuntu 26.04.1 與支援期](https://kubuntu.org/news/kubuntu-26-04-1-bullet-proof-kde/)
- [Kubuntu 26.10 Beta 尚未正式發布](https://www.kubuntu.org/news/kubuntu-26-10-beta/)
- [NixOS 26.05 正式公告](https://nixos.org/blog/announcements/2026/nixos-2605/)
- [NixOS 官方手冊](https://nixos.org/manual/nixos/stable/)
- [RedHawk 官方軟件入口／版本公告](https://redhawk.concurrent-rt.com/)
- [RedHawk 9.6 發行說明](https://redhawk.concurrent-rt.com/docs/root/1Linux/1RedHawk/9.6/RedHawk-Release-Notes-0898003-9.6a.pdf)
- [RHEL 正式發布紀錄](https://access.redhat.com/articles/red-hat-enterprise-linux-release-dates)
- [RHEL for Real Time](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_for_real_time/10/html/installing_rhel_for_real_time/installing-rhel-for-real-time)
- [SpaceX Starshield 嵌入式平台官方職缺](https://job-boards.greenhouse.io/spacex/jobs/8880385002)
- [Palantir Rubix 官方架構](https://www.palantir.com/rubix)
- [Palantir Rubix 技術要求](https://www.palantir.com/rubix-specs)
- [Palantir Foundry Agent 官方支援 OS](https://www.palantir.com/docs/foundry/data-connection/set-up-agent)
- [Microsoft WSLg 不提供完整 Linux 桌面](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)
- [Nix 套件管理器可在其他 Linux 執行](https://wiki.nixos.org/wiki/Nix_%28package_manager%29/en)

## 七、全部提示標籤可追蹤性（不把標籤當內建指令）

原輸入標籤共 **88 次**，去重後 **85 種**。以下逐一登記適用及執行狀態；尤其不宣稱完成無資料支援的統計檢驗或軟件測試。

| 序 | 使用者指定標籤 | 實施狀態 | 具體內容／限制 |
|---:|---|---|---|
| 1 | `literature_review/` | 已用於本輪定性核查 | 官方手冊、發布公告、職缺與規格資料的敘述性文獻審查 |
| 2 | `systematic_review/` | 限官方證據的定向檢索；未達正式系統回顧 | 限於針對性官方來源檢索，未完成 PRISMA 式系統綜述 |
| 3 | `meta_analysis/` | 未執行（無可合併的效應量） | 未形成可合併的同質量化研究；不宣稱完成 |
| 4 | `source_check/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 5 | `cross_validation/` | 提出可執行驗證規格；尚未實測 | 無 OS 性能樣本或時間序列，僅定義日後多環境重複驗證 |
| 6 | `evidence_grade/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 7 | `provenance/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 8 | `uncertainty/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 9 | `first_principles/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 10 | `socratic/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 11 | `steelman/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 12 | `falsification/` | 已用於本輪定性核查 | 若找到星盾官方系統映像或 SBOM，再更新現有未知裁定 |
| 13 | `sensitivity/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 14 | `eda/` | 本題無相應資料／程式／實驗，未執行 | 未提供系統測量原始資料 |
| 15 | `data_quality/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 16 | `feature_engineering/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 17 | `anomaly_detection/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 18 | `hypothesis_test/` | 提出可執行驗證規格；尚未實測 | 預先定義「星盾採用某發行版」須第一手明確型號版本證明 |
| 19 | `bootstrap/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 20 | `bayesian/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 21 | `survival/` | 本題無相應資料／程式／實驗，未執行 | 不是故障時間或人員存活資料任務 |
| 22 | `forecast/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 23 | `ml/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 24 | `deep_learning/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 25 | `transformer/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 26 | `reinforcement_learning/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 27 | `multi_agent/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 28 | `model_card/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 29 | `ablation/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 30 | `calibration/` | 提出可執行驗證規格；尚未實測 | 沒有概率預測輸出，僅制定校準條件 |
| 31 | `portfolio/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 32 | `risk_management/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 33 | `walk_forward/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 34 | `stress_test/` | 提出可執行驗證規格；尚未實測 | 未獲實機，不可宣稱壓力測試 |
| 35 | `architecture_review/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 36 | `code_review/` | 本題無相應資料／程式／實驗，未執行 | 未取得星盾或 Palantir 專有原始碼 |
| 37 | `unit_test/` | 本題無相應資料／程式／實驗，未執行 | 未寫新軟件，不可虛稱測試通過 |
| 38 | `integration_test/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 39 | `profiling/` | 本題無相應資料／程式／實驗，未執行 | 無實機性能資料 |
| 40 | `zero_trust/` | 已用於本輪定性核查 | 最小權限、安全更新、離線機房限制的架構審視 |
| 41 | `privacy/` | 已用於本輪定性核查 | 只用公開官方資料，未連接內部或受限伺服器 |
| 42 | `access_control/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 43 | `incident_response/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 44 | `due_diligence/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 45 | `cost_benefit/` | 已用於本輪定性核查 | 成本屬定性判斷，RedHawk／RHEL商務報價需廠商確認 |
| 46 | `gap_analysis/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 47 | `decision_matrix/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 48 | `acceptance_test/` | 提出可執行驗證規格；尚未實測 | 定義版本、安裝、登入、圖形、回滾及負載驗收 |
| 49 | `executive_summary/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 50 | `technical_spec/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 51 | `reproducibility/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 52 | `changelog/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 53 | `research/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 54 | `verify/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 55 | `factcheck/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 56 | `analyze/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 57 | `deepdive/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 58 | `compare/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 59 | `redteam/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 60 | `critic/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 61 | `killcritic/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 62 | `blindspot/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 63 | `assumptions/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 64 | `model/` | 提出可執行驗證規格；尚未實測 | 比較及層級架構模型；非已訓練模型 |
| 65 | `simulate/` | 提出可執行驗證規格；尚未實測 | 未啟動 VM 或硬體模擬 |
| 66 | `backtest/` | 提出可執行驗證規格；尚未實測 | 已制定後續需要的資料、場景或接受門檻 |
| 67 | `causal/` | 提出可執行驗證規格；尚未實測 | 沒有因果識別設計或實驗干預 |
| 68 | `counterfactual/` | 提出可執行驗證規格；尚未實測 | 僅規劃 WSL2／原生／VM 選型假設 |
| 69 | `architect/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 70 | `code/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 71 | `debug/` | 本題無相應資料／程式／實驗，未執行 | 沒有可供負責任實測的輸入及環境 |
| 72 | `optimize/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 73 | `benchmark/` | 提出可執行驗證規格；尚未實測 | 需相同硬體負載比較 p50/p95/p99 延遲、吞吐與記憶體 |
| 74 | `security/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 75 | `threatmodel/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 76 | `blueprint/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 77 | `cheatsheet/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 78 | `strategy/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 79 | `scenario/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 80 | `actionplan/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 81 | `roadmap/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 82 | `checklist/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 83 | `audit/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 84 | `report/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |
| 85 | `summary/` | 已用於本輪定性核查 | 用於 Linux 發行版與星盾／Palantir 技術版本之方法選型 |

**本研究為公開技術文件查證與工程選型，不是以實機跑出來的跨發行版基準測試，亦未取得國防專用內部系統影像。**
