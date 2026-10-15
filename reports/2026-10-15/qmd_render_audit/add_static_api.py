"""Add readable historical API indexes to snapshots whose UI assets are absent."""
from pathlib import Path
import json,hashlib,re
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
changes=json.loads((OUT/'source_changes.json').read_text(encoding='utf-8'))
baseline={r['path']:r for r in json.loads((OUT/'before.json').read_text(encoding='utf-8'))['files']}
counts=[]
for stem in ('twse','tpex'):
    base=ROOT/'reports/2026-10-07/financial_universe_b06/raw'
    specpath=base/(stem+'_swagger.json');spec=json.loads(specpath.read_text(encoding='utf-8-sig'))
    qmd=base/(stem+'_openapi.qmd');rel=qmd.relative_to(ROOT).as_posix();old=qmd.read_bytes()
    rs=[]
    for route,ops in spec.get('paths',{}).items():
        for method,op in ops.items():
            if method not in {'get','put','post','delete','options','head','patch','trace'}:continue
            def esc(v):return str(v).replace('|','&#124;').replace('\n',' ').replace('\r',' ')
            rs.append('| '+method.upper()+' | `'+route+'` | '+esc(op.get('summary',''))+' | '+esc(', '.join(op.get('tags',[])))+' |')
    url=('https://'+spec['host']+spec.get('basePath','')) if 'host' in spec else spec['servers'][0]['url']
    title=spec.get('info',{}).get('title',stem.upper())
    if b'<!-- STATIC_API_APPENDIX_20261015 -->' not in old:
        note='\n\n<!-- STATIC_API_APPENDIX_20261015 -->\n\n# '+title+'：離線端點索引\n\n原 HTML 是 Swagger UI 的頁面殼，所需腳本及樣式沒有隨該快照保存；單純還原 HTML 不會顯示 API 清單。本節直接從同批保存的 `'+specpath.name+'` 產生靜態索引，離線閱讀不依賴 Swagger JavaScript。\n\n這是歷史批次的接口規格，不代表本輪已重新呼叫全部端點，也不是最新公司名冊、證券普查或交易資料。方法及路徑按保存的 JSON 原樣列示，錯誤回應、授權、資料時效和現行可用性仍須逐端點核實。\n\n- 保存規格 SHA256：`'+hashlib.sha256(specpath.read_bytes()).hexdigest()+'`\n- 規格基址：['+url+']('+url+')\n- 本地規格記錄：'+str(len(rs))+' 個 HTTP 方法／路徑組合。\n\n| 方法 | 路徑 | 規格摘要 | 分類 |\n|---|---|---|---|\n'+'\n'.join(rs)+'\n'
        new=old.replace(b'recovery-kind: lossless-html-snapshot',b'recovery-kind: html-snapshot-with-markdown-appendix',1)
        new=re.sub(rb'<!-- Byte-exact renderer:.*?-->',b'<!-- Renderer: reports/2026-10-15/qmd_render_audit/audit_render.py. Render the preserved snapshot and its static Markdown appendix together. -->',new,count=1)
        new+=note.encode('utf-8');h=hashlib.sha256(old).hexdigest()
        (OUT/'original_bytes'/(h+'.bin')).write_bytes(old);qmd.write_bytes(new)
    if not any(r['path']==rel for r in changes):
        changes.append(dict(path=rel,before_sha256=baseline[rel]['sha256'],after_sha256=hashlib.sha256(qmd.read_bytes()).hexdigest(),
            change='Preserve snapshot HTML; add offline endpoint index from existing same-batch Swagger JSON; correct renderer metadata'))
    counts.append(dict(path=rel,http_method_path_pairs=len(rs),source_spec=specpath.relative_to(ROOT).as_posix(),
                       source_spec_sha256=hashlib.sha256(specpath.read_bytes()).hexdigest()))
(OUT/'source_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'static_api_receipt.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(counts,ensure_ascii=True))
