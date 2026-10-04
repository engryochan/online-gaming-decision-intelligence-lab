"""第四批：官网受阻者改走替代官方渠道（文档站、GitHub 官方组织、监管登记、监管名单、SEC 原件）。

    py reports/2026-10-04/cross_document_consistency/adjudicate_batch04.py
输出 tables/u_review_batch04_adjudication.csv。另含两条无自动请求、只经浏览器读监管原件之记录（EXTRA）。
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = HERE / "tables/u_review_batch04_checks.csv"
OUT = HERE / "tables/u_review_batch04_adjudication.csv"
CURRENT = HERE.parents[0] / "tables/01_services/strategy_services_registry_20261004_r4.csv"
CFTC = "https://www.cftc.gov/IndustryOversight/IndustryFilings/TradingOrganizations"
B = "内置浏览器读得"

OVERRIDES = {
    "E0058": ("V", B + "官网，标题“企查查 - 查企业_查老板_查风险_企业信息查询系统”；脚本请求连接失败", "https://www.qcc.com/"),
    "E0182": ("V", "官网与文档站本轮不可达；改据 Clarifai 之 GitHub 官方组织页", "https://github.com/Clarifai"),
    "E0275": ("V", "imf.org 对脚本与浏览器均拒绝；改据 IMF eLibrary 官方站", "https://www.elibrary.imf.org/"),
    "E0318": ("V", "tesla.com 与 ir.tesla.com 均拒绝访问；改据 SEC EDGAR 登记页（Tesla, Inc.，CIK 0001318605）。只证发行人登记，不证产品细项",
              "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=TSLA&type=10-K"),
    "E0348": ("V", B + "官网首页，标题“国家电网有限公司”；英文子页现为 404", "http://www.sgcc.com.cn/"),
    "E0349": ("V", B + "官网，标题“Where energy is opportunity | Aramco”", "https://www.aramco.com/"),
    "E0350": ("V", B + "官网，标题“中国石油天然气集团有限公司”", "https://www.cnpc.com.cn/cnpc/index.shtml"),
    "E0383": ("V", "openbet.com 出安全检查页；改据 SEC 8-K 附件 EX-99.2：2025 年 Endeavor 将 OpenBet 售予 OB Global Holdings（管理层收购，Jordan Levin 续任 CEO）",
              "https://www.sec.gov/Archives/edgar/data/1766363/000119312525060947/d897469dex992.htm"),
    "E0171": ("U", "官网连接被服务器中断（脚本与浏览器）", ""),
    "E0298": ("U", "ipcinfo.org 为 Cloudflare 人机验证，未绕过；FAO 替代页 404", ""),
    "E0306": ("U", "官网对脚本与浏览器均 403", ""),
    "E0330": ("U", "官网 502（主机连接超时），两次尝试相同", ""),
}
EXTRA = [
    ("E0121", "V", "CFTC 指定合约市场名单：Kalshi 自 2020-11-03 为 DCM；2025-01-17 获准修改指定令以允许中介化期货交易", CFTC),
    ("E0120", "V", "CFTC 指定合约市场名单：QCX LLC d/b/a Polymarket US 自 2025-07-09 为 DCM，现以 Polymarket US 之名营运；"
                   "取代前批之媒体口径。国际站与美国站法域不同", CFTC),
    ("E0380", "P", "Sportradar 官网可读；“2025-11 完成收购 IMG ARENA 及其博彩权益组合”只见业界媒体，未读 Sportradar 一手公告",
     "https://www.sportradar.com/"),
]


def main():
    with CURRENT.open(encoding="utf-8-sig") as f:
        cur = {r["id"]: r for r in csv.DictReader(f)}
    with CHECKS.open(encoding="utf-8-sig") as f:
        checks = list(csv.DictReader(f))
    rows = []

    def add(rid, status, basis, url, cited, http, note, at):
        rows.append(dict(registry_id=rid, registry_name=cur[rid]["name"], prior_status=cur[rid]["status"],
                         final_status=status, basis=basis, evidence_url=url, cited_url=cited,
                         cited_url_http=http, note=note, checked_at=at, supersedes=cur[rid]["review_batch"]))

    for c in checks:
        rid = c["registry_id"]
        if rid in OVERRIDES:
            status, note, alt = OVERRIDES[rid]
            add(rid, status, "MANUAL_REVIEW", alt or c["url"], c["url"], c["http_status"], note, c["checked_at"])
        elif c["verdict"] == "V_CONFIRMED":
            add(rid, "V", "AUTOMATED", c["final_url"], c["url"], c["http_status"],
                f"替代官方渠道页内见“{c['terms_found']}”；标题：{c['title'][:60]}", c["checked_at"])
        else:
            raise SystemExit(f"{rid} 无裁定：{c['verdict']}")
    for rid, status, note, url in EXTRA:
        add(rid, status, "MANUAL_REVIEW", url, url, "", note, "2026-10-04")
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), Counter((r["prior_status"], r["final_status"]) for r in rows))


if __name__ == "__main__":
    main()
