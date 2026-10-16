"""Build a searchable delivery index from actual render and fact-check receipts."""
from pathlib import Path
from html import escape
from urllib.parse import quote
import json,collections
OUT=Path(__file__).resolve().parent
results=json.loads((OUT/'results.json').read_text(encoding='utf-8'))
facts=json.loads((OUT/'verified_facts.json').read_text(encoding='utf-8'))['facts']
verdict_counts=collections.Counter(f['status'] for f in facts)
baseline=json.loads((OUT/'before.json').read_text(encoding='utf-8'))
validation=json.loads((OUT/'output_validation.json').read_text(encoding='utf-8'))
links=json.loads((OUT/'delivery_link_repairs.json').read_text(encoding='utf-8'))
unique_mappings=len({(x['document'],e['before'],e['after']) for x in links['changed_documents'] for e in x['edits']})
total=sum(r['path'].lower().endswith('.qmd') for r in baseline['files'])
late=json.loads((OUT/'late_inputs.json').read_text(encoding='utf-8')) if (OUT/'late_inputs.json').exists() else []
late_qmd=sum(r['path'].lower().endswith('.qmd') for r in late)
current_total=total+late_qmd
ok=sum(r['exit_code']==0 and r['html_exists'] for r in results)
table=[]
for r in results:
    path=r['path'];target='rendered/'+str(Path(path).with_suffix('.html')).replace('\\','/')
    state='成功' if r['exit_code']==0 and r['html_exists'] else '失敗'
    warnings='；'.join(r['warnings'])
    table.append(f'<tr data-state="{state}"><td><a href="{quote(target,safe="/")}">{escape(path)}</a></td>'
                 f'<td>{state}</td><td>{escape(r.get("renderer","Quarto HTML；停用程式碼執行"))}</td>'
                 f'<td>{escape(warnings)}</td></tr>')
fact_rows=''.join(f'<tr><td>{f["id"]}</td><td>{escape(f["claim"])}</td><td>{f["status"]}</td>'
                  f'<td><a href="{escape(f["source"],quote=True)}">一手來源</a><br>{escape(f["boundary"])}</td></tr>' for f in facts)
page='''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>全項目 QMD 渲染與事實查證台帳 · 2026-10-15</title>
<style>body{font:16px/1.65 system-ui,sans-serif;max-width:1500px;margin:auto;padding:32px;color:#182b3a}h1{font-size:28px}table{width:100%;border-collapse:collapse;font-size:14px}th,td{padding:10px;border:1px solid #ced8df;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#edf3f6}a{color:#075eae}input,select{font:inherit;padding:8px;margin:12px 8px 16px 0}input{width:min(600px,70%)}.notice{border-left:5px solid #b87213;background:#fff5e4;padding:16px}.count{font-size:22px;font-weight:700}</style>
<h1>全項目 QMD 渲染與事實查證台帳</h1><p>2026-10-15 · 所有原有 QMD；正式稿、歷史稿、預覽稿與網頁快照一併列入。</p>
'''
page+=f'<p class="count">已成功渲染 {ok} / {current_total} 份；原基線 {total} 份，工作期間新增 {late_qmd} 份。</p>'
ledger=json.loads((OUT/'verified_facts.json').read_text(encoding='utf-8'))
page+=f'<p>最近外部事實續核日期：{escape(ledger.get("last_updated",ledger.get("checked_on","")))}。</p>'
if (OUT/'rendered_passages_20261016_manifest.json').exists():
    page+='<p><a href="rendered_passages_20261016_manifest.json">含 HTML 快照的閱讀版段落清單</a> · <a href="rendered_passages_20261016.jsonl.gz">壓縮段落資料</a>。這些段落全部標為待審文字，不是已核實數量，也不是完整原子主張清單。</p>'
