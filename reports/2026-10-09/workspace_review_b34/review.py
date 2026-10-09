from pathlib import Path
import json,csv,subprocess,hashlib,collections
O=Path(__file__).resolve().parent;R=O.parents[2]
S=R/'reports/2026-10-06/workspace_change_audit'
summary=json.loads((S/'review_b34_20261009_summary.json').read_text(encoding='utf-8'))
before=json.loads((R/'reports/2026-10-09/weather_spatial_b33/baseline.json').read_text(encoding='utf-8'))
rows=[]
for p,h in before['protected'].items():
    f=R/p;rows.append(dict(path=p,status='MISSING' if not f.exists() else 'UNCHANGED' if hashlib.sha256(f.read_bytes()).hexdigest()==h else 'MODIFIED',sha256_current=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else ''))
with (O/'protected_comparison.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
targets=['附錄_提問卌核校與開源生態變現_20261009.qmd','registry_license_audit_20261009.csv']
inventory=list(csv.DictReader((S/'review_b34_20261009_files.csv').open(encoding='utf-8-sig')))
referenced={n:[r['path'] for r in inventory if Path(r['path']).name==n] for n in targets}
diff=subprocess.check_output(['git','diff','--unified=0','6a7a83a','HEAD','--','Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd']).decode('utf-8')
removed=[s[1:] for s in diff.splitlines() if s.startswith('-') and not s.startswith('---')]
assert len(removed)==7 and all(s.startswith('### ') for s in removed)
current=(R/'Reference/Inteligent_egaming_platform_ref_v000.000.001.qmd').read_text(encoding='utf-8-sig')
restored_headers={h:current.count(h) for h in removed}
stats=dict(head=summary['head'],compared_to='6a7a83a',files_hashed=summary['regular_files_hashed'],bytes_hashed=summary['bytes_hashed'],unreadable=summary['skipped'],unstable=summary['unstable_files'],referenced_deliverables=referenced,removed_lines=removed,current_header_occurrences=restored_headers,protected_comparison=rows,scope='File inventory plus committed-change review, not independent verification of every factual claim')
(O/'validation_receipt.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
report='''---
title: "B34：施工前全項目變動核對與續作定位"
date: 2026-10-09
format:
  html:
    toc: true
    embed-resources: true
---

## 已確認的變動

B33提交 `6a7a83a` 後，使用者提交 `b679168`、`ccf3b73`。本輪開始時Git工作區乾淨，但現行內容已有實質改動。相較B33，Inteligent報告新增2731行、刪除7行；weather.com盤點新建251行。沒有Git追蹤文件刪除。兩份宇航／地緣主報告及v2.3.0交接文件的本地指紋與B33保護基線一致；Inteligent內容已改，後續不得套用舊正文覆寫。

七條刪除行均為模型解答標題（Kimi、Perplexity、Grok、深度求索、Gemini、Copilot、Meta AI），現行文件仍含這些標題。這只確認標題移動或重組，不能憑此宣稱所有原有信息已完成逐句無損驗證。

## 全項目快照與限制

已雜湊8018個普通文件，其中7675個Git追蹤文件，共4245260485位元組；未發現掃描期间不穩定文件。含忽略文件，排除Git內部與符號連結。四處因權限無法讀取：RStudio會話lock_file，以及B08 local_runtime的bin、xlrd、xlrd-2.0.2.dist-info。這是可讀文件版本清點，不是每個文件內容的實質真偽驗證。掃描器的舊before比較是歷史基線；本輪近期Git差異以6a7a83a為起點，不混淆兩種時段。

`Untitled.qmd` 現已不存在，亦未見本輪Git追蹤刪除；它在B33時為未追蹤文件。保留此差異記錄，不自動恢復。

## 影響後續工作的內容

新增內容包括提問卌授權與變現附錄、weather.com生態比較、果敢／緬甸實體和多模型回答、商業路徑及尺度論述。原文中的其他模型自述「核實」「交付」不是本輪驗收證據，保留為來源陳述。

兩個被正文稱為已交付的獨立文件 `附錄_提問卌核校與開源生態變現_20261009.qmd`、`registry_license_audit_20261009.csv` 未在本次可讀文件清單中找到。附錄內容已內嵌於Inteligent，不能把獨立附件未找到誤寫成內嵌內容丟失；34條授權審計的独立CSV仍待取得／重建核證。

正文的「不存在」「必死」「全部無缺漏」、價格、客戶、所有權、產品生命週期及授權法律結論尚未由本輪外部逐項查證。不將無公開證據升格成不存在，也不以市場假設當作已成交價。維持來源、時間、實體範圍和UNKNOWN分層。

## 已接續的施工定位

1. 保留使用者两次提交及weather.com原文，建立新施工基線。
2. 續作氣象B33新站的單位／缺值／窗口／位置覆核；現有11163條來源日摘要不回填零。
3. 另開來源主張核證清單，優先核查weather.com定價與覆蓋、產品生命周期、法人及授權；查證後用有界增補，未核實之前不改原文。
4. 金融2608項、六項工商查詢及歷史缺口保留；SDG業務分析繼續凍結，不重啟受限系統。

[全文件快照](../reports/2026-10-06/workspace_change_audit/review_b34_20261009_files.csv)、[近期提交差異](../reports/2026-10-06/workspace_change_audit/review_b34_20261009_committed_changes.csv)、[保護文件比較](../reports/2026-10-09/workspace_review_b34/protected_comparison.csv)、[驗收與讀取限制](../reports/2026-10-09/workspace_review_b34/validation_receipt.json)。
'''
(R/'Reference/Workspace_Review_B34_20261009.qmd').write_text(report,encoding='utf-8')
for n in ['redteam','critic','killcritic','blindspot','blueprint','cheatsheet','actionplan']:
    (R/n/'workspace_review_b34_20261009.md').write_text('# '+n+'｜B34施工前變動核查\n\n已核對8018份可讀文件及使用者兩次提交；保留原文，4處權限讀取限制明列。正文自述交付不等於附件存在，缺證不等於不存在；下一輪先核新站品質，再獨立核市場／授權主張。\n\n[核對報告](../Reference/Workspace_Review_B34_20261009.qmd)。\n',encoding='utf-8')
print(json.dumps(dict(referenced=referenced,protected=rows),ensure_ascii=False))
