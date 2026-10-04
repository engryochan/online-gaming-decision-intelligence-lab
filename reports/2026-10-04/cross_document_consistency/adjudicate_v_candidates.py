"""CDC-05：把 verify_v_candidates.py 之自动结果与人工复核合成最终裁定。

    py reports/2026-10-04/cross_document_consistency/adjudicate_v_candidates.py
输出 tables/v_candidate_adjudication.csv；名录 CSV 不改，待重建时合并。
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = HERE / "tables/v_candidate_checks.csv"
OUT = HERE / "tables/v_candidate_adjudication.csv"

# 人工复核（2026-10-04）：自动名称匹配过严、页面受拒或出处已失效者。
OVERRIDES = {
    "E0241": ("V", "页面标题“Worldwide Governance Indicators”，世界银行官方域名", ""),
    "E0264": ("V", "GLEIF 官方检索站 search.gleif.org，标题“LEI Search”；页面为 JS 渲染", ""),
    "E0265": ("V", "欧委会公司法页载“BRIS is operational since 8 June 2017”", ""),
    "E0269": ("V", "ACRA 官方页标题“Bizfile”", ""),
    "E0270": ("V", "日本国税厅法人番号公表站官方页标题", ""),
    "E0271": ("V", "ASIC 官方“Search ASIC registers”页", ""),
    "E0277": ("V", "WHO 官方“Global Health Observatory”页", ""),
    "E0284": ("V", "UN 人口司“World Population Prospects”页", ""),
    "E0305": ("V", "国家航天局官网可达，标题“国家航天局”；只证 CNSA，ILRS 分项未核", ""),
    "E0161": ("V", "内置浏览器读得 CoStar Group 官方品牌页：商业地产信息平台", ""),
    "E0289": ("V", "正文所引 ECMWF 页现须登录（出处失效）；改据哥白尼 CDS 公开页，载 ERA5 及早期版 ERA5T",
              "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels"),
    "E0272": ("V", "ilostat.ilo.org 出 Cloudflare 人机验证，未绕过；改据 ILO 官方数据页，载 ILOSTAT 并链至 ilostat.ilo.org",
              "https://www.ilo.org/data-and-statistics"),
    "E0301": ("V", "正文为此条配到 Earthdata 网址，与 Horizons 不符；改据 DGEF/inbox 中 JPL Horizons API 原始响应（本仓已存证）；SPICE 分项未核",
              "DGEF/inbox/horizons_399_e57f5f64ddb4.json"),
    "E0287": ("P", "gis.earthdata.nasa.gov 为 JS 门户，未渲染出正文；只证域名属 NASA", ""),
    "E0355": ("P", "只得 forbes.com 首页，未见 Global 2000 榜单页", ""),
    "E0124": ("U", "spglobal.com 对脚本与浏览器均拒绝访问（Akamai）；未绕过", ""),
    "E0268": ("U", "data.gov.in 连接被拒，mca.gov.in 返回 Access Denied；未绕过", ""),
}


def main():
    with CHECKS.open(encoding="utf-8-sig") as f:
        checks = list(csv.DictReader(f))
    rows = []
    for c in checks:
        if c["registry_id"] in OVERRIDES:
            status, note, alt = OVERRIDES[c["registry_id"]]
            basis = "MANUAL_REVIEW"
        elif c["verdict"] == "V_CONFIRMED":
            status, note, alt, basis = "V", f"页内见“{c['name_terms_found']}”；标题：{c['title'][:60]}", "", "AUTOMATED"
        else:
            raise SystemExit(f"{c['registry_id']} 无裁定：{c['verdict']}")
        rows.append(dict(registry_id=c["registry_id"], registry_name=c["registry_name"], prior_status="U",
                         final_status=status, basis=basis, evidence_url=alt or c["url"],
                         cited_url=c["url"], cited_url_http=c["http_status"], note=note,
                         checked_at=c["checked_at"]))
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), Counter(r["final_status"] for r in rows), Counter(r["basis"] for r in rows))


if __name__ == "__main__":
    main()
