"""Read historical verdict code; do not refetch or rerun old adjudications."""
from pathlib import Path
import csv,json,hashlib,collections,re
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new batch'
old=ROOT/'reports/2026-10-07/service_version_review/field_semantics_v10.csv'
a=read(old);b=[dict(r) for r in a];sources={old:sha(old)}
folder=ROOT/'reports/2026-10-04/cross_document_consistency'
adjudication={
 'registry_id':'裁決所指歷史名錄的批次行鍵，不是永久法人根號',
 'registry_name':'该批次名錄展示名稱，非本批重新核實法人名',
 'prior_status':'該裁決批次採用的前置狀態，不能與累積日志的原始基線狀態混用',
 'final_status':'該裁決批次的最終 V/P/U 判定，仍受 note 與證據範圍限制',
 'basis':'該批採用人工或自動判定的依據類型，不直接表示證據品質等級',
 'cited_url':'該批原始引用／請求 URL，可能不同於 evidence_url 或重定向結果',
 'cited_url_http':'原引用 URL 的歷史 HTTP 回應狀態，不單獨證明內容或當前可達性',
 'note':'該裁決的理由、限制與人工補充，不能在僅取狀態時丟棄',
 'supersedes':'該裁決對照的前版 review_batch 標記；僅記有值不證明所有改判均被覆蓋'}
checks={
 'registry_id':'歷史網址檢查所對應的名錄批次行鍵',
 'registry_name':'歷史網址檢查所用展示名，不重新認證法人',
 'http_status':'當時請求取得的 HTTP 狀態；200 不等於主張真實',
 'final_url':'當時請求的重定向後 URL，不保證今日仍相同',
 'title':'從當時響應擷取的頁面標題，可能被截斷，不等於內容核全文',
 'terms_found':'預定詞在當時正文或標題的命中標記，非語義主張獨立驗證',
 'name_terms_found':'由名称及來源基礎導出的詞在當時正文命中，非完整身份消歧',
 'verdict':'原程式按 HTTP、詞命中等產生的歷史分類，V_CONFIRMED 不表示全部產品或性能已核實',
 'error':'當時請求錯誤摘要，可能截斷；空字串不保證內容有效'}
changes=[];summaries=[];seen_tables=set()
for r in b:
    if r['definition_status']!='UNRESOLVED':continue
    name=Path(r['path']).name
    if name=='v_candidate_adjudication.csv':script='adjudicate_v_candidates.py';defs=adjudication
    elif re.fullmatch(r'u_review_batch0[2-6]_adjudication.csv',name):script='adjudicate_batch'+name[14:16]+'.py';defs=adjudication
    elif name=='v_candidate_checks.csv':script='verify_v_candidates.py';defs=checks
    elif re.fullmatch(r'u_review_batch0[2-5]_checks.csv',name):script='verify_url_batch.py';defs=checks
    else:continue
    p=ROOT/r['path'];code=folder/script;assert code.exists(),script
    sources[p]=sha(p);sources[code]=sha(code);assert sha(p)==r['source_sha256']
    c=r['column_name'];assert c in defs,c
    code_lines=code.read_text(encoding='utf-8-sig').splitlines();positions=[i+1 for i,s in enumerate(code_lines) if c in s];assert positions,c
    r['definition']=defs[c];r['definition_status']='CONTEXT_DEFINED_OWNER_REVIEW_REQUIRED'
    r['definition_locator']=code.relative_to(ROOT).as_posix()+':'+str(positions[0])
    changes.append(dict(path=r['path'],column_name=c,definition=defs[c],definition_locator=r['definition_locator'],owner_approval='PENDING',current_facts='NOT_REVERIFIED'))
    if r['path'] not in seen_tables:
        data=read(p);assert len(data)==int(r['row_count']);seen_tables.add(r['path'])
        assert len({x['registry_id'] for x in data})==len(data)
        field='final_status' if 'adjudication' in name else 'verdict'
        summaries.append(dict(path=r['path'],rows=len(data),unique_registry_ids=True,counted_field=field,counts_json=json.dumps(dict(collections.Counter(x[field] for x in data)),ensure_ascii=False)))
assert len(changes)==88,len(changes)
remaining=[r for r in b if r['definition_status']=='UNRESOLVED'];assert len(remaining)==73
for x,y in zip(a,b):
    if x!=y:assert {k for k in x if x[k]!=y[k]}=={'definition','definition_status','definition_locator'}
for p,h in sources.items():assert sha(p)==h
write('field_semantics_v11.csv',b);write('definition_changes.csv',changes);write('remaining_unresolved.csv',remaining);write('historical_status_summary.csv',summaries)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
result=dict(pass_check=True,definitions_added=len(changes),unresolved=73,unchanged_records=1901,tables=len(summaries),source_files_unchanged=len(sources),owner_approval='PENDING',current_facts_verified=False)
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
