"""两套核验标记对照：服务名录 V/P/U ↔ 名录 v2.4 编号条目 ◎/○/△/★。

只读两个来源，写出 tables/mark_crosswalk.csv：
    py reports/2026-10-04/cross_document_consistency/build_mark_crosswalk.py
按名称词元匹配，匹配结果附 match_basis，供人工复核；不改任何源文件。
"""
import csv
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SERVICES = ROOT / "reports/2026-10-04/tables/01_services"
# 以最新已签发之名录版本为准（r3 > r2 > 原表）。
REGISTRY = max(SERVICES.glob("strategy_services_registry_20261004_r*.csv"), default=SERVICES / "strategy_services_registry.csv",
               key=lambda p: int(p.stem.rsplit("_r", 1)[1]))
BATCH = HERE / "tables/u_review_batch01.csv"
MD = ROOT / "Reference/真实版人物分析与治国策略服务_名录与九十日行令_v2_4_全球行政通信宇航生命证据增强版_20261004.md"
OUT = HERE / "tables/mark_crosswalk.csv"

ROW = re.compile(r"^\|\s*(\d{1,3})\s*([★◎○△→\s]*)\|(.*)$")
CDC08 = re.compile(r"〔CDC-08：([^〕]*)〕")
# 过短或过泛之词元易误配，不用作匹配键。
# 已人工确认之误配：(名录 ID, 正文条目) → 理由。
EXCLUDE = {("E0196", "49"): "名录 E0196 为阿里云平台；正文 #49 所指为阿里云城市大脑（E0098），子串误配"}
STOP = {"AI", "API", "R", "IAF", "UN", "Pro", "Group", "Inc", "Lab", "Data", "Labs", "One", "SES", "PPI"}


def catalogue_rows():
    """名录 v2.4 中“| 编号 标记 | 名称 | ...”之目录行；同号多见时取首见。"""
    rows = {}
    for no, line in enumerate(MD.read_text(encoding="utf-8").splitlines(), 1):
        m = ROW.match(line)
        if not m:
            continue
        num, marks, rest = m.groups()
        name_cell = rest.split("|")[0]
        # “○→◎”：箭头后为现行标记，箭头前留作历史。
        current = marks.split("→")[-1]
        note = CDC08.search(line)
        if num not in rows:
            rows[num] = dict(num=num, marks="".join(sorted(set(current.replace(" ", "")))),
                             name_cell=name_cell.strip(), line=no,
                             partial=note.group(1) if note else "")
    return rows


def tokens(name):
    """由名录名称取匹配词元：按分隔符切分，去括号注释，保留足够独特者。"""
    name = re.sub(r"（[^）]*）|\([^)]*\)", " ", name)
    parts = re.split(r"\s*[/／|、,，]\s*|\s+—\s+", name)
    out = []
    for p in parts:
        p = p.strip(" ·")
        if len(p) >= 3 and p not in STOP:
            out.append(p)
    return out


def token_in(token, text):
    """拉丁词元须整词出现（防 Meta↔Metaculus、ITU↔Institute）；汉字词元按子串。"""
    if re.search(r"[A-Za-z]", token):
        return re.search(rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])", text, re.I) is not None
    return token in text


URL = re.compile(r"https?://[^\s)>\]|；，。、（）《》“”]+")


def source_lines():
    """名录 v2.4 中含网址之非目录行（来源各节及正文链接），供为 ◎ 条目找出处。"""
    return [(no, line) for no, line in enumerate(MD.read_text(encoding="utf-8").splitlines(), 1)
            if not ROW.match(line) and URL.search(line)]


def find_source(toks, sources):
    """取词元出现位置之后最近的网址；同一行列多家来源时不串用他家网址。"""
    for no, line in sources:
        for t in toks:
            m = (re.search(rf"(?<![A-Za-z0-9]){re.escape(t)}(?![A-Za-z0-9])", line, re.I)
                 if re.search(r"[A-Za-z]", t) else re.search(re.escape(t), line))
            if not m:
                continue
            after = [u for u in URL.finditer(line) if u.start() >= m.start()]
            nxt = re.search(r"[；;]", line[m.end():])
            limit = m.end() + nxt.start() if nxt else len(line)
            # 网址须落在本词元所属之分句内（下一个分号之前），否则视为他家来源。
            after = [u for u in after if u.start() <= limit]
            if after:
                return after[0].group(0).rstrip(".,"), no, t
    return "", "", ""


