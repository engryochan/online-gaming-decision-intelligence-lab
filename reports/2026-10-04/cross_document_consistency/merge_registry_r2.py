"""把第一批（u_review_batch01）与 CDC-05（v_candidate_adjudication）合并为现行名录 r2。

    py reports/2026-10-04/cross_document_consistency/merge_registry_r2.py

原 strategy_services_registry.csv 是 DGEF fabric.py 之已签发输入（build_report 之 catalogue 指纹），
覆盖它会触发“Input baseline changed: explicit migration required”。故原表不动，另出 r2：
列与原表相同，末尾追加 review_batch、reviewed_at；并写逐行变更日志。
"""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = ROOT / "reports/2026-10-04/tables/01_services/strategy_services_registry.csv"
# 版本 → 所含批次；每版一经在文档登记哈希即不再覆盖，新批次另出新版。
RELEASES = {
    "r2": ("tables/v_candidate_adjudication.csv",),
    "r3": ("tables/v_candidate_adjudication.csv", "tables/u_review_batch02_adjudication.csv"),
    "r4": ("tables/v_candidate_adjudication.csv", "tables/u_review_batch02_adjudication.csv",
           "tables/u_review_batch03_adjudication.csv"),
    "r5": ("tables/v_candidate_adjudication.csv", "tables/u_review_batch02_adjudication.csv",
           "tables/u_review_batch03_adjudication.csv", "tables/u_review_batch04_adjudication.csv"),
    "r6": ("tables/v_candidate_adjudication.csv", "tables/u_review_batch02_adjudication.csv",
           "tables/u_review_batch03_adjudication.csv", "tables/u_review_batch04_adjudication.csv",
           "tables/u_review_batch05_adjudication.csv", "tables/u_review_batch06_adjudication.csv"),
}
BATCH_NAME = {"tables/v_candidate_adjudication.csv": "CDC-05",
              "tables/u_review_batch02_adjudication.csv": "u_review_batch02",
              "tables/u_review_batch03_adjudication.csv": "u_review_batch03",
              "tables/u_review_batch04_adjudication.csv": "u_review_batch04",
              "tables/u_review_batch05_adjudication.csv": "u_review_batch05",
              "tables/u_review_batch06_adjudication.csv": "u_review_batch06"}
RELEASE = sys.argv[1] if len(sys.argv) > 1 else "r2"
R2 = ROOT / f"reports/2026-10-04/tables/01_services/strategy_services_registry_20261004_{RELEASE}.csv"
LOG = HERE / f"tables/registry_{RELEASE}_changes.csv"
RECEIPT = HERE / f"registry_{RELEASE}_receipt.json"
BUILD = ROOT / "DGEF/artifacts/build_report.json"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    with p.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main():
    base_sha = sha(BASE)
    dgef_sha = json.loads(BUILD.read_text(encoding="utf-8"))["input_sha256"]["catalogue"]
    assert base_sha == dgef_sha, "原名录已非 DGEF 签发版本，停止合并"

    rows = load(BASE)
    by_id = {r["id"]: r for r in rows}
    updates = {}
    for r in load(HERE / "tables/u_review_batch01.csv"):
        updates[r["id"]] = dict(status=r["proposed_status"], url=r["primary_url"],
                                scope=f"{r['finding']}；限定：{r['limits']}", batch="u_review_batch01",
                                at=r["checked_on"])
    for path in RELEASES[RELEASE]:
        batch = BATCH_NAME[path]
        for r in load(HERE / path):
            rid = r["registry_id"]
            # 不变量：本批所记之 prior_status 须等于此刻该行之真实状态（原表或前批结果）。
            current = updates[rid]["status"] if rid in updates else by_id[rid]["status"]
            assert r["prior_status"] == current, f"{rid} prior_status {r['prior_status']} ≠ 当前 {current}"
            # 后批改判前批：只许带 supersedes 栏之批次，且所改判者须与前批记录一致。
            if rid in updates:
                assert r.get("supersedes") == updates[rid]["batch"], f"{rid} 多批重复而未声明改判"
                batch_label = f"{batch}（改判 {updates[rid]['batch']}）"
            else:
                batch_label = batch
            updates[rid] = dict(status=r["final_status"], url=r["evidence_url"],
                                scope=r["note"], batch=batch_label, at=r["checked_at"][:10])

    log = []
    for rid, u in updates.items():
        old = by_id[rid]
        new = dict(old)
        new["status"] = u["status"]
        if u["status"] in ("V", "P") and u["url"]:
            new["verification_url"] = u["url"]
        new["verified_scope"] = u["scope"]
        by_id[rid] = new
        log.append(dict(id=rid, name=old["name"], old_status=old["status"], new_status=u["status"],
                        old_verification_url=old["verification_url"], new_verification_url=new["verification_url"],
                        review_batch=u["batch"], reviewed_at=u["at"]))

    fields = list(rows[0].keys()) + ["review_batch", "reviewed_at"]
    out = []
    for r in rows:
        merged = dict(by_id[r["id"]])
        u = updates.get(r["id"])
        merged["review_batch"] = u["batch"] if u else ""
        merged["reviewed_at"] = u["at"] if u else ""
        out.append(merged)
    with R2.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    with LOG.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(log[0]))
        w.writeheader()
        w.writerows(log)

    # 不变量：行数、ID 顺序、未触及行之原列逐字相同。
    assert [r["id"] for r in out] == [r["id"] for r in rows]
    for a, b in zip(rows, out):
        if a["id"] not in updates:
            assert all(a[k] == b[k] for k in a), a["id"]
    assert sha(BASE) == base_sha, "原名录在合并中被改动"

    before, after = Counter(r["status"] for r in rows), Counter(r["status"] for r in out)
    receipt = dict(base=BASE.relative_to(ROOT).as_posix(), base_sha256=base_sha, base_is_dgef_input=True,
                   r2=R2.relative_to(ROOT).as_posix(), r2_sha256=sha(R2), changed_rows=len(log),
                   status_before=dict(before), status_after=dict(after),
                   by_batch=dict(Counter(x["review_batch"] for x in log)),
                   rule="原表不改；r2 为现行名录；DGEF 若改用 r2 须走显式迁移")
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
