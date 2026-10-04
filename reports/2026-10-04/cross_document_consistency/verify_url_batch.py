"""按“名录 ID, 官网网址, 主体名词元(| 分隔)”清单逐一请求官网，判定主体是否自述于页内。

    py reports/2026-10-04/cross_document_consistency/verify_url_batch.py tables/u_review_batch02_urls.csv tables/u_review_batch02_checks.csv
沿用 verify_v_candidates.fetch：只读 GET，不登录，不绕过人机验证或访问控制。
"""
import csv
import hashlib
import html
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_v_candidates import fetch  # noqa: E402

CHALLENGE = re.compile(r"Just a moment|cf-chl|Attention Required|Access Denied|captcha", re.I)


def check(row):
    code, final, body, err = fetch(row["url"])
    text = body.decode("utf-8", "replace")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    title = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()[:120] if m else ""
    plain = html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", text, flags=re.S | re.I))
    terms = [t for t in row["terms"].split("|") if t]
    found = [t for t in terms if re.search(re.escape(t), plain + " " + title, re.I)]
    if code == 200 and CHALLENGE.search(title):
        verdict = "BLOCKED_CHALLENGE"
    elif code == 200 and found:
        verdict = "V_CONFIRMED"
    elif code == 200:
        verdict = "REACHABLE_NAME_NOT_FOUND"
    elif code in (401, 403, 429, 202):
        verdict = "BLOCKED_MANUAL_REVIEW"
    else:
        verdict = "FAILED"
    return dict(registry_id=row["id"], url=row["url"], http_status=code, final_url=final, title=title,
                bytes=len(body), sha256=hashlib.sha256(body).hexdigest() if body else "",
                terms_found="+".join(found), verdict=verdict, error=err.strip()[:160],
                checked_at=datetime.now(timezone.utc).isoformat(timespec="seconds"))


def main(src, dst):
    src, dst = HERE / src, HERE / dst
    with src.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(check, rows))
    with dst.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    print(len(results), Counter(r["verdict"] for r in results))
    for r in results:
        if r["verdict"] != "V_CONFIRMED":
            print(r["verdict"], r["registry_id"], r["http_status"], r["title"][:50], r["url"][:60], r["error"][:50])


if __name__ == "__main__":
    main(*sys.argv[1:3])
