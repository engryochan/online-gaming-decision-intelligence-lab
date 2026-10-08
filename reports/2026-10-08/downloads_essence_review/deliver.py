from pathlib import Path
import json,csv,hashlib,subprocess
O=Path(__file__).resolve().parent;R=O.parents[2];a=json.loads((O/'audit.json').read_text(encoding='utf-8'));assert len(a['files'])==15 and not any('error'in r for r in a['files'])
files={r['name']:r for r in a['files']};table=[]
for r in a['files']:
    status='FORMAT_AND_SCOPE_REVIEWED_SEMANTIC_CLAIMS_PENDING'
    if r.get('members') and r['name'].endswith('.csv.zip'):status='FULL_CSV_STREAM_CRC_AND_SHAPE_CHECKED_NOT_IMPORTED'
    if r['name'].endswith('.iso'):status='HASH_AND_VOLUME_METADATA_ONLY_AUTHENTICITY_UNKNOWN_NO_PROJECT_USE'
    if r['name']=='desktop.ini':status='SHELL_LOCALIZATION_ONLY_NO_RESEARCH_USE'
    table.append(dict(file=r['name'],bytes=r['bytes'],sha256=r['sha256'],review_method=r.get('kind'),status=status,original_imported=False))
with (O/'file_review_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)
rar=next(r for r in a['files'] if r['name'].endswith('.rar'));workbooks=sum(bool(m.get('sheets')) for m in rar['members']);sheets=sum(len(m.get('sheets',[])) for m in rar['members'])
lei=[r for r in a['files'] if r['name'].endswith('.csv.zip')]
lei_table='\n'.join('| '+r['name']+' | '+str(r['members'][0]['data_rows'])+' | '+str(r['members'][0]['columns'])+' | 0 |' for r in lei)
review_table='\n'.join('| '+r['file']+' | '+r['status']+' |' for r in table)
db=files['official_public_data_value_audit_20261008.sqlite'];dbrows=', '.join(t['table']+': '+str(t['rows']) for t in db['tables'])
report=f'''---
title: "下載資料只讀核查與精華採用：2026-10-08"
date: 2026-10-08
lang: zh-TW
format:
  html:
    toc: true
    embed-resources: true
---

## 採用範圍與已完成核查

Windows 下載資料夾本輪共 15 個文件，全部計算 SHA256 並按格式檢查；來源檔未修改、原始文件與業務明細匯入數為零。项目僅採用方法、用途、模型合同及有一手證據的更正。雜湊及格式驗收不能證明官方下載身份、每個法人真實性、全部敘述正確或軟體映像可信。

三份 GLEIF ZIP 全部讀至結尾，檢查解壓 CRC、內部內容雜湊並全量解析 CSV 欄位數；不存在欄位數不一致的行。以下是來源資料行數，不是去重或核實後的全球公司總數，未驗證每筆 LEI 校驗碼、關係正確性或更新狀態。

| 本地文件 | 全檔資料行（不含表頭） | 欄位數 | 本輪入庫明細 |
|---|---:|---:|---:|
{lei_table}

ISIC CSV 實測 830 個不同分類代碼，22 個一位節點、87 個二位節點、258 個三位節點及 463 個四位節點。原檔不是有效 UTF8，採 CP1252 解碼後核對结构；官方編碼宣告尚未獨立核定。解釋工作簿讀取 ISIC5 表 831 行、Notes 表 59 行，可讀行與公式文字均檢查；未轉存原始說明正文或改寫工作簿。ISIC 是經濟活動分類，分類數不能當作法人數。[UN 官方分類入口](https://unstats.un.org/unsd/classifications/Econ/isic)。

SDG RAR 可由本機 tar 逐成員讀取，確認 {len(rar['members'])} 個成員、{workbooks} 個可讀工作簿、{sheets} 個工作表；另外兩個成員是本地審計 Markdown 與 SQLite 的相同雜湊副本，沿用已核對結果，不算額外獨立來源。保留成員雜湊與形狀統計，未收錄联系人資料。讀取器提示部分資料驗證擴充與列印區域不支援，原始檔未寫回。這些是指標採集及來源治理材料，不能當作全球統計觀測全量或企業資料。[UN SDG 採集資訊](https://unstats.un.org/sdgs/dataContacts/)。

SQLite 以唯讀、immutable 模式檢查，integrity_check 為 ok；逐表記錄數：`{dbrows}`。其中 GLEIF 檔首樣本仍是有序樣本，不具全球代表性。本地 SDG 比較 CSV 有 5 行、可讀樣例 CSV 有 90 行；它們引用的五個大型封存 ZIP 並未出現在本輪資料夾，不能依第三方審計文字或 CRC／大小宣稱全內容相同，也不能重現其全量或樣本缺失率。

## 文本主張校對與採用結果

兩份宇航／策略文本已全文解碼審閱，下載 Markdown 與項目現行宇航 QMD 不是同一份內容，未覆蓋任何舊版本。採用分層架構與證據方法；不把模型回答當官方來源，也不把未核定的產品、性能、採用、軍工配置及營收主張移入正式登記。

| 主張 | 本輪校對結果 | 採用方式 |
|---|---|---|
| Athea 是 Helsing／Saab 合資 | 與 2021-05-27 官方成立公告不符，成立方為 Atos／Thales | 在現行生態報告追加有日期的更正；不據此推斷今日所有權 |
| cFS 是作業系統 | NASA 將其列為飛行軟體框架，OSAL 隔離底層作業系統 | 分开 framework／OS／BSP 層，不評為較高級作業系統 |
| 中國來源開源組件因 ITAR／EAR／CMMC 一律不能用於美歐國防 | 一般性國別白名單結論缺少具體項目、條款與範圍；不能由此推出 | 降為未核定的逐案合規主張，分離工程能力與法規判斷 |
| 多個模型重複敘述即可提升證據等級 | 不成立；須追溯獨立的一手來源 | 模型文本為待證主張，不自動 VERIFIED |
| 免費下載等於任何用途均已獲授權 | 不成立 | 資料授權、再發布、訓練及本輪操作授权分職 |
| 官方分類或 LEI 已涵蓋世界所有公司 | 不成立 | 地方工商、上市工具、券商牌照及歷史實體分源登記，未知分母保持 NULL |

Athea 成立方見 [Atos 官方公告](https://atos.net/en/2021/press-release_2021_05_27/thales-and-atos-create-european-champion)；框架角色見 [NASA cFS](https://github.com/nasa/cFS)。出口管制需核定管轄與交易範圍，見 [BIS EAR 734](https://www.bis.gov/regulations/ear/734)；CMMC 關注合同資訊保護，見 [DoD 官方問答](https://dodcio.defense.gov/Portals/0/Documents/CMMC/CMMC-FAQsv5.pdf)。本輪不作任何具體出口或採購的法律許可判定。

GLEIF 身份、RR 關係與 REPEX 例外應分表；會計合併父關係不能自動當作股權、實益所有權或全部控制鏈。[GLEIF 官方字典](https://www.gleif.org/en/lei-data/access-and-use-lei-data/gleif-data-dictionary)。資料使用條款見 [GLEIF CC0 條款](https://www.gleif.org/en/meta/lei-data-terms-of-use)，其可用性不改變使用者本輪「不收錄原始文件」的限制。

## 已落實的項目強化

採用規則已整合至[外部資料精華採用合同](../V2.0.1/governance/source_review_contract.md)、DGEF 架構說明、治理入口、現行前沿生態報告及下載故障審計增補。业务粒度以 source／release／identifier／typed_relationship／classification_assignment／observation／coverage 分職；處理以串流、版本去重、批次對賬及未知分母治理為原則。這是已寫入的合同與研究改進，未冒稱資料庫遷移、分散式湖倉、全量資料匯入或性能基準已實作。

Windows ISO 僅計算完整檔案雜湊及讀取卷描述符，未掛載、執行或驗證映像內每個程式與官方簽章；desktop.ini 僅屬本機顯示配置。两者不提供可採用研究內容，未納入產品或技術能力登記。其餘未逐項外部佐證的文本主張維持 UNKNOWN；不可將「15 檔已格式核查」改稱「15 檔所有信息已證實」。

## 逐檔範圍

| 文件 | 本輪核查及限制 |
|---|---|
{review_table}

逐檔雜湊及覆核元資料見[清單](../reports/2026-10-08/downloads_essence_review/file_review_inventory.csv)。本輪未複製下載資料夾的任何原始檔，未建立法人或统计觀測來源副本，沒有改動任何正式資料庫。
'''
(R/'Reference/Downloads_Essence_Review_20261008.qmd').write_text(report,encoding='utf-8')
def append(name,marker,body):
    p=R/name;old=p.read_bytes()
    if marker.encode() not in old:p.write_bytes(old+('\n\n'+marker+'\n'+body+'\n').encode('utf-8'))
append('Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','<!-- DOWNLOADS_ESSENCE_REVIEW_20261008 -->','''## 2026-10-08 下載文本校對及資料方法增補

本增補用於更正同項歷史主張，保留原文供追溯；不以外部 Markdown 覆寫本報告。下載文件與業務明細本輪均未收錄。完整方法及逐檔限制見 [審閱報告](Downloads_Essence_Review_20261008.qmd)。

Athea 的 2021-05-27 成立公告列 Atos／Thales，原附件「Helsing／Saab 合資」不採用；歷史成立方與目前股權需分開核查。[官方公告](https://atos.net/en/2021/press-release_2021_05_27/thales-and-atos-create-european-champion)。NASA cFS 歸為飛行軟體框架，OSAL 與實際底層作業系統分層，不能以框架名稱推斷任務 OS。[NASA cFS](https://github.com/nasa/cFS)。

「中國來源組件因 ITAR／EAR／CMMC 一律排除於美歐國防」的概括不能採為已核實結論；須按產品、管轄、使用者、用途、目的地與合同保護要求核定。[BIS](https://www.bis.gov/regulations/ear/734)、[DoD CMMC](https://dodcio.defense.gov/Portals/0/Documents/CMMC/CMMC-FAQsv5.pdf)。工程適配另按時延、確定性、吞吐、失效處理、硬體資源、介面、實測方法與證據日期比較，不以國別或宣傳詞判高低。

採用分層架構：公開來源與傳感資料、地理空間、資料工程／時序儲存、身份與本體、模型推論、模擬、可審核決策及部署治理；每一層有独立證據。讀寫或雙向神經介面能力仍須人體試驗、模態、帶寬、距離、寫入方式及監管證據；遠端通信不等於無設備心靈相通，文藝比喻不升級 N0～N7 等級。

法人身份、會計合併關係、例外、產業活動及宏觀觀測分職；分類與來源目錄不得冒充全國企業全集。詳見 [精華採用合同](../V2.0.1/governance/source_review_contract.md)。''')
append('Reference/global_dns_download_audit_v2_2_0.md','<!-- LOCAL_DOWNLOAD_REVIEW_20261008 -->','''## 本機已有下載文件的後續核查

原 DNS／網頁工具觀測是當時環境證據，保留原文。2026-10-08 在 Windows Downloads 發現並核查本地 GLEIF、ISIC 與 SDG 文件；本地存在不證明前次容器 DNS 已恢復，也不能由檔名或雜湊獨立驗證官方下載鏈。RAR 可由本機 tar 逐成員讀取，先前文本「沒有 RAR 工具」不適用於本次 Windows 環境。ISIC CSV 不能預設 UTF8；編碼、文件格式、HTTP 及 DNS 狀態應分別記錄。本輪僅採用精華，未匯入來源文件。詳見 [核查報告](Downloads_Essence_Review_20261008.qmd)。''')
append('README.md','<!-- DOWNLOADS_ESSENCE_REVIEW_20261008 -->','''## 外部下載資料的核查與精華採用

[15 檔只讀審閱與採用結果](Reference/Downloads_Essence_Review_20261008.qmd)；[來源治理合同](V2.0.1/governance/source_review_contract.md)。只整合经覆核的研究方法與更正，不複製原始下載檔或匯入業務明細。''')
print(json.dumps({'files_reviewed':15,'gleif_rows_read':sum(r['members'][0]['data_rows'] for r in lei),'rar_workbooks':workbooks,'rar_sheets':sheets,'source_records_imported':0}))