def doc_status(marks):
    if "◎" in marks:
        return "VERIFIED_THIS_ROUND"
    if "○" in marks:
        return "INHERITED_UNRECHECKED"
    if "△" in marks:
        return "UNVERIFIED"
    return "NO_MARK"


def relation(reg_status, marks):
    d = doc_status(marks)
    if d == "VERIFIED_THIS_ROUND" and reg_status == "U":
        return "DOC_AHEAD"      # 正文已核，名录未登
    if d in ("INHERITED_UNRECHECKED", "UNVERIFIED") and reg_status == "V":
        return "REGISTRY_AHEAD"  # 名录已核，正文标记陈旧
    if d == "VERIFIED_THIS_ROUND" and reg_status == "V":
        return "AGREE_VERIFIED"
    if d == "VERIFIED_THIS_ROUND" and reg_status == "P":
        return "DOC_AHEAD_PARTIAL"
    return "AGREE_OR_WEAK"


def generic_url(url, name):
    """根域网址而非该主体自家域名（如 sec.gov/ 之于 Meta）：不足以单独支撑 V。"""
    m = re.match(r"https?://(?:www\.)?([^/]+)/?$", url)
    if not m:
        return False
    host = m.group(1).lower()
    words = [w.lower() for w in re.findall(r"[A-Za-z0-9]{3,}", name)]
    return not any(w in host for w in words)


def proposal(status, marks, url, name=""):
    """仅供人工复核之建议，不自动改名录。"""
    rel = relation(status, marks)
    if rel == "DOC_AHEAD":
        if not url:
            return "KEEP_U_NO_SOURCE_URL"
        return "REVIEW_FOR_V" if not generic_url(url, name) else "KEEP_U_GENERIC_URL"
    if rel == "REGISTRY_AHEAD":
        return "UPDATE_DOC_MARK"
    return "NONE"


def main():
    cat = catalogue_rows()
    sources = source_lines()
    proposed = {}
    # 已签发版本（r2 以降）已含各批裁定；只有对原表时才叠加第一批拟定。
    if BATCH.exists() and not REGISTRY.stem.rsplit("_", 1)[-1].startswith("r"):
        with BATCH.open(encoding="utf-8-sig") as f:
            proposed = {r["id"]: r["proposed_status"] for r in csv.DictReader(f)}
    with REGISTRY.open(encoding="utf-8-sig") as f:
        registry = list(csv.DictReader(f))

    out = []
    for r in registry:
        toks = tokens(r["name"])
        hits = []
        for c in cat.values():
            matched = [t for t in toks if token_in(t, c["name_cell"])]
            if matched:
                hits.append((c, matched))
        if not hits:
            continue
        status = proposed.get(r["id"], r["status"])
        src_url, src_line, src_basis = find_source(toks, sources)
        hits = [(c, m) for c, m in hits if (r["id"], c["num"]) not in EXCLUDE]
        for c, matched in hits:
            marks = c["marks"]
            for part in c["partial"].split("；"):
                if "已 ◎" in part and any(token_in(tk, part) for tk in matched):
                    marks = "◎"
            c = dict(c, marks=marks)
            out.append(dict(
                registry_id=r["id"], registry_name=r["name"], registry_status=r["status"],
                registry_status_after_batch01=status, doc_entry=c["num"], doc_marks=c["marks"],
                doc_line=c["line"], match_basis="name_token:" + "+".join(matched),
                relation=relation(status, c["marks"]),
                doc_source_url=src_url, doc_source_line=src_line, doc_source_basis=src_basis,
                proposal=proposal(status, c["marks"], src_url, r["name"]),
            ))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    linked = {o["registry_id"] for o in out}
    print(f"名录版本 {REGISTRY.name}")
    print(f"目录行 {len(cat)}；名录 {len(registry)} 条中 {len(linked)} 条可回指；对照 {len(out)} 行")
    print(Counter(o["relation"] for o in out))
    first = {}
    for o in out:
        first.setdefault(o["registry_id"], o)
    print("按名录 ID 去重之建议：", Counter(
        max((x["proposal"] for x in out if x["registry_id"] == i),
            key=["NONE", "KEEP_U_NO_SOURCE_URL", "KEEP_U_GENERIC_URL", "UPDATE_DOC_MARK", "REVIEW_FOR_V"].index)
        for i in first))
    return out


if __name__ == "__main__":
    main()
