"""第三批：CDC-08 对照后“正文 ◎、名录 U／P”者，改用替代官方页复核；含对前批之改判。

    py reports/2026-10-04/cross_document_consistency/adjudicate_batch03.py
输出 tables/u_review_batch03_adjudication.csv（与前批同格式，另加 supersedes 栏）。
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = HERE / "tables/u_review_batch03_checks.csv"
OUT = HERE / "tables/u_review_batch03_adjudication.csv"
R3 = HERE.parents[0] / "tables/01_services/strategy_services_registry_20261004_r3.csv"

OVERRIDES = {
    "E0091": ("V", "Michael Reich 官网（polimap.com 跳转至此）载“A new web-based version of PolicyMaker 5 is available”；"
                   "改判第一批之 P——当时只检得 2.0／2.2，判断过于保守（SC-01）", ""),
    "E0120": ("V", "官网自述为预测市场；美国监管路径仍只有媒体口径，未读 CFTC 一手文件", ""),
    "E0250": ("V", "内置浏览器读得 Harvard Dataverse 之 ICEWS 数据集页；页载维护方为 Leidos 等（transitioned from Lockheed Martin）", ""),
    "E0193": ("V", "同日首轮脚本请求读得标题“Google DeepMind”；补入 Polis 后重跑时该站返回空页（线上页面不稳定），"
                   "经内置浏览器复读确认。教训：核验快照不宜整批重抓，只宜增补", ""),
    "E0079": ("V", "Computational Democracy Project 官网与 pol.is 均可读；改判原表 P", ""),
    "E0124": ("P", "只到官方登录页，页显 S&P Capital IQ Pro 产品名；定位说明未能读取", ""),
    "E0121": ("P", "kalshi.com 出 Vercel 安全检查页，未绕过；维持第一批 P", ""),
    "E0268": ("U", "mca.gov.in 对脚本拒绝访问，前批 data.gov.in 亦连接失败；未绕过", ""),
}


def main():
    with R3.open(encoding="utf-8-sig") as f:
        r3 = {r["id"]: r for r in csv.DictReader(f)}
    with CHECKS.open(encoding="utf-8-sig") as f:
        checks = list(csv.DictReader(f))
    rows = []
    for c in checks:
        rid = c["registry_id"]
        if rid in OVERRIDES:
            status, note, alt = OVERRIDES[rid]
            basis = "MANUAL_REVIEW"
        elif c["verdict"] == "V_CONFIRMED":
            status, alt, basis = "V", "", "AUTOMATED"
            note = f"替代官方页内见“{c['terms_found']}”；标题：{c['title'][:60]}"
        else:
            raise SystemExit(f"{rid} 无裁定：{c['verdict']}")
        prior = r3[rid]
        rows.append(dict(registry_id=rid, registry_name=prior["name"], prior_status=prior["status"],
                         final_status=status, basis=basis, evidence_url=alt or c["final_url"] or c["url"],
                         cited_url=c["url"], cited_url_http=c["http_status"], note=note,
                         checked_at=c["checked_at"], supersedes=prior["review_batch"]))
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), Counter((r["prior_status"], r["final_status"]) for r in rows))


if __name__ == "__main__":
    main()
