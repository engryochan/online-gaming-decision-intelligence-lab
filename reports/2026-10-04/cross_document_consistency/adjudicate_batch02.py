"""第二批：官网自述核验之最终裁定（自动结果 + 2026-10-04 人工／浏览器复核）。

    py reports/2026-10-04/cross_document_consistency/adjudicate_batch02.py
输出 tables/u_review_batch02_adjudication.csv。V 之范围：官网可达，主体名或其产品见于官网自述；
不证效果、价格、授权、牌照或名录所列每一分项。
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = HERE / "tables/u_review_batch02_checks.csv"
OUT = HERE / "tables/u_review_batch02_adjudication.csv"
REGISTRY = HERE.parents[0] / "tables/01_services/strategy_services_registry.csv"

BROWSER = "内置浏览器读得官方页"
OVERRIDES = {
    # 浏览器或官网内页人工确认
    "E0007": ("V", BROWSER + "，标题“国务院发展研究中心”", ""),
    "E0019": ("V", BROWSER + "，SAP HCM 页载 SuccessFactors", ""),
    "E0020": ("V", "官网“About SAS”页", "https://www.sas.com/en_us/company-information.html"),
    "E0105": ("V", BROWSER + "，标题“National Defense University”", ""),
    "E0191": ("V", BROWSER + "，标题“OpenAI | 研究与部署”", ""),
    "E0196": ("V", "官网标题“Alibaba Cloud: AI and Cloud Computing Services”；通义分项未逐一核", ""),
    "E0217": ("V", BROWSER + "，Simulink 产品页", ""),
    "E0225": ("V", BROWSER + "，Tableau 官网", ""),
    "E0232": ("V", BROWSER + "，CBDB 项目官网", ""),
    "E0235": ("V", BROWSER + "，标题“漢籍全文資料庫”", "https://hanchi.ihp.sinica.edu.tw/ihp/hanji.htm"),
    "E0254": ("V", BROWSER + "，标题“Geopolitical Risk (GPR) Index”", ""),
    "E0255": ("V", BROWSER + "，标题“Economic Policy Uncertainty Index”", ""),
    "E0257": ("V", BROWSER + "（JS 自动跳转后），标题“Open Data Watch”", ""),
    "E0267": ("V", BROWSER + "，标题“EDGAR Full Text Search”；脚本请求曾触发 SEC 频率限制", ""),
    "E0285": ("V", BROWSER + "，“Refugee Data Finder”", ""),
    "E0286": ("V", BROWSER + "，“Displacement Tracking Matrix”", ""),
    "E0323": ("V", "官网标题为 iFLYTEK 英文定位，页内多见“讯飞”", ""),
    "E0326": ("V", BROWSER + "，Thales 集团官网", "https://www.thalesgroup.com/en"),
    "E0327": ("V", BROWSER + "，BAE Systems“Who we are”页", "https://www.baesystems.com/en/our-company"),
    "E0334": ("V", "官网内页“航天服务业_中国航天科技集团有限公司”", "https://www.spacechina.com/n25/n146/n234/n252/index.html"),
    "E0345": ("V", BROWSER + "，Applied Materials 官网（欧洲区）", ""),
    # 部分可证
    "E0059": ("P", "返回非标准状态码 419，但页标题为“天眼查-商业查询平台”；内容未能完整读取", ""),
    "E0361": ("P", "官网返回“当前地区暂不支持访问”，只证域名与品牌，不证功能", ""),
    # 受阻或失败：不绕过，保持 U
    "E0008": ("U", "官网连接失败（脚本与浏览器）", ""),
    "E0058": ("U", "官网连接失败", ""),
    "E0127": ("U", "Bloomberg 人机验证（Are you a robot?），未绕过", ""),
    "E0171": ("U", "官网连接超时", ""),
    "E0173": ("U", "官网对脚本与浏览器均返回 403", ""),
    "E0182": ("U", "官网连接失败（脚本与浏览器）", ""),
    "E0203": ("U", "Cloudflare 人机验证，未绕过", ""),
    "E0214": ("U", "Cloudflare 人机验证，未绕过", ""),
    "E0222": ("U", "官网连接失败", ""),
    "E0275": ("U", "IMF 对脚本与浏览器均拒绝访问", ""),
    "E0298": ("U", "Cloudflare 人机验证，未绕过", ""),
    "E0306": ("U", "官网对脚本与浏览器均返回 403", ""),
    "E0318": ("U", "Tesla 对脚本与浏览器均拒绝访问", ""),
    "E0330": ("U", "官网 502（主机连接超时）", ""),
    "E0348": ("U", "官网返回 412", ""),
    "E0349": ("U", "官网连接被重置", ""),
    "E0350": ("U", "官网返回 412", ""),
    "E0352": ("U", "官网对脚本 403，浏览器渲染为空", ""),
    "E0383": ("U", "Vercel 安全检查页，未绕过", ""),
    "E0386": ("U", "Cloudflare 人机验证，未绕过", ""),
}
# 官网自述之现实变化（V 照常，另入注记）
NOTES = {
    "E0017": "官网 AI 页未见 Einstein，现以 Agentforce 为名；名录旧称待更正",
    "E0174": "官网现自称“电科金仓”，名录旧称“人大金仓”待更正",
    "E0357": "nist.gov/caisi 现跳转至 nist.gov/caissi，页称 Center for Advancing Innovation and Standards for Super Intelligence (CAISSI)；同页 2026 年新闻仍用 CAISI",
    "E0312": "跳转至 spaceweather.gov",
}


def main():
    with REGISTRY.open(encoding="utf-8-sig") as f:
        names = {r["id"]: r["name"] for r in csv.DictReader(f)}
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
            note = f"官网页内见“{c['terms_found']}”；标题：{c['title'][:60]}"
        else:
            raise SystemExit(f"{rid} 无裁定：{c['verdict']}")
        if rid in NOTES:
            note += "；" + NOTES[rid]
        rows.append(dict(registry_id=rid, registry_name=names[rid], prior_status="U", final_status=status,
                         basis=basis, evidence_url=alt or c["final_url"] or c["url"], cited_url=c["url"],
                         cited_url_http=c["http_status"], note=note, checked_at=c["checked_at"]))
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), Counter(r["final_status"] for r in rows), Counter(r["basis"] for r in rows))


if __name__ == "__main__":
    main()
