"""跨件对账：两份总纲与 DGEF 实物之数字、状态与链接是否一致。

只读运行，不改任何文件：
    py reports/2026-10-04/cross_document_consistency/check_cross_doc.py
退出码 0 表示无矛盾；1 表示发现须人工裁定之处（不自动改文）。
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = {
    "qmd": ROOT / "_大秦赋算筹_v1_3_9.qmd",
    "md": ROOT / "Reference/真实版人物分析与治国策略服务_名录与九十日行令_v2_4_全球行政通信宇航生命证据增强版_20261004.md",
    "dgef_readme": ROOT / "DGEF/README.md",
}
REPORT = json.loads((ROOT / "DGEF/artifacts/build_report.json").read_text(encoding="utf-8"))
SOURCES = json.loads((ROOT / "DGEF/verification_sources.json").read_text(encoding="utf-8"))

# 主张 → 应出现的规范值；文中凡提及而数值不同者记为漂移。
NUMERIC_CLAIMS = [
    ("DGEF 实体表数", r"(\d+)\s*(?:张\s*)?(?:SQLite STRICT 表|实体表)", str(REPORT["table_count"])),
    ("DGEF 视图数", r"(\d+)\s*(?:个)?视图", str(REPORT["view_count"])),
    ("DGEF 实体根号", r"([\d,]+)\s*(?:个\s*)?(?:UUIDv7 )?实体根号", f'{REPORT["row_counts"]["registry_entity"]:,}'),
    ("服务候选名录", r"(\d+)\s*(?:行|条)(?:候选资料|服务候选)", str(REPORT["row_counts"]["staging_service_catalogue"])),
    ("获准训练行", r"(\d+)\s*条获准训练", str(REPORT["training_approved_rows"])),
]
# 已知因施工阶段不同而合法并存的历史数值（只在注明的历史段落出现）。
HISTORICAL_OK = {"DGEF 实体表数": {"43"}, "DGEF 实体根号": {"5,295", "5295"}}


def lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def check_numeric():
    issues = []
    for name, pattern, expected in NUMERIC_CLAIMS:
        for key, path in DOCS.items():
            for no, line in enumerate(lines(path), 1):
                for m in re.finditer(pattern, line):
                    got = m.group(1)
                    norm = lambda s: s.replace(",", "")
                    if norm(got) != norm(expected) and got not in HISTORICAL_OK.get(name, set()):
                        issues.append(f"[数值漂移] {name}: {key}:{no} 写 {got}，实物 {expected}")
    return issues


def check_status_conflicts():
    """同一来源在核验账为 UNKNOWN，而正文称 PASS／◎ 者，须显式裁定。"""
    issues = []
    for src in SOURCES if isinstance(SOURCES, list) else SOURCES.get("sources", []):
        if src.get("status") != "UNKNOWN":
            continue
        sid = src["id"]
        for key in ("qmd", "md"):
            for no, line in enumerate(lines(DOCS[key]), 1):
                if re.search(rf"\b{re.escape(sid)}\b", line) and re.search(r"PASS|◎", line):
                    resolved = any("CDC-01" in l for l in lines(DOCS[key]))
                    tag = "已裁定(CDC-01)" if resolved else "未裁定"
                    issues.append(f"[状态冲突·{tag}] {sid}: 核验账 UNKNOWN，{key}:{no} 标 PASS/◎")
    return issues


def check_links():
    issues = []
    for key in ("qmd", "md"):
        base = DOCS[key].parent
        for no, line in enumerate(lines(DOCS[key]), 1):
            for target in re.findall(r"\]\(([^)\s]+)\)", line):
                if target.startswith(("http", "#", "mailto")):
                    continue
                if not (base / target.split("#")[0]).exists():
                    issues.append(f"[断链] {key}:{no} → {target}")
    return issues


def check_database():
    db = ROOT / "DGEF/artifacts/dgef.sqlite"
    con = sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)
    issues = []
    for table, expected in REPORT["row_counts"].items():
        got = con.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]
        if got != expected:
            issues.append(f"[库表漂移] {table}: 库内 {got}，build_report {expected}")
    if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
        issues.append("[库完整性] integrity_check 未通过")
    return issues


def main():
    issues = check_numeric() + check_status_conflicts() + check_links() + check_database()
    unresolved = [i for i in issues if "已裁定" not in i]
    for i in issues:
        print(i)
    print(f"共 {len(issues)} 项提示，未裁定 {len(unresolved)} 项")
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
