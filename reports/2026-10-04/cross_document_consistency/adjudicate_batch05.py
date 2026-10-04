"""第五批：长尾官网核验（含同名误认之拒收与现实变化注记）。

    py reports/2026-10-04/cross_document_consistency/adjudicate_batch05.py
输出 tables/u_review_batch05_adjudication.csv。
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = HERE / "tables/u_review_batch05_checks.csv"
OUT = HERE / "tables/u_review_batch05_adjudication.csv"
CURRENT = HERE.parents[0] / "tables/01_services/strategy_services_registry_20261004_r5.csv"
B = "内置浏览器读得"

OVERRIDES = {
    "E0104": ("V", B + "官网，标题“CNA | National Security Analysis”；语境为美国国家安全研究分析机构，非同名他者", ""),
    "E0109": ("V", B + "美国空军官方报道“USAF GE 26 showcases new AI-enabled WarMatrix wargaming capability”", ""),
    "E0147": ("V", B + "官网，标题“Citadel - Identifying the Highest and Best Uses of Capital”；子实体角色未核", ""),
    "E0186": ("V", B + "蚂蚁集团官网，页内载芝麻信用", ""),
    "E0213": ("V", B + "linode.com，标题为 Akamai 云平台；Linode 已并入 Akamai", ""),
    "E0316": ("P", "seradata.com 现跳转至 Slingshot Aerospace；Seradata 数据库现况未在页内读得", ""),
    "E0337": ("P", "官网 geosat.com.tw 本机解析失败（脚本与浏览器）；只得台北市政府投资推广页与业界名录介绍",
              "https://invest.taipei/en/geosat-aerospace-technology/"),
    "E0372": ("U", "拒收：推测之 sentientgaming.com 为游戏测试与本地化公司，非名录所指 AI 荷官主体；所指主体只见业界媒体，官网未得", ""),
    "E0178": ("U", "官网连接失败（脚本与浏览器）", ""),
    "E0315": ("U", "官网 502", ""),
    "E0335": ("U", "官网证书不受本机信任（SEC_E_UNTRUSTED_ROOT），未绕过证书校验", ""),
    "E0375": ("U", "官网证书或 SNI 校验失败（脚本与浏览器），未绕过；所见只有业界媒体", ""),
}
NOTES = {
    "E0204": "x.ai 页面标题现为“SpaceXAI”；与 SpaceX 之关系以带日期之一手公告为准，本轮未核",
    "E0215": "产品页现位于 ansys.synopsys.com：Ansys 已归 Synopsys，“当前厂商归属待核”结案",
    "E0216": "只证 Teamcenter；MindSphere 现名未核",
    "E0221": "timescale.com 现跳转至 tigerdata.com（TigerData）",
    "E0188": "IBM 官方 Watson SDK 说明载 Personality Insights 已停用（2020-12-01 公告，2021-12-01 下线）；登记为历史产品，不列现售",
    "E0190": "官网自述“Facial Personality Analytics”；依名录原注，不据脸部输出人格结论",
    "E0299": "reach-initiative.org 现跳转至 IMPACT Initiatives",
    "E0243": "INSCR 数据页载 Polity5；更新状态另核",
    "E0365": "官网产品为 ChipVue 筹码识别与分析",
}


def main():
    with CURRENT.open(encoding="utf-8-sig") as f:
        cur = {r["id"]: r for r in csv.DictReader(f)}
    with CHECKS.open(encoding="utf-8-sig") as f:
        checks = list(csv.DictReader(f))
    rows = []
    for c in checks:
        rid = c["registry_id"]
        if rid in OVERRIDES:
            status, note, alt = OVERRIDES[rid]
            basis, url = "MANUAL_REVIEW", alt or c["url"]
        elif c["verdict"] == "V_CONFIRMED":
            status, basis, url = "V", "AUTOMATED", c["final_url"]
            note = f"官网页内见“{c['terms_found']}”；标题：{c['title'][:60]}"
        else:
            raise SystemExit(f"{rid} 无裁定：{c['verdict']}")
        if rid in NOTES:
            note += "；" + NOTES[rid]
        rows.append(dict(registry_id=rid, registry_name=cur[rid]["name"], prior_status=cur[rid]["status"],
                         final_status=status, basis=basis, evidence_url=url, cited_url=c["url"],
                         cited_url_http=c["http_status"], note=note, checked_at=c["checked_at"],
                         supersedes=cur[rid]["review_batch"]))
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), Counter((r["prior_status"], r["final_status"]) for r in rows))


if __name__ == "__main__":
    main()
