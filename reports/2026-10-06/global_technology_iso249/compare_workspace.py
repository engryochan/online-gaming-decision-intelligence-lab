from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
AUDIT=ROOT/"reports/2026-10-06/workspace_change_audit"
def load(name):
    with (AUDIT/name).open(encoding="utf-8-sig",newline="") as f:return {r["path"]:r for r in csv.DictReader(f)}
before=load("global_start_files.csv");after=load("global_finish_files.csv")
added=sorted(after.keys()-before.keys());removed=sorted(before.keys()-after.keys())
changed=sorted(p for p in before.keys()&after.keys() if before[p]["sha256"]!=after[p]["sha256"])
expected={"AGENTS.md","Reference/Geostrategy_Defense_Industry_Aerospace_and_Artificial_Interlligence_Ecosystem_Report.qmd","Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd"}
unexpected=sorted(set(changed)-expected)
result={"baseline":"global_start_files.csv","final":"global_finish_files.csv","hashes_compared":len(before),"added":added,"removed":removed,"content_changed":changed,"unexpected_content_changes":unexpected,"state":"PASS" if not removed and not unexpected else "REVIEW_REQUIRED","note":"The pre-existing user edit to the active report HTML is unchanged from this turn's baseline. Git still shows it as modified against HEAD. Hash scan excludes its own changing receipts and Git internals."}
(HERE/"workspace_delta.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
assert result["state"]=="PASS",result
print(json.dumps({"state":result["state"],"baseline_files":len(before),"final_files":len(after),"added":len(added),"removed":removed,"content_changed":changed},ensure_ascii=False))