page+=f'<p>新生成 HTML 已記錄 {unique_mappings} 組不重複的本地導覽修復映射；仍有 {len(links["unresolved_links"])} 處原始引用未找到目標。映射以文件、原引用與新引用去重，避免重新渲染後重複計數。詳見 <a href="delivery_link_repairs.json">引用修復與缺口台帳</a>。資料附件連回同一工作區的原文件，交付目錄不是可任意搬移的獨立資料包。</p>'
page+=f'''<div class="notice"><strong>外部事實逐條查證尚未完成。</strong>本輪對照一手來源的具體主張共 {len(facts)} 項：{verdict_counts['SUPPORTED']} 項在限定範圍獲支持、{verdict_counts['CONTRADICTED']} 項與所讀來源矛盾、{verdict_counts['INSUFFICIENT_EVIDENCE']} 項證據不足。18,272 段候選文字與 5,067 個網址是初步抽取清單，並非已核實事實數量，亦非完整原子主張清單。渲染成功只表示對應模式產生 HTML，不代表事實正確、程式碼可執行、所有遠端資源可離線使用或已完成視覺驗收。</div>
<p>原有 HTML 與資產保留；Quarto 輸出使用停用計算、保留外部依賴的 HTML 交付模式。純 HTML 快照直接保留原 HTML；帶 Markdown 增補的快照另行渲染增補段並插入頁面。Windows 長路徑文件使用短暫存路徑。查證增補與快照模式修正逐項記錄於 <a href="source_changes.json">源文件變更台帳</a>。</p>
<p>資源限制：三份歷史網頁快照有 15 個未隨原快照保存的腳本、樣式或圖示參照。兩份 Swagger 頁已補入離線可讀的接口索引；嫦娥五號頁面保留正文，但原站版式不能保證。沒有把外部資源缺失當作正文或外部事實已驗收。</p>
<p><a href="results.json">逐文件結果</a> · <a href="output_validation.json">輸出與資源檢查</a> · <a href="before.json">渲染前基線</a> · <a href="after_delta.json">源文件差異</a> · <a href="fact_candidates.json">候選文字</a> · <a href="external_urls.json">網址清單</a> · <a href="verified_facts.json">具體查證證據</a></p>
<h2>文件索引</h2><input id="search" placeholder="搜尋路徑、檔名或警告"><select id="state"><option value="">全部結果</option><option>成功</option><option>失敗</option></select>
<table id="documents"><thead><tr><th>文件／HTML 閱讀版</th><th>結果</th><th>渲染方式</th><th>警告</th></tr></thead><tbody>'''
page+=''.join(table)+'</tbody></table><h2>已逐項對照來源的主張</h2><table><thead><tr><th>編號</th><th>具體主張</th><th>裁決</th><th>來源與邊界</th></tr></thead><tbody>'+fact_rows+'</tbody></table>'
if (OUT/'current_acceptance.json').exists():
    page+='<p>最新重新掃描及驗收：<a href="current_acceptance.json">現行驗收回執</a> · <a href="rescan_diagnostics.json">格式與渲染一致性診斷</a> · <a href="rescan_candidate_dispositions.json">診斷候選判讀</a>。首輪 final_acceptance.json 為歷史回執。本輪以使用者最新提交 d1f93f3 為基準，保留其《冊二》及原 HTML 更新。</p>'
page+='''<script>const search=document.querySelector('#search'),state=document.querySelector('#state');function filter(){for(const row of document.querySelectorAll('#documents tbody tr'))row.hidden=!(row.textContent.toLowerCase().includes(search.value.toLowerCase())&&(!state.value||row.dataset.state===state.value));}search.addEventListener('input',filter);state.addEventListener('change',filter);</script></html>'''
(OUT/'index.html').write_text(page,encoding='utf-8')
summary=dict(original_qmd_count=total,late_added_qmd_count=late_qmd,current_qmd_count=current_total,recorded=len(results),successful=ok,failed=len(results)-ok,
             external_fact_checks=len(facts),external_fact_check_complete=False,
             external_fact_status_counts=dict(verdict_counts),
             missing_historical_resource_references=len(validation['missing_dependencies']),
             repaired_local_links=sum(len(x['edits']) for x in links['changed_documents']),
             repaired_local_links_metric='Cumulative repair operations, including repeated repairs after re-render; not unique occurrences',
             unique_navigation_repair_mappings=unique_mappings,
             unresolved_local_link_occurrences=len(links['unresolved_links']),
             scope='HTML rendering with code execution disabled; external fact verification remains incomplete')
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary))
