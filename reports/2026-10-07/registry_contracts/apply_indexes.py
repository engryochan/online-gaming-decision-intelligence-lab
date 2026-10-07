"""Append navigational summaries only, guarded by this turn's immutable baseline."""
from pathlib import Path
import csv,json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
base={r['path']:r for r in csv.DictReader((ROOT/'reports/2026-10-06/workspace_change_audit/registry_contracts_20261007_start_files.csv').open(encoding='utf-8-sig'))}
targets=['Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd','Reference/Global_Technology_ISO249_Registry.qmd','Reference/Project_Information_Integration_20261007.qmd']
def sha(b):return hashlib.sha256(b).hexdigest()
suffix='''
<!-- REGISTRY_CONTRACTS_20261007_BEGIN -->
## 2026-10-07 資料契約與分範圍查詢增補

[本輪資料契約報告](Global_Registry_Data_Contracts_20261007.qmd)為 B04 九表、135 個欄位提供粒度與業務用途，交付保留原值的可查詢 SQLite。344 筆未決欄位獲上下文定義，未決尚有424筆；定義仍待負責人簽核，未新增全球已核機構或能力。

機構候選國別列表拆成341條橋接關係，原字串與候選狀態保留。全球主張中219條為公開描述核實，2條為研究隸屬核實，分別統計；7筆機構及對應主張仍缺來源ID。國家能力與N0～N7仍為UNKNOWN。欄位、關係與數字能查詢不代表全球查全或性能已獨立重現。

新視圖保留249母表條目，區分任意範圍／僅公開描述／已核國別關係；未將跨國候選歸屬當作法人住所。原CSV、歷史批次、DGEF與使用者HTML均不覆寫。歸檔及更名的現行路徑見本輪報告與對照表，舊驗收只適用原雜湊版本。
<!-- REGISTRY_CONTRACTS_20261007_END -->
'''
updates={};manifest=[];copies=OUT/'originals';copies.mkdir(exist_ok=True)
for path in targets:
    original=(ROOT/path).read_bytes();assert sha(original)==base[path]['sha256'],'User changed '+path
    assert b'REGISTRY_CONTRACTS_20261007_BEGIN' not in original,'Already appended'
    archive=copies/(sha(original)+'.qmd');archive.write_bytes(original);candidate=original+suffix.encode()
    assert candidate[:len(original)]==original
    preview=OUT/'preview'/path;preview.parent.mkdir(parents=True,exist_ok=True);preview.write_bytes(candidate)
    updates[path]=candidate;manifest.append(dict(path=path,before_sha256=sha(original),before_bytes=len(original),after_sha256=sha(candidate),snapshot=archive.relative_to(ROOT).as_posix()))
for path in targets:assert sha((ROOT/path).read_bytes())==base[path]['sha256'],'Concurrent target edit'
for path,data in updates.items():(ROOT/path).write_bytes(data)
(OUT/'append_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print('APPEND_PASS 3')
