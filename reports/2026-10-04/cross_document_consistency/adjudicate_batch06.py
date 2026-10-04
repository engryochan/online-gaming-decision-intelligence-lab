"""第六批（终批）：运营方、历史案例、同名待消歧与无主体者，逐条定案。

    py reports/2026-10-04/cross_document_consistency/adjudicate_batch06.py
本批无自动请求表；每条证据均经人工（检索、浏览器或脚本下载）读取，出处与限定写入 note。
运营方只读官网公示或监管名册，不注册、不登录、不提交表单；内置浏览器对博彩域名之安全限制一律遵守。
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "tables/u_review_batch06_adjudication.csv"
CURRENT = HERE.parents[0] / "tables/01_services/strategy_services_registry_20261004_r5.csv"
DAY = "2026-10-04"
RULE = "依名录原注：牌照主体、公司登记号、官方域名三者未闭环者不升格；同名站、代理站与镜像站之宣称不作事实"

DECISIONS = [
    # 历史与监管一手
    ("E0189", "V", "https://ico.org.uk/media2/migrated/2259371/investigation-into-data-analytics-for-political-purposes-update.pdf",
     "英国 ICO 调查报告原件（PDF，2,163,050 字节，SHA256 3ee5e6b4…）载 Cambridge Analytica；登记为历史案例，不列现售"),
    ("E0398", "V", "https://www.gamblingcommission.gov.uk/public-register/business/detail/domain-names/55149",
     "英国博彩委员会公开名册：持牌主体 Hillside (UK Gaming) ENC，账号 55149，域名 bet365.com 状态 Active；只证该法域牌照"),
    ("E0400", "V", "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=CZR&type=10-K",
     "SEC EDGAR：Caesars Entertainment, Inc.，CIK 0001590895（SIC 7011）；只证发行人登记，各州牌照另核"),
    ("E0399", "V", "https://www.evokeplc.com/",
     "evoke plc 官网投资者栏目列“Historical 888”：888 品牌归 evoke 集团；各法域牌照另核"),
    ("E0397", "V", "https://www.dafabet.com/",
     "官网自述由 Osmila N.V. 运营，2007-06-28 于库拉索注册；只证运营方自述，牌照有效性未经监管名册复核"),
    # 部分可证
    ("E0098", "P", "https://developer.aliyun.com/article/1655357",
     "阿里云开发者社区文章“阿里云城市数据大脑赋能杭州智能交通管理”；官方社区文章，非产品页"),
    ("E0187", "P", "https://www.cac.gov.cn/2015-05/21/c_1115354879.htm",
     "网信办 2015 年转载：腾讯征信列入个人征信准备机构；后未获独立牌照、参股百行征信之说只见媒体，未读人民银行一手公示"),
    ("E0395", "P", "https://bc.game/",
     "品牌官网可读，页内只称“our gaming license”，未披露持牌主体与牌照号。" + RULE),
    ("E0396", "P", "https://1xbet.com/",
     "脚本只取得地区化登录页，未见持牌主体；内置浏览器以安全规则禁止打开，未绕过。" + RULE),
    ("E0401", "P", "https://www.rivalry.com/",
     "官网为纯脚本渲染，未读得正文；只得第三方市场资料（Rivalry Corp，TSXV：RVLY，2026 年债务重组）"),
    ("E0234", "P", "https://www.news.cn/20260807/88295ec0ad4e4ecaa3b50ba8cb2df352/c.html",
     "新华社 2026-08-07 报道：《儒藏》“精华编”数字平台上线，北京大学出版社与北大《儒藏》编纂与研究中心共建，"
     "收 510 种、近 2 亿字；平台网址本轮未读。此条前五批漏核，由竣工检查发现补入"),
    # 保持 U
    ("E0394", "U", "https://stake.com/", "官网 Cloudflare 人机验证，未绕过。" + RULE),
    ("E0362", "U", "https://fund.joinquant.com/", "页面为纯脚本渲染，未读得正文；与 JoinQuant 研究平台（E0361，P）分开"),
    ("E0026", "U", "", "三轮检索未得主体或官网；检索未得不等于停业"),
    ("E0078", "U", "", "三轮检索未得主体；检索结果之“新通联”为包装企业，不得混认"),
    ("E0115", "U", "https://www.ithome.com/0/906/456.htm", "只见“墨子·未来指挥官”之公开报道；与“华戍防务”之主体关系无证据，不据名称并列推定"),
    ("E0366", "U", "", "同名待消歧：原文语境不足以锁定主体，不择一而认"),
    ("E0373", "U", "", "同名待消歧：检索所得为 Flutter 旗下 Sky Betting & Gaming，与原文“内容／直播生态”是否同一未证"),
    ("E0402", "U", "", "同名待消歧，依名录原注保持 UNKNOWN。" + RULE),
    ("E0403", "U", "", "同名待消歧，依名录原注保持 UNKNOWN。" + RULE),
    ("E0404", "U", "", "同名待消歧，依名录原注保持 UNKNOWN；不与同名奢侈品集团合并。" + RULE),
]


def main():
    with CURRENT.open(encoding="utf-8-sig") as f:
        cur = {r["id"]: r for r in csv.DictReader(f)}
    rows = []
    for rid, status, url, note in DECISIONS:
        rows.append(dict(registry_id=rid, registry_name=cur[rid]["name"], prior_status=cur[rid]["status"],
                         final_status=status, basis="MANUAL_REVIEW", evidence_url=url, cited_url=url,
                         cited_url_http="", note=note, checked_at=DAY, supersedes=cur[rid]["review_batch"]))
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), Counter((r["prior_status"], r["final_status"]) for r in rows))


if __name__ == "__main__":
    main()
