"""复核 CDC-04 之 REVIEW_FOR_V 候选：逐一请求来源网址，记录状态、跳转、标题与主体名是否在页内。

    py reports/2026-10-04/cross_document_consistency/verify_v_candidates.py
只发 GET 请求读取公开页面；不登录、不绕过访问控制；结果写 tables/v_candidate_checks.csv。
"""
import csv
import hashlib
import html
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CROSSWALK = HERE / "tables/mark_crosswalk.csv"
OUT = HERE / "tables/v_candidate_checks.csv"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DGEF-public-research/1.0"


def fetch(url):
    """curl.exe 走系统证书库；--fail 不用，以便记录 4xx/5xx。"""
    cmd = ["curl.exe", "-sS", "-L", "--max-time", "40", "--max-filesize", "8000000", "-A", UA,
           "-o", "-", "-w", "\n@@META@@%{http_code} %{url_effective}", url]
    try:
        run = subprocess.run(cmd, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        return 0, url, b"", "timeout"
    body, _, meta = run.stdout.rpartition(b"\n@@META@@")
    parts = meta.decode("utf-8", "replace").split(" ", 1)
    code = int(parts[0]) if parts[0].isdigit() else 0
    return code, parts[1] if len(parts) > 1 else url, body, run.stderr.decode("utf-8", "replace")[:200]


def name_terms(name, basis):
    terms = {basis}
    terms.update(p.strip() for p in re.split(r"[/／|、]", re.sub(r"（[^）]*）|\([^)]*\)", " ", name)))
    return [t for t in terms if len(t) >= 3]


def check(row):
    code, final, body, err = fetch(row["doc_source_url"])
    text = body.decode("utf-8", "replace")
    title = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    title = html.unescape(re.sub(r"\s+", " ", title.group(1))).strip()[:120] if title else ""
    plain = html.unescape(re.sub(r"<[^>]+>", " ", text))
    found = [t for t in name_terms(row["registry_name"], row["doc_source_basis"])
             if re.search(re.escape(t), plain, re.I)]
    is_pdf = body[:5] == b"%PDF-"
    if code == 200 and (found or is_pdf):
        verdict = "V_CONFIRMED" if found else "V_PDF_NAME_UNCHECKED"
    elif code == 200:
        verdict = "REACHABLE_NAME_NOT_FOUND"
    elif code in (401, 403, 429, 202):
        verdict = "BLOCKED_MANUAL_REVIEW"
    else:
        verdict = "FAILED"
    return dict(
        registry_id=row["registry_id"], registry_name=row["registry_name"], url=row["doc_source_url"],
        http_status=code, final_url=final, title=title, bytes=len(body),
        sha256=hashlib.sha256(body).hexdigest() if body else "", name_terms_found="+".join(found),
        verdict=verdict, error=err.strip(), checked_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )


def main():
    with CROSSWALK.open(encoding="utf-8-sig") as f:
        seen, todo = set(), []
        for r in csv.DictReader(f):
            if r["proposal"] == "REVIEW_FOR_V" and r["registry_id"] not in seen:
                seen.add(r["registry_id"])
                todo.append(r)
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(check, todo))
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    from collections import Counter
    print(len(results), Counter(r["verdict"] for r in results))
    for r in results:
        if r["verdict"] != "V_CONFIRMED":
            print(r["verdict"], r["registry_id"], r["registry_name"][:24], r["http_status"], r["url"][:70], r["error"][:60])


if __name__ == "__main__":
    main()
