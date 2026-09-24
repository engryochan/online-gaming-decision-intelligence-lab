#!/usr/bin/env python3
"""
OGDIL v0.2 项目生成器
生成 online-gaming-decision-intelligence-lab 的目录骨架与基础配置文件。

说明：
本脚本此前存在未闭合的三引号字符串（files["README.md"] 未结束），
导致文件无法通过 Python 语法检查，实际上从未能被执行。

修复时同时收窄了本脚本的职责范围：仅负责生成【目录结构】与【纯配置类文件】
（.gitignore / .editorconfig）。README.md、CONTRIBUTING.md、CHANGELOG.md、
ROADMAP.md 等文档内容不再由本脚本硬编码生成——这些文件目前已经存在于仓库中，
并且是被直接维护的"唯一来源"；如果继续把文档正文复制一份到本脚本里，会与
scripts/metadata/bootstrap_metadata_governance.py 犯下同样的问题：脚本里的
硬编码内容会在重新运行时无提示覆盖掉手工维护过的正文。

因此本脚本改为幂等（idempotent）：目录始终确保存在，但对于已存在的文件
一律跳过，不会覆盖。
"""

from pathlib import Path

# 基础目录（相对于当前工作目录）
BASE = Path("online-gaming-decision-intelligence-lab")

# ---------- 目录结构 ----------
directories = [
    "docs/01_Project",
    "docs/02_Architecture",
    "docs/03_Data_Dictionary",
    "docs/04_Research",
    "sql/ods",
    "sql/dwd",
    "sql/dws",
    "sql/ads",
    "sql/etl",
    "sql/quality",
    "R/R",
    "R/man",
    "R/tests",
    "python/src/ogdil",
    "python/tests",
    "dashboards",
    "experiments",
    "feature_store",
    "models",
    "notebooks",
    "tests",
    "deployment",
    "docker",
    "website",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
]

# ---------- 纯配置文件（非文档正文，可安全由脚本管理） ----------
files = {}

files[".gitignore"] = """# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
.venv/
*.egg-info/
dist/
build/

# R
.Rproj.user
.Rhistory
.RData
.Ruserdata
*.Rproj

# IDE
.vscode/
.idea/
*.swp
*.swo

# 操作系统
.DS_Store
Thumbs.db

# 项目专属
*.log
*.tmp
data/
output/
"""

files[".editorconfig"] = """root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{md,yml,yaml}]
indent_size = 2

[*.{R,r}]
indent_size = 2

[*.py]
indent_size = 4
"""


def 主程序() -> None:
    BASE.mkdir(exist_ok=True)

    for 相对路径 in directories:
        (BASE / 相对路径).mkdir(parents=True, exist_ok=True)
    print(f"目录骨架已确认（共 {len(directories)} 个目录）。")

    for 相对路径, 内容 in files.items():
        目标路径 = BASE / 相对路径
        if 目标路径.exists():
            print(f"已存在，跳过：{相对路径}")
            continue
        目标路径.parent.mkdir(parents=True, exist_ok=True)
        目标路径.write_text(内容, encoding="utf-8")
        print(f"已生成：{相对路径}")

    print("")
    print("骨架生成完成（README / CONTRIBUTING / CHANGELOG / ROADMAP 等文档请直接编辑对应文件，不经由本脚本生成）。")


if __name__ == "__main__":
    主程序()
