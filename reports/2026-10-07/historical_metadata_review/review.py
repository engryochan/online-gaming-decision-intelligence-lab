"""Complete contextual metadata proposals, retaining each original catalogue cell."""
from pathlib import Path
import csv,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
csv.field_size_limit(16*1024*1024)
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert not (OUT/'validation.json').exists(),'Use a new batch'
old=ROOT/'reports/2026-10-07/adjudication_field_review/field_semantics_v11.csv'
a=read(old);b=[dict(r) for r in a];sources={old:sha(old)}
defs={
 'registry_id':'歷史名錄批次行鍵，不能直接當永久法人鍵',
 'registry_name':'歷史名錄展示名稱，未重新消歧',
 'registry_status':'對照時讀取的名錄狀態，非今日認證',
 'registry_status_after_batch01':'採用第一批提案後的對照狀態，與原名錄狀態分開',
 'doc_entry':'原文名錄条目編號，非全項目共用鍵',
 'doc_marks':'原文條目符號標記；不能自動等價 V/P/U',
 'doc_line':'對照時文本的行號，後續編輯可能移動',
 'relation':'名錄狀態與原文符號的程式對照分類，不是機構業務關係',
 'doc_source_url':'原文可配對的引用 URL，非本批即時核實',
 'doc_source_line':'原文引用定位行號，受歷史文本版本限定',
 'doc_source_basis':'原文來源匹配的文字基礎，不能擴張證據範圍',
 'proposal':'狀態／標記一致性處理提案，非已執行改判',
 'id':'所屬批次的名錄行鍵，非永久實體根號',
 'name':'所屬種子／審阅／抽取批次的展示名稱，非法人認證',
 'prior_status':'本批提案前的歷史狀態',
 'proposed_status':'本批建議狀態，與後續採納及今日有效性分開',
 'finding':'本批審阅發現摘要，須保留證據與限制',
 'secondary_url':'補充來源 URL，不單獨代表主來源或現行可達性',
 'evidence_type':'當批證據來源性質標記，非完整品質評分',
 'limits':'當批判定限制，不得在聚合中省略',
 'terms':'供 URL 檢查的預定匹配詞，竪線分隔；命中不等於语義主張核實',
 'table':'覆蓋對賬所指的實體表名',
 'name_zh':'覆蓋對賬中的表中文名稱',
 'grain':'覆蓋對賬采用的表記錄粒度',
 'records':'生成該歷史對賬時的表行數，非今日數量或機構總數',
 'status':'本歷史表的局部狀態／施工標記；不同表不可混用',
 'source_route':'對賬說明的來源追溯路徑，不表示所有來源已接入',
 'gap_reason':'對賬記錄的資料缺口或非窮盡限制',
 'old_path':'分類搬移前的工作區相對路徑，不強制恢復原位置',
 'new_path':'該次分類搬移的目標路徑，後續改名需另按版本定位',
 'category':'本表用途下的編輯分類；不是事實核實等級',
 'moved':'歷史分類记录的搬移標記，非本批執行動作',
 'aliases':'種子匹配用的名稱／別名清單，竪線分隔，不完成實體合併',
 'role':'種子清單的編輯用途／角色，非性能認證',
 'number':'原文抽取的條目序號，非永久實體根號',
 'original_description':'原文表格說明文字的抽取，不代表本批認可內容',
 'path':'本表用途所引用的歷史文件路徑；需按版本與搬移映射定位',
 'line':'來源抽取文本的行號；不保證當前文件相同行仍對應',
 'label':'原文條目的展示標籤，未重新消歧',
 'boundary':'原文條目附帶的範圍／限制文字，須與主張合讀',
 'context':'名稱匹配的歷史局部上下文，不等於完整原文',
 'key':'歷史人工／來源核查的名稱匹配鍵，不是全局主鍵',
 'lines':'歷史抽取文本行數，非文件內容已實質核查程度',
 'review_method':'歷史讀取／抽取方法及成功失敗說明，不等於事實核實完成',
 'state':'兩次 B03 快照的 ADDED／REMOVED／MODIFIED 比較結果，不推定改動原因',
 'before_sha256':'前次工作區快照內容指紋；未有該文件時空值',
 'after_sha256':'後次工作區快照內容指紋；後次沒有該文件時空值',
}
code_map={
 'mark_crosswalk.csv':'reports/2026-10-04/cross_document_consistency/build_mark_crosswalk.py',
 'gaming_70_entries.csv':'reports/2026-10-04/build_catalogue.py',
 'original_172_entries.csv':'reports/2026-10-04/build_catalogue.py',
 'entity_source_evidence.csv':'reports/2026-10-04/build_catalogue.py',
 'source_urls.csv':'reports/2026-10-04/audit_project.py',
 'file_inventory.csv':'reports/2026-10-04/audit_project.py',
 'workspace_delta.csv':'reports/2026-10-06/global_technology_iso249_b03/audit_delta.py'}
changes=[]
for r in b:
    if r['definition_status']!='UNRESOLVED':continue
    assert r['role']=='HISTORICAL_REPORT_OUTPUT'
    p=ROOT/r['path'];sources[p]=sha(p);assert sha(p)==r['source_sha256'];c=r['column_name'];assert c in defs,c
    definition=defs[c]
    if p.name=='workspace_delta.csv' and c=='category':definition='B03 交付／運行時變更的粗分類；按路徑生成，不證明改動因果'
    if p.name=='live_checks.tsv' and c=='status':definition='歷史種子核查的 V/P/U 等狀態，须与范围及日期合讀'
    code=code_map.get(p.name)
    if '/dgef/tables/coverage/' in r['path']:code='DGEF/report_public_ingestion.py'
    if '/table_reclassification/' in r['path']:code='DGEF/reclassify_tables.py'
    locator=r['path']+':1; historical header and row context; proposed'
    if code:
        q=ROOT/code;sources[q]=sha(q);lines=q.read_text(encoding='utf-8-sig').splitlines();positions=[i+1 for i,s in enumerate(lines) if c in s]
        if positions:locator=code+':'+str(positions[0])
    r['definition']=definition;r['definition_status']='PROPOSED_HISTORICAL_CONTEXT_REVIEW';r['definition_locator']=locator
    changes.append(dict(path=r['path'],column_name=c,definition=definition,definition_locator=locator,owner_approval='PENDING',facts_verified='NOT_REVERIFIED'))
assert len(changes)==73
assert len(a)==len(b)==1989
assert sum(x!=y for x,y in zip(a,b))==73
for x,y in zip(a,b):
    if x!=y:assert {k for k in x if x[k]!=y[k]}=={'definition','definition_status','definition_locator'}
assert not any(r['definition_status']=='UNRESOLVED' for r in b)
for p,h in sources.items():assert sha(p)==h
write('field_semantics_v12.csv',b);write('definition_changes.csv',changes)
write('source_manifest.csv',[dict(path=p.relative_to(ROOT).as_posix(),sha256=h) for p,h in sources.items()])
counts=collections.Counter(r['definition_status'] for r in b)
write('definition_status_summary.csv',[dict(status=k,records=v) for k,v in sorted(counts.items())])
result=dict(pass_check=True,definitions_added=73,unchanged_records=1916,unresolved=0,records=1989,status_counts=dict(counts),source_files_unchanged=len(sources),business_approval='PENDING',all_facts_verified=False)
(OUT/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
